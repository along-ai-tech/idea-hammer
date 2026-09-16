# simplification/ — 代码简洁之道

> 把"代码简洁"从口号变成 10 条具体纪律 + AI 写代码特有的反模式清单。

## 为什么独立成主题

dev-builder/principles/code-style.md 有零散的"代码精简"规则，但缺：
- 具体可量化的阈值（文件长度 / 函数长度 / 圈复杂度）
- 反模式清单（命名 / 抽象 / 注释 / dead code）
- 自动化校验（check_simplicity.py）
- AI 写代码特有的反模式
- 跨语言的简明指南

本主题把这些补齐 —— **10 条原则**，每条都是工程共识 + AI 经常翻车点。

## 10 条原则

| # | 原则 | 关键约束 |
|---|---|---|
| 1 | [单一职责](./single-responsibility.md) | 函数 / 文件 / 模块各做一件事 |
| 2 | [YAGNI](./yagni.md) | 不为假想的未来写代码 |
| 3 | [抽象时机](./abstraction-timing.md) | Rule of Three：第 3 次重复才抽象 |
| 4 | [文件 / 函数 / 圈复杂度阈值](./file-and-function-size.md) | 文件 ≤ 300 / 函数 ≤ 50 / 圈复杂度 ≤ 10 |
| 5 | [命名即文档](./naming-is-documentation.md) | 好命名 = 无需注释 |
| 6 | [默认不写注释](./no-comments-by-default.md) | 注释解释 why 不解释 what |
| 7 | [删 dead code](./dead-code-deletion.md) | 注释掉的代码 = 负债 |
| 8 | **[依赖最小化](./dependency-minimalism.md)** ⭐ | 每个 dep 是债务，优先 stdlib + 现有生态 |
| 9 | **[副作用隔离](./pure-functions.md)** ⭐ | 纯函数优先，副作用集中到边界 |
| 10 | **[幂等性](./idempotency.md)** ⭐ | 脚本 / hook 反复执行结果相同 |

⭐ = 针对 AI 写代码特有补充（依赖最小化 / 副作用隔离 / 幂等性）

## AI 写代码特有的反模式

> AI 倾向"看起来专业"但实际是过度设计。以下是必须避免的：

| 反模式 | 为什么是反模式 |
|---|---|
| 装包解决 5 行问题 | 依赖膨胀、lockfile 复杂、安全面大 |
| 第一个用例就写抽象 | 抽象时机未到（Rule of Three） |
| 长函数（> 50 行）含 print + db + 计算 | 难测、难维护、副作用未隔离 |
| 装饰器套装饰器（@lru_cache + @timer + @auth + @log） | 调试噩梦 |
| 注释解释 what（"计算总价"）而非 why | 命名即文档 |
| "TODO: 后面会处理" | YAGNI 失守；要么现在做要么删 |
| 大量 # comment-out 代码 | dead code，git history 有 |
| 装饰性单元测试（assert x == mock_value） | mirror assertion，不测真实行为 |
| Pattern 套娃（Factory + Strategy + Builder + Singleton） | "看起来专业"陷阱 |
| 生成大量动态代码（exec / eval / 元类） | 可读性归零 |

## 自动化校验

`scripts/check_simplicity.py`（待实现）检查：
- 文件 ≤ 300 行
- 函数 ≤ 50 行（启发式）
- 圈复杂度 ≤ 10
- dead code（注释掉的代码 / unused import）
- 命名质量（避免 a / tmp / foo）
- TODO / FIXME 残留
- 装饰器套娃检测

## 与现有原则关系

| 现有 | 落地点 |
|---|---|
| dev-builder/principles/code-style.md | 引用本主题 10 条 |
| external-and-real.md 的"真实优先" | 部分整合到 yagni.md |
| scope-and-modification.md 的"修改纪律" | 文件 / 函数长度 |
| quality-and-security.md 的"代码质量" | 抽象 / 命名 / 死代码 |

## 接入点

- ✅ `dev-builder/principles/code-style.md` 引用本主题
- ✅ `code-review/principles/stage2-checklist.md` 加"代码简洁性"检查项
- ⏳ `scripts/check_simplicity.py`（待实现）
- ⏳ `tests/contract/test_simplification.py`（待实现）

## 源头 / 致敬

10 条原则来自工程共识，非单本书。综合源头：

- **单一职责** — Robert C. Martin《Clean Code》(2008) + SOLID
- **YAGNI** — Kent Beck《Extreme Programming Explained》(1999)
- **Rule of Three** — Martin Fowler《Refactoring》(1999)
- **文件 / 函数 / 圈复杂度阈值** — Robert C. Martin《Clean Code》
- **命名即文档** — Boswell & Foucher《The Art of Readable Code》(2011) 第 1 章
- **注释 why 不 what** — 同上 +《Clean Code》
- **删 dead code** — 通用工程实践（Python PEP 8 / Rust clippy / Go vet）
- **依赖最小化** — Sandi Metz 等"框架设计"共识
- **副作用隔离** — 函数式编程共识（HOF / 纯函数）
- **幂等性** — 分布式系统共识 + REST 规范
