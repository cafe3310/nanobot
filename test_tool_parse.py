import re
import json_repair
import uuid

def extract_tool_calls(content):
    if not content:
        return []
    
    # Match <tool_call>...</tool_call> blocks
    pattern = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)
    matches = pattern.findall(content)
    
    tool_calls = []
    for match in matches:
        try:
            data = json_repair.loads(match.strip())
            if isinstance(data, dict) and "name" in data:
                tool_calls.append({
                    "id": f"call_{uuid.uuid4().hex[:12]}",
                    "name": data["name"],
                    "arguments": data.get("arguments", {})
                })
        except Exception as e:
            print(f"Failed to parse tool call: {e}")
            
    return tool_calls

content = """这里是思考过程。
<tool_call>
{"name": "agent_browser", "arguments": {"task": "打开煎蛋的页面"}}
</tool_call>
这是后续文本。"""

print(extract_tool_calls(content))
