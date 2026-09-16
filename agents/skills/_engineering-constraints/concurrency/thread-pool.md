# 线程池命名与配置

## 强制规则

### 1. 必须有名字前缀

```java
// ✅ 正确：业务前缀
ThreadFactory namedFactory = new ThreadFactory() {
    private final AtomicInteger counter = new AtomicInteger(1);
    @Override
    public Thread newThread(Runnable r) {
        Thread t = new Thread(r, "order-pool-" + counter.getAndIncrement());
        t.setDaemon(true);
        return t;
    }
};

// ❌ 错误：默认名（pool-1-thread-1）
```

### 2. 必须有界队列

```java
// ✅ 正确
new ThreadPoolExecutor(5, 20, 60, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(1000), namedFactory, new CallerRunsPolicy());

// ❌ 错误：默认无界 → OOM
Executors.newFixedThreadPool(10);  // 内部用 LinkedBlockingQueue 无界
```

### 3. 必须配拒绝策略

```java
// 业务场景选合适的：
new ThreadPoolExecutor.CallerRunsPolicy()    // 主线程兜底（不丢任务）
new ThreadPoolExecutor.AbortPolicy()        // 抛异常（快速失败）
new ThreadPoolExecutor.DiscardPolicy()      // 丢弃（容忍丢失）
new ThreadPoolExecutor.DiscardOldestPolicy() // 丢老的（队列满时）
```

### 4. 核心参数经验值

| 场景 | core | max | queue |
|---|---|---|---|
| CPU 密集（计算） | N+1 | N+1 | 100 |
| IO 密集（DB / HTTP） | 2N | 4N | 500-1000 |
| 混合 | N | 2N | 200-500 |

N = CPU 核心数

## Spring Boot 配置

```java
@Configuration
public class ThreadPoolConfig {
    @Bean(name = "orderPool")
    public ThreadPoolTaskExecutor orderPool() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(500);
        executor.setKeepAliveSeconds(60);
        executor.setThreadNamePrefix("order-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(60);
        executor.initialize();
        return executor;
    }
}

@Service
public class OrderService {
    @Async("orderPool")
    public void asyncProcess(Long orderId) {
        // 在 orderPool 里跑
    }
}
```

## 监控

```java
// Micrometer 自动埋点
executor.setTaskDecorator(runnable -> {
    long start = System.nanoTime();
    try {
        return runnable;
    } finally {
        long duration = System.nanoTime() - start;
        Timer.record("thread.pool.task", duration, "pool", "order");
    }
});
```

## 反模式

- ❌ `Executors.newFixedThreadPool`（无界队列）
- ❌ `Executors.newCachedThreadPool`（无限线程）
- ❌ `@Async` 不指定 pool（默认 SimpleAsyncTaskExecutor 每次新建）
- ❌ 不命名（排查问题找不到）
- ❌ shutdown 不 wait（任务丢失）
