# DEV-PLAN — Personal Blog MVP

> 按 IdeaHammer `dev-planner` 产出：每个 Work Item（WI）独立验收，按 WI 粒度可拆 commit

---

## 0. 目标

按 8 步流水线 product-spec → design → plan → dev → test → review → PR 跑通 MVP：
**9 端点 + 3 模型 + 前端 6 路由 + 39 测试（后端 29 + 前端 10）**，最后产出真 PR 描述 + 可复跑的测试/追踪证据。

## 1. 范围（来自 Spec §2.2）

9 端点 = 博客 CRUD(5) + 置顶(1) + 评论创建/删除(2) + 点赞点踩(1)

| ID | 端点 | Spec |
|----|------|------|
| EP-1 | POST /api/posts | F-2.1 |
| EP-2 | GET /api/posts | F-2.2 |
| EP-3 | GET /api/posts/{id_or_slug} | F-2.3 |
| EP-4 | PUT /api/posts/{id} | F-2.4 |
| EP-5 | DELETE /api/posts/{id} | F-2.5 |
| EP-6 | POST /api/posts/{id}/comments | F-2.6 |
| EP-7 | POST /api/posts/{id}/react | F-2.7 |
| EP-8 | PATCH /api/posts/{id}/pin | F-2.8 |
| EP-9 | DELETE /api/comments/{id} | F-2.9 |

---

## 2. WI 拆解

每 WI 一个 commit。**先 RED，再 GREEN**。

### WI-1 · 项目骨架（脚手架）

| 项 | 详情 |
|---|---|
| **做什么** | `pyproject.toml` + `app/main.py` + `app/db.py` + `app/models/__init__.py` + `tests/conftest.py` + `app/api/health.py` + `/api/health` |
| **依赖** | 无 |
| **关联需求** | 无（范围外：脚手架，不直接交付 REQ） |
| **完成标准** | `uv run uvicorn app.main:app` 起服务；`curl /api/health` 返回 `{status: "ok"}`；`pytest` 跑通 1 个 health 测试 |
| **TDD** | 先写 `test_health.py::test_health_endpoint_returns_ok_status`，跑 FAILED，再写实现 |
| **Commit** | `feat(blog): 项目骨架 + health endpoint` |
| **预估** | 10 分钟 |

### WI-2 · Post 模型 + CRUD（5 端点 + 测试）

| 项 | 详情 |
|---|---|
| **做什么** | `app/models/post.py` (Post ORM) + `app/api/posts.py` (EP-1 ~ EP-5 + EP-8) + `tests/test_posts.py` |
| **依赖** | WI-1 |
| **关联需求** | REQ-001 / AC-001-01 / AC-001-02 / AC-001-03 / REQ-002 / AC-002-01 / AC-002-02 / AC-002-03 / REQ-005 / AC-005-01 |
| **完成标准** | 14 个测试全绿（CRUD + 422 + 404 + 置顶优先排序 + slug 唯一性） |
| **TDD 纪律** | 先 9 个 RED（建文件即失败因为端点不存在），再写实现，再 GREEN，再 REFACTOR 抽 helper |
| **Commit** | `feat(blog): Post 模型 + 5 CRUD 端点 + 置顶（9 测试）` |
| **预估** | 25 分钟 |

### WI-3 · Comment 模型 + 端点（2 端点）

| 项 | 详情 |
|---|---|
| **做什么** | `app/models/comment.py` + `app/api/comments.py` (EP-6 + EP-9) + `tests/test_comments.py` |
| **依赖** | WI-2（需要 post_id 外键） |
| **关联需求** | REQ-003 / AC-003-01 / AC-003-02 / AC-003-03 |
| **完成标准** | 7 个测试全绿（创建 + 422 空内容 + 404 博客不存在 + 删除 + 级联删除） |
| **Commit** | `feat(blog): Comment 模型 + 创建/删除端点（7 测试）` |
| **预估** | 15 分钟 |

### WI-4 · Reaction 模型 + 端点（点赞点踩防重复）

| 项 | 详情 |
|---|---|
| **做什么** | `app/models/reaction.py` + `app/api/reactions.py` (EP-7) + `tests/test_reactions.py` |
| **依赖** | WI-3 |
| **关联需求** | REQ-004 / AC-004-01 / AC-004-02 / AC-004-03 |
| **完成标准** | 7 个测试全绿（点赞 + 点踩 + 同 IP 重复点赞不变计数 + 切换 type + 非法 type + 404） |
| **Commit** | `feat(blog): Reaction 模型 + 点赞点踩防重复（7 测试）` |
| **预估** | 15 分钟 |

### WI-5 · 详情端点（聚合评论 + 点赞数）

| 项 | 详情 |
|---|---|
| **做什么** | 修改 `GET /api/posts/{id_or_slug}` 端点，join 拉评论列表 + 点赞/点踩 count |
| **依赖** | WI-3 + WI-4 |
| **关联需求** | REQ-002 / AC-002-04 |
| **完成标准** | 3 个测试（详情含评论 + 含点赞数 + slug 查询） |
| **Commit** | `feat(blog): 详情端点聚合评论 + 点赞计数（3 测试）` |
| **预估** | 10 分钟 |

### WI-6 · code-reviewer spawn（两阶段审查）

| 项 | 详情 |
|---|---|
| **做什么** | 跑完 WI-5 → spawn code-reviewer.toml（两阶段审查） |
| **依赖** | WI-1 ~ WI-5 全绿 |
| **关联需求** | 无（范围外：质量门，不新增需求） |
| **完成标准** | Stage 1 完整性 ✅ / Stage 2 质量 ✅（含工程级约束 + simplification） |
| **产物** | `Code-Review-Report.md`（真审查产出） |
| **预估** | 5 分钟 |

### WI-7 · PR 描述 + 推送

| 项 | 详情 |
|---|---|
| **做什么** | 写 `PR-Description.md`（实际 PR 描述）+ 给出 WI 与交付物对照表 |
| **依赖** | WI-6 通过 |
| **关联需求** | 无（范围外：交付动作） |
| **完成标准** | PR 描述覆盖需求映射、变更、测试证据、审查结论；39 测试全绿 |
| **预估** | 5 分钟 |

### WI-8 · 前端骨架 + API 客户端

| 项 | 详情 |
|---|---|
| **做什么** | `frontend/`（Vite + Vue3 + Element Plus）+ `src/api/`（fetch 封装 / posts / comments / reactions）+ 路由与布局 |
| **依赖** | WI-2 ~ WI-5（后端契约稳定） |
| **关联需求** | REQ-001 / REQ-002 / AC-001-01 / AC-002-03 |
| **完成标准** | `npm run dev` 起前端；`/api` 代理到 8000；请求错误统一转 `ApiError`；6 条路由可访问 |
| **TDD** | 先写 `client.test.js`（TEST-029）与 `validation.test.js`（TEST-030/031），再补实现 |
| **Commit** | `feat(blog-web): 前端骨架 + API 客户端` |
| **预估** | 20 分钟 |

### WI-9 · 列表页 + 详情页（评论 / 点赞点踩）

| 项 | 详情 |
| --- | --- |
| **做什么** | `HomeView`（置顶优先 + 分页）、`PostDetailView`（正文 / 评论 / 点赞点踩）、`PostCard`、`ReactionBar` |
| **依赖** | WI-8 |
| **关联需求** | REQ-002 / REQ-003 / REQ-004 / AC-002-01 / AC-003-01 / AC-003-02 / AC-004-01 / AC-004-02 |
| **完成标准** | 访客可完成"看列表 → 看详情 → 评论 → 点赞"完整路径；空/加载/错误状态齐全 |
| **TDD** | 先写 `HomeView.test.js`（TEST-033）与 `PostDetailView.test.js`（TEST-034/035），再补实现 |
| **Commit** | `feat(blog-web): 列表页 + 详情页（评论/点赞）` |
| **预估** | 30 分钟 |

### WI-10 · 管理后台（发布 / 编辑 / 删除 / 置顶）

| 项 | 详情 |
| --- | --- |
| **做什么** | `AdminView`（表格 + 置顶 + 删除）、`PostEditorView`（新建 / 编辑） |
| **依赖** | WI-9 |
| **关联需求** | REQ-001 / REQ-005 / AC-001-01 / AC-001-03 / AC-005-01 |
| **完成标准** | 作者可发布、编辑、删除、置顶；表单空值前端拦截；保存后回列表 |
| **TDD** | 先写 `AdminView.test.js`（TEST-036/037）与 `PostEditorView.test.js`（TEST-038），再补实现 |
| **Commit** | `feat(blog-web): 管理后台（发布/编辑/删除/置顶）` |
| **预估** | 25 分钟 |

### WI-11 · 前端测试 + 构建 + 追踪收口

| 项 | 详情 |
| --- | --- |
| **做什么** | 跑通 10 个前端测试；`npm run build`；更新 RELEASE / TRACEABILITY / Product-Spec-CHANGELOG |
| **依赖** | WI-8 ~ WI-10 |
| **关联需求** | REQ-001 / REQ-002 / REQ-003 / REQ-004 / REQ-005 |
| **完成标准** | `npm test` 10 passed；`npm run build` 成功；`check_traceability.py --write` 覆盖前端 TEST |
| **Commit** | `chore(blog): 前端测试 + 构建 + 追踪收口` |
| **预估** | 10 分钟 |

---

## 3. 串并行图

```mermaid
gantt
    title WI 串并行
    dateFormat HH:mm
    section 后端
    WI-1 骨架         :a1, 00:00, 10m
    WI-2 Post CRUD    :a2, after a1, 25m
    WI-3 Comment      :a3, after a2, 15m
    WI-4 Reaction     :a4, after a3, 15m
    WI-5 详情聚合     :a5, after a4, 10m
    section 前端
    WI-8 骨架+API     :b1, after a5, 20m
    WI-9 列表+详情    :b2, after b1, 30m
    WI-10 管理后台    :b3, after b2, 25m
    WI-11 测试+构建   :b4, after b3, 10m
    section 审查+发布
    WI-6 code-review  :crit, a6, after b4, 10m
    WI-7 PR           :a7, after a6, 5m
```

**预计总耗时：175 分钟**（含前后端与审查）

---

## 4. 测试策略

| 层级 | 工具 | 覆盖 |
|------|------|------|
| 后端单元 | pytest | 服务层 helper（slug 生成、reaction 防重） |
| 后端集成 | pytest + TestClient | 9 个端点（29 测试，TEST-001 ~ TEST-028） |
| 前端单元 | Vitest | 校验、反应状态机、API 客户端（TEST-029 ~ TEST-032） |
| 前端组件 | Vitest + Vue Test Utils | 列表 / 详情 / 管理 / 编辑（TEST-033 ~ TEST-038） |
| 端到端 | 手动 | clone → uv sync → pytest → uvicorn → npm install → npm run dev |

**TDD 铁律**：每个 WI 必先 RED（看到 FAILED 才能进 GREEN）。

---

## 5. 风险与缓解

| 风险 | 缓解 |
|------|------|
| slug 冲突（title 重） | slug 加 `-{id}` 后缀 |
| 同 IP 重复点赞 | `UNIQUE(post_id, ip)` 数据库约束 |
| 评论删除后博客评论数显示不一致 | join 时实时 count（性能允许） |
| SQLite 文件没自动建表 | lifespan 启动 `create_all` |
| 已有 SQLite 文件不兼容 | dev 阶段一次性 db，**无迁移场景**（v0 不涉及） |
| 前端跨域 | Vite `server.proxy` / `preview.proxy` 把 `/api` 代理到 8000 |
| 管理端无鉴权被误暴露 | 页面显式警示"仅本机演示"；公网部署前必须加 v1 登录 |

---

## 6. 验收门（Phase 整体完成）

- [x] 39 测试全绿（后端 29 + 前端 10）
- [x] `curl /api/health` 返回 ok
- [x] `curl POST /api/posts` 创建一篇
- [x] `curl GET /api/posts` 返回该博客
- [x] `curl POST /api/posts/1/comments` 加评论
- [x] `curl POST /api/posts/1/react {type:"up"}` 点赞
- [x] `npm run build` 成功产出 `frontend/dist/`
- [x] `check_traceability.py --project examples/personal-blog` 通过
- [x] Code-Review-Report.md 写入 examples/personal-blog/
- [x] PR-Description.md 写入 examples/personal-blog/

---

## 7. 不在 Phase 1 的"以后做"

- **v1.0**：登录 / Markdown / 评论审核 / 标签 / 搜索 / RSS
- **v1.5**：多用户 / 通知 / 邮件订阅
- **永远不做**：广告 / 联盟营销 / 内容付费

---

<!-- owner: architecture -->