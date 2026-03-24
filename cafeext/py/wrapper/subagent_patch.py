"""增强型子代理补丁 (Subagent Extension Patch)。
扩展 spawn 工具以支持 model 和 images 参数，实现多模态委派。
"""

import json
import base64
from pathlib import Path
from typing import Any, Optional, List
from loguru import logger

def apply_subagent_patch():
    try:
        # 1. 拦截 SpawnTool
        from nanobot.agent.tools.spawn import SpawnTool
        
        # 更新参数定义
        @property
        def patched_parameters(self) -> dict[str, Any]:
            return {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "需要子代理完成的任务描述。",
                    },
                    "model": {
                        "type": "string",
                        "description": "可选：指定子代理使用的模型（如针对图片的 Qwen3.5-35B-A3B）。",
                    },
                    "images": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "可选：图片文件路径或 URL 列表，用于多模态识别。",
                    },
                    "label": {
                        "type": "string",
                        "description": "可选：任务的简短标签。",
                    },
                },
                "required": ["task"],
            }
        
        @property
        def patched_description(self) -> str:
            return (
                "开启一个后台子代理来处理任务。支持通过 'model' 指定特定模型，"
                "并通过 'images' 传递图片进行多模态分析。子代理完成后会向主代理汇报。"
            )

        async def patched_execute(self, task: str, model: Optional[str] = None, images: Optional[List[str]] = None, label: Optional[str] = None, **kwargs: Any) -> str:
            return await self._manager.spawn(
                task=task,
                model=model,
                images=images,
                label=label,
                origin_channel=self._origin_channel,
                origin_chat_id=self._origin_chat_id,
                session_key=self._session_key,
            )

        SpawnTool.parameters = patched_parameters
        SpawnTool.description = patched_description
        SpawnTool.execute = patched_execute

        # 2. 拦截 SubagentManager
        from nanobot.agent.subagent import SubagentManager
        import uuid
        import asyncio
        from nanobot.utils.helpers import detect_image_mime

        # 更新 spawn 方法接收新参数
        async def patched_spawn(
            self,
            task: str,
            model: Optional[str] = None,
            images: Optional[List[str]] = None,
            label: Optional[str] = None,
            origin_channel: str = "cli",
            origin_chat_id: str = "direct",
            session_key: str | None = None,
        ) -> str:
            task_id = str(uuid.uuid4())[:8]
            display_label = label or task[:30] + ("..." if len(task) > 30 else "")
            origin = {"channel": origin_channel, "chat_id": origin_chat_id}

            # 将新参数传递给内部运行方法
            bg_task = asyncio.create_task(
                self._run_subagent(task_id, task, display_label, origin, model=model, images=images)
            )
            self._running_tasks[task_id] = bg_task
            if session_key:
                self._session_tasks.setdefault(session_key, set()).add(task_id)

            def _cleanup(_: asyncio.Task) -> None:
                self._running_tasks.pop(task_id, None)
                if session_key and (ids := self._session_tasks.get(session_key)):
                    ids.discard(task_id)
                    if not ids:
                        del self._session_tasks[session_key]

            bg_task.add_done_callback(_cleanup)
            logger.info("Spawned extended subagent [{}]: {} (model: {})", task_id, display_label, model or "default")
            return f"Subagent [{display_label}] started (id: {task_id}). I'll notify you when it completes."

        # 重写核心运行逻辑以支持多模态
        async def patched_run_subagent(
            self,
            task_id: str,
            task: str,
            label: str,
            origin: dict[str, str],
            model: Optional[str] = None,
            images: Optional[List[str]] = None,
        ) -> None:
            logger.info("Subagent [{}] starting task: {}", task_id, label)
            try:
                from nanobot.agent.tools.registry import ToolRegistry
                from nanobot.agent.tools.filesystem import ReadFileTool, WriteFileTool, EditFileTool, ListDirTool
                from nanobot.agent.tools.shell import ExecTool
                from nanobot.agent.tools.web import WebSearchTool, WebFetchTool
                from nanobot.agent.skills import BUILTIN_SKILLS_DIR
                from nanobot.utils.helpers import build_assistant_message

                # 初始化工具
                tools = ToolRegistry()
                allowed_dir = self.workspace if self.restrict_to_workspace else None
                extra_read = [BUILTIN_SKILLS_DIR] if allowed_dir else None
                # 注意：这里我们使用了原始类名，因为 SubagentManager 的 init 里也是这么写的
                tools.register(ReadFileTool(workspace=self.workspace, allowed_dir=allowed_dir, extra_allowed_dirs=extra_read))
                tools.register(WriteFileTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(EditFileTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(ListDirTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(ExecTool(
                    working_dir=str(self.workspace),
                    timeout=self.exec_config.timeout,
                    restrict_to_workspace=self.restrict_to_workspace,
                    path_append=self.exec_config.path_append,
                ))
                tools.register(WebSearchTool(config=self.web_search_config, proxy=self.web_proxy))
                tools.register(WebFetchTool(proxy=self.web_proxy))
                
                system_prompt = self._build_subagent_prompt()
                
                # --- 多模态消息构造 ---
                user_content = [{"type": "text", "text": task}]
                if images:
                    for img_path in images:
                        if img_path.startswith(("http://", "https://")):
                            user_content.append({"type": "image_url", "image_url": {"url": img_path}})
                        else:
                            # 处理本地文件
                            p = Path(img_path)
                            if not p.is_absolute():
                                p = self.workspace / p
                            if p.exists():
                                data = p.read_bytes()
                                mime = detect_image_mime(data) or "image/jpeg"
                                b64 = base64.b64encode(data).decode("utf-8")
                                user_content.append({
                                    "type": "image_url", 
                                    "image_url": {"url": f"data:{mime};base64,{b64}"},
                                    "_meta": {"path": str(p)} # 方便审计日志记录路径
                                })
                            else:
                                logger.warning("Subagent image path not found: {}", img_path)

                messages: list[dict[str, Any]] = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ]

                # 使用指定模型或默认模型
                target_model = model or self.model
                
                max_iterations = 15
                iteration = 0
                final_result: str | None = None

                while iteration < max_iterations:
                    iteration += 1
                    response = await self.provider.chat_with_retry(
                        messages=messages,
                        tools=tools.get_definitions(),
                        model=target_model,
                    )

                    if response.has_tool_calls:
                        tool_call_dicts = [tc.to_openai_tool_call() for tc in response.tool_calls]
                        messages.append(build_assistant_message(
                            response.content or "",
                            tool_calls=tool_call_dicts,
                            reasoning_content=response.reasoning_content,
                            thinking_blocks=response.thinking_blocks,
                        ))
                        for tool_call in response.tool_calls:
                            result = await tools.execute(tool_call.name, tool_call.arguments)
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_call.name,
                                "content": result,
                            })
                    else:
                        final_result = response.content
                        break

                if final_result is None:
                    final_result = "Task completed but no final response was generated."

                await self._announce_result(task_id, label, task, final_result, origin, "ok")

            except Exception as e:
                logger.error("Subagent [{}] failed: {}", task_id, e)
                await self._announce_result(task_id, label, task, f"Error: {str(e)}", origin, "error")

        SubagentManager.spawn = patched_spawn
        SubagentManager._run_subagent = patched_run_subagent

    except Exception as e:
        logger.error("Failed to apply extended subagent patch: {}", e)
