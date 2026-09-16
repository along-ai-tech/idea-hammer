# Evolution 三层捕获

> 把 evolution 从两层（显式 + 主动扫）升级为三层（显式 / 隐式 / 效果）。让规则改动可量化。

## 三层定义

### Layer 1: 显式（Explicit）

**触发**：用户主动表达不满/纠正

**捕获方式**：
- `detect-feedback-signal` hook（关键词匹配）
- 主 Agent 识别后补记

**信号类型**：`correction`

**示例**：
```json
{
  "id": "...",
  "type": "correction",
  "layer": "explicit",
  "prompt": "这个不对，应该用 Redisson",
  "created_at": "2026-09-16T..."
}
```

### Layer 2: 隐式（Implicit）

**触发**：系统发现反复出现的失败模式（无需用户主动报告）

**捕获方式**：
- evolution-runner 主动扫 git 历史找反复出现的修复模式（已有）
- **新增** code-reviewer Stage 2 报出同类缺陷 N 次 → 自动入队
- **新增** 契约测试反复发现反模式（同类失败）→ 自动入队

**信号类型**：`bug_pattern` / `review_finding`

**示例**：
```json
{
  "id": "...",
  "type": "review_finding",
  "layer": "implicit",
  "pattern": {
    "occurrences": 5,
    "files": ["src/order/OrderService.java", "src/order/PaymentService.java"],
    "first_seen": "2026-09-01T...",
    "last_seen": "2026-09-15T..."
  },
  "context": "5 处自造连接池，应该用 HikariCP"
}
```

### Layer 3: 效果（Effect）

**触发**：proposal 落地后跑效果指标验证

**捕获方式**：
- 主 Agent 接受 proposal 后 → 跑契约测试 + example 测试
- 跑 lint / format 检查
- 记录 improvement_pct

**信号类型**：`effect_metric`

**示例**：
```json
{
  "id": "...",
  "type": "effect_metric",
  "layer": "effect",
  "metric": {
    "name": "契约测试通过率",
    "value_before": 0.95,
    "value_after": 1.0,
    "improvement_pct": 5.26
  }
}
```

## 工具

`scripts/evolution_stats.py` 跟踪效果指标：

```bash
# 初始化
python3 scripts/evolution_stats.py init

# 记录 proposal 接受
python3 scripts/evolution_stats.py add-acceptance \
  --proposal_id D-NNN --accepted true

# 记录信号层计数
python3 scripts/evolution_stats.py add-signal --layer explicit

# 记录影响指标
python3 scripts/evolution_stats.py add-impact \
  --metric_name "契约测试通过率" --before 0.95 --after 1.00

# 显示统计
python3 scripts/evolution_stats.py show
```

## 三层协调流程

```
[1] 用户反馈 / Agent 识别（显式层）
    ↓
[2] 主 Agent 接受 proposal → 改文档
    ↓
[3] 跑契约测试 / example 测试
    ↓
[4] 记录效果指标（effect 层）→ 写入 .codex/evolution/effect-stats.json
    ↓
[5] 反向影响后续 proposal：接受率 < 50% 的 proposal 类型建议降低优先级
```

## 与现有机制的关系

- 兼容：保留 detect-feedback-signal hook + signals.jsonl 格式
- 扩展：signals.jsonl 每行加 `layer` 字段（默认 `explicit`）
- 新增：.codex/evolution/effect-stats.json 跟踪效果

## 验收

- [x] schemas/evolution-signal.schema.json — 信号三层 schema
- [x] schemas/effect-stats.schema.json — 效果统计 schema
- [x] scripts/evolution_stats.py — 效果统计工具
- [x] docs/evolution-3-layer.md — 三层捕获文档
- [x] evolution-engine SKILL.md（更新消化流程）

## 为什么需要三层

当前 evolution 只看用户主动反馈（explicit）+ git 历史（半隐式）。缺：
- **隐式层**：code-reviewer 反复发现同类问题 → 应该让 framework 主动识别
- **效果层**：proposal 落地后没人验证 → 净规则量可能越积越多却没改善

三层让 evolution 从"被动的反馈机"升级为"主动的规则优化闭环"。
