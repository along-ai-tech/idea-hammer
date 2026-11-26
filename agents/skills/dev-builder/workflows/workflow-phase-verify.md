# 流程：四步走验证（Phase 完成度判断）

> 所有 Task 完成后必须过四步走，全通过才算 Phase 完成。

## 第一步：Code Review

**目标**：对照交付清单逐项确认 + 检查超范围改动
**动作**：
1. 对照 DEV-PLAN 当前 Phase 交付清单逐项确认
2. 检查 git diff 有无超范围改动（不该动的文件被动过）
3. spawn code-reviewer 跑两阶段审查（Stage 2 检 TDD 合规）

**完成**：交付清单逐项确认 + 无超范围改动

## 第二步：测试完整性 + TDD 合规

**目标**：所有功能有测试 + 测试满足纪律
**动作**：
1. 每个行为点都有测试，测试 commit 时间早于或同于生产代码（git blame 抽查）
2. 每条测试的 `@trace TEST-### REQ-###/AC-###-##` 指向当前 Phase 的 DT
3. 不算 TDD 的标"测试后挂"
4. 每条「绿」能证明行为真的对：独立推导预期值（手算、字面量、表驱动），不用被测代码生成
5. 用假前提或不可达输入把缺陷盖成预期等于没测，揪出
6. 断言测真实行为，不测 mock 存在
7. 功能声明的错误态、空态、边界要有用例真的走到
8. mutation check 过：脑里改一处生产代码，至少一个测试要失败
9. 工具链自动生成的中间代码豁免 TDD；AI 生成代码不豁免
10. 跑 `python3 scripts/check_traceability.py --project <项目根>`，确认本 Phase 的 REQ/AC 无未覆盖项
11. 测试层级齐（对照 principles/test-pyramid.md）：本 Phase 该有的 Unit / Integration / Contract / E2E 层都有，缺的写明理由
12. 并发不变量门禁：业务规则里有"不允许重复 / 不允许超量"时，单元测试 + 数据库唯一约束 + 并发测试三件套齐全
13. 回归：本 Phase 改动后跑全套测试，不只跑新增的那几条

**完成**：TDD 合规 + 追踪校验通过

## 第三步：编译验证

**目标**：TypeScript / Lint 零错误
**动作**：
1. 跑 `tsc --noEmit`（或对应语言的类型检查）
2. 跑 linter（eslint / ruff 等）
3. 零错误零警告

**完成**：tsc --noEmit 零错误

## 第四步：功能测试

**目标**：启动 dev server 无错，新功能可用，现有功能未破坏
**动作**：
1. 启动 dev server 无错
2. 新功能可用（手动 / API 调用验证）
3. 现有功能未破坏（跑 e2e / 回归测试）
4. 有 Playwright 测核心流程，无则 curl 查 API 返回再提醒用户看 UI

**完成**：dev server 起得来 + 新功能 + 现有功能 + e2e/curl 通过

## 四步走之后：持久化开发进度

**目标**：让下一个 Session 能接着干，而不是重新分析整个项目
**动作**：
1. 更新 session.json 的 current_phase / current_task
2. 记 checkpoint，带上本 Phase 的测试证据与下一步：
   `python3 scripts/session.py checkpoint --phase "<Phase>" --task "<最后完成的 DT>" --commit "$(git rev-parse --short HEAD)" --tests '{"unit_test":"passed","integration_test":"passed"}' --next "<下一步>" --artifacts "Technical-Design.md,DEV-PLAN.md"`
3. 关键决策追加到 session.json 的 key_decisions，并落到 DECISIONS.md 或 Spec 原文

**完成**：session.json 有新 checkpoint + 下一步写得出来

## 每步附证据

- 每步必须当场跑命令，把输出贴在汇报里
- 中间有任何改动，四步重新来
- 通过后向用户汇报附证据，用户确认后 Phase 完成
- 修验证中发现的问题用 fix: 提交
- checkpoint 里的测试结论是"当时的快照"，恢复时要重新核实（代码变过就重跑），见 CONTEXT.md
