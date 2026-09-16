# 原则：质量、安全与 Git 工作流

> 质量门槛、环境安全、数据库规范、Git 工作流——所有写代码时的硬约束。

## 质量门槛

- 每个功能要有：正常流程、错误提示、加载态、空状态、基本输入校验
- 无敏感信息硬编码

## 环境与安全

- 浏览器可见的前缀变量不放密钥，AI 调用走服务端
- .env.example 进 Git，实际值进 .gitignore
- 不硬编码密钥、绝对路径、个人信息

## 数据库规范

- 表名字段名 snake_case，每表有 id、created_at、updated_at
- migration 用 ALTER TABLE，执行前查列或表是否已存在
- 参数化查询防注入，不裸拼 SQL

## Git 工作流

- 原子提交：每完成一个独立功能就 commit，一个 commit 一个逻辑变更
- commit message 用 feat、fix、refactor、chore、test 前缀（区分 TDD 步骤里的 test: 与 fix:）
- 提交门槛：编译通过才能 commit，不过编译不提交
- push 由 hook 处理，保护分支不自动推
- 两阶段 review 都过：echo clean > .codex/.needs-review → commit
