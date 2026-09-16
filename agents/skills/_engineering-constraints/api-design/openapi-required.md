# OpenAPI 强制

## 规则

**所有 REST API 必须生成 OpenAPI（Swagger）文档**。

## Spring Boot

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>
```

```yaml
springdoc:
  api-docs:
    path: /v3/api-docs
  swagger-ui:
    path: /swagger-ui.html
```

```java
@Operation(summary = "创建订单", description = "需要 Idempotency-Key")
@ApiResponses({
    @ApiResponse(responseCode = "201", description = "创建成功"),
    @ApiResponse(responseCode = "422", description = "参数校验失败")
})
@PostMapping("/orders")
public Order createOrder(
    @Parameter(description = "幂等键") @RequestHeader("Idempotency-Key") String key,
    @RequestBody OrderDTO dto
) { ... }
```

访问 `/swagger-ui.html` 看文档。

## FastAPI（Python）

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API 文档",
    version="1.0.0",
)

@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    idempotency_key: str = Header(..., description="幂等键"),
    dto: OrderDTO = Body(...)
):
    ...
```

访问 `/docs`（Swagger UI）/ `/redoc`（ReDoc）。

## Express（Node.js）

```bash
npm install swagger-jsdoc swagger-ui-express
```

```typescript
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';

const spec = swaggerJsdoc({
    definition: {
        openapi: '3.0.0',
        info: { title: 'My API', version: '1.0.0' },
    },
    apis: ['./routes/*.ts'],  // JSDoc 注释
});

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(spec));
```

```typescript
/**
 * @openapi
 * /orders:
 *   post:
 *     summary: 创建订单
 *     parameters:
 *       - name: Idempotency-Key
 *         in: header
 *         required: true
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/OrderDTO'
 *     responses:
 *       201:
 *         description: 创建成功
 */
router.post('/orders', ...);
```

## 文档必含

- [ ] 每个端点 summary + description
- [ ] 所有请求参数（path / query / header / body）
- [ ] 所有响应状态码 + schema
- [ ] 错误响应示例
- [ ] 鉴权方式（Bearer / API Key）
- [ ] 示例值（避免空 schema）

## CI 卡门禁

```yaml
- name: OpenAPI 校验
  run: |
    # 拉取生成的 openapi.json
    curl http://localhost:8080/v3/api-docs > openapi.json
    
    # 用 swagger-cli 校验
    npx swagger-cli validate openapi.json
    
    # 用 openapi-diff 对比 master 分支
    npx openapi-diff baseline.json openapi.json --fail-on-changes
```

## 反模式

- ❌ 手写 Markdown 文档（容易过时）
- ❌ 文档与代码不同步（生成式优于手写）
- ❌ 文档不带示例（前端难对接）
- ❌ 不暴露 `/swagger-ui`（开发环境必须有）
- ❌ 错误响应没文档（前端不知道怎么处理）
