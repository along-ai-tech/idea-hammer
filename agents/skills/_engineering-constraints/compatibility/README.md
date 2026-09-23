# compatibility/ — 完整性交付与兼容性约束

> 让 AI 改代码时不破坏上下游。完整交付 = 代码 + 数据 + 用户 + 依赖 + 文档 + 测试 + 监控 + 回滚。

## 必读 2 件

| 文件 | 何时读 |
|---|---|
| [blast-radius.md](./blast-radius.md) | **改任何代码 / schema / API 前必读** —— 4 类外部世界影响分析 |
| [completeness-delivery.md](./completeness-delivery.md) | **每次提交必填** —— 8 项 Checklist（代码/数据/API/用户/依赖/文档/测试/监控+回滚） |

## 参考 4 件（按需深读）

- [backward-compatibility.md](./backward-compatibility.md) —— API / 数据兼容模式
- [data-migration.md](./data-migration.md) —— schema 迁移 3 阶段 + snapshot 模式
- [api-versioning.md](./api-versioning.md) —— API 版本控制 + 弃用
- [feature-flag.md](./feature-flag.md) —— 灰度发布

## 与现有主题关系

| 现有 | 关系 |
|---|---|
| `database/transactions.md` | 短事务原则；本主题说"改 schema 怎么迁移" |
| `ci-cd/migration-safety.md` | **发布时**的 schema 安全；本主题是**日常改代码**的影响 |
| `dev-builder/scope-and-modification.md` | 扩段，加影响范围分析 |
| `code-review/stage2-checklist.md` | 加兼容性 / 完整性交付检查项 |

## 源头

完整性交付理念来自 Pragmatic Programmer / Refactoring（Expand-Contract）/ SRE Book / Feature Flag 模式（Fowler blog）。
