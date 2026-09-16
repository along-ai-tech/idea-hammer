# 指标埋点

## 四大黄金指标（Google SRE）

1. **流量（Traffic）**：QPS / RPS
2. **延迟（Latency）**：p50 / p95 / p99
3. **错误率（Errors）**：HTTP 5xx / 4xx 比率
4. **饱和度（Saturation）**：CPU / 内存 / 队列长度

## 强制埋点

### HTTP 服务

```java
// ✅ Spring Boot + Micrometer
@RestController
public class OrderController {
    @PostMapping("/orders")
    public Order create(@RequestBody OrderDTO dto) {
        return Timer.builder("order.create")
            .tag("status", "success")
            .register(meterRegistry)
            .record(() -> orderService.create(dto));
    }
}

// 自动埋点（Spring Boot Actuator）
management.endpoints.web.exposure.include=health,metrics,prometheus
management.metrics.export.prometheus.enabled=true
```

### 数据库

```java
Timer.builder("db.query")
    .tag("table", "users")
    .tag("operation", "select")
    .register(meterRegistry)
    .record(() -> userMapper.findById(id));
```

### 业务指标

```java
Counter.builder("order.created")
    .tag("channel", "web")
    .register(meterRegistry)
    .increment();

Gauge.builder("queue.size", queue, q -> q.size())
    .register(meterRegistry);
```

## 指标类型

| 类型 | 用途 | 例 |
|---|---|---|
| **Counter** | 累计计数 | 订单数、错误数 |
| **Gauge** | 当前值 | 队列长度、连接池大小 |
| **Histogram** | 分布统计 | 请求耗时、响应大小 |
| **Summary** | 分布统计（预聚合） | 同上 |

## 命名规范

```
格式：<namespace>.<entity>.<action>
例：order.create.duration / http.request.duration / db.query.duration
```

## 标签规范

```java
// ✅ 正确：低基数标签
.tag("method", "GET")
.tag("status", "200")
.tag("table", "users")

// ❌ 错误：高基数标签（爆炸）
.tag("userId", userId)  // 100 万用户 = 100 万时间序列
.tag("orderId", orderId)  // 每订单一个时间序列
```

**低基数**：状态码 / 方法名 / 表名 / endpoint
**高基数**：用户 ID / 订单 ID（用日志，不用指标）

## 告警规则

```yaml
# Prometheus
groups:
- name: order-service
  rules:
  - alert: HighErrorRate
    expr: |
      sum(rate(order_create_errors_total[5m])) 
      / 
      sum(rate(order_create_total[5m])) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "订单创建错误率 > 5%"

  - alert: HighLatency
    expr: |
      histogram_quantile(0.99, sum(rate(order_create_duration_seconds_bucket[5m])) by (le))
      > 1.0
    for: 5m
    annotations:
      summary: "P99 延迟 > 1 秒"
```

## 反模式

- ❌ 用 Gauge 累计（应该用 Counter）
- ❌ 高基数标签（用户 ID）
- ❌ 不分命名空间（所有指标混在一起）
- ❌ 不带 status / method 标签
- ❌ 告警阈值不合理（太宽松 / 太严格）
- ❌ 只看 QPS 不看错误率
