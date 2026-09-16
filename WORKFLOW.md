<!-- owner: architecture -->
# WORKFLOW

规划与执行模式、工作流程、文件结构三部分。

[规划与执行]
    所有环节同一个模式：主 Agent 先写规划，再自驱执行到达标。需求、设计、计划、开发、审查、发布都适用，不止开发。

    规划：主 Agent 自己把要做的事拆成有序、可独立验收的步骤，每步写明目标和完成标准。

    执行方式，按工作可隔离的程度选一种：
    - 主 Agent 直做：步骤少、彼此耦合，或要和用户来回对话的环节
    - 主 Agent 并行直做：步骤多、互不依赖，但要共享同一份上下文
    - 显式 spawn 子 Agent 并行：步骤能隔离、需要 fresh 上下文或独立判断。Codex 只在主 Agent 显式请求时 spawn，每个子 Agent 一个 fresh 实例，主 Agent 把完整上下文复制过去并合并结果

    执行标准，无论哪种方式都要做到：
    - 上下文自带：执行前自己把相关原文读进来，不靠记忆和摘要；spawn 子 Agent 时把完整上下文复制给它
    - 结果自检：拿产出对照完成标准，用证据说话，不用"应该没问题"
    - 排障自驱：没达标就自己定位、修、重验，循环到达标；同一问题反复卡住才停下来找用户

    有依赖的步骤按序执行，无依赖的并行，并行时不碰同一文件，冲突由主 Agent 合并。
    默认主 Agent 执行，关键节点回用户。要把整个目标交给自驱执行，用 goal-creator 生成指令交用户发送。

[工作流程]
    串联靠产出物：每个环节消费上一环节的产出，生成自己的产出，下一环节凭它启动。环节能不能跑看输入产出物在不在，由各 Skill [依赖检测] 把关。[项目状态检测与路由] 管入口在哪，这里管谁交接给谁。

    第一步 · 需求收集
        用户说出想做什么，你用 product-spec-builder 追问到底，把模糊想法变成可开发的 Product-Spec，完成后进入设计规范或开发计划。

    第二步 · 设计规范
        基于 Product-Spec，用 design-brief-builder 定下视觉方向，产出 Design-Brief，可选；定完进设计图或开发计划。

    第三步 · 设计图
        拿着 Product-Spec 和 Design-Brief，用 design-maker 通过设计工具生成整套设计稿，可选；出图后进开发计划。

    第四步 · 开发计划
        基于 Product-Spec，有 Design-Brief 或设计稿就一起带上，用 dev-planner 拆出分阶段的 DEV-PLAN，然后进项目开发。

    第五步 · 项目开发
        照着 Product-Spec 和 DEV-PLAN，有 Design-Brief 或设计稿就一并参照、UI 以设计稿为准，用 dev-builder 按 Phase 逐步写出项目代码，然后进审查或发布。

    第六步 · 构建发布
        项目代码就绪后，用 release-builder 打包或部署成发布产物，到此完成。

    各 Skill 的内部标准、验收、循环细节，以对应 SKILL.md 为单一真相源，本文件不复述。完成一个环节引导用户进下一个，要把整段目标交给自驱执行用 goal-creator。

    按需横切触发，不属于流水线：
    Bug 修复：报 bug 或 code-review 失败 → bug-fixer → 修完建议 code-review
    代码审查：功能完成自动进 review→fix，或主动审查 → spawn code-reviewer → Stage 1 失败回 dev-builder，Stage 2 质量重构回 dev-builder、缺陷安全回 bug-fixer，重派从 Stage 1 起
    内容修订：按改动量级判断，轻改直接 dev-builder，涉及需求或结构才回 product-spec-builder 和 dev-planner 迭代
    本地运行：用户说"跑起来" → 检测类型、装依赖、启动，给地址和用法

[文件结构]
    project/
    ├── Product-Spec.md / Product-Spec-CHANGELOG.md   # 需求文档 + 变更记录
    ├── Design-Brief.md                                # 设计规范，可选
    ├── DEV-PLAN.md                                     # 分阶段开发计划
    ├── <project-name>/                                 # 项目代码，以项目名命名的子文件夹
    ├── AGENTS.md                                       # 主控，本文件
    ├── .agents/
    │   └── skills/                                     # 各阶段能力模块（SKILL.md + references/ + assets/）
    └── .codex/
        ├── hooks.json                                 # 事件驱动的确定性门禁
        ├── hooks/                                     # hook 脚本本体
        ├── agents/                                    # code-reviewer.toml、evolution-runner.toml
        ├── evolution/                                 # 自进化，signals 队列 + proposals 建议
        └── EVOLUTION.md                               # 进化引擎说明

<!-- owner: architecture -->
