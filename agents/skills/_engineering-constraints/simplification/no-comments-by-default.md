# 原则：默认不写注释

> 好代码自解释，注释解释 why 不解释 what。

## 写注释的判断

**先问 3 问**：

1. **这段代码在做什么**：→ 命名即文档，改命名而不是写注释
2. **为什么要这么做**：→ ✅ 写注释（解释 why / 决策原因）
3. **有什么坑要注意**：→ ✅ 写注释（解释陷阱）

## 不写注释

```python
# ❌ 错误：注释解释 what（命名应是动词）
# 计算总价
def calc(items):
    return sum(p * q for p, q in items)

# ✅ 正确：命名即文档
def calculate_total(items):
    return sum(price * quantity for price, quantity in items)
```

```typescript
// ❌ 错误
// 设置用户名为输入值
user.name = input;

// ✅ 正确：直接读代码就行
user.name = input;
```

## 要写注释

```python
# ✅ 写 why：解释决策原因
# 我们用 insert + update 两次查询而非 UPSERT，
# 因为 PG 9.6 之前不支持 ON CONFLICT，
# 但当前部署最低版本是 9.4（DBA- 09/2023）。
def upsert_user(user):
    insert_or_update(user)


# ✅ 写 why：解释非显然的坑
# 注意：这里必须用 strict=False，
# 因为旧数据有 None 字段，新 schema 不允许。
parser = Parser(strict=False)


# ✅ 写 why：解释业务背景
# Spec 4.2 节要求这个字段始终在第 3 位，
# 改顺序会破坏现有 API 用户。
FIELDS_ORDER = ["id", "name", "email", "phone"]
```

## 反模式

```python
# ❌ 错误：注释掉的代码（git history 有）
# def old_implementation(x):
#     return x * 2

# ❌ 错误：解释 what 而非 why
# 这里 i 从 0 开始
for i in range(n):
    ...

# ❌ 错误：长块注释解释逻辑（应该改代码）
# 这个函数做以下事情：
# 1. 验证输入
# 2. 转换格式
# 3. 调用服务
# 4. 处理错误
def process(x):
    ...

# ✅ 正确：注释解释 why + 短小
# 用 HashMap 而非 TreeMap：QPS 高，O(n log n) 不可接受
def group_by(items):
    ...
```

## 类型注解代替注释

```python
# ❌ 错误：注释说明参数含义
def transfer(from_acc, to_acc, amt, t):
    """
    from_acc: 来源账户 ID
    to_acc: 目标账户 ID
    amt: 金额（分）
    t: 时间戳
    """
    pass

# ✅ 正确：用类型注解
from dataclasses import dataclass
from datetime import datetime

def transfer(source_account_id: AccountId,
            target_account_id: AccountId,
            amount_cents: int,
            timestamp: datetime):
    pass
```

## 检测

- check_simplicity.py 检测：注释/代码行数比 > 30%（"过度注释"）
- 检测：注释掉的代码（# 后跟代码 / // 后跟代码）
