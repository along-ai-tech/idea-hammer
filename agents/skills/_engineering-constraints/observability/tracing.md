# 链路追踪

## OpenTelemetry（推荐）

### Java

```xml
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-api</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

```java
// 自动埋点（Java Agent）
// -javaagent:opentelemetry-javaagent.jar
// -Dotel.service.name=order-service
// -Dotel.exporter.otlp.endpoint=http://otel-collector:4317

// 手动埋点
Tracer tracer = GlobalOpenTelemetry.getTracer("order-service");

Span span = tracer.spanBuilder("createOrder")
    .setAttribute("order.id", orderId)
    .setAttribute("user.id", userId)
    .startSpan();

try (Scope scope = span.makeCurrent()) {
    // 业务
    db.query();  // 自动埋点（如果用 JDBC instrumentation）
    httpClient.post();  // 自动埋点
} catch (Exception e) {
    span.recordException(e);
    span.setStatus(StatusCode.ERROR);
    throw e;
} finally {
    span.end();
}
```

### Python

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi
```

```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("create_order") as span:
    span.set_attribute("order.id", order_id)
    db.query()
```

## 关键字段

- `service.name`：服务名
- `trace.id`：请求链路 ID（串联所有 span）
- `span.id`：单个操作 ID
- `parent.span_id`：父 span
- `http.method` / `http.url` / `http.status_code`
- `db.statement` / `db.system`
- 自定义业务字段：`user.id` / `order.amount`

## 采样策略

```yaml
# 生产：1% 采样（避免性能开销）
otel:
  traces:
    sampler: traceidratio
    sampler.arg: 0.01
    
# 错误全采样
- rule: errors
  sampler: always_on
```

## 集成

- **Jaeger / Tempo / Zipkin**：可视化链路
- **Grafana**：指标 + 链路查询
- **APM（Datadog / New Relic）**：商业方案

## 反模式

- ❌ 不带 trace_id（无法关联）
- ❌ 自造追踪协议（用 OpenTelemetry）
- ❌ 100% 采样（生产环境性能差）
- ❌ 错误不 recordException
- ❌ 关键业务字段不带（无法定位慢请求）
- ❌ span 名不具体（`"process"` 而不是 `"createOrder"`）
