# coding-style/ — 语言特定编码规范

> 主原则之外，按语言引用的具体规范。AI 生成代码必须遵循。

## 强制引用

dev-builder 在生成代码前必须读对应语言规范。Code-review Stage 2 必须对照检查。

| 语言/框架 | 规范 |
|---|---|
| Java | [java-alibaba.md](./java-alibaba.md) — 阿里 Java 手册关键条款 |
| Python | [python-pep8.md](./python-pep8.md) — PEP8 + 项目补充 |
| TypeScript / JavaScript | [typescript-airbnb.md](./typescript-airbnb.md) — Airbnb + Google TypeStyle |
| Go | [go-effective.md](./go-effective.md) — Effective Go + Go Code Review Comments |
| Rust | [rust-api-guidelines.md](./rust-api-guidelines.md) — Rust API Guidelines |
| SQL | [sql-conventions.md](./sql-conventions.md) — 跨方言 SQL 规范 |

## 选择规则

1. 先确认项目语言 + 框架（DEV-PLAN.md 技术栈表）
2. 读对应规范文档
3. 项目已有 README/CONTRIBUTING.md 写明规范 → 以项目为准，覆盖通用规范
4. 通用规范是底线，项目规范可加严但不能放松

## 与主原则关系

- 主原则：复用优先 / SDK-First / 真实优先 → **做什么**
- 语言规范：具体怎么写 → **怎么做**
- 两者不冲突：主原则说"用现成库"，语言规范说"用现成库时怎么命名、怎么 import、怎么排版"
