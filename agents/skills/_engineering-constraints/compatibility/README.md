# compatibility/ — 完整性交付与兼容性约束

> 让 AI 改代码时主动消除对项目其他功能的影响。完整交付 = 代码 + 数据 + 用户 + 依赖 + 文档 + 测试 + 监控 + 回滚。

## 为什么独立成主题

AI 写代码最致命的不是造轮子 / 长函数，而是**改一处破坏全局**。

例子：商品加版本功能 → 直接 ALTER TABLE → 老订单历史被覆盖 → 财务 / 售后 / 法律全乱。

AI 倾向：
- 看当前代码状态，不看**已有数据 + 已有用户 + 已有依赖**
- 改完就 commit，不考虑**完整性交付**（数据迁移 / API 兼容 / 文档 / 回滚）

本主题治**这一类**问题，不修单一例子。

## 6 条原则

| # | 原则 | 解决什么 |
|---|---|---|
| 1 | blast-radius.md | 改一处影响谁？4 类外部世界（数据 / API / 用户 / 依赖）|
| 2 | backward-compatibility.md | 老代码 / 老客户端 / 老数据 怎么继续跑 |
| 3 | feature-flag.md | 灰度发布，不全量上线 |
| 4 | data-migration.md | 数据迁移：snapshot / backfill / 双写 |
| 5 | api-versioning.md | API 版本控制 + 弃用策略 |
| 6 | completeness-delivery.md | 完整性交付 checklist（代码 + 数据 + 文档 + 测试 + 监控 + 回滚）|

## 与现有主题关系

| 现有 | 关系 |
|---|---|
| database/transactions.md | 短事务原则，本主题说"改 schema 怎么迁移" |
| ci-cd/migration-safety.md | **发布时**的 schema 迁移安全，本主题是**日常改代码**的影响 |
| dev-builder/principles/scope-and-modification.md | 扩段，加影响范围分析 |
| code-review/principles/stage2-checklist.md | 加兼容性 / 完整性交付检查项 |

## 接入点

- dev-builder 启动必读（按"有 schema 改动 / 业务逻辑改动"触发）
- code-review Stage 2 必查（卡 6 项）

## 源头

完整性交付理念来自：
- **Pragmatic Programmer**（Hunt & Thomas）：完整性 = 软件质量
- **Refactoring**（Fowler）：Parallel Change / Expand-Contract
- **SRE Book**（Google）：可回滚优先
- **Feature Flag** 模式（Fowler blog）
