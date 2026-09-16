# 原则：删 dead code

> Dead code 是负债，不是资产。git history 永远能找回。

## 什么是 dead code

- 注释掉的代码块（`# old_function()` / `// const x = ...`）
- 未使用的 import / require / include
- 未调用的函数 / 类 / 变量
- 未触发的分支（`if False:` / `if 0:` / 永假条件）
- 注释掉的测试（`# def test_x():`）

## 为什么必须删

| 论点 | 反论点 |
|---|---|
| "保留以备后用" | git history 永久保留 |
| "可能改回去" | 改了改回去概率 < 5%，dead code 拖累 100% |
| "删了就不见了" | git blame / git log 找回 |
| "测试需要" | 测试删了就删了，重写比保留好 |
| "我刚写的" | 越早删越容易 |

## 反模式

```python
# ❌ 错误：注释掉的代码（应该直接删）
def old_validate(user):
    # if user.age > 18:
    #     return True
    return user.age >= 18


# ❌ 错误：未使用的 import
import json  # 没用
import os
from typing import List  # 没用


# ❌ 错误：永远不执行的分支
if False:
    debug_mode()
DEBUG = False
if DEBUG:  # DEBUG 永远是 False
    setup_logging()


# ❌ 错误：未使用的导出
export function unusedHelper() { /* 没人调 */ }
```

## 检测

- ruff（Python）：F401（unused import）/ F841（unused variable）
- eslint（TS）：no-unused-vars / no-unused-imports
- check_simplicity.py：扫描注释掉的代码 / unused import

## 渐进清理策略

- 每周一次："Dead Code Day"，跑工具 + 删
- PR review：发现 dead code 必删，不留 TODO
- 大重构前：先清 dead code（小步安全）

## 不算 dead code

- 公开 API 的导出（即使内部不用）
- 类型导出（IDE 用）
- 测试 fixture（可被多个测试引用）
- 配置文件中的注释（解释为什么这么配）
