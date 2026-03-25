"""
错误自愈补丁 (Error Recovery Patch)。
拦截 LLM 错误响应，注入排查模板引导模型自我修正。
"""

from loguru import logger
import json

ERROR_RECOVERY_TEMPLATE = """
## 🛠️ 错误排查与自愈建议 (Error Recovery Guide)

你刚才的尝试触发了系统错误。请根据以下指导进行修正：

1. **检查工具名称**: 
   - 确认你调用的工具是否在「模型技能(Agent Skills)」列表中。
   - **重要提示**: `agent-browser` 不是一个独立的 Tool Call，它必须通过 `exec` 工具执行命令行（例如 `exec(command="agent-browser open ...")`）。

2. **检查参数格式**: 
   - 确保 JSON 参数闭合正确。
   - 确保路径是绝对路径，或者相对于当前工作区的路径。

3. **调整策略**: 
   - 如果某个工具持续报错，尝试换一种方式（例如从 `agent-browser` 换成 `web_search` 或 `read_file`）。
   - 解释你为什么出错，并告诉主人你将如何修正。

请基于以上建议，重新生成你的响应或工具调用。
"""

def apply_error_patch():
    try:
        from nanobot.agent.loop import AgentLoop
        
        # 记录原始方法
        original_run_loop = AgentLoop._run_agent_loop

        async def patched_run_agent_loop(
            self,
            initial_messages: list[dict],
            on_progress = None,
        ):
            # 为了能完全控制消息流，我们可能需要复刻一部分原有的循环逻辑
            # 或者通过包装器捕获 iteration 的状态。
            # 这里选择「装饰器+上下文注入」的思路
            
            messages = initial_messages
            iteration = 0
            final_content = None
            tools_used = []
            
            error_retry_count = 0
            MAX_ERROR_RETRIES = 2 # 同一个任务最多允许 2 次错误自愈重试

            while iteration < self.max_iterations:
                iteration += 1
                tool_defs = self.tools.get_definitions()

                response = await self.provider.chat_with_retry(
                    messages=messages,
                    tools=tool_defs,
                    model=self.model,
                )

                if response.has_tool_calls:
                    # --- 正常的工具调用逻辑 (保留原版) ---
                    if on_progress:
                        thought = self._strip_think(response.content)
                        if thought: await on_progress(thought)
                        tool_hint = self._tool_hint(response.tool_calls)
                        tool_hint = self._strip_think(tool_hint)
                        await on_progress(tool_hint, tool_hint=True)

                    tool_call_dicts = [tc.to_openai_tool_call() for tc in response.tool_calls]
                    messages = self.context.add_assistant_message(
                        messages, response.content, tool_call_dicts,
                        reasoning_content=response.reasoning_content,
                        thinking_blocks=response.thinking_blocks,
                    )

                    for tool_call in response.tool_calls:
                        tools_used.append(tool_call.name)
                        result = await self.tools.execute(tool_call.name, tool_call.arguments)
                        messages = self.context.add_tool_result(
                            messages, tool_call.id, tool_call.name, result
                        )
                else:
                    clean = self._strip_think(response.content)
                    
                    # --- 核心拦截点：错误自愈 ---
                    if response.finish_reason == "error" and error_retry_count < MAX_ERROR_RETRIES:
                        error_retry_count += 1
                        error_msg = clean or "Unknown model error"
                        logger.warning(f"Intercepted LLM error (Retry {error_retry_count}): {error_msg[:100]}")
                        
                        # 构造「错题本」上下文
                        recovery_context = f"""错误信息
--------
{error_msg}

{ERROR_RECOVERY_TEMPLATE}"""
                        
                        # 将错误作为 assistant 消息存入（虽然它是错的，但它是发生的历史）
                        # 注意：原版是不存 error 响应的，但为了自愈，我们需要让模型知道它刚才说了啥。
                        messages.append({
                            "role": "assistant",
                            "content": f"ERROR: {error_msg}"
                        })
                        
                        # 注入抢救提示（作为 system 或 user 角色）
                        messages.append({
                            "role": "user", 
                            "content": recovery_context
                        })
                        
                        # 不 break，继续下一次循环（即重试）
                        continue
                    
                    # 正常的结束逻辑
                    if response.finish_reason == "error":
                        logger.error("LLM returned error (max retries reached): {}", (clean or "")[:200])
                        final_content = clean or "Sorry, I encountered an error calling the AI model."
                        break
                    
                    messages = self.context.add_assistant_message(
                        messages, clean, reasoning_content=response.reasoning_content,
                        thinking_blocks=response.thinking_blocks,
                    )
                    final_content = clean
                    break

            if final_content is None and iteration >= self.max_iterations:
                logger.warning("Max iterations ({}) reached", self.max_iterations)
                final_content = f"Reached max tool call iterations ({self.max_iterations})."

            return final_content, tools_used, messages

        # 注入补丁
        AgentLoop._run_agent_loop = patched_run_agent_loop
        logger.info("Successfully applied error recovery patch.")

    except Exception as e:
        logger.error(f"Failed to apply error recovery patch: {e}")
