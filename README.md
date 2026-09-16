# IdeaHammer

> AI 辅助从模糊想法锤出可发布产品

**一个 AI 主导的产研全流程协同框架**——把产品经理的纪律（反模糊、Spec 驱动）和研发的工程化（TDD、review、release、**工业级编码约束**）合成一条端到端流水线。

| 11 | 188 | 1 | **70** | MIT |
|---|---|---|---|---|
| skill 模块 | 测试通过 | 端到端 demo | 工程级约束 | 开源协议 |

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0--dev-blue.svg)](CHANGELOG.md)
[![Main Repo](https://img.shields.io/badge/GitHub-along-ai-tech-181717?logo=github)](https://github.com/along-ai-tech/idea-hammer)
[![Mirror](https://img.shields.io/badge/Gitee-zhilong811-C71D23?logo=gitee)](https://gitee.com/zhilong811/idea-hammer)

---

## 方法论：8 步流水线

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

## 和同类项目有什么不同

| 项目 | 端到端 | Spec 驱动 | TDD 强制 | 审查闭环 | **工程级约束** | 进化机制 |
|------|--------|-----------|---------|---------|---------|---------|
| **IdeaHammer** | ✅ 8 步 | ✅ | ✅ 内置 | ✅ 两阶段 | ✅ **13 主题 / 70 文件** | ✅ |
| GitHub Spec Kit | ⚠️ 3 段 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 裸 Codex/Claude Code | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 纯 vibe coding | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**它是 Spec Kit + 工程级约束的组合**——比 vibe coding 多纪律围栏，比传统 PRD 多 AI 执行力，比裸 Codex 多工程级底线（不让 AI 反复造轮子 / 写四不像代码 / 留 N+1 / 用 `setnx` 当分布式锁）。

---

## 它解决什么问题

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

**工程级约束把 AI 写代码的"反面教材"全列出来**——13 主题 / 70 文件 / 6440 行具体规则，dev-builder 启动必读，code-review Stage 2 必查。

---

## 快速开始

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

## 详细文档

| 入口 | 内容 |
|------|------|
| [AGENTS.md](./AGENTS.md) | 主控：编排规则、Skill 调用、Sub-Agent 调度 |
| [agents/skills/](./agents/skills/) | **11 个 skill**（每个含 SKILL.md + principles/ + workflows/ + contracts/）|
| [agents/skills/_engineering-constraints/](./agents/skills/_engineering-constraints/) | **13 主题工程级约束**（coding-style / ecosystem-matrix / anti-reinvent / performance / security / concurrency / api-design / observability / ci-cd / error-handling / database / dependency-mgmt / i18n-a11y） |
| [examples/flashcards/](./examples/flashcards/) | 端到端 demo：本地闪卡应用（Python + Vue3 + Element Plus，已跑通 Phase 1-5） |
| [schemas/session.schema.json](./schemas/session.schema.json) | Session State schema（跨 session 持久化上下文） |
| [tests/contract/](./tests/contract/) | **132 个 skill 契约测试**（TDD 纪律 / 调用规则 / 错误处理） |
| [CHANGELOG.md](./CHANGELOG.md) | 变更记录 |
| [.codex/](./.codex/) | Hook 门禁 + 子 Agent + 自进化机制 |

---

## 方法论详解

**SDD（Spec-Driven Development）** — 文档是开发的入口和单一真相源。代码从 Spec 生成，Spec 变则下游文档和代码同步更。

**TDD（Test-Driven Development）** — 铁律：*无失败测试不写生产代码*。RED → GREEN → REFACTOR 强制循环；bug 修复前必先写失败复现测试。**132 个契约测试 + CI 卡门禁**确保框架自身遵循纪律（解决"框架说 TDD 但不测"的自相矛盾）。

**Design-Brief 与设计稿** — Spec 是文字（可能歧义），设计稿是图片（无歧义但不直接驱动代码）。Design-Brief 在中间做翻译：把 Spec 钉成可执行的视觉规范，再由 design-maker 生成精确参照图。UI 实现以设计稿为准；无稿无 Brief 时继承项目既有先例，不自由发挥。

**工程级约束（Engineering Constraints）** — IdeaHammer 的核心差异化能力。13 主题 / 70 文件 / 6440 行具体规则，覆盖 AI 写代码的常见反模式：

| 主题 | 解决什么 | 关键文件 |
|---|---|---|
| **coding-style/** | 强制引用正式规范（阿里 Java / PEP8 / Airbnb TS / Effective Go / SQL / Rust） | `java-alibaba.md` `python-pep8.md` |
| **ecosystem-matrix/** | "X 场景该用哪个库"决策（Redisson / Hutool / Jackson / FastAPI） | `java-ecosystem.md` `redis-clients.md` |
| **anti-reinvent/** | **10 条造轮子红线**：禁止自造连接池 / 日期 / 集合 / HTTP / JSON / 线程池 / 分布式锁 / ID / 缓存 / 配置中心 | `no-connection-pool.md` `no-distributed-lock.md` |
| **performance/** | N+1 / 慢查询 / 缓存策略 / benchmark-first | `db-query.md` `caching.md` |
| **security/** | OWASP Top 10 / JWT / bcrypt / Vault / 漏洞扫描 / License 白名单 | `owasp-top10.md` `password-hashing.md` |
| **concurrency/** | 线程池命名 / 分布式锁 / 幂等 / 超时 | `distributed-lock.md` `timeouts.md` |
| **api-design/** | REST / 状态码 / 分页 / 错误响应 / OpenAPI 强制 | `rest-conventions.md` `http-status-codes.md` |
| **observability/** | 结构化日志 / 指标 / OpenTelemetry / 健康检查 | `structured-logging.md` `metrics.md` |
| **ci-cd/** | 必备检查 / migration 安全 / 回滚策略 | `required-checks.md` `migration-safety.md` |
| **error-handling/** | 异常规范 / stacktrace / 统一错误响应 | `exception-practices.md` |
| **database/** | 索引策略 / 事务边界 / 连接池 | `indexing.md` `transactions.md` |
| **dependency-mgmt/** | lockfile / 漏洞扫描 / 重复依赖 | `lockfile-required.md` |
| **i18n-a11y/** | 国际化 / 时区 / WCAG AA | `i18n.md` `a11y.md` |

dev-builder 启动时强制读 `principles/engineering-constraints.md` → 按语言加载对应规范 → 写代码时遵守。code-review Stage 2 必查"是否造轮子"。下次再看到 `new SimpleDateFormat()` / `setnx` / `Executors.newFixedThreadPool()` 这种反模式会被立刻 catch。

**Session State 持久化** — `.idea-hammer/session.json` 跨 session 保留上下文：当前 Phase / Task / 关键决策摘要（D-001 ~ D-N）/ 用户偏好（语言 / 风格 / 技术栈 / commit 风格）。启动时先读精简版（~1KB），不重读全部域文件（~12KB），**节省 93.1% 启动 token**。

**进化机制** — 你提的纠正被抓成信号，session 启动时主 Agent 同步消化，逐条问同意即改对应文档。框架越用越准，不是一次性写死的剧本。

---

## 路线图

- ✅ **v0.1** — 8 skill 骨架 + Hook 门禁 + 自进化机制
- ✅ **v0.2** — 端到端 demo 跑通（example/flashcards Phase 1-5：CRUD + SM-2 + 学习模式 UI，56 测试全绿）
- ✅ **v0.3** — 框架升级：拆 AGENTS.md（按域拆分）+ 拆 Skill 模板（三层结构）+ Session State 持久化
- ✅ **v0.4** — **工程级约束体系**（13 主题 / 70 文件 / 6440 行）+ **Skill 契约测试**（132 测试 + CI 卡门禁）+ 工程约束纳入 README
- ⏳ **v0.5** — 流水线改路由图（spike / refine / 并发）+ Skill 触发改为意图分类
- ⏳ **v1.0** — 稳定 API，向后兼容承诺

---

## 许可

[MIT](LICENSE) © 2026 wuzhilong

## 致谢

方法论受 [superpowers](https://github.com/obra/superpowers)（TDD + systematic-debugging）和 [GitHub Spec Kit](https://github.com/github/spec-kit)（SDD 三段式）启发。工程级约束覆盖的阿里 Java 手册 / PEP8 / Airbnb TS Style / OWASP Top 10 / Effective Go 等是开放共享的工业标准。
