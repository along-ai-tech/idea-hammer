# 流程：迭代模式（Spec 变更后更新 DEV-PLAN.md）

> Spec 变更后，分析影响范围，更新 DEV-PLAN.md。

## 阶段 1：定位变更

**目标**：理解改了什么
**动作**：
1. 读更新后的 Product-Spec.md
2. 读 Product-Spec-CHANGELOG.md
3. 读现有 DEV-PLAN.md
4. 对比识别：哪些 Phase 受影响

**完成**：受影响 Phase 列表

## 阶段 2：影响分析

**动作**：
1. 已完成 Phase：是否回溯修改？
2. 进行中 Phase：调整交付清单
3. 未开始 Phase：增删改
4. 依赖图重排

**完成**：变更方案

## 阶段 3：向用户说明

**动作**：
1. 列出受影响 Phase + 变更内容
2. 用户确认

**完成**：用户同意

## 阶段 4：更新 DEV-PLAN.md

**动作**：
1. 已完成 Phase 不动
2. 进行中 + 未开始 Phase 按方案改
3. 重新校验依赖图

**完成**：DEV-PLAN.md 更新

## 阶段 5：回 dev-builder 同步

**动作**：
1. 变更动到已写代码的 Phase → 提醒用户回 dev-builder 同步实现
2. 只提醒，不自动改

**完成**：用户收到提醒
