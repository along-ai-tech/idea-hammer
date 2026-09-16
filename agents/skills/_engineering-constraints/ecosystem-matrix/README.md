# ecosystem-matrix/ — 库选择指南

> "X 场景该用哪个库"决策矩阵。AI 写代码必须查这个，不要凭记忆选。

## 决策原则

1. **优先框架自带**（Spring 自带的，Python 标准库的）
2. **其次成熟生态**（Java 优先 Hutool > Apache Commons > Guava）
3. **不造轮子**：每个场景都有推荐，禁止自造
4. **查最新版**：用前 WebSearch 确认当前生态版本

## 矩阵目录

| 主题 | 文档 |
|---|---|
| Java 工具库 | [java-ecosystem.md](./java-ecosystem.md) |
| Python 工具库 | [python-ecosystem.md](./python-ecosystem.md) |
| 前端库 | [frontend-ecosystem.md](./frontend-ecosystem.md) |
| Redis 客户端 | [redis-clients.md](./redis-clients.md) |
| 数据库 ORM | [database-orm.md](./database-orm.md) |

## 反模式

- ❌ 同一个能力引入 2 个库（如同时用 Hutool + Guava）
- ❌ 用小众/未维护的库（如 Fastjson 已停更）
- ❌ 用 GPL / AGPL 等传染性 license
- ❌ 选了"看起来高大上"的库但项目简单（如 GraphQL 用于 CRUD）
