# 原则：单一职责（SRP）

> 一个函数 / 类 / 模块只做一件事。

## 函数级

- 一个函数做一件事，做完就返回
- 函数名说"做什么"（动词）而不说"怎么做的细节"
- 嵌套抽象不超过 3 层（function 里调 function 里调 function）

## 类 / 模块级

- 一个类一个职责（不"万能类"）
- 一个文件一个主要导出（除 index / __init__）
- 修改原因只有一个：改这个文件只能因为一个理由

## 文件级

- 文件名 = 模块名（不要 utils.ts / helpers.ts / misc.ts）
- 不超过 300 行（强制）
- 副作用集中：API 层 / hooks 层 / store 层分离

## 反模式

```python
# ❌ 错误：函数做多件事
def process_user(user):
    validate(user)
    save_to_db(user)
    send_email(user)
    log(user)
    update_cache(user)
    return user

# ✅ 正确：每函数做一件事，组合
def validate_and_save(user):
    validate(user)
    save_to_db(user)
    return user

def notify(user):
    send_email(user)
    log(user)

def process_user(user):
    saved = validate_and_save(user)
    update_cache(saved)
    notify(saved)
    return saved
```

## 检测

- check_simplicity.py 检测：函数 > 50 行
- code-review 检测：函数名是否含"and"（如 `validate_and_save` 通常意味着拆 2 个）

## 不适用

- main() / 入口函数（合理的组合）
- 测试函数（可长，但应聚焦一个场景）
- 配置 / fixture 函数（数据组装）
