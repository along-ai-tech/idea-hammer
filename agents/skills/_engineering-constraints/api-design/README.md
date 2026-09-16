# api-design/ — API 设计规范

> REST / 状态码 / 分页 / 错误响应 / OpenAPI。

## 文档

| 主题 | 文档 |
|---|---|
| REST 资源命名 | [rest-conventions.md](./rest-conventions.md) |
| HTTP 状态码 | [http-status-codes.md](./http-status-codes.md) |
| 分页 | [pagination.md](./pagination.md) |
| 统一错误响应 | [error-response.md](./error-response.md) |
| OpenAPI 强制 | [openapi-required.md](./openapi-required.md) |

## 核心原则

1. **RESTful 但不教条**（业务优先）
2. **状态码准确**（200/201/204/400/401/403/404/409/422/500）
3. **分页用 cursor**（不用 offset）
4. **错误响应统一格式**（{code, message, trace_id, details}）
5. **OpenAPI 文档必须生成**（前后端协作）
