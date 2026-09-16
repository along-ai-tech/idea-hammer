---
name: <skill-name>
description: <一句话说明何时使用本 skill。触发场景 + 核心动作 + 产出物。>
---

# <skill-name>

[任务]
    <本 skill 的核心职责：一两句话讲清做什么、产生什么产出物。>

[依赖检测]
    <启动第一步：扫什么目录/文件决定走哪个分支；缺什么提示用户补什么。>

[使用方式]
    0-1 模式：<首次使用场景描述> → 读 workflows/workflow-0-1.md。
    迭代模式：<已有产出物后修改> → 读 workflows/workflow-iteration.md。
    （按 skill 实际需要增减模式）

[文件结构]
    <skill-name>/
    ├── SKILL.md          # 本文件（≤ 50 行）
    ├── principles/       # 第一性原则（跨 skill 共享）
    ├── workflows/        # 执行流程
    ├── contracts/        # 输入输出 schema
    └── assets/           # 静态资源

[引用]
    原则：principles/*.md（按需读）
    流程：workflows/*.md（按需读）
    契约：contracts/*.schema.json（机器校验）
    资源：assets/*（按需用）
