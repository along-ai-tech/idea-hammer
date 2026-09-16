# OWASP Top 10 防护

## 1. 注入（Injection）

### SQL 注入

```java
// ❌ 错误：字符串拼接
String sql = "SELECT * FROM users WHERE name = '" + name + "'";

// ✅ 正确：参数化
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE name = ?");
ps.setString(1, name);
```

### NoSQL 注入

```python
# ❌ 错误
db.users.find({"name": request.json["name"]})  # name 可能是 {"$ne": null}

# ✅ 正确：类型校验
name = str(request.json["name"])  # 强制字符串
db.users.find({"name": name})
```

### 命令注入

```python
# ❌ 错误：shell=True
os.system(f"ls {user_input}")
subprocess.Popen(f"ls {user_input}", shell=True)

# ✅ 正确
subprocess.Popen(["ls", user_input], shell=False)
```

### LDAP / XPath 注入

避免直接拼接，用参数化库。

## 2. 跨站脚本（XSS）

```typescript
// ❌ 错误
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ 正确：自动转义
<div>{userInput}</div>

// ✅ 如果必须 HTML：用 DOMPurify 净化
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
```

**CSP 头**：
```nginx
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-xxx'
```

## 3. CSRF

```typescript
// 前端：CSRF token
axios.post('/api/transfer', data, {
    headers: { 'X-CSRF-Token': getCsrfToken() }
});

// 后端：SameSite cookie + token 校验
httpOnly + cookies + SameSite=Strict
```

## 4. SSRF（服务端请求伪造）

```java
// ❌ 错误：用户控制 URL
URL url = new URL(userInput);
HttpURLConnection conn = (HttpURLConnection) url.openConnection();

// ✅ 正确：白名单 / 域名校验
if (!ALLOWED_HOSTS.contains(url.getHost())) {
    throw new SecurityException("host not allowed");
}
// 内网地址过滤（10.0.0.0/8、172.16.0.0/12、192.168.0.0/16、127.0.0.0/8）
if (isPrivateIp(url.getHost())) {
    throw new SecurityException("private IP not allowed");
}
```

## 5. 反序列化漏洞

```java
// ❌ 错误：ObjectInputStream 反序列化不可信数据
ObjectInputStream ois = new ObjectInputStream(untrustedStream);
Object obj = ois.readObject();  // RCE 风险

// ✅ 正确：用 JSON / protobuf
ObjectMapper mapper = new ObjectMapper();
User user = mapper.readValue(jsonString, User.class);
```

**禁止 Fastjson 1.x**（反序列化 RCE）：用 Jackson 或 Fastjson2

## 6. 不安全的直接对象引用（IDOR）

```java
// ❌ 错误：用自增 ID
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userService.getById(id);  // 任何人都能看任何用户
}

// ✅ 正确：鉴权 + 检查所有权
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id, Authentication auth) {
    User user = userService.getById(id);
    if (!user.getId().equals(auth.getId())) throw new ForbiddenException();
    return user;
}
```

## 7. 安全配置错误

- 默认密码改掉
- 调试模式关闭（Spring `spring.profiles.active=prod`）
- 详细错误信息不返给前端（避免泄露内部细节）
- HTTPS 强制
- 安全头：HSTS、X-Frame-Options、X-Content-Type-Options

## 8. 不充分的日志和监控

- 登录失败、权限拒绝、输入验证失败必记录
- 告警：异常登录、异常流量、敏感操作

## 10. 服务端请求伪造（SSRF）

（已在 #4 涵盖）
