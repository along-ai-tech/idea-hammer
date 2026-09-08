# 本地闪卡应用

> IdeaHammer 端到端流水线的演示项目

## 项目定位

一个本地运行的闪卡应用，用于学习和记忆任意主题的问答对。目标用户是个人学习者。

## 演示价值

为什么选这个项目作为 IdeaHammer 的首个 example：

| 维度 | 说明 |
|------|------|
| **CRUD 完整** | 卡片的增删改查覆盖后端基础路径 |
| **学习模式** | 翻转卡片、标记掌握度、复习队列——演示状态机 |
| **本地存储** | SQLite，演示数据持久化与 TDD |
| **前后端分离** | Python 后端 + Vue 前端，演示联调、API 设计、跨端 TDD |
| **UI 路径多** | 列表、详情、复习、统计——演示 Element Plus 组件库复用 |
| **小而完整** | 半天到一天能跑完核心 Phase，完整展示 RED-GREEN-REFACTOR 全循环 |

## 预期技术栈（版本待 dev-planner 联网敲定）

### 后端

- **运行时**：Python 3.11+
- **Web 框架**：FastAPI
- **ORM**：SQLAlchemy 2.0
- **数据校验**：Pydantic v2
- **存储**：SQLite
- **包管理**：uv（或 poetry）
- **测试**：pytest + httpx（接口测试）
- **代码质量**：Ruff（lint + format）、mypy（类型检查）

### 前端

- **框架**：Vue 3
- **UI 库**：Element Plus
- **构建**：Vite
- **语言**：TypeScript（strict）
- **状态**：Pinia
- **路由**：Vue Router
- **包管理**：pnpm（或 npm）
- **测试**：Vitest + @vue/test-utils（单元）、Playwright（e2e）
- **代码质量**：ESLint + Prettier

## 预期 Phase 拆分（草稿，待 Spec 敲定后细化）

| Phase | 内容 | 关键文件 |
|-------|------|---------|
| **Phase 1 · 骨架** | Python 后端 + Vue 前端双工程初始化、SQLite schema、pytest + Vitest + Playwright 测试栈、CI 接入钩子 | `backend/`、`frontend/`、根目录配置 |
| **Phase 2 · 后端数据层** | 卡片模型 + Repository + CRUD API + TDD（pytest） | `backend/app/models/`、`backend/app/api/cards.py` |
| **Phase 3 · 后端学习模式** | 翻转、掌握度标记、复习队列 API + TDD | `backend/app/api/study.py`、`backend/app/services/spaced_repetition.py` |
| **Phase 4 · 前端骨架** | Vue3 + Element Plus + 路由 + Pinia + Axios + 前后端联调 | `frontend/src/`、路由配置、API client |
| **Phase 5 · 前端功能页** | 卡片列表、详情、复习界面（CRUD UI + 学习模式 UI） | `frontend/src/views/` |
| **Phase 6 · 统计与可视化** | 学习数据统计、图表展示 | `frontend/src/views/stats/` |
| **Phase 7 · 打包发布** | 后端 wheel 包、前端静态构建、release-builder 出产物 | `dist/`、`release/` |

## 当前状态

⏳ **待启动**——IdeaHammer 骨架审完后，由 product-spec-builder 开启需求澄清。

详细 Product-Spec.md 待补。
