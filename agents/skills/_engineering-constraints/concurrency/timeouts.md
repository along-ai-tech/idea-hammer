# 超时配置

> 所有网络 / IO 调用必须配超时。无限等待 = 雪崩起点。

## 强制规则

### 1. HTTP 超时

```java
// ✅ 正确：OkHttp
OkHttpClient client = new OkHttpClient.Builder()
    .connectTimeout(5, TimeUnit.SECONDS)    // 连接超时
    .readTimeout(30, TimeUnit.SECONDS)      // 读超时
    .writeTimeout(30, TimeUnit.SECONDS)     // 写超时
    .callTimeout(60, TimeUnit.SECONDS)      // 总超时
    .retryOnConnectionFailure(true)         // 自动重试连接
    .build();

// ✅ 正确：Spring RestTemplate
SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
factory.setConnectTimeout(5000);
factory.setReadTimeout(30000);
RestTemplate restTemplate = new RestTemplate(factory);

// ✅ 正确：Spring WebClient（响应式）
WebClient client = WebClient.builder()
    .clientConnector(new ReactorClientHttpConnector(
        HttpClient.create()
            .responseTimeout(Duration.ofSeconds(30))
            .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)))
    .build();
```

```python
# ✅ 正确：httpx
httpx.get(url, timeout=10.0)  # 总超时
httpx.get(url, timeout=(5.0, 30.0))  # (连接, 读)

# ✅ 正确：requests
requests.get(url, timeout=(5, 30))
```

```typescript
// ✅ 正确：fetch + AbortSignal
const resp = await fetch(url, {
    signal: AbortSignal.timeout(10_000),
});

// ✅ 正确：axios
axios.get(url, { timeout: 10_000 });
```

### 2. 数据库超时

```yaml
spring:
  datasource:
    hikari:
      connection-timeout: 30000     # 连接超时（默认 30 秒）
      validation-timeout: 5000      # 验证超时
      max-lifetime: 1800000         # 连接最长存活 30 分钟
```

```java
// ✅ SQL 查询超时（JDBC）
Statement stmt = conn.createStatement();
stmt.setQueryTimeout(30);  // 30 秒
ResultSet rs = stmt.executeQuery(sql);
```

### 3. Redis 超时

```java
Config config = new Config();
config.useSingleServer()
    .setAddress("redis://localhost:6379")
    .setTimeout(3000)               // 命令超时 3 秒
    .setConnectTimeout(5000)         // 连接超时 5 秒
    .setRetryAttempts(2);           // 重试 2 次
```

### 4. RPC 超时（gRPC / Dubbo）

```java
// gRPC
ManagedChannel channel = ManagedChannelBuilder.forAddress("host", 50051)
    .keepAliveTime(30, TimeUnit.SECONDS)
    .keepAliveTimeout(5, TimeUnit.SECONDS)
    .build();

// Stub
OrderServiceGrpc.OrderServiceBlockingStub stub = OrderServiceGrpc.newBlockingStub(channel)
    .withDeadlineAfter(5, TimeUnit.SECONDS);  // 每次调用超时
```

### 5. 异步任务超时

```java
CompletableFuture<Order> future = CompletableFuture.supplyAsync(() -> 
    orderService.create());

try {
    Order order = future.get(30, TimeUnit.SECONDS);  // 30 秒超时
} catch (TimeoutException e) {
    future.cancel(true);
    throw new BusinessException("处理超时");
}
```

## 超时时间经验值

| 场景 | 连接超时 | 读超时 | 总超时 |
|---|---|---|---|
| 内部 API（同机房） | 1s | 3s | 5s |
| 外部 API（HTTP） | 5s | 30s | 60s |
| 数据库查询 | 5s | 30s | 60s |
| Redis 操作 | 1s | 3s | 5s |
| 长任务（导出 / 报表） | - | - | 600s |

## 反模式

- ❌ 无超时（默认可能 0 = 无限）
- ❌ 所有调用同一个超时（不分场景）
- ❌ 超时不重试（瞬时失败放大）
- ❌ 重试不带指数退避（打挂下游）
- ❌ 超时但忘了释放资源
