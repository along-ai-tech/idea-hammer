# 原则：幂等性（重复执行安全）

> 脚本 / hook 反复触发，结果相同。第一次成功 ≠ 第二次安全。

## 核心问题

```python
# ❌ 错误：第二次会重复追加
def add_signal(signal):
    signals.append(signal)  # 每次都加
    save(signals)

# 第一次：signals = [A]
# 第二次：signals = [A, A]  # bug
```

## 为什么 IdeaHammer 必须重视

- **hook 反复触发**：`UserPromptSubmit` 每次用户输入都触发，`detect-feedback-signal` 可能同一 prompt 多次
- **scripts 可重入**：CI / 手动手动跑都可能重复 `session.py update`
- **AI 写脚本倾向"append"**：对"加信号 / 加状态"这类操作，AI 默认 append，忘了去重

## 4 种幂等模式

### 1. 按 ID 去重

```python
def add_signal(signal):
    existing = load_signals()
    if any(s.id == signal.id for s in existing):
        return  # 幂等
    existing.append(signal)
    save(existing)
```

### 2. 状态判断（先查后改）

```python
def mark_processed(order_id):
    order = db.get(order_id)
    if order.processed:
        return  # 已处理，跳过
    process(order)
    db.update(order)
```

### 3. 完整覆盖（用最新值）

```python
def update_session(state_key, value):
    session = load_session()
    session[state_key] = value  # 覆盖不是追加
    save(session)
```

### 4. 事务回滚

```python
@transaction
def transfer(from_id, to_id, amount):
    """数据库事务保证：失败则全部回滚"""
    from_account = lock(from_id)
    from_account.balance -= amount
    to_account = lock(to_id)
    to_account.balance += amount
```

## 反模式

```python
# ❌ 反模式 1：append 而不查重
def add_signal(signal):
    signals.append(signal)
    save(signals)

# ❌ 反模式 2：用时间戳不查重
def add_signal(signal):
    if signal.timestamp != last_timestamp:  # 时间戳冲突
        signals.append(signal)
    # 同一秒内两次会重复

# ❌ 反模式 3：random id 但不查重
def add_signal(signal):
    signal.id = str(uuid4())  # 每次新 ID
    signals.append(signal)    # 不查重

# ❌ 反模式 4：retry 不幂等
def process(order):
    order.charge()  # 网络调用
    order.save()
# retry 时 charge 两次但 save 一次 → 重复扣款
```

## IdeaHammer 实践

```python
# session.py update 用模式 3（覆盖）
session[key_decisions][-1] = new_decision  # 不是 append

# signals.jsonl 写入用模式 1
def add_signal(signal):
    if any(line.id == signal.id for line in load_signals()):
        return
    signals.append(signal)

# hook 用模式 2
def detect_signal(prompt):
    signal = make_signal(prompt)
    if already_recorded(signal):
        return  # 同 prompt 不重复入队
    record(signal)
```

## 检测

- code-review："append"操作必查幂等
- pytest：同一函数调 2 次结果相同 = 幂等测试
  ```python
  def test_idempotent():
      before = run()
      after = run()  # 再跑一次
      assert after == before
  ```

## 不变量

- **所有写操作**默认要求幂等（即使文档没写）
- **all hooks**：同一事件触发 N 次 = 触发 1 次的效果
- **CI 重跑**：重跑 CI = 第一次跑结果
