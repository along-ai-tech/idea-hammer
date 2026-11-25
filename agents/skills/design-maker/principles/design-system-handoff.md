---
name: design-system-handoff
description: 设计系统与交付纪律：Design Token、组件系统（按钮/状态徽标/输入/表格）、交付物清单（Tokens/组件清单/交互说明/页面状态/资产清单/响应式）、Design-to-Code 流程与视觉验收四类。
---

# 原则：设计系统、交付与验收

> 只给截图不算交付。下游要能用它写代码、能验收，才算设计完成。

## 一、Design System

### 1. Design Token

至少覆盖：`color.*`（背景 / 表面 / 主色 / 危险 / 文本 / 边框）、`space.*`、`radius.*`、`shadow.*`、`font.*`、`motion.*`。

- Token 是跨页面统一的变量，不是"少写 CSS"的缩写
- 命名按语义（`color.danger`），不按外观（`red`）
- 交付时给变量表 + 可直接落地的前端映射（CSS Variables / Element Plus 变量覆盖 / Tailwind theme）

### 2. Component System

组件清单至少覆盖：Button、Status Badge、Input、Table、Feedback（Toast / Dialog / Empty）。

| 组件 | 最小变体 | 最小状态 |
|---|---|---|
| Button | 主 / 次 / 危险 / 文字 | default / hover / active / focus / disabled / loading |
| Status Badge | 成功 / 警告 / 错误 / 中性 / 处理中 | 静态 + 文案规则 |
| Input | 单行 / 多行 / 带校验 | default / focus / filled / error / disabled / readonly |
| Table | 基础 / 可排序 / 可选择 / 空 | default / loading / empty / error / selected / 行禁用 |

每个组件必须写：点击反馈、键盘焦点、加载中是否禁止重复提交、禁用原因。

## 二、Design Handoff 交付物（七件）

1. 设计稿（页面 + 关键状态）
2. Design Tokens（变量表 + 前端映射）
3. Component Inventory（组件清单：变体 / 状态 / 使用页面）
4. Interaction Spec（每个操作的确认 / 处理中 / 成功 / 失败 / 超时 / 重试）
5. Page State（每页状态矩阵，见下）
6. Asset Manifest（图标 / 图片 / 字体：名称、尺寸、格式、来源、是否装饰性）
7. Responsive Rules（断点、栅格、折叠顺序、最小可操作尺寸）

缺任一项即视为交付不完整，dev-builder 可退回。

## 三、页面状态矩阵（最少 8 态）

正常 / Loading / Empty / Error / Disabled / Permission Denied / Submitting / Success。

| 状态 | 必答 |
|---|---|
| 正常 | 默认内容与主操作 |
| Loading | 骨架屏或加载指示，避免布局跳动 |
| Empty | 为什么空 + 下一步入口 |
| Error | 错误原因 + 重试 / 返回 |
| Disabled | 禁用原因 + 如何解除 |
| Permission Denied | 谁能做 + 申请 / 切换账号路径 |
| Submitting | 按钮 loading、防重复提交、可取消（长任务） |
| Success | 成功反馈 + 数据刷新 + 下一步 |

## 四、Design-to-Code 流程

1. 读技术栈与既有设计系统（组件库版本、Token 来源）
2. 读 Design Brief 与设计稿（含状态与交互说明）
3. 识别可复用组件，先映射到既有组件，不新造
4. 明确数据结构与 API（字段 → 界面元素）
5. 先搭骨架（布局 + 路由 + 空壳组件）
6. 再实现组件与交互
7. 覆盖 Loading / Empty / Error / Success / Submitting
8. 启动验证（本地跑通）
9. 截图对比设计稿
10. 修复差异并复验

铁律：不得为还原单页破坏既有组件体系；确需新组件，先补进组件清单并说明复用范围。

## 五、视觉验收四类

| 类别 | 检查内容 | 不通过示例 |
|---|---|---|
| Visual QA | 布局、间距、字号、颜色、圆角、图标、对齐、状态样式 | 卡片间距 12/16 混用 |
| Interaction QA | 点击反馈、loading、防重复提交、确认与取消、错误恢复 | 提交中按钮仍可点 |
| Responsive QA | 断点布局、栅格折叠、表格横向滚动、触控尺寸 | 移动端表格溢出不可滚 |
| Accessibility QA | 键盘可达、焦点可见、label 关联、对比度、语义、替代文本 | 图标按钮无 aria-label |

验收结论写回交付报告，未通过项列明修复责任与复验结果。

## 六、企业级后台场景补强

面向"AI Tool 管理平台"这类后台，额外要求：

- 列表：筛选 / 排序 / 分页 / 批量操作 / 行状态（启用 / 禁用）
- 详情：结构化参数 Schema 的展示（字段名、类型、必填、默认值、枚举、嵌套），支持折叠与复制
- 关联管理：一个 Tool 授权给多个 Agent（多选 + 已授权列表 + 撤销确认）
- 指标：调用次数 / 成功率 / 耗时（数值 + 趋势 + 空/异常数据态）
- 危险操作：禁用 Tool 必须二次确认，说明影响范围（哪些 Agent 会失效）
