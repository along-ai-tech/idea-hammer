# 流程：发布（Web / Desktop / CLI）

## 阶段 1：问清需求

**动作**：
1. 打包还是发布？
2. 什么渠道？
3. 什么平台？

**完成**：发布类型确定

## 阶段 2：依赖检测

**动作**：
1. 检测项目代码 / git / 构建工具 / package.json
2. 按发布渠道检测所需 CLI + 认证状态
3. 只打包不发布 → 跳过部署工具

**完成**：依赖就绪

## 阶段 3：确认版本

**动作**：
- package.json version 已更新
- CHANGELOG 已更新
- 工作区干净（git status 无 uncommitted）

**完成**：版本合规

## 阶段 4：构建 + 打包

**动作**：
- 跑构建命令，零错误
- 产物大小合理（异常偏大排查是否打了不该打的）

**完成**：构建产物

## 阶段 5：隐私审计（绝对底线）

对构建产物目录执行：

```bash
# 开发者路径
grep -rn "/Users/" dist/

# 数据文件
find dist/ -name "*.db" -o -name ".env*" -o -name "credentials*" -o -name "*.pem" -o -name "*.key"

# 凭据
grep -rn -E "sk-ant-|sk-proj-|ANTHROPIC_API_KEY|OPENAI_API_KEY|password.*=.*['\"]" dist/
```

**任一项发现 → 立刻停，修完重新构建**

## 阶段 6：安装测试

| 类型 | 验证 |
|---|---|
| Web | 访问部署 URL，无白屏 |
| Desktop | 从安装包装到系统目录启动 |
| CLI | 全局安装 |

## 阶段 7：冒烟测试

- 对照 Spec 跑核心功能
- 关键 API 验证返回

## 阶段 8：发布

**动作**：
- 用户确认后发布
- 发布后再验证（Web 访问 / Desktop 安装 / CLI 命令）

## 发布策略

### Web

构建 → 隐私审计 → 配生产环境变量 → 部署 Vercel 或 Netlify → 访问 URL 验证无白屏 → 对照 Spec 冒烟测试

### Desktop

构建 → 打包对应平台 → 检查签名配置（无证书告知用户绕过方式） → 隐私审计 → 提醒用户从安装包启动 → 冒烟测试

### CLI

构建 → 隐私审计 → npm publish 或打二进制 → 全局安装验证命令 → 核心命令逐个冒烟测试

## 回退策略

### Web | Vercel rollback 或控制台回退上一个部署
### Desktop | 无法远程回退已分发包，修完 bump 版本重新打包发布
### CLI | npm deprecate 旧版本；严重问题 72h 内 unpublish；修完 bump 版本重发

## 失败处理

- 隐私审计任何一项失败 → 立刻停
- 安装测试失败 → 重构产物，重打
- 冒烟测试失败 → 回 dev-builder 修
- 发布后问题 → 走回退策略
