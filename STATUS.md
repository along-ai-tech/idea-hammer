# 当前状态快照

> 让换电脑/换同事的同事**30 秒内知道现在到哪、卡在哪、接下来做什么**。

---

## 一句话状态

**v0.12.0-dev**。上下文工程域与跨 Session 恢复已补齐（Day9 AI Coding 工程化缺口）；全局安装已打通——装一次，**所有 Codex 项目**自动生效，并由 CI 冒烟守住。

---

## 版本

| 项 | 值 |
|----|-----|
| 当前 tag | **v0.12.0-dev**（全局安装固化：路径锚点 + 契约测试 + CI 冒烟） |
| 已发布版本 | v0.3.0 / v0.3.1 / v0.4.0 / v0.5.0 / v0.6.0-dev（TODO-401）/ v0.7.0-dev（P1 业务纪律）/ v0.8.0-dev（spec 纪律）/ v0.9.0-dev（SDD）/ v0.10.0-dev（需求追踪） |
| 已完成 | v0.4.0 P0 + v0.5.0 P1 + TODO-401 simplification + P1 业务纪律 + **v0.9.0 SDD 任务循环 + v0.10.0 需求追踪体系 + v0.11.0 上下文工程域 + v0.12.0 全局安装** |
| 下一步 | 提交 v0.12.0（全局安装固化 + 文档校正）；再进 v1.0 规划（TODO-301 API 稳定化 + TODO-201 英文 README） |
| 最近一次 push | 双 remote 一致（origin / github 均在 `5e3a2c4`）；v0.12.0 待 push |

---

## 各 Phase 状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| **v0.1 骨架** | ✅ 完成 | AGENTS.md + 8 skill + Hook + EVOLUTION + LICENSE |
| **v0.2 example 跑通** | ✅ 完成 | flashcards Phase 1-5，56 测试全绿 |
| **v0.3 框架升级** | ✅ 完成 | README 30 秒扫视 + AGENTS.md 拆分 + 知识归档 4 件套 + hook 路径修复 |
| **v0.4 P0 改进** | ✅ 完成 | 拆 Skill 模板（三层）+ Session State + 契约测试 |
| **v0.5 P1 业务改进** | ✅ 完成 | 路由图 + 意图分类 + Hook v2 + Evolution 三层 |
| **v0.6 simplification** | ✅ 完成 | 代码简洁之道 10 条 + check_simplicity |
| **v0.7 P1 业务纪律** | ✅ 完成 | 5 问快筛 + 竞品 + 多视角 + pre-mortem + 版本化（2026-09-24） |
| **v0.8 spec 纪律** | ✅ 完成 | 需求工程重构为五层 + 两轮 Phase 0 + 4 个原则文件 |
| **v0.9 SDD 任务循环** | ✅ 完成 | subagent-driven-development skill + judgment ledger + breaker |
| **v0.10 需求追踪** | ✅ 完成 | REQ/AC/DT/TEST 稳定 ID + @trace 注解 + check_traceability.py + CI |
| **v0.11 上下文工程** | ✅ 完成 | CONTEXT.md 域 + context-engineering / test-pyramid 原则 + session checkpoint 工具 |
| **v0.12 全局安装** | ✅ 完成 | install_global.py + global_install/ 包 + Codex 真实 hook 协议 + 信任登记 + 22 项契约测试 + CI 冒烟 |
| **v1.0 CI + 英文** | ⏳ 远期 | API 稳定化 + 英文 README |

---

## 测试统计

| 端 | 测试数 | 文件 |
|----|--------|------|
| 框架契约测试 pytest | 292 | `tests/contract/` |
| 示例后端 pytest | 29 | `examples/personal-blog/backend/tests/` |
| 示例前端 Vitest | 10 | `examples/personal-blog/frontend/src/**/*.test.js` |
| **示例合计** | **39** | |

最近一次跑测：框架契约测试 **292 passed**（`python3 -m pytest tests/contract/ -q`），全绿。其中 22 项是全局安装器契约测试（装齐 / 不越界 / 可重复 / 可卸载），CI 里另有一条隔离安装冒烟。

---

## 仓库

- **主仓库**：https://github.com/along-ai-tech/idea-hammer
- **镜像**：https://gitee.com/zhilong811/idea-hammer
- **License**：MIT
- **作者署名**：wuzhilong

---

## 关键决策摘要（详见 DECISIONS.md）

| 编号 | 决策 | 日期 |
|------|------|------|
| D-001 | 命名采用 IdeaHammer（见 DECISIONS.md） | 2026-09-08 |
| D-002 | 项目名 IdeaHammer | 2026-09-08 |
| D-003 | example 技术栈：Python + Vue3 + Element Plus | 2026-09-08 |
| D-004 | P0 改进优先级排序 | 2026-09-15 |
| D-005 | 8 步流水线 bug-fixer 算回路 | 2026-09-15 |
| D-006 | README 30 秒扫视重写 | 2026-09-16 |
| D-007 | AGENTS.md 按域拆分 | 2026-09-16 |
| D-008 | hook 路径修复（codex/ → .codex/） | 2026-09-16 |
| **D-009** | **P1 业务纪律体系（5 问快筛+竞品+多视角+pre-mortem+版本化）** | **2026-09-24** |
| **D-013** | v0.9.0 subagent 任务循环（SDD）+ 代码纪律补强 | 2026-10-02 |
| **D-014** | v0.10.0 需求追踪体系（REQ/AC/DT/TEST + check_traceability.py） | 2026-11-25 |
| **D-015** | examples/personal-blog 补齐前端与 10 个 Vitest 测试 | 2026-11-25 |
| **D-016** | v0.11.0 上下文工程域 + 跨 Session 恢复（补 Day9 缺口） | 2026-11-26 |
| **D-017** | **v0.12.0 全局安装：Codex 真实 hook 协议 + 信任登记 + 路径锚点** | **2026-11-27** |

---

## 接下来做什么（按优先级）

### 🔴 P0：v0.12.0 收口

- [x] 全局安装器路径锚点：`--codex-home` 带动框架副本与技能目录，隔离安装不碰真实 `~/.codex`
- [x] 15 项安装器契约测试（装齐 / 不越界 / 可重复）+ CI 隔离安装冒烟
- [x] README / STATUS 数字校正（292 契约测试 / 12 skill / 15 主题 88 文件）
- [ ] commit + push 双 remote + 打 tag `v0.12.0`

### 🟡 P1：进 v1.0 规划

| 项 | 目标 | 工时 |
|---|---|---|
| TODO-301 | 12 个 skill 的 description + contracts 锁定为 v1.0 API，连同 `schemas/session.schema.json` 的 `checkpoints` 字段纳入向后兼容承诺 | 4 周 |
| TODO-201 | 英文版 README，海外传播的前置条件 | 1 周 |
| TODO-202 | PR 检查 + 自动 release workflow（当前 CI 只跑测试与校验） | 1 周 |
| TODO-203 | Sub-Agent 从手动 spawn 升级为 dag 编排 | 3-4 周 |

### 🟢 P2：降低首次安装摩擦

当前"全局可用"仍需手动 clone + 跑一次 `install_global.py`。可以做成 `codex plugin`
或一键 bootstrap——但要先确认 Codex 是否提供 plugin 机制，否则不值得投入。

---

## 风险与阻塞

| 风险 | 状态 | 应对 |
|------|------|------|
| Codex 升级可能改 hook 协议或信任机制 | 中 | 协议以 `openai/codex` 源码为准，schema 收紧到"未知字段即报错"；升级后先跑 `tests/contract/test_global_install.py` |
| 全局副本与源码仓库漂移 | 低 | `install_global.py sync` 是镜像语义（源码删了副本也删）；CI 每次跑隔离安装冒烟 |
| 首次安装仍需手动 clone + 一条命令 | 低 | 确认 Codex 是否有 plugin 机制再决定是否做一键 bootstrap |

---

## 如何接手（新同事 / 换电脑）

按以下顺序读这 5 个文件，30 分钟内可完全理解项目当前状态：

1. **README.md**（30 秒扫视）—— 项目是什么、方法论、关键数字
2. **STATUS.md**（本文档，2 分钟）—— 当前到哪、接下来做什么
3. **DECISIONS.md**（10 分钟选读）—— 关键决策 Why，避免重蹈覆辙
4. **TODO.md**（5 分钟）—— Backlog 详情，知道接下来做什么
5. **CHANGELOG.md**（5 分钟）—— 演进历史，知道哪些是历史决策

然后：

- 跑框架测试：`python3 -m pytest tests/contract/ -q`（285 项）
- 跑示例测试：`cd examples/personal-blog/backend && uv run pytest -v` + `cd ../frontend && npx vitest run`
- 装到本机：`python3 scripts/install_global.py install`，之后任意目录开 Codex 会话即可生效
- 看 `AGENTS.md`（入口）+ 7 个域文件，理解主控怎么工作
- 看 `agents/skills/*/SKILL.md` 12 个 skill，理解每个 skill 怎么用

---

## 联系方式

- 维护者：wuzhilong
- 项目定位：面向 AI-native coding 的开源工程框架
