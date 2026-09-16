# 原则：YAGNI（You Aren't Gonna Need It）

> 不为假想的未来需求写代码。只写现在需要的。

## 核心

- 现在的需求：✅ 写
- 可能的未来需求：❌ 不写
- 抽象层"为了未来扩展"：❌ 不写

## 实际决策

| 场景 | YAGNI | 反 YAGNI |
|---|---|---|
| 加配置开关 | 只加现在需要的 | 加 "未来可能用到的" 配置项 |
| 设计模式 | 直接 if/else | Strategy / Factory / Template Method |
| 接口抽象 | 具体类足够 | 提前 abstract base class |
| 数据库字段 | 现在用的字段 | "以后可能加"字段 |
| API 端点 | 现在调用的 | "其他系统可能用" |
| 缓存 | 实测慢再加 | "未来用户多了会慢" |

## 判断信号

- 写代码时想"以后我可能..." → 大概率 YAGNI，删
- 加新参数 / 配置 / 选项 → 如果只有一个调用方，硬编码
- 写 helper 函数但只有一处调用 → 内联

## 何时不算 YAGNI

- **已知需求**（Spec 写了，只是当前 Phase 不做）→ 不是 YAGNI，是分阶段
- **公开 API 的向后兼容**（breaking change 成本极高）→ 应该预留
- **安全性**（永远先做）→ 不算 YAGNI
- **性能关键路径**（实测瓶颈）→ 不是 YAGNI

## 反模式

```python
# ❌ 错误：YAGNI 反例
class UserService:
    def get_user(self, id, include_deleted=False, fields=None, locale='en', version='v2'):
        # include_deleted：未来可能用
        # fields：未来可能用
        # locale：未来国际化
        # version：未来 API 版本
        pass

# ✅ 正确：只写现在需要的
class UserService:
    def get_user(self, id):
        # 当前 Spec 只说按 ID 查
        pass
```
