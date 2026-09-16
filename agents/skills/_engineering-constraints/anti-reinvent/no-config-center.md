# 禁止自造配置中心

> Nacos / Apollo / Consul / Spring Cloud Config 都成熟。

## 选型

| 场景 | 推荐 |
|---|---|
| Java + Spring | **Nacos**（阿里）/ Apollo（携程） |
| 多语言 | **Consul** / **etcd** |
| Kubernetes | **ConfigMap / Secret** + Reloader |
| 小项目 | **Spring Cloud Config** |

## 反模式

```java
// ❌ 错误：数据库存配置
public class ConfigService {
    public String get(String key) {
        return jdbc.queryForObject("SELECT value FROM config WHERE key = ?", key);
    }
}
// 没热更新、没变更通知、没权限管理

// ❌ 错误：环境变量硬编码
String dbUrl = "jdbc:mysql://localhost:3306/mydb";
// 不同环境（dev/staging/prod）切换要改代码

// ❌ 错误：本地文件配置
File config = new File("/etc/myapp/config.properties");
// 多实例时不同步
```

## ✅ 正确：用 Nacos

```yaml
# bootstrap.yml
spring:
  cloud:
    nacos:
      config:
        server-addr: nacos.example.com:8848
        file-extension: yaml
```

```java
// 自动注入
@Value("${user.max-retry:3}")
private int maxRetry;

// 热更新（@RefreshScope + @NacosValue）
@NacosValue(value = "${user.max-retry:3}", autoRefreshed = true)
private int maxRetry;
```

## 配置原则

1. **配置分层**：
   - 全局（公共）：数据库地址、Redis 地址
   - 应用级：业务参数
   - 实例级：端口、workerId
   - 用户/租户级：自定义参数

2. **敏感配置**（密码、密钥）：
   - **不进配置中心**
   - 用 Vault / AWS Secrets Manager / K8s Secret

3. **配置规范**：
   - Kebab-case key：`user.max-retry`
   - 命名空间隔离：`prod` / `staging` / `dev`
   - 改配置要走审批 + 审计
   - 大配置（> 100KB）拆文件

## 反模式检测

- 数据库 `config` 表存配置
- 环境变量硬编码在代码里
- `@Value("${...}")` 但配置来源不明
- 改配置要发版（没热更新）
