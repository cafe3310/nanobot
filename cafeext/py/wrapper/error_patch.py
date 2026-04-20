"""
错误自愈补丁 (Error Recovery Patch)。
适配 nanobot v0.1.5+ 的 AgentRunner 架构。
拦截 LLM 错误响应，注入排查模板引导模型自我修正。
"""

from loguru import logger
from typing import Any, Optional
from dataclasses import replace

ERROR_RECOVERY_TEMPLATE = """
## 🛠️ 错误排查与自愈建议 (Error Recovery Guide)

你刚才的尝试触发了系统错误。请根据以下指导进行修正：

1. **检查工具名称**: 
   - 确认你调用的工具是否在提供的工具列表中。
   - **注意**: `agent-browser` 必须通过 `exec` 工具执行命令行（例如 `exec(command="agent-browser open ...")`）。

2. **检查参数格式**: 
   - 确保 JSON 参数闭合正确。
   - 确保路径是绝对路径，或者相对于当前工作区的路径。

3. **调整策略**: 
   - 如果某个工具持续报错，尝试换一种方式（例如换成 `web_search` 或 `read_file`）。
   - 解释你为什么出错，并告诉主人你将如何修正。

请基于以上建议，重新生成你的响应或工具调用。
"""

def apply_error_patch():
    try:
        from nanobot.agent.runner import AgentRunner, AgentRunSpec, AgentRunResult
        
        # 记录原始方法
        original_run = AgentRunner.run

        async def patched_run(
            self,
            spec: AgentRunSpec,
        ) -> AgentRunResult:
            error_retry_count = 0
            MAX_ERROR_RETRIES = 2
            
            # 记录当前 spec 的副本，因为我们可能需要修改其 initial_messages 进行重试
            current_spec = spec
            
            while True:
                result = await original_run(self, current_spec)
                
                # 如果是正常的成功或非错误中断，直接返回
                if result.stop_reason != "error" or error_retry_count >= MAX_ERROR_RETRIES:
                    return result
                
                # 核心拦截点：错误自愈
                error_retry_count += 1
                error_msg = result.final_content or "Unknown model error"
                logger.warning(f"Intercepted LLM error (Retry {error_retry_count}/{MAX_ERROR_RETRIES}): {error_msg[:100]}")
                
                # 构造「错题本」上下文
                recovery_context = f"""错误信息
--------
{error_msg}

{ERROR_RECOVERY_TEMPLATE}"""
                
                # 获取最新的消息列表（包含刚才失败的那一轮）
                new_messages = list(result.messages)
                
                # 1. 将错误作为 assistant 消息存入（让模型知道自己刚才失败了）
                # 注意：如果最后一条已经是错误 assistant，则不重复添加
                if not (new_messages and new_messages[-1].get("role") == "assistant" and "ERROR:" in str(new_messages[-1].get("content", ""))):
                    new_messages.append({
                        "role": "assistant",
                        "content": f"ERROR: {error_msg}"
                    })
                
                # 2. 注入抢救提示
                new_messages.append({
                    "role": "user", 
                    "content": recovery_context
                })
                
                # 3. 更新 spec 进行下一轮「抢救运行」
                # 我们通过修改 initial_messages 并减少最大迭代次数（防止无限循环）来构造新的运行
                current_spec = replace(
                    current_spec,
                    initial_messages=new_messages,
                    max_iterations=max(1, current_spec.max_iterations - result.iteration)
                )
                
                # 继续循环进行下一次尝试
                continue

        # 注入补丁
        AgentRunner.run = patched_run
        logger.info("Successfully applied AgentRunner error recovery patch.")

    except Exception as e:
        logger.error(f"Failed to apply AgentRunner error recovery patch: {e}")
