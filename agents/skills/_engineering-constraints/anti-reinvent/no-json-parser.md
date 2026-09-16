# 禁止自造 JSON 解析

> Jackson / Fastjson2 / Gson / orjson / pydantic 已完全够用。

## 选型

| 语言 | 推荐 | 禁止 |
|---|---|---|
| Java | **Jackson** | ❌ Fastjson 1.x（有安全漏洞）/ 自造 |
| Python | **pydantic**（首选）/ **orjson** | ❌ json.loads 配手写校验 |
| Node.js | **JSON.parse**（原生） | ❌ 自造 |
| Go | **encoding/json**（标准库） | ❌ 自造 |

## Java 示例

```java
// ✅ 正确：用 Jackson
ObjectMapper mapper = new ObjectMapper();
mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
User user = mapper.readValue(jsonString, User.class);
String json = mapper.writeValueAsString(user);

// ✅ 正确：Spring Boot 自动注入
@RestController
public class UserController {
    @PostMapping
    public User create(@RequestBody User user) {  // 自动反序列化
        return user;
    }
}

// ❌ 错误：用 Fastjson 1.x（有 CVE）
import com.alibaba.fastjson.JSON;
User user = JSON.parseObject(json, User.class);  // 反序列化漏洞

// ❌ 错误：自造 JSON 解析
public static Object parseJson(String json) { ... }
```

## Python 示例

```python
# ✅ 正确：用 pydantic（带校验）
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # 自动校验

user = User.model_validate_json(json_str)  # 校验失败抛 ValidationError
json_str = user.model_dump_json()

# ✅ 正确：用 orjson（高性能）
import orjson
data = orjson.loads(json_bytes)
json_bytes = orjson.dumps(data)

# ❌ 错误：手写校验
import json
data = json.loads(json_str)
if 'email' not in data:  # 手写
    raise ValueError("missing email")
if not re.match(r'.*@.*', data['email']):  # 手写
    raise ValueError("invalid email")
```

## 反模式检测

- `import com.alibaba.fastjson`（用 Fastjson 1.x）
- `JSON.parse` 不带类型参数
- 自造 JSON 解析器
- `json.loads` 后手写字段校验（用 pydantic）
