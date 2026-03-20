"""安全策略常量定义与拦截逻辑。"""

# 禁用列表定义 (使用代码中的真实工具名)
DISABLED_SKILLS = ["clawhub"]
DISABLED_TOOLS = ["exec", "spawn"]

def apply_security_policy():
    """通过 Monkey Patch 强制执行安全策略。"""
    try:
        # 1. 深度拦截 Agent Skills (SkillsLoader)
        from nanobot.agent.skills import SkillsLoader
        
        # 拦截 1: 屏蔽列表显示
        original_list_skills = SkillsLoader.list_skills
        def patched_list_skills(self, *args, **kwargs):
            skills = original_list_skills(self, *args, **kwargs)
            return [s for s in skills if s["name"] not in DISABLED_SKILLS]
        SkillsLoader.list_skills = patched_list_skills
        
        # 拦截 2: 屏蔽内容读取 (这是核心安全开关，确保 load_skill 返回 None)
        original_load_skill = SkillsLoader.load_skill
        def patched_load_skill(self, name):
            if name in DISABLED_SKILLS:
                return None
            return original_load_skill(self, name)
        SkillsLoader.load_skill = patched_load_skill
        
        # 拦截 3: 屏蔽元数据 (确保 build_skills_summary 看不到它)
        original_get_meta = SkillsLoader.get_skill_metadata
        def patched_get_meta(self, name):
            if name in DISABLED_SKILLS:
                return None
            return original_get_meta(self, name)
        SkillsLoader.get_skill_metadata = patched_get_meta

        # 2. 禁用 核心工具 (Tools) - 动态拦截注册行为
        from nanobot.agent.tools.registry import ToolRegistry
        original_register = ToolRegistry.register
        def patched_register(self, tool):
            if tool.name in DISABLED_TOOLS:
                return
            return original_register(self, tool)
        ToolRegistry.register = patched_register
        
    except Exception as e:
        print(f"Warning: Failed to apply security policy: {e}")
