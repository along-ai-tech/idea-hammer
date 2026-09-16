# principles/ — 第一性原则

> 写"为什么这样做"的规则。每文件一原则；可被多个 skill 引用。

## 命名规则

- 文件名用 kebab-case
- 命名格式：`<价值取向>-principle.md` 或 `<领域>-rule.md`
- 例：`tdd-discipline.md`、`scope-discipline.md`、`reuse-first.md`

## 文件结构

每原则一文件，至少包含：

```markdown
# 原则：<原则名>

> 一两句话陈述原则本身。

## 为什么

<背景、为何重要、违反的代价>

## 怎么做

<具体执行规则（编号或要点）>

## 反模式

<常见错误做法 + 为什么错>
```

## 复用 vs 新建

- 跨 skill 引用的原则：放这里，被引用 skill 在 SKILL.md 的 [引用] 段列出
- 只本 skill 用的原则：也放这里；不必为了"复用"而过度拆分
- 真正高度复用（≥ 3 skill）：考虑抽到独立 `_shared/principles/`

## 校验

`check_skill_structure.sh` 默认不强制本目录存在；
`--strict` 模式要求存在且有内容。
