# 数据库 Migration 安全

## 核心原则

**Schema 变更必须向前兼容**（发布期间老版本和新版本同时在线）。

## 危险操作清单

| 操作 | 风险 | 应对 |
|---|---|---|
| DROP COLUMN | 老代码查该列报错 | 1. 双写 2. 切读 3. 删 |
| RENAME COLUMN | 老代码引用旧名报错 | 1. 加新列 2. 双写 3. 切读 4. 删旧列 |
| CHANGE TYPE | 隐式转换丢失数据 | 用临时列 |
| ADD NOT NULL 无默认值 | 历史数据问题 | 1. 加 nullable 2. backfill 3. NOT NULL |
| DROP TABLE | 外键失效 | 先解除外键约束 |
| ADD INDEX | 锁表（MySQL） | pt-online-schema-change / gh-ost |

## 安全变更模式

### 模式 1：加列（无锁）

```sql
-- ✅ 安全：MySQL 8.0+ instant DDL
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;
```

```sql
-- ❌ 危险（老 MySQL）：加 NOT NULL 无默认值
ALTER TABLE users ADD COLUMN phone VARCHAR(20) NOT NULL;
-- 历史数据没 phone → 失败
```

### 模式 2：删列（4 步）

```sql
-- 第 1 步：代码停止写旧列
--（不需要 SQL 变更）

-- 第 2 步：代码停止读旧列
--（不需要 SQL 变更）

-- 第 3 步：代码部署完，确认无访问

-- 第 4 步：真正删列（用 gh-ost）
ALTER TABLE users DROP COLUMN phone;
```

### 模式 3：rename 列（4 步）

```sql
-- 第 1 步：加新列（nullable）
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20) NULL;

-- 第 2 步：双写（应用层：写两个列）
-- 部署 v2：写 phone + phone_number

-- 第 3 步：数据回填（一次性脚本）
UPDATE users SET phone_number = phone WHERE phone_number IS NULL;

-- 第 4 步：切读到 phone_number
-- 部署 v3：读 phone_number

-- 第 5 步：删除 phone 列
ALTER TABLE users DROP COLUMN phone;
```

### 模式 4：改类型（用临时列）

```sql
-- 老列 phone VARCHAR(15) → 新列 phone VARCHAR(20)

-- 1. 加新列
ALTER TABLE users ADD COLUMN phone_v2 VARCHAR(20) NULL;

-- 2. 双写
-- 3. 回填
UPDATE users SET phone_v2 = phone;

-- 4. 切读
-- 5. 删旧列
ALTER TABLE users DROP COLUMN phone;
ALTER TABLE users RENAME COLUMN phone_v2 TO phone;
```

## 大表 ALTER 工具

| 工具 | 数据库 | 说明 |
|---|---|---|
| **gh-ost** | MySQL | GitHub 开源，无锁 |
| **pt-online-schema-change** | MySQL | Percona 工具 |
| **pg_repack** | PostgreSQL | 无锁 |
| **pgroll** | PostgreSQL | 新兴工具 |

```bash
# gh-ost 示例
gh-ost   --host=db.example.com   --database=myapp   --table=users   --alter="ADD COLUMN phone VARCHAR(20) NULL"   --execute
```

## Migration 工具

| 工具 | 语言 |
|---|---|
| **Flyway** | Java / JVM |
| **Liquibase** | Java / JVM |
| **Alembic** | Python |
| **Knex migrations** | Node.js |
| **goose** | Go |
| **sqlx migrate** | Go |

## 强制规则

1. **每个 migration 都有 up + down**
2. **migration 不可修改**（已合并的不改）
3. **migration 必须向前兼容**
4. **大表变更用 gh-ost / pg_repack**
5. **migration 在 deploy 前在 staging 验证**

## 反模式

- ❌ 一次性大改多个表
- ❌ 不写 down migration
- ❌ 加 NOT NULL 列不带默认值（不回填历史数据）
- ❌ 在大表上直接 ALTER（锁表 → 服务挂）
- ❌ 删列前不验证代码不再引用
