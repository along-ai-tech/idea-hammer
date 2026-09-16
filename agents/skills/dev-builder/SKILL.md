---
name: dev-builder
description: 当 DEV-PLAN.md 就绪、用户说要开始写代码或继续开发下一个 Phase 时使用。新项目搭建骨架，已有项目按 Phase 逐步实现功能。
---

# dev-builder

[任务]
    初始化模式：无代码 + 有 DEV-PLAN.md → 搭骨架 → 进 Phase 1 执行流程。
    持续开发模式：有代码 + 有 DEV-PLAN.md → 按 Phase 逐步开发，每 Task 走 RED/GREEN/REFACTOR + review→fix 循环，每 Phase 末过四步走验证。
    规划与执行方式见 AGENTS.md [规划与执行]。

[依赖检测]
    启动第一步执行。
    必需：Product-Spec.md、DEV-PLAN.md、DEV-PLAN 技术栈表里列的系统工具和运行时。缺了提示先补。
    可选，缺了标降级模式继续：Design-Brief.md、设计工具 MCP、gh CLI、playwright。
    必需依赖缺失你自己判断装法直接装；要用户权限或认证才提示用户。
    进已有项目先读它自带的 agent 约定文件（AGENTS.md / CLAUDE.md），按项目规矩来。

[使用方式]
    启动 → 读 contracts/input.schema 校验输入 → 读 workflows/workflow-init-or-continue.md 决定模式 → 按对应 workflow 走。

[文件结构]
    dev-builder/
    ├── SKILL.md                       # 本文件（≤ 50 行）
    ├── principles/                    # 第一性原则（按主题归类，8 个）
    ├── workflows/                     # 执行流程（5 个）
    └── contracts/                     # 输入输出 schema（2 个）

[引用]
    原则：principles/engineering-constraints.md（必读，指向 _engineering-constraints/ 13 主题）、principles/tdd-discipline.md（必读）、principles/scope-and-modification.md（必读）、principles/verification-evidence.md（必读）、principles/reuse-and-design.md、principles/code-style.md、principles/external-and-real.md、principles/doc-sync.md、principles/quality-and-security.md
    流程：workflows/workflow-init-or-continue.md（启动路由）、workflows/workflow-init.md、workflows/workflow-task-loop.md、workflows/workflow-phase-verify.md、workflows/workflow-self-drive.md
    契约：contracts/input.schema.json、contracts/output.schema.json
