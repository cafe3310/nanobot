import sys
import os
from pathlib import Path

# 获取项目根目录
wrapper_dir = Path(__file__).parent.absolute()
cafext_dir = wrapper_dir.parent.parent.absolute()
project_root = cafext_dir.parent.absolute()

# 将项目根目录加入 Python 路径
sys.path.insert(0, str(project_root))

from nanobot.config.loader import set_config_path, load_config
from nanobot.cli.commands import app

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

def main():
    # 1. 加载 .env 到环境变量
    load_dotenv(cafext_dir / ".env")
    
    # 2. 锁定配置路径
    config_path = cafext_dir / "config.json"
    workspace_path = cafext_dir / "workspace"
    set_config_path(config_path)
    
    # 3. [注入逻辑] 
    try:
        config = load_config(config_path)
        custom_key = os.environ.get("CUSTOM_API_KEY")
        
        # Pydantic v2 使用 snake_case 字段名: api_key
        if custom_key and hasattr(config.providers, 'custom'):
            config.providers.custom.api_key = custom_key
            
        # 针对 Discord Token 等其它环境变量的扩展注入也可以放在这里
        # if os.environ.get("DISCORD_TOKEN"):
        #     config.channels.discord.token = os.environ.get("DISCORD_TOKEN")

        # 猴子补丁拦截 nanobot 的配置加载
        import nanobot.config.loader
        nanobot.config.loader.load_config = lambda *args, **kwargs: config
    except Exception as e:
        # 失败时不中断，让其尝试使用默认流程
        print(f"Warning: Sidecar config injection failed: {e}")

    # 4. 自动注入参数
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        if "--workspace" not in sys.argv and "-w" not in sys.argv:
            sys.argv.extend(["--workspace", str(workspace_path)])
            
    # 启动
    app()

if __name__ == "__main__":
    main()
