# 时区处理

## 核心原则

- **存储**：UTC（数据库 + 服务端）
- **传输**：ISO 8601（带时区或 Z）
- **显示**：用户本地时区（前端转换）

## 存储

```sql
-- ✅ 正确：UTC
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW()  -- 带时区
);

-- PostgreSQL 用 TIMESTAMPTZ（不是 TIMESTAMP）
-- MySQL 用 TIMESTAMP（自动转换时区） 或 DATETIME（不转换）
```

```python
# ✅ 正确：UTC
from datetime import datetime, timezone

created_at = datetime.now(timezone.utc)  # 2026-09-16 17:00:00+00:00
db.insert(created_at=created_at)
```

```java
// ✅ 正确：Instant（UTC）
Instant now = Instant.now();
order.setCreatedAt(now);
```

## 反模式：存储本地时区

```sql
-- ❌ 错误：DATETIME（不转换时区）
created_at DATETIME  -- 不知道是哪里的时区

-- ❌ 错误：VARCHAR 存时间字符串
created_at VARCHAR(20)  -- "2026-09-16 17:00:00" 不知道时区
```

## 传输

```json
{
    "createdAt": "2026-09-16T17:00:00Z"  // ✅ UTC ISO 8601
}

{
    "createdAt": "2026-09-16T17:00:00+00:00"  // ✅ 显式 UTC
}

{
    "createdAt": "2026-09-16T17:00:00"  // ❌ 无时区
}

{
    "createdAt": "2026-09-16 17:00:00"  // ❌ 格式错（不是 ISO 8601）
}
```

## 显示

```typescript
// 前端转换到本地时区
const date = new Date(order.createdAt);  // 自动解析
const local = date.toLocaleString('zh-CN', { 
    timeZone: 'Asia/Shanghai',
    dateStyle: 'medium',
    timeStyle: 'short',
});
// "2026年9月16日 17:00:00"
```

```python
# Python：转换到用户时区
import pendulum

utc_dt = pendulum.parse(order.created_at)  # UTC
user_tz = pendulum.timezone("Asia/Shanghai")
local_dt = utc_dt.in_timezone(user_tz)
local_dt.format("YYYY-MM-DD HH:mm:ss")
```

## JavaScript Date 陷阱

```typescript
// ❌ 错误：构造时按本地时区
new Date(2026, 8, 16, 17, 0, 0);  // 本地时区

// ✅ 正确：ISO 8601
new Date("2026-09-16T17:00:00Z");  // UTC
```

## Cron / 定时任务

```bash
# crontab 用本地时区（默认）
# 服务器在 UTC → 表达式按 UTC 写
0 17 * * *  # 每天 UTC 17:00

# 或显式指定时区
CRON_TZ=Asia/Shanghai
0 17 * * *  # 每天北京时间 17:00
```

## 反模式

- ❌ 数据库存本地时区
- ❌ JSON 传输不带时区
- ❌ 前端 hardcode UTC 显示
- ❌ 用 `Date.parse()` 解析非 ISO 字符串
- ❌ 跨时区计算没转 UTC
- ❌ 夏令时混乱（美国 / 欧盟不同时区切换）
