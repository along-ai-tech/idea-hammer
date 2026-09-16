---
name: goal-creator
description: 当用户想把一个目标交给 /goal 自驱执行时使用。结合当前上下文理解用户要自驱什么，按 Goal 模板写好 /goal 指令，用户复制发送即可启动。
---

# goal-creator

[任务]
    结合当前上下文，理解用户接下来想自驱完成什么，按 Goal 模板写好一条 /goal 指令，交给用户复制发送。
    只准备指令，不替用户触发。slash command 必须用户自己发。

[依赖检测]
    无前置文件。读当前对话和项目状态作为上下文。

[使用方式]
    读 contracts/output.schema.json 校验输出 → 按 workflows/write-goal.md 走流程。

[文件结构]
    goal-creator/
    ├── SKILL.md            # 本文件（≤ 30 行）
    ├── principles/         # 第一性原则
    ├── workflows/          # 写 Goal 指令流程
    └── contracts/          # /goal 输出 schema

[引用]
    原则：principles/*.md（按需读）
    流程：workflows/write-goal.md（必读）
    契约：contracts/output.schema.json（机器校验）
