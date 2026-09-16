# 认证与 JWT

## JWT 标准

```java
// ✅ 正确：用 jjwt / nimbus-jose-jwt
String token = Jwts.builder()
    .setSubject(userId)
    .setIssuedAt(new Date())
    .setExpiration(Date.from(Instant.now().plus(15, ChronoUnit.MINUTES)))  // 短过期
    .signWith(SignatureAlgorithm.HS256, secret)
    .compact();

// 必带字段
{
    "sub": "user-id",
    "iat": 1700000000,
    "exp": 1700000900,  // 15 分钟过期
    "iss": "my-app",
    "aud": "my-app"
}
```

## 强制规则

### 1. 必须有 exp（过期时间）

```java
// ❌ 错误：无 exp
Jwts.builder().setSubject(id).compact();

// ✅ 正确：15 分钟
.setExpiration(Date.from(Instant.now().plus(15, ChronoUnit.MINUTES)))
```

### 2. 短 access token + 长 refresh token

- **Access token**：15 分钟，存内存
- **Refresh token**：7-30 天，存 HttpOnly cookie + 数据库

```java
// 刷新流程
@PostMapping("/refresh")
public TokenPair refresh(@CookieValue("refresh_token") String refreshToken) {
    // 1. 验证 refresh token
    // 2. 检查是否在黑名单（已登出）
    // 3. 生成新的 access + refresh token
    // 4. 旧的 refresh token 加入黑名单（轮转）
}
```

### 3. 不要在 JWT 里存敏感信息

```java
// ❌ 错误：存密码 / 邮箱
.setClaim("password", password)
.setClaim("ssn", "123-45-6789")

// ✅ 只存 ID
.setSubject(userId)
```

JWT 是 base64 编码，**任何人都能解码**。敏感信息加密也不行，用 DB 查询。

### 4. 签名算法必须指定

```java
// ❌ 错误：默认 HS（256，密钥可被猜到）
Jwts.builder().compact();  // 默认不安全

// ✅ 正确：显式指定 + 强密钥
.signWith(SignatureAlgorithm.HS256, secretKey)
```

### 5. 不要用 `alg: none`

```java
// ❌ 危险：允许 alg=none
Jwts.parser().setSigningKey(secret).parse(token);

// ✅ 正确：限制算法
Jwts.parser().require("alg", "HS256").setSigningKey(secret).parse(token);
```

## OAuth 2.1

- Authorization Code Flow + PKCE（前端 / SPA）
- Client Credentials（服务间）
- Refresh Token Rotation

## Session 替代方案

如果不用 JWT，用 Session：
- HttpOnly + Secure + SameSite=Strict cookie
- Session ID 随机（不预测）
- 服务端 session 存 Redis

## 反模式

- ❌ JWT 存密码 / 邮箱 / SSN
- ❌ JWT 不过期
- ❌ JWT 签名密钥硬编码（用 KMS）
- ❌ 不验证 token 签名
- ❌ 前端存 JWT 到 localStorage（XSS 风险）→ HttpOnly cookie
- ❌ 长 token（payload 大 = 带宽浪费）
