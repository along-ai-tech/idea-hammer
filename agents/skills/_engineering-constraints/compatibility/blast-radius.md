# 原则：影响范围分析（Blast Radius）

> 改一处前必须知道影响谁。AI 默认看当前代码，要强制看 4 类外部世界。

## 4 类外部世界

| 类别 | 检查点 |
|---|---|
| **数据** | 老数据会怎样？字段删了值丢吗？NOT NULL 历史 NULL 怎么办？ |
| **API** | 老客户端 404？删字段变 undefined？状态码语义变了？ |
| **用户** | 草稿 / 收藏 / 工作流 / localStorage / 路由 改了？ |
| **依赖** | 内部 service 签名变了？第三方 SDK breaking？ |

## 检查清单（每改一处必填）

- [ ] 4 类外部世界影响哪些？
- [ ] 老数据 / 老 API / 老用户 / 老依赖 各自怎么处理？
- [ ] 有没有"安静的破坏"（不报错但数据错）？
- [ ] 用版本号 / feature flag 隔离老路径？
- [ ] 测试覆盖：老 + 新？

## 反模式

```python
# 反：改一处不考虑其他
def update_product(id, **kwargs):
    Product.objects.filter(id=id).update(**kwargs)
    # 老订单的 product_name 跟着变（如果 Product 有此字段）

# 正：分清 SNAPSHOT_FIELDS vs REALTIME_FIELDS
REALTIME_FIELDS = ["name", "description", "status"]
SNAPSHOT_FIELDS = ["price_at_purchase", "sku_at_purchase"]

def update_product(id, **kwargs):
    product = Product.objects.get(id=id)
    for key in REALTIME_FIELDS:
        if key in kwargs:
            setattr(product, key, kwargs[key])
    product.save()
    # SNAPSHOT_FIELDS 不动（订单查 snapshot）
```

## 接入：[completeness-delivery.md](./completeness-delivery.md) 8 项 Checklist 中的 #2 数据 / #3 API / #4 用户 / #5 依赖就是 4 类外部世界的交付检查。
