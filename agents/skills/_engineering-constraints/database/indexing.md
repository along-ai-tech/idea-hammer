# 索引策略

## 何时建索引

- WHERE 子句涉及的字段
- JOIN ON 子句涉及的字段
- ORDER BY 子句涉及的字段（覆盖索引更佳）
- 复合索引按查询模式排序

## 复合索引最左前缀

```sql
-- 索引 (a, b, c)
CREATE INDEX idx_users_a_b_c ON users(a, b, c);

-- ✅ 能用索引
WHERE a = 1
WHERE a = 1 AND b = 2
WHERE a = 1 AND b = 2 AND c = 3
WHERE a = 1 ORDER BY b
WHERE a = 1 AND b > 1 ORDER BY c

-- ❌ 不能用索引
WHERE b = 2  -- 跳过 a
WHERE c = 3  -- 跳过 a, b
WHERE b = 2 AND c = 3  -- 跳过 a
```

## 覆盖索引（避免回表）

```sql
-- 表 users(id, name, email, age)
-- 查询
SELECT id, name FROM users WHERE email = ?;

-- ✅ 索引 (email) + 包含 id, name（覆盖）
CREATE INDEX idx_users_email ON users(email) INCLUDE (name);
-- MySQL: 用 (email, name)（最左前缀 + 全字段）
```

## 何时不建索引

- 低区分度（boolean / enum / 状态值 < 10 个）
- 超长字段（TEXT / BLOB → 全文索引）
- 频繁更新（索引维护成本）
- 单表 < 1000 行（全表扫更快）
- 写多读少（log / audit）

## 索引失效场景

```sql
-- ❌ 函数 / 表达式
WHERE YEAR(created_at) = 2026  -- 不用索引

-- ✅ 范围
WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'

-- ❌ 前缀模糊
WHERE name LIKE '%keyword%'

-- ✅ 后缀模糊
WHERE name LIKE 'keyword%'

-- ❌ 类型不匹配（name 是 varchar）
WHERE name = 123  -- 隐式转换，不走索引

-- ✅ 正确
WHERE name = '123'

-- ❌ OR 条件
WHERE a = 1 OR b = 2  -- 可能不走索引

-- ✅ UNION
WHERE a = 1
UNION
WHERE b = 2
```

## 索引监控

```sql
-- MySQL
SHOW INDEX FROM users;
EXPLAIN SELECT * FROM users WHERE email = 'a@b.com';
-- 看 type（ALL = 全表扫，ref/range = 用索引）
-- 看 rows（扫描行数，越少越好）
-- 看 Extra（Using filesort / Using temporary = 性能警告）

-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@b.com';
```

## 索引维护

```sql
-- MySQL: 看索引使用情况
SHOW STATUS LIKE 'Handler_read%';
-- Handler_read_key 高 = 索引命中好
-- Handler_read_rnd 高 = 全表扫多

-- 清理冗余索引
-- pt-duplicate-key-checker / akkeba
```

## 反模式

- ❌ 每个字段都建索引
- ❌ 不看 EXPLAIN 就建索引
- ❌ 用函数 / 表达式
- ❌ 索引列做计算（`WHERE price * 2 > 100`）
- ❌ 索引列类型不一致
