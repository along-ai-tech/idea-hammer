# Redis 客户端矩阵

> 不同语言下选哪个 Redis 客户端。

## Java

| 场景 | 首选 | 次选 | 禁止 |
|---|---|---|---|
| 通用客户端 | **Lettuce**（Spring Boot 默认） | Jedis | ❌ 手写 RESP 协议 |
| 分布式锁 / 限流 / 队列 | **Redisson** | Lettuce + 手写 | ❌ `SETNX + EXPIRE` 手写 |
| 缓存注解 | **Spring Cache + Redis** | JetCache | ❌ AOP 自造 |

**Redisson 优势**：
- 分布式锁：`RLock` 自动续期（watchdog）
- 限流：`RRateLimiter`
- 队列：`RQueue` / `RDelayQueue`
- 布隆过滤器：`RBloomFilter`
- 分布式集合：`RMap` / `RList` / `RSet`

```java
// ✅ 正确：用 Redisson
RLock lock = redisson.getLock("order:123");
lock.lock();
try {
    // 业务
} finally {
    lock.unlock();
}

// ❌ 错误：手写 SETNX
jedis.setnx("lock:123", "1");
// 忘了设置过期时间 → 死锁
```

## Python

| 场景 | 首选 | 次选 |
|---|---|---|
| 同步客户端 | **redis-py**（官方） | - |
| 异步客户端 | **redis.asyncio**（redis-py 内置） | aioredis（已并入 redis-py） |
| 连接池 | redis-py 内置 | - |
| 分布式锁 | **redis-py + Lua** | pottery |

```python
# ✅ 正确：用 redis-py
import redis
r = redis.Redis(host='localhost', port=6379)
r.set('key', 'value', ex=60)  # TTL 一起设

# 分布式锁用 SET NX EX
ok = r.set('lock:123', token, nx=True, ex=10)
```

## Node.js / TypeScript

| 场景 | 首选 | 次选 |
|---|---|---|
| 通用客户端 | **ioredis** | node-redis |
| BullMQ（队列） | ioredis（BullMQ 依赖） | - |

```typescript
import Redis from 'ioredis';
const redis = new Redis({ host: 'localhost', port: 6379 });
await redis.set('key', 'value', 'EX', 60);
```

## Go

| 场景 | 首选 | 次选 |
|---|---|---|
| 通用客户端 | **go-redis** | redigo |
| 高级特性 | rueidis（基于 RESP3） | - |

## 反模式（绝对禁止）

- ❌ 手写 RESP 协议
- ❌ 手写 `SETNX` + `EXPIRE`（两步非原子，分布式锁经典 bug）
- ❌ 不用连接池（每次 `new Jedis()`）
- ❌ 用 Jedis 时多线程共享一个实例（非线程安全）
- ❌ 锁不带超时（死锁风险）
- ❌ 用 `KEYS` 命令（O(N) 阻塞）
- ❌ 用 `FLUSHDB` 在生产

## 选型决策树

```
需要分布式锁 / 限流 / 队列 / BloomFilter？
├── 是 → Redisson（Java）/ pottery（Python）
└── 否 → 通用客户端即可
    ├── Java → Lettuce（Spring Boot 默认）
    ├── Python → redis-py
    ├── Node → ioredis
    └── Go → go-redis
```
