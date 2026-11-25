---
name: product-spec-builder
description: 当用户说想做一个产品、应用或工具，或者说要加功能、改需求、调 UI 时使用。主线：一句话需求 → 引导补齐 → 形成可直接交给下游 AI coding 的 Product-Spec.md。
---

# product-spec-builder

[任务]
    0-1 模式：从用户的一句话出发，先拆清候选能力与缺失维度，再按五问引导补齐，生成可直接排任务、写代码的 Product-Spec.md。
    迭代模式：用户开发中提新功能、改需求时，追问清楚变更，检测与现有 Spec 的冲突，更新 Spec 并记变更日志。

[依赖检测]
    扫项目目录找需求文档：精确匹配 Product-Spec.md，模糊匹配 *spec*.md、*prd*.md、*需求*.md。
    找到 → 迭代模式，读 workflows/workflow-iteration.md。
    没找到 → 0-1 模式，读 workflows/workflow-0-1.md，进场前先按 [搜索增强双遍] 第一遍搜竞品。
    多个候选 → 列文件名问用户改哪个。

[使用方式]
    启动 → 读 principles/ 必读 → 按模式走 workflows/ 对应流程 → 用 templates/product-spec-template.md 写 Product-Spec.md → contracts/output.schema.json 校验。
    需求按五层组织：PRD（为什么做 / 为谁做 / 什么价值）→ FRD（每个功能怎么工作）→ User Story（作为一个…我希望…以便于…）→ AC（可验证的完成条件）→ Spec（组织成可执行规格）。
    主线：一句话入口（idea-intake）→ Discovery 五问（值不值得投入）→ 引导补齐 5 问（用户与场景）→ Spec 成稿；出口判据 = `check_spec_standard.py` 通过且下游能直接据此排任务、写代码。

[方法与契约]（需求工程同样由 AI 执行，不允许自由发挥）
    目标层 Q1–Q3：苏格拉底式追问（socratic-questioning.md）
    FRD 层：竞品与业界实现调研 + 逻辑严谨清单（frd-research.md）
    四要素标准：spec-standard.md（含 Spec 唯一事实源 + US / AC 质量规则 + Phase 0 硬门禁）
    输出契约：contracts/output.schema.json（PRD 字段、US 三句、AC ≥ 3 且编号合规）
    校验：scripts/check_spec_standard.py（结构）+ scripts/check_traceability.py（链路）
    测试：tests/contract/test_spec_contract.py（schema）+ tests/contract/test_spec_standard.py（门禁行为）

[文件结构]
    product-spec-builder/
    ├── SKILL.md                  # 本文件（≤ 30 行）
    ├── principles/               # 第一性原则
    ├── workflows/                # 0-1 + 迭代流程
    ├── contracts/                # 输入输出 schema
    ├── templates/                # Product-Spec 模板
    └── examples/                 # 填充示例

[引用]
   原则：principles/interview-discipline.md（必读）/ principles/spec-standard.md（必读：四要素标准 + Phase 0 硬门禁）/ principles/socratic-questioning.md（Q1–Q3 必读）/ principles/frd-research.md（FRD 必读）/ principles/ai-capability-awareness.md / principles/scope-discipline.md / principles/phase-discipline.md / principles/question-bank.md / **principles/idea-intake.md（一句话入口必走）** / **principles/product-definition.md（0-1 必走）** / **principles/competitive-scan.md（0-1 必走）** / **principles/ceo-lens.md（收尾必走）** / **principles/eng-lens.md（收尾必走）** / **principles/qa-lens.md（收尾必走）** / **principles/spec-red-green.md（改 spec 前必读）** / **principles/path-classification.md（Phase 0 前必读）** / **principles/spec-audit.md（收尾必读）**
    流程：workflows/workflow-0-1.md（0-1）/ workflows/workflow-iteration.md（迭代）
    契约：contracts/input.schema.json / contracts/output.schema.json
    模板：templates/product-spec-template.md / templates/changelog-template.md
    示例：examples/claude-code-desktop.md
