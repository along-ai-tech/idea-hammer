# 依赖漏洞扫描

## 强制规则

### 1. 每次 PR 必跑漏洞扫描（卡门禁）

| 语言 | 工具 | 命令 |
|---|---|---|
| Java | OWASP Dependency-Check | `mvn dependency-check:check` |
| Java | Snyk | `snyk test` |
| Python | pip-audit | `pip-audit` |
| Python | Safety | `safety check` |
| Node.js | npm audit | `npm audit --audit-level=high` |
| Node.js | Snyk | `snyk test` |
| Go | govulncheck | `govulncheck ./...` |
| Rust | cargo-audit | `cargo audit` |
| 通用 | Snyk | 跨语言支持 |

### 2. 漏洞响应

| 等级 | 响应时间 | 动作 |
|---|---|---|
| **Critical** | 24 小时内 | 立即升级 / 替换 |
| **High** | 7 天内 | 升级 / 替换 / 缓解 |
| **Medium** | 30 天内 | 评估 + 计划 |
| **Low** | 下次维护 | 记录 |

### 3. lockfile 强制

```bash
# ❌ 错误：用 * 锁定
flask>=2.0

# ✅ 正确：精确版本 + hash
flask==3.0.0     --hash=sha256:...
```

lockfile 必须 commit，PR 必带 lockfile 变更。

## Java 示例（OWASP Dependency-Check）

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>9.0.9</version>
    <configuration>
        <failBuildOnAnyVulnerability>true</failBuildOnAnyVulnerability>
    </configuration>
</plugin>
```

```bash
mvn dependency-check:check
# 报告：target/dependency-check-report.html
```

## Python 示例（pip-audit）

```bash
pip-audit --strict
# 或在 requirements.txt 上跑
pip-audit -r requirements.txt
```

## Node.js 示例（npm audit）

```bash
npm audit --audit-level=high  # high 以上报错退出
```

## CI 配置示例

```yaml
# GitHub Actions
- name: Security audit
  run: |
    pip install pip-audit
    pip-audit --strict || exit 1
    npm audit --audit-level=high || exit 1

- name: OWASP check
  uses: dependency-check/Dependency-Check_Action@main
  with:
    project: 'pom.xml'
    args: >
      --failOnCVSS 7
      --enableRetired
```

## 反模式

- ❌ 用 `*` 锁定版本（不可重现）
- ❌ lockfile 不 commit
- ❌ 漏洞扫描只在本地跑（CI 必须卡）
- ❌ 漏洞太多"先这样"（高危必须修）
- ❌ 自己 fork 旧版本库（增加维护负担）
