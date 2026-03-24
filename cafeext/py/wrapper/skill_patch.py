"""技能覆盖补丁 (Skill Override Patch)。
支持严格优先级加载: vault/skill-override > vault/skills > builtin_skills > workspace/skills
"""

from cafeext.py.wrapper.config import VAULT_DIR

def apply_skill_patch():
    try:
        import nanobot.agent.skills
        SkillsLoader = nanobot.agent.skills.SkillsLoader
        
        OVERRIDE_DIR = VAULT_DIR / "skill-override"
        VAULT_SKILLS_DIR = VAULT_DIR / "skills"

        def patched_list_skills(self, filter_unavailable: bool = True):
            """重写 list_skills 以按照严格优先级收集技能，并去重。"""
            skills_dict = {} # 用于去重，key为name
            
            # 辅助函数，按优先级添加技能
            def add_skills_from_dir(directory, source_label):
                if directory and directory.exists():
                    for skill_dir in directory.iterdir():
                        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                            name = skill_dir.name
                            if name not in skills_dict:
                                skills_dict[name] = {
                                    "name": name,
                                    "path": str(skill_dir / "SKILL.md"),
                                    "source": source_label
                                }

            # 优先级顺序：override > vault > builtin > workspace
            add_skills_from_dir(OVERRIDE_DIR, "vault-override")
            add_skills_from_dir(VAULT_SKILLS_DIR, "vault")
            add_skills_from_dir(self.builtin_skills, "builtin")
            add_skills_from_dir(self.workspace_skills, "workspace")

            skills = list(skills_dict.values())

            if filter_unavailable:
                return [s for s in skills if self._check_requirements(self._get_skill_meta(s["name"]))]
            return skills

        def patched_load_skill(self, name: str):
            """重写 load_skill 以按照严格优先级读取技能内容。"""
            # 1. vault/skill-override
            override_skill = OVERRIDE_DIR / name / "SKILL.md"
            if override_skill.exists():
                return override_skill.read_text(encoding="utf-8")
                
            # 2. vault/skills
            vault_skill = VAULT_SKILLS_DIR / name / "SKILL.md"
            if vault_skill.exists():
                return vault_skill.read_text(encoding="utf-8")
                
            # 3. builtin_skills
            if self.builtin_skills:
                builtin_skill = self.builtin_skills / name / "SKILL.md"
                if builtin_skill.exists():
                    return builtin_skill.read_text(encoding="utf-8")
                    
            # 4. workspace/skills
            workspace_skill = self.workspace_skills / name / "SKILL.md"
            if workspace_skill.exists():
                return workspace_skill.read_text(encoding="utf-8")
                
            return None

        SkillsLoader.list_skills = patched_list_skills
        SkillsLoader.load_skill = patched_load_skill

    except Exception as e:
        print(f"Warning: Failed to apply skill override patch: {e}")
