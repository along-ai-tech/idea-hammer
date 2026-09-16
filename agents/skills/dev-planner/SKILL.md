---
name: dev-planner
description: 当 Product-Spec.md 已完成、需要规划怎么分阶段开发时使用。也在 Spec 变更后用于更新已有开发计划。输出 DEV-PLAN.md。
---

# dev-planner

[任务]
    生成模式：读 Product-Spec.md 和 Design-Brief.md，分析功能依赖，WebSearch 验证技术选型，输出分阶段开发计划 DEV-PLAN.md。
    迭代模式：Spec 变更后分析影响范围，更新 DEV-PLAN.md 的 Phase 划分和文件清单，已完成的 Phase 不动。

[依赖检测]
    必需：Product-Spec.md。
    可选，缺了标降级：Design-Brief.md、设计工具 MCP、已有项目代码。

[使用方式]
    启动 → 读 workflows/workflow-generate.md 或 workflows/workflow-iterate.md → 按对应模式走 → 输出 DEV-PLAN.md 用 templates/dev-plan-template.md。

[文件结构]
    dev-planner/
    ├── SKILL.md                  # 本文件（≤ 30 行）
    ├── principles/               # 第一性原则
    ├── workflows/                # 生成 / 迭代流程
    ├── contracts/                # 输入输出 schema
    └── templates/
        └── dev-plan-template.md  # DEV-PLAN.md 输出模板

[引用]
    原则：principles/*.md（必读 phase-planning + tech-validation）
    流程：workflows/workflow-generate.md（生成模式）/ workflow-iterate.md（迭代模式）
    契约：contracts/input.schema.json / contracts/output.schema.json
    模板：templates/dev-plan-template.md
