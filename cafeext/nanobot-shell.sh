#!/bin/bash

# 穿透软链接获取脚本真实的物理路径
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do 
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" 
done
CAFEEXT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

# 获取项目根目录 (cafeext 的上级)
PROJECT_ROOT="$( dirname "$CAFEEXT_DIR" )"

VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
LAUNCHER_PY="$CAFEEXT_DIR/py/wrapper/launcher.py"

# 检查虚拟环境
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment python not found at $PROJECT_ROOT/.venv"
    echo "Current CAFEEXT_DIR: $CAFEEXT_DIR"
    exit 1
fi

# 打印执行诊断信息
echo -e "\033[0;34m[nb-shell] Project Root:\033[0m $PROJECT_ROOT"
echo -e "\033[0;34m[nb-shell] Config Dir:  \033[0m $CAFEEXT_DIR"
echo -e "\033[0;34m[nb-shell] Executing:   \033[0m nanobot $@"
echo ""

# 启动附加包封装的 nanobot
"$VENV_PYTHON" "$LAUNCHER_PY" "$@"
