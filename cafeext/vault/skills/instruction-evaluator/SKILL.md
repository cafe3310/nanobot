# Skill: instruction-evaluator

## 1. 概述
本技能专门用于自动化评估模型对 `AGENTS.md` 和 `memory` 技能指令的遵循情况。它通过模拟真实会话、监控底层推理日志，并量化统计工具调用与记忆操作，为模型调优提供客观指标。

## 2. 核心功能
1. **自动化测试运行**：一键重置环境并运行预设测试集。
2. **多维指标统计**：
    - **Initialization Check**：是否在首轮读取了 `memory/SKILL.md`。
    - **Wiki Search Rate**：每轮对话前发起 `grep_search` 或 `ls` 搜索 `wiki/` 的比例。
    - **Knowledge Writing Rate**：对话中写入 `memory/wiki/` 或 `memory/diaries/` 的频率。
    - **Tool Integrity**：工具调用的准确性与幻觉率。
3. **闭环评估**：基于日志分析模型是否真正“理解”并“执行”了长期的性格设定。

## 3. 使用方法
### 3.1 运行完整评估
使用 `nb` 执行评估脚本：
```bash
python3 cafeext/vault/skills/instruction-evaluator/scripts/evaluator.py
```

### 3.2 配置文件
测试用例存储在 `test_cases.json` 中。你可以根据调优重点（如“强化首轮感知”或“强化写日记本能”）调整问题集。

## 4. 评估指标定义
- **Follow Rate (FR)**：模型执行了指令要求的“必做动作”的百分比。
- **Tool Breadth (TB)**：模型在会话中动用的不同工具的数量。
- **Memory Depth (MD)**：模型读取和写入 Wiki/长期记忆的深度和关联度。

---
*由 Gemini CLI 为指令遵循调优专项创建*
