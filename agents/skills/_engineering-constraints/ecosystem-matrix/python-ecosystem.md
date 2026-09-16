# Python 生态矩阵

> Python 后端 + 工具库选择决策。

## Web 框架

| 场景 | 首选 | 次选 |
|---|---|---|
| 同步 Web | **Django** / **Flask** | Pyramid |
| 异步 Web | **FastAPI** | Starlette / Sanic |
| 全栈（admin/ORM） | **Django** | - |

## 工具库

| 场景 | 首选 | 次选 | 禁止 |
|---|---|---|---|
| 配置 | **pydantic-settings** | dynaconf | ❌ 手写 yaml/json 加载 |
| 数据验证 | **pydantic** | marshmallow | ❌ 手写 if-else 校验 |
| ORM | **SQLAlchemy 2.0** | Django ORM / Tortoise | ❌ 裸 cursor / pymysql |
| HTTP 客户端 | **httpx**（异步同步两用） | requests | ❌ urllib / aiohttp 单独 |
| JSON | **orjson** / pydantic | ujson / json | ❌ 自造 JSON 解析 |
| 日期时间 | **pendulum** | arrow / datetime | ❌ 自造 DateUtil |
| 测试 | **pytest** | unittest | ❌ doctest 作主测 |
| Mock | **pytest-mock** / unittest.mock | - | ❌ 自造 mock |
| 日志 | **structlog** / loguru | stdlib logging | ❌ print 留生产 |
| 异步 | **asyncio + httpx** | trio / curio | ❌ 同步调用在 async |
| 分布式锁 | **redis-py + Lua** | pottery | ❌ `SETNX` 不带 EX |
| 缓存 | **cachetools** + redis | - | ❌ 自造 LRU |
| 任务队列 | **Celery** / **RQ** | dramatiq | ❌ 自造 worker |
| 数据库迁移 | **Alembic** | yoyo-migrations | ❌ 手写 ALTER |
| API 文档 | **FastAPI 自动生成** | apispec | ❌ 手写接口文档 |
| 密码哈希 | **passlib[bcrypt]** / argon2-cffi | bcrypt | ❌ md5 / sha1 |
| JWT | **PyJWT** | authlib | ❌ 手写 base64 解码 |
| 加密 | **cryptography** | PyCrypto（已停更） | ❌ 自造 |

## 数据处理

| 场景 | 首选 | 次选 |
|---|---|---|
| 数值计算 | **numpy** | - |
| 数据分析 | **pandas** | polars |
| 机器学习 | **scikit-learn** / **PyTorch** | XGBoost |
| HTTP 爬虫 | **httpx + selectolax** | requests + bs4 |
| 浏览器自动化 | **playwright** | selenium |

## 反模式

- ❌ 用 `requests` + `asyncio`（同步调用阻塞 event loop）
- ❌ 用 `pymysql` 裸 SQL（用 SQLAlchemy）
- ❌ 用 `pickle` 反序列化外部数据（RCE 风险）
- ❌ 用 `eval` / `exec` 处理用户输入
- ❌ 用 `subprocess.Popen(shell=True)` 处理用户输入（命令注入）
- ❌ 用 `random` 做密码 / token（用 `secrets`）
