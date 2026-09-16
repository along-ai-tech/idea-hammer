# 幂等性

> 防止重复请求 / 重试导致数据错误。

## 强制规则

### 所有 POST / PUT / DELETE 必须考虑幂等性

### 方案 1：Idempotency Key（HTTP 头）

```typescript
// 客户端：每次请求带唯一 key
POST /api/orders
Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000

// 服务端：第一次请求正常处理，记录结果
// 相同 key 第二次请求：返回第一次的结果（不重复处理）
```

```java
@PostMapping("/orders")
public Order createOrder(
    @RequestHeader("Idempotency-Key") String idempotencyKey,
    @RequestBody OrderDTO dto
) {
    // 1. 检查 key 是否已处理
    Order existing = redis.get("idemp:" + idempotencyKey);
    if (existing != null) return existing;
    
    // 2. 加锁防并发
    RLock lock = redisson.getLock("idemp-lock:" + idempotencyKey);
    if (lock.tryLock(5, 30, SECONDS)) {
        try {
            // 双重检查
            existing = redis.get("idemp:" + idempotencyKey);
            if (existing != null) return existing;
            
            // 3. 处理业务
            Order order = orderService.create(dto);
            
            // 4. 缓存结果（24 小时）
            redis.setex("idemp:" + idempotencyKey, 86400, JsonUtil.toJson(order));
            
            return order;
        } finally {
            lock.unlock();
        }
    }
    throw new BusinessException("处理中，请稍后查询");
}
```

### 方案 2：业务唯一键

```sql
-- 用户创建订单，user_id + business_no 唯一
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    business_no VARCHAR(64) NOT NULL,  -- 业务单号（前端生成）
    UNIQUE KEY uniq_user_bizno (user_id, business_no)
);

-- INSERT ON DUPLICATE KEY（重复则忽略）
INSERT INTO orders (user_id, business_no, amount)
VALUES (?, ?, ?)
ON DUPLICATE KEY UPDATE id = id;  -- 无操作，返回已存在

-- 或 SELECT 现有
SELECT * FROM orders WHERE user_id = ? AND business_no = ?;
```

### 方案 3：状态机（乐观锁）

```sql
UPDATE orders
SET status = 'PAID', paid_at = NOW()
WHERE id = ? AND status = 'PENDING';  -- 只在 PENDING 时改
-- 影响 0 行 = 已支付（重复回调）
-- 影响 1 行 = 首次处理
```

## 重试策略

```java
// ✅ 正确：幂等 + 指数退避
RetryTemplate retry = RetryTemplate.builder()
    .maxAttempts(3)
    .exponentialBackoff(1000, 2.0, 10000)  // 1s, 2s, 4s
    .retryOn(TransientException.class)
    .build();

retry.execute(ctx -> {
    return httpClient.post(url, data);  // POST 必须支持幂等
});

// ❌ 错误：无限重试
while (true) {
    try { httpClient.post(url, data); }
    catch (Exception e) { continue; }  // 死循环
}
```

## 反模式

- ❌ POST 不带 Idempotency-Key
- ❌ 重试不带幂等（可能重复扣款）
- ❌ 用时间戳 / 随机数当幂等 key（重试时不同）
- ❌ 数据库无唯一约束（双写问题）
- ❌ 状态机缺少状态校验
