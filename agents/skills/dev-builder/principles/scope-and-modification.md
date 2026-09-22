# 原则：范围纪律与修改纪律

> 只动当前 Phase 和 Task 范围内的东西，范围外的不碰；改之前想清楚，不改坏已有功能。

## 范围纪律

- 只动当前 Phase 和 Task 范围内的东西，范围外的不碰，哪怕 Spec 里写了该行为
- 接到任务时先读 DEV-PLAN.md 确认当前 Phase / Task 范围

## 修改前

- 评估影响范围：先 grep 全项目列出所有引用点
- 删或改一个被多处引用的东西（常量、导出、内置数据、组件、接口、文案）前，一次性同步清理，别只改定义留下游脱节

## 修改后

- 改完跑全测试套件（typecheck + 单测 + e2e）
- 不靠 typecheck 一条路就判定通过——typecheck 过不代表单测/e2e 不挂

## 持久化连带

- 删/改的东西若会被持久化（写进 db、本地存储、缓存、配置文件），还要管已经落库的存量数据
- 加启动迁移清理或做兼容，否则老用户的旧数据会变成「代码已删、却顽固显示、还删不掉」的僵尸
- 删持久化数据的改动配一条迁移测试

## 影响范围分析（必读 compatibility/）

改任何代码 / schema / API 前必做 [blast-radius.md](../../_engineering-constraints/compatibility/blast-radius.md) 分析：

### 4 类外部世界
1. **数据**：老数据 / 持久化（见 data-migration.md 的 snapshot + Expand-Contract）
2. **API**：老客户端 / 调用方（见 backward-compatibility.md + api-versioning.md）
3. **用户**：老用户行为状态（localStorage / 草稿 / 工作流）
4. **依赖**：内部模块 / 第三方 SDK

### 完整性交付 8 项 Checklist

每次提交必过 [completeness-delivery.md](../../_engineering-constraints/compatibility/completeness-delivery.md)：

1. 代码本身（+ TDD + check_simplicity）
2. 数据（migration + backfill + 校验）
3. API（向后兼容 + 版本号）
4. 用户状态（迁移 + 兼容）
5. 依赖（grep import + SDK changelog）
6. 文档（API + 迁移指南 + CHANGELOG）
7. 测试（老 + 新 + 边界 + 契约）
8. 监控 + 回滚（metric + log + alert + feature flag + 回滚方案）

### 实战：商品加版本

如果业务说"商品要加版本"，必须按 `data-migration.md` 的 snapshot + versioning 组合做：
- order_items 存 product_snapshot JSON（购买时完整快照）
- products 加 current_version 字段
- 老订单读 product_snapshot，不读 products 实时字段
- 详情见 compatibility/completeness-delivery.md 实战部分
