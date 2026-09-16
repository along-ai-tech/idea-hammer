# TypeScript / JavaScript 编码规范 — Airbnb + Google TypeStyle

> 引用 [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) + [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)。

## 强制条款

### 命名

- 变量、函数：`camelCase`
- 类、类型、接口、枚举：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`
- 文件：`kebab-case.ts`（除 React 组件 `PascalCase.tsx`）
- 不要用 `I` 前缀（`IUser` → `User`）
- 不要用下划线前缀（除私有字段约定）

### TypeScript

- **强制 `strict: true`**：tsconfig 必开
- 不用 `any`，用 `unknown` + 类型守卫
- 函数返回类型必标（公开 API）
- 避免 `Function` / `Object` / `{}`（用具体类型）
- `interface` 用于对象形状，`type` 用于联合/工具
- `readonly` 标记不可变字段
- `enum` 慎用（const enum 或 union type）

```typescript
type Status = 'pending' | 'success' | 'error';  // 优于 enum
```

### 函数

- 纯函数优先（无副作用）
- 短函数（< 30 行）；超了拆
- 默认参数：`function foo(x = 1)` 而不是 `x = x || 1`（0 是合法值）
- Rest 参数：`function foo(...args: unknown[])`
- 箭头函数：表达式简短的；长逻辑用 `function`

### 异步

- 必用 `async/await`，不用 raw promise chain
- 错误必 catch：`await foo().catch(err => logger.error(err))`
- 并行：`Promise.all([a(), b()])` 而不是 `await a(); await b();`（除非有依赖）
- 超时：所有网络调用配 AbortController
- 不在循环里 `await`（批量用 `Promise.all`）

### React（前端）

- 函数组件 + Hooks
- Props interface：`interface ButtonProps { ... }`
- 不用 class 组件（新代码）
- 不用 `dangerouslySetInnerHTML`（除非 XSS 已审计）
- key 用稳定 ID，不用 index
- 副作用用 `useEffect`，不要在 render 里改 state
- 自定义 hook `use*` 前缀

### 模块

- ES Modules：`import / export`
- 不要 CommonJS（`require`）
- 默认导出少用（影响重构）
- 命名导出：`export function foo() { ... }`

### 错误处理

- 错误边界 + `try-catch`
- 不要静默吞错：`try { foo() } catch (e) { /* nothing */ }` ❌
- 用户可见的错误用 toast / UI 组件，不要 `alert`
- 错误上报用 Sentry 等

## 格式

- 2 空格缩进
- 单引号字符串（除非含单引号）
- 模板字符串：`\`hello ${name}\``
- 分号必加（Prettier）
- 尾逗号：`trailingComma: "all"`

## 推荐工具链

- ESLint + `@typescript-eslint`
- Prettier
- Vitest（前端测试，不要 Jest）
- Vite（不要 Webpack）
- TypeScript strict mode

## 反模式（绝对禁止）

- ❌ `var`（let / const）
- ❌ `==`（用 `===`）
- ❌ `console.log` 留生产代码（用 logger）
- ❌ `any`（用 `unknown`）
- ❌ `Function` / `Object`（具体类型）
- ❌ `document.querySelector` 而不 null 检查
- ❌ React 中直接修改 state（`state.x = 1`）
- ❌ `setTimeout(fn, 0)`（用 `requestAnimationFrame` / `queueMicrotask`）
- ❌ `eval` / `new Function(...)`（XSS / RCE）

## 引用

- Airbnb JavaScript Style Guide
- Google TypeScript Style Guide
- TypeScript 官方 Handbook
- React 官方文档（新版本）
