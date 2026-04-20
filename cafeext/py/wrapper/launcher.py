"""
=== cafe3310 nanobot sidecar function ===
注入点：Sidecar 启动入口，拦截并注入 nanobot.cli.commands.app, nanobot.config.loader 及 OpenAICompatProvider.chat。
作用：初始化 Sidecar 运行环境，注入安全策略与各项 Patch，提供 nb config/logs/doctor 等增强指令，并劫持 OpenAI 兼容 Provider 实现全链路日志审计。
=== end(keep this block) ===
"""

import sys
import os
import json
import subprocess
import shutil
from pathlib import Path
from functools import wraps
from datetime import datetime

# 获取项目根目录
wrapper_dir = Path(__file__).parent.absolute()
cafeext_dir = wrapper_dir.parent.parent.absolute()
project_root = cafeext_dir.parent.absolute()


# 将项目根目录加入 Python 路径
sys.path.insert(0, str(project_root))

# --- [极早期的安全补丁] ---
# 必须在从 nanobot 导入任何内容之前执行，以防止原版类被缓存
try:
    from cafeext.py.wrapper.security import apply_security_policy
    apply_security_policy()
    
    from cafeext.py.wrapper.context_patch import apply_context_patch
    apply_context_patch()

    from cafeext.py.wrapper.skill_patch import apply_skill_patch
    apply_skill_patch()

    from cafeext.py.wrapper.prompt_patch import apply_prompt_patch
    apply_prompt_patch()

    from cafeext.py.wrapper.subagent_patch import apply_subagent_patch
    apply_subagent_patch()

    from cafeext.py.wrapper.error_patch import apply_error_patch
    apply_error_patch()

    from cafeext.py.wrapper.image_gen import apply_image_gen_patch
    apply_image_gen_patch()

    from cafeext.py.wrapper.model_patch import apply_model_patch
    apply_model_patch()
except Exception as e:
    print(f"Critical Warning: Security policy injection failed early: {e}")
# -------------------------

from cafeext.py.wrapper.config import (
    VAULT_DIR, WORKSPACE_DIR, LOG_DIR, CONFIG_JSON_PATH, DOTENV_PATH, CAFEEXT_DIR
)
from nanobot.config.loader import set_config_path, load_config
from nanobot.cli.commands import app
import typer

def load_dotenv(path: Path):
    if not path.exists():
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"\'')

def setup_injection():
    """核心注入逻辑：配置、Key 与 日志拦截"""
    config_path = CONFIG_JSON_PATH
    workspace_path = WORKSPACE_DIR
    vault_path = VAULT_DIR
    session_path = workspace_path / "sessions"
    log_dir = LOG_DIR
    
    # 修正 Typer 显示名称和描述
    app.info.name = "nb"
    app.info.help = f"🐈 nanobot [Sidecar Active: {cafeext_dir}]"

    # 1. 注入配置与 Key
    try:
        config = load_config(config_path)
        custom_key = os.environ.get("CUSTOM_API_KEY")
        if custom_key and hasattr(config.providers, 'custom'):
            config.providers.custom.api_key = custom_key
        discord_token = os.environ.get("DISCORD_TOKEN")
        if discord_token:
            discord_cfg = getattr(config.channels, 'discord', None)
            if isinstance(discord_cfg, dict):
                discord_cfg["token"] = discord_token
                
        # 注入 Vault MCP (金库级 MCP)
        vault_mcp_path = vault_path / "mcp.json"
        if vault_mcp_path.exists():
            with open(vault_mcp_path, "r", encoding="utf-8") as f:
                vault_mcp = json.load(f)
                if isinstance(vault_mcp, dict):
                    for name, server_data in vault_mcp.items():
                        config.tools.mcp_servers[name] = server_data

        import nanobot.config.loader
        nanobot.config.loader.load_config = lambda *args, **kwargs: config
    except Exception as e:
        print(f"Warning: Config injection failed: {e}")

    # 2. 注入 Sidecar 便捷命令 (并分组)
    panel_name = "Sidecar (Custom)"
    
    @app.command(name="config", help="Open private config.json with Zed", rich_help_panel=panel_name)
    def open_config():
        print(f"Opening {config_path} with Zed...")
        subprocess.run(["zed", str(config_path)])

    @app.command(name="workspace", help="Open private workspace in Finder", rich_help_panel=panel_name)
    def open_workspace():
        print(f"Opening {workspace_path} in Finder...")
        subprocess.run(["open", str(workspace_path)])

    @app.command(name="vault", help="Open private vault in Finder", rich_help_panel=panel_name)
    def open_vault():
        print(f"Opening {vault_path} in Finder...")
        subprocess.run(["open", str(vault_path)])

    @app.command(name="doctor", help="Check and initialize missing Sidecar files/dirs", rich_help_panel=panel_name)
    def run_doctor():
        """Sidecar 环境健康检查与初始化"""
        print("\n🩺 [Sidecar Doctor] Checking environment...")
        print(f"  - Config:    {CONFIG_JSON_PATH}")
        print(f"  - Workspace: {WORKSPACE_DIR}")
        print(f"  - Vault:     {VAULT_DIR}")
        
        missing = []
        # 检查金库目录
        if not VAULT_DIR.exists(): missing.append(("dir", VAULT_DIR))
        
        # 检查金库核心文件
        vault_files = [
            "AGENTS.md", "HEARTBEAT.md", "SOUL.md", "USER.md", "TOOLS.md",
            "memory/MEMORY.md", "memory/HISTORY.md", "mcp.json"
        ]
        for f in vault_files:
            p = VAULT_DIR / f
            if not p.exists(): missing.append(("file", p))
            
        # 检查工作区目录
        for d in ["sessions", "skills", "memory"]:
            p = WORKSPACE_DIR / d
            if not p.exists(): missing.append(("dir", p))

        if not missing:
            print("\n✅ All systems go! Your environment is complete.")
            return

        print("\n⚠️  Found missing items:")
        for type, path in missing:
            print(f"  [{type}] {path}")

        if typer.confirm("\nWould you like me to initialize these missing items?"):
            for type, path in missing:
                if type == "dir":
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"  Created directory: {path.name}")
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.touch()
                    if path.name == "mcp.json":
                        path.write_text("{}", encoding="utf-8")
                    print(f"  Created file: {path.name}")
            print("\n✨ Initialization complete.")
        else:
            print("\nAborted. Please manually create the missing items.")

    @app.command(name="logs", help="Tail the latest inference logs", rich_help_panel=panel_name)
    def tail_logs():
        log_files = sorted(log_dir.glob("*.log"))
        if not log_files:
            print(f"No log files found in {log_dir}")
            return
        latest_log = log_files[-1]
        print(f"Tailing latest log: {latest_log.name}")
        try:
            subprocess.run(["tail", "-f", "-n", "20", str(latest_log)])
        except KeyboardInterrupt:
            print("\nStopped tailing logs.")

    @app.command(name="reset", help="Clear session history", rich_help_panel=panel_name)
    def reset_data():
        if session_path.exists():
            print(f"Clearing sessions in {session_path}...")
            shutil.rmtree(session_path)
            session_path.mkdir(parents=True, exist_ok=True)
        print("Done. Bot memory is now fresh.")

    # 3. 拦截 OpenAICompatProvider 以捕获日志
    try:
        from nanobot.providers.openai_compat_provider import OpenAICompatProvider
        from cafeext.py.callbacks.logger import cafe_input_callback, cafe_success_callback, cafe_failure_callback
        
        def create_patched_chat(original_method):
            @wraps(original_method)
            async def patched_chat(self, *args, **kwargs):
                messages = kwargs.get("messages") or (args[0] if len(args) > 0 else [])
                tools = kwargs.get("tools") or (args[1] if len(args) > 1 else None)
                log_kwargs = {
                    "model": kwargs.get("model") or getattr(self, "default_model", "unknown"),
                    "api_base": self.api_base,
                    "additional_args": {"complete_input_dict": {"messages": messages, "tools": tools}}
                }
                cafe_input_callback(log_kwargs)
                start_time = datetime.now()
                try:
                    response = await original_method(self, *args, **kwargs)
                    cafe_success_callback(log_kwargs, response, start_time, datetime.now())
                    return response
                except Exception as e:
                    cafe_failure_callback(log_kwargs, e, start_time, datetime.now())
                    raise e
            return patched_chat

        OpenAICompatProvider.chat = create_patched_chat(OpenAICompatProvider.chat)
        OpenAICompatProvider.chat_stream = create_patched_chat(OpenAICompatProvider.chat_stream)

    except Exception as e:
        print(f"Warning: OpenAICompatProvider log injection failed: {e}")

def main():
    load_dotenv(DOTENV_PATH)
    set_config_path(CONFIG_JSON_PATH)
    setup_injection()
    
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        if "--workspace" not in sys.argv and "-w" not in sys.argv:
            sys.argv.extend(["--workspace", str(WORKSPACE_DIR)])
    app()

if __name__ == "__main__":
    main()
