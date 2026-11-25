# Personal Blog — IdeaHammer 从 0 到 1 完整案例

> 按 IdeaHammer 8 步流水线真跑出来的一条完整链路：
> **需求 → Product-Spec → Design-Brief → DEV-PLAN → TDD 代码 → 两阶段审查 → 发布清单 → 需求追踪矩阵**。
> 前后端都可运行，测试可复跑，每个功能都能回溯到 REQ / AC / DT / TEST / 版本。

---

## 30 秒看懂：8 步各自留下了什么

| 步骤 | Skill | 本案例产物 | 能验证什么 |
|---|---|---|---|
| ① 需求澄清 | product-spec-builder | [Product-Spec.md](./Product-Spec.md) | 5 条 P0 REQ、13 条 AC、9 个端点、竞品与反假设 |
| ② 产品规范 | product-spec-builder | [Product-Spec.md](./Product-Spec.md) | 单一真相源：范围 / 用户任务 / 流程 / 数据模型 |
| ③ 设计简报 | design-brief-builder | [Design-Brief.md](./Design-Brief.md) | 路由、线框、状态机、反 UI 假设、错误码 |
| ④ 设计稿 | design-maker | 复用 Element Plus（见 Design-Brief §6） | 无设计稿场景下如何约束 UI 一致性 |
| ⑤ 开发计划 | dev-planner | [DEV-PLAN.md](./DEV-PLAN.md) | WI/DT 拆分、每 WI 验收标准、TDD 纪律 |
| ⑥ TDD 开发 | dev-builder | [backend/](./backend/) + [frontend/](./frontend/) | RED → GREEN → REFACTOR，39 个测试 |
| ⑦ 两阶段审查 | code-reviewer | [Code-Review-Report.md](./Code-Review-Report.md) | Stage 1 完整性 + Stage 2 工程质量，含返工记录 |
| ⑧ 构建发布 | release-builder | [RELEASE.json](./RELEASE.json) | 版本、需求清单、测试全绿、变更记录 |
| 贯穿 | — | [TRACEABILITY.md](./TRACEABILITY.md) | REQ → DT → TEST → 版本的完整追踪矩阵 |

---

## 5 分钟跑起来

### 后端（FastAPI + SQLite，9 个端点）

```bash
cd backend
uv sync --extra dev          # 没有 uv：python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
uv run pytest -q             # 29 passed
uv run uvicorn app.main:app --reload
```

另开终端验证：

```bash
curl http://127.0.0.1:8000/api/health
curl -X POST http://127.0.0.1:8000/api/posts \
  -H 'Content-Type: application/json' \
  -d '{"title":"第一篇","content":"Hello IdeaHammer"}'
curl http://127.0.0.1:8000/api/posts
```

### 前端（Vue 3 + Element Plus + Vite）

```bash
cd frontend
npm install
npm run dev                  # http://127.0.0.1:5173，/api 已代理到 8000
```

打开后可走完整用户路径：

1. `/` 或 `/posts`：列表（置顶优先、分页）
2. `/posts/:id`：详情、评论、点赞 / 点踩
3. `/admin`：文章管理（编辑 / 置顶 / 删除）
4. `/admin/new`、`/admin/posts/:id/edit`：发布与编辑

### 前端测试与构建

```bash
cd frontend
npm test                     # 10 passed（Vitest + Vue Test Utils）
npm run build                # 产物在 dist/
```

> 生产部署：把 `dist/` 与后端同源托管即可；若前后端分域，构建时设置
> `VITE_API_BASE=https://your-api.example.com`，`src/api/client.js` 会自动拼接。

---

## 需求追踪怎么查

```bash
# 在仓库根目录执行
python3 scripts/check_traceability.py --project examples/personal-blog
python3 scripts/check_traceability.py --project examples/personal-blog --strict   # 发布门禁
python3 scripts/check_traceability.py --project examples/personal-blog --impact REQ-003
python3 scripts/check_traceability.py --project examples/personal-blog --write examples/personal-blog/TRACEABILITY.md
```

它会校验：

- 每个 P0 REQ 是否有 TASK / AC / DT / TEST
- 测试注解 `@trace TEST-### REQ-###/AC-###-##` 是否指向真实需求
- RELEASE.json 是否覆盖全部 P0 需求且测试全绿
- 重复 ID、悬空 ID、未进发布清单的 P0 需求

---

## 这个案例演示了哪些方法论

1. **反模糊**：先写 5 条 P0 REQ + 13 条 Given/When/Then AC，再动代码。
2. **反假设**：Design-Brief §4 明确拒绝评论分页、富文本、点赞动画、登录后台四个"看起来该做"的方案。
3. **行业标杆参考**：Spec §1.7 / §1.8 对照 Hexo、Halo、WordPress、Notion 等，逐行写清契合点、需定制点与原创点。
4. **TDD 铁律**：每个 WI 先写失败测试；后端 29 个测试、前端 10 个测试都可用一条命令复跑。
5. **两阶段审查**：Code-Review-Report 记录了 Stage 1 发现 F-2.3 详情聚合缺失 → WI-5 返工 → 复审 PASS 的完整闭环。
6. **工程约束**：Pydantic 校验、SQLAlchemy 表达式查询、`selectinload` 防 N+1、前端纯函数拆分状态机与校验。
7. **发布与追踪**：RELEASE.json 把版本、需求、测试绑定；TRACEABILITY.md 可回答"这个功能来自哪、被谁实现、被哪些测试覆盖、进了哪个版本"。

---

## 代码地图

```text
examples/personal-blog/
├── Product-Spec.md              # ② 需求单一真相源
├── Design-Brief.md              # ③ 设计与状态机
├── DEV-PLAN.md                  # ⑤ WI/DT 计划 + 验收门
├── Code-Review-Report.md/.json  # ⑦ 两阶段审查
├── RELEASE.json                 # ⑧ 发布清单
├── TRACEABILITY.md              # 追踪矩阵（脚本生成）
├── PR-Description.md            # 交付说明
├── backend/
│   ├── app/api/                 # posts / comments / reactions / health
│   ├── app/models/              # Post / Comment / Reaction
│   └── tests/                   # 29 个 pytest 测试（含 @trace）
└── frontend/
    ├── src/api/                 # fetch 封装 + 资源 API
    ├── src/utils/               # 校验 / 反应状态机 / 格式化（纯函数）
    ├── src/views/               # 列表 / 详情 / 管理 / 编辑
    └── src/**/*.test.js         # 10 个 Vitest 测试（含 @trace）
```

---

## v0 边界（有意不做）

- **无登录**：管理端仅本机演示，请勿直接暴露公网；登录在 v1。
- **正文纯文本**：不渲染 Markdown，避免 XSS；markdown-it + DOMPurify 在 v1。
- **单机 SQLite**：点赞/点踩按 `IP + post_id` 去重，适合单进程演示。
- **无评论审核 / 搜索 / RSS**：均在 Spec §2.2 的 OUT 列表中，明确不做。

---

## 想复用到自己的项目

1. 复制 8 步产物结构，先写 `Product-Spec.md`（需求 + AC）。
2. 用 `dev-planner` 拆 `DEV-PLAN.md`，每个 DT 标注 `关联需求: REQ-xxx / AC-xxx-xx`。
3. 写测试时加 `@trace TEST-### REQ-###/AC-###-##`。
4. 发布前生成 `RELEASE.json` 并跑 `check_traceability.py`。
5. 把 `TRACEABILITY.md` 作为 PR 的"需求覆盖证据"。
