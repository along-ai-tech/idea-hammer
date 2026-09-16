# 流程：初始化模式（无代码搭骨架）

> 用户已有 Product-Spec.md 和 DEV-PLAN.md，但项目还没建代码库。本流程搭骨架到 Phase 1 可执行为止。

## 阶段 1：环境准备

**目标**：按 DEV-PLAN 技术栈表配齐工具链
**动作**：
1. 读 DEV-PLAN 技术栈表，确认运行时版本（Python / Node / Go 等）
2. 装系统级依赖（包管理器、编译器）
3. 准备目录结构

**完成**：包管理器、运行时可用

## 阶段 2：项目骨架

**目标**：建项目代码目录、装依赖、配环境
**动作**：
1. 项目代码放在以项目名命名的子文件夹（如 `flashcards/`），不平铺根目录
2. 规划文档（Product-Spec.md / DEV-PLAN.md / Design-Brief.md）留根目录
3. 按 DEV-PLAN 技术栈表初始化项目（package.json / pyproject.toml / go.mod 等）
4. TypeScript strict（如适用）、lint / format 配置、目录约定
5. 装运行时依赖 + 开发依赖

**完成**：项目代码目录可 `cd` 进去跑 `dev` / `test` 命令

## 阶段 3：Git 初始化

**目标**：版本控制就绪
**动作**：
1. `git init`
2. 写 `.gitignore`：规划文档、环境变量、构建产物、IDE 配置
3. 建 private 远程仓库（gh CLI / gitee CLI / 手动）
4. 首次 commit + push
5. hook 系统就位（detect-feedback-signal 等）

**完成**：`git status` 干净 + 远程仓库可达

## 阶段 4：进入 Phase 1

**目标**：开始第一个 Phase 的开发
**动作**：
1. 读 DEV-PLAN Phase 1 章节 + Product-Spec 相关章节
2. 切到 workflow-task-loop.md，按 Phase 1 的 Task 拆分逐个执行

**完成**：第一个 Task 进入 RED 阶段

## 失败处理

- 阶段 1 缺系统工具 → 提示用户装；能自己装的直接装
- 阶段 2 装依赖失败 → 看错误信息，常见是网络 / 权限
- 阶段 3 git remote 认证失败 → 提示用户配 SSH key 或 PAT
- 阶段 4 Phase 1 任务不清晰 → 回 product-spec-builder 补 Spec，或 dev-planner 补 Plan
