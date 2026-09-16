# 原则：依赖最小化

> 每个 dep 是债务。优先标准库 + 现有生态，不为简单功能装包。

## 核心判断

| 问题 | 决策 |
|---|---|
| stdlib 能做吗 | ✅ 用 stdlib（import 0 字节成本） |
| 已装的某个包能做吗 | ✅ 用它（不增 dep） |
| 真需要新 dep 吗 | 评估：学习成本 / 维护成本 / lockfile / 体积 / 安全 |
| 是 dev-only 吗 | devDep OK（不影响生产 bundle） |

## 反"装包诱惑"

```python
# ❌ 错误：装包只为简单功能
import humanize  # 4MB 依赖，只为 print("2 minutes ago")
print(humanize.naturaltime(dt))

# ✅ stdlib 替代
from datetime import datetime, timezone
def naturalize(dt):
    delta = datetime.now(timezone.utc) - dt
    if delta.days > 0:
        return f"{delta.days} 天前"
    if delta.seconds > 3600:
        return f"{delta.seconds // 3600} 小时前"
    return "刚刚"

print(naturalize(dt))
```

```python
# ❌ 错误：装饰器只为美观
from functools import lru_cache
@lru_cache
def get_user(id): ...  # 不需要缓存！只查一次

# ✅ 不用任何东西
def get_user(id): ...
```

```python
# ❌ 错误：环境变量库
import dotenv
dotenv.load_dotenv()

# ✅ stdlib
import os
value = os.environ.get("KEY", "")
```

## IdeaHammer 现状（保持轻）

当前 7 个 Python 脚本（session.py / orchestrator.py / evolution_stats.py / intent_classifier.py / check_skill_structure.py / check_simplicity.py / session.py）**全部 stdlib only**：

```
pytest + jsonschema + pyyaml  # 仅 tests/contract 需要
```

dev dependencies 之外，零运行时依赖。

## 何时该装新包

- **生态共识**（如 requests / httpx / sqlalchemy）：行业普遍用，长期维护
- **复杂领域**（如 cryptography 处理加密 / Pillow 处理图像）：自己实现 bug 多
- **明确收益**：装包省 > 100 行代码 + 长期维护负担减轻

## 反模式

```python
# ❌ 反模式
- "这个库很酷，我想试试" → 装
- "自己写 5 行代码" → 不，写库更简单 → 装
- "其他项目用了" → 抄过来 → 装
- "作者是名人" → 装

# ✅ 正确决策
- stdlib 有 → 不用
- 已装的有 → 不用
- 真省 > 100 行且长期 → 装
```

## 检测

- `requirements.txt` / `package.json` 行数趋势监控
- code-review：新 dep PR 必须说明"为什么不用 stdlib / 现有包"
- 定期审计：哪些 dep 实际被 import 了？unused 卸
