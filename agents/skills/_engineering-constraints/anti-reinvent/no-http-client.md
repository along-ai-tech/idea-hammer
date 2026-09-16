# 禁止自造 HTTP 客户端

> OkHttp / httpx / fetch / undici 已覆盖所有场景。

## 选型

| 语言 | 推荐 | 禁止 |
|---|---|---|
| Java | **OkHttp** / Spring RestTemplate | ❌ HttpURLConnection / 自造 |
| Python | **httpx**（同步 + 异步统一） | ❌ urllib / requests + 异步混用 |
| Node.js | **fetch**（原生） / undici | ❌ http 模块 / XHR / axios 老用法 |
| Go | **net/http**（标准库） / fasthttp | ❌ 自造 |

## Java 示例

```java
// ✅ 正确：用 OkHttp
OkHttpClient client = new OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS)
    .build();

Request request = new Request.Builder()
    .url("https://api.example.com/users")
    .build();

try (Response response = client.newCall(request).execute()) {
    return response.body().string();
}

// ✅ 正确：用 Spring RestTemplate / WebClient
ResponseEntity<User> resp = restTemplate.getForEntity(url, User.class);

// ❌ 错误：HttpURLConnection
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
// 老 API，难用，已被 OkHttp 替代
```

## Python 示例

```python
# ✅ 正确：httpx（同步 + 异步统一）
import httpx

# 同步
resp = httpx.get("https://api.example.com/users", timeout=10.0)
user = resp.json()

# 异步
async with httpx.AsyncClient() as client:
    resp = await client.get("https://api.example.com/users")
    user = resp.json()

# 错误处理
try:
    resp = httpx.get(url, timeout=10.0)
    resp.raise_for_status()
except httpx.HTTPError as e:
    log.error(f"HTTP failed: {e}")

# ❌ 错误：requests + asyncio（阻塞 event loop）
async def bad():
    import requests
    resp = requests.get(url)  # 阻塞！
```

## Node.js / TypeScript

```typescript
// ✅ 正确：用 fetch（原生）
const resp = await fetch('https://api.example.com/users', {
    signal: AbortSignal.timeout(10_000),  // 超时
});
if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
const user = await resp.json();

// ✅ 正确：undici（更高性能）
import { request } from 'undici';
const { body } = await request('https://api.example.com');

// ❌ 错误：http 模块
const req = http.request(url, callback);  // 老 API
```

## 反模式检测

- `import java.net.HttpURLConnection`（老 API）
- `new XMLHttpRequest()`（浏览器场景外）
- `axios` 老用法（已被 fetch + AbortController 替代）
- 自造 HTTP 客户端类

## 必须配超时

所有 HTTP 调用必须显式超时：
- 连接超时：5-10 秒
- 读超时：30-60 秒
- 总超时：业务预期 + buffer
