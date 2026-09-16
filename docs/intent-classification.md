# 意图分类（Intent Classification）

> 替代 description 关键词匹配。基于规则 + 启发式对用户 prompt 分类到最匹配 skill。

## 当前方案：关键词 + 规则启发式

骨架版本（不调 LLM），按 description 提取触发关键词 + 通用动词加权。

## 算法

```python
def classify(prompt):
    for skill in skills:
        score = 0
        for trigger in skill["triggers"]:
            if trigger in prompt:
                score += 2
        if skill["name"] in prompt:
            score += 5
        for verb in ["写代码", "改需求", "审查", "修 bug", ...]:
            if verb in prompt and verb in skill.description:
                score += 1
    return top N by score
```

## 用法

```bash
# 分类
python3 scripts/intent_classifier.py classify --prompt "我想做一个 X"

# Top N
python3 scripts/intent_classifier.py classify --prompt "改需求" --top 3

# 列所有 skill
python3 scripts/intent_classifier.py list
```

## 测试场景

| Prompt | 预期 Top 1 |
|---|---|
| "我想做一个产品" | product-spec-builder |
| "这个功能报错了" | bug-fixer |
| "帮我审查代码质量" | code-review |
| "打包发布我的应用" | release-builder |
| "我要定设计风格" | design-brief-builder |

## 验证

6 个契约测试在 `tests/contract/test_intent_classifier.py`。

## 升级路径

骨架版本只覆盖"明显场景"。三个升级方向：

1. **LLM 分类**（准确率最高）：
   - 把所有 skill description 作为系统 prompt
   - 用户 prompt 一次性分类到 skill + 触发模式
   - 成本：每次调用 LLM

2. **Embedding 相似度**（速度最快）：
   - 预计算每个 skill description 的 embedding
   - 用户 prompt embedding vs skill embedding 余弦相似度
   - 成本：embedding 模型

3. **混合方案**（推荐）：
   - 关键词匹配做粗筛（top 5）
   - LLM 在 top 5 中精排（top 1）
   - 兼顾速度 + 准确率

## 验收

- [x] scripts/intent_classifier.py — 关键词 + 规则启发式
- [x] tests/contract/test_intent_classifier.py — 6 个契约测试
- [x] docs/intent-classification.md — 设计文档
