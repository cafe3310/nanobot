"""安全策略常量定义与拦截逻辑。"""

import time
import sys
from datetime import datetime

# 禁用列表定义 (使用代码中的真实工具名)
DISABLED_SKILLS = ["clawhub"]
DISABLED_TOOLS = ["exec", "spawn"]

def apply_security_policy():
    """通过全局 Monkey Patch 强制执行安全策略与审计逻辑。"""
    try:
        from cafeext.py.callbacks.logger import (
            cafe_tool_start_log, cafe_tool_end_log, cafe_message_log
        )

        # 1. 拦截 ToolRegistry (工具审计)
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
            cafe_tool_start_log(name, params)
            start_t = time.perf_counter()
            try:
                result = await original_execute(self, name, params)
                duration = (time.perf_counter() - start_t) * 1000
                cafe_tool_end_log(name, result, duration)
                return result
            except Exception as e:
                duration = (time.perf_counter() - start_t) * 1000
                cafe_tool_end_log(name, f"Exception: {str(e)}", duration)
                raise e
        ToolRegistry.execute = patched_execute

        # 2. 拦截 MessageBus (消息进出审计)
        import nanobot.bus.queue
        MessageBus = nanobot.bus.queue.MessageBus

        original_publish_inbound = MessageBus.publish_inbound
        async def patched_publish_inbound(self, msg):
            # 记录收到消息
            cafe_message_log("inbound", msg.channel, msg.sender_id, msg.content)
            return await original_publish_inbound(self, msg)
        MessageBus.publish_inbound = patched_publish_inbound

        original_publish_outbound = MessageBus.publish_outbound
        async def patched_publish_outbound(self, msg):
            # 记录发送回复
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
