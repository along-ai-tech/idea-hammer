# 必备 CI 检查

## 必过门禁（PR 不通过 = 不合并）

### 1. Lint / Format

| 语言 | 工具 |
|---|---|
| Java | checkstyle / spotless / sonarqube |
| Python | ruff / black / mypy |
| TypeScript | eslint / prettier |
| Go | golangci-lint / gofumpt |
| Rust | clippy / rustfmt |

### 2. 单元测试

- 覆盖率：行 ≥ 80%，分支 ≥ 70%
- 必须有失败测试（不能全 mock）
- mutation score ≥ 60%

### 3. 集成测试 / E2E

- 核心流程必须有 e2e
- Playwright / Cypress / 真实 HTTP

### 4. 编译 / Build

```yaml
- name: Build
  run: mvn -B verify --fail-at-end

# 前端必须 `tsc --noEmit` 零错误（TypeScript 严格类型检查）
- name: TypeScript check
  run: npx tsc --noEmit
```

### 5. 安全扫描

- OWASP Dependency-Check / Snyk
- 代码扫描（Semgrep / SonarQube）
- 密钥扫描（gitleaks / TruffleHog）

### 6. License 检查

- 拒绝 GPL / AGPL / SSPL

### 7. 镜像扫描（如有 Docker）

- Trivy / Snyk Container

## GitHub Actions 模板

```yaml
name: CI

on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Lint
      run: |
        mvn checkstyle:check
        ruff check .
        eslint .
    
    - name: Unit test
      run: |
        mvn test
        pytest --cov=app --cov-fail-under=80
    
    - name: E2E test
      run: npm run test:e2e
    
    - name: Build
      run: mvn -B package
    
    - name: Security scan
      uses: github/codeql-action/analyze@v2
    
    - name: Dependency audit
      run: |
        mvn dependency-check:check
        pip-audit --strict
    
    - name: License check
      run: npx license-checker --failOn 'GPL;AGPL;SSPL'
    
    - name: OpenAPI validate
      run: npx swagger-cli validate openapi.json
```

## 必填检查项（最少集合）

任何 PR 必须满足：
- [ ] Lint 通过
- [ ] 单测通过 + 覆盖率达标
- [ ] E2E 通过
- [ ] Build 通过
- [ ] 安全扫描通过（无 high / critical）
- [ ] License 检查通过
- [ ] 2 人 code review 通过（CODEOWNERS）

## 反模式

- ❌ 跳过 CI（"我自己测过了"）
- ❌ CI 只跑 lint 不跑测试
- ❌ 测试覆盖率无门禁
- ❌ 安全扫描只在 main 分支跑
- ❌ PR 自动化 merge（绕过 review）
