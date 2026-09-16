# 流程：启动路由（初始化 vs 持续开发）

> 启动 dev-builder 第一步：检测项目状态，决定走初始化模式还是持续开发模式。

## 阶段 1：依赖检测

**目标**：确认前置输入就绪
**动作**：
1. 扫项目根目录找 Product-Spec.md、DEV-PLAN.md
2. 找 Product-Spec.md 和 DEV-PLAN.md 都齐全 → 进入阶段 2
3. 缺 Product-Spec.md → 提示用户先调 product-spec-builder
4. 缺 DEV-PLAN.md → 提示用户先调 dev-planner
5. 读 DEV-PLAN.md 技术栈表，确认必需的系统工具和运行时已装

**完成**：依赖检测结论（已就绪 / 缺什么）

## 阶段 2：模式判断

**目标**：决定走初始化还是持续开发
**动作**：
1. 扫 `agents/skills/dev-builder/` 的兄弟目录（即项目代码目录）是否存在且有代码
2. 无代码 + 有 DEV-PLAN → 初始化模式 → 读 workflow-init.md
3. 有代码 + 有 DEV-PLAN → 持续开发模式 → 读 workflow-task-loop.md
4. 进已有项目先读它自带的 agent 约定文件（AGENTS.md / CLAUDE.md），按项目规矩来

**完成**：模式确定 + 对应 workflow 入口已读

## 失败处理

- 必需依赖缺失 → 自己判断装法直接装；要用户权限或认证才提示用户
- 进已有脚手架 → 用项目自带约定，不用 dev-builder 默认覆盖
