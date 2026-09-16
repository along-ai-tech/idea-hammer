# 原则：抽象时机（Rule of Three）

> 第三次出现才抽象。"两次就抽象"是过度设计。

## 经验法则

```
1st occurrence: 直接写（copy-paste 都行）
2nd occurrence: 警觉，但还能忍（注释 TODO）
3rd occurrence: 抽象（extract function / class）
4th+ occurrences: 用抽象
```

## 反"两次就抽象"

- "DRY 必须"是过度设计
- 重复 < 3 次时抽象 = 抽象层级过深 = 难懂
- 重复 ≥ 3 次 = 真有规律 = 该抽象

## 抽象的代价

每多一层抽象：
- 学习成本：+1（新人要懂接口）
- 修改成本：+1（改实现要改接口）
- 测试成本：+1（mock 接口）

**所以**：抽象要有显著收益（消除 ≥ 3 次重复 + 边界稳定）。

## 何时应该提前抽象

- **公开 API**：外部依赖，破坏成本高 → 抽象要稳
- **安全相关**：auth / crypto / permission → 必须抽象（接口稳定优先）
- **业务核心领域**：订单 / 支付 / 用户 → 抽象 + 文档
- **Spec 明确要求**：3 个 Feature 都用同一个组件 → 提前做

## 反模式

```typescript
// ❌ 错误：第一次出现就抽象
// 场景：只有 UserCard 需要 renderName
function renderName(user: User): string {
  return user.name;
}

// 又写 Card / ProductCard 时复制 renderName
// 这是正常 copy-paste，不是抽象时机

// ✅ 正确：第二次出现时忍
// 第三次出现时抽象：
function renderEntityName(entity: { name: string }): string {
  return entity.name;
}
```

## 检测

- "我应该提前抽象吗" 自检：先数重复次数
- code-review：第一次出现就抽象的代码标 "premature abstraction"
