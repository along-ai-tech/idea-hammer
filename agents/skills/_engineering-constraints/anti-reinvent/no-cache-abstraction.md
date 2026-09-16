# 禁止自造缓存抽象

> Spring Cache / Caffeine / Redisson 已完全够用。

## 选型

| 场景 | 推荐 |
|---|---|
| Java 单机缓存 | **Caffeine**（最快） |
| Java 分布式缓存 | **Redisson** / Spring Cache + Redis |
| Python 进程内缓存 | **cachetools** / `functools.lru_cache` |
| Python 分布式缓存 | redis-py |
| Node.js 进程内缓存 | **node-cache** / lru-cache |
| Go 进程内缓存 | **ristretto** / go-cache |

## Java 示例

```java
// ✅ 正确：用 Caffeine（Spring Boot 集成）
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CaffeineCacheManager cacheManager() {
        CaffeineCacheManager manager = new CaffeineCacheManager();
        manager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(10_000)
            .expireAfterWrite(Duration.ofMinutes(10))
            .recordStats());
        return manager;
    }
}

@Service
public class UserService {
    @Cacheable(value = "user", key = "#id")
    public User getById(Long id) { ... }
    
    @CacheEvict(value = "user", key = "#id")
    public void update(Long id, ...) { ... }
}

// ✅ 正确：用 Spring Cache + Redis（分布式）
spring.cache.type=redis
spring.cache.redis.time-to-live=600000

// ❌ 错误：自造 cache 单例
public class MyCache {
    private static Map<String, Object> map = new ConcurrentHashMap<>();
    public static Object get(String key) { return map.get(key); }
}
// 没 TTL、没 LRU、没容量控制 → 内存泄漏
```

## Python 示例

```python
# ✅ 正确：cachetools（TTL + LRU）
from cachetools import TTLCache, LRUCache
import time

cache = TTLCache(maxsize=1000, ttl=600)  # 600 秒 TTL

def get_user(user_id):
    if user_id in cache:
        return cache[user_id]
    user = db.fetch(user_id)
    cache[user_id] = user
    return user

# ✅ 正确：functools.lru_cache（无 TTL）
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_compute(x):
    return ...

# ✅ 正确：分布式用 redis-py
def get_user_distributed(user_id):
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.fetch(user_id)
    redis.setex(f"user:{user_id}", 600, json.dumps(user))
    return user
```

## 反模式

- ❌ 自造 `Map<>` 单例做缓存（没 TTL）
- ❌ `ConcurrentHashMap` 全局（内存泄漏）
- ❌ 没 TTL / 没 LRU / 没容量限制
- ❌ 缓存击穿（热门 key 失效打 DB）→ 用 singleflight / Redisson `RMapCache` 带 TTL
- ❌ 缓存雪崩（大量 key 同时失效）→ TTL 加随机偏移

## 高级特性

- **防击穿**：Redisson `RMapCache` / Caffeine `LoadingCache`
- **防穿透**：缓存空值 + 短 TTL
- **防雪崩**：TTL 加随机 ±10%
- **热 key 探测**：京东 hotkey / 阿里 Tair 热 key
