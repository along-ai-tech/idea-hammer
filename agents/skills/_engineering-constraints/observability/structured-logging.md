# 结构化日志

## 强制规则

### 1. 用 JSON 格式

```json
{
    "timestamp": "2026-09-16T17:00:00.123Z",
    "level": "INFO",
    "logger": "OrderService",
    "message": "Order created",
    "trace_id": "abc-123-def-456",
    "span_id": "span-789",
    "user_id": "user-123",
    "order_id": "order-456",
    "amount": 99.99,
    "duration_ms": 45
}
```

### 2. 用 trace_id 串联

```java
// 每个请求生成 trace_id
String traceId = UUID.randomUUID().toString();
MDC.put("trace_id", traceId);

// 所有日志自动带 trace_id
log.info("Order processing started");
log.info("Payment processing");
log.info("Order completed");

// HTTP 响应头也带（前端可拿）
response.setHeader("X-Trace-Id", traceId);

// 请求结束时清理
MDC.clear();
```

### 3. 不记敏感信息

```java
// ❌ 错误
log.info("Login: email={}, password={}", email, password);
log.info("Payment: card={}", cardNumber);

// ✅ 正确：脱敏
log.info("Login: email={}", maskEmail(email));
log.info("Payment: card_last4={}", cardNumber.substring(cardNumber.length() - 4));
```

**禁止日志包含**：
- 密码 / API Key / Token
- 信用卡完整号（PCI-DSS 要求）
- 身份证 / SSN
- 邮箱完整（脱敏为 `w***@example.com`）
- 手机号完整（脱敏为 `138****1234`）

### 4. 日志级别

| 级别 | 何时用 |
|---|---|
| ERROR | 需立即处理（系统错误、未捕获异常） |
| WARN | 不阻塞但需注意（重试、降级） |
| INFO | 关键业务节点（订单创建、支付成功） |
| DEBUG | 调试信息（开发环境） |

```java
// ✅ 正确
log.error("Payment failed", throwable);  // ERROR 带异常
log.warn("Retry payment, attempt={}", attempt);  // WARN
log.info("Order created, orderId={}", orderId);  // INFO
log.debug("Request body={}", body);  // DEBUG
```

### 5. 必备字段

```java
log.info("Order created",
    kv("orderId", order.getId()),
    kv("userId", order.getUserId()),
    kv("amount", order.getAmount()),
    kv("traceId", MDC.get("trace_id")));
```

## 框架配置

### Java（Logback）

```xml
<!-- logback-spring.xml -->
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
        <providers>
            <timestamp/>
            <logLevel/>
            <loggerName/>
            <message/>
            <mdc/>  <!-- trace_id / span_id -->
            <stackTrace/>
        </providers>
    </encoder>
</appender>
```

### Python（structlog）

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

log = structlog.get_logger()
log.info("order_created", order_id=order.id, user_id=user.id, amount=99.99)
```

### Node.js（pino）

```typescript
import pino from 'pino';

const log = pino();
log.info({ orderId: order.id, userId: user.id }, 'Order created');
// {"level":30,"time":1700000000000,"orderId":"...","userId":"...","msg":"Order created"}
```

## 反模式

- ❌ `log.info("message")` 不带结构化字段
- ❌ 字符串拼接（`"Order " + orderId + " created"`）
- ❌ 记密码 / 密钥
- ❌ 不带 trace_id
- ❌ 所有日志都是 INFO（淹没 ERROR）
- ❌ 生产环境开 DEBUG（性能 + 噪声）
