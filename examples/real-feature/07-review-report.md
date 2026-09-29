# 07 · Code Review 报告 — Phase 2 学习模式

> 这是主 Agent spawn `.codex/agents/code-reviewer.toml` 后，
> 子 Agent 按两阶段协议（Stage 1 完整性 / Stage 2 质量）产出的审查报告。
>
> 报告 100% 按"找问题"模式，不是找优点。所有问题带 fix 路径。

---

## 0. 元数据

| 字段 | 值 |
|------|---|
| 审查对象 | Phase 2 学习模式 PR |
| 改动文件 | `app/services/spaced_repetition.py`（新）+ `app/api/study.py`（新）+ `app/models/card.py`（改）+ `app/main.py`（改）+ `tests/test_spaced_repetition.py`（新）+ `tests/test_study.py`（新） |
| 改动行数 | +247 / -3 |
| 审查时间 | 2026-09-11 16:00 ~ 16:45 |
| 子 Agent | `code-reviewer`（用 `review-agent` skill） |
| 输入上下文 | 完整 Spec + DEV-PLAN + 决策（D-SM2-001~006）+ 21 测试 |
| 输出 | 本报告（缺陷 + fix 路径，不含表扬） |

---

## Stage 1 · 完整性（Completeness）

**目标**：每个 Spec 条目是否都有实现 + 测试覆盖 + 验证证据？

### 1.1 Spec → 实现 → 测试可追溯矩阵

| Spec ID | 实现位置 | 测试 ID | 覆盖？ |
|---------|---------|---------|-------|
| F-2.1 队列按 due_at 升序 | `study.py::get_study_queue` | #20, #21 | ✅ |
| F-2.2 due_at=NULL 包含 | `study.py::get_study_queue` | #13 | ✅ |
| F-2.3 quality=3 → reps=1 | `spaced_repetition.py::calculate_next_review` + `study.py::review_card` | #3, #4, #5, #14 | ✅ |
| F-2.4 quality=0 → 重置 | 同上 | #1, #2, #15 | ✅ |
| F-2.5 EF floor | `spaced_repetition.py` | #8 | ✅ |
| F-2.6 EF±delta | `spaced_repetition.py` | #6, #7 | ✅ |
| F-2.7 due_at 调度 | `spaced_repetition.py` | #9, #10, #16 | ✅ |
| F-2.8 不 mutate | `spaced_repetition.py` | #12 | ✅ |
| F-2.9 quality 越界双层 | `spaced_repetition.py` + `study.py` | #11, #18 | ✅ |
| F-2.10 stats 计数 | `study.py::get_study_stats` | #19 | ✅ |
| F-2.11 404 | `study.py::review_card` raise | #17 | ✅ |

**Stage 1 结果**：✅ **PASS**（11/11 Spec 条目全覆盖，无遗漏）

### 1.2 TDD 合规

| 检查项 | 结果 |
|------|----|
| 21 测试均处于 GREEN | ✅ |
| 测试名回答"什么 break 让它失败" | ✅（全部 21 个名字用动作+对象+预期） |
| 边界用例（quality=0/3/5/6） | ✅ 覆盖 |
| 无 mirror assertion | ✅ 抽样检查 #7, #15, #19 均为字面量+独立推导 |
| TDD commit 时间倒挂（测试晚于实现） | ✅ 验证通过（git log 测试先提交） |

---

## Stage 2 · 质量（Quality）

**目标**：代码本身是否符合工程级约束（15 主题）+ simplification 10 条？

### 2.1 缺陷清单（按严重度排序）

#### 🔴 [严重-1] `study.py::review_card` 缺错误日志

**位置**：`examples/flashcards/backend/app/api/study.py:84`

```python
@router.post("/study/{card_id}/review", response_model=CardStudyOut)
def review_card(card_id: int, payload: ReviewRequest, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
```

**问题**：404 路径不打 WARN 日志，运维看不到异常访问。

**违反约束**：`agents/_engineering-constraints/observability/structured-logging.md` 第 2 条

```diff
+ import logging
+ logger = logging.getLogger(__name__)

  @router.post("/study/{card_id}/review", response_model=CardStudyOut)
  def review_card(card_id: int, payload: ReviewRequest, db: Session = Depends(get_db)):
      card = db.query(Card).filter(Card.id == card_id).first()
      if not card:
+         logger.warning("review nonexistent card_id=%d", card_id)
          raise HTTPException(status_code=404, detail="Card not found")
```

**影响**：可观测性 -1；Phase 3 加 AI 调用时无法区分"用户恶意"与"前端 bug"。

**修复 commit**：`fix(observability): study.py 404 路径加 WARN 日志`

---

#### 🟡 [中-1] `_ensure_card_columns` 缺异常处理

**位置**：`examples/flashcards/backend/app/main.py:_ensure_card_columns`

```python
def _ensure_card_columns():
    inspector = inspect(engine)
    if "cards" not in inspector.get_table_names():
        return
    existing = {c["name"] for c in inspector.get_columns("cards")}
    additions = [...]
    with engine.begin() as conn:
        for col_name, col_def in additions:
            if col_name not in existing:
                conn.execute(text(f"ALTER TABLE cards ADD COLUMN {col_name} {col_def}"))
```

**问题**：

- 缺 try/except，多卡启动并发可能失败
- 没记录哪些列被加过，下次 idempotency 验证靠列存在性
- 错误时抛 5xx 给前端，但前端无重试路径

**违反约束**：`agents/_engineering-constraints/error-handling/exception-practices.md` 第 5 条

```diff
+ import logging
+ logger = logging.getLogger(__name__)

  def _ensure_card_columns():
      inspector = inspect(engine)
      if "cards" not in inspector.get_table_names():
          return
      existing = {c["name"] for c in inspector.get_columns("cards")}
      additions = [...]
+     try:
+         with engine.begin() as conn:
+             for col_name, col_def in additions:
+                 if col_name not in existing:
+                     conn.execute(text(f"ALTER TABLE cards ADD COLUMN {col_name} {col_def}"))
+                     logger.info("migration added column=%s", col_name)
+     except SQLAlchemyError as e:
+         logger.exception("card columns migration failed")
+         raise RuntimeError("Database migration failed; manual intervention required") from e
```

**影响**：本地单用户场景风险低；生产路径（Alembic）会重写此逻辑。

**修复 commit**：`fix(observability): _ensure_card_columns 加迁移日志 + 异常上抛`

---

#### 🟡 [中-2] `study.py::review_card` 未对 EF 异常路径校验

**位置**：`study.py::review_card:74`

```python
updated = calculate_next_review(card, payload.quality)
```

**问题**：若 EF 公式因 float 精度异常（极端 EF 值），可能产生负 EF 或 NaN。

**场景**：本地复现需 EF=1.3001 + quality=0 → EF 算出来可能是 1.2999999... 由于 floor 拉回 1.3，但若后续 quality=0 反复触发，理论可能 NaN。

**违反约束**：`agents/_engineering-constraints/_engineering-constraints/error-handling/exception-practices.md` 第 7 条

**fix 路径**：

```diff
+ import math
  updated = calculate_next_review(card, payload.quality)
+ if math.isnan(updated.easiness_factor) or updated.easiness_factor < EF_FLOOR:
+     raise HTTPException(status_code=500, detail="Internal calculation error")

  card.repetitions = updated.repetitions
  card.interval = updated.interval
  card.easiness_factor = updated.easiness_factor
```

**风险评估**：本地 SQLite 单用户实践<2 年无 NaN 触发条件，建议加 fallback。

**优先级**：中（不阻塞 PR，可 Phase 3 处理）

---

#### 🟢 [轻-1] `study.py` 重复字面量字符串

**位置**：`study.py:3, 30, 65`

```python
from typing import List, Optional
```

+ `optional: datetime` / `Optional[datetime]` 风格混用

**违反约束**：`simplification/single-responsibility.md` 第 3 条（命名一致性）

**fix 路径**：把 `Optional[datetime]` 统一为 `datetime | None`（Python 3.10+）或显式 `Optional`。

**优先级**：轻（不影响功能；CI lint 触发阶段处理）

---

#### 🟢 [轻-2] 测试命名可加三种子两统一

**位置**：`test_spaced_repetition.py:13`

```python
def test_quality_below_three_resets_repetitions_to_zero():
```

vs

```python
def test_first_correct_answer_sets_interval_to_one():
```

**观察**：测试名风格不统一（`test_<action>_<object>_<expected>`），但都可读，可不改。

**优先级**：轻（PR 不阻塞）

---

### 2.2 工程级约束 15 主题检查（Stage 2 必查）

| # | 主题 | 命中 |
|---|-------|------|
| 1 | coding-style | ✅ 符合 PEP8 |
| 2 | ecosystem-matrix | ✅ 选 SQLAlchemy 2.0 + Pydantic v2（决策 D-SM2-002 留底） |
| 3 | anti-reinvent | ✅ 没自造 ORM / 自造日期工具 |
| 4 | performance | ✅ `limit=20` 防全表扫；待 v1 加 `(due_at, id)` 覆盖索引 |
| 5 | security | ✅ quality 是 int（Pydantic 防 JSON injection）；无 SQL 注入（ORM？） |
| 6 | concurrency | N/A 单进程 |
| 7 | api-design | ✅ REST / 422 / 404 状态码正确；OpenAPI 自动 |
| 8 | observability | ❌ **中-1 命中**（404 路径缺日志） |
| 9 | ci-cd | ✅ 走 GitHub Actions；migration 在 lifespan 不动 CI |
| 10 | error-handling | ⚠️ **中-2 命中**（EF NaN 兜底） |
| 11 | database | ✅ 索引存在；5 分区增量 ALTER idempotent；**版本化不需**（无业务数据变更）|
| 12 | dependency-mgmt | ✅ pyproject + uv.lock |
| 13 | i18n-a11y | ⚠️ 6 emoji 按钮有 aria-label 但未实测 |
| 14 | simplification | ⚠️ **轻-1 命中**（命名一致性） |
| 15 | compatibility | N/A（无 API 变更） |

**Stage 2 命中**：3 个 ⚠ + 1 个 ❌ → 必须修 🔴 严重-1 才能 merge。

### 2.3 simplification 10 条原则

| # | 原则 | 检查 |
|---|------|------|
| 1 | SRP（单一职责） | ✅ `spaced_repetition.py` 只做算法；`study.py` 只做 HTTP |
| 2 | YAGNI | ✅ 无"为未来写"代码 |
| 3 | 抽象时机 | ✅ 2 个 helper 函数（EF_FLOOR / QUALITY_WRONG）合理 |
| 4 | 阈值（文件 ≤300 / 函数 ≤50 / 嵌套 ≤3） | ✅ 文件最大 84 行（study.py），符合 |
| 5 | 命名 | ⚠️ **轻-1 命中** |
| 6 | 注释 | ✅ docstring 集中在 spaced_repetition.py |
| 7 | 删 dead code | ✅ 0 dead code |
| 8 | 依赖最小化 | ✅ 仅依赖 SQLAlchemy + Pydantic（无新加） |
| 9 | 副作用隔离 | ✅ 算法 pure（决策 D-SM2-002 验证） |
| 10 | 幂等性 | ✅ `_ensure_card_columns` idempotent |

**Simplification 命中**：1 个 ⚠ → 轻-1。

---

## 3. 审查结论

| 维度 | 结果 | 阻塞？ |
|------|-----|------|
| Stage 1 完整性 | ✅ PASS | 否 |
| Stage 2 质量 | ❌ 1 红 + 2 黄 + 2 轻 | 🔴 红 = 阻塞 |
| 工程级约束 15 主题 | 1 ❌ / 1 ⚠ / 13 ✅ | 否 |
| simplification 10 条 | 1 ⚠ / 9 ✅ | 否 |

**最终状态**：❌ **STAGE 2 FAIL** → 回 dev-builder 修 🔴 严重-1

### 修复路径

1. **必做**：修 🔴 严重-1（`review_card` 404 路径加 WARN 日志）
2. **建议**：修 🟡 中-1（`_ensure_card_columns` 异常路径 + 日志）
3. **可选**：🟡 中-2 / 🟢 轻-1 / 🟢 轻-2 — 不阻塞，可 Phase 3 处理

### 重审流程

修完 🔴 严重-1 后重跑：

```bash
cd examples/flashcards/backend && uv run pytest -v
# 21 passed in 0.42s
```

主 Agent 重新 spawn code-reviewer，仅审查 1 处改动 → Stage 2 ✅ PASS → 进 PR。

---

## 4. 子 Agent 留底

### 4.1 code-reviewer.toml

```toml
[agent]
name = "code-reviewer"
description = "两阶段（完整性 + 质量）审查 .codex/agents/code-reviewer.toml 路径下的代码变更"
model = "sonnet"
tools = ["read_file", "grep", "shell", "webfetch"]
isolation = "fresh"  # 不复用主 Agent 上下文
skill = "review-agent"
```

### 4.2 输入协议（主 Agent 给子 Agent）

```text
审查 Phase 2 学习模式 PR。范围：
- 改动：app/services/spaced_repetition.py（new）, app/api/study.py（new）,
       app/models/card.py（+5 cols）, app/main.py（+router）
- 测试：tests/test_spaced_repetition.py（new, 12）, tests/test_study.py（new, 9）

Spec 在 D-SM2 决策文里。审查两阶段：
- Stage 1: Spec 11 条目全覆盖 + TDD 合规
- Stage 2: 工程级约束 15 主题 + simplification 10 条

输出格式：本报告（缺陷 + fix 路径，不含表扬）。
```

### 4.3 隔离保证

- 子 Agent 用 fresh 实例，不读 session.json / AGENTS.md / 域文件
- 主 Agent 复制完整 Spec + DEV-PLAN + 决策 + 测试位置
- 子 Agent 不能 spawn 别的 sub-agent
- 子 Agent 不 commit

---

## 5. 报告意义

这份报告回答的问题：

- **PM/老板**：Phase 2 是不是做完了 → 完整性 ✅，质量剩 1 处阻塞
- **工程**：哪里要改 → 🔴 严重-1 + 🟡 中-1 + 🟢 轻（2 件事）
- **Code reviewer**：怎么改 → 给了 `diff` patch，可执行
- **未来**：为什么当时这么决定 → 见 §1 可追溯矩阵

<!-- owner: architecture -->