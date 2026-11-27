# 原则：任务循环纪律

> SDD 存在的理由：一次性干完的返工面太大。切任务 + 独立 review + 账本留底，让每一步都留下可追溯的判断。

## 隔离优先

- 每个 task 用 fresh subagent，不复用、不继承 session 历史
- 主 Agent 显式提供完整上下文：brief、接口契约、Global Constraints、报告路径
- subagent 不得自己再 spawn 子 agent（no-self-dispatch）

## 先契约后并行

- 并行的前提是任务独立、契约明确、修改范围可隔离、结果可集成
- 共享接口或共享文件的任务必须串行，否则并行只是更快地产生冲突
- preflight scan 要在 dispatch 前找出冲突，而不是在 review 阶段才发现

## 两段 verdict，不接受单一结论

每次 review 必须输出两段：

1. **Spec Compliance** —— brief 里的交付项是否都实现并被证据验证
2. **Code Quality** —— Critical / Important / Minor 分级

两段都清才算 review clean。任何一段 ❌ → 进 fix loop。

## fix loop 有上限

- Round 1-3：resume 原 implementer，传 finding 列表
- Round 4-5：换 fresh implementer（更 capable model），带历史
- Round 5 后仍未清 → breaker 触发，由主 Agent 仲裁（park / rule / stop）

不设上限会烧光 token 还收敛不了；上限太低会把真问题误判成"改不动"。

## 判断必须留底

- 所有假设、判断、parking、ruling 都写 ledger，不靠聊天记录
- 状态行：`Task <N>: complete (commits ..., review clean)` / `Task <N>: fix round <R>/5 (<X> addressed, <Y> open)`
- 仲裁行：`Task <N>: Ruling: <finding> — <why code stands>`
- 合账后 ledger 归档到 `.idea-hammer/sdd-archive/`，永久留底不入 gitignore

## 不可逆动作不自己做

- commit / push / merge / publish / 删除 → 主 Agent 在 Phase 3 执行
- 安全敏感动作 → 停下来问用户
- 其余场景主 Agent 持续跑，不 poll 问进度

