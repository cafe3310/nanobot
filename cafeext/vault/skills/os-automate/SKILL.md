---
name: os-automate
description: "macOS 原生 UI 自动化技能。使用 Peekaboo 工具集操作 Finder、菜单栏、系统设置及各类原生应用。"
---

# macOS 自动化指南 (Peekaboo)

作为我的 macOS 自动化核心，你可以使用渐进式指南来操作电脑，完成任务。

最关键事项：

1. 先定位，再操作。先了解你要操作什么 app, 然后在后续的命令上通过 --app 指定目标。
2. 先看帮助，再执行。对任何命令，先加 --help 看看需要哪些参数。

## 1. 快速定位操作文档 (Action Map)

你可以根据下表，读取详细步骤文档：

- **操作应用与窗口**: 见 `<skill_dir>/peekaboo/commands/app.md` 和 `<skill_dir>/peekaboo/commands/window.md`。
- **处理系统弹窗**: 见 `<skill_dir>/peekaboo/commands/dialog.md`。
- **管理剪贴板**: 见 `<skill_dir>/peekaboo/commands/clipboard.md`。
- **控制 Dock 栏**: 见 `<skill_dir>/peekaboo/commands/dock.md`。
- **多显示器/桌面空间**: 见 `<skill_dir>/peekaboo/commands/space.md`。
- **高级手势 (拖拽/滑动)**: 见 `<skill_dir>/peekaboo/commands/drag.md` 和 `<skill_dir>/peekaboo/commands/swipe.md`。

## 2. 精简指南 (快速开始)

这几个操作是最常见的。

### 检查环境与状态
- **列出窗口/应用**: `peekaboo list`(列出所有 app 和 pid) 找到目标应用的名称或窗口 id。
- **“看见”屏幕内容**: 执行 `peekaboo see --app "PID:<pid>" --window-id "<win_id>" --json` 它会给你生成一个带 elem_id 的 UI 地图。这是你进行后续点击的前提。

### 执行基本操作
- **点击元素**: 始终优先通过 `see` 获取的标签点击：`peekaboo click --app "PID:<pid>" --window-id "<win_id>" --id <elem_id>`。
- **输入文本**: `peekaboo type --app "PID:<pid>" --window-id "<win_id>" "内容"`。
- **操作菜单**: ，直接执行 `peekaboo menu list` 或 `peekaboo menu click "文件 > 保存"`。
- **使用快捷键**: `peekaboo hotkey cmd,shift,n`。

### 故障排除
- **找不到元素？**: 尝试 `peekaboo window focus "应用名"` 确保目标窗口在前台，然后重新 `see`。
- **命令报错？**: 先在命令后加 `--help` 查看参数规范，例如 `peekaboo click --help`。

## 3. 完整参考指南 (Escalation)

如果精简指南无法解决问题，或者你需要深入了解某个工具的底层逻辑，请按以下顺序操作：

1. **查阅总目录**: 读取 `os-automate/toc.md`，通过摘要定位最相关的文档。
2. **查阅命令速查**: 读取 `<skill_dir>/peekaboo/cli-command-reference.md` 获取全量命令清单。
3. **深入底层架构**: 如果你对执行效率或 TCC 权限有疑问，读取 `<skill_dir>/peekaboo/ARCHITECTURE.md` 和 `<skill_dir>/peekaboo/security.md`。

## 4. 最终准则

- **安全第一**: 在执行 `peekaboo run` 或任何涉及系统设置修改的操作前，确保你已经描述了清晰的意图，并等待主人的 HITL 拦截器确认。
- **文档先行**: 既然我们有如此详尽的文档库（位于 `os-automate/peekaboo/`），遇到不确定的参数，先 `read_file` 确认后再执行。
- **如果 Peekaboo 无法解决**: 诚实地告诉主人：“Peekaboo 目前无法识别该应用的自定义 UI 元素，我可能需要尝试使用 picc 视觉方案或寻求人工帮助。”
