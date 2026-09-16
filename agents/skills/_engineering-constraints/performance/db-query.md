# 数据库查询性能

## 强制规则

### N+1 禁止

```python
# ❌ 错误：N+1 查询
users = User.query.all()
for user in users:
    print(user.department.name)  # 每次都查一次

# ✅ 正确：JOIN / eager load
users = User.query.options(joinedload(User.department)).all()
```

```java
// ❌ 错误：N+1
List<User> users = userMapper.findAll();
for (User u : users) {
    Department dept = deptMapper.findById(u.getDeptId());  // N+1
}

// ✅ 正确：JOIN
@Select("SELECT u.*, d.name dept_name FROM users u LEFT JOIN departments d ON u.dept_id = d.id")
List<UserWithDept> findAllWithDept();
```

### SELECT * 禁止

```sql
-- ❌ 错误
SELECT * FROM users WHERE id = ?;

-- ✅ 正确
SELECT id, email, created_at FROM users WHERE id = ?;
```

### LIMIT 强制

```sql
-- ❌ 错误（扫全表）
SELECT id, name FROM users WHERE status = 'active';

-- ✅ 正确
SELECT id, name FROM users WHERE status = 'active' LIMIT 100;
```

### 慢查询监控

- **阈值**：单查询 > 100ms 警告，> 500ms 必查
- **工具**：MySQL `slow_query_log` / PostgreSQL `pg_stat_statements` / APM
- **优化方向**：EXPLAIN → 索引 → 改写 → 缓存

### 深分页禁止

```sql
-- ❌ 错误：offset 越大越慢
SELECT * FROM users LIMIT 1000000, 20;

-- ✅ 正确：cursor 分页
SELECT * FROM users WHERE id > 12345 ORDER BY id LIMIT 20;
```

### 索引策略

- WHERE / JOIN / ORDER BY 字段建索引
- 复合索引按最左前缀排序
- 高频查询用覆盖索引（SELECT 字段都在索引里）
- 不索引：低区分度字段、超长字段、频繁更新的字段

### 连接池配置

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20  # 经验：业务并发 QPS / 单查询 RT
      minimum-idle: 5
      connection-timeout: 30000  # 30 秒
      max-lifetime: 1800000      # 30 分钟
      idle-timeout: 600000       # 10 分钟
```

## 反模式

- ❌ 循环里 `await db.query()`
- ❌ `SELECT COUNT(*) FROM huge_table`
- ❌ `SELECT MAX(id) FROM table`（用 `ORDER BY id DESC LIMIT 1`）
- ❌ `WHERE YEAR(created_at) = 2026`（不用索引）→ `WHERE created_at >= '2026-01-01'`
- ❌ `LIKE '%keyword%'`（全表扫）→ 全文索引
- ❌ `ORDER BY RAND()`（O(N log N)）
