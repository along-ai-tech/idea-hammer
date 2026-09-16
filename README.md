# IdeaHammer

> AI 辅助从模糊想法锤出可发布产品

**一个 AI 主导的产研全流程协同框架**——把产品经理的纪律（反模糊、Spec 驱动）和研发的工程化（TDD、review、release）合成一条端到端流水线。

| 8 | 56 | 1 | MIT |
|---|---|---|---|
| skill 模块 | 测试通过 | 端到端 demo | 开源协议 |

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.2-blue.svg)](CHANGELOG.md)
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

8 步对应 8 个 skill 模块，按依赖顺序串行（bug-fixer 由审查失败触发，作为 ⑦ 的回路）。每步有独立产出物，下一步按它启动。

---

## 和同类项目有什么不同

| 项目 | 端到端 | Spec 驱动 | TDD 强制 | 审查闭环 | 进化机制 |
|------|--------|-----------|---------|---------|---------|
| **IdeaHammer** | ✅ 8 步 | ✅ | ✅ 内置 | ✅ 两阶段 | ✅ |
| GitHub Spec Kit | ⚠️ 3 段 | ✅ | ❌ | ❌ | ❌ |
| 裸 Codex/Claude Code | ❌ | ❌ | ❌ | ❌ | ❌ |
| 纯 vibe coding | ❌ | ❌ | ❌ | ❌ | ❌ |

**它是 Spec Kit 往工程化推一步的版本**——比 vibe coding 多纪律围栏，比传统 PRD 多 AI 执行力。

---

## 它解决什么问题

做产品最大的浪费不是写代码，是**做完发现做错了**：

- 需求没想清楚就动手 → 做完发现用户不要
- 设计稿没敲定就开发 → 做完发现交互对不上
- 没有 Spec 单一真相源 → 代码和文档脱节
- 跳过测试直接交付 → 回归一次挂一片
- 没有 review 闭环 → 缺陷流到生产

IdeaHammer 把这些纪律**内化到 AI Agent 的执行流程里**——不靠人记性，靠 skill + hook 内置门禁。

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
| [agents/skills/](./agents/skills/) | 8 个 skill 模块（每个含 SKILL.md + references/ + templates/） |
| [examples/flashcards/](./examples/flashcards/) | 端到端 demo：本地闪卡应用（Python + Vue3 + Element Plus，已跑通 Phase 1-3） |
| [CHANGELOG.md](./CHANGELOG.md) | 变更记录 |
| [.codex/](./.codex/) | Hook 门禁 + 子 Agent + 自进化机制 |

---

## 方法论详解

**SDD（Spec-Driven Development）** — 文档是开发的入口和单一真相源。代码从 Spec 生成，Spec 变则下游文档和代码同步更。

**TDD（Test-Driven Development）** — 铁律：*无失败测试不写生产代码*。RED → GREEN → REFACTOR 强制循环；bug 修复前必先写失败复现测试。

**Design-Brief 与设计稿** — Spec 是文字（可能歧义），设计稿是图片（无歧义但不直接驱动代码）。Design-Brief 在中间做翻译：把 Spec 钉成可执行的视觉规范，再由 design-maker 生成精确参照图。UI 实现以设计稿为准；无稿无 Brief 时继承项目既有先例，不自由发挥。

**进化机制** — 你提的纠正被抓成信号，session 启动时主 Agent 同步消化，逐条问同意即改对应文档。框架越用越准，不是一次性写死的剧本。

---

## 路线图

- ✅ **v0.1** — 8 skill 骨架 + Hook 门禁 + 自进化机制
- ✅ **v0.2** — 端到端 demo 跑通（example/flashcards Phase 1-3：CRUD + SM-2 + 学习模式 UI，56 测试全绿）
- 🚧 **v0.3** — 框架升级：拆 AGENTS.md（按域拆分）/ 拆 Skill 模板（三层结构）/ Session State 持久化
- ⏳ **v0.4** — 英文版 README + CI 自动化
- ⏳ **v1.0** — 稳定 API，向后兼容承诺

---

## 许可

[MIT](LICENSE) © 2026 wuzhilong

## 致谢

方法论受 [superpowers](https://github.com/obra/superpowers)（TDD + systematic-debugging）和 [GitHub Spec Kit](https://github.com/github/spec-kit)（SDD 三段式）启发。
