# SDD Execute Workflow（任务循环）

> 借鉴 superpowers:subagent-driven-development。一次性干完是 dev-builder；本流程是"切任务循环"。

[Phase 0: Pre-flight]
    - 创建 workspace：bash scripts/sdd-workspace.sh <plan-file>（建 .idea-hammer/sdd/<plan-id>/）
    - 检查旧 ledger：如已有同 plan-id 的 progress.md，读最后一条任务续跑
    - 写第一行 ledger：# SDD ledger — plan: <plan-file path>
    - preflight scan：找 task 间冲突（共享文件 / 共享接口 / 矛盾规定）
    - 写扫描结果到 ledger

[Phase 1: Task Loop]
    对每个未完成任务，循环：

    [1.1 Brief]
        bash scripts/task-brief.sh <plan-file> <N> → 抽 task N 的 brief 到 .idea-hammer/sdd/<plan-id>/task-N-brief.md
        含：Files（Create/Modify/Test）+ Interfaces（Consumes/Produces）+ Step 列表

    [1.2 Dispatch Implementer]
        主 Agent spawn fresh subagent（不带 session 历史）传：
        - brief 路径
        - 报告文件路径 .idea-hammer/sdd/<plan-id>/task-N-report.md
        - 接口契约（从前面 task 产出）
        - 全局约束（Plan 的 Global Constraints）
        Implementer 写报告：状态 + commits + 一行测试摘要 + 任何 concerns
        Implementer 严格遵守：no-self-dispatch（不自己再 spawn 子 agent）

    [1.3 Review Package]
        bash scripts/review-package.sh <plan-file> <N> <base> <head> → 抽 commit diff 到 .idea-hammer/sdd/<plan-id>/task-N-review-pkg.txt
        base = 该 task dispatch 前记录的 HEAD

    [1.4 Two-Stage Review]
        spawn fresh reviewer subagent 传：brief + report + review-pkg + Global Constraints
        输出两段 verdict：
        - Spec Compliance: ✅ / ❌
        - Code Quality: ✅ / ❌ + Critical/Important/Minor finding 列表
        ⚠️ Cannot verify 项需主 Agent 自己判定

    [1.5 Fix Loop]
        如有 Critical/Important finding 或 Spec ❌：
        - Round 1-3：resume 原 implementer（同一个 subagent），传 finding list
        - Round 4-5：dispatch fresh implementer（更 capable model）含历史
        - 每轮 implementer 修后 append 到原 report 文件
        - 每轮 fix 后跑 review-package + 重 review（scoped re-review）
        - Round 5 后仍未清：breaker 触发
        ⚠ breaker 由 reviewer subagent 报出（"breaker tripped — <findings list>"），
          主 Agent 在循环间统一收集并仲裁：
            - 错的/可争议：park（ledger 写 Ruling: ...）
            - 真的但不影响下游：park
            - 真的且 load-bearing：rule 最小改动 + ledger 记录 + 带到下个 task

    [1.6 Complete Task]
        两段 review 都清（或 breaker 已仲裁）后：
        - append ledger: Task <N>: complete (commits <a7>..<b7>, review clean)
        - mark todo done

    [1.7 Loop Until All Tasks Done]
        More tasks remain → 跳 1.1
        没有 → 跳 Phase 2

[Phase 2: Final Whole-Branch Review]
    - spawn 一次最 capable reviewer subagent 传 MERGE_BASE..HEAD diff + ledger 全文
    - 输出全局 findings，Critical/Important 进 fix loop
    - fix loop 同 1.5 但只允许一轮 fix
    - 残留 findings → 主 Agent 仲裁（park / rule / stop）

[Phase 3: Finish]
    - 收 ledger 的所有 Ruling: 行为最终 message 列出来
    - **ledger 留底**：合账前 `cp .idea-hammer/sdd/<plan-id>/progress.md .idea-hammer/sdd-archive/<plan-id>-progress.md`
      （sdd-archive 不入 gitignore，是 plan 执行历史的永久留底）
    - **workspace 清理**：`rm -rf .idea-hammer/sdd/<plan-id>/`
    - git history 是 record，workspace 是 scratch
    - 用户决定 commit / push

[judgment ledger 记录规则]
    所有 implementer / reviewer 假设、判断、parking、ruling 都要写到 ledger：
    - 状态行：`Task <N>: complete (commits ..., review clean)` 或 `Task <N>: fix round <R>/5 (<X> addressed, <Y> open)`
    - 假设：`Task <N>: brief assumed <X>, implementer confirmed/refuted <Y>`
    - 仲裁：`Task <N>: Ruling: <finding> — <why code stands>` 或 `<decision and why>`
    - 警戒：`Task <N>: breaker tripped — <findings list>`
    Ledger 是 plan 工作目录下的 git-ignored 文件（不被 commit）

[Break condition]
    - 不可逆操作（merge / push / publish / 删除）→ 立刻停下问用户
    - 安全敏感动作 → 停下问用户
    - plan so broken every path a guess → 停下问用户
    其他场景主 Agent 持续跑不打断用户（不 poll 问进度）
