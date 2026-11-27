# 关键决策记录（Decision Log）

每个决策记录"为什么这样选"，让换同事/换电脑时能理解历史决策，避免重蹈覆辙。

---

## 2026-11-27

### D-017：v0.12.0 全局安装——Codex 真实 hook 协议 + 信任登记 + 路径锚点

**背景**：v0.11.0 之后，用户的目标从"框架能用"变成"**所有 Codex 项目都能用**"。
要做到这点，安装器必须一次装齐五类产物，并且装出来的 hook 真的会被 Codex 执行——
而不是"文件在那儿，看着挺像"。

自检时挖出三个真问题：

1. **hook 协议是框架自造的，Codex 从来没加载过。** 仓库里的 `hooks.json` 用了
   `$version` / `events` / `mode`（advisory / transform / retry 三模式），
   Codex 解析时遇到未知字段直接丢弃整个文件——所有 hook 静默失效，不报任何错。
   按 `openai/codex` `rust-v0.171.0` 源码核对后，真实格式是
   `{description, hooks: {事件名: [MatcherGroup]}}`，顶层 `deny_unknown_fields`。
2. **hook 信任机制此前完全没被处理。** Codex 对用户级 hook 默认判 Untrusted，
   不在 `config.toml` 写 `[hooks.state."<key>"] trusted_hash` 就静默不执行。
   信任 key 的哈希算法（规范化 handler → 递归排序键的紧凑 JSON → sha256）
   是从 Codex 源码复刻的。
3. **安装器的路径模型有耦合缺陷。** `--codex-home` 不会带动 `--framework-home`，
   想自检就得先动真实的 `~/.codex/idea-hammer`；而且 `_register_repo_hooks`
   硬编码 `REPO_ROOT`，`--source` 形同虚设。
4. **Codex 的三条路径各走各的，不能互相推导。** 探针实验（同名探针技能分别放两处）
   证明：技能根**只认 `$HOME/.agents/skills`**，不认 `$CODEX_HOME/../.agents/skills`；
   `CODEX_HOME` 只决定配置目录。把技能目录跟着 `--codex-home` 走，
   会让自定义 `CODEX_HOME` 的用户整套技能静默失效。

**候选**：

- A. 保留自造协议，加一个"协议转换器"把框架格式转成 Codex 格式
- B. 直接对齐 Codex 真实协议，框架侧只保留一份 schema
- C. 放弃 hook，只靠全局 AGENTS.md + 技能目录生效

**决定**：B 方案

**理由**：

- A 等于长期维护两套协议 + 一层翻译器，而错误的信号是"静默失效"——
  最难发现的一种失败。既然真实协议可查可抄，就没有理由再造。
- C 砍掉的正是进化机制（signals 捕获与 session 启动提醒），
  而自进化是框架的差异化能力之一，不该为了省事丢掉。
- B 让"装了就真的在跑"成为可验证的事实：装完能立刻用
  `codex debug prompt-input "hi"` 看到全局 AGENTS.md 与 12 个技能命中。

**落地**：

| 层 | 产物 | 作用 |
|---|---|---|
| 协议 | `.codex/hooks.json` | 全部改成 Codex 真实格式；`mode` / `$version` / `events` 作废 |
| schema | `schemas/hook-protocol.schema.json` | draft-07，比 Codex 更严（未知字段即报错） |
| 文档 | `docs/codex-hooks.md` | 8 章，含信任机制、stdout 语义、常见错误 |
| 工具 | `scripts/global_install/` | 装齐五类产物 + 登记 hook 信任 |
| 路径 | 三条路径各按 Codex 规则 | 配置 → `~/.codex`（或 `$CODEX_HOME`）；技能 → `$HOME/.agents/skills`；框架副本 → 配置目录旁 |
| 门禁 | 3 个安装器契约测试文件 + CI 冒烟 | 22 项契约 + 每次 CI 装一遍到临时目录 |

**关键取舍**：

1. **全局只装 2 条安全 hook**（进化信号捕获 + session 启动提醒）。
   `stop-gate`（拦截未审代码）、`auto-push`（自动推送）、`auto-lint`（改用户文件）
   会改变所有仓库的行为，默认不装，需要时用 `project <dir>` 单独开启。
2. **技能用复制而不是符号链接**：技能之间有跨目录相对引用
   （`code-review/principles/../../dev-builder/...`），链接安装后这些路径在推理层会解析到别处。
3. **信任登记归安装器管**：用户不该需要手算 sha256。安装器算好写进 `config.toml`。
4. **schema 比 Codex 严**：Codex 静默忽略未知字段，本 schema 直接判错——
   拼错要当场发现，而不是装出一份死配置。
5. **路径不互相推导**：三条路径各自遵守 Codex 的规则。技能的落点由 `$HOME` 决定，
   配置落点由 `CODEX_HOME` / `--codex-home` 决定，框架副本跟着配置走。
   要完全隔离的安装，把 `HOME` 指到临时目录——三条路径会一起跟着走。

**影响**：

- TODO-103 的"三模式协议"正式作废，`TODO.md` 已加更正说明。
- `docs/codex-hooks.md` 与 `schemas/hook-protocol.schema.json` 成为 hook 的唯一真相源；
  Codex 升级若改协议，先跑 `tests/contract/test_global_install.py`。
- v1.0 的 API 稳定化（TODO-301）应把 `hooks.state` 信任 key 的格式也纳入承诺范围——
  改了 key 格式，老用户的 hook 会静默不执行。

---

## 2026-11-26

### D-016：v0.11.0 上下文工程域 + 跨 Session 恢复（补 Day9 AI Coding 工程化缺口）

**背景**：v0.10.0 打通需求追踪后，做了一次框架自检——拿 Day9「AI Coding 工程化」的七个知识域逐条比对项目现状。结果：

- TDD、Anti-Reinvent、Simplification、独立 Code Review、Task Decomposition、Multi-Agent 已落地且质量高
- **Context Engineering 整域零覆盖**：`rg -il "context engineering|渐进式加载|上下文压缩"` 全仓库 0 命中
- Checkpoint 概念缺失：`rg -il checkpoint` 只命中无关文件
- 恢复流程只做"产物在不在"的文件存在性检测，不核实代码与测试真实性
- Plan / Agent Mode 无按规模与风险分流的判据；Human-in-the-loop 停手判据只散落一句
- 测试金字塔缺 Contract / Regression 分层，无并发不变量门禁

根因判断：框架一直在教「先读原文、不凭记忆」，但**从没定义该读什么**。这是长任务上下文膨胀的源头——不是纪律不够，是缺一个可操作的上下文选择规则。

**候选**：

- A. 只补一份 CONTEXT.md 文档，讲清概念
- B. CONTEXT.md + 可执行门禁（checkpoint 工具 + 契约测试 + skill 接线）
- C. 新建一个 context-engineer skill，走 8 步流水线加一环

**决定**：B 方案

**理由**：

- A 不符合本仓库"把模糊审美判断转成可检查指标"的一贯做法（simplification、traceability 都是这么做的），纯文档写完就无人执行。
- C 过度：上下文管理是横切关注点，不是流水线上一环。塞进流水线会破坏"8 步"的清晰结构，也会和 SKILLS.md 的职责边界打架。
- B 保持横切关注点用**根域文件**承载（与 TESTING.md 平级），细则下沉到 dev-builder 的 principles，工具落到 scripts，纪律落到契约测试。四层各有落点，不新增流水线环节。

**落地**：

| 层 | 产物 | 作用 |
|---|---|---|
| 域 | `CONTEXT.md` | 7 类上下文 / Context Selection / 三种技术 / Memory-State-Checkpoint 分工 / 恢复协议 |
| 原则 | `dev-builder/principles/context-engineering.md` | Task 启动的 6 层渐进式装配顺序、该读/不该读表、压缩触发与保留项 |
| 原则 | `dev-builder/principles/test-pyramid.md` | Unit/Integration/Contract/E2E/Regression 五层映射 + 并发不变量三件套门禁 |
| 工具 | `scripts/session.py checkpoint` / `restore` | 记录恢复点、输出待核实清单 |
| 门禁 | `tests/contract/test_context_engineering.py` / `test_session_checkpoint.py` | 概念必现 + 工具行为可执行验证 |
| 接线 | AGENTS.md / WORKFLOW.md / STATE-ROUTING.md / dev-builder SKILL + workflows / code-review stage2 | 域文件进启动顺序；模式分流与停手判据进 WORKFLOW；恢复核实进 STATE-ROUTING |

**关键取舍**：

1. **Checkpoint ≠ Git Commit**：Checkpoint 记任务恢复信息（做到哪、测试证据、下一步、关联产物），Git Commit 管代码版本。两者可关联，职责不同。恢复时用 `session.py restore` 拿到位置，但**不轻信其中的测试结论**——代码变过就重跑。
2. **Context 是按任务选，不是按项目大小选**：不引入向量库。代码搜索 + 符号索引已足够，且引入 RAG 会让框架复杂度陡增。
3. **压缩保留"索引"而非"细节"**：Spec / Plan / 源码永远可重读，所以压缩时保留"在哪、是什么"，细节丢了能重读。永远保留验收标准、已确认决策、验证证据。
4. **不新增流水线环节**：横切关注点用根域文件 + skill 细则承载，保住"8 步流水线"的清晰边界。
5. **"四步走验证"保持四步**：持久化进度是验证**之后**的收尾动作，不算第 5 步验证，避免与 TESTING.md 的铁律冲突。

**影响**：

- 后续 D-017+ 若涉及"AI 自主性"扩展，CONTEXT.md 的"停手问人判据"是唯一真相源。
- `session.json` 新增 `checkpoints` 数组，为 1.0 稳定 API 预留（TODO-301 需把该字段纳入锁定范围）。

---

## 2026-10-02

### D-013：v0.9.0 subagent 任务循环（SDD）+ 代码纪律补强

**背景**：v0.8.0 解决了"spec 出得更可执行"（D-012）。剩两个悬而未决：

1. 大 DEV-PLAN（≥5 独立 Phase 任务）一次性干完风险高：implementer 跑歪、中途换上下文、review 只在终审看，返工面巨大。
2. 代码层纪律分散：bug-fixer 流程不显式、code-review 输出没两段契约、dev-builder 任务循环无 fix-loop 上限、dev-planner 不做 subagent 模式路由。

参考 superpowers:subagent-driven-development 的核心机制（任务级 fresh subagent + 两段 review + judgment ledger），结合本仓库约束（不破坏现有 dev-builder / code-review 闭环），落到 v0.9.0。

**候选**：

- A. 全盘照搬 superpowers:subagent-driven-development 模板（spec-test-mvp / process-tasks / process-review 等 13 份模板 + 4 个 subagent 类型）
- B. 只借鉴核心机制，自建轻量 SKILL + 5 文件代码纪律补强
- C. 只做纪律补强，不做 SDD

**决定**：B 方案

**理由**：

- A 模板 13 份过长（合计数千行），且与本仓库阶段式执行风格不匹配；强塞会破坏 dev-builder 主导路径。
- C 只补纪律不够：大 DEV-PLAN 风险不解决。
- B 是最小可工作集：1 个 SKILL（45 行）+ 1 个 workflow（87 行）+ 3 个 shell 脚本 + 5 个纪律补强文件，闭环建立且不膨胀。

**4 个待决项的最终处理**：

| # | 待决 | 决定 |
|---|---|---|
| 1 | task 标题格式 | 接受硬匹配 `### Task N:`。task-brief.sh 用 awk 匹配，Plan 模板自身规范 |
| 2 | base/head 来源 | 主 Agent 在 1.2 dispatch 前 `git rev-parse HEAD` 记录，作为参数传入 review-package.sh |
| 3 | breaker 谁执行 | reviewer subagent 报出"breaker tripped"，主 Agent 在循环间统一收集并仲裁（park / rule / stop） |
| 4 | workspace 清理 | 合账前 `cp progress.md` 到 `.idea-hammer/sdd-archive/<plan-id>-progress.md`（不入 gitignore 永久留底），然后 `rm -rf` workspace |

**借鉴但不照搬**：

- 借鉴：fresh subagent 隔离 / 两段 review / 5 轮 fix loop / judgment ledger / breaker 机制
- 不照搬：spec-test-mvp 三件套（用现有 Product-Spec 已含 TDD 纪律）/ 分支策略（沿用仓库 direct-commit-on-master）/ 多个固定 subagent 类型（只复用 code-reviewer）

**代码纪律补强 5 文件**：

1. `agents/skills/bug-fixer/workflows/debug.md`：4 阶段升级三级标题 + 卡门段 + 退出条件 + 阶段间回退
2. `agents/skills/code-review/principles/review-discipline.md`：加两段输出契约（Spec Compliance 二元 + Code Quality 二元 + Finding 分级）
3. `agents/skills/dev-builder/principles/engineering-constraints.md`：加"任务级 fix loop 与 SDD 路由"段
4. `agents/skills/dev-planner/SKILL.md`：加"路由:subagent 模式选择"段（≥5 走 SDD / <5 走 dev-builder / 强耦合不切）
5. `SUBAGENTS.md`：结构化为"固定 Sub-Agent / 调度纪律 / v0.9.0 起 SDD 模式"三段

**影响**：

- v0.9.0 起：大 DEV-PLAN（≥5 独立 Phase 任务）自动走 SDD，其他照旧走 dev-builder。
- code-review 输出契约升级：两段 verdict 成为强约束，主 Agent 不接受单一"通过/不通过"。
- 5 轮 fix loop 上限进入 dev-builder 任务循环（不强制 fresh subagent）。
- D-014 留位：v1.0.0 运行时验证 / 自进化机制完善。

---

## 2026-09-30

### D-012：v0.8.0 PRD 吸收 + spec 纪律补强

**背景**：参考 PRD（prd-standard.md）含可借鉴的"AI 一次写对"纪律元素；结合 v0.7.0-dev 业务纪律路线，把 spec 层纪律补到位。

**候选**：
- A. PRD 10 条全吸收 + 纪律 3 文件全进 v0.8.0
- B. PRD 8 条 + 纪律 3 文件进 v0.8.0
- C. PRD 8 条单独进 v0.8.0，纪律进 v0.9.0（用户拍板）

**决定**：C 方案

**理由**：A 膨胀 v0.8.0；B 纪律补强不在 spec 层不应混；C 划界清晰——v0.8.0 解决"spec 出得更可执行"，v0.9.0 解决"subagent 循环与代码纪律"。

**PRD 不采的 2 条**：菜单层级（绑死 UI）、菜单路径分组（同上）。

**借鉴 superpowers/gstack 但不进 v0.8.0**：subagent 任务循环、judgment ledger、auto-fix 二元、3+fix 架构门——统一进 v0.9.0。

**影响**：v0.8.0 spec 层纪律上线；D-013 / D-014 留位。

---

## 2026-09-24

### D-009：P1 业务纪律体系（防方向错 + 防遗漏 + 防上下游影响）

**背景**：用户洞察 IdeaHammer 在三方面缺纪律：
1. 竞品分析 / 商业可行性 / 多视角评审——做完发现没人要 / 方向错
2. AI 改业务数据（价格/规格/规则）会把老订单也改了——上下游影响
3. Spec 收尾只靠主 Agent 一种视角——漏防方向错

**候选**：
- A. 重写 product-spec-builder 的 question-bank，加全套（评审 / 多视角 / 风险）
- B. 加 5 个独立轻量原则文件，主 Agent 显式戴帽子切换提示词
- C. 真的 spawn subagent 做 CEO/Eng/QA/Security 多视角（参考 gstack `plan-ceo-review`）

**决定**：B + 部分 C

**理由**：
- A 会膨胀 question-bank，违反"规则只许更精炼"原则
- B 每个文件 ≤ 80 行，6 个文件总计 ~600 行，是最小侵入式增量
- C 的子 agent spawn 太重，且没看出能比提示词切换多 catch 多少问题——先把 B 跑起来，效果不行再升级到 C
- 借鉴 gstack `/office-hours` 6 问 → 化为 Phase 0 5 问快筛（"凭什么你活"/"1 年后死在哪"等）
- 借鉴 gstack `/plan-ceo-review` `/plan-eng-review` → ceo-lens / eng-lens

**轻量化措施**：
- 不进 Spec 模板（除 1.6 节一表）
- 不 spawn subagent（提示词切换足够）
- Phase 0/1.5/3.5/收尾 迭代模式统一跳过

**和现有原则关系**：
- scope-discipline "不问商业化" 保留——我们只问"值不值得"不问"怎么变现"
- phase-discipline 7 Phase 顺序保留——Phase 0 是"之前"插入，1.5/3.5 是"之间"插入
- 模板保持原 12 节，只在 1.5 后加 1.6 竞品扫描表

**借鉴 gstack 但没抄的**：
- design-review（我们已有 design-brief-builder）
- qa（运行时浏览器交互，我们不做运行时）
- cso（已部分被 _engineering-constraints/security/ 覆盖）

**影响**：
- v0.7.0-dev 版本上线
- product-spec-builder/principles/ 加 5 个文件（~280 行）
- _engineering-constraints/database/ 加 1 个文件（75 行）
- 接线改动 < 10 处，每处 < 5 行
- 不动 SPEC 模板大结构（除 1.6 一表）
- 框架对外的卖点从"工程级约束"扩到"工程级约束 + 业务纪律"

---

## 2026-09-16

### D-008：hook 路径 bug 修复（`codex/` → `.codex/`）

**背景**：v0.3.1 收尾时发现 v0.1.1 起 hook 路径就错了 —— `hooks.json` 里 6 处 command + `hooks/*.sh` 里 4 处引用都写 `.codex/`，但实际目录是 `codex/`（创建时少打点号）。导致 5 类 hook 事件全部失效、`signals.jsonl` 永远空、自进化机制一直空转。

**候选**：
- A. `git mv codex/ → .codex/`（改目录名）
- B. 改 24 处文档/脚本引用为 `codex/`
- C. 加 symlink 兼容两边

**决定**：A 方案

**理由**：
- 24 处引用全部按 `.codex/` 写，文档也是 `.codex/`，改目录名零改动
- `.codex/` 是 Codex app 约定（`CODEX_HOME`），符合惯例
- C 方案会留下双路径歧义
- 自进化机制从 v0.1.1 起从未工作过，4 个月盲区，是这次 v0.3.1 收尾关键发现

**影响**：hook 体系首次真正生效；evolution signals 队列从空 → 真实采集。

---

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
