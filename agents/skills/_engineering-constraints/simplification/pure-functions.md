# 原则：副作用隔离（纯函数优先）

> 纯函数 = 输入相同输出相同 + 无副作用 = 可测、可推理、可缓存。副作用集中到边界。

## 纯函数 vs 副作用

| 类型 | 定义 | 例子 |
|---|---|---|
| **纯函数** | 输入 → 输出，无外部影响 | `add(a, b)`, `validate_email(s)`, `parse_json(s)` |
| **副作用** | 改变外部状态（文件 / DB / 网络 / print） | `db.save(x)`, `http.get(url)`, `print("...")` |
| **混合** | 计算 + 副作用混在一起 | `process(x)` 里 print + db.save + 计算 |

## 反模式：计算 + 副作用混

```python
# ❌ 错误：一个函数什么都做
def process_order(order):
    print(f"processing {order.id}")          # 副作用
    db.save(order)                            # 副作用
    notify.send(order.user.email, "...")     # 副作用
    log.info("order done")                    # 副作用
    cache.set(f"order:{order.id}", order)     # 副作用
    return calculate_total(order.items)       # 纯计算被埋在里面


# ✅ 正确：拆分
def calculate_total(items) -> Money: ...    # 纯函数
def save_order(order) -> None: ...           # 一个副作用一个函数
def notify_user(order) -> None: ...
def log_order_event(order) -> None: ...
def cache_order(order) -> None: ...

def process_order(order) -> OrderResult:
    total = calculate_total(order.items)     # 纯
    save_order(order)
    notify_user(order)
    log_order_event(order)
    cache_order(order)
    return OrderResult(order, total)
```

## 边界在哪

| 层 | 边界 |
|---|---|
| **库代码** | 纯函数为主；副作用极少 |
| **API 层** | 集中副作用（HTTP 入口 / DB 出口） |
| **CLI 入口** | 集中副作用（参数解析 / print 结果 / 退出码） |
| **hook** | 集中副作用（文件 I/O / signal） |
| **业务核心** | 纯函数 |

## 副作用的可测试性

```python
# 纯函数：易测
def test_validate_email():
    assert validate_email("a@b.com") is True
    assert validate_email("not-email") is False
# 1 个函数，10 个测试，无 mock

# 副作用函数：难测（要 mock db / network）
def test_process_order():
    with mock.patch('db.save'), mock.patch('notify.send'):
        result = process_order(order)
    # mock 设置比测试本身长
```

## IdeaHammer 实践

- `orchestrator.py` 的 `eval_condition` 是纯（输入 state 返回 bool）
- `orchestrator.py` 的 `find_next_nodes` 是纯（输入 graph + state 返回节点列表）
- `orchestrator.py` 的 `run` 是副作用（print / 调 skill / 更新 state）
- 这种分离让契约测试只测纯函数，副作用函数手动验

## 反模式

```python
# ❌ 错误：混合
def validate_and_save(user):
    if not user.email:
        log.error("missing email")              # 副作用
    db.save(user)                               # 副作用
    return True

# ✅ 正确：分两段
def is_valid(user) -> bool: ...               # 纯
def save_user(user) -> None: ...              # 副作用
def validate_and_save(user) -> bool:
    if not is_valid(user):
        return False
    save_user(user)
    return True
```

## 检测

- code-review：函数含 print / db / http / open() / 等副作用，标"需要拆分"
- pytest：纯函数能直接 `assert func(x) == y`，副作用函数需要 mock
