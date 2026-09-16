# workflows/ — 执行流程

> 写"步骤怎么走"的流程。每文件一流程；阶段化、含完成标准。

## 命名规则

- 文件名用 kebab-case
- 命名格式：`workflow-<场景>.md`
- 例：`workflow-0-1.md`（首次创建）/ `workflow-iteration.md`（修改已有）/ `workflow-review.md`（审查流程）

## 文件结构

每流程一文件，包含：

```markdown
# 流程：<流程名>

> <流程做什么、产生什么产出物、用户怎么触发>

## 阶段 1：<阶段名>

**目标**：<一句话目标>
**动作**：<具体动作清单>
**完成**：<可验证的完成标志>

## 阶段 2：<阶段名>
...

## 失败处理

<失败时的回退 / 重试策略>

## 完成标志

<整个流程结束的判定标准>
```

## 与 SKILL.md 的关系

- SKILL.md 的 [使用方式] 段引用具体 workflow 文件
- SKILL.md 不展开流程细节，只说"何时走哪条"
- 修改流程时只改 workflow 文件，SKILL.md 不动

## 校验

`check_skill_structure.sh` 不强制本目录存在；
仅当存在时校验 `*.md` 是合法 markdown（文件可读）。
