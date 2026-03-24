"""技能补丁 (Skill Patch)。
支持严格优先级加载: vault/skills > builtin_skills > workspace/skills
"""

from cafeext.py.wrapper.config import VAULT_DIR

def apply_skill_patch():
    try:
        import nanobot.agent.skills
        SkillsLoader = nanobot.agent.skills.SkillsLoader
        
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

            # 优先级顺序：vault > builtin > workspace
            add_skills_from_dir(VAULT_SKILLS_DIR, "vault")
            add_skills_from_dir(self.builtin_skills, "builtin")
            add_skills_from_dir(self.workspace_skills, "workspace")

            skills = list(skills_dict.values())

            if filter_unavailable:
                return [s for s in skills if self._check_requirements(self._get_skill_meta(s["name"]))]
            return skills

        def patched_load_skill(self, name: str):
            """重写 load_skill 以按照严格优先级读取技能内容。"""
            # 1. vault/skills (最高优先级)
            vault_skill = VAULT_SKILLS_DIR / name / "SKILL.md"
            if vault_skill.exists():
                return vault_skill.read_text(encoding="utf-8")
                
            # 2. builtin_skills
            if self.builtin_skills:
                builtin_skill = self.builtin_skills / name / "SKILL.md"
                if builtin_skill.exists():
                    return builtin_skill.read_text(encoding="utf-8")
                    
            # 3. workspace/skills
            workspace_skill = self.workspace_skills / name / "SKILL.md"
            if workspace_skill.exists():
                return workspace_skill.read_text(encoding="utf-8")
                
            return None

        def patched_build_skills_summary(self) -> str:
            """重写 build_skills_summary 为更自然的 Markdown 列表格式，而非 XML。"""
            all_skills = self.list_skills(filter_unavailable=False)
            if not all_skills:
                return ""

            lines = ["# 模型技能(Agent Skills)\n"]
            lines.append("如果你发现自己不会做某件事，请**主动使用 `read_file` 工具**读取下表对应技能的 `SKILL.md` 文件。读取后你就会获得该领域的专业知识。")
            lines.append("**注意：不要尝试直接调用下表中的技能名称作为工具，它们只是存储在磁盘上的知识库。**\n")
            for s in all_skills:
                name = s["name"].lower()
                path = s["path"]
                desc = self._get_skill_description(s["name"])
                skill_meta = self._get_skill_meta(s["name"])
                available = self._check_requirements(skill_meta)

                status = "" if available else "(禁用)"
                lines.append(f"- {name}{status}: {desc}，位于 {path}")

            return "\n".join(lines)

        SkillsLoader.list_skills = patched_list_skills
        SkillsLoader.load_skill = patched_load_skill
        SkillsLoader.build_skills_summary = patched_build_skills_summary

    except Exception as e:
        print(f"Warning: Failed to apply skill patch: {e}")
