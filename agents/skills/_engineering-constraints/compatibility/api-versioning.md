# 原则：API 版本控制

> API 改了，老客户端不报错。

## 3 种版本方式

| 方式 | 例子 | 用法 |
|---|---|---|
| **URL** | `/api/v1/users` | 公开 API（最常见） |
| **Header** | `Accept: ...vnd.api.v2+json` | 内部 API |
| **无版本** | `/api/users` | 单一客户端，敢破坏就破坏 |

推荐：**URL 版本 + 弃用策略**（公开 API）。

## 弃用策略

```http
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Deprecation: true
Link: <https://docs.api.com/v2-migration>; rel="deprecation"
```

## 弃用窗口

| 客户规模 | 窗口 |
|---|---|
| 内部 | 1-2 周 |
| SaaS 小客户 | 3 个月 |
| SaaS 大客户 | 6-12 个月 |
| 移动客户端 | 12+ 个月 |

## 响应兼容

新版本返回老字段 + 新字段，老客户端忽略新字段：

```json
{
  "id": 123,
  "name": "iPhone 16",        // 老字段
  "display_name": "iPhone 16"  // 新字段（老客户端忽略）
}
```

详见 [backward-compatibility.md](./backward-compatibility.md) 的 Expand-Contract。
