# 需求追踪（Traceability）

> 从需求到发布的每条链路都要有稳定 ID，能被机器解析、能被脚本校验。只知道"功能开发了"不够。

[链路]
    需求 → 用户任务 → 开发任务 → 测试 → 发布版本
    REQ  → TASK     → DT       → TEST → vX.Y.Z

    每个箭头都必须靠 ID 显式关联，不靠文件名、标题或记忆：
    - Product-Spec.md：REQ 声明关联 TASK / FLOW，并给出可测试的 AC
    - DEV-PLAN.md：每个开发任务 DT 声明覆盖的 REQ / AC
    - 测试代码：每条测试声明自己的 TEST ID 和验证的 REQ / AC
    - RELEASE.json：发布清单声明版本、覆盖的 REQ、通过的 TEST
    - Product-Spec-CHANGELOG.md：每次需求变更声明影响的 REQ / DT / TEST

[ID 规范]

| 类型 | 格式 | 示例 | 定义位置 | 规则 |
|------|------|------|----------|------|
| 需求 | `REQ-###` | `REQ-003` | Product-Spec §5 | 全局唯一，只增不改 |
| 验收标准 | `AC-<REQ>-<nn>` | `AC-003-01` | Product-Spec §5 | 挂在 REQ 下，全局唯一 |
| 用户任务 | `TASK-###` | `TASK-005` | Product-Spec §3 | 用户目标，不含实现 |
| 用户流程 | `FLOW-###` | `FLOW-001` | Product-Spec §4 | 可跨多个 REQ |
| 范围项 | `SCOPE-###` / `OUT-###` | `SCOPE-001` | Product-Spec §2 | 做 / 不做 |
| 开发任务 | `DT-###` | `DT-004` | DEV-PLAN | 一个 DT 可覆盖多个 REQ |
| 测试 | `TEST-###` | `TEST-012` | 测试代码注解 | 一条测试一个 ID |
| 版本 | `vMAJOR.MINOR.PATCH` | `v1.0.0` | RELEASE.json | SemVer |

    ID 一旦发布就不复用、不重编号。需求删除标 `[已废弃]`，新需求用新号。
    AC 编号必须带所属 REQ 前缀，禁止每条 REQ 内从 AC-001 重新开始。

[Product-Spec 写法]
    ### REQ-003: 评论
    **优先级：** P0
    **关联任务：** TASK-005 / TASK-008
    **关联流程：** FLOW-001
    **验收标准：**
    - [ ] AC-003-01: Given 博客存在, when 提交非空评论, then 返回 201 且评论可见.
    - [ ] AC-003-02: Given 内容为空, when 提交, then 返回 422.

[DEV-PLAN 写法]
    ### DT-004 · 评论创建与删除
    **关联需求：** REQ-003 / AC-003-01 / AC-003-02
    **关键文件：** `app/api/comments.py`
    **验收：** AC-003-01 / AC-003-02 对应测试全绿

    每个 DT 至少关联一个 REQ。没有 REQ 的 DT 视为范围外任务，需在 DEV-PLAN 标注原因。

[测试注解]
    在测试函数上方（或文件顶部）加一行注解，注释符随语言：
    # @trace TEST-012 REQ-003/AC-003-01
    // @trace TEST-012 REQ-003/AC-003-01

    规则：
    - 格式 `@trace TEST-### REQ-###/AC-###-##`；可追加多个 `REQ/AC`，空格或逗号分隔
    - 只写 `REQ-003` 表示覆盖需求但不精确到 AC
    - 注解放在测试声明上方 5 行内；一条注解声明一个 TEST，一个 TEST 对应一条测试
    - TEST ID 全局唯一；改测试语义时换新 ID，不挪旧号
    - 脚本默认扫描 `test_*.py` / `*_test.py` / `*.test.ts(x)` / `*.spec.ts(x)` / `*_test.go` / `*Test.java` / `*.test.dart`

[RELEASE.json]
    {
      "version": "v1.0.0",
      "date": "2026-11-25",
      "commit": "a1b2c3d",
      "requirements": ["REQ-001", "REQ-002"],
      "tests": {"total": 29, "passed": 29, "ids": ["TEST-001", "TEST-002"]},
      "changelog": "Product-Spec-CHANGELOG.md#v100"
    }

    发布前校验：版本号合法；P0 REQ 全部出现在 requirements；tests.ids 都能在代码里找到；
    tests.passed == tests.total；任一不满足不得发布。
    tests.ids 只列带 @trace 的测试；health 等纯基础设施测试计入 total，但不强行挂需求。

[变更影响]
    Product-Spec-CHANGELOG.md 每个版本块下加：

    ### 影响追踪
    | 类型 | ID | 影响 |
    |------|----|------|
    | REQ | REQ-003 | 新增 AC-003-03，评论需审核 |
    | DT | DT-004 | 需重做评论创建逻辑 |
    | TEST | TEST-012 | 需补审核态断言 |

    查询某需求的影响面：
    python3 scripts/check_traceability.py --project <项目根> --impact REQ-003

[校验]
    python3 scripts/check_traceability.py --project <项目根>
    python3 scripts/check_traceability.py --project <项目根> --strict
    python3 scripts/check_traceability.py --project <项目根> --write TRACEABILITY.md

    默认规则（失败退出码 1）：
    - REQ / AC / DT / TEST ID 重复，或引用了不存在的 ID
    - P0 REQ 没有开发任务、没有测试、没有进入发布清单
    - AC 前缀与所属 REQ 不一致
    - RELEASE.json 版本号非法或 tests.passed != tests.total

    警告项（--strict 时升级为失败）：
    - P0 REQ 缺 AC
    - P1 REQ 缺开发任务 / 测试 / 发布
    - DT 未关联 REQ
    - AC 没有被任何测试引用

[纪律]
    - 先有 REQ/AC，再有 DT/TEST；禁止先写代码后补编号
    - 编号是接口，不是注释；改编号等于破坏下游引用
    - 发布门禁只看链路证据，不看"我觉得测过了"
    - 需求变更先更新 Spec/CHANGELOG，再跑 --impact 找 DT/TEST 影响面，最后动代码
