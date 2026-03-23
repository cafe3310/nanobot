"""上下文金库 (Vault) 补丁。
修正路径规范：统一使用 memory/MEMORY.md 结构。
实现层级化叠加：Vault (核心) + Workspace (扩展)。
"""

import json
from cafeext.py.wrapper.config import VAULT_DIR

def apply_context_patch():
    """注入符合官方路径规范的层级化上下文补丁。"""
    try:
        # 1. 拦截 ContextBuilder (引导文件叠加 - 位于根目录)
        import nanobot.agent.context
        ContextBuilder = nanobot.agent.context.ContextBuilder
        
        def patched_load_bootstrap(self):
            parts = []
            for filename in self.BOOTSTRAP_FILES:
                vault_path = VAULT_DIR / filename
                workspace_path = self.workspace / filename
                if vault_path.exists():
                    content = vault_path.read_text(encoding="utf-8")
                    parts.append(f"## 🛡️ [VAULT] {filename}\n*(Priority memory, strictly follow)*\n\n{content}")
                if workspace_path.exists():
                    content = workspace_path.read_text(encoding="utf-8")
                    parts.append(f"## 📄 [WORKSPACE] {filename}\n\n{content}")
            return "\n\n".join(parts) if parts else ""
        ContextBuilder._load_bootstrap_files = patched_load_bootstrap

        # 2. 拦截 MemoryStore (记忆层叠加 - 位于 memory/ 目录)
        import nanobot.agent.memory
        MemoryStore = nanobot.agent.memory.MemoryStore
        
        original_memory_init = MemoryStore.__init__
        def patched_memory_init(self, workspace):
            original_memory_init(self, workspace)
            # 重定向核心写入口至 Vault (记忆金库)
            self.memory_dir = VAULT_DIR / "memory"
            self.memory_dir.mkdir(parents=True, exist_ok=True)
            self.memory_file = self.memory_dir / "MEMORY.md"
            self.history_file = self.memory_dir / "HISTORY.md"
            # 记录工作区记忆路径用于读取
            self.workspace_memory_file = workspace / "memory" / "MEMORY.md"
        MemoryStore.__init__ = patched_memory_init

        def patched_get_memory_context(self):
            all_memories = []
            
            # A. 核心层: Vault 长期记忆 (优先级最高)
            if self.memory_file.exists():
                content = self.read_long_term().strip()
                if content: all_memories.append(f"### 🧠 [VAULT-MEMORY]\n{content}")
            
            # B. 扩展层: Workspace 长期记忆 (优先级次之)
            if hasattr(self, "workspace_memory_file") and self.workspace_memory_file.exists():
                content = self.workspace_memory_file.read_text(encoding="utf-8").strip()
                if content: all_memories.append(f"### 📄 [WORKSPACE-MEMORY]\n{content}")
            
            return "# Memory\n\n" + "\n\n".join(all_memories) if all_memories else ""
        MemoryStore.get_memory_context = patched_get_memory_context

        # 3. 拦截 SkillsLoader
        import nanobot.agent.skills
        SkillsLoader = nanobot.agent.skills.SkillsLoader
        current_list_skills = SkillsLoader.list_skills
        def vault_list_skills(self, *args, **kwargs):
            skills = current_list_skills(self, *args, **kwargs)
            vault_skills_dir = VAULT_DIR / "skills"
            if vault_skills_dir.exists():
                for skill_dir in vault_skills_dir.iterdir():
                    if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                        existing = next((s for s in skills if s["name"] == skill_dir.name), None)
                        if existing:
                            existing["path"] = str(skill_dir / "SKILL.md")
                            existing["source"] = "vault (override)"
                        else:
                            skills.append({"name": skill_dir.name, "path": str(skill_dir / "SKILL.md"), "source": "vault"})
            return skills
        SkillsLoader.list_skills = vault_list_skills
        
    except Exception as e:
        print(f"Warning: Failed to apply standard context patch: {e}")

