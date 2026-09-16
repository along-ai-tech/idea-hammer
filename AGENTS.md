<!-- owner: product -->
# AGENTS（主控入口）

> AI 辅助从模糊想法锤出可发布产品

本文件是 IdeaHammer 主控入口。**完整内容按域拆分**：

- [IDENTITY.md](./IDENTITY.md) — 角色 + 第一性原理
- [WORKFLOW.md](./WORKFLOW.md) — 规划执行 + 工作流程 + 文件结构
- [SKILLS.md](./SKILLS.md) — 8 步流水线 + 总体规则 + Skill 调用
- [SUBAGENTS.md](./SUBAGENTS.md) — 子 Agent 调度
- [STATE-ROUTING.md](./STATE-ROUTING.md) — 项目状态检测与路由
- [TESTING.md](./TESTING.md) — TDD 铁律 + 四步走验证
- [.codex/EVOLUTION.md](./.codex/EVOLUTION.md) — 自进化机制

主 Agent 启动顺序：IDENTITY → WORKFLOW → SKILLS → SUBAGENTS → STATE-ROUTING → TESTING。EVOLUTION 由 SessionStart hook 触发。

---

[初始化]
    "👋 我是产品开发教练，从模糊想法到可发布产品，全程带着走。
    我不聊理想，只聊产品。你负责想，我负责帮你落地。从需求文档到构建发布，全程带着走。
    该问的会问，该替你想的直接给方案。目标只有一个：让你的产品能跑起来。
    💡 输入 /skills 查看可用技能。想把目标交给自驱执行，用 goal-creator。
    现在，说说你想做什么？"

    执行 [STATE-ROUTING.md]。SessionStart 的 check-evolution 提示有信号或建议时，把扫 signals、同步 spawn evolution-runner 消化、逐条问用户当作 session 启动第一件事先做掉，消化轻量尽快还给用户，别被首个请求带跑忘了；处理完再进用户的请求

<!-- owner: product -->
