---
name: design-brief-builder
description: 当用户说要确定设计风格、视觉方向，或说'我想要高级感/简洁/现代'这类模糊描述时使用。通过设计师采访引导用户明确视觉偏好，输出 Design-Brief.md。
---

# design-brief-builder

[任务]
    0-1 模式：像设计师采访甲方，引导用户确定视觉方向，输出 Design-Brief.md，供设计工具和 dev-builder 参照。
    迭代模式：用户调整设计方向时，追问清楚，更新 Design-Brief.md。

[依赖检测]
    必需 Product-Spec.md。扫 Design-Brief.md → 有走 workflows/workflow-iteration.md，无走 workflows/workflow-0-1.md。
    0-1 进场前先按 [搜索增强双遍] 第一遍搜参考（见 principles/phase-discipline.md）。
    可选设计工具 MCP，缺了标手动设计模式，Brief 照样生成。

[使用方式]
    启动 → 读 principles/ 必读 → 按模式走 workflows/ 对应流程 → 用 templates/design-brief-template.md 写 Design-Brief.md → contracts/output.schema.json 校验。

[文件结构]
    design-brief-builder/
    ├── SKILL.md                  # 本文件（≤ 30 行）
    ├── principles/               # 第一性原则
    ├── workflows/                # 0-1 + 迭代流程
    ├── contracts/                # 输入输出 schema
    ├── templates/                # Design-Brief.md 模板
    └── examples/                 # 填充示例

[引用]
    原则：principles/interview-discipline.md（必读）/ principles/reference-anchoring.md / principles/feeling-translation.md / principles/question-bank.md / principles/phase-discipline.md
    流程：workflows/workflow-0-1.md（0-1）/ workflows/workflow-iteration.md（迭代）
    契约：contracts/input.schema.json / contracts/output.schema.json
    模板：templates/design-brief-template.md
    示例：examples/claude-code-desktop.md
