# 禁止自造日期工具

> Java 8+ `java.time` / Python `pendulum` / JavaScript `date-fns` 已经完全够用。

## Java

**使用 `java.time`（JDK 8+）**，不用 `Date` / `Calendar` / `SimpleDateFormat`：

```java
// ✅ 正确
LocalDateTime now = LocalDateTime.now();
LocalDate date = LocalDate.of(2026, 9, 16);
Instant instant = Instant.now();
ZonedDateTime shanghai = instant.atZone(ZoneId.of("Asia/Shanghai"));

// 时间差
Duration duration = Duration.between(start, end);
Period period = Period.between(startDate, endDate);

// 格式化（DateTimeFormatter 线程安全）
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String str = date.format(fmt);

// 解析
LocalDate parsed = LocalDate.parse("2026-09-16", fmt);

// ❌ 错误：自造 DateUtil
public class DateUtil {
    public static String format(Date date, String pattern) { ... }  // 不要
}

// ❌ 错误：用 SimpleDateFormat（非线程安全）
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
// 多线程共享会出错
```

## Python

**使用 `pendulum`**（或 `arrow`，或标准库 `datetime`）：

```python
# ✅ 正确：用 pendulum
import pendulum
now = pendulum.now("Asia/Shanghai")  # 带时区
dt = pendulum.parse("2026-09-16")
formatted = dt.to_iso8601_string()
human = dt.diff_for_humans()  # "1 day ago"

# ✅ 正确：UTC 存储 + 本地显示
utc_dt = pendulum.now("UTC")
local_dt = utc_dt.in_timezone("Asia/Shanghai")

# ❌ 错误：自造
def format_date(date, pattern):
    return ...  # 不要
```

## JavaScript / TypeScript

**使用 `date-fns`**（不用 moment，已停更）：

```typescript
import { format, parseISO, addDays, isAfter } from 'date-fns';

const now = new Date();
const formatted = format(now, 'yyyy-MM-dd');
const tomorrow = addDays(now, 1);
const parsed = parseISO('2026-09-16');
```

## 反模式检测

code-review Stage 2 grep：
- `class.*DateUtil`（自造）
- `SimpleDateFormat`（非线程安全）
- `moment(`（已停更）
- `new Date().getFullYear()` + 字符串拼接

## 时区原则

- **存储**： UTC（`TIMESTAMP` / `TIMESTAMPTZ`）
- **计算**： UTC
- **显示**： 本地时区（前端转换）
