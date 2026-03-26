---
name: memory
description: "具备基于 grep 召回机制的双层记忆系统（MEMORY.md 与 HISTORY.md），并集成「经验金库」功能，用于记录复杂的自动化实战经验与教训。当需要保存长期事实或记录任务成功经验时使用。"
always: true
---

# 核心记忆系统 (Memory & Experience Vault)

## 1. 结构化存储

- **长期事实**: `memory/MEMORY.md` — 存放用户偏好、项目背景、固定关系。始终加载进上下文。
- **事件日志**: `memory/HISTORY.md` — 追加式日志。不自动加载，需使用 `grep` 检索。
- **经验金库**: `memory/wiki/经验-{分类}.md` — 存放复杂的自动化实战经验。

## 2. 检索历史事件 (Search)

根据文件大小选择检索方式：
- **常规检索**: `grep -i "关键词" memory/HISTORY.md`
- **查看经验**: 在执行复杂任务前，习惯性检查 `ls memory/wiki/` 是否有相关的「经验-」文档。

## 3. 实战经验记录 (Experience Recording)

为了提高可靠性，在完成复杂的自动化任务（如多次尝试才成功）后，应主动记录：

- **内容结构**:
    1. **任务描述**: 简单描述目标。
    2. **遇到的坑 (Failed Attempts)**: 记录失败尝试与报错。
    3. **最终方案 (Successful Strategy)**: 贴出验证成功的代码/命令。
    4. **核心秘籍 (Key Takeaway)**: 总结最关键的知识点。

- **规范示例**:
    ```markdown
    # 经验-macOS自动化
    ### 任务：打开 Finder 下载目录 (2026-03-24)
    - **坑**: 直接拼接 `folder "Downloads"` 路径常因权限/语法报错。
    - **方案**: 使用 `osascript -e 'tell application "Finder" to open folder (path to downloads folder)'`。
    - **秘籍**: 优先使用系统内置路径函数 `(path to ... folder)`。
    ```

## 4. 自动固化

当会话增长到限制时，旧对话会自动总结并追加到 `HISTORY.md`，重要事实提取到 `MEMORY.md`。你只需负责手动记录「关键事实」和「实战经验」。
