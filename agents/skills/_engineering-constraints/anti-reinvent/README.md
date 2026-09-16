# anti-reinvent/ — 禁止造轮子红线

> AI 写代码最常见错误：生态里已有成熟方案，自己重写一个。

## 红线（绝对禁止）

| 主题 | 文档 |
|---|---|
| 连接池 | [no-connection-pool.md](./no-connection-pool.md) |
| 日期工具 | [no-date-util.md](./no-date-util.md) |
| 集合工具 | [no-collection-util.md](./no-collection-util.md) |
| HTTP 客户端 | [no-http-client.md](./no-http-client.md) |
| JSON 解析 | [no-json-parser.md](./no-json-parser.md) |
| 线程池 | [no-thread-pool-default.md](./no-thread-pool-default.md) |
| 分布式锁 | [no-distributed-lock.md](./no-distributed-lock.md) |
| 分布式 ID | [no-distributed-id.md](./no-distributed-id.md) |
| 缓存抽象 | [no-cache-abstraction.md](./no-cache-abstraction.md) |
| 配置中心 | [no-config-center.md](./no-config-center.md) |

## 检测方式

code-review Stage 2 必查：
- 关键词 `setnx` / `dateutil` / `simplelist` / `httputil` / `new ObjectMapper` 自定义继承
- grep `extends ThreadPoolExecutor` 自定义
- 看 `pom.xml` / `requirements.txt` / `package.json` 有无成熟生态库（如 hutool / commons-lang3）

## 决策树

```
要造一个工具类 X？
├── 生态有 Hutool / Apache Commons / Guava 等覆盖 → 用现成的
├── 框架自带（如 Spring 的 StringUtils） → 用框架自带的
├── 生态有但项目没引入 → 先引入，再决定（不要单独造）
└── 真的生态没有（罕见）→ 写，但要：
    - 单测覆盖率 ≥ 95%
    - 文档说明为什么自造 + 引用现有方案的不够之处
```
