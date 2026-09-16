# 错误信息规范

## 用户可见消息（前端展示）

### 原则

1. **清楚**：用户能理解
2. **简洁**：不超过 30 字
3. **可操作**：告诉用户怎么办
4. **礼貌但不奉承**：不用"抱歉给您""

### 示例

```
✅ ✅ 正确
"订单创建成功"
"用户不存在"
"邮箱格式不正确"
"密码长度至少 8 位"
"该订单已支付，无法取消"
"系统繁忙，请稍后重试"
"网络异常，请检查连接"

❌ 错误
"内部错误"（太笼统）
"操作失败"（没说为什么）
"Invalid input parameter xxx"（英文）
"很抱歉，系统出现异常..."（啰嗦 + 奉承）
"Something went wrong"（英文 + 笼统）
```

### 分类

| 类别 | 风格 | 例 |
|---|---|---|
| 成功 | 简短陈述 | "操作成功" |
| 业务错误 | 陈述 + 原因 | "邮箱已注册" |
| 校验失败 | 字段 + 规则 | "邮箱格式不正确" |
| 系统错误 | 笼统 + 建议 | "系统繁忙，请稍后重试" |

## 开发者日志（排查用）

### 原则

1. **必须带 context**（userId / orderId / traceId）
2. **必须带 stacktrace**（ERROR 级别）
3. **结构化字段**（不用字符串拼接）
4. **不重复**（不在多层 catch 重复 log）

### 示例

```java
// ✅ 正确：带 context + 结构化
log.error("Order creation failed, userId={}, amount={}, traceId={}",
    userId, amount, MDC.get("trace_id"), e);  // 异常作为最后一个参数

// ❌ 错误：字符串拼接
log.error("Order creation failed for user " + userId + ": " + e.getMessage());

// ❌ 错误：丢 stacktrace
log.error("Order creation failed: {}", e.getMessage());

// ❌ 错误：多 catch 都 log
try {
    foo();
} catch (Exception e) {
    log.error("foo failed", e);  // 第一次
    throw e;
}
// 上层 catch
try {
    bar();
} catch (Exception e) {
    log.error("bar failed", e);  // 重复 log
    throw e;
}
```

## i18n 错误消息

```java
// ✅ 正确：用 MessageSource 支持多语言
@Component
public class ErrorMessages {
    @Autowired
    private MessageSource messageSource;
    
    public String get(String code, Locale locale, Object... args) {
        return messageSource.getMessage(code, args, locale);
    }
}

// 配置文件
// messages_zh.properties
error.user.not_found=用户不存在
error.order.invalid_state=订单状态无效

// messages_en.properties
error.user.not_found=User not found
error.order.invalid_state=Invalid order state
```

## 反模式

- ❌ 用户消息带 emoji（不专业）
- ❌ 用户消息带感叹号（"出错了！"）
- ❌ 用户消息用第一人称（"我不理解您的请求"）
- ❌ 用户消息过长（> 50 字）
- ❌ 用户消息泄露技术细节（"SQL 语法错误"）
- ❌ 多语言用 if-else（用 MessageSource）
