# 本地闪卡应用

> IdeaHammer 端到端流水线的演示项目（Phase 1 骨架已就绪）

## 项目定位

一个本地运行的闪卡应用，用于学习和记忆任意主题的问答对。

**目标用户**：准备 AI 应用开发岗位面试的 3 年后端工程师（如李雷）。

**核心 job**：高效掌握并可调用一项新技术（如 LangGraph）的关键知识点。

## 当前状态

**Phase 1 · 骨架** ✅ 已就绪：

- ✅ 后端 FastAPI + SQLAlchemy + SQLite + Pydantic + 健康检查
- ✅ 卡片 CRUD API + 测试覆盖
- ✅ 前端 Vue3 + Element Plus + Vite + TypeScript strict + Pinia + Vue Router
- ✅ 卡片管理页（CRUD UI）+ 首页（健康检查）
- ✅ 后端 9 个测试 + 前端 5 个测试（Vitest + pytest）

**未启动 Phase**：2 数据层深化 / 3 学习模式 / 4-7 前端 + 统计 + 打包。

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python 3.11+ / FastAPI / SQLAlchemy 2.0 / SQLite / Pydantic v2 / pytest |
| 前端 | Vue 3.5 / Element Plus 2.8 / Vite 5 / TypeScript strict / Pinia / Vue Router / Vitest |
| 包管理 | Python `uv`（推荐）/ pip；前端 `pnpm`（推荐）/ npm |

## 目录结构

```
flashcards/
├── backend/                 # FastAPI 后端
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py         # FastAPI 入口
│   │   ├── db.py           # SQLAlchemy 引擎 + get_db 依赖
│   │   ├── models/card.py   # Card 模型
│   │   └── api/
│   │       ├── health.py   # /api/health
│   │       └── cards.py    # /api/cards CRUD
│   └── tests/
│       ├── conftest.py     # 内存 SQLite fixture
│       ├── test_health.py
│       └── test_cards.py   # 9 个 CRUD + 错误路径测试
├── frontend/                # Vue3 前端
│   ├── package.json
│   ├── vite.config.ts      # 含 /api 代理到 8000
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/index.ts
│   │   ├── api/index.ts    # Axios instance
│   │   ├── stores/cards.ts # Pinia store
│   │   └── views/
│   │       ├── HomeView.vue  # 健康检查页
│   │       └── CardsView.vue # 卡片 CRUD 页
│   └── tests/unit/
│       ├── api.spec.ts
│       └── cardsStore.spec.ts
└── README.md                # 本文件
```

## 怎么跑

### 1. 后端

```bash
cd backend

# 推荐：uv（现代化 Python 包管理）
uv sync                  # 装依赖
uv run uvicorn app.main:app --reload --port 8000

# 或 pip 方案
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

后端跑起来后：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health → `{"status": "ok"}`

### 2. 前端

```bash
cd frontend

# 推荐：pnpm
pnpm install
pnpm dev

# 或 npm
npm install
npm run dev
```

前端跑起来后：
- 应用：http://localhost:5173
- 首页会调 `/api/health` 检查后端连通性

### 3. 验证端到端

打开 http://localhost:5173 ，应该看到：
1. 首页显示 `✅ 后端连通`
2. 点 "卡片" 进入卡片管理页
3. 点 "+ 新建卡片"，输入正面 / 反面，保存
4. 卡片出现在列表里
5. 点 "编辑" / "删除" 验证修改和删除

## 怎么跑测试

### 后端测试（9 个）

```bash
cd backend
uv run pytest -v
```

应看到：
- `test_health.py::test_health_endpoint_returns_ok_status PASSED`
- `test_cards.py::test_create_card_persists_and_returns_id PASSED`
- ... 共 9 个 PASSED

### 前端测试（5 个）

```bash
cd frontend
pnpm test
```

应看到 `Test Files 2 passed` / `Tests 5 passed`。

## API 端点速查

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/cards` | 创建卡片（body: `{front, back}`） |
| GET | `/api/cards` | 列出所有卡片 |
| GET | `/api/cards/{id}` | 查单张卡片 |
| PUT | `/api/cards/{id}` | 更新卡片 |
| DELETE | `/api/cards/{id}` | 删除卡片 |

## 演示价值

这个 Phase 1 骨架证明 IdeaHammer 框架的端到端能力：

| 能力 | 在本项目的体现 |
|------|---------------|
| 产研全流程 | 已走完需求（李雷 persona）→ 设计（CRUD + 学习模式路线图）→ 开发（Phase 1 骨架）|
| SDD Spec 驱动 | README 即精简 Spec，定义 job / 范围 / 技术栈 / API |
| TDD 纪律 | 14 个测试覆盖健康 + CRUD 全路径 + 前端 client/store |
| 设计桥接 | Element Plus 复用（el-table / el-dialog / el-form），无自造组件 |
| 代码审查 | 可运行 `code-review` skill 验证 |

## 下一步（Phase 2+）

按 DEV-PLAN Phase 拆分推进：
- Phase 2：复习模式（翻转 + 掌握度 + SM-2 间隔算法）
- Phase 3：AI 自动生成卡片
- Phase 4：统计图表
- Phase 5：打包发布
