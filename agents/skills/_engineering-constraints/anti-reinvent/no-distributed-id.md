# 禁止自造分布式 ID

> Snowflake 算法 / Leaf / UUIDv7 都已成熟。

## 选型

| 语言 | 推荐 | 理由 |
|---|---|---|
| Java | **Hutool** `IdUtil` / 美团 Leaf / 百度 UID | Snowflake 实现 |
| Python | **uuid.uuid4()** / `ulid-py` | 标准库 / ULID |
| Node.js | **uuid** / **ulid** | 主流库 |
| Go | **google/uuid** / **oklog/ulid** | 官方 / ULID |

## 选 ID 类型

| 场景 | 推荐 ID 类型 | 理由 |
|---|---|---|
| 数据库主键（自增也行） | UUIDv7 / ULID / Snowflake | 全局唯一 + 趋势递增 |
| 用户 ID（对外暴露） | UUIDv7 / Snowflake | 防猜测（不要自增 int） |
| 订单号 | Snowflake + 业务前缀 | 趋势递增 + 高性能 |
| 短链 ID | nanoid | 短 + URL 安全 |
| 分布式追踪 ID | UUIDv4 | 通用 |

## Java 示例

```java
// ✅ 正确：用 Hutool（Snowflake 实现）
import cn.hutool.core.lang.UUID;
import cn.hutool.core.util.IdUtil;

long id = IdUtil.getSnowflake(1, 1).nextId();  // 参数：workerId, datacenterId
String uuid = UUID.randomUUID().toString();

// ✅ 正确：用美团 Leaf
// 配置 Leaf 集群，每个节点分配 datacenterId + workerId

// ❌ 错误：自造雪花
public class MySnowflake {
    private long sequence = 0L;
    private long lastTimestamp = -1L;
    public synchronized long nextId() { ... }  // 时钟回拨、机器 ID 分配都是坑
}

// ❌ 错误：System.currentTimeMillis()（多机冲突）
long id = System.currentTimeMillis();
// 不同机器同一毫秒生成相同 ID
```

## Python 示例

```python
# ✅ 正确：UUIDv4（标准库）
import uuid
uid = uuid.uuid4()  # 'e6c4b2a-9b9b-4a8e-8b6f-1234567890ab'

# ✅ 更好：UUIDv7（趋势递增 + 全局唯一）
import uuid7  # pip install uuid7
uid = uuid7.uuid7()  # '018e3a4c-9b9b-7890-1234-56789abcdef0'

# ✅ 更好：ULID
import ulid
u = ulid.new()  # 26 字符，趋势递增

# ❌ 错误：自造
def my_id():
    return str(int(time.time() * 1000)) + str(random.randint(0, 999))
# 多机时钟漂移 + 重复
```

## 反模式检测

- `System.currentTimeMillis()` + random
- `UUID.randomUUID().toString()` 但项目需要趋势递增（性能差，B+ 树分裂）
- 自造雪花算法
- `random.randint(0, 999999)`（重复率高）

## Worker ID 分配

Snowflake 必须解决 workerId 分配（避免冲突）：
1. **数据库分配**：Leaf 方案
2. **Redis 分配**：启动时 incr 一个 key
3. **配置分配**：每台机器手动配不同 workerId
4. **Zookeeper 顺序节点**

禁止硬编码 `workerId = 1`（多机部署会冲突）。
