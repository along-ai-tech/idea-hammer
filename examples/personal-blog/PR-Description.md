# feat(blog): Personal Blog MVP（前后端 + 需求追踪）

## 摘要

按 IdeaHammer 8 步流水线从零到一交付一个可运行的个人博客 MVP：

- **后端**：FastAPI + SQLAlchemy + SQLite，9 个 REST 端点
- **前端**：Vue 3 + Element Plus + Vite，6 条路由
- **测试**：39 个（后端 29 + 前端 10），全部通过
- **追踪**：REQ → AC → DT → TEST → v1.0.0 全链路可查

## 需求映射

| 需求 | 用户价值 | 实现 | 验收标准 | 测试 |
|---|---|---|---|---|
| REQ-001 | 发布 / 编辑 / 删除博客 | `backend/app/api/posts.py` + `frontend/src/views/PostEditorView.vue` | AC-001-01/02/03 | TEST-001/002/003/009/010/031/037/038 |
| REQ-002 | 列表（置顶优先）/ 详情 | `list_posts` + `get_post` + `HomeView` | AC-002-01/02/03/04 | TEST-004 ~ 008、012 ~ 014、033 |
| REQ-003 | 评论创建 / 删除 | `backend/app/api/comments.py` + `PostDetailView` | AC-003-01/02/03 | TEST-015 ~ 021、030、034 |
| REQ-004 | 点赞 / 点踩（防重复） | `backend/app/api/reactions.py` + `ReactionBar` | AC-004-01/02/03 | TEST-022 ~ 028、032、035 |
| REQ-005 | 置顶 / 取消置顶 | `toggle_pin` + `AdminView` | AC-005-01 | TEST-011、036 |

完整矩阵见 [TRACEABILITY.md](./TRACEABILITY.md)。

## 变更内容

### 后端

- `posts` / `comments` / `reactions` 三张表 + 级联删除
- 9 个端点：CRUD、分页、置顶优先、详情聚合评论与点赞数、评论创建/删除、点赞点踩
- Pydantic 入参校验（title ≤ 200、nickname ≤ 50、content ≤ 5000）
- `selectinload` 避免详情 N+1；SQLite `PRAGMA foreign_keys=ON` 保证级联
- 同 IP 点赞去重 + 切换 type 的 toggle 语义

### 前端

- `/`、`/posts`：列表（置顶标记、分页、空/加载/错误状态）
- `/posts/:id`：详情、评论提交、点赞点踩（乐观更新 + 失败回滚）
- `/admin`：文章管理（编辑 / 置顶 / 删除）
- `/admin/new`、`/admin/posts/:id/edit`：发布与编辑
- 纯函数抽离：`validation.js`、`reaction.js`、`format.js`，便于单测
- Vite `server.proxy` / `preview.proxy` 把 `/api` 代理到 8000

### 文档与追踪

- `Product-Spec.md` / `Design-Brief.md` / `DEV-PLAN.md`
- `Code-Review-Report.md`（两阶段审查 + 返工记录）
- `RELEASE.json` / `TRACEABILITY.md`
- 测试注解：`# @trace`（pytest）/ `// @trace`（Vitest）

## 测试证据

```bash
# 后端
cd backend && uv run pytest -q
# 29 passed

# 前端
cd frontend && npm test
# 10 passed (7 files)

# 前端构建
npm run build
# ✓ built

# 需求追踪
python3 scripts/check_traceability.py --project examples/personal-blog --strict
# ✅ 追踪链路通过（strict），警告 0 个
```

## 两阶段审查

| 阶段 | 结论 | 关键记录 |
|---|---|---|
| Stage 1 完整性 | ✅ PASS | 首轮发现 F-2.3 详情聚合缺失（HIGH）→ WI-5 返工 → 复审 PASS |
| Stage 2 质量 | ✅ PASS | 文件/函数阈值、N+1、SQL 注入、XSS、TDD 真实性均通过 |
| 前端复审 | ✅ PASS | 6 路由对齐 Design-Brief；10 测试全绿；无 `v-html` / 硬编码密钥 |

## 如何验证

```bash
# 1. 后端
cd examples/personal-blog/backend
uv sync --extra dev && uv run pytest -q
uv run uvicorn app.main:app --reload

# 2. 前端（另开终端）
cd ../frontend
npm install && npm test && npm run dev
```

浏览 `http://127.0.0.1:5173`：

1. 首页看到空列表 → 去 `/admin/new` 发布一篇
2. 回首页看到文章 → 进详情写评论、点赞
3. 去 `/admin` 置顶 / 删除

## 范围外（v1）

- 登录 / 权限、Markdown 渲染、评论审核、标签 / 搜索 / RSS
- 多用户、通知、邮件订阅

## v0 已知边界

- 管理端**无鉴权**，仅本机演示，请勿直接暴露公网
- 正文按纯文本存储与展示，避免 XSS
- 单机 SQLite，点赞按 `IP + post_id` 去重

## Checklist

- [x] 所有 P0 需求实现并有 AC 覆盖
- [x] 后端 29 / 前端 10 测试全绿
- [x] `check_traceability.py` 通过
- [x] 两阶段审查 PASS
- [x] `RELEASE.json` 覆盖全部 P0 需求与测试 ID
- [x] 前端 `npm run build` 成功
- [x] v0 边界写入 README / Spec
