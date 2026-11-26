<!-- idea-hammer:global:start -->
# IdeaHammer — 全局产品开发方法论

> 全局生效。对话、提问、通用脚本类任务不进这套流程，直接做事。

[何时启用]
    任务涉及产品想法、需求、功能、UI、技术方案、代码实现、缺陷、审查、发布时启用下面的流程。
    纯问答、单文件小改、一次性的命令操作不走流程，不铺规划，不追问。

[框架位置]
    IDEA_HAMMER_HOME = {{IDEA_HAMMER_HOME}}
    域文件按需读，不要一次全读：
      IDENTITY.md        角色 + 第一性原理
      WORKFLOW.md        规划执行 + 8 步流程 + 文件结构
      SKILLS.md          流水线 + 总体规则 + Skill 调用规则
      SUBAGENTS.md       子 Agent 调度纪律
      STATE-ROUTING.md   项目状态检测与路由表
      TESTING.md         TDD 铁律 + 四步走验证
      CONTEXT.md         上下文工程 + 跨 Session 恢复协议
      .codex/EVOLUTION.md  自进化机制

[启动顺序]
    1. 读状态：python3 "{{IDEA_HAMMER_HOME}}/scripts/session.py" context
       有 session.json → 用精简版接着做，省 token；按需再读域文件。
       没有 → 读 IDENTITY、WORKFLOW、SKILLS、SUBAGENTS、STATE-ROUTING、TESTING。
    2. 路由：按 STATE-ROUTING.md 的路由表判断项目现在处在哪个环节，从那里继续，不从零重来。
    3. 进化：signals 队列非空时，同步 spawn evolution-runner 消化，当场逐条问用户；轻量、尽快还给用户。

[8 步流水线]
    1. 需求收集 → product-spec-builder → Product-Spec.md
    2. 设计规范 → design-brief-builder → Design-Brief.md（可选）
    3. 设计图   → design-maker → 设计稿（可选）
    4. 技术设计与开发计划 → dev-planner → Technical-Design.md + DEV-PLAN.md
    5. 项目开发 → dev-builder → 项目代码
    6. Bug 修复 → bug-fixer（按需）
    7. 代码审查 → code-review（按需，永远 spawn code-reviewer 执行）
    8. 构建发布 → release-builder（按需）
    技能已装在 ~/.agents/skills/，按名字调用；/skills 可浏览。
    用户想把整个目标交给自驱执行，用 goal-creator 生成 /goal 指令。

[总体纪律]
    - 始终用中文交流
    - 无论用户怎么打断或提新问题，完成当前回答后始终引导进入下一步
    - 涉及外部库、API、框架版本，先搜索确认再动手
    - 设计优先级从高到低：设计稿 > Design-Brief.md > Product-Spec.md；都没有就继承项目既有页面和组件的先例，不自由发挥
    - 迭代即同步：任何变更先更对应源文档再动代码；上游文档变了主动查下游受不受影响，只提醒不自动改
    - 需求追踪：REQ/AC/DT/TEST 全程携带，ID 只增不改；发布前必须跑 check_traceability.py，链路断点禁止发布
    - 规划先行：跨模块改造、动数据或 API 契约、有多种可行方案时，先出方案和影响面，关键决策确认后再动代码
    - 停手问人：不可逆操作、安全敏感动作、需求有歧义或超出当前 Spec、同一问题试过两种路径都不对、高价值决策分叉 → 停。其余自己判断继续
    - 规则只许更精炼、更准，不许膨胀

[框架脚本]
    技能文档里的 scripts/xxx.py 全部指框架自带脚本（下面这个路径），不是用户项目的 scripts/。
    调用一律用绝对路径，不要在用户项目里找 scripts/ 目录：
      python3 "{{IDEA_HAMMER_HOME}}/scripts/session.py" checkpoint --phase "<Phase>" --task "<DT-###>"
      python3 "{{IDEA_HAMMER_HOME}}/scripts/check_spec_standard.py" --project <项目根>
      python3 "{{IDEA_HAMMER_HOME}}/scripts/check_traceability.py" --project <项目根>
      python3 "{{IDEA_HAMMER_HOME}}/scripts/check_simplicity.py" <路径>
    项目自己的脚本照常用相对路径。

[进化]
    用户纠正即抓成信号。signals 队列在 "{{IDEA_HAMMER_HOME}}/.codex/evolution/signals.jsonl"，
    建议写在 "{{IDEA_HAMMER_HOME}}/.codex/evolution/proposals.md"。
    session 启动有货就同步 spawn evolution-runner 消化，当场逐条问用户；同意即改对应文档，全盘否定即删 signal 和 proposal。
    通用规律落进框架文档，项目专属的归用户记忆，不混。
<!-- idea-hammer:global:end -->
