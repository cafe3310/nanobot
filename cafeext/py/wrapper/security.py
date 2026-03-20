"""安全策略常量定义与拦截逻辑。"""

# 禁用列表定义 (使用代码中的真实工具名)
DISABLED_SKILLS = ["clawhub"]
DISABLED_TOOLS = ["exec", "spawn"]

def apply_security_policy():
    """通过 Monkey Patch 强制执行安全策略。"""
    try:
        # 1. 禁用 Agent Skills
        from nanobot.agent.skills import SkillsLoader
        original_list_skills = SkillsLoader.list_skills
        
        def patched_list_skills(self, *args, **kwargs):
            skills = original_list_skills(self, *args, **kwargs)
            # 过滤掉禁用的技能
            return [s for s in skills if s["name"] not in DISABLED_SKILLS]
        
        SkillsLoader.list_skills = patched_list_skills
        
        # 2. 禁用 核心工具 (Tools) - 动态拦截注册行为
        from nanobot.agent.tools.registry import ToolRegistry
        original_register = ToolRegistry.register
        
        def patched_register(self, tool):
            if tool.name in DISABLED_TOOLS:
                # 拒绝注册危险工具
                return
            return original_register(self, tool)
            
        ToolRegistry.register = patched_register
        
        # 3. 针对已实例化对象的「补救式」清理 (双重保险)
        # 如果有些工具在拦截器加载前已经注入了某个全局注册表，这里可以手动清理
        # 但在我们的 launcher 流程中，setup_injection 发生在 app() 运行前，
        # 所以主要的拦截逻辑是在 (2) 中完成的。
        
    except Exception as e:
        print(f"Warning: Failed to apply security policy: {e}")
