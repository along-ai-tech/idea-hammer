# database/ — 数据库规范（详细）

> 主 dev-builder principles/quality-and-security 已覆盖基础。这里是详细规则。

## 文档

| 主题 | 文档 |
|---|---|
| 索引策略 | [indexing.md](./indexing.md) |
| 事务边界 | [transactions.md](./transactions.md) |
| 连接池 | [connection-pool.md](./connection-pool.md) |

## 见主原则

dev-builder/principles/quality-and-security.md 已包含：
- snake_case 命名
- 每表 id / created_at / updated_at
- 参数化查询
- migration 用 ALTER TABLE
