---
name: skill-builder
description: 当用户说要创建新技能，或 EVOLUTION.md 提议自动生成新 Skill 时使用。按照框架模块化规范创建结构一致的新 Skill。
---

# skill-builder

[任务]
    根据用户需求或 EVOLUTION 提议，创建符合框架规范的新 Skill，结构和现有 Skill 一致、即插即用。

[依赖检测]
    无必需依赖。可选：来自进化提议时读对应 proposal 了解背景。

[使用方式]
    读 principles/ 必读 → 按 workflows/create-skill.md 走 → 校验 contracts/。

[文件结构]
    skill-builder/
    ├── SKILL.md             # 本文件（≤ 30 行）
    ├── principles/          # 创建 + 写作纪律
    ├── workflows/           # 创建流程
    └── contracts/           # 输出 schema

[引用]
    原则：principles/structure-discipline.md / principles/writing-discipline.md
    流程：workflows/create-skill.md
    契约：contracts/output.schema.json
