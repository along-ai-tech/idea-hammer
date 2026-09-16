# 密码哈希

## 算法选择

| 算法 | 推荐 | 理由 |
|---|---|---|
| **Argon2id** | ⭐⭐⭐ 最强 | 抗 GPU / 抗侧信道 |
| **bcrypt** | ⭐⭐ 主流 | 成熟、自动加盐 |
| **scrypt** | ⭐⭐ 备选 | 老牌稳定 |
| PBKDF2 | ❌ 弱 | 不抗 GPU 攻击 |
| MD5 / SHA1 / SHA256 | ❌❌❌ 禁止 | 不抗碰撞 / 不抗暴力 |

## 选型

- **新项目**：Argon2id（OWASP 2024 推荐）
- **老项目维护**：bcrypt
- **已有 PBKDF2**：升级到 Argon2id（在用户登录时 rehash）

## Java 示例

### Argon2id

```xml
<dependency>
    <groupId>de.mkammerer</groupId>
    <artifactId>argon2-jvm</artifactId>
    <version>2.11</version>
</dependency>
```

```java
import de.mkammerer.argon2.Argon2;
import de.mkammerer.argon2.Argon2Factory;

Argon2 argon2 = Argon2Factory.create(Argon2Types.ARGON2id);

// 注册
String hash = argon2.hash(10, 65536, 1, password.toCharArray());
// 10 = iterations, 65536 = memory (KB), 1 = parallelism

// 验证
boolean ok = argon2.verify(hash, password.toCharArray());
```

### bcrypt

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-crypto</artifactId>
</dependency>
```

```java
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);  // strength 12
String hash = encoder.encode(password);
boolean ok = encoder.matches(password, hash);
```

## Python 示例

```python
# ✅ Argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
hash = ph.hash(password)
ph.verify(hash, password)  # 失败抛异常

# ✅ bcrypt
import bcrypt
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
bcrypt.checkpw(password.encode(), hash)
```

## Node.js

```typescript
import argon2 from 'argon2';

const hash = await argon2.hash(password);
const ok = await argon2.verify(hash, password);
```

## 强制规则

### 1. 自动加盐

不要手写 salt，库自动处理。

### 2. 不存明文 / 加密密码

```java
// ❌ 错误：明文
String passwordPlain = user.getPassword();

// ❌ 错误：可逆加密（密钥泄露 = 全完）
String encrypted = AES.encrypt(password, masterKey);

// ✅ 正确：单向哈希
String hash = argon2.hash(password);
```

### 3. 不在日志 / URL 里出现密码

```java
// ❌ 错误
log.info("User login: " + password);
@GetMapping("/reset?password=xxx")

// ✅ 正确
log.info("User login attempt for userId={}", userId);
@PostMapping("/reset") @RequestBody PasswordResetDto dto
```

### 4. 失败响应时间恒定

```java
// ❌ 错误：用户不存在立即返回，用户存在再哈希（时间差异泄露用户存在）
if (user == null) return false;
return encoder.matches(password, user.getHash());

// ✅ 正确：无论用户是否存在都做哈希
String fakeHash = "$argon2id$v=19$m=65536,t=10,p=1$...";
String hash = user != null ? user.getHash() : fakeHash;
return encoder.matches(password, hash);
```

### 5. 重置流程要安全

- token 一次性 + 短过期（15 分钟）
- token 随机（`secrets.token_urlsafe(32)`）
- 用后立即失效

## 强度参数

- **bcrypt**：rounds ≥ 12（OWASP 推荐）
- **Argon2id**：time ≥ 3, memory ≥ 64MB, parallelism = 1
- **定期评估**：硬件升级后调整（保证 ~250ms 一次哈希）
