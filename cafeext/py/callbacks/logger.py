"""
=== cafe3310 nanobot sidecar function ===
注入点：由 launcher.py 拦截 OpenAICompatProvider.chat 并在其回调中被调用。
作用：实现视觉化日志记录。格式化推理请求、成功/失败响应及工具链执行详情，支持 Base64 图片截断与 JSON 美化，生成人类可读的 .log 文件。
=== end(keep this block) ===
"""

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Any, List, Dict

# 从中央配置中心导入
from cafeext.py.wrapper.config import (
    EMOJI_MAP, LOG_SEPARATOR, LOG_SUFFIX, LOG_TRUNCATE_LIMIT, LOG_DIR
)

def format_content(content: Any) -> str:
    """将内容转换为单行字符串，替换换行符为 ↵，消除转义地狱"""
    if content is None:
        return ""
    if not isinstance(content, str):
        # 仅对非字符串使用 json.dumps，且确保不转义中文
        content = json.dumps(content, ensure_ascii=False)
    
    # 1. 替换物理换行为 ↵ 符号
    content = content.replace("\n", " ↵ ").replace("\r", "")
    # 2. 压缩连续空白
    content = re.sub(r"\s+", " ", content)
    
    # 3. 特殊处理：截断 Base64 图片数据 (data:image/...;base64,...)
    def truncate_base64(match):
        prefix = match.group(1) # data:image/xxx;base64,
        data = match.group(2)   # 原始 base64 数据
        if len(data) > 40:
            # 保留前 10 位和后 10 位，中间使用省略号
            return f"{prefix}{data[:10]}......(base64)......{data[-10:]}"
        return match.group(0)

    # 匹配 data:image/xxx;base64, 后跟一大串 Base64 字符
    b64_pattern = r"(data:image\/[a-zA-Z]*;base64,)([a-zA-Z0-9+\/]+={0,2})"
    content = re.sub(b64_pattern, truncate_base64, content)

    # 4. 使用配置的阈值进行全局截断
    if len(content) > LOG_TRUNCATE_LIMIT:
        return content[:LOG_TRUNCATE_LIMIT] + "... (truncated)"
    return content.strip()

def get_log_path() -> Path:
    """获取符合配置后缀的日志路径"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d-%H") + LOG_SUFFIX
    return LOG_DIR / filename

def write_pretty_entry(event_type: str, attrs: Dict[str, Any], context: List[Dict[str, str]]):
    """
    写入符合规范的视觉化日志
    """
    path = get_log_path()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    emoji = EMOJI_MAP.get(event_type, "📝 日志记录")
    
    lines = [f"{emoji} [{timestamp}]"]
    
    # 1. 写入属性 (attr=val)
    for k, v in attrs.items():
        lines.append(f"  {k}={v}")
    
    # 2. 写入上下文/参数 (context)
    if context:
        lines.append("  context:")
        for i, item in enumerate(context, 1):
            role = item.get("role", "info")
            content = format_content(item.get("content", ""))
            lines.append(f"    - {i:02d}. {role}: {content}")
    
    lines.append(LOG_SEPARATOR + "\n")
    
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))

# --- 拦截器适配逻辑 ---

def cafe_input_callback(kwargs):
    """处理推理请求日志"""
    try:
        payload = kwargs.get("additional_args", {}).get("complete_input_dict", {})
        messages = payload.get("messages", [])
        total_chars = sum(len(str(m.get("content", ""))) for m in messages)
        
        attrs = {
            "model": kwargs.get("model", "unknown"),
            "turns": len(messages),
            "total_chars": total_chars
        }
        context = [{"role": m.get("role"), "content": m.get("content")} for m in messages]
        write_pretty_entry("request", attrs, context)
    except Exception as e:
        print(f"DEBUG: Input logging failed: {e}")

def cafe_success_callback(kwargs, completion_response, start_time, end_time):
    """处理推理成功响应日志"""
    try:
        res_content = ""
        reasoning = None
        
        # 适配 nanobot v0.1.5+ 的 LLMResponse 对象
        if hasattr(completion_response, "content"):
            res_content = completion_response.content or ""
            if hasattr(completion_response, "tool_calls") and completion_response.tool_calls:
                # 如果有工具调用且没有内容，显示工具调用
                if not res_content:
                    res_content = f"Call tools: {completion_response.tool_calls}"
                else:
                    res_content += f" (Tools: {completion_response.tool_calls})"
            
            # 提取推理内容 (Thinking)
            reasoning = getattr(completion_response, "reasoning_content", None)
        # 兼容旧版本的 OpenAI 响应对象
        elif hasattr(completion_response, "choices") and completion_response.choices:
            msg = completion_response.choices[0].message
            res_content = msg.content or (f"Call tools: {msg.tool_calls}" if msg.tool_calls else "")
        else:
            res_content = str(completion_response)

        attrs = {
            "model": kwargs.get("model", "unknown"),
            "duration": f"{(end_time - start_time).total_seconds():.2f}s"
        }
        
        context = []
        if reasoning:
            context.append({"role": "thinking", "content": reasoning})
        context.append({"role": "assistant", "content": res_content})
        
        write_pretty_entry("success", attrs, context)
    except Exception as e:
        print(f"DEBUG: Success logging failed: {e}")

def cafe_failure_callback(kwargs, exception, start_time, end_time):
    """处理推理失败响应日志"""
    try:
        attrs = {
            "model": kwargs.get("model", "unknown"),
            "duration": f"{(end_time - start_time).total_seconds():.2f}s"
        }
        context = [{"role": "error", "content": str(exception)}]
        write_pretty_entry("failure", attrs, context)
    except Exception as e:
        print(f"DEBUG: Failure logging failed: {e}")

def cafe_tool_start_log(name: str, params: dict[str, Any]):
    """处理工具执行开始日志"""
    attrs = {"tool": name}
    context = [{"role": "parameters", "content": params}]
    write_pretty_entry("tool_start", attrs, context)

def cafe_tool_end_log(name: str, result: str, duration_ms: float):
    """处理工具执行响应日志"""
    event_type = "tool_error" if "Error" in result or "Exception" in result else "tool_end"
    attrs = {"tool": name, "duration": f"{duration_ms:.1f}ms"}
    context = [{"role": "result", "content": result}]
    write_pretty_entry(event_type, attrs, context)

def cafe_message_log(direction: str, channel: str, user_or_chat: str, content: str):
    """处理消息进出日志"""
    role_map = {"inbound": "user", "outbound": "assistant"}
    attrs = {
        "channel": channel,
        "target": user_or_chat if direction == "outbound" else "bot",
        "sender": user_or_chat if direction == "inbound" else "bot"
    }
    context = [{"role": role_map.get(direction, "info"), "content": content}]
    write_pretty_entry(direction, attrs, context)
