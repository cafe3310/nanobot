---
name: experience-recorder
description: "Record successful automation experiences, task descriptions, and lessons learned into the 'Experience Vault' (经验金库). Use this after completing a complex task to ensure I don't make the same mistakes twice."
always: true
---

# 经验记录器 (Experience Recorder)

为了成为一个更可靠的助手，我需要在完成复杂的自动化任务后，主动总结并记录下我的「实战经验」。

## 我应该何时记录？

- 当我为了完成一个任务，尝试了多次工具调用才成功时。
- 当我发现某个特定的命令、路径或代码在当前系统环境下是「唯一正确解」时。
- 当用户显式要求我“记住这个操作”时。

## 记录规范

- **存储路径**: `memory/wiki/经验-{分类}.md` (例如：`memory/wiki/经验-macOS自动化.md`)
- **内容结构**:
    1. **任务描述**: 简单说一下刚才要做什么。
    2. **遇到的坑 (Failed Attempts)**: 记录失败的尝试、报错信息以及原因分析。
    3. **最终方案 (Successful Strategy)**: 贴出验证成功的完整代码或命令。
    4. **核心秘籍 (Key Takeaway)**: 用一句话总结最关键的那个知识点。

## 记录示例

```markdown
# 经验-macOS自动化

### 任务：打开 Finder 并跳转到下载目录 (2026-03-24)

- **遇到的坑**: 
    - 尝试 1: 直接拼接路径 `folder "Downloads" of home folder` 失败 (错误 -1728)。
    - 尝试 2: 使用硬编码路径 `folder "Downloads" of folder "Users" of startup disk` 失败 (权限/语法错误)。
- **最终方案**: 
    使用 AppleScript 的系统内置函数获取路径最为稳健：
    `osascript -e 'tell application "Finder" to set target of front window to (path to downloads folder as text)'`
- **核心秘籍**: 在 AppleScript 中，永远优先使用 `(path to ... folder)` 而不是手动构建路径字符串。
```

## 我应该如何回想？

在执行任何新的自动化任务前，我会习惯性地 `list_dir` 查看 `memory/wiki/` 目录下是否有前缀为 `经验-` 的文件。如果有相关的，我会先读一下，避免重蹈覆辙。
