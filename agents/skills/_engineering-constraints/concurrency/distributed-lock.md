# 分布式锁

> 见 `anti-reinvent/no-distributed-lock.md` 详细禁止项。本文档讲怎么用对。

## Redisson 实战

```java
@Service
public class OrderService {
    @Autowired
    private RedissonClient redisson;
    
    public void createOrder(Long userId, OrderDTO dto) {
        // ✅ 推荐：业务前缀 + 资源 ID
        String lockKey = "lock:order:create:" + userId;
        RLock lock = redisson.getLock(lockKey);
        
        try {
            // 默认 30 秒，watchdog 自动续期
            boolean ok = lock.tryLock(5, 30, TimeUnit.SECONDS);
            if (!ok) {
                throw new BusinessException("系统繁忙，请稍后重试");
            }
            
            // 双重检查（防击穿）
            if (userHasPendingOrder(userId)) {
                throw new BusinessException("已有进行中的订单");
            }
            
            // 业务逻辑
            createOrderInDb(userId, dto);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new BusinessException("操作被中断");
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}
```

## 锁分类选择

| 锁类型 | 用法 | 场景 |
|---|---|---|
| `getLock` | 默认可重入非公平 | 通用 |
| `getFairLock` | 公平锁（FIFO） | 防止饥饿 |
| `getReadWriteLock` | 读写锁 | 读多写少 |
| `getSpinLock` | 自旋锁 | 短任务 |
| `getMultiLock` | 多锁合并 | 跨资源 |

## 锁粒度

```java
// ❌ 错误：粒度太粗
RLock lock = redisson.getLock("lock:all-users");

// ✅ 正确：粒度适中
RLock lock = redisson.getLock("lock:order:user:" + userId);

// ✅ 更细：粒度到资源
RLock lock = redisson.getLock("lock:order:" + orderId);
```

## 信号量（限流）

```java
RSemaphore semaphore = redisson.getSemaphore("api:rate-limit");
semaphore.trySetPermits(100);  // 100 个许可

// 申请
if (semaphore.tryAcquire(1, 5, TimeUnit.SECONDS)) {
    try {
        // 业务
    } finally {
        semaphore.release();
    }
} else {
    throw new BusinessException("请求过于频繁");
}
```

## 闭锁（CountDownLatch）

```java
RCountDownLatch latch = redisson.getCountDownLatch("task:batch:123");
latch.trySetCount(10);  // 等待 10 个任务

// 子任务
latch.countDown();

// 主线程等待
latch.await(30, TimeUnit.SECONDS);
```

## 反模式

- ❌ `SETNX + EXPIRE`（非原子）
- ❌ 释放锁不检查 token（删别人的锁）
- ❌ 锁不带超时（死锁）
- ❌ 锁粒度太粗（性能差）
- ❌ 业务执行 > 锁超时（要续期）
