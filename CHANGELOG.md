# 变更日志

本项目的所有重要变更记录于此。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- v0.4.0：拆 Skill 模板（三层结构）+ Session State 持久化 + Skill 契约测试
- DECISIONS.md / TODO.md / STATUS.md 在 v0.3.1 补全（见 v0.3.1 变更）

## [0.4.0-dev]

最新开发分支。包含 v0.3.0 全部内容 + 知识归档 4 件套（CHANGELOG / DECISIONS / TODO / STATUS）。

## [0.3.1] - 2026-09-16

### 新增
- 知识归档 4 件套（让换电脑/换同事能完整接手）：
  - `CHANGELOG.md` — 完整变更日志（本文档）
  - `DECISIONS.md` — 关键决策 Why 归档
  - `TODO.md` — P0/P1/P2 backlog 详情
  - `STATUS.md` — 当前状态快照
- 8 步流水线修正：拆 design-brief-builder 和 design-maker 为两个独立步骤（之前 README 误合并）

## [0.3.0] - 2026-09-16

### 重构
- **README.md 30 秒扫视重写**（272 → 128 行，-53%）：数字卡片前置、8 步流水线图前置到第 19 行、对比表简化
- **AGENTS.md 按域拆分**（162 行 12 章节 → 7 个文件）：
  - `AGENTS.md`（29 行入口） / `IDENTITY.md`（17 行） / `WORKFLOW.md`（69 行） / `SKILLS.md`（56 行） / `SUBAGENTS.md`（16 行） / `STATE-ROUTING.md`（18 行） / `TESTING.md`（11 行）
  - 每个域文件底部 `<!-- owner: -->` 标注
  - 主 Agent 启动顺序：IDENTITY → WORKFLOW → SKILLS → SUBAGENTS → STATE-ROUTING → TESTING

## [0.2.2] - 2026-09-11

### 新增
- `examples/flashcards` Phase 4-5 前端学习模式 UI：
  - `useStudyStore`（Pinia store，14 个测试）
  - `StudyView.vue`（卡片 + 翻转 + 6 档评分按钮）
  - `tests/unit/StudyView.spec.ts`（5 个组件交互测试）
- 前端路由加 `/study`，App.vue 导航加"学习"链接

## [0.2.1] - 2026-09-11

### 新增
- `examples/flashcards` Phase 3 后端学习模式：
  - `app/services/spaced_repetition.py`：经典 SM-2 算法（Wozniak 1985）
  - `app/api/study.py`：3 个端点（queue / review / stats）
  - `tests/test_spaced_repetition.py`：12 条算法单元测试
  - `tests/test_study.py`：9 条 API 测试
- Card 模型扩展 5 个 SM-2 字段
- `app/main.py` lifespan 加 idempotent 增量 ALTER TABLE（dev 用）

## [0.2.0] - 2026-09-11

### 新增
- `examples/flashcards` Phase 1 骨架：
  - 后端 FastAPI + SQLAlchemy 2.0 + SQLite + Pydantic v2（13 文件）
  - 前端 Vue 3.5 + Element Plus 2.8 + Vite 5 + Pinia + Vue Router（15 文件）
  - 卡片 CRUD + 卡片管理 UI
  - 9 个 pytest 测试 + 5 个 Vitest 测试

## [0.1.2] - 2026-09-11

### 变更
- 主仓库迁移至 GitHub：https://github.com/along-ai-tech/idea-hammer
- Gitee 作为镜像仓库保留
- README 同步：git clone URL 指向 GitHub，新增 GitHub/Gitee 双 badge
- README 新增"快速预览"段：8 步流水线 ASCII 图 + 目录树速览

## [0.1.1] - 2026-09-08

### 新增
- 项目骨架：AGENTS.md 主控 + 8 个 skill 模块（product-spec-builder、design-brief-builder、design-maker、dev-planner、dev-builder、bug-fixer、code-review、release-builder）
- 方法论：SDD（Spec 驱动开发）作为核心，文档为单一真相源
- 设计桥接：Design-Brief 与设计稿在 Spec 与 Plan 之间做翻译
- 质量闭环：TDD（RED-GREEN-REFACTOR）作为强制度假纪律
- 审查闭环：code-reviewer 两阶段审查（功能完整性 + 质量/TDD 合规）
- 进化机制：EVOLUTION 信号队列 + 规则沉淀
- Hook 门禁：5 类事件驱动确定性检查（UserPromptSubmit / SessionStart / PreToolUse / PostToolUse / Stop）
- LICENSE：MIT
- README：中文项目门面

### 变更
- 命名 IdeaHammer + 方法论风格（直白、反模糊、不奉承）

## [0.1.0] - 2026-09-08

### 新增
- 初始版本（未发布）
