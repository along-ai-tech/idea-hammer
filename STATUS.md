# 当前状态快照

> 让换电脑/换同事的同事**30 秒内知道现在到哪、卡在哪、接下来做什么**。

---

## 一句话状态

**v0.3.0 路线图 3/4 已完成**。AGENTS.md 拆分 + README 优化 + 8 步流水线修正已落地；剩**知识归档 4 件套**进行中。下一步开 P0-1（拆 Skill 模板）。

---

## 版本

| 项 | 值 |
|----|-----|
| 当前 commit | `43b4f39` |
| 已发布版本 | v0.3.0（README + AGENTS.md 拆分） |
| 进行中 | v0.3.1（知识归档 4 件套） |
| 下一步 | v0.4.0（P0 改进：拆 Skill / Session State / Skill 契约） |
| 最近一次 push | 2026-09-16（双 remote 一致） |

---

## 各 Phase 状态

| 阶段 | 状态 | 说明 |
|------|------|------|
| **v0.1 骨架** | ✅ 完成 | AGENTS.md + 8 skill + Hook + EVOLUTION + LICENSE |
| **v0.2 example 跑通** | ✅ 完成 | flashcards Phase 1-5，56 测试全绿 |
| **v0.3 框架升级** | 🚧 进行中 | README ✅ / AGENTS.md 拆分 ✅ / 知识归档（当前） |
| **v0.4 P0 改进** | ⏳ 计划 | 拆 Skill / Session State / Skill 契约 |
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

- **主仓库**：https://github.com/wuzhilong0811/idea-hammer
- **镜像**：https://gitee.com/zhilong811/idea-hammer
- **License**：MIT
- **作者署名**：wuzhilong

---

## 关键决策摘要（详见 DECISIONS.md）

| 编号 | 决策 | 日期 |
|------|------|------|
| D-001 | 品牌确立（见 DECISIONS.md D-001 详情） | 2026-09-08 |
| D-002 | 项目名 IdeaHammer | 2026-09-08 |
| D-003 | example 技术栈：Python + Vue3 + Element Plus | 2026-09-08 |
| D-004 | P0 改进优先级排序 | 2026-09-15 |
| D-005 | 8 步流水线 bug-fixer 算回路 | 2026-09-15 |
| D-006 | README 30 秒扫视重写 | 2026-09-16 |
| D-007 | AGENTS.md 按域拆分 | 2026-09-16 |

---

## 接下来做什么（按优先级）

### 本周内（v0.3.1 收尾）

- [x] 4 份归档（CHANGELOG / DECISIONS / TODO / STATUS）✅ 当前
- [ ] commit + push 双 remote
- [ ] 验证新人按本文件 + README + AGENTS.md 能否完整接手

### 下周起（v0.4.0 开 P0-1）

1. **TODO-003 拆 Skill 模板**（2-3 周）
   - 先做 `_template/` + `check_skill_structure.sh` 脚手架
   - 再用 dev-builder 做样板
   - 最后推广其余 7 个

2. **TODO-004 Session State 持久化**（2 周，可与 TODO-003 并行）

3. **TODO-005 Skill 契约测试**（2-3 周，依赖 TODO-003）

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
