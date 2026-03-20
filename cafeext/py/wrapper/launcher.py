import sys
from pathlib import Path

# 获取当前脚本的绝对路径
# 结构：cafeext/py/wrapper/launcher.py
wrapper_dir = Path(__file__).parent.absolute()
cafeext_dir = wrapper_dir.parent.parent.absolute()
project_root = cafeext_dir.parent.absolute()

# 将项目根目录加入 Python 路径，确保能导入 nanobot 核心包
sys.path.insert(0, str(project_root))

from nanobot.config.loader import set_config_path
from nanobot.cli.commands import app

def main():
    # 锁定配置和工作区到 cafeext 目录下
    config_path = cafeext_dir / "config.json"
    workspace_path = cafeext_dir / "workspace"
    
    # 设置 nanobot 的全局配置路径
    set_config_path(config_path)
    
    # 自动注入 workspace 路径给 onboard 命令
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        if "--workspace" not in sys.argv and "-w" not in sys.argv:
            sys.argv.extend(["--workspace", str(workspace_path)])
            
    # 启动 nanobot
    app()

if __name__ == "__main__":
    main()
