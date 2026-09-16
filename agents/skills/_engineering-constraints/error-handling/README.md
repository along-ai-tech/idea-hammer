# error-handling/ — 错误处理规范

> 异常 vs 返回码 / stacktrace / 统一错误响应。

## 文档

| 主题 | 文档 |
|---|---|
| 异常 vs 返回码 | [exception-vs-returncode.md](./exception-vs-returncode.md) |
| 异常处理实践 | [exception-practices.md](./exception-practices.md) |
| 错误信息规范 | [error-messages.md](./error-messages.md) |

## 核心原则

1. **业务错误用异常**（不要用返回码）
2. **必须带 stacktrace**（不要 `e.printStackTrace()`）
3. **不要吞异常**（catch 后必须有动作）
4. **不暴露内部细节**（错误响应不带 SQL / 堆栈）
5. **统一错误响应格式**（见 api-design/error-response.md）
