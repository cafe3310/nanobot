"""
安全策略常量定义与拦截逻辑。
"""

import time
import sys
import json
import termios
import tty
from pathlib import Path
from datetime import datetime

# 从中央配置中心导入禁用列表
from cafeext.py.wrapper.config import DISABLED_SKILLS, DISABLED_TOOLS
from cafeext.py.wrapper.notification import ask_macos_permission

def get_char():
    """读取单个按键，无需回车。仅限类 Unix 系统 (macOS/Linux)。"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# --- 规则辅助算子 (Rule Operators) ---

def is_simple_command(cmd: str) -> bool:
    """
    确保命令是单一的，没有通过 shell 符号拼接。
    防御：&&, ||, ;, |, &, \n, ` (反引号), $()
    """
    if not cmd: return False
    separators = ["&&", "||", ";", "|", "&", "\n", "`", "$("]
    # 简单的包含检查，如果需要更严谨可以用正则处理转义情况
    return not any(sep in cmd for sep in separators)

def is_exec_starting_with(params: dict, allowed_prefixes: list) -> bool:
    """检测 exec 命令是否以特定前缀开头且没有多命令拼接"""
    cmd = params.get("command", "").strip()
    if not is_simple_command(cmd):
        return False
    return any(cmd.startswith(p) for p in allowed_prefixes)

# --- 工具执行白名单 (Whitelist) ---

WHITELIST_RULES = [
    {
        "name": lambda n: n in ["read_file", "list_dir", "list_directory"],
        "args": lambda a: True,
        "description": "只读文件系统操作"
    },
    {
        "name": lambda n: n == "exec",
        "args": lambda a: is_exec_starting_with(a, ["cat ", "ls ", "find ", "wc ", "tail ", "head ", "which "]),
        "description": "受控的只读 CLI 探测操作"
    },
    {
        "name": lambda n: n == "exec",
        "args": lambda a: is_exec_starting_with(a, ["agent-browser "]),
        "description": "浏览器自动化操作"
    },
    {
        "name": lambda n: n == "web_search",
        "args": lambda a: True,
        "description": "联网搜索"
    },
    {
        "name": lambda n: n == "web_fetch",
        "args": lambda a: True,
        "description": "网页内容抓取"
    }
]

def check_whitelist(name: str, params: dict) -> str | None:
    """检查工具调用是否匹配白名单。匹配成功返回规则描述，否则返回 None。"""
    for rule in WHITELIST_RULES:
        try:
            if rule["name"](name) and rule["args"](params):
                return rule["description"]
        except:
            continue
    return None

def apply_security_policy():
    """通过全局 Monkey Patch 强制执行安全策略、全链路审计与多维人工确认。"""
    try:
        from cafeext.py.callbacks.logger import (
            cafe_tool_start_log, cafe_tool_end_log, cafe_message_log
        )

        # 1. 拦截 ToolRegistry
        import nanobot.agent.tools.registry
        ToolRegistry = nanobot.agent.tools.registry.ToolRegistry
        
        original_register = ToolRegistry.register
        def patched_register(self, tool):
            if tool.name in DISABLED_TOOLS: return
            return original_register(self, tool)
        ToolRegistry.register = patched_register

        original_execute = ToolRegistry.execute
        async def patched_execute(self, name, params):
            # A. 审计日志 (开始)
            cafe_tool_start_log(name, params)
            
            # 特殊逻辑：允许只读工具访问整个 Vault 目录 (只读穿透)
            # 注意：这里的逻辑在白名单之前，但功能上是互补的。
            # 为了统一，我们保持这个逻辑，但后续白名单会处理通用的放行。
            if name in ["read_file", "list_dir", "list_directory"]:
                from cafeext.py.wrapper.config import VAULT_DIR
                path_val = params.get("path") or params.get("dir_path", "")
                if path_val and str(VAULT_DIR.resolve()) in str(Path(path_val).resolve()):
                    tool_instance = self.get(name)
                    if tool_instance:
                        # 注入 Vault 目录到工具的额外允许清单中
                        old_extra = getattr(tool_instance, "_extra_allowed_dirs", [])
                        tool_instance._extra_allowed_dirs = (old_extra or []) + [VAULT_DIR.resolve()]
                        try:
                            result = await tool_instance.execute(**params)
                            cafe_tool_end_log(name, result, 0)
                            return result
                        finally:
                            tool_instance._extra_allowed_dirs = old_extra

            # B. 白名单检测与人工确认
            allowed = True
            is_whitelisted = False
            
            # 提前准备参数展示，以便白名单和人工确认都能使用
            try:
                pretty_params = json.dumps(params, indent=2, ensure_ascii=False)
            except:
                pretty_params = str(params)

            # 忽略 message 工具，它是沟通核心
            if name not in ["message"]:
                # 1. 检查白名单
                whitelist_reason = check_whitelist(name, params)
                if whitelist_reason:
                    print(f"\n🛡️  [WHITELIST] Auto-approving '{name}' (原因: {whitelist_reason})")
                    print(f"🔧 Tool  : {name}")
                    print(f"📝 Params: {pretty_params}")
                    is_whitelisted = True
                    allowed = True
                else:
                    # 2. 不在白名单，执行多维人工确认
                    # 终端提示
                    print(f"\a\n\n{'='*50}")
                    print(f"🛡️  [HUMAN-IN-THE-LOOP] Confirm Tool Execution")
                    print(f"{'='*50}")
                    print(f"🔧 Tool  : {name}")
                    print(f"📝 Params: {pretty_params}")
                    print(f"{'-'*50}")
                    
                    # 尝试 macOS 原生确认
                    ui_result = ask_macos_permission(name, params)
                    
                    if ui_result is True:
                        allowed = True
                    elif ui_result is False:
                        allowed = False 
                    else:
                        # 终端物理交互
                        print("📢 macOS Dialog unavailable. Fallback to terminal...")
                        sys.stdout.write("👉 Action: [1] ✅ Execute | [2] ❌ Deny\nSelection: ")
                        sys.stdout.flush()
                        choice = get_char()
                        sys.stdout.write(f"{choice}\n")
                        allowed = (choice == "1")

                if not allowed:
                    deny_msg = "[Operation Cancelled] Reason: User denied execution."
                    cafe_tool_end_log(name, deny_msg, 0)
                    print(f"⚠️  Execution DENIED by user.\n{'='*50}\n")
                    return deny_msg

            # C. 继续执行
            if not is_whitelisted:
                print(f"🚀 Executing {name}...")
            
            start_t = time.perf_counter()
            try:
                result = await original_execute(self, name, params)
                duration = (time.perf_counter() - start_t) * 1000
                cafe_tool_end_log(name, result, duration)
                print(f"✅ Execution finished ({duration:.1f}ms).\n{'='*50}\n")
                return result
            except Exception as e:
                duration = (time.perf_counter() - start_t) * 1000
                cafe_tool_end_log(name, f"Exception: {str(e)}", duration)
                print(f"❌ Execution failed: {e}\n{'='*50}\n")
                raise e

        ToolRegistry.execute = patched_execute

        # 2. 拦截 MessageBus (审计)
        import nanobot.bus.queue
        MessageBus = nanobot.bus.queue.MessageBus
        original_pub_in = MessageBus.publish_inbound
        async def patched_pub_in(self, msg):
            cafe_message_log("inbound", msg.channel, msg.sender_id, msg.content)
            return await original_pub_in(self, msg)
        MessageBus.publish_inbound = patched_pub_in

        original_pub_out = MessageBus.publish_outbound
        async def patched_pub_out(self, msg):
            cafe_message_log("outbound", msg.channel, msg.chat_id, msg.content)
            return await original_pub_out(self, msg)
        MessageBus.publish_outbound = patched_pub_out

        # 3. 拦截 SkillsLoader
        import nanobot.agent.skills
        SkillsLoader = nanobot.agent.skills.SkillsLoader
        orig_list = SkillsLoader.list_skills
        def patched_list(self, *args, **kwargs):
            return [s for s in orig_list(self, *args, **kwargs) if s["name"] not in DISABLED_SKILLS]
        SkillsLoader.list_skills = patched_list
        
    except Exception as e:
        print(f"Warning: Failed to apply security policy with notification: {e}")
