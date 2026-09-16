# 原则：代码规范与精简

> 单文件不超过 300 行，TypeScript strict，三行直白代码好过一个过度抽象。

## 文件与命名

- 单文件不超过 300 行，超了按职责拆分
- TypeScript strict，不用 any，用 unknown + 类型守卫
- 命名：组件 PascalCase，函数变量 camelCase，文件 kebab-case，常量 UPPER_SNAKE_CASE
- 每个文件单一职责，副作用隔离到 hooks 或 API 层

## 风格

- 跟随已有代码库的风格，不强推个人偏好，不做无关重构
- YAGNI：不为假想的未来需求写代码
- 代码精简：三行直白代码好过一个过度抽象

## 喂模型不截断

- 喂给模型/Agent 的工具结果与给人看的 UI 摘要是两份产物
- UI 可截断省略，喂模型的绝不能截断
- 处理长文档/长输入时保证数据全量进模型，扛不住就改精简格式（如逐条压成单行）而不是砍条数

## 详细约束见 simplification/ 主题（10 条原则）

代码规范与精简的具体规则、阈值、反模式、AI 特有反模式详见：

[`_engineering-constraints/simplification/`](../../_engineering-constraints/simplification/)

包含：
- single-responsibility / yagni / abstraction-timing / file-and-function-size
- naming-is-documentation / no-comments-by-default / dead-code-deletion
- **dependency-minimalism / pure-functions / idempotency**（AI 写代码特有补充）

自动化校验：`scripts/check_simplicity.py`
