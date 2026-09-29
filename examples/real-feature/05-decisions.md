# 05 · 关键决策记录（Phase 2 学习模式）

> 这是 `DECISIONS.md` 里 Phase 2 章节的 WHY 留底。每条决策都带候选对比 + 拒绝理由 + 影响范围。
> 目的：换同事 / 换电脑 / 换 AI 模型都能理解历史决策，避免重蹈覆辙。

---

## D-SM2-001 · 算法选型：SM-2 而非 FSRS

**背景**：要实现间隔重复，可选 SM-2（Wozniak 1985）或 FSRS（Jarrett 2023）。

**候选**：

| 方案 | 成熟度 | 实现复杂度 | 用户感知 | 维护成本 |
|------|------|---------|--------|---------|
| **A. SM-2** | ✅ 40 年历史，Anki 早期默认 | 60 行 Python | 用户不感知 | 0（无状态） |
| **B. FSRS** | ⚠️ 1 年新算法 | 200+ 行 + 依赖矩阵 | 用户不感知 | 中（需要训练数据） |
| **C. 固定间隔（如 1/3/7/30 天）** | ✅ 极简 | 100 行 | 用户感知（"为什么今天要答"） | 0 |

**决定**：A

**理由**：

- 本地单用户，无训练数据，FSRS 优势发挥不出
- SM-2 实现 ≤ 60 行，12 测试能完整覆盖边界
- "用户感知差异" 对本地 MVP 不重要
- Phase 4+ 可平滑替换（纯函数接口不变）

**影响**：

- `app/services/spaced_repetition.py` 新增 1 个 pure 函数
- `Card` 加 5 字段
- 测试 12 个

---

## D-SM2-002 · 算法纯函数返回新 Card，不 mutate 入参

**背景**：SM-2 算法可以原地 mutate 或返回新对象。

**候选**：

| 方案 | 测试性 | 副作用隔离 | idempotency | 性能 |
|------|------|---------|------------|------|
| **A. 纯函数 / 返回新 Card** | ✅ 易写 | ✅ 无 | ✅ 强 | N+1 次构造 |
| **B. mutate 入参** | ⚠️ 需 mock db | ❌ 有 | ❌ 重跑破坏 | 单次 UPDATE |

**决定**：A

**理由**：

- 简化之道第 3 条（pure functions 优先）：算法本身是纯计算
- 测试覆盖 `test_original_card_is_not_mutated` 强制约束
- API 层负责 commit (review_card 端)
- 性能：单次构造 ORM 对象，开销 < 1ms，可接受

**影响**：

- `calculate_next_review` 不调 db
- API 层显式赋值 + db.commit + db.refresh

---

## D-SM2-003 · 数据库迁移：dev 用 lifespan 增量 ALTER，生产留 Alembic

**背景**：Phase 1 已有 SQLite 文件 3 列（id/front/back），Phase 2 加 5 列。

**候选**：

| 方案 | 适用阶段 | 风险 |
|------|--------|------|
| **A. lifespan 启动时增量 ALTER** | dev / 单用户 | 生产多进程会竞态 |
| **B. 一次性手动 SQL** | dev 一次性 | Phase 3 再加字段还得手动 |
| **C. 引入 Alembic** | 生产 | 增加依赖，Phase 2 还没生产 |

**决定**：A（短期）+ C（v1+）

**理由**：

- 单用户本地应用，无并发启动
- 增量 ALTER idempotent（启动检查列存在性，缺啥补啥）
- Phase 2 后写一段注释明确"生产用 Alembic"
- 引入 Alembic 是 v1+ 的事，不在 Phase 2 scope

**影响**：

- `main.py::lifespan` 加 1 个 helper 函数（30 行）
- 注释明确"Alembic 是生产路径"
- 测试覆盖：现有 SQLite 文件启动不报错

---

## D-SM2-004 · 队列查询加 limit=20 防全表扫

**背景**：复习时一次拉几张卡。

**候选**：

| 方案 | UX | 性能（1000 张卡） | 性能（100 张卡） |
|------|----|------------------|------------------|
| **A. 全量返回** | 用户可滚动选 | ⚠️ O(N) + 内存 | ✅ |
| **B. limit=20 一次** | 一次答 20 张 | ✅ | ✅ |
| **C. 分页** | UX 复杂 | ✅ | ✅ |

**决定**：B

**理由**：

- SM-2 推荐 20-30 张/次（认知科学共识）
- 本地 SQLite 无需分页（≤1000 张）
- 测试明确断言 `len(queue) <= 20`

**影响**：

- `get_study_queue(limit=20)` 默认参数
- 前端假设每次答完即拉新队列（无客户端分页）

---

## D-SM2-005 · quality 校验双层（service ValueError + Pydantic 422）

**背景**：复习接口接 `{quality: 0-5}`。

**候选**：

| 方案 | 防御深度 | 测试性 |
|------|--------|------|
| **A. 仅 Pydantic 422** | 仅 HTTP 边界 | ⚠️ 单元测试无法触发（HTTP 层） |
| **B. 仅 service ValueError** | 仅服务层 | ⚠️ HTTP 层 500 漏出 |
| **C. 双层（HTTP 422 / service ValueError）** | ✅ | ✅ 都测 |

**决定**：C

**理由**：

- 简化之道深黑原则：边界校验靠框架 + 业务校验靠算法
- service ValueError 让 12 算法单元测试能直接覆盖边界
- Pydantic 422 让 9 API 集成测试能验证 HTTP 层
- 不重复 = 在中间层只做一次校验（算法层 OR HTTP 层选其一）

**影响**：

- `spaced_repetition.py` 头部 `if quality < 0 or quality > 5: raise ValueError`
- `study.py` Pydantic `Field(ge=0, le=5)` + `HTTPException(400)` 兜底
- 2 个测试覆盖：service 抛 ValueError + HTTP 422

---

## D-SM2-006 · SM-2 字段不存"上次答对的 quality"

**背景**：SM-2 EF 公式需要 `q` 才能算下次 EF。

**候选**：

| 方案 | 数据量 | 可还原性 |
|------|------|---------|
| **A. 存 q** | +1 列 | 100% 还原 |
| **B. 不存 q（用 last_reviewed_at 推断）** | 0 | ❌ 丢数据 |

**决定**：A

**理由**：

- 不存 q → 调试 / A/B 测试 / 统计难做
- 本地 SQLite 列成本 = 0
- 与 versioning-and-immutability 对齐：历史决策不丢

**影响**：

- `Card` 模型加 `last_quality: int` 字段（Phase 2 暂未实现，留 Phase 3）
- 注：Phase 2 暂不需要，决策先留底，v0.8+ 再加

---

## 决策如何被使用

| 时机 | 谁来读 |
|------|------|
| Phase 启动 | 主 Agent 通过 session.json 查关键决策 |
| 变更需求 | 主 Agent 查 DECISIONS.md，找历史决策的 WHY，看是否矛盾 |
| 1 年后回看 | 主 Agent / 人类同事查 DECISIONS.md |
| 招新人 | 文档入口在 README 末尾"贡献"段 |

---

## 决策的反例（不能这么写）

❌ **只写 WHAT 不写 WHY**：

```markdown
## D-X · 选 SM-2
我们选 SM-2 算法。
```

✅ **完整**：

```markdown
## D-X · 选 SM-2 而非 FSRS
背景 / 候选对比 / 决定 / 理由 / 影响
```

❌ **决定无影响范围**：

写完决定后没写"哪些文件改了 / 多少行 / 哪些下游受牵连"。

<!-- owner: architecture -->