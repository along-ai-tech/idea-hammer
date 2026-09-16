# 统一错误响应

## 格式

```json
{
    "code": "VALIDATION_FAILED",
    "message": "请求参数校验失败",
    "trace_id": "abc-123-def-456",
    "details": [
        {
            "field": "email",
            "message": "邮箱格式不正确"
        }
    ],
    "timestamp": "2026-09-16T17:00:00Z"
}
```

## 字段规范

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `code` | string | ✅ | 业务错误码（4 位 + 模块） |
| `message` | string | ✅ | 用户可读消息 |
| `trace_id` | string | ✅ | 用于排查日志 |
| `details` | object[] | ❌ | 字段级错误（校验失败） |
| `timestamp` | string | ❌ | ISO 8601 |

## 业务错误码规范

```
格式：<MODULE>_<NUMBER>
例：USER_001 / ORDER_002 / AUTH_003
```

| 模块 | 范围 | 例 |
|---|---|---|
| 通用 | 0 | `INVALID_PARAM` / `UNAUTHORIZED` / `FORBIDDEN` |
| USER | 1xxx | `USER_NOT_FOUND` / `USER_DUPLICATE` |
| AUTH | 2xxx | `AUTH_INVALID_TOKEN` / `AUTH_EXPIRED` |
| ORDER | 3xxx | `ORDER_NOT_FOUND` / `ORDER_INVALID_STATE` |
| PAY | 4xxx | `PAY_FAILED` / `PAY_INSUFFICIENT` |

## 实现

```java
// ✅ Spring Boot 全局异常处理
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(ValidationException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code("VALIDATION_FAILED")
            .message("请求参数校验失败")
            .traceId(MDC.get("trace_id"))
            .details(e.getErrors())
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.status(422).body(error);
    }
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(BusinessException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code(e.getCode())
            .message(e.getMessage())
            .traceId(MDC.get("trace_id"))
            .timestamp(Instant.now())
            .build();
        return ResponseEntity.status(e.getHttpStatus()).body(error);
    }
}

// 业务异常
public class BusinessException extends RuntimeException {
    private final String code;
    private final HttpStatus httpStatus;
    
    public BusinessException(String code, String message, HttpStatus status) {
        super(message);
        this.code = code;
        this.httpStatus = status;
    }
}
```

## 反模式

- ❌ 错误响应不带 `trace_id`（无法排查）
- ❌ 错误码用 HTTP 状态码（200 / 500 表示错误码）
- ❌ 错误 message 暴露内部细节（堆栈 / SQL）
- ❌ 错误响应不带 `code`（前端无法编程处理）
- ❌ 中文 message（前后端协作不便）
- ❌ 错误 message 用感叹号 / Emoji（不专业）
