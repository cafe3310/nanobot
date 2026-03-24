# 经验-macOS自动化

### 任务：打开 Finder 并跳转到特定系统目录 (2026-03-24)

- **任务描述**: 通过自动化指令打开 Finder 窗口并直接导航到「下载 (Downloads)」文件夹。
- **遇到的坑**: 
    - 尝试使用 `folder "Downloads" of home folder`：报错错误码 -1728（找不到对象）。
    - 尝试使用 `folder "Downloads" of folder "Users" of startup disk`：路径解析逻辑在不同系统环境下极不稳定。
- **最终方案**: 
    使用 AppleScript 提供的原生路径函数是最稳健的方案：
    ```bash
    osascript -e 'tell application "Finder" to set target of front window to (path to downloads folder as text)'
    ```
- **核心秘籍**: 在涉及 macOS 系统目录（如下载、桌面、文档）的操作时，**永远优先使用 `(path to ... folder)` 语法**，它能自动处理不同用户的家目录名，且不会因为路径字符串的细微差异而失效。
