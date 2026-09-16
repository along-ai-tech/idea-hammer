---
name: evolution-engine
description: 自进化的消化引擎。由 evolution-runner 调用，drain 信号队列、扫 git 挖掘重复模式、生成改动建议供主 Agent 当场问用户。也可由用户手动 /evolution-engine 触发。
---

# evolution-engine

[任务]
    消化待处理的纠正信号，产出改动建议写进 proposals.md，供主 Agent 在 session 启动时当场问用户。不替用户决定，不自己落地。

[输入源]
    被动：.codex/evolution/signals.jsonl 里的纠正信号。
    主动：git log 和 git diff，找反复出现的修复模式。

[使用方式]
    读 principles/ 必读 → 按 workflows/digest.md 走 → 写 proposals.md → contracts/output.schema.json 校验。

[文件结构]
    evolution-engine/
    ├── SKILL.md             # 本文件（≤ 30 行）
    ├── principles/          # 消化标准
    ├── workflows/           # 消化流程
    └── contracts/           # 输出 schema

[引用]
    原则：principles/abstraction-discipline.md
    流程：workflows/digest.md
    契约：contracts/output.schema.json
