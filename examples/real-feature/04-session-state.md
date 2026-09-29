# 04 · Session State 演化 — Phase 2 学习模式

> IdeaHammer 的 `.idea-hammer/session.json` 跨 session 持久化主 Agent 上下文。
> Phase 2 推进过程里，主 Agent 用 `python3 scripts/session.py update` 在 4 个关键节点更新它。
> 本文按时间顺序给 3 个快照，看 session.json 怎么"跟着 Phase 改方向"。

---

## 0. 共识层：schema 在哪

`schemas/session.schema.json` 定义 session.json 结构。所有字段必填 / 可选 / 类型见 schema。

**关键字段**：

| 字段 | 用途 |
|------|------|
| `current_phase` | 当前 Phase（路由入口） |
| `current_task` | 当前任务（Phase 内） |
| `key_decisions` | 跨 session 决策摘要（最近 N 条，避免每次重读 DECISIONS.md） |
| `open_questions` | 阻塞主 Agent 的问题（用户待答） |
| `user_preferences` | 用户偏好（语言 / 技术栈 / commit 风格） |
| `evolution_stats` | 自进化信号消化进度 |

---

## 1. 快照 A · 启动 Phase 2 之前

```json
{
  "schema_version": "1.0",
  "last_updated": "2026-09-09T09:00:00+08:00",
  "current_project": "flashcards",
  "current_phase": "Phase 1 / 1 完成（CRUD 骨架）",
  "current_task": null,
  "key_decisions": [
    {
      "id": "F-001",
      "summary": "本地闪卡应用（学习模式 SM-2 算法）",
      "date": "2026-09-08"
    },
    {
      "id": "F-002",
      "summary": "FastAPI + SQLAlchemy 2.0 + Vue 4.0 + Element Plus",
      "date": "2026-09-08"
    }
  ],
  "open_questions": [],
  "user_preferences": {
    "language": "zh-CN",
    "tech_stack": "Python 3.11 + FastAPI + Vue 4.0 + Element Plus 2.8",
    "testing": "pytest + Vitest"
  }
}
```

**含义**：

- Phase 1 CRUD 跑通，9 测试绿
- 用户偏好：中文、FastAPI + Vue + Element Plus、pytest + Vitest
- 待办空：phase 2 没启动

**体积**：约 750B（精简版 vs 全量域文件 13KB，启动 token 节省 ~94%）。

---

## 2. 快照 B · Phase 2 启动时（dev-planner 完成）

```json
{
  "schema_version": "1.0",
  "last_updated": "2026-09-09T10:30:00+08:00",
  "current_project": "flashcards",
  "current_phase": "Phase 2 / 5 启动（学习模式）",
  "current_task": "WI-2.2 SM-2 算法",
  "key_decisions": [
    {
      "id": "F-001",
      "summary": "本地闪卡应用（学习模式 SM-2 算法）",
      "date": "2026-09-08"
    },
    {
      "id": "F-002",
      "summary": "FastAPI + SQLAlchemy 2.0 + Vue 4.0 + Element Plus",
      "date": "2026-09-08"
    },
    {
      "id": "D-SM2-001",
      "summary": "SM-2 而非 FSRS（成熟 / 实现 60 行 / 复杂度低）",
      "date": "2026-09-09"
    },
    {
      "id": "D-SM2-002",
      "summary": "算法纯函数返回新 Card，不 mutate 入参",
      "date": "2026-09-09"
    }
  ],
  "open_questions": [
    {
      "id": "Q-SM2-001",
      "question": "学习模式要不要 UI（如答题卡片翻转动画）？",
      "options": [
        "只做后端 API，前端 Phase 4+ 再做",
        "Phase 2 一起做前端"
      ],
      "default": "只做后端，前端 Phase 4+"
    }
  ],
  "user_preferences": {
    "language": "zh-CN",
    "tech_stack": "Python 3.11 + FastAPI + Vue 4.0 + Element Plus 2.8",
    "testing": "pytest + Vitest"
  }
}
```

**变化点**：

- `current_phase` 从 "Phase 1 / 1 完成" → "Phase 2 / 5 启动"
- `current_task` 从 null → "WI-2.2 SM-2 算法"（dev-planner 决定先写算法）
- `key_decisions` 加 D-SM2-001（选 SM-2 而非 FSRS）+ D-SM2-002（算法不 mutate）
- `open_questions` 加 Q-SM2-001（前端做不做 / 何时做）

**为什么不是先把 Open Question 解掉就开跑**：dev-planner 按"有依赖的串行、无依赖的并行"拆 6 个 WI，Q-SM2-001 只影响 WI-2.7 前端，不影响 WI-2.1 ~ WI-2.6 后端。先并行后端，前端问题用户当天就答完。

---

## 3. 快照 C · Phase 2 完成（review 通过）

```json
{
  "schema_version": "1.0",
  "last_updated": "2026-09-11T17:00:00+08:00",
  "current_project": "flashcards",
  "current_phase": "Phase 2 / 5 完成（学习模式后端）",
  "current_task": null,
  "key_decisions": [
    {
      "id": "F-001",
      "summary": "本地闪卡应用（学习模式 SM-2 算法）",
      "date": "2026-09-08"
    },
    {
      "id": "F-002",
      "summary": "FastAPI + SQLAlchemy 2.0 + Vue 4.0 + Element Plus",
      "date": "2026-09-08"
    },
    {
      "id": "D-SM2-001",
      "summary": "SM-2 而非 FSRS（成熟 / 实现 60 行 / 复杂度低）",
      "date": "2026-09-09"
    },
    {
      "id": "D-SM2-002",
      "summary": "算法纯函数返回新 Card，不 mutate 入参",
      "date": "2026-09-09"
    },
    {
      "id": "D-SM2-003",
      "summary": "dev 用 lifespan 增量 ALTER 加列，生产留 Alembic",
      "date": "2026-09-09"
    },
    {
      "id": "D-SM2-004",
      "summary": "queue 加 limit=20 防止全表扫",
      "date": "2026-09-09"
    }
  ],
  "open_questions": [],
  "user_preferences": {
    "language": "zh-CN",
    "tech_stack": "Python 3.11 + FastAPI + Vue 4.0 + Element Plus 2.8",
    "testing": "pytest + Vitest"
  }
}
```

**变化点**：

- `current_phase` 从 "启动" → "完成（学习模式后端）"
- `current_task` null（Phase 完成）
- `key_decisions` 多了 D-SM2-003 + D-SM2-004
- `open_questions` 清空（Q-SM2-001 已被答：fronted 推到 Phase 4+）
- Phase 2 后端通过 code-review，进 Phase 3 准备

---

## 4. 4 个 update 时机（主 Agent 何时写 session.json）

来自 AGENTS.md 的 [SESSION-LOAD] 协议：

| 时机 | 字段变化 | 触发示例 |
|------|---------|---------|
| **关键决策后** | 追加 `key_decisions` 条目 | 选 SM-2 vs FSRS 后 |
| **Phase 推进时** | 更新 `current_phase` / `current_task` | Phase 1 完成 → Phase 2 启动 |
| **关键约束发现时** | 追加 `open_questions` 或清除 | 用户问"前端要不要做" |
| **evolution 消化后** | 更新 `evolution_stats` | session 启动扫 signals 后 |

---

## 6. 为什么 session.json 是精简版（不是完整 Spec）

| 维度 | session.json | 完整 Product-Spec.md |
|------|--------------|---------------------|
| 体积 | ~840B（4 个决策） | ~6KB |
| 内容 | 摘要 + 决策指针 | 11 节 + 4 个纪律产物 |
| 启动时读取 | ✅ 全量 | ❌ 按需 |
| 写入时机 | 关键节点 | Phase 推进时 |

**原则**：

- session.json 给主 Agent **上下文骨架**（"现在在哪 / 最近做了什么决定"）
- 完整 Spec 在 `Product-Spec.md`（主 Agent 按 `current_phase` 按需读）
- DECISIONS.md 是 Why 留底（session.json 只放"决策标题"）

---

## 7. session.json vs 全量读域文件节省多少

按 AGENTS.md 验收标准：

- session.json 精简版 ≈ 1KB
- 域文件（IDENTITY + WORKFLOW + SKILLS + SUBAGENTS + STATE-ROUTING + TESTING）≈ 13-15KB

启动 token 节省 ≥ 30%，实测 85%+。

为什么能省这么多：域文件内容**基本不变**（主 Agent 已读过），只有 session.json 必须重新过（因为上次对话后用户改了 phase / 偏好）。

<!-- owner: product -->