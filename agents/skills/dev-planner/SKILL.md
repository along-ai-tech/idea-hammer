---
name: dev-planner
description: 当 Product-Spec.md 已完成、需要先定技术方案再拆开发计划时使用。先在 Technical-Design.md 收敛架构、领域、数据与 API Contract，再输出 DEV-PLAN.md。也在 Spec 变更后更新已有计划。
---

# dev-planner

[任务]
    技术设计模式：读 Product-Spec.md 和 Design-Brief.md，定架构模式、模块边界、领域模型、数据设计、API Contract 与 ADR，输出 Technical-Design.md。
    生成模式：基于 Technical-Design.md 分析依赖，WebSearch 验证版本与漏洞，输出 DEV-PLAN.md。
    迭代模式：Spec 变更后先判断是否影响架构 / 数据 / 接口，受影响先改 Technical Design，再更新 Phase 与文件清单；已完成 Phase 不动。

[依赖检测]
    必需：Product-Spec.md。新项目还必须有 Technical-Design.md，缺了先走 workflow-technical-design.md。
    可选（缺了标降级）：Design-Brief.md、设计工具 MCP、已有项目代码。存量迭代缺 Technical Design 时补最小版（架构 / 数据 / API 三节）。

[使用方式]
    启动 → 需要技术设计时先读 workflows/workflow-technical-design.md，用 templates/technical-design-template.md 输出 Technical-Design.md；再读 workflows/workflow-generate.md 或 workflow-iterate.md，用 templates/dev-plan-template.md 输出 DEV-PLAN.md。

[引用]
    原则：principles/*.md（必读 technical-design + phase-planning + tech-validation）
    Spec 字段映射：
    - §5 REQ/AC → 每个 DT 的 **关联需求**；P0 REQ 至少一个 DT，AC 至少被一个测试引用
    - §5 输入字段 → API 入参；展示字段 → UI；状态流转 → 状态机；派生计算 → 后端计算
    - §1.5 架构 → 模块边界；§3 业务流程 → 实现顺序；§6 数据模型 → 领域模型、表结构与迁移
    - §8 并发与一致性 → 锁/幂等/事务边界（单机可显式"不要求"）
    流程：workflows/workflow-technical-design.md / workflow-generate.md / workflow-iterate.md
    契约：contracts/input.schema.json / output.schema.json
    模板：templates/technical-design-template.md / dev-plan-template.md
