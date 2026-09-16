# 原则：文件 / 函数 / 圈复杂度 阈值

> 量化"代码简洁"。超过阈值必拆分。

## 阈值表

| 指标 | 阈值 | 例外 |
 |---|---|---|
| **文件行数** | ≤ 300 行 | HTML / CSS / SQL migration / 长 enum 数据 / 长 README 表格 |
| **函数行数** | ≤ 50 行 | 数据 fixture / 配置加载 |
| **圈复杂度** | ≤ 10 | 状态机本身（用 state machine 拆） |
| **嵌套深度** | ≤ 3 层 | 递归算法 |
| **参数个数** | ≤ 4 个 | 超过用参数对象 |
| **单文件 import 数** | ≤ 30 个 | barrel re-export |

## 为什么这些数字

- **300 行 / 文件**：人脑能装下一个屏幕（典型 24 寸 1080p ≈ 60 行）
- **50 行 / 函数**：典型函数应该做一件事，50 行已经偏多
- **圈复杂度 10**：McCabe 经典阈值（> 10 难测试、难理解）
- **嵌套 3 层**：再多就要 extract function
- **参数 4 个**：超过 4 个就该用 options 对象 / builder

## 检测方式

```bash
# 跑 scripts/check_simplicity.py
python3 scripts/check_simplicity.py path/to/file.py
```

## 怎么拆分（不是删，是拆）

```python
# ❌ 100 行函数
def process_order(order):
    # 验证 (10 行)
    # 计算价格 (15 行)
    # 扣库存 (20 行)
    # 发邮件 (15 行)
    # 写日志 (10 行)
    # 更新缓存 (10 行)
    # 返回结果 (5 行)
    # 接收 webhook (15 行)
    pass

# ✅ 拆 7 个函数
def process_order(order):
    validate(order)
    price = calculate_price(order)
    deduct_inventory(order, price)
    send_confirmation(order)
    log_order_event(order)
    update_cache(order)
    return OrderResult(order)
```

## 反模式

- 巨型类 / 巨型函数（"上帝对象"）
- "我把这个文件做完整，方便阅读" → 实际是难读
- 一个文件塞多种语言（`.html.ts` 之类）
- 注释掉的代码（git history 里有）
