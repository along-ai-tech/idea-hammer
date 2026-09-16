# 工程级约束（Engineering Constraints）

> IdeaHammer 的工程级硬约束，跨 skill 共享。让 AI 写出"工业级"代码，不造轮子、不写四不像。

## 为什么独立成域

主 skill（dev-builder / code-review 等）只能塞泛原则（"复用优先"、"SDK-First"），落地时缺：
- 不知道该用 Redisson 还是 Jedis
- 不知道该遵循阿里 Java 手册还是 Google Java Style
- 不知道"禁止自造连接池"的红线
- 不知道 N+1 查询算反模式
- 不知道 JWT 该怎么用、bcrypt 该用哪个变种

这个目录用 13 个主题装这些具体约束，dev-builder / code-review / bug-fixer 按需引用。

## 主题地图

| 主题 | 解决什么 | 用户原始痛点 |
|---|---|---|
| **coding-style/** | 语言特定的强制规范 | 阿里/Pep8/Airbnb 等 |
| **ecosystem-matrix/** | "X 场景该用哪个库"决策 | Redisson / Hutool 等 |
| **anti-reinvent/** | 禁止造轮子的红线 | "老是造轮子" |
| **performance/** | N+1 / 缓存 / benchmark | |
| **security/** | OWASP / 认证 / 哈希 / 密钥 | |
| **concurrency/** | 线程池 / 分布式锁 / 幂等 | |
| **api-design/** | REST / 状态码 / 分页 / OpenAPI | |
| **observability/** | 结构化日志 / 指标 / 链路 | |
| **ci-cd/** | 必需检查 / migration / 回滚 | |
| **error-handling/** | 异常规范 / 统一错误响应 | |
| **database/** | 索引 / 事务 / 慢查询 | |
| **dependency-mgmt/** | lockfile / 漏洞 / license | |
| **i18n-a11y/** | 国际化 / 可访问性 | |

## 引用方式

主 skill 在 principles/ 或 SKILL.md 里加：

```markdown
[工程级约束]
    启动前必读：_engineering-constraints/anti-reinvent/no-connection-pool.md
    改代码前对照：_engineering-constraints/coding-style/<lang>.md
    选择库时查：_engineering-constraints/ecosystem-matrix/<lang>-ecosystem.md
```

code-review Stage 2 增加检查项：

```markdown
[Stage 2 检查项]
    - 工程级约束符合度：对照 _engineering-constraints/anti-reinvent/ 检查是否造轮子
```

## 不算 skill

本目录以 `_` 开头，被 `check_skill_structure.py` 排除（不参与 skill 校验）。
它是跨 skill 共享的"约束数据库"，不是可独立调用的 skill。

## 怎么扩展

新主题直接建子目录 + README.md + 文档。不需要修改现有 skill 结构，只在 SKILL.md 加引用。

## 维护规则

- 新增约束先放 anti-reinvent/ 或 ecosystem-matrix/，被多个 skill 引用后再升级
- 约束必须有具体禁止项或强制项，禁止泛泛"应该注意 X"
- 每条约束写明"为什么" + "怎么做" + "反模式"
