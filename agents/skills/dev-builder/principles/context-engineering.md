# 原则：上下文装配

> Task 启动前先装配上下文，再动手改代码。上下文不是越多越好，是够且相关。

域定义见 [CONTEXT.md](../../../../CONTEXT.md)（7 类上下文 / Context Selection / 三种技术 / Memory-State-Checkpoint 分工）。本文件讲 dev-builder 怎么落地。

## Task 启动前的装配顺序

渐进式加载，逐层展开，不提前铺满：

1. **第 1 层 · 定位**：DEV-PLAN 当前 Phase / Task 章节 → 知道这轮做什么
2. **第 2 层 · 业务**：Product-Spec 对应 REQ/AC 原文 → 知道对与错
3. **第 3 层 · 方案**：Technical-Design 对应模块的边界、不变量、数据约束、API Contract
4. **第 4 层 · 现状**：相关源码、调用方、同层测试 → 知道现有系统怎么跑
5. **第 5 层 · 规范**：本次改动命中的工程约束主题（语言规范 + 对应 anti-reinvent 条目）
6. **第 6 层 · 必要时**：详细参考文档、CI 配置、上游历史

第 1 层读完如果发现 Task 范围不清 → 回 dev-planner 补，不要硬做。

## 该读 / 不该读

| 该读 | 不该读 |
|---|---|
| 当前 Task 的交付清单与验收标准 | 无关业务模块的源码 |
| Spec 对应章节原文 | 与本任务无关的历史 bug |
| Technical-Design 对应模块 | 其他 Skill 的完整 SKILL.md |
| 相关源码 + 调用方 + 同层测试 | 全部历史会话 |
| 命中的工程约束主题 | 整个代码仓库 |

判据：读到的内容能不能直接支撑这次修改？不能就放下。

## 反模式

- **开局全量读仓库**：50 万行仓库塞进上下文，Token 成本暴涨、无关信息稀释判断、关键信息被埋没
- **凭摘要开工**：拿上次的交接摘要当事实，不重读原文 → 违反 [CONTEXT.md 的恢复协议]
- **只读不定位**：知道文件在哪，但不查调用方 → 改出回归
- **上下文塞爆**：一个 Task 装了三个 Task 的东西 → Task 拆得太粗，回 dev-planner 拆

## 压缩触发与做法

触发条件（满足任一就压缩）：

- 单个 Task 内工具调用超过约 30 次
- 开始反复引用早期读过的文件却记不清结论
- 用户插入新需求，原 Task 上下文被挤占

压缩时保留（不可丢）：

1. 当前任务与验收标准
2. 已完成项与已确认决策（含理由）
3. 未完成事项与当前问题
4. 验证证据（跑过的命令与结果）

可丢：中间探索过程、已被推翻的假设、工具原始输出的重复片段（保留结论与证据位置即可）。

关键决策要落回 Spec / DECISIONS.md / session.json，压缩丢了还能重读原文。

## Checkpoint 落盘

Task 完成、commit 之后记一个恢复点：

```bash
python3 scripts/session.py checkpoint \
  --phase "phase_3" \
  --task "DT-004" \
  --commit "$(git rev-parse --short HEAD)" \
  --tests '{"unit_test":"passed","integration_test":"pending"}' \
  --next "完成授权 API 集成测试" \
  --artifacts "Technical-Design.md,DEV-PLAN.md"
```

Checkpoint 记的是任务恢复信息（做到哪、测试证据、下一步、关联产物），不是代码版本快照——代码版本归 Git Commit 管。详见 [CONTEXT.md](../../../../CONTEXT.md)。

