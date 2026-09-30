---
name: path-classification
description: Phase 0 之前先判定需求类型（spike / bounded / architectural），决定跳过哪些 phase、深度如何。与 0.5 产品类型路由叠加不冲突。
---

# 原则：3 路径分类

> 需求类型不同，工作深度不同。"能不能用 RAG 做 X"和"做一个完整电商系统"不能走同样的 8 阶段。

[定位]
    借鉴 superpowers brainstorming 的 spike / bounded / architectural 三路径分类，叠加在现有 0.5 产品类型路由之上（不冲突）。
    0.5 = 业务参照型 / 市场机会型（决定竞品/借鉴权重）
    path-classification = spike / bounded / architectural（决定跳过哪些 phase）

[三路径]
    [spike]
        可行性问题（"能不能…/可行吗…/快速试一下…"），输出是答案不是产品。
        - 跳过 Phase 0 商业快筛 / Phase 1.5/1.6 竞品扫描 / Phase 5 AI 能力 / Phase 6 UI 状态 / Phase 7.2 非功能
        - 仅走 Phase 1 问题确认 + Phase 3.5 pre-mortem + 一句话结论
        - 抛报告不是 spec 文件
    [bounded]
        已有项目的局部修改（新 flag / 新 endpoint / 一文件 fix）。
        - 跳过 Phase 0 / Phase 1.5/1.6 / Phase 5 / Phase 6.2 五态
        - 仅走 Phase 1 快速对齐 + Phase 4.2 功能拆解 + Phase 7.1 GWT 验收
        - 直接进 dev-builder，不走设计桥
    [arbitrary architectural]
        新项目 / 新模块 / 重塑组件关系（默认 0-1 模式走的就是这个）。
        - 走全部 Phase + 收尾多视角

[判定清单]
    问用户一句："这需求是哪种？"
    1. 输出是答案不是产品？ → spike
    2. 改动只在已有项目局部？ → bounded
    3. 都不沾？ → arbitrary architectural

[冲突时升级]
    如果问完发现一个需求看起来 spike 但讨论中变成 architectural，**升档**不降档。ratchet 单向。

[纪律]
    - 判定在 Phase 0 之前做
    - 跳过 phase 时在 Spec 顶部文档元信息表"版本内容"写明跳过了哪些
    - 迭代模式（已有 Spec 改需求）默认 bounded，跳过判定