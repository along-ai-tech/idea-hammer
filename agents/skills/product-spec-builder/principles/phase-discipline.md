# 原则：Phase 划分 + 搜索增强双遍

> 0-1 模式先过地基才解锁细节。视觉方向（product-form）和 AI 能力都不是一次问出来的。

## Phase 划分

| Phase | 主题 | 对应原则 |
|---|---|---|
| Phase 0 | 商业可行性快筛（仅 0-1 模式） | business-context-check |
| Phase 0.5 | 产品类型判断（业务参照型 / 市场机会型，扫描路由开关） | competitive-scan |
| Phase 1 | 问题与人 | question-bank |
| Phase 1.5 | 竞品扫描（直接竞品 + 替代方案，权重看 0.5 类型） | competitive-scan |
| Phase 1.6 | 行业借鉴（相邻品类/跨界优秀做法，权重看 0.5 类型） | competitive-scan |
| Phase 2 | Job 与成功 | question-bank |
| Phase 3 | 范围与非目标 | question-bank |
| Phase 3.5 | pre-mortem 反向思考 | question-bank |
| Phase 4 | 旅程与功能 | question-bank |
| Phase 5 | AI 能力 | question-bank + ai-capability-awareness |
| Phase 6 | UI 与状态 | question-bank |
| Phase 7 | 验收与边界 | question-bank |
| 收尾 | 多视角自检（CEO/Eng/QA） | ceo-lens + eng-lens + qa-lens |

**关键**：
- Phase 0 / 0.5 / 1 / 3 是地基
- **不过地基不解锁后面**
- Phase 0 跳过条件：迭代模式（已存在 Spec 的功能调整）
- Phase 0.5 跳过条件：迭代模式
- 收尾多视角自检跳过条件：迭代模式

**搜索增强双遍与竞品/借鉴扫描的关系**：
- 第一遍（提问前搜种子）→ 落地为 Phase 0 + Phase 0.5 类型判断 + Phase 1.5 竞品扫描 + Phase 1.6 行业借鉴四段结构化产出物
- 第二遍（聊完再搜可行性）→ 仍由主 Agent 在 Spec 收尾前跑

**Phase 0.5 产品类型路由作用**：
- 业务参照型（公司既有业务方向 / 行业有成熟方案 / 用户主动"参考 XX"）→ 1.6 弱化、1.7 强化为价值核心
- 市场机会型（默认）→ 1.6 严格必填、1.7 选填顶级品类
- Phase 1.5 / 1.6 顶部必须先读 0.5 类型再决定填充深度

## 搜索增强双遍

### 第一遍：提问前搜种子

- 0-1 进场先按 0.5 类型分支搜：
        - 业务参照型：搜主关键词 + "best practices" / "行业标准" / 同行案例 / 跨界关键词 → 行业借鉴素材为主
        - 市场机会型：搜主关键词 + "alternatives to X" / "X vs Y" / 行业报告 → 竞品扫描素材为主
- "市面已有十个你凭什么活"要先搜出那十个，质问才有据
- "这块谁做得好可以拿"要先搜出相邻品类的成熟做法，避免重新发明轮子
- 用户中途报竞品也立刻搜其做法，追问"它的 X 你要不要、差异在哪"

### 第二遍：聊完根据对话再搜

- 访谈收尾、生成 Spec 前
- 按已聊出的核心功能、AI 能力、技术方向再搜一遍当前最佳方案和可行性
- 让写进 Spec 的技术选型和 AI 能力是当前的、有针对性的，不是泛泛的

### 用外部库、API、框架、AI 模型前

- 搜确认当前版本和可行性
- 不凭过期记忆
