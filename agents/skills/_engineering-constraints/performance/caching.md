# 缓存策略

## 三类问题与防护

### 缓存穿透（不存在的 key）

**问题**：每次都打 DB（缓存没数据）

**防护**：
- 缓存空值（短 TTL，如 60 秒）
- 布隆过滤器（Redisson `RBloomFilter`）

```java
// ✅ 缓存空值
public User getById(Long id) {
    String key = "user:" + id;
    String cached = redis.get(key);
    if (cached == null) {
        if ("__NULL__".equals(cached)) return null;
        User user = db.findById(id);
        if (user == null) {
            redis.setex(key, 60, "__NULL__");  // 短 TTL
        } else {
            redis.setex(key, 600, JsonUtil.toJson(user));
        }
        return user;
    }
    return JsonUtil.fromJson(cached, User.class);
}
```

### 缓存雪崩（大量 key 同时失效）

**问题**：TTL 同时到期 → DB 被打挂

**防护**：
- TTL 加随机偏移：`TTL ± 10%`
- 多级缓存（本地 + Redis）
- 预热（启动时加载热点）

```java
// ✅ TTL 加随机
int ttl = 600 + ThreadLocalRandom.current().nextInt(-60, 60);
redis.setex(key, ttl, value);
```

### 缓存击穿（热点 key 失效）

**问题**：并发请求同一个 key，DB 被瞬间打挂

**防护**：
- 分布式锁（只让一个请求查 DB）
- singleflight（Go）/ Redisson `RMapCache`

```java
// ✅ 分布式锁
public User getById(Long id) {
    String key = "user:" + id;
    User cached = redis.get(key);
    if (cached != null) return cached;
    
    RLock lock = redisson.getLock("lock:user:" + id);
    if (lock.tryLock(5, 30, SECONDS)) {
        try {
            // 双重检查
            cached = redis.get(key);
            if (cached != null) return cached;
            User user = db.findById(id);
            redis.setex(key, 600, JsonUtil.toJson(user));
            return user;
        } finally {
            lock.unlock();
        }
    }
    // 锁失败 → 短暂 sleep 重试
    return getById(id);
}
```

## Cache Aside 模式

```java
// 读
value = cache.get(key);
if (value == null) {
    value = db.get(key);
    cache.set(key, value, ttl);
}
return value;

// 写
db.update(key, value);
cache.del(key);  // 不更新（避免并发写）
```

## 缓存设计原则

1. **过期时间必填**（避免内存泄漏）
2. **key 加业务前缀**（`user:123` / `order:456`）
3. **value 不要太大**（> 100KB 考虑压缩或分片）
4. **缓存不是真相**（DB 是 source of truth）
5. **更新缓存要原子**（CAS / Lua）
