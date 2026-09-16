# 分页规范

## 选型

| 场景 | 推荐 | 禁止 |
|---|---|---|
| 列表分页（无限滚动） | **cursor 分页** | ❌ offset 深分页 |
| 跳页（页码 1/2/4） | **page + size**（带总数） | ❌ 深 offset |
| 导出全量 | **异步任务**（不带分页参数） | ❌ LIMIT 1000000 |

## Cursor 分页（推荐）

```http
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ==

Response:
{
    "data": [...],
    "next_cursor": "eyJpZCI6MTQzfQ==",
    "has_more": true
}
```

```sql
-- 第一次请求
SELECT * FROM users
WHERE id > 0  -- 初始游标
ORDER BY id
LIMIT 20;

-- 后续请求（cursor = 上一批的最后一个 id）
SELECT * FROM users
WHERE id > ?  -- cursor 解码后的 id
ORDER BY id
LIMIT 20;
```

**优势**：
- 性能稳定（不扫 OFFSET 行）
- 新数据插入不影响（offset 分页会跳数据）
- 适合无限滚动

## Page + Size（适合跳页）

```http
GET /users?page=1&size=20

Response:
{
    "data": [...],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 1234,
        "total_pages": 62
    }
}
```

**限制**：
- 必须带 `total` 限制（`total_pages ≤ 500` 或类似）
- 深页警告（`page > 100` 返回警告）
- 默认 `size ≤ 100`

## 排序

```http
GET /users?sort=created_at:desc,name:asc
```

- 多字段用逗号分隔
- 字段:asc / 字段:desc
- 默认值：`created_at:desc`（最新优先）

## 过滤

```http
GET /users?status=active&role=admin&created_after=2026-01-01
```

- 字段名 + 值
- 多个字段 AND 关系
- 范围：`created_after` / `created_before`
- 数组：`role=admin,user`（IN 查询）

## 反模式

- ❌ `LIMIT 1000000, 20`（深分页）
- ❌ `OFFSET` 配合插入频繁的表（跳数据）
- ❌ 不带 limit 的查询
- ❌ `total` 不限制（`SELECT COUNT(*)` 扫全表）
- ❌ 客户端算分页（`page = (offset / size) + 1`）
