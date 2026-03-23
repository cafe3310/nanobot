"""上下文金库 (Vault) 补丁。
实现全方位的层级化叠加架构：Vault (核心/优先) + Workspace (扩展/次之)。
"""

import json
from cafeext.py.wrapper.config import VAULT_DIR

def apply_context_patch():
    """注入全方位的层级化上下文补丁。"""
    try:
        # 确保基础目录存在
        VAULT_DIR.mkdir(parents=True, exist_ok=True)
        (VAULT_DIR / "skills").mkdir(parents=True, exist_ok=True)
        
        # 1. 拦截 ContextBuilder (Bootstrap 层级叠加)
        import nanobot.agent.context
        ContextBuilder = nanobot.agent.context.ContextBuilder
        
        def patched_load_bootstrap(self):
            parts = []
            for filename in self.BOOTSTRAP_FILES:
                vault_path = VAULT_DIR / filename
                workspace_path = self.workspace / filename
                
                # 情况 A: 核心层 (Vault)
                if vault_path.exists():
                    content = vault_path.read_text(encoding="utf-8")
                    parts.append(f"## 🛡️ [CORE AUTHORITY] {filename}\n*(This is your primary directive, strictly follow it)*\n\n{content}")
                
                # 情况 B: 扩展层 (Workspace)
                if workspace_path.exists():
                    content = workspace_path.read_text(encoding="utf-8")
                    prefix = "📄 [EXTENDED CONTEXT]" if vault_path.exists() else "📄 [WORKSPACE]"
                    parts.append(f"## {prefix} {filename}\n\n{content}")
                    
            return "\n\n".join(parts) if parts else ""
        ContextBuilder._load_bootstrap_files = patched_load_bootstrap

        # 2. 拦截 MemoryStore (记忆层全方位双层叠加)
        import nanobot.agent.memory
        MemoryStore = nanobot.agent.memory.MemoryStore
        
        original_memory_init = MemoryStore.__init__
        def patched_memory_init(self, workspace):
            original_memory_init(self, workspace)
            # 强制将写入口锁定为金库中的 BOT.md
            self.memory_file = VAULT_DIR / "BOT.md"
        MemoryStore.__init__ = patched_memory_init

        def patched_get_memory_context(self):
            all_memories = []
            
            # 辅助函数: 安全读取并注入
            def inject_if_exists(path, label):
                if path.exists():
                    content = path.read_text(encoding="utf-8").strip()
                    if content:
                        all_memories.append(f"### {label}\n{content}")

            # A. Experience (BOT.md) - 金库核心优先，工作区扩展次之
            inject_if_exists(VAULT_DIR / "BOT.md", "🧠 [PRIMARY EXPERIENCE] (vault/BOT.md)")
            inject_if_exists(self.workspace / "memory" / "BOT.md", "📄 [EXTENDED EXPERIENCE] (workspace/memory/BOT.md)")
            
            # B. Facts (MEMORY.md) - 金库核心优先，工作区扩展次之
            inject_if_exists(VAULT_DIR / "MEMORY.md", "🛡️ [CORE FACTS] (vault/MEMORY.md)")
            inject_if_exists(self.workspace / "memory" / "MEMORY.md", "📄 [EXTENDED FACTS] (workspace/memory/MEMORY.md)")
            
            return "# Memory\n\n" + "\n\n".join(all_memories) if all_memories else ""
        MemoryStore.get_memory_context = patched_get_memory_context

        # 3. 拦截 SkillsLoader (金库 Skills 叠加)
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
                            skills.append({
                                "name": skill_dir.name,
                                "path": str(skill_dir / "SKILL.md"),
                                "source": "vault"
                            })
            return skills
        SkillsLoader.list_skills = vault_list_skills
        
    except Exception as e:
        print(f"Warning: Failed to apply full hierarchical context patch: {e}")
