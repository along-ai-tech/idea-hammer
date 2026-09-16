# 前端生态矩阵

> React / Vue / 通用前端库选择。

## 框架

| 场景 | 首选 | 次选 |
|---|---|---|
| React 全栈 | **Next.js** | Remix |
| Vue 全栈 | **Nuxt 3** | - |
| React SPA | **Vite + React** | Create React App（已停更） |
| Vue SPA | **Vite + Vue** | Vue CLI（已停更） |
| 桌面（Web 技术栈） | **Electron + Vite** | Tauri（更小） |
| 移动端 | **React Native** / **Expo** | Flutter |

## 组件库

| 场景 | 首选 | 次选 |
|---|---|---|
| React + TypeScript | **shadcn/ui**（Radix + Tailwind） | Ant Design / MUI |
| React 企业后台 | **Ant Design** | Element Plus React（不存在） |
| Vue + TypeScript | **Element Plus** | Naive UI / Vuetify |
| 设计系统 | **Tailwind CSS + Headless UI** | styled-components |

## 状态管理

| 场景 | 首选 | 次选 |
|---|---|---|
| React | **Zustand** | Jotai / Redux Toolkit |
| Vue | **Pinia** | Vuex（已弃用） |
| 服务端状态 | **TanStack Query** | SWR / Apollo |
| 表单 | **React Hook Form + Zod** | Formik |
| 路由 | **TanStack Router** / React Router v6 | - |

## 工具库

| 场景 | 首选 | 次选 | 禁止 |
|---|---|---|---|
| 类型 | **TypeScript strict** | - | ❌ any / Flow |
| 样式 | **Tailwind CSS** | CSS Modules | ❌ 内联 style / styled-components 重度 |
| 动画 | **Framer Motion** | - | ❌ jQuery |
| HTTP | **fetch**（原生） / **TanStack Query** | axios（已被 fetch + AbortController 替代） | ❌ XHR |
| 时间 | **date-fns** | dayjs | ❌ moment（已停更） |
| 测试 | **Vitest** + **Playwright** | Jest | ❌ Karma / Mocha |
| 表单 | **React Hook Form + Zod** | Formik | ❌ 手写表单状态 |
| 国际化 | **i18next** | react-intl | ❌ 自造 i18n |
| 工具库 | **es-toolkit**（替代 lodash） | lodash | ❌ 自造 deep clone |
| Linter | **ESLint + Prettier** | - | ❌ TSLint（已弃用） |
| 图表 | **Recharts** / **echarts** | Chart.js | ❌ D3 for simple chart |
| 富文本 | **TipTap** / Lexical | Slate | ❌ 自造 |
| 拖拽 | **dnd-kit** | react-beautiful-dnd（已停更） | ❌ 自造拖拽 |
| 模态 | **Headless UI** / Radix | - | ❌ 自造 modal + focus trap |

## 反模式

- ❌ 用 jQuery（现代浏览器原生 API 已够）
- ❌ 用 moment（已停更，体积大）
- ❌ 用 lodash 全量（按需引入 es-toolkit）
- ❌ 用 Redux 经典版（用 Redux Toolkit）
- ❌ 用 Vuex（用 Pinia）
- ❌ 内联复杂样式（用 Tailwind / CSS Modules）
- ❌ 自造 modal / dropdown（无障碍难做）
- ❌ `dangerouslySetInnerHTML` 不脱敏
- ❌ `console.log` 留生产代码
