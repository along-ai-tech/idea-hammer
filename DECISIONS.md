# 关键决策记录（Decision Log）

每个决策记录"为什么这样选"，让换同事/换电脑时能理解历史决策，避免重蹈覆辙。

---

## 2026-09-16

### D-007：AGENTS.md 按域拆分为 6 个域文件

**背景**：原 AGENTS.md 162 行 12 章节单文件，维护性硬伤。

**候选**：
- A. 保持单文件
- B. 拆为 6 个域文件（IDENTITY / WORKFLOW / SKILLS / SUBAGENTS / STATE-ROUTING / TESTING）
- C. 拆为 12 个文件（每个原章节一个）

**决定**：B 方案

**理由**：
- 单文件改一处要重读 13KB 全文
- 12 个文件太碎，跨文件维护成本高
- 6 个域文件每个单 owner（产品/架构/工程/框架），权限隔离到位
- 是 P0-1（拆 Skill 模板）的前置：skill 调用规则要从 AGENTS.md 抽出

**影响**：P0-3 改进；P0-1 解锁。

---

### D-006：README 30 秒扫视重写

**背景**：已写入简历，技术官 + HR 30 秒内必须看懂方法论。原 272 行过长。

**决定**：重写为 128 行，顶部摘要 + 数字卡片 + 8 步流水线图前置到第 19 行。

**理由**：
- HR 看 5 秒能记住"8 skill / 56 测试 / 1 demo / MIT"
- 技术官看 30 秒能看到方法论
- 对外展示价值：简历明天就要用

---

### D-005：8 步流水线：bug-fixer 算回路不算独立步

**背景**：原 README 把 design-brief 和 design-maker 合并为"设计桥接"，实际是 2 步而非 1 步。

**决定**：8 步分明（product-spec-builder / design-brief-builder / design-maker / dev-planner / dev-builder / code-review / bug-fixer / release-builder），bug-fixer 作为 ⑦ 的回路（↺ 标记），不画在主流程上。

**理由**：
- bug-fixer 由 code-review 失败触发，不是必经步骤
- 但要在主流程图里能看到"如果失败怎么走"
- ↺ 回路标记既不漏也明确"不是必经"

---

## 2026-09-15

### D-004：P0 改进优先级排序

**背景**：框架 review 后识别 10 个改进点，需要排优先级。

**决定**：P0 = 4 项（拆 Skill 模板 / Session State 持久化 / AGENTS.md 拆分 / Skill 契约测试），其余 P1/P2 后续。

**理由**：
- 拆 Skill 模板是其他改进的基础设施
- Session State 是用户能感知的硬伤（启动慢、跨 session 不记忆）
- AGENTS.md 拆分是 Skill 拆分的前置
- Skill 契约测试解决"IdeaHammer 自己说 TDD 但不测"的自相矛盾

**已完成的 P0**：D-007（拆 AGENTS.md）。
**待开的 P0**：拆 Skill 模板、Session State、Skill 契约测试（详见 TODO.md）。

---

## 2026-09-08

### D-003：example 技术栈选 Python + Vue3 + Element Plus

**背景**：选定首个 example 项目（本地闪卡应用）作为 IdeaHammer 端到端演示。

**决定**：后端 Python 3.11+ / FastAPI / SQLAlchemy 2.0 / SQLite / Pydantic v2 / pytest；前端 Vue 3.5 / Element Plus 2.8 / Vite 5 / TypeScript strict / Pinia / Vitest。

**理由**：
- 个人技术栈匹配（AI 应用工程师背景）
- FastAPI 现代化、文档自动生成
- Element Plus 组件丰富，减少自造组件
- TypeScript strict 强制纪律
- pytest + Vitest 双端测试生态成熟

---

### D-002：项目正式名 IdeaHammer

**背景**：项目需要通用品牌名。

**候选**：
- IdeaHammer（Idea = 想法 + Hammer = 锤炼）
- SpecForge（SDD 暗合）
- IdeaToShip（端到端直白）
- ProductHammer（产品视角）
- NeedToPR（直白命名）

**决定**：IdeaHammer

**理由**：
- Idea = 起点（产端）
- Hammer = 锤炼出产品（研发端，含锻造感）
- 4 字母 + 6 字母，简洁好记
- 隐含端到端锻造全流程

**Tagline**："AI 辅助从模糊想法锤出可发布产品"

---

### D-001：品牌选择（采用 IdeaHammer）

**背景**：本项目以"产品开发教练"为角色定位，需要一个能传达"产研全流程 + 锻造感"的通用品牌名。

**决定**：采用 IdeaHammer 作为唯一品牌名，AGENTS.md 角色定义改写为"产品开发教练"。

**理由**：
- Idea = 起点（产端）
- Hammer = 锤炼出产品（研发端，含锻造感）
- 4 字母 + 6 字母，简洁好记
- 隐含端到端锻造全流程

**保留的方法论风格**：直白 / 不废话 / 主动给方案 / 追问到底 / 该嘲讽时嘲讽。
**通用化处理**：所有品牌元素（ASCII art、emoji 等）已通用化。

---

## 决策原则

新增决策时遵循以下原则：

1. **记录 Why 不只 What** —— "为什么这样选"比"选了什么"重要
2. **候选要列全** —— 至少 2-3 个备选，避免事后"为什么没考虑 X"的质疑
3. **影响要写** —— 后续决策依赖此决策的，要写明
4. **时间倒序** —— 最新决策在最上面，方便回顾
5. **不删除历史** —— 即使决策后来被推翻，也保留原条目，加 "（已废止）" 标记
