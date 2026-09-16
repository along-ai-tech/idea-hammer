# 禁止手写分布式锁

> `SETNX` + `EXPIRE` 经典 bug（非原子），Redisson 已解决。

## 经典反模式

```java
// ❌ 错误：经典分布式锁 bug（非原子）
jedis.setnx("lock:order:123", "1");
jedis.expire("lock:order:123", 30);
// 如果 setnx 后服务器崩溃 → 永远不 expire → 死锁

// ❌ 错误：释放别人的锁（没检查 token）
String token = "my-token";
if (jedis.setnx("lock:123", token) == 1) {
    // 业务执行超过 30 秒，锁已过期被别人拿到
    jedis.del("lock:123");  // 删了别人的锁！
}
```

## ✅ 正确：用 Redisson

```java
// ✅ 正确：Redisson RLock（自动续期 / 可重入 / 公平锁）
RLock lock = redisson.getLock("order:123");
try {
    // 默认 30 秒，自动 watchdog 续期（直到 unlock）
    lock.lock();
    // 业务逻辑
} finally {
    lock.unlock();
}

// ✅ 正确：tryLock 带超时
boolean ok = lock.tryLock(5, 30, TimeUnit.SECONDS);
if (ok) {
    try {
        // 业务
    } finally {
        lock.unlock();
    }
}

// ✅ 正确：公平锁（按等待顺序）
RLock fairLock = redisson.getFairLock("order:123");

// ✅ 正确：读写锁
RReadWriteLock rwLock = redisson.getReadWriteLock("data:123");
rwLock.read().lock();
try { ... } finally { rwLock.read().unlock(); }
```

## Redisson 优势

- **自动续期**：watchdog 默认 30 秒，看门狗每 10 秒续期（业务执行多久锁就多久）
- **可重入**：同一线程可多次 lock
- **公平锁**：`getFairLock` 按等待顺序
- **多种语义**：读写锁、信号量、闭锁
- **Lua 原子**：释放锁前检查 token（防误删）

## Python

```python
# ✅ 正确：用 redis-py + Lua 脚本
import redis
import uuid

LOCK_SCRIPT = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
"""

class RedisLock:
    def __init__(self, client, name):
        self.client = client
        self.name = name
        self.token = str(uuid.uuid4())
    
    def acquire(self, ttl=10):
        return self.client.set(self.name, self.token, nx=True, ex=ttl)
    
    def release(self):
        # Lua 脚本保证原子性
        return self.client.eval(LOCK_SCRIPT, 1, self.name, self.token)

# ✅ 更好：用 pottery 库
from pottery import RedisLock
lock = RedisLock(key='order:123', redis=redis_client, expire=10)
with lock:
    # 业务
```

## Node.js

```typescript
// ✅ 正确：用 ioredis + redlock 库
import Redis from 'ioredis';
import Redlock from 'redlock';

const redis = new Redis();
const redlock = new Redlock([redis]);

const lock = await redlock.acquire(['order:123'], 30_000);  // 30 秒
try {
    // 业务
} finally {
    await lock.release();
}
```

## 反模式检测

- grep `setnx.*EXPIRE`（经典 bug）
- `jedis.del("lock")` 不带 token 检查
- `@Lock` 注解手写（用 Redisson Spring Boot Starter）
