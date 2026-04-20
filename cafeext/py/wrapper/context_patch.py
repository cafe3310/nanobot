"""
=== cafe3310 nanobot sidecar function ===
注入点：拦截 nanobot.agent.context.ContextBuilder 与 nanobot.agent.memory.MemoryStore。
作用：实现层级化上下文叠加（Vault 提供长期核心设定，Workspace 提供临时事实），并将 Memory 物理存储重定向至 Vault 目录，确保多项目共用核心记忆。
=== end(keep this block) ===
"""

import json
from cafeext.py.wrapper.config import VAULT_DIR

def apply_context_patch():
    """注入全量对齐的层级化上下文补丁。"""
    try:
        # 1. 拦截并补强 ContextBuilder
        import nanobot.agent.context
        ContextBuilder = nanobot.agent.context.ContextBuilder
        
        # 显式扩展引导文件清单
        ContextBuilder.BOOTSTRAP_FILES = ["AGENTS.md", "HEARTBEAT.md", "SOUL.md", "USER.md", "TOOLS.md"]
        
        # (原 Identity 补丁已迁移至 prompt_patch.py)
        
        def patched_load_bootstrap(self):
            parts = []
            for filename in self.BOOTSTRAP_FILES:
                vault_path = VAULT_DIR / filename
                workspace_path = self.workspace / filename
                
                # A. 固定记忆层 (Vault)
                if vault_path.exists():
                    content = vault_path.read_text(encoding="utf-8")
                    parts.append(f"## 🛡️ [VAULT] {filename}\n*(Priority memory, strictly follow)*\n\n{content}")
                
                # B. 工作区层 (Workspace)
                if workspace_path.exists():
                    content = workspace_path.read_text(encoding="utf-8")
                    parts.append(f"## 📄 [WORKSPACE] {filename}\n\n{content}")
                    
            return "\n\n".join(parts) if parts else ""
        ContextBuilder._load_bootstrap_files = patched_load_bootstrap

        # 2. 拦截并重定向 MemoryStore
        import nanobot.agent.memory
        MemoryStore = nanobot.agent.memory.MemoryStore
        
        original_init = MemoryStore.__init__
        def patched_init(self, workspace):
            original_init(self, workspace)
            # 统一写入口至金库
            self.memory_dir = VAULT_DIR / "memory"
            self.memory_dir.mkdir(parents=True, exist_ok=True)
            self.memory_file = self.memory_dir / "MEMORY.md"
            self.history_file = self.memory_dir / "HISTORY.md"
            # 记录工作区记忆路径用于叠加读取
            self.workspace_memory_file = workspace / "memory" / "MEMORY.md"
        MemoryStore.__init__ = patched_init

        def patched_get_memory_context(self):
            all_memories = []
            def inject_if_exists(path, label):
                if path.exists():
                    content = path.read_text(encoding="utf-8").strip()
                    if content: all_memories.append(f"### {label}\n{content}")

            # 经验记忆层叠加
            inject_if_exists(VAULT_DIR / "memory" / "MEMORY.md", "🧠 [VAULT-MEMORY]")
            inject_if_exists(self.workspace_memory_file, "📄 [WORKSPACE-MEMORY]")
            
            return "# Memory\n\n" + "\n\n".join(all_memories) if all_memories else ""
        MemoryStore.get_memory_context = patched_get_memory_context

        # (原 SkillsLoader 补丁已迁移至 skill_patch.py)
        
    except Exception as e:
        print(f"Warning: Failed to apply fully aligned context patch: {e}")
