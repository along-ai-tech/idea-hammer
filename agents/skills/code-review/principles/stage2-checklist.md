# 原则：Stage 2 审查维度（做好了没有）

> Stage 2 才进。Stage 2 不通过 = dev-builder / bug-fixer 必须修。

## 代码质量

- 命名规范、无 any、文件 ≤ 300 行、单一职责、无重复、错误处理

## 工程级约束符合度（必查）

- 对照 `_engineering-constraints/anti-reinvent/` 检查是否造轮子
  - 连接池 / 日期 / 集合 / HTTP / JSON / 线程池 / 分布式锁 / ID / 缓存 / 配置
- 库选择合规
  - Java 用 Hutool 不用自造工具
  - Python 用 pydantic 不用手写校验
  - 锁用 Redisson 不用 SETNX
- 安全基线
  - 硬编码密钥 / 字符串拼 SQL / MD5 存密码 / Fastjson 1.x
- 性能
  - N+1 / SELECT * / 无 LIMIT / 深分页 / 无超时
- 错误处理
  - 吞异常 / 不带 stacktrace / 把内部异常返给前端

## 测试真实性 + TDD 合规

- **测试是否先写**：git blame 抽样，测试 commit 时间早于或同于生产代码
- **预期值是否独立推导**：手算/字面量/表驱动，不用被测代码生成（mirror assertion 揪出）
- **断言是否测真实行为**：`expect(mock).toBe...` 算无效断言
- **mock 是否镜像真实数据结构全字段**：只镜像测试读到的字段 = 部分 mock
- **mutation check**：脑里改一处生产代码（错常量、错分支、漏副作用、空返回、漏校验），至少一个测试应失败
- **故障路径和交互层有没用例真的走到**：只测纯函数和顺畅路径的标测试盲区
- **边界用例**：空、零、nil、未授权、畸形输入有无覆盖
- 工具链自动生成的中间代码豁免 TDD；AI 生成代码不豁免

## 安全扫描

- Grep 搜：`eval(`、`dangerouslySetInnerHTML`、`innerHTML`、`VITE_.*KEY|SECRET|TOKEN`、`/Users/`、`password.*=.*['"]`、`sk-ant-|sk-proj-`、`ANTHROPIC_API_KEY`、`OPENAI_API_KEY`

## Spec 漂移

- 代码里有 Spec 没写的页面 / API / 表 / 组件 → 标"可能 scope creep"

## 代码简洁性（必查，对照 [simplification/ 10 条原则](../../_engineering-constraints/simplification/)）

- [ ] 文件 ≤ 300 行、函数 ≤ 50 行、圈复杂度 ≤ 10、嵌套 ≤ 3 层、参数 ≤ 4 个
- [ ] 无 YAGNI 失守（"以后用" / "预留" 接口 / 配置 / 字段）
- [ ] 抽象时机正确（Rule of Three，第 3 次重复才抽象）
- [ ] 单一职责（函数名有"and"通常是反模式）
- [ ] 命名即文档（无 a / tmp / foo / bar / data1 这类无意义名）
- [ ] 注释解释 why 不解释 what（注释掉的代码 = dead code）
- [ ] 依赖最小化（不引入 stdlib 能解决的包）
- [ ] 副作用隔离（纯函数优先，副作用集中到边界）
- [ ] 幂等性（脚本 / hook 反复执行安全，同操作不重复追加）

自动校验：`python3 scripts/check_simplicity.py path/to/file.py`
