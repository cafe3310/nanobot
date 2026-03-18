# 🐈 nanobot: Full-Featured Bot Evolution

## 🌟 背景与愿景

**背景**：我们希望基于现有的 `nanobot` 框架，结合自研的多种模型（语言模型 LLM、推理模型 Reasoning、多模态模型 Multimodal），逐步将其发展为一个全功能的智能助手。

**核心目标**：
1.  **全功能化**：通过集成多种模型，使 Bot 能够胜任各种复杂、有趣的实际任务。
2.  **模型验证**：在开发和运行过程中，通过真实场景发现自研模型的问题并挖掘其潜在优势。
3.  **规范演进**：采用 `doc-todo-log-loop` (基于日志记录驱动的轻量级项目开发和管理方案) 来严格管理项目的变更与文档，确保开发过程的可追溯性和知识沉淀。

## 📚 知识体系索引

- [架构设计：nanobot 基础架构](./cafe_docs/2026-03-18-16-54-架构设计-nanobot基础架构.md) (由原始 GEMINI.md 转化)

## 🛠️ 核心 Agent Skills

在本项目开发中，我们将深度协同以下 Agent Skills：

`doc-todo-log-loop` -- 我们将以此作为定制开发的唯一管理性 skill。我们用 `cafe_docs` 作为日志目录。

## 🚀 运行与开发

本项目的文档存储在 `cafe_docs` 目录下，遵循 `YYYY-MM-DD-HH-mm-{类别}-{标题}.md` 的命名规范。

- **新增需求**：请用户提出高阶目标，由 Gemini 撰写需求文档并拆分 TODO。
- **开始开发**：由用户指派 TODO 任务后，Gemini 进入「开发与确认」循环。
- **记录日志**：任务完成后，Gemini 记录开发日志。

---
*nanobot is evolving...*
