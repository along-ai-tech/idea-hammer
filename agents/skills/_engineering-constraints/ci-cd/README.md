# ci-cd/ — CI/CD 约束

> 必备检查 / 数据库 migration / 回滚策略。

## 文档

| 主题 | 文档 |
|---|---|
| 必备检查 | [required-checks.md](./required-checks.md) |
| 数据库 Migration | [migration-safety.md](./migration-safety.md) |
| 回滚策略 | [rollback.md](./rollback.md) |

## 核心原则

1. **CI 卡门禁**：lint + test + build + e2e + security + license 必过
2. **Migration 必须向前兼容**（发布过程中新老版本共存）
3. **必须可回滚**（blue/green / canary / feature flag）
4. **green build 才能 merge / deploy**
