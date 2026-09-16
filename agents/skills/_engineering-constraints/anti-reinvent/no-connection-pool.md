# 禁止自造连接池

> 数据库 / HTTP / Redis 都有成熟连接池生态，自造是反模式。

## 数据库连接池

**禁止手写数据库连接池**。成熟方案：

- **Java**: HikariCP（Spring Boot 默认）/ Druid（带监控）
- **Python**: SQLAlchemy 内置连接池 / pgbouncer
- **Node.js**: pg-pool / mysql2 pool
- **Go**: database/sql 内置 pool / sqlx

```java
// ✅ 正确：用 HikariCP（Spring Boot 自动配置）
spring.datasource.url=jdbc:mysql://...
spring.datasource.hikari.maximum-pool-size=20

// ❌ 错误：自造连接池
public class MyConnectionPool {
    private List<Connection> pool = new ArrayList<>();
    public Connection getConnection() { ... }  // 不要写
}
```

## HTTP 连接池

**禁止每次新建 HTTP 客户端**。必须用连接池：

- **Java**: OkHttp（内置连接池）/ Apache HttpClient 5
- **Python**: httpx.Client（复用）
- **Node.js**: undici（Node 内置）/ axios.create()

```python
# ✅ 正确：复用 httpx.Client
client = httpx.Client(timeout=10.0)
for url in urls:
    resp = client.get(url)

# ❌ 错误：每次新建（连接泄漏）
for url in urls:
    resp = httpx.get(url)  # 每次新建连接
```

## Redis 连接池

**禁止手写 Redis 连接池**：

- **Java**: Lettuce / Jedis / Redisson（都有连接池）
- **Python**: redis-py 默认连接池
- **Node.js**: ioredis（自动管理）

```java
// ✅ 正确：用 Redisson 配置连接池
Config config = new Config();
config.useSingleServer()
    .setAddress("redis://localhost:6379")
    .setConnectionPoolSize(64);
RedissonClient redisson = Redisson.create(config);
```

## 反模式检测

code-review Stage 2 grep：
- `class.*ConnectionPool`（自造连接池）
- `new Jedis()`（每次新建，不用连接池）
- `httpx.get()` 在循环里（每次新建）

## 例外（允许自造的情况）

1. 极其特殊的硬件 / 协议（罕见）
2. 成熟方案都不满足的极限性能需求（先 benchmark 证明）
3. 自造后必须写：
   - 性能对比 benchmark
   - 与成熟方案的差异说明
   - 单测覆盖率 ≥ 95%
