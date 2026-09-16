---
name: code-review
description: 当用户说要审查代码、检查质量、验证功能是否完整，或需要对照 Spec 和设计稿验证代码实现时使用。输出结构化审查报告，每项结论附证据。
---

# code-review

[任务]
    对照 Product-Spec.md 和设计稿，审查代码实现的完整度和质量，输出结构化报告。
    修复由主 Agent 拿报告后用 dev-builder 或 bug-fixer 执行。

[依赖检测]
    必需：Product-Spec.md、项目代码。
    可选增强：DEV-PLAN.md、Design-Brief.md、设计工具 MCP、Playwright、git。

[使用方式]
    读 workflows/workflow-review.md → 跑 Stage 1（做对了没有） → 通过才进 Stage 2（做好了没有） → 输出 contracts/output.schema.json 格式报告。

[文件结构]
    code-review/
    ├── SKILL.md                # 本文件（≤ 30 行）
    ├── principles/             # 第一性原则 + 审查维度
    ├── workflows/              # 执行流程
    └── contracts/              # 输入输出 schema

[引用]
    原则：principles/review-discipline.md（必读）/ principles/stage1-checklist.md / principles/stage2-checklist.md
    流程：workflows/workflow-review.md（Stage 1 + Stage 2 完整流程）
    契约：contracts/input.schema.json / contracts/output.schema.json
    工程级约束：../_engineering-constraints/（Stage 2 必查）
