import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

def mask_key(key: str) -> str:
    """脱敏处理：保留首尾，中间遮掩"""
    if not key or len(key) <= 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"

def mask_headers(headers: dict[str, Any]) -> dict[str, Any]:
    """对敏感 Header 进行脱敏"""
    masked = dict(headers)
    for k in masked:
        if k.lower() in ("authorization", "api-key", "x-api-key"):
            val = str(masked[k])
            if "Bearer " in val:
                masked[k] = f"Bearer {mask_key(val.replace('Bearer ', ''))}"
            else:
                masked[k] = mask_key(val)
    return masked

def get_log_path() -> Path:
    """生成 yyyy-mm-dd-hh.jsonl 路径"""
    # 路径结构：cafeext/logs/yyyy-mm-dd-hh.jsonl
    base_dir = Path(__file__).parent.parent.parent / "logs"
    base_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d-%H.jsonl")
    return base_dir / filename

def write_jsonl(data: dict[str, Any]):
    """写入文件"""
    path = get_log_path()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def cafe_input_callback(kwargs):
    """请求拦截"""
    try:
        # 提取 LiteLLM 组装后的原始输入
        payload = kwargs.get("additional_args", {}).get("complete_input_dict", {})
        
        # 模拟提取 Header (LiteLLM 回调中获取 headers 的方式因 provider 而异)
        # 这里尝试从 kwargs 中寻找可能的配置信息
        headers = {
            "model": kwargs.get("model"),
            "api_base": kwargs.get("api_base")
        }
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "request",
            "headers": mask_headers(headers),
            "payload": payload
        }
        write_jsonl(entry)
    except Exception as e:
        print(f"DEBUG: Input logging failed: {e}")

def cafe_success_callback(kwargs, completion_response, start_time, end_time):
    """响应拦截 (成功)"""
    try:
        logging_obj = kwargs.get("litellm_logging_obj")
        raw_res = {}
        raw_req_headers = {}
        
        if logging_obj:
            collected = getattr(logging_obj, "collected_data", {})
            raw_res = collected.get("raw_response", {})
            raw_req = collected.get("raw_request", {})
            if isinstance(raw_req, dict):
                raw_req_headers = raw_req.get("headers", {})

        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "response",
            "status": "success",
            "request_headers": mask_headers(raw_req_headers),
            "payload": completion_response.model_dump() if hasattr(completion_response, "model_dump") else str(completion_response),
            "raw_http_response": raw_res
        }
        write_jsonl(entry)
    except Exception as e:
        print(f"DEBUG: Success logging failed: {e}")

def cafe_failure_callback(kwargs, exception, start_time, end_time):
    """响应拦截 (失败)"""
    try:
        logging_obj = kwargs.get("litellm_logging_obj")
        raw_res = {}
        raw_req_headers = {}
        
        if logging_obj:
            collected = getattr(logging_obj, "collected_data", {})
            raw_res = collected.get("raw_response", {})
            raw_req = collected.get("raw_request", {})
            if isinstance(raw_req, dict):
                raw_req_headers = raw_req.get("headers", {})

        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "response",
            "status": "failure",
            "error": str(exception),
            "request_headers": mask_headers(raw_req_headers),
            "raw_http_response": raw_res
        }
        write_jsonl(entry)
    except Exception as e:
        print(f"DEBUG: Failure logging failed: {e}")
