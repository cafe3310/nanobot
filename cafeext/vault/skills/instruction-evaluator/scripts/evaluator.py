import json
import subprocess
import time
import os
import re
from pathlib import Path

# 路径配置
CAFEEXT_DIR = Path("/Users/sipan/workspace/nanobot/cafeext")
LOG_DIR = CAFEEXT_DIR / "logs"
SKILLS_DIR = CAFEEXT_DIR / "vault/skills"
EVAL_DIR = SKILLS_DIR / "instruction-evaluator"
TEST_CASES_PATH = EVAL_DIR / "test_cases.json"

def run_nb_command(args):
    """运行 nb 命令并返回输出"""
    cmd = ["/Users/sipan/workspace/nanobot/cafeext/nanobot-shell.sh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def get_latest_log():
    """获取最新的日志文件路径"""
    logs = sorted(LOG_DIR.glob("*.log"))
    return logs[-1] if logs else None

def parse_log_for_tools(log_content):
    """从日志内容中解析工具调用 (强化版)"""
    tool_calls = []
    
    # 找到所有 "tool=NAME" 的起始位置
    matches = list(re.finditer(r"tool=([a-zA-Z0-9_-]+)", log_content))
    for i, match in enumerate(matches):
        tool_name = match.group(1)
        start_pos = match.end()
        
        # 确定当前工具块的边界：直到下一个 tool= 或 下一个 推理成功
        next_tool = matches[i+1].start() if i+1 < len(matches) else len(log_content)
        next_success = log_content.find("✨ 推理成功", start_pos)
        end_pos = next_success if (next_success != -1 and next_success < next_tool) else next_tool
            
        block = log_content[start_pos:end_pos]
        
        # 寻找 parameters: { ... } 并提取最外层的大括号
        # 使用 rfind 确保找到最后一个大括号，以支持嵌套大括号的内容
        params_match = re.search(r"parameters:\s*(\{.*)", block, re.DOTALL)
        if params_match:
            params_str = params_match.group(1)
            last_brace = params_str.rfind("}")
            if last_brace != -1:
                params_json = params_str[:last_brace+1]
                # 清理日志转义符
                params_json = params_json.replace(" ↵", "").replace("↵", "")
                tool_calls.append({
                    "name": tool_name,
                    "args": params_json
                })
    return tool_calls

def run_evaluation():
    print("🚀 Starting Instruction Evaluation (v3 - Robust Paths)...")
    
    # 1. Reset
    print("🧹 Resetting environment...")
    run_nb_command(["reset", "--logs"])
    time.sleep(1)
    
    if not TEST_CASES_PATH.exists():
        print(f"❌ Test cases not found at {TEST_CASES_PATH}")
        return

    with open(TEST_CASES_PATH, "r") as f:
        cases = json.load(f)
    
    results = []
    
    for case in cases:
        print(f"\n📝 Running Case: {case['name']} ({case['id']})")
        print(f"Prompt: {case['prompt']}")
        
        # 记录当前日志位置
        latest_log = get_latest_log()
        start_pos = latest_log.stat().st_size if latest_log else 0
        
        # 2. Run Chat
        output = run_nb_command(["agent", "--message", case['prompt']])
        print(f"Assistant: {output.strip()}")
        
        # 3. Analyze Logs
        time.sleep(2)
        latest_log = get_latest_log()
        if not latest_log:
            print("❌ No log file found.")
            continue
            
        with open(latest_log, "r") as f:
            f.seek(start_pos)
            new_log_content = f.read()
            
        tools = parse_log_for_tools(new_log_content)
        
        # 统计指标 (全面放宽匹配逻辑)
        stats = {
            "case_id": case['id'],
            "response": output.strip(),
            "tools_called": [t['name'] for t in tools],
            "metrics": {
                # 初始读取：读了 SOUL, USER 或 MEMORY.md
                "initialization_read": any(any(x in t['args'].lower() for x in ["soul.md", "user.md", "memory.md"]) for t in tools if t['name'] == 'read_file'),
                # 专门检查是否读了 memory 技能的 SKILL.md
                "memory_skill_read": any("memory" in t['args'].lower() and "skill.md" in t['args'].lower() for t in tools if t['name'] == 'read_file'),
                # Wiki 搜索：只要包含 "wiki" 这个词就算
                "wiki_search": any("wiki" in t['args'].lower() for t in tools if t['name'] in ['list_dir', 'grep_search', 'ls', 'read_file']),
                # Wiki 写入：写了 wiki, diaries 或者更新了长期记忆 MEMORY.md
                "wiki_write": any(any(x in t['args'].lower() for x in ["wiki", "diaries", "memory.md"]) for t in tools if t['name'] in ['write_file', 'replace', 'edit_file', 'write_file'])
            }
        }
        
        # 验证是否符合预期
        passed = True
        for key, expected in case['expectations'].items():
            if stats['metrics'].get(key) != expected:
                passed = False
        
        stats['status'] = "PASS" if passed else "FAIL"
        results.append(stats)
        
        print(f"Status: {stats['status']}")
        if tools:
            print(f"Tools Detected: {', '.join(stats['tools_called'])}")
            
    # 4. Final Report
    report_path = EVAL_DIR / f"report_{int(time.time())}.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Evaluation complete. Report saved to: {report_path}")
    
    # Summary Table
    print("\n--- Summary ---")
    for r in results:
        tools_str = ', '.join(r['tools_called']) if r['tools_called'] else "(No tools)"
        print(f"[{r['status']}] {r['case_id']}: {tools_str}")

if __name__ == "__main__":
    run_evaluation()
