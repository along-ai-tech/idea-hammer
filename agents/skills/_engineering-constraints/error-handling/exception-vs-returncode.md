# 异常 vs 返回码

## 决策

| 场景 | 推荐 |
|---|---|
| 业务流程中的"可预期错误" | **抛业务异常** |
| 内部错误（DB 连接失败 / 第三方 API 失败） | **抛系统异常** |
| 边界检查（参数校验） | **校验失败抛异常** |
| 计算结果（成功 / 失败二选一） | 返回值 |

## 业务异常（可预期）

```java
// ✅ 正确：业务异常
public Order createOrder(CreateOrderDTO dto) {
    if (dto.getAmount() <= 0) {
        throw new BusinessException("INVALID_AMOUNT", "金额必须大于 0", HttpStatus.UNPROCESSABLE_ENTITY);
    }
    if (!user.hasQuota()) {
        throw new BusinessException("QUOTA_EXCEEDED", "用户配额不足", HttpStatus.CONFLICT);
    }
    // ...
}

// 调用方
try {
    Order order = orderService.create(dto);
} catch (BusinessException e) {
    if ("QUOTA_EXCEEDED".equals(e.getCode())) {
        return upgradePrompt();
    }
    throw e;
}
```

## 返回值（简单结果）

```java
// ✅ 正确：用返回值（不抛异常）
public Optional<User> findById(Long id) {
    return userRepository.findById(id);
}

// ✅ 正确：解析操作
public sealed interface ParseResult<T> {
    record Success<T>(T value) implements ParseResult<T> {}
    record Failure(String message) implements ParseResult<T> {}
}

public ParseResult<Config> parseConfig(String yaml) {
    try {
        return new Success<>(yamlMapper.readValue(yaml, Config.class));
    } catch (Exception e) {
        return new Failure("配置解析失败: " + e.getMessage());
    }
}
```

## 系统异常（不可预期）

```java
// ✅ 正确：让异常自然抛出
public List<Order> listOrders(Long userId) {
    return jdbc.queryForList("SELECT * FROM orders WHERE user_id = ?", userId);
    // 数据库连接失败 → 自动抛 DataAccessException
    // 不需要 catch
}
```

## 反模式

### ❌ 用返回码当异常

```java
// ❌ 错误：返回 -1 / null / false 表示错误
public int createOrder(...) {
    if (invalid) return -1;
    if (quotaExceeded) return -2;
    if (systemError) return -3;
    // 调用方：
    int code = createOrder(...);
    if (code == -1) ...
    else if (code == -2) ...
    // 难维护、难测试
}

// ✅ 正确：用异常
public void createOrder(...) {
    if (invalid) throw new InvalidArgumentException(...);
    if (quotaExceeded) throw new QuotaExceededException(...);
}
```

### ❌ 用异常做流程控制

```java
// ❌ 错误：用异常当 if
try {
    user = userRepository.findById(id);
} catch (NotFoundException e) {
    user = createDefaultUser();
}
// 用 Optional
Optional<User> user = userRepository.findById(id).orElseGet(() -> createDefaultUser());
```

### ❌ 太宽泛的 catch

```java
// ❌ 错误
try {
    riskyOperation();
} catch (Exception e) {
    log.error("failed", e);
}
// 不知道到底什么失败、怎么失败

// ✅ 正确
try {
    riskyOperation();
} catch (SpecificException e) {
    log.error("Expected failure", e);
    handle(e);
} catch (RuntimeException e) {
    log.error("Unexpected failure", e);
    throw e;
}
```

### ❌ 吞异常

```java
// ❌ 错误
try {
    closeResource();
} catch (IOException e) {
    // 什么也不做
}

// ✅ 正确
try {
    closeResource();
} catch (IOException e) {
    log.warn("Failed to close resource", e);
    // 或者抛出
    throw new UncheckedIOException(e);
}
```
