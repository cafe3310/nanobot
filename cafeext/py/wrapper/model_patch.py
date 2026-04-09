import re
import uuid
from typing import Any
import json_repair
from nanobot.providers.custom_provider import CustomProvider
from nanobot.providers.base import LLMResponse, ToolCallRequest

def apply_model_patch():
    """
    Monkey patch for CustomProvider to support embedded <tool_call> tags 
    in the content text (common in reasoning/thinking models).
    """
    original_parse = CustomProvider._parse

    def patched_parse(self, response: Any) -> LLMResponse:
        # Call original parse first to get basic LLMResponse
        llm_res = original_parse(self, response)
        
        # If there's content, try to extract embedded tool calls
        content = llm_res.content or ""
        if "<tool_call>" in content:
            pattern = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
            matches = pattern.findall(content)
            
            # Ensure we have a list to append to
            if not llm_res.tool_calls:
                llm_res.tool_calls = []
                
            for match in matches:
                try:
                    data = json_repair.loads(match.strip())
                    if isinstance(data, dict) and "name" in data:
                        # Append the extracted tool call
                        llm_res.tool_calls.append(ToolCallRequest(
                            id=f"call_{uuid.uuid4().hex[:12]}",
                            name=data["name"],
                            arguments=data.get("arguments", {})
                        ))
                except Exception:
                    # Silent fail for malformed XML-tool-calls
                    pass
                    
        return llm_res

    # Apply the patch
    CustomProvider._parse = patched_parse
    # print("[nb-patch] CustomProvider._parse patched for <tool_call> support.")
