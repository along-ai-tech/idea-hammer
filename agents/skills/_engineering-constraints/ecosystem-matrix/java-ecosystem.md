# Java 生态矩阵

> Java 后端常用场景的库选择决策。

## 工具库 / 工具集

| 场景 | 首选 | 次选 | 禁止 |
|---|---|---|---|
| 工具集（Collection/Date/Codec/Crypto/IO） | **Hutool** | Apache Commons Lang / Guava | ❌ 自造 DateUtil / CollectionUtil |
| 集合增强 | **Guava** Collections | Eclipse Collections | ❌ 重复造 immutable / Multimap |
| 字符串 | **Hutool** StrUtil | Apache Commons Lang | ❌ 手写判空 / 拼接 |
| 日期时间 | **java.time** (JDK 8+) | Joda-Time（老项目） | ❌ `Date` / `Calendar` / `SimpleDateFormat` |
| JSON | **Jackson** | Fastjson2 / Gson | ❌ Fastjson 1.x（有安全漏洞） |
| HTTP 客户端 | **OkHttp** | Apache HttpClient 5 | ❌ 自造 / `HttpURLConnection` |
| 校验 | **Jakarta Validation**（Hibernate Validator） | - | ❌ 手写 if 判断 |
| 日志 | **SLF4J + Logback** | Log4j2 | ❌ `System.out` / `e.printStackTrace()` |
| 测试 | **JUnit 5 + Mockito** | TestNG | ❌ JUnit 4 / 手写断言 |
| 断言（增强） | **AssertJ** | Hamcrest | ❌ `assertTrue(a == b)` |
| Mock | **Mockito** | PowerMock（避免） | ❌ 自造 mock 框架 |
| Bean 映射 | **MapStruct** | Spring BeanUtils（性能差） | ❌ 反射手写 copy |
| 缓存抽象 | **Spring Cache + Caffeine** | JCache | ❌ 自造 cache 单例 |
| 分布式锁 | **Redisson** | Curator (ZK) | ❌ `SETNX` + 过期时间手写 |
| 分布式 ID | **Snowflake**（美团 Leaf / 百度 UID） | UUID | ❌ `System.currentTimeMillis()` |
| 配置中心 | **Nacos** | Apollo / Consul | ❌ 数据库存配置 |
| 限流 | **Sentinel** | Resilience4j | ❌ 手写令牌桶 |
| 分布式事务 | **Seata** | 消息队列最终一致 | ❌ 同步 RPC 链式事务 |
| API 文档 | **SpringDoc OpenAPI** | Swagger 2 | ❌ 手写接口文档 |
| 监控 | **Micrometer + Prometheus** | - | ❌ 自造 metrics |
| 链路追踪 | **OpenTelemetry** | Sleuth（已弃用） | ❌ log4j MDC 手写 trace_id |
| 加密 | **Hutool Crypto** / Bouncy Castle | - | ❌ 自造加密算法 |
| 配置读取 | **Spring Boot @ConfigurationProperties** | - | ❌ `Properties.load` |

## 框架

| 场景 | 首选 | 次选 |
|---|---|---|
| Web | **Spring Boot 3.x** | Quarkus / Helidon |
| 微服务 | **Spring Cloud Alibaba** | Spring Cloud Netflix（部分停更） |
| ORM | **MyBatis-Plus** / Spring Data JPA | JOOQ（复杂查询） |
| 数据库迁移 | **Flyway** | Liquibase |
| 安全 | **Spring Security** | Shiro |
| WebSocket | **Spring WebFlux** | Netty |

## 规则

1. **Hutool + Spring Boot + MyBatis-Plus + Redisson + Nacos + Sentinel + Hutool Crypto** 是基线
2. 同一类别只用 1 个（不要 Hutool + Guava 一起）
3. 引入新库前查：
   - GitHub star（> 5k）
   - 最近 commit（< 6 个月）
   - License（MIT / Apache 2.0 优先）
   - CVE 历史（无高危未修复）
4. 禁止引 GPL / AGPL（传染性）

## 反模式

- ❌ 自造工具类（用 Hutool）
- ❌ 用 `Date` 而不是 `LocalDateTime`
- ❌ 用 `SimpleDateFormat` 共享实例（非线程安全）
- ❌ 用 Fastjson 1.x
- ❌ 自造连接池（用 HikariCP，Spring Boot 默认）
- ❌ 自造 HTTP 客户端（用 OkHttp / RestTemplate）
- ❌ 自造分布式锁（用 Redisson `RLock`）
- ❌ 自造雪花 ID（用 Hutool / Leaf）
- ❌ `System.out.println` 留生产代码
