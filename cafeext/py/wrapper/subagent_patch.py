"""增强型子代理补丁 (Subagent Extension Patch)。
适配 nanobot v0.1.5+ 的 AgentRunner 架构，并支持 model 和 images 参数实现多模态委派。
"""

import json
import base64
import asyncio
import uuid
from pathlib import Path
from typing import Any, Optional, List
from loguru import logger
from functools import wraps

def apply_subagent_patch():
    try:
        # 1. 拦截 SpawnTool
        from nanobot.agent.tools.spawn import SpawnTool
        
        # 扩展参数定义以支持 model 和 images
        SpawnTool._parameters = {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "需要子代理完成的任务描述。",
                },
                "model": {
                    "type": "string",
                    "description": "可选：指定子代理使用的模型。",
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
        
        SpawnTool.description = (
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

        SpawnTool.execute = patched_execute

        # 2. 拦截 SubagentManager
        from nanobot.agent.subagent import SubagentManager, SubagentStatus
        from nanobot.utils.helpers import detect_image_mime

        # 更新 spawn 方法接收新参数，并兼容 SubagentStatus
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
            import time
            task_id = str(uuid.uuid4())[:8]
            display_label = label or task[:30] + ("..." if len(task) > 30 else "")
            origin = {"channel": origin_channel, "chat_id": origin_chat_id, "session_key": session_key}

            # 兼容上游的状态对象
            status = SubagentStatus(
                task_id=task_id,
                label=display_label,
                task_description=task,
                started_at=time.monotonic(),
            )
            self._task_statuses[task_id] = status

            # 将新参数传递给内部运行方法
            bg_task = asyncio.create_task(
                self._run_subagent(task_id, task, display_label, origin, status, model=model, images=images)
            )
            self._running_tasks[task_id] = bg_task
            if session_key:
                self._session_tasks.setdefault(session_key, set()).add(task_id)

            def _cleanup(_: asyncio.Task) -> None:
                self._running_tasks.pop(task_id, None)
                self._task_statuses.pop(task_id, None) # 确保状态也被清理
                if session_key and (ids := self._session_tasks.get(session_key)):
                    ids.discard(task_id)
                    if not ids:
                        del self._session_tasks[session_key]

            bg_task.add_done_callback(_cleanup)
            logger.info("Spawned extended subagent [{}]: {} (model: {})", task_id, display_label, model or "default")
            return f"Subagent [{display_label}] started (id: {task_id}). I'll notify you when it completes."

        # 重写核心运行逻辑以支持多模态和 AgentRunner
        async def patched_run_subagent(
            self,
            task_id: str,
            task: str,
            label: str,
            origin: dict[str, str],
            status: SubagentStatus,
            model: Optional[str] = None,
            images: Optional[List[str]] = None,
        ) -> None:
            import time
            logger.info("Subagent [{}] starting task: {}", task_id, label)
            
            async def _on_checkpoint(payload: dict) -> None:
                status.phase = payload.get("phase", status.phase)
                status.iteration = payload.get("iteration", status.iteration)

            try:
                from nanobot.agent.tools.registry import ToolRegistry
                from nanobot.agent.tools.filesystem import ReadFileTool, WriteFileTool, EditFileTool, ListDirTool
                from nanobot.agent.tools.shell import ExecTool
                from nanobot.agent.tools.web import WebSearchTool, WebFetchTool
                from nanobot.agent.tools.search import GlobTool, GrepTool
                from nanobot.agent.skills import BUILTIN_SKILLS_DIR
                from nanobot.agent.runner import AgentRunSpec
                from nanobot.agent.subagent import _SubagentHook

                # 1. 初始化工具
                tools = ToolRegistry()
                allowed_dir = self.workspace if (self.restrict_to_workspace or self.exec_config.sandbox) else None
                extra_read = [BUILTIN_SKILLS_DIR] if allowed_dir else None
                
                tools.register(ReadFileTool(workspace=self.workspace, allowed_dir=allowed_dir, extra_allowed_dirs=extra_read))
                tools.register(WriteFileTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(EditFileTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(ListDirTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(GlobTool(workspace=self.workspace, allowed_dir=allowed_dir))
                tools.register(GrepTool(workspace=self.workspace, allowed_dir=allowed_dir))
                
                if self.exec_config.enable:
                    tools.register(ExecTool(
                        working_dir=str(self.workspace),
                        timeout=self.exec_config.timeout,
                        restrict_to_workspace=self.restrict_to_workspace,
                        sandbox=self.exec_config.sandbox,
                        path_append=self.exec_config.path_append,
                        allowed_env_keys=self.exec_config.allowed_env_keys,
                    ))
                if self.web_config.enable:
                    tools.register(WebSearchTool(config=self.web_config.search, proxy=self.web_config.proxy))
                    tools.register(WebFetchTool(proxy=self.web_config.proxy))
                
                # 2. 构造 System Prompt
                system_prompt = self._build_subagent_prompt()
                
                # 3. 构造多模态 User Content
                user_content = [{"type": "text", "text": task}]
                if images:
                    for img_path in images:
                        if img_path.startswith(("http://", "https://")):
                            user_content.append({"type": "image_url", "image_url": {"url": img_path}})
                        else:
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
                                    "_meta": {"path": str(p)}
                                })
                            else:
                                logger.warning("Subagent image path not found: {}", img_path)

                messages: list[dict[str, Any]] = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ]

                # 4. 运行 AgentRunner
                target_model = model or self.model
                
                # --- 注入审计日志 ---
                from cafeext.py.callbacks.logger import write_pretty_entry
                write_pretty_entry("request", {"subagent_id": task_id, "model": target_model, "label": label}, messages)
                
                result = await self.runner.run(AgentRunSpec(
                    initial_messages=messages,
                    tools=tools,
                    model=target_model,
                    max_iterations=15,
                    max_tool_result_chars=self.max_tool_result_chars,
                    hook=_SubagentHook(task_id, status),
                    max_iterations_message="Task completed but no final response was generated.",
                    error_message=None,
                    fail_on_tool_error=True,
                    checkpoint_callback=_on_checkpoint,
                ))
                
                status.phase = "done"
                status.stop_reason = result.stop_reason

                if result.stop_reason == "tool_error":
                    status.tool_events = list(result.tool_events)
                    # 记录失败日志
                    write_pretty_entry("failure", {"subagent_id": task_id, "stop_reason": "tool_error"}, [{"role": "error", "content": str(result.error)}])
                    await self._announce_result(
                        task_id, label, task,
                        self._format_partial_progress(result),
                        origin, "error",
                    )
                elif result.stop_reason == "error":
                    write_pretty_entry("failure", {"subagent_id": task_id, "stop_reason": "error"}, [{"role": "error", "content": str(result.error)}])
                    await self._announce_result(
                        task_id, label, task,
                        result.error or "Error: subagent execution failed.",
                        origin, "error",
                    )
                else:
                    final_result = result.final_content or "Task completed but no final response was generated."
                    # 记录成功日志
                    write_pretty_entry("success", {"subagent_id": task_id}, [{"role": "assistant", "content": final_result}])
                    logger.info("Subagent [{}] completed successfully", task_id)
                    await self._announce_result(task_id, label, task, final_result, origin, "ok")

            except Exception as e:
                from cafeext.py.callbacks.logger import write_pretty_entry
                write_pretty_entry("failure", {"subagent_id": task_id, "label": label, "error_type": type(e).__name__}, [{"role": "error", "content": str(e)}])
                status.phase = "error"
                status.error = str(e)
                logger.error("Subagent [{}] failed: {}", task_id, e)
                await self._announce_result(task_id, label, task, f"Error: {str(e)}", origin, "error")

        SubagentManager.spawn = patched_spawn
        SubagentManager._run_subagent = patched_run_subagent

    except Exception as e:
        logger.error("Failed to apply extended subagent patch: {}", e)
