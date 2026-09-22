# 原则：数据迁移（Data Migration）

> Schema 变更不破坏老数据。改一处数据，要管好老数据 + 老引用。

## 迁移 3 阶段

### Phase 1: Expand（扩展）

- 加新列（新表 / 新字段）
- 老列保留
- 写双写（新老列同时写）

### Phase 2: Migrate（迁移）

- 把老数据 backfill 到新列
- 分批迁移（避免长事务）
- 校验（新老列值一致）

### Phase 3: Contract（收缩）

- 读切到新列
- 删老列（独立发布）

## 4 种迁移模式

### 模式 1: 加列 + backfill（最常用）

```sql
-- Phase 1
ALTER TABLE users ADD COLUMN email_v2 VARCHAR(255);

-- Phase 2 (分批)
UPDATE users SET email_v2 = email WHERE id BETWEEN 1 AND 10000;
UPDATE users SET email_v2 = email WHERE id BETWEEN 10001 AND 20000;
-- ... 分批跑，避免锁表

-- Phase 3 (独立发布)
ALTER TABLE users DROP COLUMN email;
```

### 模式 2: Snapshot（订单类场景）

订单表存创建时的完整快照，不依赖实时商品表：

```sql
ALTER TABLE orders ADD COLUMN product_snapshot JSON;

-- 下单时快照
INSERT INTO orders (product_id, product_snapshot) VALUES (
  123,
  JSON_OBJECT(
    "name", "iPhone 15",
    "price", 5999,
    "spec", {"color": "black", "storage": "128GB"}
  )
);

-- 查询时读快照（不读 products 表）
SELECT id, product_snapshot->"$.name" FROM orders;
```

核心：订单查 product_snapshot，商品升级不影响订单历史。

### 模式 3: Versioning（多版本共存）

商品表分离可变状态：

```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    current_version_id BIGINT
);

CREATE TABLE product_versions (
    id BIGINT PRIMARY KEY,
    product_id BIGINT,
    version INT,
    name VARCHAR(255),
    price DECIMAL(10,2),
    spec JSON,
    created_at TIMESTAMP,
    UNIQUE (product_id, version)
);

-- 订单引用具体版本
ALTER TABLE orders ADD COLUMN product_version_id BIGINT;
```

核心：商品可变，但每个订单绑死具体版本。

### 模式 4: Event Sourcing（事件溯源）

不修改状态，记录事件，重建状态：

```
events:
  - {type: "OrderCreated", order_id: 123, items: [...]}
  - {type: "ItemAdded", order_id: 123, product_id: 456}
  - {type: "PaymentReceived", order_id: 123, amount: 99.99}
  - {type: "OrderShipped", order_id: 123}

current_state = replay(events)
```

核心：历史不可变，重建状态而非修改。

## 实战：商品加版本

### 推荐方案：snapshot + versioning 组合

```sql
-- 1. products 加 version 字段
ALTER TABLE products ADD COLUMN current_version INT DEFAULT 1;

-- 2. order_items 存创建时的快照
ALTER TABLE order_items ADD COLUMN product_snapshot JSON;
ALTER TABLE order_items ADD COLUMN product_version INT;

-- 3. backfill 老订单
UPDATE order_items oi
JOIN products p ON oi.product_id = p.id
SET oi.product_snapshot = JSON_OBJECT(
    "name", p.name, "price", p.price_at_purchase
), oi.product_version = 1
WHERE oi.product_snapshot IS NULL;

-- 4. 商品升级不动 order_items
UPDATE products SET name = "iPhone 16", current_version = 2 WHERE id = 123;
-- 老订单查 product_snapshot 还是 "iPhone 15"
-- 新订单查 product_snapshot 绑死新版本
```

## 迁移检查清单

- [ ] 老数据需要 backfill 吗？需要多少时间？
- [ ] backfill 分批跑（每批 < 10k 行，避免长事务）
- [ ] 校验：迁移后老列 vs 新列值一致
- [ ] 迁移期间读写兼容（双写双读）
- [ ] 迁移完成后删老列（独立发布）
- [ ] 大表 migration 用 gh-ost / pg_repack（避免锁表）
- [ ] 有回滚方案（保留老列几个版本）

## 反模式

```sql
-- 反模式：一次性大改
ALTER TABLE products DROP COLUMN name;
ALTER TABLE products ADD COLUMN display_name VARCHAR(255);
UPDATE products SET display_name = name;
-- 老订单查 name 字段 → 全部 NULL


-- 正确：3 阶段
-- 发布 1: 加 display_name（nullable）
ALTER TABLE products ADD COLUMN display_name VARCHAR(255);

-- 发布 2: backfill
UPDATE products SET display_name = name WHERE display_name IS NULL;

-- 发布 3: 应用层切到 display_name
-- 发布 4: 删 name（独立）
```
