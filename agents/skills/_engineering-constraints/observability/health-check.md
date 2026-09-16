# 健康检查

## 三种检查

### 1. Liveness（存活性）

**目的**：进程是否还活着（没死锁）

```yaml
GET /health/live
Response: 200 OK
{
    "status": "UP"
}
```

K8s 配置：
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
```

### 2. Readiness（就绪性）

**目的**：能不能接受流量（依赖是否就绪）

```yaml
GET /health/ready
Response: 200 OK
{
    "status": "UP",
    "checks": {
        "database": {"status": "UP", "latency_ms": 5},
        "redis": {"status": "UP", "latency_ms": 1},
        "external_api": {"status": "DOWN", "error": "timeout"}
    }
}
```

K8s 配置：
```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3
```

### 3. Startup（启动）

**目的**：慢启动服务（Kafka 消费者等）

```yaml
GET /health/startup
Response: 200 OK
```

K8s：
```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

## Spring Boot 实现

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```yaml
management:
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  health:
    db:
      enabled: true
    redis:
      enabled: true
```

## 自定义检查

```java
@Component
public class ExternalApiHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        try {
            ResponseEntity<String> resp = httpClient.get(
                "https://api.example.com/health", 
                String.class, 
                5_000);  // 5 秒超时
            
            if (resp.getStatusCode().is2xxSuccessful()) {
                return Health.up()
                    .withDetail("endpoint", "https://api.example.com")
                    .build();
            }
            return Health.down()
                .withDetail("status", resp.getStatusCode())
                .build();
        } catch (Exception e) {
            return Health.down(e).build();
        }
    }
}
```

## 检查项

| 检查 | 含义 | K8s |
|---|---|---|
| 数据库连接 | DB 可达 | readiness |
| Redis 连接 | Redis 可达 | readiness |
| 外部 API | 关键依赖 | readiness（可降级） |
| 磁盘空间 | > 10% | readiness |
| 内存 | < 80% | liveness |
| 消息队列 | 可连接 | readiness |

## 反模式

- ❌ `/health` 检查外部 API（每次调用慢 → 影响 readiness → pod 被踢）
- ❌ liveness 检查数据库（DB 抖动 → pod 被杀 → 雪崩）
- ❌ 没有区分 liveness / readiness
- ❌ 启动后立即就绪（数据库连接池还没建好）
- ❌ `/health` 返回 200 但服务实际挂了
