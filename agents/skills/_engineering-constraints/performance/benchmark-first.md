# Benchmark-First

> 优化前先 benchmark。优化后验证有效果。

## 原则

**不靠记忆优化，不靠直觉优化**。所有性能改动必须：

1. **优化前**：跑 benchmark 记录基线
2. **优化中**：每次改动再 benchmark，对比
3. **优化后**：保留 benchmark 脚本 + 结果

## 工具

| 语言 | Benchmark 工具 |
|---|---|
| Java | JMH（Java Microbenchmark Harness） |
| Python | pytest-benchmark / timeit |
| Go | 内置 `testing.B` |
| Node.js | benchmark.js / clinic.js |
| 通用 | wrk / k6 / ab（HTTP 压测） |

## 示例（Java JMH）

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
public class MyBenchmark {
    @Benchmark
    public String stringConcat() {
        return "a" + "b" + "c";  // 字符串拼接
    }
    
    @Benchmark
    public String stringBuilder() {
        return new StringBuilder().append("a").append("b").append("c").toString();
    }
}
```

## HTTP 压测（wrk）

```bash
wrk -t12 -c400 -d30s https://api.example.com/orders
# 输出：Requests/sec、Latency、Transfer/sec
```

## 优化判断标准

- **< 5%**：不优化（噪声）
- **5-20%**：看场景（关键路径优化 / 非关键跳过）
- **> 20%**：优化有意义，记录到 CHANGELOG

## 反模式

- ❌ "我觉得这样会快一点"（不 benchmark）
- ❌ "原来就这么写的"（不是不改的理由）
- ❌ "理论上是 O(N)" 但实际是 O(N²)
- ❌ 优化一个 1ms 的循环（用户感知不到）
- ❌ 不保留 benchmark 结果（半年后回滚时不知道为啥改的）
