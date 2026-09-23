# 原则：向后兼容（Backward Compatibility）

> 新版上线，老代码 / 老客户端 / 老数据 还能继续跑。

## 4 维度兼容

| 维度 | 兼容 | 破坏 |
|---|---|---|
| **请求** | 加可选参数 | 删参数 / 改语义 |
| **响应** | 加字段（老忽略） | 删字段 / 改类型 / 改语义 |
| **状态码** | 加新状态码 | 复用老状态码返回新错误 |
| **行为** | （罕见） | 改业务规则 / 性能降级 |

## 数据兼容

- 加列（nullable / default）→ OK
- 删列 / 改列类型（不兼容方向）→ 失败
- 加 NOT NULL 约束（老数据可能不满足）→ 失败

## Expand-Contract（推荐模式）

```
Phase 1 (Expand): 加新列，老列保留，backfill
Phase 2 (Migrate): 写双写（新老列同时写），分批迁移
Phase 3 (Contract): 读切到新列
Phase 4 (独立发布): 删老列
```

详见 [data-migration.md](./data-migration.md)。

## Sunset 弃用

```http
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Deprecation: true
Link: <https://docs.api.com/v2-migration>; rel="deprecation"
```

弃用窗口：
- 内部 API: 1-2 周
- SaaS: 6-12 个月
- 移动客户端: 12+ 个月

## 反模式

```sql
-- 反：一次发布删字段 + 改语义
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users ADD COLUMN email_v2;
UPDATE users SET email_v2 = email;  -- 已经 DROP email，崩

-- 正：分 3 次发布（Expand / Switch / Contract）
```

详见 [api-versioning.md](./api-versioning.md) 的版本控制策略。
