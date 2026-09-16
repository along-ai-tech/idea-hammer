# 当前状态快照

> 让换电脑/换同事的同事**30 秒内知道现在到哪、卡在哪、接下来做什么**。

---

## 一句话状态

**v0.3.1 已发布**。知识归档 4 件套 + hook 路径 bug 修复全部完成。下一步进 v0.4.0 P0-1（拆 Skill 模板）。

---

## 版本

| 项 | 值 |
|----|-----|
| 当前 tag | **v0.3.1**（fix `8687f1c` + docs `711a053`） |
| 已发布版本 | v0.3.0（README + AGENTS.md 拆分）/ **v0.3.1（知识归档 + hook 路径修复）** |
| 进行中 | v0.4.0 P0-1（拆 Skill 模板，阶段 1） |
| 下一步 | 阶段 2：dev-builder 样板重构 |
| 最近一次 push | 2026-09-16（双 remote 一致） |

---

## 各 Phase 状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| **v0.1 骨架** | ✅ 完成 | AGENTS.md + 8 skill + Hook + EVOLUTION + LICENSE |
| **v0.2 example 跑通** | ✅ 完成 | flashcards Phase 1-5，56 测试全绿 |
| **v0.3 框架升级** | ✅ 完成 | README 30 秒扫视 + AGENTS.md 拆分 + 知识归档 4 件套 + hook 路径修复 |
| **v0.4 P0 改进** | 🚧 进行中 | TODO-003 拆 Skill 模板（阶段 1 即将开始） |
| **v0.5 CI + 英文** | ⏳ 远期 | CI 自动化 + 英文 README |
| **v1.0 稳定 API** | ⏳ 远期 | 锁定 skill API，向后兼容 |

---

## 测试统计

| 端 | 测试数 | 文件 |
|----|--------|------|
| 后端 pytest | 31 | `backend/tests/` |
| 前端 Vitest | 25 | `frontend/tests/unit/` |
| **合计** | **56** | |

最近一次跑测：commit `a51e3af` 之后，**全部通过**。

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

---

## 接下来做什么（按优先级）

### ✅ v0.3.1 已完成（tag v0.3.1 待打）

- [x] 4 份归档（CHANGELOG / DECISIONS / TODO / STATUS）✅
- [x] 修复 hook 路径 bug（D-008，commit `8687f1c`）
- [x] STATUS.md / DECISIONS.md / CHANGELOG.md 同步到 v0.3.1
- [x] tag v0.3.1 推送双 remote ✅

### 🚧 本周内（v0.4.0 P0-1 阶段 1）

1. **TODO-003 阶段 1**（1-2 天）：写 `agents/skills/_template/` 三层结构模板 + `scripts/check_skill_structure.sh`
2. 验证阶段 1 → 阶段 2 用 dev-builder 做样板（3-4 天）

### 📅 后续阶段

- **TODO-003 阶段 3**：平行重构其余 7 个 skill（10 天）
- **TODO-004**：Session State 持久化（2 周，可与 #3 并行）
- **TODO-005**：Skill 契约测试（2-3 周，依赖 #3 完成）

---

## 风险与阻塞

| 风险 | 状态 | 应对 |
|------|------|------|
| P0-1 拆 Skill 模板期间无自动化校验 | 中 | 阶段 1 必须先出 `check_skill_structure.sh` 才能进入阶段 2 |
| Session State 持久化可能改变主 Agent 行为 | 低 | 加 A/B 开关，默认关闭，先观察 |
| P0-4 契约测试需要先有 P0-1 结构 | 已识别 | 严格按依赖顺序，P0-1 完成后才开 P0-4 |

---

## 如何接手（新同事 / 换电脑）

按以下顺序读这 5 个文件，30 分钟内可完全理解项目当前状态：

1. **README.md**（30 秒扫视）—— 项目是什么、方法论、关键数字
2. **STATUS.md**（本文档，2 分钟）—— 当前到哪、接下来做什么
3. **DECISIONS.md**（10 分钟选读）—— 关键决策 Why，避免重蹈覆辙
4. **TODO.md**（5 分钟）—— Backlog 详情，知道接下来做什么
5. **CHANGELOG.md**（5 分钟）—— 演进历史，知道哪些是历史决策

然后：

- 跑 `pnpm install` + `cd examples/flashcards/backend && uv sync --extra dev`
- 跑测试：`cd backend && uv run pytest -v` + `cd frontend && ./node_modules/.bin/vitest run`
- 看 `AGENTS.md`（29 行入口）+ 6 个域文件，理解主控怎么工作
- 看 `agents/skills/*/SKILL.md` 8 个 skill，理解每个 skill 怎么用

---

## 联系方式

- 作者：wuzhilong
- 简历已包含本项目（IdeaHammer GitHub 仓库链接）
- 项目目的：展示 AI 编程标准化落地能力
