# License 白名单

## 白名单（允许使用）

| License | 允许 | 条件 |
|---|---|---|
| **MIT** | ✅ | 保留 copyright |
| **Apache 2.0** | ✅ | 保留 copyright + NOTICE |
| **BSD 2-Clause / 3-Clause** | ✅ | 保留 copyright |
| **ISC** | ✅ | 保留 copyright |
| **MPL 2.0** | ✅ | 修改的文件需公开 |
| **Unlicense / Public Domain** | ✅ | - |

## 需评估（咨询法务）

| License | 风险 |
|---|---|
| LGPL | 动态链接 OK，静态链接需公开修改 |
| GPL | 传染性强（项目也变 GPL） |
| AGPL | 网络服务也需开源 |
| CDDL | 类似 GPL |
| Eclipse Public License | 类似 Apache，需评估兼容性 |

## 禁止（项目不能用）

| License | 理由 |
|---|---|
| **SSPL** | 服务端也要开源 |
| **Commons Clause** | 商业限制 |
| **Elastic License v2** | 商业限制 |
| **Busl** | 商业限制 |
| 未知 / 自定义 license | 无法评估 |

## 检测工具

| 工具 | 适用 |
|---|---|
| **license-checker** (npm) | Node.js |
| **pip-licenses** | Python |
| **license-maven-plugin** | Java |
| **reuse-tool** | 通用（SPDX） |
| **scancode-toolkit** | 通用（深度扫描） |

## CI 卡门禁

```yaml
# .github/workflows/license-check.yml
- name: License check
  run: |
    npx license-checker --failOn 'GPL;AGPL;SSPL'
    # 或 Python
    pip-licenses --fail-on 'GPL;AGPL;SSPL'
```

## 处理冲突依赖

如果 transitive dependency 用了 GPL：

```bash
# 1. 看依赖树
npm ls
mvn dependency:tree
pip show <package>

# 2. 找替代品
- GPL 库 → 找 MIT / Apache 等价库
- 例如：Fastjson 1.x → Jackson（避免 Fastjson 反序列化漏洞）

# 3. 如果必须用 → 走法务流程
```

## 文档

每个项目 README 列出第三方依赖的 license 摘要：

```
## Third-Party Licenses

This project uses the following open-source libraries:
- Spring Boot (Apache 2.0)
- Jackson (Apache 2.0)
- ...

Full license texts: THIRD_PARTY_LICENSES.md
```
