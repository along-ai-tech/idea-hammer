# 流程：执行审查（Stage 1 → Stage 2 → 报告）

> 两阶段审查。Stage 1 通过才进 Stage 2。

## 阶段 0：准备

**目标**：加载审查输入
**动作**：
1. 读 contracts/input.schema.json 校验输入
2. 读 Product-Spec.md 全文（审查基线）
3. 读设计稿 / Design-Brief（如有）
4. 读 DEV-PLAN.md（如有，了解当前 Phase）
5. 列项目代码结构

**完成**：审查基线就绪

## 阶段 1：做对了没有

**目标**：验证功能完整
**动作**（按 principles/stage1-checklist.md）：
1. **功能完整性**：Spec 每条功能逐项对照代码
2. **引导真实性**：UI 占位 / 引导文案对应行为
3. **UI 一致性**：设计数值逐项比对

每项输出：完整实现 / 部分实现 / 未实现

**完成判定**：
- 没有 HIGH 级别问题 → 进 Stage 2
- 有 HIGH 级别问题 → 停在 Stage 1，报告标注"Stage 2 未执行"

## 阶段 2：做好了没有

**目标**：验证实现质量
**动作**（按 principles/stage2-checklist.md）：
1. 代码质量（命名 / any / 文件 ≤ 300 行 / 单一职责 / 错误处理）
2. 工程级约束符合度（造轮子 / 库选择 / 安全 / 性能 / 错误处理）
3. 测试真实性 + TDD 合规
4. 安全扫描（grep）
5. Spec 漂移检查

**完成**：Stage 2 全维度检查完毕

## 阶段 3：报告输出

**目标**：输出结构化审查报告
**动作**：
1. 按 contracts/output.schema.json 格式
2. 分组列出：完整实现 / 部分实现 / 未实现 / Spec 漂移 / 安全问题 / 代码质量 / 编译结果
3. 每项附文件路径 + 行号 + 验证方式
4. Priority 标记：HIGH / MEDIUM / LOW
5. 安全问题单独高亮

**完成**：报告落地 + 通知主 Agent

## 报告路由

- Stage 1 失败 → dev-builder 补实现
- Stage 2 失败（质量 / 重构）→ dev-builder 修
- Stage 2 失败（缺陷 / 安全）→ bug-fixer 修
- 修完重派从 Stage 1 起

## 失败处理

- 阶段 1 HIGH 问题 → 停，不进 Stage 2
- 阶段 2 严重违规（如硬编码密钥）→ 安全告警，主 Agent 立即决策
- 报告无法生成（schema 不匹配）→ 重写

## 审查策略（参考）

- 逐项对照：读 Spec 条目 → 搜代码对应实现 → 验证行为 → 记证据
- 设计数值对比：提取设计稿数值 → 读代码 Tailwind class 或 style → 逐项比对
- 安全扫描：见 stage2-checklist.md "安全扫描" 段
- 有 Playwright 则测：核心路径 / 错误场景 / 状态变化 / 导航
