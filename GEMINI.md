# 🐈 nanobot 开发与模型集成

## 背景与愿景

背景：用户希望基于现有的 `nanobot` 框架，接入自研的语言模型、推理模型及多模态模型，逐步扩展其功能。

核心目标：
1.  全功能化：通过集成多种模型，使 Bot 能够胜任各种复杂、有趣的实际任务。
2.  模型验证：在开发和运行过程中，通过真实场景发现自研模型的问题并挖掘其潜在优势。
3.  规范演进：采用 `doc-todo-log-loop` (基于日志记录驱动的轻量级项目开发和管理方案) 来严格管理项目的变更与文档，确保开发过程的可追溯性和知识沉淀。

## 重要文档

- [设计：nanobot 基础架构](./cafeext/docs/2026-03-18-16-54-设计-nanobot基础架构.md)
- [需求：模型对接与 Discord 接入](./cafeext/docs/2026-03-18-17-58-需求-模型对接与 Discord 接入.md)
- [需求：Bot 配置计划](./cafeext/docs/2026-03-18-19-37-需求-Bot配置计划.md)
- [定制：Sidecar 附加包启动器](./cafeext/docs/2026-03-20-20-12-定制功能-Sidecar附加包启动器.md)

## Agent Skills

在本项目开发中，我们将深度协同以下 Agent Skills：

`doc-todo-log-loop` -- 我们将以此作为定制开发的唯一管理性 skill。我们用 `cafeext/docs` 作为日志目录。

本项目的文档存储在 `cafeext/docs` 目录下，遵循 `YYYY-MM-DD-HH-mm-{类别}-{标题}.md` 的命名规范。

- 新增需求：请用户提出高阶目标，由 Gemini 撰写需求文档并拆分 TODO。
- 开始开发：由用户指派 TODO 任务后，Gemini 进入「开发与确认」循环。
- 记录日志：任务完成后，Gemini 记录开发日志。

注意事项

- 给文档标题取名时，避免浮夸，平和描述，忌用比喻。
- 写文档时描述平实具体，勿滥用大词，也忌用比喻。

## 工程准则 (Engineering Standards)

1. **严格使用外挂方案 (Sidecar Only)**：
   本项目禁止直接修改 `nanobot/` 核心目录下的源码。
   所有的定制化功能、逻辑补丁、Provider 劫持、工具注入或新命令实现，必须且只能在 `cafeext/` 目录下通过外挂模式实现。这确保了核心框架可以随时同步上游更新。

2. **外挂模块作用描述规范**：
   每个外挂模块（特别是 `cafeext/py/` 下的补丁脚本）必须在文件头部或核心注入逻辑上方，以固定的格式写明其技术原理。格式如下：

   ```text
   === cafe3310 nanobot sidecar function ===
   描述其注入点依赖（例如：拦截了哪个类、哪个方法、依赖了哪个内部模块）
   描述其作用（添加或改变了什么功能，解决了什么问题）
   === end(keep this block) ===
   ```

## 目录规范 (Directory Specs)

### `cafeext/` - 针对 Ling 系列模型的 Harness Plugin (附加包根目录)

这些模块本质上是针对自研 Ling 系列模型特化的 Harness Plugin。它们以「外挂模块」的形式存在，旨在不破坏上游核心框架的前提下，针对性地弥补特定模型在指令遵循、工具调用或长上下文处理上的偏差，从而提升 Bot 的效果。

这种「模型特化外挂」的设计思路，允许我们针对不同的模型（对我们来说是 Ling/Ring）切换不同的适配套件，是控制开发成本并最大化模型能力的有效方案。

所有偏离上游的自定义逻辑、配置、日志和持久化数据均存放在此。

- **`docs/`**：方案设计、需求拆解、开发日志及 `doc-todo-log-loop` 产出的文档。
- **`logs/`**：推理审计日志，详细记录模型输入、输出、耗时及工具调用详情。
- **`py/`**：外挂包的核心 Python 源码。
  - `wrapper/`：存放所有运行时 MonkeyPatch（如 `launcher.py`, `model_patch.py`, `error_patch.py`）。
  - `callbacks/`：存放用于 Provider 拦截的日志回调逻辑。
- **`vault/`**：Bot 的“灵魂”所在地。包含：
  - `AGENTS.md`：Bot 的核心指令准则。
  - `SOUL.md` & `USER.md`：Bot 的性格设定与用户关系。
  - `skills/`：Bot 专用的外挂技能目录。
- **`workspace/`**：Bot 运行时的沙盒空间。
  - `sessions/`：会话历史记录。
  - `memory/`：Bot 的短期与长期记忆存储。
  - `downloads/`：工具下载或处理的文件产出。

### 核心配置文件
- **`nanobot-shell.sh`**：Sidecar 的入口脚本。负责动态计算物理路径、加载环境变量、注入 `PYTHONPATH` 并启动 `launcher.py`。
- **`config.json`**：Sidecar 专用的私有配置文件，定义了 Provider 参数、默认模型及工作区路径。
- **`.env` / `.env.example`**：环境变量管理。包含 API Key、Discord Token 等凭证。
