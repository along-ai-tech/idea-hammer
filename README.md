# IdeaHammer

> **AI 辅助从模糊想法锤出可发布产品** — 一个真实跑通过端到端产研流水线的工程化作品集

**给面试官的 3 分钟路径**：看一眼 [`examples/personal-blog/`](./examples/personal-blog/)（按方法论从零到一真跑的 demo）。

---

## 📊 首屏证据（3 秒看清这不是 PPT）

| 数字 | 含义 |
|------|------|
| **11 skill** | product-spec-builder / design-brief-builder / dev-builder / code-review / bug-fixer / release-builder …全 8 步流水线 |
| **172 契约测试 + 21 真实 Feature 测试** | 框架自身契约 100% + 真实案例（SM-2 学习模式）全绿 |
| **1 真实 Feature 案例** | [`examples/personal-blog/`](./examples/personal-blog/)：按 IdeaHammer 8 步流水线从零到一跑出（建设中） |
| **15 主题 / 73 文件 / ~7300 行** 工程级约束 | 编码规范 / 库选型 / 性能 / 安全 / 错误处理 / 数据库 / **simplification 10 条** / **compatibility 6 条** |
| **5 主题 / 6 文件** 业务纪律 | Phase 0 5 问快筛 / 竞品扫描 / pre-mortem / ceo-eng-qa 多视角 / 版本化与不可变 |
| **MIT** | 可商用 / 可改 / 可二次发布 |

[![CI](https://img.shields.io/github/actions/workflow/status/along-ai-tech/idea-hammer/ci.yml?label=CI&logo=github)](.github/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.7.0--dev-blue.svg)](CHANGELOG.md)
[![Main Repo](https://img.shields.io/badge/GitHub-along--ai--tech-181717?logo=github)](https://github.com/along-ai-tech/idea-hammer)
[![Gitee Mirror](https://img.shields.io/badge/Gitee-mirror-C71D23?logo=gitee)](https://gitee.com/zhilong811/idea-hammer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-贡献)

[English](./README_EN.md) · 镜像仓库：[Gitee](https://gitee.com/zhilong811/idea-hammer) · [CHANGELOG](./CHANGELOG.md) · [STATUS](./STATUS.md) · [DECISIONS](./DECISIONS.md) · [TODO](./TODO.md)

---

## 🛠️ 一句话方法论（30 秒懂）

把产品经理的纪律（反模糊、Spec 驱动）和研发的工程化（TDD、review、release、**工业级编码约束**）
合成一条端到端流水线。Codex / Claude Code 启动即用，主 Agent 自动按 8 步推进：

```
① 需求澄清 → ② Product-Spec.md → ③ Design-Brief.md → ④ 设计稿（可选）
            → ⑤ DEV-PLAN.md → ⑥ 按 Phase 开发（RED → GREEN → REFACTOR）
            → ⑦ 两阶段审查 → ⑧ 构建发布
```

---

## 📑 目录

1. [首屏证据（已在顶部）](#-首屏证据3-秒看清这不是-ppt)
2. [真实 Feature 端到端案例](./examples/personal-blog/) ← **3 分钟看这个就够了（建设中）**
3. [AI Coding 痕迹自证](./AIDER-FOOTPRINT/ai-coding-footprint.md)
4. [它解决什么问题](#-它解决什么问题)
5. [快速开始](#-快速开始)
6. [示例对话](#-示例对话)
7. [架构与组件关系](#-架构与组件关系)
8. [详细文档](#-详细文档)
9. [方法论详解](#-方法论详解)
10. [路线图](#-路线图)
11. [谁会用 / 项目目的](#-谁会用--项目目的)
12. [贡献](#-贡献)
13. [许可 & 致谢](#-许可--致谢)

---

## 🛠 方法论：8 步流水线

```
① 需求澄清（product-spec-builder）
            ↓
② Product-Spec.md  ← 单一真相源
            ↓
③ Design-Brief.md（design-brief-builder）
            ↓
④ 设计稿（design-maker）
            ↓
⑤ DEV-PLAN.md（dev-planner）
            ↓
⑥ 按 Phase 开发（dev-builder）── RED → GREEN → REFACTOR
            ↓
⑦ 两阶段审查（code-review → code-reviewer）── 失败回派
                                            ↺ bug-fixer（先写复现测试）
            ↓
⑧ 构建发布（release-builder）
            ↓
   可发布产品 ✅
```

8 步对应 8 个流水线 skill，加上 `goal-creator` / `evolution-engine` / `skill-builder` 3 个元 skill，共 **11 个 skill**。bug-fixer 由审查失败触发，作为 ⑦ 的回路。每步有独立产出物，下一步按它启动。**dev-builder / code-review 启动时强制读工程级约束**（见下）。

---

## 🤔 和同类项目有什么不同

| 项目                  | 端到端    | Spec 驱动 | TDD 强制 | 审查闭环  | **工程级约束**           | **业务纪律** | 进化机制 |
| ------------------- | ------ | ------- | ------ | ----- | ------------------- | --------- | ---- |
| **IdeaHammer**      | ✅ 8 步  | ✅       | ✅ 内置   | ✅ 两阶段 | ✅ **15 主题 / 73 文件** | ✅ **5 主题 / 6 文件** | ✅    |
| GitHub Spec Kit     | ⚠️ 3 段 | ✅       | ❌      | ❌     | ❌                   | ❌         | ❌    |
| 裸 Codex/Claude Code | ❌      | ❌       | ❌      | ❌     | ❌                   | ❌         | ❌    |
| 纯 vibe coding       | ❌      | ❌       | ❌      | ❌     | ❌                   | ❌         | ❌    |

**它是 Spec Kit + 工程级约束 + 业务纪律的三重组合**——比 vibe coding 多纪律围栏，比传统 PRD 多 AI 执行力，比裸 Codex 多工程级底线 + 业务底线。防"做完发现没人要 / AI 改价格把老订单也改了 / Spec 只过一种视角漏问题"。

---

## 🎯 它解决什么问题

做产品最大的浪费不是写代码，是**做完发现做错了**：

- 需求没想清楚就动手 → 做完发现用户不要
- 设计稿没敲定就开发 → 做完发现交互对不上
- 没有 Spec 单一真相源 → 代码和文档脱节
- 跳过测试直接交付 → 回归一次挂一片
- 没有 review 闭环 → 缺陷流到生产

**AI 写代码的独特浪费**：

- 反复造轮子 → 不知道行业已有成熟方案（Redis 不用 Redisson 手写 `setnx`、Java 不用 Hutool 自造 DateUtil、锁不用 Redisson 用 `SETNX+EXPIRE`）
- 写四不像代码 → 缺编码规范（不引用阿里 Java / PEP8 / Airbnb TS 等正式规范）
- 库选择无依据 → 不知道该选 Fastjson 还是 Jackson、httpx 还是 requests、Vitest 还是 Jest
- 性能反模式 → N+1 查询、`SELECT *`、深分页、无超时
- 安全漏洞 → MD5 存密码、Fastjson 1.x、`dangerouslySetInnerHTML` 不脱敏
- 上下文污染 → 不分层（pure 函数、副作用隔离、幂等性）
- 增量退化 → dead code / 无意义命名 / 装饰器套娃 / TODO 残留

**工程级约束把 AI 写代码的"反面教材"全列出来**——15 主题 / 73 文件 / 7300+ 行具体规则，dev-builder 启动必读，code-review Stage 2 必查：

- 13 个**原始主题**（编码规范 / 库选型 / 造轮子红线 / 性能 / 安全 / 并发 / API / 可观测 / CI·CD / 异常 / 数据库 / 依赖 / 国际化）+ **`simplification`（代码简洁之道 10 条）** + **`compatibility`（API 版本化 / 向后兼容 / blast radius / 数据迁移 / feature flag / 交付完整性）**

**自动化校验**：`scripts/check_simplicity.py`（270 行）按 10 条原则量化校验：

- 文件 ≤ 300 行 / 函数 ≤ 50 行 / 圈复杂度 ≤ 10 / 嵌套 ≤ 3 层 / 参数 ≤ 4 个
- 检测 dead code / 无意义命名 / 装饰器套娃 / TODO 残留

AI 写代码的 **3 大特有补充**（写在 `simplification/` 主题下）：

- **依赖最小化**：每个 dep 是债务，优先 stdlib（AI 倾向"装包解决 5 行问题"）
- **副作用隔离**：纯函数优先，副作用集中到边界（契约测试可写性靠这个）
- **幂等性**：脚本 / hook 反复执行结果相同（不重复追加 / 误删）

**AI 写产品（不只是代码）的独特浪费**：

- 没扫竞品就动手 → 做完发现市场已饱和 / 已有巨头
- 没做商业可行性快筛 → 做完发现没人付费 / 凭什么是你
- Spec 只过一种视角（主 Agent） → 漏掉 CEO/工程/QA 各自能看见的问题
- AI 改业务数据（价格/规格/规则）→ 把老订单 / 历史快照也改了（最常见、最隐蔽）
- 唯一视角写 Spec → 1 年后回看才后悔"当时没记下来"
- API 不版本化 → 上游改动炸下游所有调用方（兼容性问题）

**P1 业务纪律把以上 5 类"做完才发现"全列出来**——6 个文件 / ~600 行轻量纪律：

| 主题 | 解决什么 | 关键文件 |
|---|---|---|
| **business-context-check** | Phase 0 商业可行性 5 问快筛（防"做完没人要"） | `product-spec-builder/principles/business-context-check.md` |
| **competitive-scan** | Phase 1.5 竞品扫描（≥ 2 直接 + ≥ 2 替代，每行必填"我们凭什么"） | `product-spec-builder/principles/competitive-scan.md` |
| **ceo-lens / eng-lens / qa-lens** | Spec 收尾多视角自检（不 spawn subagent，提示词切换 + 自检清单） | 同上目录 3 文件 |
| **pre-mortem (Phase 3.5)** | question-bank 反向思考："1 年后死在哪 3 个原因 + 监控信号" | `principles/question-bank.md` |
| **versioning-and-immutability** | 价格/规格/规则字段必 version，禁止 UPDATE 覆盖（防 AI 改代码影响上下游） | `_engineering-constraints/database/versioning-and-immutability.md` |

dev-builder 启动必读，code-review Stage 2 必查。借鉴 gstack `office-hours` / `plan-ceo-review` 的 adversarial planning 思路，不抄实现，化为最小侵入式纪律。

---

## 🚀 快速开始

```bash
git clone https://github.com/along-ai-tech/idea-hammer.git
cd idea-hammer
mv agents .agents && mv codex .codex   # 装为隐藏目录
codex
```

主 Agent 自动应用本框架。输入一句"我想做一个 X"启动 product-spec-builder，8 步流水线自动推进。

> 镜像仓库：https://gitee.com/zhilong811/idea-hammer  
> 前置：Codex CLI、Python 3.10+（hook 脚本依赖）

---

## 💬 示例对话

```
👤 用户：我想做一个本地闪卡应用，准备 AI 应用岗面试。

🤖 主 Agent：好，进入 product-spec-builder。先做 Phase 0 商业可行性 5 问快筛，
   然后是 persona 和核心 job。准备好了就开始。

👤 用户：（回答 5 问 + persona + job）

🤖 主 Agent：Phase 0 通过 → 进 Phase 1 核心功能。继续 Phase 1.5 竞品扫描。
   你能想到 ≥ 2 直接竞品 + ≥ 2 替代方案吗？每行告诉我"我们凭什么"。

👤 用户：（答竞品）

🤖 主 Agent：Phase 1.5 通过 → 写完 Product-Spec.md，做收尾多视角自检
   （ceo-lens / eng-lens / qa-lens）→ Spec 定稿。

   → design-brief-builder / design-maker 跳过（用户不做 UI）
   → dev-planner：基于 Spec 拆 DEV-PLAN.md（Phase 1 骨架 / Phase 2 学习模式 / ...）
   → dev-builder：按 Phase 1 骨架开跑，RED → GREEN → REFACTOR
        后端 FastAPI + SQLAlchemy + SQLite
        前端 Vue3 + Element Plus + Vite
        14 个测试先写失败再补实现
   → code-reviewer：Stage 1 完整性 ✅ / Stage 2 质量 ✅（按工程级约束扫了 0 反模式）
   → release-builder：打包
   ✅ 可发布产品
```

完整 demo：`examples/personal-blog/`（按方法论从零到一真跑，README 在 `examples/personal-blog/README.md`）

---

## 🏗 架构与组件关系

```mermaid
flowchart TB
    User([用户输入"我想做 X"])

    subgraph Main["主 Agent（AGENTS.md）"]
        SessionLoad["SESSION-LOAD<br/>读精简版 session.json"]
        Router["STATE-ROUTING<br/>检测项目进度"]
        Orchestrator["规划 + 自驱执行"]
    end

    subgraph Skills["11 个 skill（按 description 自动触发）"]
        S1[product-spec-builder]
        S2[design-brief-builder]
        S3[design-maker]
        S4[dev-planner]
        S5[dev-builder]
        S6[bug-fixer]
        S7[code-review]
        S8[release-builder]
        M1[goal-creator]
        M2[evolution-engine]
        M3[skill-builder]
    end

    subgraph SubAgents["子 Agent（显式 spawn）"]
        CR[code-reviewer<br/>两阶段审查]
        ER[evolution-runner<br/>消化 signals]
    end

    subgraph Hooks["Hook 门禁（确定性检查）"]
        H1[SessionStart<br/>check-evolution]
        H2[PreToolUse<br/>pre-tool-shell]
        H3[PostToolUse<br/>auto-lint / mark-review-needed]
        H4[Stop<br/>stop-gate]
        H5[UserPromptSubmit<br/>detect-feedback-signal]
    end

    subgraph EC["工程级约束（跨 skill 共享）"]
        EC1[15 主题 / 73 文件<br/>编码规范 + 库选型 + 反模式]
        EC2[simplification<br/>10 条原则]
        EC3[compatibility<br/>API 版本化]
    end

    User --> SessionLoad --> Router --> Orchestrator
    Orchestrator -->|"按 description 触发"| Skills
    Orchestrator -->|"显式 spawn"| SubAgents
    Orchestrator -.->|"写入 / 读出"| SessionState[(session.json)]

    H1 --> ER
    ER -->|"产出 proposals"| Orchestrator

    S5 -.->|"启动必读"| EC
    S7 -.->|"Stage 2 必查"| EC

    H5 --> Signals[(signals.jsonl)]
    H2 -.->|"防误删 / 超时"| Orchestrator
    H3 -.->|"标 review-needed"| Orchestrator

    classDef main fill:#e3f2fd,stroke:#1976d2
    classDef skill fill:#f3e5f5,stroke:#7b1fa2
    classDef hook fill:#fff3e0,stroke:#f57c00
    classDef ec fill:#e8f5e9,stroke:#388e3c
    class SessionLoad,Router,Orchestrator main
    class S1,S2,S3,S4,S5,S6,S7,S8,M1,M2,M3 skill
    class H1,H2,H3,H4,H5 hook
    class EC1,EC2,EC3 ec
```

---

## 📚 详细文档

| 入口                                                                                   | 内容                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [AGENTS.md](./AGENTS.md)                                                             | 主控：编排规则、Skill 调用、Sub-Agent 调度                                                                                                                                                                          |
| [IDENTITY.md](./IDENTITY.md)                                                         | 主 Agent 角色 + 第一性原理                                                                                                                                                                                       |
| [WORKFLOW.md](./WORKFLOW.md)                                                         | 规划与执行模式、工作流程、文件结构                                                                                                                                                                                       |
| [SKILLS.md](./SKILLS.md)                                                             | 8 步流水线 + 总体纪律 + Skill 调用规则                                                                                                                                                                               |
| [SUBAGENTS.md](./SUBAGENTS.md)                                                       | 子 Agent 调度规则                                                                                                                                                                                            |
| [STATE-ROUTING.md](./STATE-ROUTING.md)                                               | 项目状态检测与路由                                                                                                                                                                                               |
| [TESTING.md](./TESTING.md)                                                           | TDD 铁律 + 四步走验证                                                                                                                                                                                          |
| [.codex/EVOLUTION.md](./.codex/EVOLUTION.md)                                         | 自进化机制说明                                                                                                                                                                                                 |
| [agents/skills/](./agents/skills/)                                                   | **11 个 skill**（每个含 SKILL.md + principles/ + workflows/ + contracts/）                                                                                                                                      |
| [agents/skills/_engineering-constraints/](./agents/skills/_engineering-constraints/) | **15 主题工程级约束**（coding-style / ecosystem-matrix / anti-reinvent / performance / security / concurrency / api-design / observability / ci-cd / error-handling / database / dependency-mgmt / i18n-a11y / **simplification** / **compatibility**） |
| [`examples/personal-blog/`](./examples/personal-blog/)                                 | **从零到一真跑的 demo**：按 IdeaHammer 8 步流水线（Spec → Design → Plan → Dev → Test → Review → PR），Phase 0-1 完成后填入 |
| [schemas/session.schema.json](./schemas/session.schema.json)                         | Session State schema（跨 session 持久化上下文）                                                                                                                                                                  |
| [tests/contract/](./tests/contract/)                                                 | **172 个契约测试**（skill 结构 + 意图分类 + simplification 10 条原则）— CI 卡门禁                                                                                                                                  |
| [scripts/check_simplicity.py](./scripts/check_simplicity.py)                         | **代码简洁自动校验**（文件/函数/圈复杂度阈值 + dead code / 命名）                                                                                                                                                          |
| [CHANGELOG.md](./CHANGELOG.md)                                                       | 变更记录                                                                                                                                                                                                    |
| [STATUS.md](./STATUS.md)                                                             | 当前状态快照（30 秒上手）                                                                                                                                                                                          |
| [DECISIONS.md](./DECISIONS.md)                                                       | 关键决策 Why 归档（D-001 ~ D-009）                                                                                                                                                                               |
| [TODO.md](./TODO.md)                                                                 | P0 / P1 / P2 backlog 详情                                                                                                                                                                                  |
| [.codex/](./.codex/)                                                                 | Hook 门禁 + 子 Agent + 自进化机制                                                                                                                                                                                |
| [.github/workflows/ci.yml](./.github/workflows/ci.yml)                               | GitHub Actions：契约测试 + skill 结构 + session 校验 + example 测试                                                                                                                                               |

---

## 🔬 方法论详解

**SDD（Spec-Driven Development）** — 文档是开发的入口和单一真相源。代码从 Spec 生成，Spec 变则下游文档和代码同步更。

**TDD（Test-Driven Development）** — 铁律：*无失败测试不写生产代码*。RED → GREEN → REFACTOR 强制循环；bug 修复前必先写失败复现测试。**172 个契约测试 + CI 卡门禁**确保框架自身遵循纪律（解决"框架说 TDD 但不测"的自相矛盾）。

**Design-Brief 与设计稿** — Spec 是文字（可能歧义），设计稿是图片（无歧义但不直接驱动代码）。Design-Brief 在中间做翻译：把 Spec 钉成可执行的视觉规范，再由 design-maker 生成精确参照图。UI 实现以设计稿为准；无稿无 Brief 时继承项目既有先例，不自由发挥。

**工程级约束（Engineering Constraints）** — IdeaHammer 的核心差异化能力。15 主题 / 73 文件 / 7300+ 行具体规则，覆盖 AI 写代码的常见反模式：

| 主题                    | 解决什么                                                                        | 关键文件                                             |
| --------------------- | --------------------------------------------------------------------------- | ------------------------------------------------ |
| **coding-style/**     | 强制引用正式规范（阿里 Java / PEP8 / Airbnb TS / Effective Go / SQL / Rust）            | `java-alibaba.md` `python-pep8.md`               |
| **ecosystem-matrix/** | "X 场景该用哪个库"决策（Redisson / Hutool / Jackson / FastAPI）                        | `java-ecosystem.md` `redis-clients.md`           |
| **anti-reinvent/**    | **10 条造轮子红线**：禁止自造连接池 / 日期 / 集合 / HTTP / JSON / 线程池 / 分布式锁 / ID / 缓存 / 配置中心 | `no-connection-pool.md` `no-distributed-lock.md` |
| **performance/**      | N+1 / 慢查询 / 缓存策略 / benchmark-first                                          | `db-query.md` `caching.md`                       |
| **security/**         | OWASP Top 10 / JWT / bcrypt / Vault / 漏洞扫描 / License 白名单                    | `owasp-top10.md` `password-hashing.md`           |
| **concurrency/**      | 线程池命名 / 分布式锁 / 幂等 / 超时                                                      | `distributed-lock.md` `timeouts.md`              |
| **api-design/**       | REST / 状态码 / 分页 / 错误响应 / OpenAPI 强制                                         | `rest-conventions.md` `http-status-codes.md`     |
| **observability/**    | 结构化日志 / 指标 / OpenTelemetry / 健康检查                                           | `structured-logging.md` `metrics.md`             |
| **ci-cd/**            | 必备检查 / migration 安全 / 回滚策略                                                  | `required-checks.md` `migration-safety.md`       |
| **error-handling/**   | 异常规范 / stacktrace / 统一错误响应                                                  | `exception-practices.md`                         |
| **database/**         | 索引策略 / 事务边界 / 连接池 / **版本化与不可变**                                            | `indexing.md` `versioning-and-immutability.md`  |
| **dependency-mgmt/**  | lockfile / 漏洞扫描 / 重复依赖                                                      | `lockfile-required.md`                           |
| **i18n-a11y/**        | 国际化 / 时区 / WCAG AA                                                          | `i18n.md` `a11y.md`                              |
| **simplification/**   | 代码简洁之道 10 原则（SRP / YAGNI / 抽象时机 / 阈值 / 命名 / 注释 / 删 dead code / 依赖最小化 / 纯函数 / 幂等） | `single-responsibility.md` `pure-functions.md`   |
| **compatibility/**    | **API 版本化 / 向后兼容 / blast radius / 数据迁移 / feature flag / 交付完整性**（防上游改动炸下游） | `api-versioning.md` `blast-radius.md`           |

dev-builder 启动时强制读 `principles/engineering-constraints.md` → 按语言加载对应规范 → 写代码时遵守。code-review Stage 2 必查"是否造轮子 / 是否版本化 / 是否符合 simplification 10 条"。下次再看到 `new SimpleDateFormat()` / `setnx` / `Executors.newFixedThreadPool()` / `UPDATE products SET price = ? WHERE id = ?` 这种反模式会被立刻 catch。

**Session State 持久化** — `.idea-hammer/session.json` 跨 session 保留上下文：当前 Phase / Task / 关键决策摘要（D-001 ~ D-N）/ 用户偏好（语言 / 风格 / 技术栈 / commit 风格）。启动时先读精简版（~2.3KB），不重读全部域文件（~15KB），**节省 ~85% 启动 token**。

**进化机制** — 你提的纠正被抓成信号，session 启动时主 Agent 同步消化，逐条问同意即改对应文档。框架越用越准，不是一次性写死的剧本。

---

## 🗺 路线图

- ✅ **v0.1** — 8 skill 骨架 + Hook 门禁 + 自进化机制
- ✅ **v0.2** — 端到端 demo 跑通（example/flashcards Phase 1-5：CRUD + SM-2 + 学习模式 UI，56 测试全绿）
- ✅ **v0.3** — 框架升级：拆 AGENTS.md（按域拆分）+ 拆 Skill 模板（三层结构）+ Session State 持久化
- ✅ **v0.4** — 工程级约束体系（13 主题）+ Skill 契约测试（132）+ 工程约束纳入 README
- ✅ **v0.5** — P1 全部完成（路由图 + 意图分类 + Hook v2 + Evolution 三层）
- ✅ **v0.6** — **代码简洁之道 10 条原则**（`simplification/` 11 文件 / 约 800 行）+ `check_simplicity.py` 自动化校验 + 框架代码以身作则重构
- ✅ **v0.7** — **P1 业务纪律体系**（防方向错 + 防遗漏 + 防上下游影响）
  - 商业可行性 5 问快筛（Phase 0）+ 竞品扫描（Phase 1.5）+ pre-mortem（Phase 3.5）
  - ceo-lens / eng-lens / qa-lens 收尾多视角自检
  - `_engineering-constraints/database/versioning-and-immutability.md`（接上轮"AI 改商品把老订单也改了"问题）
  - `_engineering-constraints/compatibility/` 新增 6 文件（API 版本化 / 向后兼容 / blast radius / 数据迁移 / feature flag / 交付完整性）
  - 借鉴 gstack adversarial planning gauntlet（office-hours / plan-ceo-review）化为轻量化纪律
- ⏳ **v1.0** — TODO-201 / TODO-202 / TODO-203 / TODO-301（英文 README + CI 补完 + Sub-Agent dag + API 稳定化）

---

## 👤 谁会用 / 项目目的

**项目目的**：展示 AI 编程标准化落地能力。IdeaHammer 本身不是产品，是一套**让 AI 在产研全流程中守住纪律的围栏**。

**典型用户**：

- **独立开发者 / 小团队 PM**：从模糊想法到可发布产品，要少走"做完发现做错了"的弯路
- **AI 重度用户**：用 Codex / Claude Code 写代码时，需要工程级约束防"AI 造轮子 / 写四不像 / 改坏上下游"
- **面试官视角看开源**：本项目是简历项目（见 [STATUS.md](./STATUS.md) 末尾"联系方式"段），README 本身按"陌生面试官 30 秒扫视 + 10 分钟可深入"的目标写

**作者**：wuzhilong · 主仓库 [along-ai-tech/idea-hammer](https://github.com/along-ai-tech/idea-hammer) · 简历已包含本项目链接

---

## 🤝 贡献

欢迎 PR / Issue。贡献前请阅读：

1. **[STATUS.md](./STATUS.md)** — 5 分钟了解当前到哪、接下来做什么
2. **[DECISIONS.md](./DECISIONS.md)** — 关键决策 Why，避免重蹈覆辙
3. **[TODO.md](./TODO.md)** — P0/P1/P2 backlog，挑你想做的
4. **[CHANGELOG.md](./CHANGELOG.md)** — 演进历史

**贡献约定**：

- 提交前跑 `python3 scripts/check_skill_structure.py --strict`（skill 结构必检）
- 提交前跑 `pytest tests/contract/`（契约测试必过）
- commit 信息用中文，格式 `<类型>(<范围>): <一句话>`，例如 `feat(skill): 新增 xxx`
- 修改 SKILL.md 必同步更新 principles/workflows/contracts 三层

**自进化机制**：你提的每条意见都会被 hook 抓成信号，下次 session 启动主 Agent 会主动问你是否同意落地——不必开 Issue，直接在对话里说就行。

---

## 📜 许可 & 致谢

[MIT](LICENSE) © 2026 wuzhilong

方法论受 [superpowers](https://github.com/obra/superpowers)（TDD + systematic-debugging）和 [GitHub Spec Kit](https://github.com/github/spec-kit)（SDD 三段式）启发。工程级约束覆盖的阿里 Java 手册 / PEP8 / Airbnb TS Style / OWASP Top 10 / Effective Go 等是开放共享的工业标准。`simplification/` 10 条原则来自工程共识综合（Robert C. Martin《Clean Code》/ Kent Beck《XP Explained》/ Martin Fowler《Refactoring》/ Boswell & Foucher《The Art of Readable Code》/ Sandi Metz）。`compatibility/` 主题对应 ThoughtWorks 技术雷达"API versioning" / "feature flag"条目。P1 业务纪律的多视角自检借鉴了 [gstack](https://github.com/garrytan/gstack) 的 adversarial planning gauntlet（office-hours / plan-ceo-review / plan-eng-review）思路。