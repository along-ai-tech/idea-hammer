# assets/ — 静态资源（可选）

> 放图片、参考代码、prompt 模板等不被结构校验的资产。

## 放什么

- 设计参考图（PNG / JPG / SVG）
- 代码片段（不是 skill 本身要执行的）
- prompt 模板（供 skill 调用 AI 时用的字符串）
- 第三方工具的样例输出

## 不放什么

- skill 的执行脚本（那应该被 hooks / scripts/ 管理）
- 测试代码（TODO-005 契约测试会单独建 tests/ 目录）
- 临时调试输出

## 命名

- 图：`diagram-<name>.svg` / `mockup-<screen>.png`
- 代码：`snippet-<purpose>.<ext>`
- 模板：`prompt-<role>.md`

## 校验

本目录不参与 `check_skill_structure.sh` 校验。
