# HTTP 状态码

## 强制规则

### 成功（2xx）

| 状态码 | 语义 | 用法 |
|---|---|---|
| **200 OK** | 通用成功 | GET / PUT / PATCH / DELETE |
| **201 Created** | 创建成功 | POST 创建资源，返回新资源 |
| **202 Accepted** | 已接受处理 | 异步任务（返回任务 ID） |
| **204 No Content** | 无返回内容 | DELETE 成功 |

### 客户端错误（4xx）

| 状态码 | 语义 | 用法 |
|---|---|---|
| **400 Bad Request** | 请求格式错误 | JSON 解析失败、参数类型错 |
| **401 Unauthorized** | 未认证 | 没带 token / token 过期 |
| **403 Forbidden** | 已认证但无权限 | 角色不够 |
| **404 Not Found** | 资源不存在 | URL 错的资源 |
| **409 Conflict** | 资源冲突 | 重复创建 / 状态冲突 |
| **422 Unprocessable Entity** | 语义错误 | 参数校验失败（业务规则） |
| **429 Too Many Requests** | 限流 | 超过速率限制 |

### 服务端错误（5xx）

| 状态码 | 语义 | 用法 |
|---|---|---|
| **500 Internal Server Error** | 服务器内部错误 | 未捕获异常 |
| **502 Bad Gateway** | 上游错误 | 网关收到无效响应 |
| **503 Service Unavailable** | 服务不可用 | 维护 / 过载 |
| **504 Gateway Timeout** | 上游超时 | 网关超时 |

## 用法细节

### 400 vs 422

```
400 = 请求本身格式错误（无法解析）
422 = 请求格式正确但业务校验失败
```

```json
// 400: JSON 格式错
{"error": "Invalid JSON syntax at line 3"}

// 422: 字段校验失败
{
    "code": "VALIDATION_FAILED",
    "message": "请求参数校验失败",
    "details": [
        {"field": "email", "message": "邮箱格式不正确"},
        {"field": "age", "message": "年龄必须 ≥ 18"}
    ]
}
```

### 401 vs 403

```
401 = "你是谁？"（没带身份 / 身份过期）
403 = "我知道你是谁，但你不能做这事"
```

```json
// 401: 没带 token
{"code": "UNAUTHORIZED", "message": "请先登录"}

// 403: 没权限
{"code": "FORBIDDEN", "message": "无权访问该资源"}
```

### 409 Conflict 场景

```json
// 重复创建
{"code": "DUPLICATE", "message": "邮箱已注册"}

// 状态冲突
{"code": "INVALID_STATE", "message": "订单已支付，无法取消"}
```

## 状态码规范

### ❌ 错误做法

- 所有成功都返回 200
- 所有错误都返回 500
- 用 200 + body 里的 code 字段表达错误

```json
// ❌ 错误
HTTP 200
{
    "code": 400,
    "message": "参数错误"
}
```

### ✅ 正确做法

```json
// HTTP 422
{
    "code": "VALIDATION_FAILED",
    "message": "请求参数校验失败",
    "trace_id": "abc-123",
    "details": [...]
}
```

## 反模式

- ❌ 错误响应不设状态码（让前端猜）
- ❌ 全部返回 200 + code 字段
- ❌ 401 和 403 混用
- ❌ 5xx 表示业务错误（应该 4xx）
- ❌ 自定义状态码（`499` / `599` 等）
