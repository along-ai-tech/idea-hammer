# 原则：工程级约束（强制遵循）

> AI 写代码前必须读 `_engineering-constraints/`。Code-review Stage 2 必须对照检查。

## 为什么独立

主原则只能塞泛原则（"复用优先"、"SDK-First"），落地时缺：
- 不知道该用 Redisson 还是 Jedis
- 不知道该遵循阿里 Java 手册还是 Google Java Style
- 不知道"禁止自造连接池"的红线
- 不知道 N+1 查询算反模式
- 不知道 JWT 该怎么用、bcrypt 该用哪个变种

`_engineering-constraints/` 13 个主题装这些具体约束。

## 强制读

启动 dev-builder 后、写代码前，按语言必读：

```
语言确认（DEV-PLAN.md 技术栈表）
├── Java → coding-style/java-alibaba.md + ecosystem-matrix/java-ecosystem.md + ecosystem-matrix/redis-clients.md
├── Python → coding-style/python-pep8.md + ecosystem-matrix/python-ecosystem.md
├── TypeScript → coding-style/typescript-airbnb.md + ecosystem-matrix/frontend-ecosystem.md
├── Go → coding-style/go-effective.md
└── SQL → coding-style/sql-conventions.md + database/indexing.md
```

## 强制遵循红线

`anti-reinvent/` 10 条红线：禁止造连接池、禁止造日期工具、禁止造集合工具、禁止造 HTTP 客户端、禁止造 JSON 解析器、禁止默认线程池、禁止手写分布式锁、禁止自造分布式 ID、禁止自造缓存抽象、禁止自造配置中心。

**任何"造一个新工具类"的冲动 → 先查 anti-reinvent/ 和 ecosystem-matrix/，确认生态没有再用。**

## 主题清单（13）

| 主题 | 解决什么 |
|---|---|
| **coding-style/** | 语言特定规范（阿里 / Pep8 / Airbnb / Effective Go） |
| **ecosystem-matrix/** | 库选择指南（Redisson / Hutool / Jackson 等） |
| **anti-reinvent/** | 禁止造轮子红线（10 条） |
| **performance/** | N+1 / 慢查询 / 缓存 / benchmark-first |
| **security/** | OWASP / 认证 / 哈希 / 密钥 / 漏洞扫描 / license |
| **concurrency/** | 线程池 / 分布式锁 / 幂等 / 超时 |
| **api-design/** | REST / 状态码 / 分页 / 错误响应 / OpenAPI |
| **observability/** | 结构化日志 / 指标 / 链路 / 健康检查 |
| **ci-cd/** | 必备检查 / migration / 回滚 |
| **error-handling/** | 异常规范 / 错误响应 |
| **database/** | 索引 / 事务 / 连接池 |
| **dependency-mgmt/** | lockfile / 漏洞 / 升级 / 重复依赖 |
| **i18n-a11y/** | 国际化 / 时区 / 可访问性 |

## 接入流程

dev-builder 每个 Task 启动：

1. 读对应语言规范
2. 查对应库选择矩阵
3. 写代码时遵守红线
4. code-review Stage 2 对照检查

## 与现有原则关系

- **SDK-First**（已有）→ 落地到 `ecosystem-matrix/`
- **复用优先**（已有）→ 落地到 `anti-reinvent/`
- **测试纪律**（已有）→ 与 `_engineering-constraints/` 并行不冲突
- **范围纪律**（已有）→ 配合 `error-handling/` 的统一异常规范
