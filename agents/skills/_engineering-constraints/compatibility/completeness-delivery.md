# 原则：完整性交付 Checklist

> 改一处代码不只是改代码。完整交付 = 8 项都到位。

## 8 项 Checklist

每改一处功能 / 修一个 bug / 加一个 API / 改 schema，必过：

### 1. 代码本身

- [ ] 代码改完
- [ ] TDD 纪律（RED → GREEN → REFACTOR）
- [ ] 通过代码简洁性校验（check_simplicity.py）
- [ ] 通过工程级约束（anti-reinvent / ecosystem-matrix）

### 2. 数据（如果有 schema / 数据改动）

- [ ] Migration 脚本（3 阶段：Expand → Migrate → Contract）
- [ ] Backfill 计划（老数据怎么处理）
- [ ] 大表用 gh-ost / pg_repack（避免锁表）
- [ ] 校验（迁移后老列 vs 新列一致）

### 3. API / 接口（如果有对外接口改动）

- [ ] 向后兼容（新版能处理老输入 / 老客户端）
- [ ] 版本号（URL 或 Header）
- [ ] 弃用 header（Sunset / Deprecation）
- [ ] OpenAPI spec 同步

### 4. 用户状态（如果有用户行为改动）

- [ ] 老用户草稿 / 收藏 / 配置迁移
- [ ] 工作流中间状态兼容
- [ ] localStorage / cookie / IndexedDB 兼容
- [ ] UI 路由 / deeplink 兼容

### 5. 依赖（如果涉及第三方 / 内部模块）

- [ ] 内部模块签名变化（grep import）
- [ ] 第三方 SDK breaking change
- [ ] 数据库 / OS / 浏览器弃用 API

### 6. 文档

- [ ] API 文档（OpenAPI / README）
- [ ] 迁移指南（给老用户）
- [ ] CHANGELOG（breaking change 必须列）
- [ ] STATUS（当前状态）

### 7. 测试

- [ ] 新功能单测（每个行为点）
- [ ] 老数据 + 新数据测试
- [ ] 老 API + 新 API 测试
- [ ] 老用户路径 + 新用户路径测试
- [ ] 边界（空 / 零 / 异常 / 权限）
- [ ] 契约测试（schema / API 兼容）

### 8. 监控 + 回滚

- [ ] Metric（关键指标埋点）
- [ ] Log（关键操作记录）
- [ ] Alert（异常自动告警）
- [ ] Feature Flag（默认关闭，灰度打开）
- [ ] 回滚方案（代码 / 数据 / 配置）
- [ ] 一键回滚（无需重新发布）

## 实战：商品加版本功能

```
需求：商品支持版本管理

## 8 项 Checklist

### 1. 代码
- [x] products.version 字段
- [x] order_items.product_snapshot / product_version 字段
- [x] ProductService.update() 不动 SNAPSHOT_FIELDS
- [x] 单测覆盖：version bump / snapshot 正确性

### 2. 数据
- [x] Migration: 加 products.version 列（default 1）
- [x] Migration: 加 order_items.product_snapshot + product_version
- [x] Backfill: 给历史订单补 snapshot
- [x] 用 gh-ost（如果 products 表 > 100w 行）

### 3. API
- [x] GET /products/{id} 返回 version（新字段，老客户端忽略）
- [x] POST /orders 接受 product_version（可选，老客户端不传）
- [x] 响应兼容：保留 product_name 老字段
- [x] OpenAPI 同步

### 4. 用户
- [x] 老用户订单详情：显示已下单版本
- [x] 老用户 deeplink 兼容（路由未变）
- [x] localStorage 无影响（不存商品信息）

### 5. 依赖
- [x] grep 调用方（搜索 service / report）
- [x] 报表：明确按 product_version 统计
- [x] 财务对账：按 product_version 对账

### 6. 文档
- [x] API doc：version 字段说明
- [x] 迁移指南：老订单查 product_snapshot
- [x] CHANGELOG：列 breaking change

### 7. 测试
- [x] 单测：ProductService.update() 不动 snapshot
- [x] 集成测：老订单查还是老版本
- [x] E2E 测：商品升级 → 老订单显示不变

### 8. 监控 + 回滚
- [x] Metric: 商品升级次数 / 老订单查询次数
- [x] Alert: order_items.product_snapshot 为空（迁移遗漏）
- [x] Feature Flag: product_version_default（默认 false，新订单才用）
- [x] 回滚: 删 version 字段（独立 migration）
```

## 反模式：只改代码

```python
# 反模式：只 commit 代码
git commit -m "feat: add product version"

# 漏：
# - 老订单数据怎么办？
# - 老 API 客户端怎么办？
# - 报表 / 财务 / 售后怎么算？
# - 老用户看到什么？
# - 测试覆盖了吗？
# - 文档更新了吗？
# - 监控告警加了吗？
# - 能回滚吗？


# 正确：完整 8 项交付
git commit -m "feat: add product version (with snapshot + backfill + flag)"

# 同时 push：
# - migration.sql
# - backfill.py
# - feature_flag_config.yaml
# - api_doc_update.md
# - tests/
# - monitoring_setup.md
# - rollback_plan.md
```
