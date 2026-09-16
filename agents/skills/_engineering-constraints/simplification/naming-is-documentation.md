# 原则：命名即文档

> 好的命名 = 无需注释。坏命名 = 必须注释。

## 命名三原则

1. **意图明确**：看到名字就知道做什么
2. **不含实现细节**：名字不写"怎么做的"
3. **可搜索**：不在名字里塞特殊字符 / 中文

## 命名 vs 注释对照

```python
# ❌ 错误：名字含糊，注释解释
def process(data):
    # 把数据转成内部格式，调用下游服务
    pass

# ✅ 正确：名字即文档
def normalize_and_dispatch(raw_event: dict):
    pass
```

```typescript
// ❌ 错误
const tmp = getData();  // 临时变量，等下用
function handle(x) { /* 处理用户提交 */ }

// ✅ 正确
const normalizedUserInput = parseFormSubmission(rawInput);
```

## 命名长度建议

| 类型 | 长度 | 例 |
|---|---|---|
| 循环变量 | 1-2 字符 | `i, j, k`（仅循环内） |
| 局部变量 | 8-20 字符 | `userName, isActive, maxRetries` |
| 函数名 | 15-30 字符 | `calculateOrderTotal, sendWelcomeEmail` |
| 类名 | 15-25 字符 | `OrderProcessor, HttpClient` |
| 模块名 | 8-20 字符 | `order_service.ts` |

## 反模式

```python
# ❌ 反模式
tmp, foo, bar, baz, test, x, y, z, data, info, stuff, thing
a1, a2, a3 (并列无意义)
obj, o, o1, o2 (类型不明)
do_stuff, process, handle, manage (太泛)
data + 数字后缀: data1, data2

# ✅ 好的命名
userInput, parsedFormData, normalizedUserName
userService, paymentProcessor, emailValidator
orderRepository, httpClient
```

## 检测

- check_simplicity.py 检测：保留字 / 无意义名 / 拼音 / 中文名（混代码）
- code-review：检查命名是否解释意图

## 不变量名

- `i, j, k` 仅用于 `for i in range(n)` 这种 1-2 行循环
- `x, y, z` 仅用于数学 / 几何上下文
- 单字母函数名永远不要
