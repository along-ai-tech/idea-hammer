# lockfile 强制

## 规则

**所有项目必须 commit lockfile**：

| 语言 | lockfile |
|---|---|
| Java (Maven) | `mvn -U dependency:resolve-plugins`（自动） |
| Java (Gradle) | `gradle.lockfile` |
| Python (pip) | `requirements.txt` + hash / `uv.lock` / `poetry.lock` |
| Python (Pipenv) | `Pipfile.lock` |
| Node.js | `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` |
| Go | `go.sum` |
| Rust | `Cargo.lock` |
| Ruby | `Gemfile.lock` |

## 强制规则

### 1. lockfile 必须 commit

```bash
# ❌ 错误
echo "*.lock" >> .gitignore

# ✅ 正确
git add package-lock.json
git commit -m "Update deps"
```

### 2. CI 必须用 lockfile

```yaml
# ❌ 错误
- run: pip install -r requirements.txt
# 不锁版本，不同机器版本不同

# ✅ 正确
- run: pip install --require-hashes -r requirements.txt
# 或
- run: npm ci  # 用 package-lock.json
```

### 3. lockfile 冲突要解决

```bash
# PR 触发 lockfile 冲突
git checkout main -- package-lock.json
npm install
git add package-lock.json
git commit -m "Resolve lockfile conflict"
```

### 4. lockfile 改动需要 review

PR 涉及 lockfile 变更 → 必须 review（确认无恶意依赖）。

### 5. hash 校验

```bash
# pip
pip install --require-hashes -r requirements.txt

# requirements.txt 带 hash
package==1.0.0     --hash=sha256:abc123...     --hash=sha256:def456...
```

## 项目规范示例

### Python（uv）

```toml
# pyproject.toml
[project]
dependencies = [
    "fastapi>=0.110",
    "pydantic>=2.6",
]
```

```bash
uv lock          # 生成 uv.lock
uv sync          # 用 uv.lock 安装
```

### Node.js（pnpm）

```yaml
# .npmrc
engine-strict=true
save-exact=true  # 精确版本（不带 ^）
```

```bash
pnpm install     # 用 pnpm-lock.yaml
pnpm add lodash  # 自动更新 lock
```

### Java（Maven）

```xml
<!-- pom.xml：用 Maven 自带锁 -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>my-lib</artifactId>
    <version>1.0.0</version>
</dependency>
```

Maven 不需要显式 lockfile，但 `mvn -U` 强制更新。

### Go（modules）

```bash
go mod download   # 用 go.sum
go mod verify     # 校验 hash
```

## 反模式

- ❌ lockfile 不 commit
- ❌ CI 不带 `--frozen-lockfile` / `npm ci`
- ❌ `requirements.txt` 不带 `--require-hashes`
- ❌ lockfile 改动无 review
- ❌ 删 lockfile 重新生成（破坏可重现）
