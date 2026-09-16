# 禁止默认线程池

> `Executors.newXxxThreadPool` 默认队列无界 → OOM 风险。

## Java 反模式

```java
// ❌ 错误：默认线程池（队列无界 → OOM）
ExecutorService pool = Executors.newFixedThreadPool(10);
ExecutorService pool = Executors.newCachedThreadPool();  // 无限线程
ExecutorService pool = Executors.newSingleThreadExecutor();

// ❌ 错误：Spring 默认
@Async  // 没配线程池 → 用 SimpleAsyncTaskExecutor（每次新建线程）
```

## ✅ 正确做法

```java
// ✅ 正确：显式 ThreadPoolExecutor
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    5,                                          // corePoolSize
    20,                                         // maximumPoolSize
    60L, TimeUnit.SECONDS,                      // keepAliveTime
    new ArrayBlockingQueue<>(1000),             // 有界队列（关键！）
    new ThreadFactory() {
        private final AtomicInteger counter = new AtomicInteger(1);
        public Thread newThread(Runnable r) {
            return new Thread(r, "biz-pool-" + counter.getAndIncrement());
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()   // 拒绝策略
);

// ✅ 正确：Spring Boot 配置（用 ThreadPoolTaskExecutor）
@Configuration
public class AsyncConfig {
    @Bean(name = "bizPool")
    public Executor bizPool() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("biz-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}

@Async("bizPool")  // 显式指定线程池
public void doAsync() { ... }
```

## 线程池核心参数

| 参数 | 推荐 | 理由 |
|---|---|---|
| corePoolSize | CPU 密集 = N+1，IO 密集 = 2N | 避免太多上下文切换 |
| maxPoolSize | 2-4 倍 core | 弹性扩容 |
| queueCapacity | **必有界**（关键！） | 防 OOM |
| keepAliveTime | 60 秒 | 释放空闲线程 |
| rejected policy | CallerRunsPolicy | 任务不丢，但主线程阻塞（兜底） |
| threadNamePrefix | 业务前缀（"order-pool"、"pay-pool"） | 调试方便 |

## Python

```python
# ✅ 正确：用 concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=20, thread_name_prefix='biz') as pool:
    futures = [pool.submit(task, arg) for arg in args]

# ✅ 正确：用 FastAPI 自带（uvicorn workers）
# 配置 workers=N（不要 N 太大）

# ❌ 错误：自造线程池
class MyThreadPool:
    def __init__(self, size):
        self.threads = = ...
```

## Node.js

单线程 + event loop，不需要线程池。但 CPU 密集任务用 worker_threads：

```typescript
// ✅ 正确：worker_threads
import { Worker } from 'node:worker_threads';

const worker = new Worker('./heavy-task.js', { workerData: { ... } });
```

## 反模式检测

- `Executors.newFixedThreadPool`
- `Executors.newCachedThreadPool`
- `@Async` 不带指定 pool
- `ThreadPoolExecutor` 但 `queueCapacity` 默认（Integer.MAX_VALUE）
- `threadName` 没设业务前缀
