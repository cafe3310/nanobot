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
        # 1. 拦截 ToolRegistry (必须在任何 AgentLoop 实例创建前完成)
        # 我们直接修改模块中的类定义，确保所有 import 都能看到补丁
        import nanobot.agent.tools.registry
        from cafeext.py.callbacks.logger import cafe_tool_start_log, cafe_tool_end_log
        
        ToolRegistry = nanobot.agent.tools.registry.ToolRegistry
        
        # 拦截注册: 强制禁用黑名单工具
        original_register = ToolRegistry.register
        def patched_register(self, tool):
            if tool.name in DISABLED_TOOLS:
                return
            return original_register(self, tool)
        ToolRegistry.register = patched_register

        # 拦截执行: 记录工具调用开始与结束
        original_execute = ToolRegistry.execute
        async def patched_execute(self, name, params):
            # 1. 记录工具开始执行
            cafe_tool_start_log(name, params)
            
            start_t = time.perf_counter()
            try:
                # 2. 执行原始逻辑
                result = await original_execute(self, name, params)
                duration = (time.perf_counter() - start_t) * 1000
                
                # 3. 记录工具执行完毕与结果
                cafe_tool_end_log(name, result, duration)
                return result
            except Exception as e:
                duration = (time.perf_counter() - start_t) * 1000
                cafe_tool_end_log(name, f"Exception: {str(e)}", duration)
                raise e

        ToolRegistry.execute = patched_execute

        # 2. 深度拦截 Agent Skills (SkillsLoader)
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
