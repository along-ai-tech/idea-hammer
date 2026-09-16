# 异常处理实践

## 强制规则

### 1. 必带 stacktrace

```java
// ❌ 错误：丢上下文
log.error("Order creation failed: " + e.getMessage());
throw new ServiceException("Order creation failed");

// ✅ 正确：保留 stacktrace
log.error("Order creation failed", e);  // 自动带 stacktrace
throw new ServiceException("Order creation failed", e);  // cause chain

// ✅ 更好：用 MDC 关联
try {
    orderService.create(dto);
} catch (Exception e) {
    log.error("Order creation failed, orderId={}", orderId, e);
    throw e;
}
```

### 2. 不要把异常信息返给前端

```java
// ❌ 错误：泄露内部
@ExceptionHandler(Exception.class)
public ResponseEntity<?> handle(Exception e) {
    return ResponseEntity.status(500).body(Map.of(
        "error", e.getMessage(),
        "stackTrace", ExceptionUtils.getStackTrace(e)  // 暴露堆栈
    ));
}

// ✅ 正确：内部详细，对外精简
@ExceptionHandler(Exception.class)
public ResponseEntity<ErrorResponse> handle(Exception e) {
    log.error("Internal error, traceId={}", MDC.get("trace_id"), e);
    
    ErrorResponse error = ErrorResponse.builder()
        .code("INTERNAL_ERROR")
        .message("服务器内部错误")  // 不暴露 e.getMessage()
        .traceId(MDC.get("trace_id"))
        .timestamp(Instant.now())
        .build();
    
    return ResponseEntity.status(500).body(error);
}
```

### 3. 自定义异常继承规范

```java
// 业务异常基类
@Getter
public class BusinessException extends RuntimeException {
    private final String code;
    private final HttpStatus httpStatus;
    
    public BusinessException(String code, String message, HttpStatus status) {
        super(message);
        this.code = code;
        this.httpStatus = status;
    }
    
    public BusinessException(String code, String message, HttpStatus status, Throwable cause) {
        super(message, cause);
        this.code = code;
        this.httpStatus = status;
    }
}

// 业务异常链
public class OrderNotFoundException extends BusinessException {
    public OrderNotFoundException(Long orderId) {
        super("ORDER_NOT_FOUND", "订单不存在: " + orderId, HttpStatus.NOT_FOUND);
    }
}

public class InvalidOrderStateException extends BusinessException {
    public InvalidOrderStateException(Long orderId, String currentState) {
        super("INVALID_ORDER_STATE",
              "订单状态无效: orderId=" + orderId + ", state=" + currentState,
              HttpStatus.CONFLICT);
    }
}
```

### 4. try-with-resources

```java
// ❌ 错误：手动 close（异常路径可能泄漏）
InputStream is = null;
try {
    is = new FileInputStream(file);
    // 处理
} finally {
    if (is != null) {
        is.close();  // 异常路径下可能没关
    }
}

// ✅ 正确：try-with-resources
try (InputStream is = new FileInputStream(file);
     BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {
    // 处理
    // 自动关闭（包括异常路径）
}
```

### 5. 不要在 finally 里抛异常

```java
// ❌ 错误：finally 抛异常覆盖原异常
try {
    return process();
} finally {
    cleanup();  // 如果 cleanup 抛异常，原异常丢失
}

// ✅ 正确
try {
    return process();
} finally {
    try {
        cleanup();
    } catch (Exception e) {
        log.warn("Cleanup failed", e);
        // 不要抛出
    }
}
```

### 6. 用 Thread.setDefaultUncaughtExceptionHandler

```java
// 全局兜底
Thread.setDefaultUncaughtExceptionHandler((thread, exception) -> {
    log.error("Uncaught exception in thread {}", thread.getName(), exception);
});
```

## Spring Boot 全局异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(BusinessException e) {
        return ResponseEntity.status(e.getHttpStatus())
            .body(ErrorResponse.builder()
                .code(e.getCode())
                .message(e.getMessage())
                .traceId(MDC.get("trace_id"))
                .build());
    }
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(ValidationException e) {
        return ResponseEntity.status(422)
            .body(ErrorResponse.builder()
                .code("VALIDATION_FAILED")
                .message("请求参数校验失败")
                .details(e.getBindingResult().getFieldErrors().stream()
                    .map(err -> Map.of(
                        "field", err.getField(),
                        "message", err.getDefaultMessage()))
                    .toList())
                .build());
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleAll(Exception e) {
        log.error("Unhandled exception", e);
        return ResponseEntity.status(500)
            .body(ErrorResponse.builder()
                .code("INTERNAL_ERROR")
                .message("服务器内部错误")
                .traceId(MDC.get("trace_id"))
                .build());
    }
}
```

## 反模式

- ❌ `e.printStackTrace()`（用 logger）
- ❌ `catch (Exception e) {}`（吞异常）
- ❌ 把异常消息返给前端
- ❌ 不带 stacktrace 的 log（`log.error("failed: " + e.getMessage())`）
- ❌ finally 抛异常
- ❌ 业务异常继承 Exception（应该 RuntimeException）
- ❌ 自定义异常不带 cause（丢上下文）
