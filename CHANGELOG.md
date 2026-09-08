# 变更日志

本项目的所有重要变更记录于此。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- examples/flashcards：本地闪卡应用，技术栈 Python(FastAPI + SQLAlchemy + SQLite) + Vue3 + Element Plus，作为 IdeaHammer 端到端流水线的演示证据

## [0.1.1] - 2026-09-08

### 变更
- 开源仓库迁移至 Gitee：https://gitee.com/zhilong811/idea-hammer
- README 安装命令指向 Gitee 仓库地址
- v0.1.1 是首个对外发布版本

## [0.1.0] - 2026-09-08

### 新增
- 项目骨架：AGENTS.md 主控 + 8 个 skill 模块（product-spec-builder、design-brief-builder、design-maker、dev-planner、dev-builder、bug-fixer、code-review、release-builder）
- 方法论：SDD（Spec 驱动开发）作为核心，文档为单一真相源
- 设计桥接：Design-Brief 与设计稿在 Spec 与 Plan 之间做翻译
- 质量闭环：TDD（RED-GREEN-REFACTOR）作为强制度假纪律，内置于 dev-builder 与 bug-fixer
- 审查闭环：code-reviewer 两阶段审查（功能完整性 + 质量/TDD 合规）
- 进化机制：EVOLUTION 信号队列 + 规则沉淀
- Hook 门禁：UserPromptSubmit / SessionStart / PreToolUse / PostToolUse / Stop 五类事件驱动确定性检查
- LICENSE：MIT 协议
- README：中文项目门面

### 变更
- 品牌确立：所有用户面文档与人设移除旧品牌标签，保留方法论风格（直白、反模糊、不奉承）

### 已知限制
- example 项目（本地闪卡）尚未启动，仅作规划占位
- 文档校对中：英文版 README 待出
