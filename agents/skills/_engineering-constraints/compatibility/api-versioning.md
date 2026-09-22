# 原则：API 版本控制

> API 改了，老客户端不报错。版本控制 + 弃用策略保兼容。

## 3 种版本控制方式

### 1. URL 版本（最常见）

```
GET /api/v1/users/123
GET /api/v2/users/123

优点：直观 / 路由层可见 / 易灰度
缺点：URL 长 / 老版本维护成本
```

### 2. Header 版本

```
GET /api/users/123
Accept: application/vnd.myapi.v2+json
或
X-API-Version: 2

优点：URL 干净
缺点：不直观 / 难发现 / 难调试
```

### 3. 无版本（破坏式）

```
GET /api/users/123

优点：简单
缺点：老客户端必挂

用法：内部 API / 一次性项目 / SaaS 客户端控制
```

## 选型

| 场景 | 推荐 |
|---|---|
| 公开 API（多客户端） | URL 版本 + 弃用策略 |
| 内部 API（团队内） | Header 版本 |
| 单一客户端 | 无版本（敢破坏就破坏） |
| SaaS | URL 版本（客户看不到迁移成本） |

## 弃用策略

### 3 阶段弃用

```
# Stage 1: 标记 deprecated（响应 header）
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Deprecation: true
Link: <https://docs.api.com/v2-migration>; rel="deprecation"

# Stage 2: 邮件通知客户 + 文档标注
# Stage 3: 弃用日 = 关闭老版本
```

### 时间窗口

| API 客户规模 | 弃用窗口 |
|---|---|
| 内部 | 1-2 周 |
| 付费 SaaS 小客户 | 3 个月 |
| 付费 SaaS 大客户 | 6-12 个月 |
| 移动客户端（需要发版） | 12+ 个月 |

### 通知

- API 文档 changelog
- email 客户
- 响应 header（Sunset / Deprecation）
- 控制台 banner
- SDK warning（升级提示）

## 兼容性矩阵

明确每个版本支持多久：

```
v1: 2024-01-01 ~ 2026-12-31（弃用）
v2: 2025-06-01 ~ 当前（主推）
v3: 2026-Q3 计划

v2 是主推版本，v1 进入弃用期，2026 年底关闭。
```

## 响应兼容

新版本返回老字段 + 新字段，老客户端忽略新字段：

```json
{
  "id": 123,
  "name": "iPhone 16",           // 老字段
  "display_name": "iPhone 16",   // 新字段
  "version": 2,                    // 新字段
  "created_at": "2026-09-01"
}

老客户端：读 name（兼容）
新客户端：读 display_name + version（推荐）
```

## 检测

- swagger-diff / openapi-diff：API 变更自动检测
- code-review: 改 API 必查兼容性
- Deprecation header：定期扫描老 endpoint

## 反模式

```python
# 反模式：无版本控制 + 删字段
GET /api/users/123
返回:
    {"id": 123, "full_name": "..."}   # 老字段 name 删了，老客户端崩


# 正确：URL 版本 + 弃用 header
GET /api/v1/users/123
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
返回:
    {"id": 123, "name": "..."}       # v1 保留老字段

GET /api/v2/users/123
返回:
    {"id": 123, "full_name": "..."}   # v2 用新字段
```
