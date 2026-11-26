<!-- owner: framework -->
# CONTEXT

上下文工程与跨 Session 恢复。

核心主张：上下文质量决定 Coding 质量。持久化的是恢复所需的状态和索引，执行时仍要重新读取关键原始资料。

[为什么]
    Coding Agent 的闭环每一步都靠上下文驱动。上下文缺了业务规则，代码就违背 Spec；上下文塞了无关模块，判断就被稀释。
    所以上下文不是"越多越好"，而是"在正确的时间，给当前任务足够且相关的信息"。

[7 类上下文]
    | 类型 | 内容 | 主要作用 |
    |---|---|---|
    | Task Context | 当前任务、目标、验收标准 | 明确本轮做什么 |
    | Product Context | Product-Spec、业务规则 | 保证业务正确 |
    | Technical Context | 架构、API Contract、数据模型 | 保证技术方案一致 |
    | Code Context | 相关源码、调用关系 | 理解现有系统 |
    | Engineering Context | 编码规范、安全、性能约束 | 控制实现质量 |
    | Execution Context | 已完成任务、测试结果、错误日志 | 支持持续执行 |
    | Session Context | 当前会话的关键决策和进度 | 支持跨轮次、跨 Session 恢复 |

    按任务选，不按项目大小选。实现 Tool 授权时不需要读课程管理模块，也不需要读全部历史会话。

[Context Selection]
    一个 Task 启动前必须回答：我现在需要哪些上下文？
    - 该读：当前 Task 的交付清单、Spec 相关章节、Technical-Design 对应模块、相关源码与测试、工程约束对应主题
    - 不该读：无关业务模块、与本任务无关的历史 bug、其他 Skill 的完整内容、全部历史会话
    - 判据：读到的内容能不能直接支撑这次修改？不能就放下

[三种技术]
    Context Retrieval（上下文检索）
        按任务动态定位：文件搜索、符号搜索、AST/LSP 导航、调用链分析、Git 历史、文档检索。
        不必先建向量库——代码搜索和符号索引通常已经够用。

    Progressive Disclosure（渐进式加载）
        项目入口 → 当前任务说明 → 相关架构与规范 → 具体源码与测试 → 必要时才展开详细参考。
        不到用时不开，读到哪层展开到哪层。

    Context Compression（上下文压缩）
        长任务持续几十分钟后，把历史过程压成：当前任务 / 已完成 / 当前问题 / 已确认决策 / 下一步。
        压缩必须保留关键事实、未完成事项和验证证据，不能只剩摘要。关键决策要有持久化原文可供重读。

[Memory / State / Checkpoint]
    | 概念 | 作用 | 载体 |
    |---|---|---|
    | Context | 当前推理要用到的信息 | 上下文窗口 |
    | Memory | 跨任务可复用的项目知识与历史决策 | session.json 的 key_decisions、DECISIONS.md、Spec 与 Plan 原文 |
    | State | 当前开发任务的进度和状态 | session.json 的 current_phase / current_task |
    | Checkpoint | 特定阶段的持久化恢复点 | session.json 的 checkpoints 数组 |

    Checkpoint ≠ Git Commit。Git Commit 是代码版本快照，Checkpoint 是任务恢复信息（做到哪、测试证据、下一步、关联产物）。两者可关联，职责不同。

[上下文预算]
    - 上下文被占满就主动压缩，不要等报错
    - 一个 Task 的上下文只装这个 Task 的东西，装不下说明 Task 拆得太粗
    - 关键原始资料随时可重读，所以压缩优先保留"索引"（在哪、是什么），细节丢了能重读
    - 永远保留：验收标准、已确认决策、验证证据

[恢复协议]
    State 只能帮助找到恢复位置，不代替对真实代码和执行结果的核查。

    新 Session 启动：
    1. 读 session.json 精简版（`python3 scripts/session.py context`）
    2. 读最近 checkpoint（`python3 scripts/session.py restore`）→ 拿到 resume_at 与 verify_required
    3. 检查 DEV-PLAN 与 Git 工作区状态
    4. 重新读取本 Task 需要的 Spec / Plan / Technical-Design / 源码原文（不凭摘要、不凭记忆）
    5. 核实 checkpoint 记录的测试结果是否仍成立——代码变过就重跑，不能沿用旧结论
    6. 定位未完成任务，继续执行

    违反：State 说测试通过就直接接着写代码。

[落地]
    - 上下文装配纪律：agents/skills/dev-builder/principles/context-engineering.md
    - 测试分层与并发不变量门禁：agents/skills/dev-builder/principles/test-pyramid.md
    - Checkpoint 工具：scripts/session.py checkpoint / restore
    - 入口路由：STATE-ROUTING.md
    - 审查侧检查：agents/skills/code-review/principles/stage2-checklist.md

<!-- owner: framework -->
