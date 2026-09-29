# Real Feature 端到端案例：闪卡学习模式（SM-2 间隔重复）

> IdeaHammer 8 步流水线在一个**真实 Feature**上的完整产物链
> 业务需求 → Product Spec → Design → Plan → AI 开发 → Test → Review → PR

这是 IdeaHammer 用 `flashcards` 项目的 **Phase 2 — 学习模式**（SM-2 间隔重复算法）
做的端到端真实走查：所有产物都来自实际产研过程，不是 demo 拼出来的样板。

每一步都有可验证证据：

- **代码**：`examples/flashcards/backend/app/api/study.py` + `app/services/spaced_repetition.py`
- **测试**：`examples/flashcards/backend/tests/test_spaced_repetition.py`（12 个） + `test_study.py`（9 个）
- **commit / PR**：`08-pr-description.md` 里给了完整 diff 描述 + checklist

---

## 📑 一页读懂：8 个产物在管线里的位置

```
业务需求（一句模糊话）
   ↓ product-spec-builder
01-product-spec.md          ← Product Spec（11 节，含 Phase 1.5 竞品扫描 + ceo/eng/qa lens）
   ↓ design-brief-builder
02-design.md                ← Design Brief（学习模式信息架构 + 状态机 + 反 UI 假设）
   ↓ dev-planner
03-plan.md                  ← DEV-PLAN（Phase 2 拆任务 / 验收 / 依赖 / 并行 / 串行）
   ↓ 主 Agent 边写代码边更新
04-session-state.md         ← session.json 跨 session 状态演化
05-decisions.md             ← 关键决策 Why（D-SM2-001 至 D-SM2-006）
   ↓ dev-builder（RED → GREEN → REFACTOR）
[实际代码 + 21 个测试]
   ↓ 主 Agent spawn code-reviewer
07-review-report.md         ← 两阶段审查报告（Stage 1 完整性 + Stage 2 质量/工程约束/simplification）
   ↓ 主 Agent 改 + 重审
08-pr-description.md        ← PR 描述 + diff 摘要 + merge checklist
```

---

## 🎯 这个 Feature 是什么

**学习模式** = 用户开始用 Phase 1 建的卡片来真正记忆东西。

Phase 1 只能"管卡"（CRUD），但**用户要的不是管卡，是记住东西**。
Phase 2 加上 SM-2 间隔重复算法：每次复习按"答得好不好"动态排下次复习时间，
让用户用最少次数记住最多。

**对应一句话业务需求**：

> "我想做一个本地闪卡应用，准备 AI 应用岗面试。"
> —— Phase 1：能加卡片 → Phase 2：**能真正用这些卡片学习**

---

## 📁 目录结构

| # | 文件 | 含义 | 来自哪一步 |
|---|------|------|----------|
| 01 | `01-product-spec.md` | Product Spec 11 节 + Phase 0/1.5/3.5/收尾 4 个纪律环节 | product-spec-builder |
| 02 | `02-design.md` | Design Brief：信息架构 + 状态机 + UI 假设 + 反假设 | design-brief-builder |
| 03 | `03-plan.md` | DEV-PLAN 的 Phase 2 章节：拆任务 / 验收 / 依赖 | dev-planner |
| 04 | `04-session-state.md` | 3 个 session.json 快照（启动前 → Phase 2 启动 → 完成） | 主 Agent 落地 |
| 05 | `05-decisions.md` | 6 条关键决策（D-SM2-001 ~ D-SM2-006）的 WHY 留底 | dev-builder |
| 06 | `06-test-plan.md` | TDD 计划 + 21 测试用例清单 + 覆盖率 | dev-builder |
| 07 | `07-review-report.md` | 两阶段审查：Stage 1 完整性 + Stage 2 质量 | code-reviewer |
| 08 | `08-pr-description.md` | PR 描述 + diff 摘要 + merge checklist | 主 Agent |

---

## ✅ 端到端怎么验收（30 秒看）

打开任一文件，能看到：

1. **业务需求 → 代码可追溯**：每个 API 端点能指回 Spec 的功能条款
2. **决策有 Why 不是 What**：05-decisions.md 6 条都给了「候选方案对比 + 拒绝理由」
4. **测试有证据**：06-test-plan.md 21 测试，每条对应一个 RED 失败原因
5. **审查有产物**：07-review-report.md Stage 2 扫了工程级约束 15 主题 + simplification 10 条
6. **PR 有 checklist**：08 不是营销文，是可勾选验收清单

---

## 🔗 对照真实产物

| 文档 | 对应的真实产物 |
|------|---------------|
| 03-plan 里的"实现 SM-2 算法" | `examples/flashcards/backend/app/services/spaced_repetition.py` |
| 03-plan 里的"复习 API 3 个端点" | `examples/flashcards/backend/app/api/study.py` |
| 06-test-plan 里的 12 算法单元测试 | `examples/flashcards/backend/tests/test_spaced_repetition.py` |
| 06-test-plan 里的 9 API 集成测试 | `examples/flashcards/backend/tests/test_study.py` |
| 04-session-state 里的 schema_version | `schemas/session.schema.json` |

---

## 💡 这套产物回答什么问题

- **"AI 写代码怎么防翻车"** → 06 RED→GREEN→REFACTOR 链 + 07 两阶段审查
- **"Spec 怎么不写空话"** → 01 的 11 节 + 4 个纪律环节 + 每个验收写"什么 break 让它失败"
- **"决策怎么留 WHY 不是 WHAT"** → 05 候选对比 + 影响范围
- **"PR 描述怎么不被当成营销"** → 08 diff 摘要 + 真实 checklist + 已知限制

---

## 📌 注意

本目录是**走查产物 + 已落地代码的索引**，不是 demo 文案。
所有 Spec 条目 / API / 测试都对应 `examples/flashcards/` 里真实运行代码。
跑测试：

```bash
cd examples/flashcards/backend && uv run pytest -v
```

应看到 `21 passed`（12 spaced_repetition + 9 study）。

<!-- owner: product -->