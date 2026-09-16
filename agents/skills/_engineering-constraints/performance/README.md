# performance/ — 性能约束

> AI 写代码必须考虑的硬性性能规则。

## 文档

| 主题 | 文档 |
|---|---|
| 数据库查询 | [db-query.md](./db-query.md) |
| 缓存策略 | [caching.md](./caching.md) |
| Benchmark-first | [benchmark-first.md](./benchmark-first.md) |
| 并发性能 | [concurrency-perf.md](./concurrency-perf.md) |

## 核心原则

1. **不靠记忆优化** — 先 benchmark 再优化
2. **批优先于循环** — 批量操作 > 循环单条
3. **缓存穿透 / 雪崩 / 击穿** 都要防护
4. **N+1 是反模式**
5. **必须 LIMIT，禁止 SELECT ***
