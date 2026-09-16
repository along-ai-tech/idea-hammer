# security/ — 安全规范

> AI 写代码必须遵循的安全基线。

## 文档

| 主题 | 文档 |
|---|---|
| OWASP Top 10 | [owasp-top10.md](./owasp-top10.md) |
| 认证与 JWT | [auth-jwt.md](./auth-jwt.md) |
| 密码哈希 | [password-hashing.md](./password-hashing.md) |
| 密钥管理 | [secrets-management.md](./secrets-management.md) |
| 依赖漏洞扫描 | [dependency-audit.md](./dependency-audit.md) |
| License 白名单 | [license-whitelist.md](./license-whitelist.md) |

## 核心规则

1. **OWASP Top 10 全防护**（注入 / XSS / CSRF / SSRF / 反序列化）
2. **密码用 bcrypt / argon2**（禁止 MD5 / SHA1）
3. **JWT 必须有 exp + refresh**
4. **密钥不落代码**（用 Vault / K8s Secret）
5. **依赖每周扫描漏洞**（卡门禁）
6. **License 严格白名单**（禁止 GPL / AGPL）
