# Backlog / 待办清单

按优先级排序。每个待办含：目标、详细任务、验收标准、依赖、工时。

---

## 🔴 P0（必做，1-3 周内）

### TODO-003：拆 Skill 模板（三层结构）

**目标**：8 个 skill 从 markdown 大文件改为"行为契约"，使规则单点定义、行为可断言。

**详细任务**：
1. ✅ 阶段 1（commit `3f253a0`）：写 `agents/skills/_template/` 模板 + `scripts/check_skill_structure.py` 校验脚本（实际 .py 而非 .sh，bash 3.2 处理 UTF-8 字节有 bug）
2. ✅ 阶段 2（commit `c8c6ec5`）：dev-builder 拆三层结构样板（135 → 33 行 + 15 文件）
3. ✅ 阶段 3（commit `af79049`+`1198c9f`+`915f0fa`+`d0500ec`+`745558d`+`fffa333`+`8f29866`）：11 skill 全部三层结构
4. ✅ 阶段 4：收尾（132 契约测试全绿）

**三层结构**：
```
skill-name/
├── SKILL.md          # < 50 行，仅 description + 引用列表
├── principles/       # 第一性原则（可被多 skill 引用）
├── workflows/        # 执行流程
└── contracts/        # 输入输出 schema（机器可解析）
```

**验收标准**：
- 8 个 skill 全按新结构组织
- SKILL.md ≤ 50 行
- 跨 skill 原则（≥ 2 处引用的）抽到 principles/，去重率 ≥ 80%
- 8 个 contracts/*.schema.json 全部合法 JSON Schema
- 知识保留率 ≥ 95%（diff 校验）

**依赖**：P0-3（AGENTS.md 拆分）✅ 已完成

**完成时间**：实际 1 个 session 内全部完成
**验收**：11 skill 全部 [PWC] + 132 契约测试全绿

**详见**：之前的"改进 #2 拆 Skill 模板"规划文档。

---

### ✅ TODO-004：Session State 持久化（commit `ffe1d9f`）

**目标**：解决"启动慢 + 跨 session 不记忆"两个硬伤。

**详细任务**：
1. 设计 `.idea-hammer/session.json` schema
2. 写主 Agent 启动读取逻辑（替代当前"扫全目录"）
3. evolution-engine 写 Session State 维护逻辑
4. 主 Agent 每次关键决策后更新 session.json

**session.json 字段**：
```json
{
  "current_phase": "Phase X / Y",
  "current_task": "T-N 描述",
  "key_decisions": ["D-001 IdeaHammer 命名", "..."],
  "open_questions": ["..."],
  "user_preferences": {"tech_stack": "Python+Vue3"}
}
```

**验收标准**：
- 启动 token 降低 ≥ 30%（不重读所有 SKILL.md）
- 跨 session 决策摘要保留
- 关键决策历史可追溯

**依赖**：无（独立模块，可与 TODO-003 并行）

**工时**：2 周

**详见**：改进 #7 Session State 持久化。

---

### ✅ TODO-005：Skill 契约测试（commit `087c46f`）

**目标**：让 IdeaHammer 自己的 skill 行为可被 TDD 验证，解决"框架说 TDD 但不测"的自相矛盾。

**详细任务**：
1. 为 8 个 skill 写契约测试（输入 fixture + 期望行为 + 验证方式）
2. 加到 CI：每次 PR 自动跑契约测试
3. 契约测试覆盖 TDD 纪律、Skill 调用规则、错误处理

**验收标准**：
- 8 个 skill 全有契约测试
- CI 卡门：契约失败 = 拒绝合并
- TDD 纪律（无失败测试不写生产代码）可被自动校验

**依赖**：TODO-003（拆 Skill 模板，contracts/ 目录存在后才能写契约）

**完成时间**：实际 1 个 session 内全部完成
**验收**：11 skill 全部 [PWC] + 132 契约测试全绿

**详见**：改进 #9 Skill 契约测试。

---

## 🟡 P1（应该做，1-3 个月内）

### ✅ TODO-101（commit `7220fdc + 后续`）：流水线改图状

**目标**：8 步强顺序流水线改为路由图，支持 spike / refine / 并发。

**候选**：
- 保持 8 步顺序
- 改为路由图（graph 替代 pipeline）
- 引入 LangGraph 作为编排器

**决定**：✅ 路由图方案

**理由**：真实工作是图状（spike / refine / 并发），线性 pipeline 适合教学不适合实战。

**工时**：4-6 周

**详见**：改进 #1 流水线改图状。

---

### ✅ TODO-102（commit `2288fe4`）：Skill 触发升级为意图分类

**目标**：用意图分类器替代 description 关键词匹配。

**工时**：3-4 周

**详见**：改进 #4 意图分类。

---

### ✅ TODO-103（commit `9f0590b`）：Hook 协议升级

**目标**：advisory / transform / retry 三种模式。

**工时**：2 周

**详见**：改进 #5 Hook 协议升级。

---

### ✅ TODO-104（commit `e2ab23f`）：Evolution 三层捕获

**目标**：从被动入队升级为三层捕获（显式 / 隐式 / 效果）。

**工时**：2 周

**详见**：改进 #6 Evolution 三层。

---

### ✅ TODO-105：P1 业务纪律体系（2026-09-24）

**目标**：补 IdeaHammer 在"竞品分析、商业可行性、多视角评审"上的空白。防"做完发现没人要 / 方向错 / AI 改代码影响上下游"。

**详细任务**：

1. ✅ **Phase 0 商业可行性快筛**：`business-context-check.md`（77 行）
   - 5 问：用户已付出 / 凭什么你 / 1 年后死在哪 / 变现 / 大厂下场
   - 和 scope-discipline "不问商业化" 不冲突——只问"值不值得"不问"怎么变现"
2. ✅ **Phase 1.5 竞品扫描**：`competitive-scan.md`（53 行）+ Spec 模板 1.6 节
   - ≥ 2 直接竞品 + ≥ 2 替代方案 + 每行必填"我们凭什么"
3. ✅ **Phase 3.5 pre-mortem**：question-bank 加新维度
   - 3 个失败原因 + 概率最高那个的"提前发现信号"
4. ✅ **收尾多视角自检**：`ceo-lens.md` + `eng-lens.md` + `qa-lens.md`（共 215 行）
   - 主 Agent 显式戴 3 顶帽子过自检，不 spawn subagent
   - 漏掉的进 Spec 10.2 待确认表
5. ✅ **业务实体版本化与不可变**：`versioning-and-immutability.md`（75 行）
   - 接用户上轮"AI 改商品信息把老订单也改了"问题
   - 价格/规格/规则/权限字段必 version，禁止 UPDATE 覆盖
   - dev-builder 启动必读 + code-review Stage 2 必查
6. ✅ **接线**：
   - phase-discipline.md：加 Phase 0/1.5/3.5/收尾映射表
   - SKILL.md：引用列表加 5 个新原则
   - workflow-0-1.md：Phase 0 加 5 问 + 加 1.5 + 加 3.5 + 加收尾
   - workflow-iteration.md：跳过规则汇总
   - dev-builder/engineering-constraints.md：database 主题加 versioning + 反模式自检卡门
   - code-review/stage2-checklist.md：加"版本化与不可变"必查项 + 多视角自检衔接段

**验收标准**：
- 6 个新文件 / 约 600 行（轻量）
- 接线改动 < 10 处，每处 < 5 行
- Spec 模板只加 1.6 节一表，不膨胀
- 借鉴 gstack adversarial planning gauntlet（office-hours + ceo/eng 视角）

**依赖**：无

**工时**：1 session

**详见**：D-009 决策记录

---

## 🟢 P2（锦上添花，6 个月+）

### TODO-201：英文版 README

**目标**：海外传播。

**工时**：1 周

---

### TODO-202：CI 自动化

**目标**：PR 检查 + 自动 release workflow。

**工时**：1 周

---

### TODO-203：Sub-Agent dag 编排

**目标**：从手动 spawn 升级为 dag 编排。

**工时**：3-4 周

**详见**：改进 #8 Sub-Agent dag。

---

## 🔵 v1.0 路线（稳定 API + 向后兼容承诺）

### TODO-301：API 稳定化

**目标**：8 个 skill 的 description + contracts 锁定为 v1.0 API，向后兼容。

**工时**：4 周

---

## 状态统计

- **P0 完成**：3 项（TODO-003 / 004 / 005）全部 ✅
- **P1 完成**：5 项（TODO-101/102/103/104/105）全部 ✅
- **P2 待办**：3 项，总工时 5-6 周
- **已完成 P0**：2 项（TODO-001 拆 AGENTS.md ✅ / TODO-002 README 30 秒扫视 ✅）
- **已完成 P1 业务纪律**：TODO-105 ✅（2026-09-24）
- **已完成简化**：TODO-401 ✅（代码简洁之道 10 条）

---

## 进度更新规则

每次新完成一项，更新本文件：
1. 把该 TODO 从对应优先级区移到「已完成」区
2. 加完成日期和 commit hash
3. 更新顶部「当前状态」段落
