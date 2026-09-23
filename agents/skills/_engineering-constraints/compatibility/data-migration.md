# 原则：数据迁移（Data Migration）

> Schema 变更不破坏老数据。

## 3 阶段（Expand → Migrate → Contract）

```
Phase 1 (Expand):    ALTER TABLE ADD（nullable）+ backfill 老数据
Phase 2 (Migrate):   写双写（新老列同时写）+ 分批迁移（每批 < 10k 行）
Phase 3 (Contract):  读切到新列 + 独立发布删老列
```

## 4 种模式

### 1. 加列 + backfill（最常用）

```sql
ALTER TABLE users ADD COLUMN email_v2 VARCHAR(255);
UPDATE users SET email_v2 = email WHERE id BETWEEN 1 AND 10000;
-- ... 分批跑，避免锁表
ALTER TABLE users DROP COLUMN email;
```

### 2. Snapshot（订单类核心场景）

订单表存创建时的完整快照，不依赖实时商品表：

```sql
ALTER TABLE orders ADD COLUMN product_snapshot JSON;

-- 下单时快照
INSERT INTO orders (product_id, product_snapshot) VALUES (
  123,
  JSON_OBJECT("name", "iPhone 15", "price", 5999)
);

-- 查询读快照（不读 products 表）
SELECT id, product_snapshot->"$.name" FROM orders;
```

核心：**订单查 snapshot，商品升级不影响订单历史**。

### 3. Versioning（多版本共存）

```sql
CREATE TABLE product_versions (
    id BIGINT PRIMARY KEY,
    product_id BIGINT,
    version INT,
    name VARCHAR(255), price DECIMAL(10,2),
    UNIQUE (product_id, version)
);
ALTER TABLE orders ADD COLUMN product_version_id BIGINT;
```

### 4. Event Sourcing（不修改状态，记录事件）

`events: OrderCreated → ItemAdded → PaymentReceived → OrderShipped`，重建状态而非修改。

## 检查清单

- [ ] 老数据需要 backfill 吗？需要多少时间？
- [ ] 分批跑（每批 < 10k 行，避免长事务）
- [ ] 校验：迁移后老列 vs 新列一致
- [ ] 迁移期间读写兼容（双写双读）
- [ ] 大表用 gh-ost / pg_repack（避免锁表）
- [ ] 删老列前确保无引用
- [ ] 回滚方案：保留老列几个版本

详见 [completeness-delivery.md](./completeness-delivery.md) #2。
