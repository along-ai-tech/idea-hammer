# 依赖升级策略

## 升级频率

| 类型 | 频率 | 验证 |
|---|---|---|
| **Patch（1.0.0 → 1.0.1）** | 自动（Dependabot / Renovate） | CI 通过即可 |
| **Minor（1.0.0 → 1.1.0）** | 每周 | 全测试 + 烟雾测试 |
| **Major（1.x → 2.0.0）** | 季度评估 | 写迁移指南 + 充分测试 |

## 自动化

### Dependabot（GitHub）

```yaml
# .github/dependabot.yml
version: 2
updates:
- package-ecosystem: "npm"
  directory: "/"
  schedule:
    interval: "weekly"
  open-pull-requests-limit: 10
  groups:
      dependencies:
        patterns:
          - "*"
  labels:
    - "dependencies"
  
- package-ecosystem: "pip"
  directory: "/"
  schedule:
    interval: "weekly"
```

### Renovate（更灵活）

```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "updateType": ["minor", "patch"],
      "automerge": true
    },
    {
      "updateType": "major",
      "labels": ["breaking-change"]
    }
  ]
}
```

## Major 升级流程

### 1. 评估影响

```bash
# 看 changelog
curl https://raw.githubusercontent.com/lib/lib/v2.0.0/CHANGELOG.md

# 看 breaking changes
curl https://raw.githubusercontent.com/lib/lib/main/MIGRATION.md
```

### 2. 创建升级分支

```bash
git checkout -b upgrade/lib-v2
```

### 3. 升级 + 跑测试

```bash
npm install lib@2
npm test
npm run e2e
```

### 4. 修复 API 变更

```bash
# IDE 重构工具
# codemod（库提供）
npx lib-codemod v1-to-v2 ./src
```

### 5. 验证

- [ ] 所有测试通过
- [ ] 烟雾测试通过
- [ ] 性能回归（benchmark 对比）
- [ ] 安全扫描（无新漏洞）

### 6. 合并 + 发布

```bash
git commit -m "Upgrade lib v1 → v2 (BREAKING)"
# 触发 release notes
```

## Patch 自动合并

Dependabot / Renovate 可以自动合并 patch，前提：
- CI 全过
- 单测 + 集成测试通过
- 2 个 reviewer（自动 + 1 个）

## 弃用依赖处理

```bash
# 1. 看弃用时间表
npm view lib deprecated

# 2. 找替代
# 推荐：先看 npm trends / 社区反馈

# 3. 迁移
# 推荐：先在 feature branch 试，跑全套测试

# 4. 删除旧依赖
npm uninstall old-lib
```

## 反模式

- ❌ 长期不升级（累积技术债 → 升级更难）
- ❌ Major 升级不写迁移指南
- ❌ 升级不跑全测试
- ❌ 弃用库不替换
- ❌ 自动合并 minor / major（破坏性变更）
- ❌ 升级不通知团队（沟通成本）
