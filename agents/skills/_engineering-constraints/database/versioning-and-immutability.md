# versioning-and-immutability — 历史快照与不可变数据

> AI 改代码最常见的"上游改完下游挂"：实现时没考虑"这个字段被历史记录引用"。本文件给出硬规则。

## 核心规则

### 1. 必须版本化的字段（硬红线）

以下字段被历史记录（订单 / 合同 / 合规快照 / 财务凭证 / 审计日志）引用 → 修改时必须新建版本，**禁止 UPDATE 覆盖**：

- **价格 / 费率 / 折扣**
- **商品 / 服务规格 / SKU 描述**
- **业务规则 / 状态机定义**
- **权限 / 角色 / 授权范围**
- **税率 / 汇率 / 计价单位**
- **SLA / 响应时间承诺**
- **合同条款 / 法务声明**

→ 必须有 `version` / `effective_time` / `effective_from` 字段，或软删除（`deleted_at` + 新建）。

### 2. 修改前必查调用方（dev-builder 必查清单）

任何涉及"修改"业务的代码（`UPDATE` / `PUT` / `PATCH`）写入前必须：

1. **grep 该字段的所有引用方**：包括但不限于历史订单查询、报表、发票、合规导出、对账单
2. **判断引用方式**：
   - **快照式查询**（订单生成时复制了价格/规格到订单表）→ 可以 UPDATE
   - **关联式查询**（订单只存商品 ID，价格/规格每次实时 JOIN 商品表）→ 禁止 UPDATE，必须新建版本
3. **写了单元测试覆盖历史快照**：`test_old_order_returns_old_price` 是 dev-builder 启动这类功能时的 TDD 卡门

### 3. Spec 层防御（product-spec-builder 必查）

`eng-lens.md` Q1（数据快照与历史回溯）就是这条规则的 Spec 入口：
- 6. 数据模型节必须显式写"哪些字段有 version / 软删除"
- 7. 外部依赖若有写操作，必须写"失败兜底：失败时历史快照保留策略"

### 4. code-review Stage 2 必查（防 AI 漏掉）

```python
# 触发条件（伪代码）
if change.field in VERSIONED_FIELDS and change.op == "UPDATE":
    assert evidence("history_snapshot_preserved")
    assert evidence("grep_callers_done")
    fail("update_on_versioned_field_without_snapshot")
```

## 反模式

❌ 直接 `UPDATE products SET price = ? WHERE id = ?`，所有历史订单价格跟着变
❌ "先做简单版，以后补版本化"——历史数据污染不可逆
❌ "反正用户不会改"——业务发展的必然
❌ 只加 `version` 字段但不强制使用（形同虚设）

## 正例

✅ 商品表加 `valid_from` + `valid_to`，订单表冗余存 `price_at_purchase`
✅ 修改价格 = 关闭旧版本 + 创建新版本，订单永远 JOIN 到下单时的版本
✅ migration 必须包含"老数据自动版本化"脚本
✅ 写测试：`test_old_order_price_unchanged_after_product_update`

## 触发场景提示

开发以下功能时主动跑这个文件：
- 商品 / 价格 / 库存 修改
- 订单状态机流转
- 权限 / 角色 修改
- 规则引擎 / 配置中心
- 合同 / 协议 / 条款生成

## 关联文件

- dev-builder/principles/quality-and-security.md（基础规则）
- dev-builder/principles/engineering-constraints.md（必读入口）
- code-review/principles/stage2-checklist.md（Stage 2 检查项）
- product-spec-builder/principles/eng-lens.md（Spec 层入口）
