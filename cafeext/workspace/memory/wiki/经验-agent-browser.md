# 经验-agent-browser

### 任务：在 agent-browser 中打开 Wikipedia 的 Dog 条目并查看页面内容

- **任务描述**：使用 agent-browser 打开指定页面，验证页面加载，提取页面摘要信息，并将操作经验记录到记忆库。
- **最终方案**：
  1. 使用 `agent-browser open <url>` 打开页面（推荐加上 `--headed` 以确保窗口可见）。如果 daemon 已运行且需要更改窗口模式，先执行 `agent-browser close` 再重新打开。
  2. 等待页面加载后，可用 `agent-browser snapshot --compact` 获取页面的可访问性树（accessibility tree），便于查看页面结构和关键文本。
  3. 如需翻页或滚动，可使用 `agent-browser press PageDown` 或 `scroll` 命令。
  4. 若需要提取文本，可结合 `web_fetch` 作为备选（当 agent-browser 不支持直接导出全文时）。
- **遇到的坑**：
  - 直接调用 `agent-browser` 作为工具名会报错，必须通过 `exec` 执行其 CLI 命令。
  - `--headed` 参数在 daemon 已运行的情况下会被忽略，需要先关闭浏览器再重新打开。
  - `extract` 和 `read` 不是有效命令，正确的查看结构命令是 `snapshot`（或 `get text` 按元素）。
- **核心秘籍**：
  - 用 `exec` 调用 agent-browser CLI，并在需要可视化时加上 `--headed`；
  - 用 `snapshot --compact` 快速获取页面结构文本；
  - 需要翻页时用 `press PageDown` 或 `scroll`；
  - 遇到 daemon 状态导致的参数被忽略时，先 `agent-browser close` 再重新打开。

记录时间：2026-03-25 15:33（CST）
上下文：用户要求打开 Wikipedia Dog 页面、查看内容并记录高级经验。