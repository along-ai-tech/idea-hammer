<!-- owner: product -->
# STATE-ROUTING

初始化时检测项目进度，路由到对应环节。

- 无 Product-Spec.md → 全新项目 → 引导描述想法或用 product-spec-builder
- 有 Spec，无 DEV-PLAN，无代码 → 输出交付指南
- 有 Spec 和 DEV-PLAN，无代码 → 引导 dev-builder
- 有 Spec 和代码，无 DEV-PLAN → 建议 dev-planner 补计划
- 有 Spec、DEV-PLAN、代码都齐 → 开发中 → 可继续开发、审查、修复或发布

显示格式：

    📊 项目进度检测
    - Product Spec：[状态]　- Design Brief：[状态]　- DEV-PLAN：[状态]　- 项目代码：[状态]
    当前环节：[名称]　下一步：[指令]

<!-- owner: product -->
