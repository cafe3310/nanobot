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

            # B. 多维人工确认 (终端 + macOS 对话框)
            allowed = True
            if name not in ["message"]:
                try:
                    pretty_params = json.dumps(params, indent=2, ensure_ascii=False)
                except:
                    pretty_params = str(params)

                # 1. 终端静默提示（包含响铃）
                print(f"\a\n\n{'='*50}")
                print(f"🛡️  [HUMAN-IN-THE-LOOP] Confirm Tool Execution")
                print(f"{'='*50}")
                print(f"🔧 Tool  : {name}")
                print(f"📝 Params: {pretty_params}")
                print(f"{'-'*50}")
                
                # 2. 尝试 macOS 原生确认 (三态判断)
                # True: Allow, False: Deny, None: UI Error
                ui_result = ask_macos_permission(name, params)
                
                if ui_result is True:
                    allowed = True
                elif ui_result is False:
                    allowed = False # 用户明确拒绝，不触发后备
                else:
                    # ui_result is None: 弹窗失败，回退到终端物理交互
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
