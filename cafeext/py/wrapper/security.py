"安全策略常量定义与拦截逻辑。"

import time
import sys
import json
import termios
import tty
from datetime import datetime

# 从中央配置中心导入禁用列表
from cafeext.py.wrapper.config import DISABLED_SKILLS, DISABLED_TOOLS

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
    """通过全局 Monkey Patch 强制执行安全策略、全链路审计与人工确认。"""
    try:
        from cafeext.py.callbacks.logger import (
            cafe_tool_start_log, cafe_tool_end_log, cafe_message_log
        )

        # 1. 拦截 ToolRegistry (工具审计与人工确认)
        import nanobot.agent.tools.registry
        ToolRegistry = nanobot.agent.tools.registry.ToolRegistry
        
        original_register = ToolRegistry.register
        def patched_register(self, tool):
            if tool.name in DISABLED_TOOLS:
                return
            return original_register(self, tool)
        ToolRegistry.register = patched_register

        original_execute = ToolRegistry.execute
        async def patched_execute(self, name, params):
            # A. 记录审计日志 (开始)
            cafe_tool_start_log(name, params)
            
            # B. 人工确认逻辑 (Terminal 交互)
            # 跳过特定无需确认的轻量工具（如消息发送）
            if name not in ["message"]:
                try:
                    pretty_params = json.dumps(params, indent=2, ensure_ascii=False)
                except:
                    pretty_params = str(params)

                print(f"\a\n\n{'='*50}")
                print(f"🛡️  [HUMAN-IN-THE-LOOP] Confirm Tool Execution")
                print(f"{'='*50}")
                print(f"🔧 Tool  : {name}")
                print(f"📝 Params: {pretty_params}")
                print(f"{'-'*50}")
                print(f"👉 Action: [1] ✅ Execute | [2] ❌ Deny")
                
                # 捕获单个按键
                sys.stdout.write("Selection: ")
                sys.stdout.flush()
                choice = get_char()
                sys.stdout.write(f"{choice}\n") # 回显按键并换行
                
                if choice != "1":
                    deny_msg = "[Operation Cancelled] Reason: User denied execution."
                    # 记录审计日志 (拒绝)
                    cafe_tool_end_log(name, deny_msg, 0)
                    print(f"⚠️  Execution DENIED by user.\n{'='*50}\n")
                    return deny_msg

            # C. 继续执行原始逻辑
            print(f"🚀 Executing {name}...")
            start_t = time.perf_counter()
            try:
                result = await original_execute(self, name, params)
                duration = (time.perf_counter() - start_t) * 1000
                
                # 记录审计日志 (结束)
                cafe_tool_end_log(name, result, duration)
                print(f"✅ Execution finished ({duration:.1f}ms).\n{'='*50}\n")
                return result
            except Exception as e:
                duration = (time.perf_counter() - start_t) * 1000
                cafe_tool_end_log(name, f"Exception: {str(e)}", duration)
                print(f"❌ Execution failed: {e}\n{'='*50}\n")
                raise e

        ToolRegistry.execute = patched_execute

        # 2. 拦截 MessageBus (消息进出审计)
        import nanobot.bus.queue
        MessageBus = nanobot.bus.queue.MessageBus

        original_publish_inbound = MessageBus.publish_inbound
        async def patched_publish_inbound(self, msg):
            cafe_message_log("inbound", msg.channel, msg.sender_id, msg.content)
            return await original_publish_inbound(self, msg)
        MessageBus.publish_inbound = patched_publish_inbound

        original_publish_outbound = MessageBus.publish_outbound
        async def patched_publish_outbound(self, msg):
            cafe_message_log("outbound", msg.channel, msg.chat_id, msg.content)
            return await original_publish_outbound(self, msg)
        MessageBus.publish_outbound = patched_publish_outbound

        # 3. 拦截 SkillsLoader (技能安全)
        import nanobot.agent.skills
        SkillsLoader = nanobot.agent.skills.SkillsLoader
        
        original_list_skills = SkillsLoader.list_skills
        def patched_list_skills(self, *args, **kwargs):
            skills = original_list_skills(self, *args, **kwargs)
            return [s for s in skills if s["name"] not in DISABLED_SKILLS]
        SkillsLoader.list_skills = patched_list_skills
        
        original_load_skill = SkillsLoader.load_skill
        def patched_load_skill(self, name):
            if name in DISABLED_SKILLS:
                return None
            return original_load_skill(self, name)
        SkillsLoader.load_skill = patched_load_skill
        
        original_get_meta = SkillsLoader.get_skill_metadata
        def patched_get_meta(self, name):
            if name in DISABLED_SKILLS:
                return None
            return original_get_meta(self, name)
        SkillsLoader.get_skill_metadata = patched_get_meta
        
    except Exception as e:
        print(f"Warning: Failed to apply security policy: {e}")
