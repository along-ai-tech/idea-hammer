# 原则：向后兼容（Backward Compatibility）

> 新代码上线，老代码 / 老客户端 / 老数据 还能继续跑。

## 兼容 vs 破坏

| 类型 | 行为 | 用法 |
|---|---|---|
| 向后兼容 | 新版能理解老输入 / 老输出 | 默认 |
| 破坏性变更 | 老代码 / 老客户端 / 老数据报错 | 必须主动标注 + 版本控制 |

## API 兼容 4 维度

### 请求兼容：老请求带新版本 server

- 新增可选参数 → 老请求仍 work
- 删参数 → 报错
- 改参数语义 → 老请求行为变（破坏）

### 响应兼容：新版 server 返回老格式

- 新增字段 → 老客户端忽略多余字段（work）
- 删字段 → 老客户端拿 undefined（破坏）
- 改字段类型（如 string → int）→ 老客户端解析失败（破坏）
- 改字段语义（如 status: 0 含义变了）→ 老客户端行为错（破坏）

### 状态码兼容

- 新增状态码 → 老客户端不认识（一般 work，新客户端才用）
- 复用老状态码返回新错误 → 老客户端误处理（破坏）
- 改老状态码语义 → 老客户端行为错（破坏）

### 行为兼容

- 改业务规则 → 老客户端调用结果变
- 改性能（响应变慢 / 变大）→ 老用户体验降级

## 数据兼容 3 类

### Schema 兼容

- 加列（nullable / 有 default）→ 老数据 OK
- 改列类型（兼容方向，如 int → bigint）→ 大部分 OK
- 改列类型（不兼容方向，如 string → int）→ 老数据失败
- 删列 → 老查询报错
- 加约束（NOT NULL / UNIQUE）→ 老数据可能不满足 → 失败

### 字段语义兼容

- 改 enum 值（如 status: 0 原本是待支付改已下单）→ 老数据语义错
- 改时间戳单位（秒 → 毫秒）→ 老数据解读错
- 改数值精度（保留 2 位小数 → 4 位）→ 老数据精度丢失

### 关联兼容

- 删外键约束 → 老数据孤儿
- 改主键格式 → 关联表找不到
- 改关联表名 / 字段 → JOIN 失败

## 用户兼容 3 类

### 状态兼容

- 老用户的草稿 / 收藏用了改之前的字段 → 数据丢失
- 老用户的工作流卡在中间状态 → 新流程不认
- 老用户的订阅 / 积分 / 等级用旧规则 → 升级后规则失效

### UI 兼容

- 路由改了 → 老用户 deeplink 失效
- 组件 props 改了 → 老版本 React 报错
- CSS class 名变了 → 老主题 / 老样式失效
- i18n key 改了 → 老语言翻译缺失

### 数据兼容

- localStorage / IndexedDB 格式变了 → 老用户登录态丢失
- Service Worker 缓存失效 → 老用户拿老版本 → 错
- 第三方 cookie 被禁用 → 老用户登录态丢失

## 依赖兼容 2 类

### 内部依赖

- 改函数签名 → 上游调用方全断
- 改返回值结构 → 上游解析失败
- 删 / 改名 export → import 报错

### 外部依赖

- 第三方 SDK breaking change（升级前查 changelog）
- 数据库版本升级（数据类型 / 函数变化）
- 浏览器 / OS 弃用某些 API

## 兼容模式 3 种

### Expand-Contract（推荐）

```
# Phase 1: Expand（加新字段，老字段保留）
ALTER TABLE users ADD COLUMN email_v2 VARCHAR(255);
BACKFILL email_v2 FROM email;

# Phase 2: Migrate（写入时同步新字段）
INSERT/UPDATE 同时写 email 和 email_v2

# Phase 3: Switch（读切到新字段）
SELECT email_v2 AS email FROM users;

# Phase 4: Contract（删老字段）
ALTER TABLE users DROP COLUMN email;
```

### Coexist（双写双读）

新老字段同时存在，读取时挑新的，fallback 老。

### Sunset（弃用）

1. 标 deprecated（响应 warning header）
2. 给迁移窗口期（如 6 个月）
3. 发公告 / 通知老用户
4. 窗口期后删除

## 检测

- code-review Stage 2: 改 API / schema / 业务逻辑必查
- API diff 工具：swagger-diff / openapi-diff
- DB migration 工具：Flyway / Liquibase（区分 backward-compatible migration）

## 反模式

```sql
-- 反模式：删字段 + 改语义同一次发布
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users ADD COLUMN email_v2;
UPDATE users SET email_v2 = email;  -- 已经 DROP 了 email，崩了


-- 正确：分 3 次发布
-- 发布 1: Expand（加新列，双写双读）
-- 发布 2: Switch（读切到新列）
-- 发布 3: Contract（删老列）
```
