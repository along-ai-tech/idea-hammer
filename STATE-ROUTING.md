<!-- owner: product -->
# STATE-ROUTING

初始化时检测项目进度，路由到对应环节。

## 先定位，再核实

有 `.idea-hammer/session.json` 时，先读恢复点：

    python3 scripts/session.py restore

拿到 resume_at（恢复位置）和 verify_required（待核实清单）。
**恢复点只定位，不代替核查**——按 CONTEXT.md 的恢复协议逐项核实后再继续：

1. Git 工作区是否与 checkpoint 记录的 commit 一致
2. checkpoint 记录的测试结果是否仍成立（代码变过就重跑，不沿用旧结论）
3. checkpoint 之后的未提交改动属于哪个 Task，是否保留
4. 引用的产物（Spec / Plan / Design）是否还在原位且未被改动

核实完再进下面的路由表。发现与 checkpoint 不一致，以实际代码和实际执行结果为准。

## 路由表

- 无 Product-Spec.md → 全新项目 → 引导描述想法或用 product-spec-builder
- 有 Spec，无 Technical-Design → 引导 dev-planner 先做技术设计
- 有 Spec 和 Technical-Design，无 DEV-PLAN，无代码 → 输出交付指南
- 有 Spec、Technical-Design 和 DEV-PLAN，无代码 → 引导 dev-builder
- 有 Spec 和代码，无 DEV-PLAN → 建议 dev-planner 补技术设计与计划
- 有 Spec、DEV-PLAN、代码都齐 → 开发中 → 可继续开发、审查、修复或发布

## 显示格式

    📊 项目进度检测
    - Product Spec：[状态]　- Design Brief：[状态]　- Technical Design：[状态]　- DEV-PLAN：[状态]　- 项目代码：[状态]
    当前环节：[名称]　下一步：[指令]

<!-- owner: product -->
