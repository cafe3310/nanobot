#!/bin/zsh

# 自动定位项目根目录 (相对于此脚本位置: scripts/../.. -> restart-bot/..)
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../../../.." && pwd )"
NB_SHELL="$PROJECT_ROOT/cafeext/nanobot-shell.sh"

TARGET_PID=$1

if [ -z "$TARGET_PID" ]; then
    echo "Error: No PID provided."
    exit 1
fi

echo "--- Bot Restart Sequence Started ---"
echo "Target PID: $TARGET_PID"
echo "NB Shell:   $NB_SHELL"

echo "1/3: Waiting 5s before killing PID $TARGET_PID..."
sleep 5
kill -9 $TARGET_PID || echo "PID $TARGET_PID already gone."

echo "2/3: Waiting 5s before 'nb reset'..."
sleep 5
"$NB_SHELL" reset

echo "3/3: Waiting 5s before 'nb gateway'..."
sleep 5
"$NB_SHELL" gateway

echo "--- Restart Completed ---"
