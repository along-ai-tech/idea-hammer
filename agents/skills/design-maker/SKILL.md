---
name: design-maker
description: 当 Design Brief 完成后、用户需要生成设计稿时使用。读取 Product-Spec.md 和 Design-Brief.md，通过设计工具 MCP 生成一整套设计交付物，包括所有页面、状态变体、组件规范和设计变量。
---

# design-maker

[任务]
    读 Product-Spec.md 和 Design-Brief.md，通过设计工具 MCP 生成完整设计交付物。Spec 里每个有 UI 的功能都要有设计页面，每个页面覆盖所有关键状态变体。

[依赖检测]
    必需：Product-Spec.md、Design-Brief.md、设计工具 MCP。
    设计工具检测：问用户用 Pencil 还是 Figma → 检测 MCP 是否连接 → 没连尝试连或提示用户 → 用户跳过则退出，后续按无设计稿模式继续。

[使用方式]
    读 principles/ 必读 → 按 workflows/execute.md 走 → 用 contracts/output.schema.json 校验交付物。

[文件结构]
    design-maker/
    ├── SKILL.md             # 本文件（≤ 30 行）
    ├── principles/          # 设计原则
    ├── workflows/           # 执行流程
    └── contracts/           # 输出 schema

[引用]
    原则：principles/coverage-discipline.md
    流程：workflows/execute.md
    契约：contracts/output.schema.json
