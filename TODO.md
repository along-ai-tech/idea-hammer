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

> **2026-11-26 更正**：advisory / transform / retry 三种模式是框架自造的，Codex 从来没加载过——
> 它解析 `hooks.json` 时遇到 `$version` / `events` / `mode` 这些字段会直接报
> `unknown field`，然后丢弃整个文件，所有 hook 静默失效。现已全部改成 Codex 真实 hook 协议，
> 详见 [`docs/codex-hooks.md`](docs/codex-hooks.md)；三模式语义不存在，勿再参考。

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

**进展（2026-11-27）**：PR 检查部分已覆盖——契约测试、skill 结构 strict 校验、
`check_simplicity` 门禁、需求追踪链路、Spec 四要素、session 校验，
另加一条隔离安装冒烟（装到临时目录 + 断言五类产物 + hook 信任条目）。
**剩余**：自动 release workflow（打 tag → 建 release → 发 changelog）。

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

**v0.11.0 起追加锁定项**：`schemas/session.schema.json` 的 `checkpoints` 数组字段一并纳入 v1.0 稳定 API 范围（checkpoint 结构一旦被下游依赖就不能随意改；新增字段只追加不重命名）。

---

## ✅ v0.11.0 已完成（2026-11-26）

### TODO-110：Day9「AI Coding 工程化」缺口补齐（D-016）

**目标**：拿 Day9 第四模块的七个知识域逐条比对框架现状，把"教纪律但没给规则"的部分补成可执行工程约束。

**诊断结论**：

| 知识域 | 现状 |
|---|---|
| TDD / Anti-Reinvent / Simplification / 独立 Code Review / Task Decomposition / Multi-Agent | ✅ 已落地，质量高 |
| **Context Engineering** | ❌ 整域零覆盖（`rg` 全仓库 0 命中） |
| Checkpoint | ❌ 概念缺失（Checkpoint ≠ Git Commit 未被区分） |
| 跨 Session 恢复 | ⚠️ 只做产物存在性检测，不核实代码与测试真实性 |
| Plan / Agent Mode | ⚠️ 无按规模与风险分流的判据 |
| Agentic Coding 闭环 | ⚠️ 无 Human-in-the-loop 停手判据 |
| Testing Pyramid | ⚠️ 缺 Contract / Regression 分层，无并发不变量门禁 |

**详细任务**：

1. ✅ **CONTEXT.md 域文件**：7 类上下文 + Context Selection 判据 + 三种技术（Retrieval / Progressive Disclosure / Compression）+ Memory/State/Checkpoint 三分工 + 上下文预算 + 恢复协议
2. ✅ **`dev-builder/principles/context-engineering.md`**：6 层渐进式装配顺序、该读/不该读对照表、压缩触发与不可丢项、checkpoint 落盘命令
3. ✅ **`dev-builder/principles/test-pyramid.md`**：五层验证映射 + 并发不变量三件套门禁 + Invariant vs Regression
4. ✅ **`scripts/session.py checkpoint` / `restore`**：记录恢复点、输出待核实清单
5. ✅ **接线**：AGENTS.md 启动顺序 / WORKFLOW.md 模式分流 + 停手判据 / STATE-ROUTING.md 恢复核实 / dev-builder SKILL + workflows / code-review stage2
6. ✅ **契约测试**：test_context_engineering.py（19 项）+ test_session_checkpoint.py（9 项）

**验收标准**：

- [x] Context Engineering 整域落地，不再是隐性纪律
- [x] Checkpoint 与 Git Commit 职责分离，恢复时强制核实
- [x] Plan/Agent 模式分流与停手判据写入 WORKFLOW
- [x] 测试金字塔五层映射 + 并发不变量门禁写入 stage2
- [x] `python3 -m pytest tests/ -q` → 269 passed（本批次新增 60 项契约测试）
- [x] `python3 scripts/check_simplicity.py scripts/` → 全部通过
- [x] `python3 scripts/check_skill_structure.py` → 12 skill 全 OK
- [x] 独立 code-reviewer 两阶段审查 → Spec Compliance ✅ / Code Quality 的 4 个 Important 全部修完

**依赖**：无（横切关注点，不新增流水线环节）

**详见**：D-016 决策记录

---

## ✅ v0.12.0 已完成（2026-11-27）

### TODO-111：全局安装——所有 Codex 项目都用上这套方法论（D-017）

**目标**：装一次，**用户电脑上所有 Codex 项目**自动生效，不用每个项目手动配置。

**诊断结论**：

| 问题 | 现状（修复前） |
|---|---|
| hook 协议 | 框架自造的 `$version` / `events` / `mode` —— Codex 从来没加载过，解析失败后丢弃整个文件，**所有 hook 静默失效** |
| hook 信任 | Codex 对用户级 hook 默认判 Untrusted，不登记 `trusted_hash` 就不执行 |
| 路径模型 | `--codex-home` 不带动 `--framework-home`，自检必须先动真实 `~/.codex` |
| 自动化 | CI 从未装过全局安装器，安装器零测试覆盖 |

**详细任务**：

1. ✅ **安装器**：`scripts/global_install/`（paths / framework / hooks / trust / agents / commands / cli），五个子命令 install / sync / status / uninstall / project
2. ✅ **协议对齐**：`.codex/hooks.json` 全部改成 `openai/codex` `rust-v0.171.0` 真实格式；`schemas/hook-protocol.schema.json`（draft-07，比 Codex 严）；`docs/codex-hooks.md`（8 章）
3. ✅ **信任登记**：安装器算好 `trusted_hash` 写进 `config.toml`（全局 2 条 + 仓库 6 条）
4. ✅ **路径锚点**：`--codex-home` 带动框架副本与技能目录；`_register_repo_hooks` 改用 `paths.source`
5. ✅ **契约测试**（22 项，拆三个文件）——装齐 / 不越界 / 可重复 / 可卸载
6. ✅ **CI**：隔离安装冒烟 + `check_simplicity` 门禁

**验收标准**：

- [x] 干净克隆 → 一条命令 → 五类产物齐全、8 条信任条目、hooks.json 过协议 schema
- [x] 隔离安装不碰真实 `~/.codex`（`--codex-home` 传临时目录）
- [x] 重复安装不产生重复内容（全局 AGENTS.md 区块幂等）
- [x] `python3 -m pytest tests/contract/ -q` → 292 passed
- [x] `python3 scripts/check_simplicity.py scripts/` → 全部通过

**依赖**：无（横切关注点，让既有 8 步流水线在任意项目里可用）

**详见**：D-017 决策记录

---

## 状态统计

- **P0 完成**：3 项（TODO-003 / 004 / 005）全部 ✅
- **P1 完成**：5 项（TODO-101/102/103/104/105）全部 ✅
- **v0.11.0 完成**：1 项（TODO-110 上下文工程域）✅
- **v0.12.0 完成**：1 项（TODO-111 全局安装）✅
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
