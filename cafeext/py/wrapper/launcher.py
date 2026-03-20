import sys
import os
from pathlib import Path

# 获取当前脚本的绝对路径
wrapper_dir = Path(__file__).parent.absolute()
cafeext_dir = wrapper_dir.parent.parent.absolute()
project_root = cafeext_dir.parent.absolute()

# 将项目根目录加入 Python 路径
sys.path.insert(0, str(project_root))

from nanobot.config.loader import set_config_path
from nanobot.cli.commands import app

def load_dotenv(path: Path):
    """简易的 .env 加载器，避免引入额外依赖"""
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
    # 1. 加载私有密钥
    load_dotenv(cafeext_dir / ".env")
    
    # 2. 锁定配置和工作区
    config_path = cafeext_dir / "config.json"
    workspace_path = cafeext_dir / "workspace"
    set_config_path(config_path)
    
    # 3. 自动注入参数
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        if "--workspace" not in sys.argv and "-w" not in sys.argv:
            sys.argv.extend(["--workspace", str(workspace_path)])
            
    app()

if __name__ == "__main__":
    main()
