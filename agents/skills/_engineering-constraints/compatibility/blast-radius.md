# 原则：影响范围分析（Blast Radius）

> 改一处前必须知道影响谁。AI 默认看当前代码，要强制看**4 类外部世界**。

## 4 类外部世界

任何代码改动都会影响其中至少 1 类。改之前必须逐项检查：

### 1. 数据（已有数据 + 持久化）

- 改字段类型 / 长度 / 约束 → 老数据会怎样？
- 删字段 → 老数据记录里这个字段值会丢失吗？
- 改字段语义（如 status 从 0/1 改 0/1/2）→ 老数据的 0/1 怎么映射？
- 加 NOT NULL 字段 → 历史 NULL 怎么办？
- 改主键 / 外键 → 关联表怎么办？

### 2. API（已有客户端 + 调用方）

- 改 endpoint 路径 → 老客户端 404
- 删响应字段 → 老客户端 undefined
- 改状态码 → 老客户端逻辑错误
- 改限流 / 鉴权 → 老用户体验降级
- Webhook 签名变化 → 老订阅方验证失败

### 3. 用户（已有用户 + 行为状态）

- 老用户的草稿 / 收藏 / 配置格式变了 → 数据丢失
- 老用户的工作流卡在中间状态 → 新流程不认
- 浏览器 localStorage / IndexedDB 格式变了 → 老用户登录态丢失
- 路由改了 → 老用户 deeplink 失效

### 4. 依赖（已有第三方 + 内部模块）

- 调用的内部 service / util 改了签名 → 上游全断
- 第三方 SDK 升级 breaking change
- 数据库 / OS / 浏览器 弃用某些 API
- CI / 部署 / 监控配置失效

## 实战：改商品加版本功能

```
需求：商品加版本号

## Blast Radius 分析

### 数据
- products 表加 version 字段 → 老 products 行的 version 是什么？
- order_items 表引用 product_id → 老订单要看的是"购买时的商品"，不是"现在的商品"
  → 需要 order_items.product_snapshot 字段
  → 或者 order_items 存 product_name / price_at_purchase

### API
- GET /products/{id} 返回 version → 老客户端不识别（可忽略）
- POST /orders 响应增加 product_version → 老订单系统解析失败？
  → 默认开启 backward-compat，老字段保留

### 用户
- 老订单的"商品信息"显示 → 必须用下单时的快照，不能用当前 products
- UI 显示订单详情 → 需要明确"已下单版本" vs "当前版本"

### 依赖
- 内部 service: search_products / recommend_products → 受 version 影响
- 报表: 销售报表按哪个 version 统计？
- 财务对账 → 必须按购买时的版本

## 实施方案
1. order_items 加 product_snapshot JSON 字段（存购买时的完整快照）
2. products 加 version 字段，新老并存
3. 旧订单读 product_snapshot，不读 products 表实时字段
4. UI 明确显示"该订单的商品版本是 X"
5. 提供 backfill：给历史订单补 product_snapshot
```

## 检查清单（每改一处必填）

- [ ] 这条改动影响 4 类外部世界的哪几个？
- [ ] 老数据 / 老 API / 老用户 / 老依赖 各自怎么处理？
- [ ] 有没有"安静的破坏"（不报错但数据错）？
- [ ] 是否有版本号 / feature flag 来隔离老路径？
- [ ] 测试覆盖：老数据 + 新数据 / 老 API + 新 API / 老用户路径 + 新用户路径

## 检测

- code-review: Stage 2 必查 blast radius 文档化
- 工具 scripts/impact_analyzer.py（可选）：扫 import 找调用方

## 反模式

```python
# 反模式：改一处不考虑其他
def update_product(id, **kwargs):
    Product.objects.filter(id=id).update(**kwargs)
    # 老订单的 product_name 也会跟着变（如果 Product 表有 product_name）


# 正确：分清楚哪些字段会影响历史引用
def update_product(id, *, version_bump=True, **kwargs):
    with transaction.atomic():
        product = Product.objects.select_for_update().get(id=id)
        # 实时字段更新
        for key in REALTIME_FIELDS:
            if key in kwargs:
                setattr(product, key, kwargs[key])
        # version bump（不动 SNAPSHOT_FIELDS）
        if version_bump:
            product.version += 1
        product.save()
        # 历史快照字段不动（order_items 用 snapshot）
```
