<!-- owner: architecture -->
# SUBAGENTS

子 Agent 调度规则。详见 `.codex/agents/` 下的 TOML 定义。

## 固定 Sub-Agent

两个有固定职责的 Sub-Agent，定义在 .codex/agents/ 的 TOML 文件：
1. code-reviewer：.codex/agents/code-reviewer.toml，用 code-review skill，做两阶段审查并输出报告。
2. evolution-runner：.codex/agents/evolution-runner.toml，用 evolution-engine skill，消化进化信号生成改动建议。

## 调度纪律

- Codex 只在主 Agent 显式请求时 spawn subagent，不自动 spawn。所以 code-review 闭环、自进化消化都靠主 Agent 主动 spawn 对应 agent。
- 除两个固定角色外，主 Agent 可按 [WORKFLOW.md] 临时 spawn 执行型子 Agent 处理可隔离的并行工作。
- **执行型子 Agent 只编码和自检，不再 spawn 子 Agent、不 commit**。review 闭环和 commit 始终由主 Agent 控制。
- **隔离原则**：每个子 Agent 用 fresh 实例，不复用、不继承 session 历史。主 Agent 显式提供完整上下文：Spec 条目、交付清单、涉及文件、项目结构。这是隔离保证，防止一个子 Agent 的错误假设污染另一个。
- code-review 永远通过 spawn code-reviewer 执行。evolution-runner 在 session 启动同步 spawn 消化信号，返回的建议由主 Agent 当场逐条问用户，同意即改对应文档、全盘否定即删 signal 和 proposal。

## v0.9.0 起:大 DEV-PLAN 走 SDD（任务循环）

当 DEV-PLAN 含 ≥5 个相互独立的 Phase 任务（由 dev-planner 在切 phase 时判定），
主 Agent 走 subagent-driven-development（`agents/skills/subagent-driven-development/`），
对每个 Phase 任务循环 dispatch fresh implementer + reviewer subagent：

- **不新设 fixed sub-agent**：复用现有执行型子 Agent 调度通道，每次按 Phase 任务 fresh spawn。
- **reviewer 复用 code-reviewer.toml**：但 review 粒度从"整 phase"降到"单 task"，输出 spec-compliance + code-quality 两段 verdict（见 `code-review/principles/review-discipline.md` 两段输出契约）。
- **judgment ledger 持久化**：每次 review/fix/仲裁写到 `.idea-hammer/sdd/<plan-id>/progress.md`，合账后归档到 `.idea-hammer/sdd-archive/`（不入 gitignore，永久留底）。
- **breaker 触发由 reviewer 报出**（"breaker tripped — <findings>"），主 Agent 在循环间统一收集仲裁：park / rule 最小改动 / stop。
- **commit / push / merge 永远由主 Agent 在 Phase 3 执行**，subagent 不碰。

短路规则：Phase 任务 <5 或跨 phase 强耦合 → 不走 SDD，直接走 dev-builder + code-reviewer 终审。

<!-- owner: architecture -->
