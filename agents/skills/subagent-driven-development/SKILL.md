---
name: subagent-driven-development
description: 当 DEV-PLAN.md 含 ≥5 个相互独立的 Phase 任务、需要任务级两段 review 与 judgment ledger 时使用。dev-builder 的一会话干完 + 现 code-reviewer 终审之外的可选路径。
---

# subagent-driven-development

[任务]
    用任务级 fresh subagent + 两段 review + ledger 持久化，把大 DEV-PLAN 切成 N 个独立可验收的任务循环。每个 task 都有独立的 spec compliance 与 code quality 两段 review，5 轮 fix loop 兜底。借鉴 superpowers:subagent-driven-development 的核心机制，不照搬超长模板。

[依赖检测]
    必需：DEV-PLAN.md、Product-Spec.md。
    触发条件（dev-planner 在切 phase 时判断）：
    - Phase 任务数 ≥5 → 默认走本 SKILL
    - Phase 任务 <5 → 用 dev-builder + 现 code-reviewer 终审
    - 跨 phase 强耦合 → 用 dev-builder 不切任务

[使用方式]
    启动 → 读 workflows/execute.md 完整流程 → 用 scripts/ 工具：
    - sdd-workspace：建/解析 plan 工作目录（.idea-hammer/sdd/<plan-id>/）
    - task-brief：抽单个 task 的 brief 文件
    - review-package：生成本次 task 的 review diff package
    → 每个 task 写一条 ledger 进度到 progress.md
    → 合账后需用户确认 commit / 不 commit

[文件结构]
    subagent-driven-development/
    ├── SKILL.md                          # 本文件（≤ 50 行）
    ├── principles/task-loop-discipline.md # 任务循环纪律（隔离 / 两段 verdict / fix loop / ledger）
    ├── workflows/execute.md              # 完整执行流程（≤ 200 行）
    ├── contracts/                        # 输入输出 schema（2 个）
    └── scripts/
        ├── sdd-workspace.sh              # workspace 管理
        ├── task-brief.sh                 # 抽 task brief
        └── review-package.sh             # 抽 review diff

[引用]
    原则：principles/task-loop-discipline.md（必读）
    流程：workflows/execute.md
    契约：contracts/input.schema.json、contracts/output.schema.json
    工具：scripts/{sdd-workspace,task-brief,review-package}.sh
    借鉴：superpowers:subagent-driven-development
    上游：agents/skills/dev-planner/SKILL.md（DEV-PLAN 来源）
    下游：agents/skills/code-review/SKILL.md（任务级两段 review 复用）

[与 dev-builder 关系]
    dev-builder = "一口气干完 + 现 code-reviewer 终审"，适合短任务
    subagent-driven-development = "切任务循环 + 任务级两段 review + ledger"，适合 ≥5 task
    不互相替代，由 dev-planner 在切 phase 时按"任务数 + 耦合度"路由
