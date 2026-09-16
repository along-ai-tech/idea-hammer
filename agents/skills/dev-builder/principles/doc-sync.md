# 原则：文档回写

> 开发中用户改了需求或设计，先回 product-spec-builder 或 design-brief-builder 更新文档再继续写，不让代码和文档脱节。

## 触发条件

- 用户改需求 → 先调 product-spec-builder 更新 Product-Spec.md
- 用户改设计 → 先调 design-brief-builder 更新 Design-Brief.md
- Spec 变更 → 同时回写 DEV-PLAN.md（通过 dev-planner）
- 改完文档再继续写代码，不让代码和文档脱节
