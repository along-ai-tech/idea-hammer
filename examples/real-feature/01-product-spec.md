# 01 · Product Spec — 学习模式（Phase 2 增量学习模式 - SM-2 间隔重复算法）

> 这是 `examples/flashcards/Product-Spec.md` 的 Phase 2 章节抽取 + 必要的 Phase 0/1.5/3.5/收尾纪律产物。
> 完整 Spec 在仓库里，本文聚焦 SM-2 学习模式怎么写 Spec。

---

## 一句话业务需求

> "我想做一个本地闪卡应用，准备 AI 应用岗面试。"

经 product-spec-builder 追问 + Phase 0/1.5/3.5/收尾 4 个纪律环节后，
需求被锤成 **Phase 2 学习模式**：用 SM-2 间隔重复算法帮用户最少次数记住最多卡片。

---

## 0. Phase 0 · 商业可行性 5 问快筛（business-context-check）

| # | 问 | 答（用户原话压缩） | 通过？ |
|---|----|----------------------|-------|
| 1 | **凭什么你活** | 市面 Anki 太重（云账号 / 插件生态 / 学习曲线陡），我只想本地、能用、3 分钟上手 | ✅ |
| 3 | **1 年后死在哪** | 用户懒得维护卡片库就跑了。缓解：本应用零运维（SQLite 本地），后期可加 AI 自动生成 | ✅ |
| 5 | **是否可发布** | v0.1 自用工具，能跑通 8 步流水线即可。商业价值低，**方法论价值高** | ✅ |

→ Phase 0 通过，进 Phase 1 核心功能。

---

## 1. Phase 1 · 核心功能 + persona + job

**Persona**：李雷，3 年后端工程师，准备 AI 应用岗面试。

**核心 job**：高效掌握并可调用一项新技术（如 LangGraph）的关键知识点。

**Phase 2 学习模式 job**：每次复习一张卡片，按"答得好不好"动态排下次时间，少间隔点不漏。

**Phase 2 必须解决**：

- 用户已经加好一堆卡片（Phase 1）但不知道怎么"用"它们
- 用户答完一张卡不知道"什么时候再答"
- 用户答错的卡片应该被更频繁拉回来

---

## 1.5. Phase 1.5 · 竞品扫描（competitive-scan）

| 类型 | 竞品 | 我们凭什么 |
|------|------|-----------|
| **直接** | Anki | 太重（云账号 / 插件 / 学习曲线）。我们：零运维、本地 SQLite、3 分钟上手、SM-2 直接可用 |
| **直接** | Quizlet 网页版 | 要账号、要联网、有广告。我们：纯本地、纯文本对记忆 |
| **替代** | Notion 表格手抄"问答对" | 没复习调度。我们：SM-2 自动排时间 |
| **替代** | 备忘录随便写 | 完全没结构。我们：CRUD + 复习 + 统计一体 |

---

## 2. Phase 2 · 学习模式 — 范围定义

### 2.1 用户故事

> 作为 **李雷（3 年后端工程师）**
> 我想要 **开始一次"复习 session"，系统按 SM-2 给我排 20 张到期卡片**
> 以便 **我按顺序翻面、给质量评分 0-5（完全忘记→完美回忆）**
> 然后 **系统记下我的表现，下次自动给我安排这张卡什么时候再出现**

---

## 2.2 功能列表 + 验收标准（"什么 break 让它失败"）

> 验收每条都写成"如果 break，哪条测试挂"。TDD 协议起点。

| ID | 功能 | 验收（=测试场景） |
|----|----|----------------|
| F-2.1 | 拉取待复习队列 | 给定：3 张卡 due_at 是未来 7 天，2 张卡 due_at 是过去 1 小时；当：GET /api/study/queue；应：返回 2 张（按 due_at 升序） |
| F-2.2 | 队列包含 due_at=NULL | 给定：从未复习过的卡（due_at 仍为 NULL）；当：GET /api/study/queue；应：返回该卡 |
| F-2.3 | 提交复习 quality=3 | 给定：从未复习过的卡；当我 POST /review 接口 quality=3；应：repetitions=1, interval=1, due_at=now+1 天 |
| F-2.4 | 提交复习 quality=0 | 给定：已复习过 2 次的卡；当我 POST /review 接口 quality=0；应：repetitions=0（重置）, interval=1 |
| F-2.5 | EF 难度系数 floor | 给定：EF=1.999 的卡连续答错；应：EF 不破 1.3 |
| F-2.6 | EF 完美回答 +0.1 | 给定：EF=2.5, quality=5；应：新 EF=2.6 |
| F-2.7 | due_at 调度 | 给定：quality=3, repetitions=0；应：due_at = now + 1 天（±1s） |
| F-2.8 | 不修改入参 | 算法应返回新 Card 实例，不 mutate 入参 |
| F-2.9 | quality 越界 | quality=6 应抛 ValueError（service 层）+ 422（HTTP 层） |
| F-2.10 | 学习统计 | GET /study/stats 返回 {due_now, total, learned} 三个计数 |
| F-2.11 | 404 处理 | review 不存在的卡片返回 404（非 500） |

---

## 2.3 范围之外（v0 不做）

- AI 自动生成卡片（Phase 3）
- 多设备同步（永远不做）
- 复习统计图表（Phase 4+）
- 标签 / 分类（v1+）
- 图片 / 音频卡（永远不做，本地 MVP）
- 用户账号系统（永远不做，本地单用户）

---

## 3. Phase 3.5 · pre-mortem（question-bank）

> 假设 1 年后这个 Phase 死透了，回溯可能是哪 3 个原因 + 监控信号。

| 1 年后死因 | 监控信号 | 缓解（已做 / 待做） |
|-----------|---------|------------------|
| **1. SM-2 在多卡场景下发 N+1 查询** | 单次 /study/queue 在 1000 张卡时 >500ms | 已加 limit=20，避免全表扫；v1 加覆盖索引 `(due_at, id)` |
| **2. EF 越界 bug 让某张卡永远不出现** | 某张卡复习次数 >10 但从不进队列 | EF floor=1.3 保证；测试覆盖 EF=1.999 答错 → 仍 ≥ 1.3 |
| **3. 时区切换导致 due_at 跳变** | 用户改系统时区后 /study/stats 突变 | 用 `datetime.utcnow()` 不带时区；v1 改 timezone-aware |

---

## 4. 收尾多视角自检（ceo-lens / eng-lens / qa-lens）

### CEO 视角：方向对吗？

- ✅ 这个 Phase 解的是真问题（用户怎么"用"卡片，不是"管"卡片）
- ✅ 与 Phase 1（CRUD）衔接自然
- ⚠️ 用户可能不熟悉 SM-2 → UI 要解释"为什么今天还要答这张"

### 工程视角：能实现吗

- ✅ 算法成熟（Wozniak 1985），Anki 早期默认
- ✅ 数据模型 5 个新字段（repetitions / interval / easiness_factor / due_at / last_reviewed_at）
- ⚠️ 数据库迁移：Phase 1 的 SQLite 文件已有，需 ALTER 增量加列
- ✅ 3 个 API 端点，全部 Pydantic v2 + SQLAlchemy 2.0

### QA 视角：能测吗

- ✅ 21 个测试用例（12 算法 + 9 API）
- ✅ 边界：quality=0/3/5、EF floor、quality=6 越界
- ✅ 集成：TestClient + in-memory SQLite fixture
- ⚠️ E2E 暂不做（无浏览器自动化预算）

---

## 5. 非功能需求

| 维度 | 要求 |
|------|------|
| **性能** | /study/queue 响应 P99 < 200ms（1000 张卡内） |
| **可用性** | 单一用户本地运行，无 SLA |
| **可观测** | 学习 stats endpoint，不打 error log（除非 5xx） |
| **国际化** | 文案中文先放（local-only） |
| **可移植** | Python 3.11+ / FastAPI 0.110+ / SQLAlchemy 2.0+ |
| **数据迁移** | 已有 SQLite 文件兼容（ALTER 增量加列） |
| **版本化** | 不涉及业务数据变更，无需 versioning |

---

## 6. 验收总表（Spec → 实现可追溯）

| Spec 条目 | 实现位置 | 测试位置 |
|----------|---------|---------|
| F-2.1 队列按 due_at 升序 | `study.py::get_study_queue` | `test_study_queue_excludes_cards_due_in_future` |
| F-2.2 due_at=NULL 包含 | 同上 + `or_(due_at.is_(None))` | `test_study_queue_includes_never_reviewed_cards` |
| F-2.3 ~ F-2.9 SM-2 算法 | `spaced_repetition.py` | `test_spaced_repetition.py` 12 个 |
| F-2.10 统计 | `study.py::get_study_stats` | `test_study_stats_returns_counts` |
| F-2.11 404 | `study.py::review_card` raise HTTPException 404 | `test_review_nonexistent_card_returns_404` |

<!-- owner: product -->