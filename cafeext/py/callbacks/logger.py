import os
import json
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Any, List, Dict

# --- 优雅日志配置 ---

EMOJI_MAP = {
    "request": "🚀 推理请求",
    "success": "✨ 推理成功",
    "failure": "❌ 推理失败",
    "tool_start": "🛠️ 工具执行",
    "tool_end": "📦 工具响应",
    "tool_error": "⚠️ 工具报错",
    "inbound": "📥 收到消息",
    "outbound": "📤 发送回复"
}

SEPARATOR = "=" * 30

def format_content(content: Any) -> str:
    """将内容转换为单行字符串，替换换行符为 ↵，消除转义地狱"""
    if content is None:
        return ""
    if not isinstance(content, str):
        content = json.dumps(content, ensure_ascii=False)
    
    # 替换物理换行为 ↵ 符号
    content = content.replace("\n", " ↵ ").replace("\r", "")
    # 压缩连续空白
    content = re.sub(r"\s+", " ", content)
    
    # 截断过长内容以保持单行性能
    if len(content) > 4000:
        return content[:4000] + "... (truncated)"
    return content.strip()

def get_log_path() -> Path:
    """获取 .log 日志路径"""
    base_dir = Path(__file__).parent.parent.parent / "logs"
    base_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d-%H.log")
    return base_dir / filename

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
    
    lines.append(SEPARATOR + "\n")
    
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
        if hasattr(completion_response, "choices") and completion_response.choices:
            msg = completion_response.choices[0].message
            res_content = msg.content or (f"Call tools: {msg.tool_calls}" if msg.tool_calls else "")
        else:
            res_content = str(completion_response)

        attrs = {
            "model": kwargs.get("model", "unknown"),
            "duration": f"{(end_time - start_time).total_seconds():.2f}s"
        }
        context = [{"role": "assistant", "content": res_content}]
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
    """
    处理消息进出日志
    direction: 'inbound' 或 'outbound'
    """
    role_map = {"inbound": "user", "outbound": "assistant"}
    attrs = {
        "channel": channel,
        "target": user_or_chat if direction == "outbound" else "bot",
        "sender": user_or_chat if direction == "inbound" else "bot"
    }
    context = [{"role": role_map.get(direction, "info"), "content": content}]
    write_pretty_entry(direction, attrs, context)
