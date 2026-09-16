---
name: bug-fixer
description: 当用户说'这个功能坏了'、'报错了'、'不正常'，或报告 bug、编译错误、运行时异常时使用。通过系统性调试定位根因并修复。
---

# bug-fixer

[任务]
    系统性定位 bug 根因并修复。一次只改一个，每次改前评估影响，修后回归验证。

[调用上下文]
    用户直接报 bug → 修完建议 /code-review 验证。
    code-review Stage 2 报出缺陷或安全问题 → 主 Agent 传入失败项，修完重派 code-review 从 Stage 1 起。

[依赖检测]
    必需：项目代码、bug 描述。
    可选增强：Product-Spec.md、DEV-PLAN.md、设计工具 MCP、Playwright、git。

[使用方式]
    读 principles/ 必读 → 按 workflows/debug.md 走四阶段（根因调查 → 复现测试 → 假设验证 → 实施修复）→ contracts/output.schema.json 校验。

[文件结构]
    bug-fixer/
    ├── SKILL.md             # 本文件（≤ 30 行）
    ├── principles/          # 调试纪律
    ├── workflows/           # 调试流程
    └── contracts/           # 输出 schema

[引用]
    原则：principles/debug-discipline.md
    流程：workflows/debug.md
    契约：contracts/output.schema.json
    系统化调试：参考 superpowers:systematic-debugging
