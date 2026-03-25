---
name: restart-bot
description: "重启 Bot 的技能。通过脚本化方案，在新的 Kitty 窗口执行获取 PID -> kill -> nb reset -> nb gateway 的标准重启序列。在加载新配置或运行异常时使用。"
---

# Bot 重启指南 (Restart Bot)

为了确保重启过程的稳健性，此技能将逻辑封装在专用的重启脚本中。

## 1. 获取当前 PID
在 Python 工具调用中获取当前 Bot 进程的 PID：
```python
import os
pid = os.getpid()
```

## 2. 在 Kitty 窗口中执行重启脚本
你可以通过 `open` 命令，利用技能目录下的 `scripts/restart.sh` 来完成整个 5s-5s-5s 序列：

```bash
# <skill_dir> 为该技能的根目录
open -n -a Kitty.app --args zsh -c "<skill_dir>/scripts/restart.sh <PID>"
```

该脚本将自动执行：
1. 等待 5 秒后，`kill -9 <PID>`
2. 等待 5 秒后，调用 `nanobot-shell.sh reset`
3. 等待 5 秒后，调用 `nanobot-shell.sh gateway`

## 关键事项
- **路径自寻**: 该脚本内置了相对于项目的路径发现逻辑，不需要手动配置 `nb` 别名。
- **环境一致**: 脚本直接通过绝对路径调用虚拟环境包装器，确保重启后的 Bot 配置和当前环境一致。

