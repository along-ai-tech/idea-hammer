# concurrency/ — 并发与分布式约束

> 线程池、分布式锁、幂等、超时 — AI 写并发代码必须遵循。

## 文档

| 主题 | 文档 |
|---|---|
| 线程池命名 | [thread-pool.md](./thread-pool.md) |
| 分布式锁 | [distributed-lock.md](./distributed-lock.md) |
| 幂等性 | [idempotency.md](./idempotency.md) |
| 超时配置 | [timeouts.md](./timeouts.md) |

## 核心原则

1. **必须配超时**（连接 / 读 / 写 / 总）
2. **幂等性优先**（网络不可靠，重试必须安全）
3. **线程池必须命名**（排查问题快）
4. **锁必须有超时**（防死锁）
5. **异步任务必须有失败处理**（重试 + 死信队列）
