---
name: product-spec-builder
description: 当用户说想做一个产品、应用或工具，或者说要加功能、改需求、调 UI 时使用。通过分阶段深入访谈收集需求，生成或更新 Product-Spec.md。
---

# product-spec-builder

[任务]
    0-1 模式：通过分阶段深入访谈收集需求，用直白甚至刺耳的追问逼用户想清楚，生成结构完整、可直接开发的 Product-Spec.md。
    迭代模式：用户开发中提新功能、改需求时，追问清楚变更，检测与现有 Spec 的冲突，更新 Spec 并记变更日志。

[依赖检测]
    扫项目目录找需求文档：精确匹配 Product-Spec.md，模糊匹配 *spec*.md、*prd*.md、*需求*.md。
    找到 → 迭代模式，读 workflows/workflow-iteration.md。
    没找到 → 0-1 模式，读 workflows/workflow-0-1.md，进场前先按 [搜索增强双遍] 第一遍搜竞品。
    多个候选 → 列文件名问用户改哪个。

[使用方式]
    启动 → 读 principles/ 必读 → 按模式走 workflows/ 对应流程 → 用 templates/product-spec-template.md 写 Product-Spec.md → contracts/output.schema.json 校验。

[文件结构]
    product-spec-builder/
    ├── SKILL.md                  # 本文件（≤ 30 行）
    ├── principles/               # 第一性原则
    ├── workflows/                # 0-1 + 迭代流程
    ├── contracts/                # 输入输出 schema
    ├── templates/                # Product-Spec 模板
    └── examples/                 # 填充示例

[引用]
    原则：principles/interview-discipline.md（必读）/ principles/ai-capability-awareness.md / principles/scope-discipline.md / principles/phase-discipline.md / principles/question-bank.md
    流程：workflows/workflow-0-1.md（0-1）/ workflows/workflow-iteration.md（迭代）
    契约：contracts/input.schema.json / contracts/output.schema.json
    模板：templates/product-spec-template.md / templates/changelog-template.md
    示例：examples/claude-code-desktop.md
