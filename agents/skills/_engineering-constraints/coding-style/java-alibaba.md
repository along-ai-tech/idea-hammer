# Java 编码规范 — 阿里 Java 手册关键条款

> 引用《阿里巴巴 Java 开发手册》（黄山版 / 嵩山版），提取 AI 写代码必须遵循的条款。

## 强制条款（AI 必须遵循）

### 命名

- 类名 UpperCamelCase；方法、参数、变量 lowerCamelCase
- 常量 UPPER_SNAKE_CASE，**多个单词**全大写下划线分隔
- 包名全小写，不允许下划线
- 抽象类 `Abstract` 开头；异常类 `Exception` 结尾；测试类 `Test` 结尾
- 布尔变量不要加 `is` 前缀（POJO 序列化会破坏）

### OOP

- 禁止 `Object.equals(Object)` 与基本类型 `==` 混用（自动装箱 NPE 风险）
- 重写 `equals` 必须重写 `hashCode`
- 构造方法禁止加入业务逻辑（仅初始化）
- 类内方法定义顺序：公有 → 保护 → 私有 → getter/setter
- setter 禁止返回 `this`（破坏链式但增加复杂度）

### 集合

- `ArrayList` 默认 `new ArrayList<>(16)`，明确指定容量
- `HashMap` 同上；负载因子 0.75 默认
- `Arrays.asList()` 返回的 List 不可 add/remove → 转 `new ArrayList<>(Arrays.asList(...))`
- `subList` 是视图，操作会反映到原集合 → 谨慎使用
- `Collections.emptyList()` 而不是 `new ArrayList<>()`（空集合单例）

### 并发

- 线程池必须显式命名（`new ThreadPoolExecutor` + `ThreadFactory`）
- `ThreadLocal` 必须 `try-finally` 清理
- 锁的获取释放要对称（`lock.lock(); try { ... } finally { lock.unlock(); }`）
- 禁止使用 `Executors.newFixedThreadPool` 等便捷方法（默认队列无界 → OOM）
- `ConcurrentHashMap` 替代 `Hashtable`/`Collections.synchronizedMap`

### 控制语句

- `if` 嵌套不超过 3 层，超了用卫语句 / 策略模式
- 循环体内不要用 `try-catch`，提到外面
- 避免用 `Object` 判断类型（用 `instanceof` + 模式匹配 Java 16+）

### 注释与日志

- 注释用 `/** */`，行注释 `//`
- 类、字段、方法必须有 Javadoc 公共部分
- 日志：SLF4J + Logback，不用 `System.out.println` / `e.printStackTrace()`
- 日志级别：ERROR（需立即处理）/ WARN（注意但不阻塞）/ INFO（关键业务节点）/ DEBUG（调试）

### 异常

- 禁止捕获 `Exception` / `Throwable`，捕获具体异常
- 禁止 `throw new Exception("...")`，业务异常用具体子类
- 不要用异常做流程控制
- `finally` 块必须关闭资源（try-with-resources 优先）

### 单元测试

- 测试方法 `public void` 不带返回值
- 测试命名 `methodName_stateUnderTest_expectedBehavior`
- 不依赖执行顺序
- 断言要有意义（assertEquals 不用 assertTrue(a == b)）
- 覆盖率：行 ≥ 80%，分支 ≥ 70%

## 推荐条款（强烈建议）

- 使用 `Optional` 避免 NPE（不要 `Optional.get()` 直接拿，先 `isPresent()`）
- 字符串拼接用 `StringBuilder`（循环内）或 `String.format` / MessageFormat
- POJO 必须重写 `toString`
- `compareTo` 实现 `Comparator` 接口
- 用 `static final` 而非接口常量（接口常量是 public 的，破坏封装）

## 反模式（绝对禁止）

- ❌ `SimpleDateFormat` 不是线程安全的 → 用 `DateTimeFormatter`
- ❌ `Calendar.getInstance()` 创建开销大 → 用 `LocalDateTime`
- ❌ `Long` 转 `long` 自动装箱 → 小心 NPE
- ❌ `BigDecimal(double)` 精度丢失 → `BigDecimal.valueOf(double)` 或 `new BigDecimal("1.0")`
- ❌ `Arrays.asList(...).add(...)` → 抛 `UnsupportedOperationException`
- ❌ `ConcurrentHashMap` 直接迭代修改 → 抛 `ConcurrentModificationException`

## 引用

- [阿里 Java 手册 GitHub](https://github.com/alibaba/p3c)
- 《Effective Java》（Joshua Bloch）作为补充
