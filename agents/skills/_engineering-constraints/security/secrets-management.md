# 密钥管理

## 反模式

```python
# ❌ 错误：硬编码密钥
DATABASE_PASSWORD = "my-secret-password"
API_KEY = "sk-1234567890abcdef"

# ❌ 错误：提交到 Git
git add .env
git commit -m "add config"

# ❌ 错误：env 变量传进程参数
os.execve("python", ["python", "app.py"], {"DB_PASS": "secret"})
# ps aux 能看到
```

## 解决方案

### 1. 本地开发

```bash
# .env（不进 Git，.gitignore 排除）
DB_HOST=localhost
DB_PASSWORD=dev-password

# .env.example（进 Git，模板）
DB_HOST=
DB_PASSWORD=
```

```python
# 用 pydantic-settings 读取
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_password: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. 生产环境

| 方案 | 适用 |
|---|---|
| **HashiCorp Vault** | 企业级 / 多云 |
| **AWS Secrets Manager** | AWS 生态 |
| **Azure Key Vault** | Azure 生态 |
| **GCP Secret Manager** | GCP 生态 |
| **Kubernetes Secret** + External Secrets Operator | K8s |
| **Doppler / Infisical** | 轻量级 / 团队 |

### 3. K8s Secret + 加密

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
data:
  # base64 编码（仅编码，不加密！）
  password: <base64-encoded-value>
---
# 推荐：External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: secret/data/db
      property: password
```

## 强制规则

### 1. .gitignore

```
.env
.env.*
!.env.example
*.pem
*.key
credentials.json
```

### 2. 定期轮转

- API Key：90 天
- 数据库密码：90 天
- JWT 签名密钥：30 天
- 自动化脚本（cron）轮转

### 3. 最小权限

```yaml
# ❌ 错误：root 账号
DATABASE_URL=postgres://root:xxx@db/myapp

# ✅ 正确：专用账号 + 最小权限
DATABASE_URL=postgres://myapp_reader:xxx@db/myapp  # 只读
DATABASE_URL=postgres://myapp_writer:xxx@db/myapp  # 只写
```

### 4. 不在错误信息里泄露密钥

```python
# ❌ 错误
except Exception as e:
    return {"error": str(e), "config": config}  # 暴露配置

# ✅ 正确
except Exception as e:
    log.error("DB connection failed", exc_info=True)  # 日志带 stack
    return {"error": "Internal error", "trace_id": trace_id}
```

## 检测

- **GitHub Secret Scanning**：自动检测 push 的密钥
- **TruffleHog**：本地扫描 Git 历史
- **gitleaks**：CI 卡门禁
- **pre-commit hook**：本地拦截
