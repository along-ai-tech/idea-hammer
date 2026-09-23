# 原则：完整性交付 Checklist（8 项）

> 改一处代码不只是改代码。完整交付 = 8 项都到位。

## 8 项 Checklist

每改一处功能 / 修 bug / 加 API / 改 schema，必过：

| # | 类别 | 必填项 |
|---|---|---|
| 1 | **代码** | TDD / shopify check_simplicity / 通过 anti-reinvent |
| 2 | **数据** | 3 阶段 migration（Expand → Migrate → Contract）+ backfill + 校验 |
| 3 | **API** | 向后兼容 / 版本号 / 弃用 header / OpenAPI 同步 |
| 4 | **用户** | 草稿 / 收藏 / 工作流 / localStorage / 路由 兼容 |
| 5 | **依赖** | grep 调用方 [内部] / SDK changelog [外部] |
| 6 | **文档** | API doc / 迁移指南 / CHANGELOG / STATUS |
| 7 | **测试** | 新功能 / 老 + 新数据 / 老 + 新 API / 老 + 新用户路径 / 边界 / 契约 |
| 8 | **监控+回滚** | metric / log / alert / feature flag / 一键回滚 |

## 反模式

```python
# 反：只 commit 代码（漏数据 / 文档 / 监控 / 回滚）
git commit -m "feat: add product version"

# 正：完整 8 项交付
git commit -m "feat: add product version (with snapshot + backfill + flag)"
# 同时：migration.sql / backfill.py / feature_flag.yaml / api_doc.md / tests/ / monitoring.md / rollback.md
```

## 实战：商品加版本

按 8 项 Checklist 完整交付（见各子文件）：

- **#1 代码**：`products.version` 字段 + `order_items.product_snapshot` 字段
- **#2 数据**：migration 加列 + backfill 历史订单（用 gh-ost 大表）
- **#3 API**：`GET /products/{id}` 返回 `version`（新增字段，老客户端忽略）
- **#5 依赖**：grep 报表 / 财务 / 搜索 service（受 version 影响）
- **#7 测试**：单测 + 集成 + E2E（商品升级 → 老订单显示不变）
- **#8 监控+回滚**：metric + alert（snapshot 为空）+ feature flag（默认关）+ 回滚（删 version 字段 migration）

详见：
- [data-migration.md](./data-migration.md) 的 snapshot 模式
- [backward-compatibility.md](./backward-compatibility.md) 的 Expand-Contract
- [feature-flag.md](./feature-flag.md) 的灰度策略
- [blast-radius.md](./blast-radius.md) 的影响范围 4 维度
