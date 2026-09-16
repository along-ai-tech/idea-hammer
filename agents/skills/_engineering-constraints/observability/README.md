# observability/ — 可观测性

> 结构化日志 / 指标 / 链路追踪 / 健康检查。

## 文档

| 主题 | 文档 |
|---|---|
| 结构化日志 | [structured-logging.md](./structured-logging.md) |
| 指标 | [metrics.md](./metrics.md) |
| 链路追踪 | [tracing.md](./tracing.md) |
| 健康检查 | [health-check.md](./health-check.md) |

## 三大支柱

1. **Logs**：发生了什么（结构化 + trace_id）
2. **Metrics**：聚合数据（QPS / p95 / 错误率）
3. **Traces**：请求链路（OpenTelemetry）

## 健康检查

每个服务必须暴露 `/health`（存活性）和 `/ready`（就绪性）。
