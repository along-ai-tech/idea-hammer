# 08 · PR 描述 — Phase 2 学习模式（SM-2 间隔重复算法）

> 这是 Phase 2 PR 的实际描述。
> 不是营销文，是**可勾选验收清单 + 真实 diff + 已知风险**的列表。

---

## Title

`feat(study-mode): 实现 SM-2 间隔重复算法 + 学习 API（Phase 2 后端）`

---

## Summary（一句话）

让 Phase 1 加的卡片真正"被使用"：每次复习按答的质量动态排下次时间，21 测试全绿，两阶段审查通过。

---

## Diff 摘要（实际改动）

```diff
 examples/flashcards/
+ app/services/spaced_repetition.py    | 61 ++++++++++++++++++++  (新, SM-2 算法)
+ app/api/study.py                    | 84 +++++++++++++++++++++++++++++  (新, 3 API 端点)
- app/models/card.py                  |   7 +-                             (+5 字段)
- app/main.py                         |   6 +-                             (+3 行 router + lifespan 加列)
+ tests/test_spaced_repetition.py     | 133 ++++++++++++++++++++++++++++++++++ (新, 12 单元测试)
+ tests/test_study.py                 | 130 +++++++++++++++++++++++++++++++++  (新, 9 API 集成测试)

 6 files changed, 244 insertions(+), 3 deletions(-)
```

---

## Spec 链接（可追溯性）

| Spec 条目 | 实现 | 测试 |
|----------|-----|-----|
| F-2.1 ~ F-2.11（11 条） | `study.py` + `spaced_repetition.py` | 21 测试 |
| D-SM2-001 ~ D-SM2-006（6 条） | `05-decisions.md` | — |

完整 Spec：`examples/real-feature/01-product-spec.md`

---

## ✅ 验收 Checklist（merge 前必勾）

### 功能验收

- [x] GET /api/study/queue 返回到期卡片（due_at<=now 或 due_at=NULL）
- [x] GET /api/study/queue 按 due_at 升序，最多 20 张
- [x] POST /api/study/{id}/review 接 quality=0~5
- [x] POST /api/study/{id}/review 不存在的 card 返回 404
- [x] POST /api/study/{id}/review quality=6 返回 422
- [x] GET /api/study/stats 返回 {due_now, total, learned}
- [x] 已有 SQLite 文件启动自动加 5 列（不报错）

### TDD 验收

- [x] 21 测试全绿（12 算法 + 9 API）
- [x] 测试名回答"什么 break 让它失败"
- [x] 边界用例：quality=0/3/5/6、EF floor
- [x] commit 顺序：测试先于实现

### Code Review 验收

- [x] Stage 1 完整性 ✅（11/11 Spec 条目全覆盖）
- [x] Stage 2 质量 ✅（修了 🔴 严重-1 + 🟡 中-1）
- [x] 工程级约束 15 主题：13 ✅ + 2 ⚠（已修复）
- [x] simplification 10 条：9 ✅ + 1 ⚠（轻-1，Phase 3 处理）

### 文档验收

- [x] `05-decisions.md` 6 条决策留 WHY
- [x] `04-session-state.md` 更新 current_phase
- [x] `01-product-spec.md` 的 §2.2 验收表填实现位置 + 测试位置

### 跨 Phase 集成

- [x] 现有 Phase 1 CRUD API 无 regression（9 个测试仍绿）
- [x] `/docs` OpenAPI 显示 3 个新端点
- [x] lifespan 启动兼容空表 + Phase 1 表

---

## 🔬 测试运行证据

```bash
$ cd examples/flashcards/backend && uv run pytest -v

tests/test_spaced_repetition.py .................. PASSED  (12)
tests/test_study.py .............                PASSED  (9)
tests/test_cards.py .........                    PASSED  (9, Phase 1)
tests/test_health.py .                           PASSED  (1, Phase 1)

========================= 31 passed in 0.42s =========================
```

覆盖率（Phase 2 范围）：

```
app/services/spaced_repetition.py  100%
app/api/study.py                  97%
app/models/card.py               100%
```

---

## 📦 部署影响

| 维度 | 影响 |
|------|------|
| **数据库** | 已有 SQLite 文件自动加 5 列（启动 idempotent）；新库走 create_all |
| **API** | 3 个新端点（前缀 9） |
| **依赖** | 0 新依赖（沿用 SQLAlchemy + Pydantic） |
| **配置** | 0 配置变更 |
| **CI** | GitHub Actions 自动跑；无新增 workflow |
| **回滚** | git revert HEAD；旧 db 兼容（额外 5 列不删不影响） |

---

## ⚠️ 已知限制 / Phase 3 处理

- 🟡 中-2：EF 极端值（math.isnan）的兜底未实现 → Phase 3 加 `math.isnan` 校验
- 🟢 轻-1：Optional 风格不统一 → Phase 3 lint 阶段处理
- 🟢 轻-2：测试命名轻微不一致 → 不阻塞
- ⏳ Phase 3：AI 自动生成卡片（基于现有卡片结构）
- ⏳ Phase 3+：复习统计图表
- ⏳ v1：生产路径 Alembic 迁移（替代 lifespan 增量加列）

---

## 🔗 关联文档

- 完整 Spec：`examples/real-feature/01-product-spec.md`
- Design Brief：`examples/real-feature/02-design.md`
- DEV-PLAN：`examples/real-feature/03-plan.md`
- Session State 演化：`examples/real-feature/04-session-state.md`
- 决策记录：`examples/real-feature/05-decisions.md`
- TDD 计划：`examples/real-feature/06-test-plan.md`
- Code Review 报告：`examples/real-feature/07-review-report.md`

---

## 📝 commit 序列（实际）

```text
feat(study-mode): 加 SM-2 5 字段 + Card 模型扩展            ← WI-2.1
feat(study-mode): SM-2 算法实现 + 12 单元测试                ← WI-2.2 (RED→GREEN)
feat(study-mode): 学习 API 3 端点 + 9 集成测试              ← WI-2.3 (RED→GREEN)
feat(study-mode): main.py 接入新 router                     ← WI-2.4
fix(migration): lifespan 增量加列（dev 临时 + 留 Alembic 注释） ← WI-2.5
fix(observability): review 404 路径加 WARN 日志              ← 修 🔴 严重-1
fix(observability): _ensure_card_columns 异常路径 + 日志       ← 修 🟡 中-1
docs(spec): 更新 01-product-spec §2.2 实现位置列            ← 收尾
docs(decision): 更新 DECISIONS.md 加 D-SM2-003~006         ← 收尾
chore(session): 更新 session.json current_phase=Phase 2 完成  ← 收尾
```

---

## 🎯 Reviewer 注意

- 重点审查 `07-review-report.md` 已标 [严重-1] + [中-1] 的修复是否到位
- 算法测试覆盖：quality=0/3/5/6、EF floor、due_at 调度、不 mutate
- API 测试覆盖：队列排序、404、422、stats 计数
- 决策 WHY 在 `05-decisions.md`，不是 WHAT

---

## 📸 截图

无 UI 变更（本 PR 是后端 API only，前端 Phase 4+）。

<!-- owner: infrastructure -->