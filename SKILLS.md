<!-- owner: framework -->
# SKILLS

8 步流水线、总体纪律、Skill 调用规则三部分。

[任务]
    引导用户走完产品开发全流程，每一步调用对应 Skill：
    1. 需求收集 → product-spec-builder → Product-Spec.md
    2. 设计规范 → design-brief-builder → Design-Brief.md，可选
    3. 设计图制作 → design-maker → 设计稿，可选
    4. 开发计划 → dev-planner → DEV-PLAN.md
    5. 项目开发 → dev-builder → 项目代码
    6. Bug 修复 → bug-fixer，按需
    7. 代码审查 → code-review，按需
    8. 构建发布 → release-builder，按需
    每个环节都先由主 Agent 写规划再执行，见 [WORKFLOW.md]。要把整个目标交给自驱执行时，用 goal-creator 生成指令。

[总体规则]
    - 无论用户如何打断或提新问题，完成当前回答后始终引导进入下一步
    - 始终使用中文交流
    - 联网优先：涉及外部库、API、框架版本时先搜索确认再动手
    - 自进化：用户纠正即抓成信号入队到 .codex/evolution/signals.jsonl，hook 靠关键词只抓措辞明显的，主 Agent 识别到 hook 没抓到的修正自己补记一条
    - Codex hook 不支持异步后台。session 启动主 Agent 第一件事：signals 有货就同步 spawn evolution-runner 消化成建议、消化轻量尽快还给用户，当场逐条问用户，同意即改对应文档、全盘否定即删 signal 和 proposal。主 Agent 照常处理用户的修正本身
    - 设计优先级从高到低：设计稿、Design-Brief.md、Product-Spec.md。有设计稿时 UI 一切以设计稿为准。无设计稿也无 Brief 时，继承项目既有页面和组件的先例，不自由发挥
    - 迭代即同步：任何变更先更对应源文档再动代码，文档是单一真相源。上游文档变了，主 Agent 主动查下游文档和代码受不受影响、要不要一起更，只提醒不自动改，不只改一个留其余脱节
    - 进化沉淀通用规则落到对应文档：编排进 AGENTS.md、技能进对应 SKILL.md、门禁进对应 hook；项目专属归用户记忆，不混

[Skill 调用规则]
    Skills 放 .agents/skills/，每个 SKILL.md 的 description 决定何时自动触发，也可用 /skills 手动浏览选用。
    匹配触发条件时，先调用 Skill 再输出响应，不要先回复再调用。
    多个 Skill 命中时，优先级：用户直接点名 ＞ 上下文最匹配 ＞ 不确定就问。

    [product-spec-builder]
        自动：用户表达产品想法，或加功能、改需求、调 UI 时进入迭代模式。
    [design-brief-builder]
        前置：Product-Spec.md
    [design-maker]
        前置：Product-Spec.md + Design-Brief.md
    [dev-planner]
        前置：Product-Spec.md
    [dev-builder]
        前置：Product-Spec.md + DEV-PLAN.md
    [bug-fixer]
        自动：用户报 bug、报错、功能异常，或 code-review 发现问题后自动修。前置：项目代码
    [code-review]
        自动：功能开发完成后自动进 review→fix，或用户要求审查。前置：Product-Spec.md + 项目代码。永远 spawn code-reviewer 执行
    [release-builder]
        前置：项目代码
    [goal-creator]
        用户想把整个目标交给自驱执行时，生成指令交用户发送
    [skill-builder]
        自动：EVOLUTION 提议新 Skill 且用户确认后。
    [evolution-engine]
        自动：session 启动主 Agent 扫 signals，有货同步 spawn evolution-runner 消化成建议、当场逐条问用户。手动：重新消化或处理待办建议。消化由 evolution-runner 做，询问和落地由主 Agent 做

<!-- owner: framework -->
