# SQL 编码规范 — 跨方言

> 不限数据库（MySQL / PostgreSQL / SQLite / Oracle），通用 SQL 规范。

## 强制条款

### 命名

- 表名、字段名 `snake_case`
- 表名复数（`users`、`orders`）
- 字段名单数（`user_id`、`created_at`）
- 主键 `id`，外键 `<table_singular>_id`（`user_id`）
- 时间字段 `created_at` / `updated_at` / `deleted_at`（TIMESTAMP / DATETIME）
- 索引：`idx_<table>_<columns>`（`idx_users_email`）
- 唯一索引：`uniq_<table>_<columns>`（`uniq_users_phone`）

### 表设计

- 每张表必含 `id`（主键 AUTO_INCREMENT / BIGSERIAL）
- 必含 `created_at` / `updated_at`
- 软删除用 `deleted_at`（NULL = 未删除）
- 字段尽量 NOT NULL（NULL 难处理）
- 字符串长度必填（`VARCHAR(255)` 不是 `VARCHAR`）
- 金额用 `DECIMAL(precision, scale)`，不用 `FLOAT` / `DOUBLE`
- 大文本 `TEXT` / `CLOB`，不用 `VARCHAR(>1000)`

### 查询

- **禁止 `SELECT *`**（必须列字段）
- **必须 `LIMIT`**（分页必须）
- 表别名简短：`u` / `o` / `p`，不要 `user_table` / `order_table_alias`
- JOIN 用显式 `INNER JOIN` / `LEFT JOIN`，不用逗号
- WHERE 条件用参数化（防止 SQL 注入）

```sql
SELECT id, email, created_at
FROM users
WHERE status = ? AND created_at > ?
LIMIT 100;
```

### 索引

- WHERE / JOIN / ORDER BY 涉及的字段建索引
- 复合索引按最左前缀原则排序（`idx_users_status_created` 是 `(status, created_at)`）
- 高频查询用覆盖索引（SELECT 字段都在索引里）
- 不要索引：低区分度字段（boolean / enum）、超长字段（TEXT / BLOB）
- 索引过多影响写入性能（单表 < 5 个）

### 事务

- 短事务原则（避免长事务锁表）
- 明确隔离级别（READ COMMITTED 是默认）
- 避免在事务里做 RPC / HTTP（容易超时回滚）
- 用 `SELECT FOR UPDATE` 时必须有 WHERE 条件 + 索引

### 迁移

- 每次 schema 变更一次 migration
- migration 文件名带时间戳（`20260101120000_add_users_email_idx.sql`）
- 向上 + 向下迁移都要写（`up` / `down`）
- 危险操作（DROP COLUMN / DROP TABLE）拆成多步：
  1. 加新字段（双写）
  2. 应用迁移数据
  3. 切流量
  4. 删旧字段

### 反模式（绝对禁止）

- ❌ `SELECT *`
- ❌ 字符串拼接 SQL（`WHERE name = '" + name + "'"`）
- ❌ `WHERE` 里用计算字段（`WHERE YEAR(created_at) = 2024`）→ `WHERE created_at >= '2026-01-01'`
- ❌ `ORDER BY RAND()`（性能差）
- ❌ `LIMIT 1000000, 20`（深分页 → 用 cursor）
- ❌ `INSERT` 不带字段名（`INSERT INTO users VALUES (...)`）
- ❌ `COUNT(*)` 不带条件（扫全表）
- ❌ 没有 LIMIT 的查询

## 数据库特定

### MySQL
- `utf8mb4` + `utf8mb4_unicode_ci`
- `InnoDB` 引擎
- 大字段（JSON）放 `JSON` 列，避免 VARCHAR(>1000)
- 不建议用 ENUM（用 VARCHAR + 应用层校验）

### PostgreSQL
- `JSONB` 优于 `JSON`
- 时间用 `TIMESTAMPTZ`（带时区），不用 `TIMESTAMP`
- `BIGSERIAL` / `SERIAL` 自增
- 用 `EXPLAIN ANALYZE` 验证查询

### SQLite
- 仅适合嵌入式 / 小型项目
- 写并发受限（用 WAL 模式）
- 类型亲和规则复杂（应用层校验）
