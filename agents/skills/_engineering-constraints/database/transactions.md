# 事务边界

## 核心原则

**短事务、明确边界、最小粒度**。

## 强制规则

### 1. 不要在事务里做 RPC

```java
// ❌ 错误：在事务里调用远程服务
@Transactional
public void createOrder(OrderDTO dto) {
    orderMapper.insert(dto);  // 事务持有连接
    paymentClient.charge(dto);  // RPC，可能慢 → 锁持有时间长
    inventoryClient.deduct(dto);  // 另一个 RPC
    // 任何一个失败 → 回滚 → 锁等待
}

// ✅ 正确：先做事，再开事务
public void createOrder(OrderDTO dto) {
    paymentClient.charge(dto);  // RPC 不在事务
    inventoryClient.deduct(dto);  // RPC 不在事务
    
    transactionTemplate.execute(status -> {
        orderMapper.insert(dto);  // 事务短
        return null;
    });
}
```

### 2. 隔离级别选 READ COMMITTED

```java
// MySQL 默认 REPEATABLE READ（间隙锁）
// 多数业务不需要 → 用 READ COMMITTED

@Transactional(isolation = Isolation.READ_COMMITTED)
public void processOrder(Long orderId) { ... }
```

### 3. 事务传播行为

```java
// 默认 REQUIRED（加入当前事务）
@Transactional(propagation = Propagation.REQUIRED)

// 内部方法新开事务（独立提交/回滚）
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void logAudit(AuditLog log) { ... }

// 不开事务
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public void queryOnly() { ... }

// 强制不开事务（已存在则抛异常）
@Transactional(propagation = Propagation.NEVER)
```

### 4. 不要用 @Transactional 兜底所有方法

```java
// ❌ 错误
@Service
public class OrderService {
    @Transactional  // 所有方法都开事务（包括查询）
    public Order getById(Long id) { ... }
    
    @Transactional
    public List<Order> list() { ... }  // 查询不该用事务
}

// ✅ 正确：只在写方法加事务
@Service
public class OrderService {
    public Order getById(Long id) { ... }  // 无事务
    
    @Transactional(readOnly = true)
    public List<Order> list() { ... }  // 只读事务
    
    @Transactional
    public Order create(OrderDTO dto) { ... }  // 写
}
```

### 5. 异常回滚规则

```java
// Spring 默认只对 RuntimeException 回滚，checked 不回滚
// 显式声明
@Transactional(rollbackFor = Exception.class)  // 所有异常都回滚

// 不要这样
@Transactional(noRollbackFor = RuntimeException.class)  // RuntimeException 不回滚（危险）
```

### 6. 不要在事务里做循环 SQL

```java
// ❌ 错误：1000 次 INSERT 在一个事务里
@Transactional
public void batchInsert(List<User> users) {
    for (User u : users) {
        userMapper.insert(u);
    }
    // 事务持有 1000 次 INSERT 的连接 + 锁
}

// ✅ 正确：批量 INSERT
public void batchInsert(List<User> users) {
    userMapper.batchInsert(users);  // 一次 SQL
}

// ✅ 或分批
public void batchInsert(List<User> users) {
    int batchSize = 500;
    for (int i = 0; i < users.size(); i += batchSize) {
        List<User> batch = users.subList(i, Math.min(i + batchSize, users.size()));
        transactionTemplate.execute(status -> {
            userMapper.batchInsert(batch);
            return null;
        });
    }
}
```

## 分布式事务

见 `concurrency/idempotency.md` 提到的方案：

| 方案 | 适用 | 工具 |
|---|---|---|
| 2PC / XA | 强一致性 | Atomikos / Narayana |
| TCC | 高性能 | Seata |
| Saga | 长事务 | Apache ServiceComb Saga |
| 本地消息表 | 最终一致 | 自建 |
| 事务消息 | 异步 | RocketMQ / Kafka |

## 反模式

- ❌ 事务里调 RPC
- ❌ 事务里 sleep / 等待
- ❌ 事务里循环 SQL
- ❌ 事务粒度太大（覆盖无关操作）
- ❌ 不指定 `rollbackFor`
- ❌ 长事务（持有锁几秒）
