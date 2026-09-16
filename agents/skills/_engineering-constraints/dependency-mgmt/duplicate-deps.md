# 重复依赖检测

## 问题

同一库的不同版本同时存在 → 增加 bundle size / 内存，可能引入 bug。

```json
// package.json
{
  "dependencies": {
    "lodash": "^4.0.0"  // 用了 4.x
  }
}
// 但某个 transitive dep 用了 lodash@3
// → node_modules 里 lodash 出现两次
```

## 检测工具

| 语言 | 工具 |
|---|---|
| Node.js | `npm ls` / `pnpm dedupe --check` |
| Python | `pip check` / `pipdeptree` |
| Java | `mvn dependency:tree` / `gradle dependencies` |
| Go | `go mod graph` + 手动分析 |
| Rust | `cargo tree --duplicates` |

## 检测示例

```bash
# Node.js
npm ls lodash
# 输出：
# my-app@1.0.0
# ├── lodash@4.17.21
# └── some-lib@2.0.0
#     └── lodash@3.10.1  ← 重复！

# Python
pipdeptree --reverse
# 输出冲突

# Java
mvn dependency:tree -Dverbose | grep "omitted for conflict"
```

## 处理

### 方案 1：升级顶层依赖

```bash
# 升级依赖到要求更新的版本
npm install some-lib@3  # 现在用 lodash@4
```

### 方案 2：npm overrides

```json
// package.json
{
  "overrides": {
    "some-lib": {
      "lodash": "^4.17.0"
    }
  }
}
```

### 方案 3：yarn resolutions

```json
{
  "resolutions": {
    "lodash": "4.17.21"
  }
}
```

### 方案 4：替换依赖

如果某个库总是引入重复依赖 → 考虑替换。

## 前端 bundle size

```bash
# Webpack
npm install --save-dev webpack-bundle-analyzer
# 在 webpack.config.js 配置，看 bundle 占比

# Vite
npm install --save-dev rollup-plugin-visualizer
# 分析依赖大小

# 大依赖警告
- moment.js（已停更）→ date-fns / dayjs
- lodash 全量 → es-toolkit（按需）
- antd 全量 → 按需 import
```

## 反模式

- ❌ 知道有重复依赖但不处理
- ❌ 用 `overrides` 强锁但不审查兼容性
- ❌ bundle 巨大但不分析
- ❌ 还在用 moment.js
