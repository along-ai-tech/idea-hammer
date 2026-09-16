# 流程：单 Task 循环（RED → GREEN → REFACTOR + review → fix）

> dev-builder 的核心循环：每个 Task 走完一遍 RED/GREEN/REFACTOR + 派发 code-reviewer 两阶段审查。

## 阶段 1：Plan

**目标**：把当前 Phase 拆成 Task
**动作**：
1. 读 DEV-PLAN 当前 Phase 章节 + Product-Spec 相关章节原文（不凭记忆）
2. 写 Task 拆分：每个页面、组件、功能一个 Task
3. 列出每个 Task 的交付清单（具体行为点）

**完成**：Task 列表 + 交付清单

## 阶段 2：单 Task 执行（每个 Task 必走）

### RED

**目标**：写失败测试
**动作**：
1. 读 DEV-PLAN 交付清单、Spec 功能描述、Design-Brief 视觉方向的原文（不凭记忆）
2. 为本 Task 每个行为点写最小失败测试，测试名回答"什么 break 让它失败"
3. 跑测试确认 FAIL 且失败原因是"功能缺失"非笔误或 typo
4. AI 生成代码不豁免 RED
5. 看不到失败不准进 GREEN

**完成**：测试 FAIL 且原因合理

### GREEN

**目标**：写最小代码让测试 PASS
**动作**：
1. 写最小代码让测试 PASS
2. 禁止超实现：不写测试没要求的功能、不"优化"无关代码、不重构
3. 跑全套测试确认零失败 + 输出干净无 error/warning

**完成**：测试全绿 + 输出干净

### REFACTOR

**目标**：清重复、改命名、抽公共方法（不新增行为）
**动作**：
1. 保持绿色前提下清重复、改命名、抽公共方法
2. 不新增行为
3. 跑测试确认仍全绿

**完成**：测试仍全绿 + 代码更清晰

### 自检

**目标**：代码实际值对照设计数值，行为对照 Spec
**动作**：
1. 读代码实际值（颜色 / 间距 / 字号）对照 Design-Brief
2. 行为对照 Spec 描述
3. 有偏差先修再提交

**完成**：代码值与设计值一致 + 行为与 Spec 一致

### 派 code-reviewer

**目标**：两阶段审查
**动作**：
1. spawn code-reviewer（参考 SUBAGENTS.md）跑两阶段审查
2. Stage 1 失败 → 回 RED 补实现，重新派
3. Stage 2 失败：质量/重构问题自己按修改纪律修；确属缺陷或安全漏洞才调 bug-fixer（bug-fixer 必先写复现测试）
4. 两阶段都过 → echo clean > .codex/.needs-review → commit

**完成**：两阶段审查 PASS + commit

## 阶段 3：commit + 下一个 Task

**目标**：原子提交 + 切下一个 Task
**动作**：
1. commit 用 feat: / fix: / test: / refactor: 前缀（区分 TDD 步骤里的 test: 与 fix:）
2. 切下一个 Task，回到阶段 2 单 Task 执行

**完成**：当前 Task commit + 下一个 Task 进入 RED

## 失败处理

- 用户强调某环节是追加要求 → 不替换基础流程，review 闭环 + TDD 循环照常走
- 测试隔离漏洞 → 立即停下修，参考 principles/tdd-discipline.md "测试隔离"段
- AI 生成代码忘了 RED → 补 RED 测试，确认 FAIL 再 GREEN
