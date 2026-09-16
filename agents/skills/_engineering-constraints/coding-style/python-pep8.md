# Python 编码规范 — PEP8 + 项目补充

> 引用 PEP8 + PEP257 + Google Python Style Guide 关键条款。

## 强制条款

### 命名

- 模块、函数、变量：`snake_case`
- 类：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 私有：下划线前缀 `_private_var` / `__name_mangled`
- 避免单字母变量（除 lambda / comprehension 短上下文）

### 导入

- 每行一个：`import os` 不写 `import os, sys`
- 顺序：标准库 → 第三方 → 本地，组间空行分隔
- 禁止 `from foo import *`
- 长导入用括号换行

```python
from package import (
    long_module_name,
    another_module,
)
```

### 格式

- 4 空格缩进，不用 Tab
- 行长 ≤ 100（项目可放宽到 120，但默认 100）
- 顶层函数 / 类定义上下空 2 行
- 类内方法空 1 行
- 文件编码 UTF-8

### 类型标注（强制）

- 所有公开函数必须有 type hints
- 用 `from __future__ import annotations` 延迟求值（PEP 563）
- 用 `typing` / `collections.abc` 标准库

```python
from typing import Optional

def fetch_user(user_id: int) -> Optional[User]:
    ...
```

### 文档字符串（PEP 257）

- 公开模块 / 函数 / 类 / 方法必须有 docstring
- Google 风格或 NumPy 风格（项目统一一种）

```python
def fetch_user(user_id: int) -> Optional[User]:
    """根据 ID 获取用户。
    
    Args:
        user_id: 用户唯一标识。
    
    Returns:
        User 实例；用户不存在返回 None。
    
    Raises:
        DatabaseError: 数据库连接失败。
    """
```

### 异常

- 不要 `except:` 捕获所有（捕获 `Exception`）
- 不要 `except Exception as e: pass`（吞异常 = 隐性 bug）
- `raise NewException("msg") from original_exception` 保留链
- 自定义异常继承 `Exception`，不要 `BaseException`
- 用 `contextlib.suppress` 显式表达"忽略某异常"

### 字符串

- f-string 优先（Python 3.6+）：`f"hello {name}"`
- 不用 `+` 拼接循环内字符串（用 `str.join` 或 `io.StringIO`）

### 列表 / 字典推导

- 简单场景用 list/dict comprehension
- 复杂场景用生成器（yield）
- 不用 `filter` / `map` 内置函数（Python 3 中 lambda 比它们可读）

## 推荐条款

- 用 `pathlib.Path` 替代 `os.path`
- 用 `dataclasses` / `pydantic` 替代裸 dict 做 DTO
- 用 `logging` 模块，`logging.getLogger(__name__)`
- 时间处理用 `pendulum` 或 `datetime`（UTC 存，本地显示）
- 异步用 `asyncio` + `async/await`
- 测试用 `pytest`，不用 `unittest`

## 反模式（绝对禁止）

- ❌ `from foo import *`
- ❌ `except: pass`
- ❌ mutable default argument：`def foo(items=[])` （共享状态）
- ❌ `==` vs `is` 混用：`None` 用 `is`，值用 `==`
- ❌ `type(x) == int`（子类判断错）→ `isinstance(x, int)`
- ❌ `while True: time.sleep(1)` 不响应 signal → 用 `select` / signal handler
- ❌ 阻塞调用在异步函数里（httpx 异步版 vs requests 同步）

## 项目补充

- 用 `ruff` 替代 flake8 / isort / black 一体化
- 用 `mypy --strict` 强制类型
- 依赖锁定用 `uv.lock` / `poetry.lock` / `pip-tools`
- 测试覆盖率 ≥ 80%
