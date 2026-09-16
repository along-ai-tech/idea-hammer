# 数据库连接池

## 推荐

| 数据库 | Java | Python | Node |
|---|---|---|---|
| **MySQL** | HikariCP | SQLAlchemy pool / pgbouncer | mysql2 pool |
| **PostgreSQL** | HikariCP | psycopg pool / pgbouncer | pg pool |
| **Oracle** | HikariCP / UCP | cx_Oracle pool | oracledb pool |

## HikariCP 配置（Java 主流）

```yaml
spring:
  datasource:
    type: com.zaxxer.hikari.HikariDataSource
    hikari:
      # 连接数
      maximum-pool-size: 20       # max connections
      minimum-idle: 5             # min idle
      
      # 超时
      connection-timeout: 30000   # 30 秒拿不到连接抛 SQLException
      validation-timeout: 5000    # 5 秒验证超时
      max-lifetime: 1800000       # 30 分钟生命周期
      idle-timeout: 600000        # 10 分钟空闲超时
      
      # 连接测试
      connection-test-query: SELECT 1
      # 或更优：connection-init-sql: SELECT 1
      
      # 监控
      register-mbeans: true
      
      # 池名（用于监控）
      pool-name: OrderServicePool
```

## 参数经验值

```yaml
# 计算公式：
# connections = ((core_count * 2) + effective_spindle_count)
# 一般：core * 2 + 1 = 5-20 之间
# 高并发：20-50
# DB 最大连接 100：app pool ≤ 80 (留 buffer)

# Web 应用经验
pool_size = (qps * avg_query_time_seconds) + buffer
# 例：QPS=1000, avg=50ms = 50 + buffer(20%) = 60
# 实际取 20-50（太多 DB 撑不住）
```

## 监控指标

```yaml
# Micrometer 自动暴露
hikaricp.connections.active       # 活跃连接
hikaricp.connections.idle         # 空闲连接
hikaricp.connections.pending      # 等待连接数（> 0 = 池满）
hikaricp.connections.acquire      # 获取连接耗时
hikaricp.connections.usage        # 使用率
```

## 告警

- `pending > 0` 持续 5 分钟：连接不够，加容量
- `active / maximum-pool-size > 80%`：快满了
- `usage.time > 1s`：获取连接慢（DB 慢 / 网络慢）

## Python（SQLAlchemy）

```python
engine = create_engine(
    "postgresql://user:pass@localhost/mydb",
    pool_size=20,
    max_overflow=10,  # 允许临时超出
    pool_pre_ping=True,  # 连接前验证
    pool_recycle=3600,  # 1 小时回收
    echo=False,  # 生产 False
)
```

## Node.js（pg-pool）

```typescript
import { Pool } from 'pg';

const pool = new Pool({
    host: 'localhost',
    database: 'mydb',
    user: 'user',
    password: 'pass',
    max: 20,            // max connections
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 5000,
});

const client = await pool.connect();
try {
    await client.query('SELECT * FROM users');
} finally {
    client.release();
}
```

## 反模式

- ❌ 不配连接池（每次新建连接）
- ❌ pool size = 1000（DB 撑不住）
- ❌ 不配超时（永久等待）
- ❌ 不监控（出问题发现不了）
- ❌ 用完后不释放（连接泄漏）
- ❌ 跨事务共享连接（线程不安全）
