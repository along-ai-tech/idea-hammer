# 流程：生成模式（从 0 生成 DEV-PLAN.md）

> 用户已有 Product-Spec.md，需要从 0 生成 DEV-PLAN.md。

## 阶段 0：技术设计门禁

**目标**：技术方案先收敛，再排计划
**动作**：
1. 检查 Technical-Design.md 是否存在，且含架构图、模块边界、聚合不变量、数据约束、API Contract、ADR、风险
2. 缺失或不完整 → 先走 workflow-technical-design.md；存量项目可补最小版（架构 / 数据 / API）
3. 确认 Architecture 与 ADR 已定，没有「待定架构」

**完成**：Technical Design 就绪，可作为 Phase 拆分的依据

## 阶段 1：加载输入

**目标**：确认输入齐全
**动作**：
1. 读 Product-Spec.md 全文
2. 读 Technical-Design.md 全文
3. 读 Design-Brief.md（可选，缺了标降级）
4. 读设计稿（如有）
5. 读现有项目代码（如有）

**完成**：输入加载 + 现状理解

## 阶段 1.5：设计输入对齐

**目标**：UI 相关工作在设计层有据可依，不在实现时即兴设计
**动作**：
1. 从 Design-Brief 提取页面（SCREEN）与组件（CMP）清单，以及每页状态矩阵
2. 每个含 UI 的 DT 写 `**设计引用**：SCREEN-### / CMP-###`
3. P0 页面无 Brief 覆盖 → 退回 design-brief-builder 补齐，不直接排期
4. 无 Design-Brief 或页面未覆盖但非阻塞 → 标 `设计降级：按 Spec + 既定组件库实现`，并在验收标准里写明
5. 前端 DT 的完成判据必须包含交互与状态（Loading / Empty / Error / Success / Submitting）

**完成**：设计映射表就绪；降级项已标注

## 阶段 2：技术栈验证

**目标**：技术栈确定并验证
**动作**：
1. 读 Spec 提到的技术栈与 Technical Design 的 ADR
2. WebSearch 验证（版本 / 兼容性 / CVE / breaking changes）
3. 有 2-3 个合理选项 → 问用户选，结论回写 ADR
4. 补全：包管理器 / 部署目标 / 工具链

**完成**：技术栈确定

## 阶段 3：依赖图 + Phase 拆分

**目标**：拆出有序 Phase
**动作**：
1. 列功能点（从 Spec 提取）
2. 以 Technical Design 的模块边界与 DEV-PLAN 衔接表（§8）为底稿
3. 问每个"依赖什么"
4. 构建 DAG（依赖图）
5. 拓扑排序得 Phase 顺序（基础设施是根节点）
6. 优先级：核心先、重要中间、辅助和收尾最后
7. 风险前置

**完成**：Phase 序列

## 阶段 4：交付清单 + 关键文件

**目标**：每个 Phase 写清楚做什么
**动作**：
1. 每个 Phase 列交付清单（动词开头，描述用户可感知功能）
2. 每个 Phase 拆成 1~N 个 `DT-###`，每个 DT 写 `**关联需求**：REQ-###/AC-###-##`
3. 每个 Phase / DT 列关键文件（具体路径）

**完成**：DEV-PLAN.md 草稿 + 每个 DT 都有 REQ/AC 映射

## 阶段 5：信息充足度检查（详见 sufficiency-check.md）

**完成**：质量门禁达标

## 阶段 6：生成 + 自检

**目标**：输出 DEV-PLAN.md
**动作**：
1. 按 templates/dev-plan-template.md 填
2. 自检：无 TBD / Spec 功能全覆盖 / 依赖不冲突
3. 自检：每个 P0 REQ 至少一个 DT，每个 DT 的关联需求在 Spec 里真实存在
4. 写文件到项目根目录，跑 `python3 scripts/check_traceability.py --project <项目根>`

**完成**：DEV-PLAN.md 落地 + 追踪校验无 P0 缺口

## 失败处理

- 阶段 2 技术栈多选 → 问用户
- 阶段 3 Phase 太大/太小 → 重新拆
- 阶段 5 任何项不达标 → 不生成，回去补
