# REST 资源命名

## URL 设计

```
GET    /users              # 列表
GET    /users/{id}         # 详情
POST   /users              # 创建
PUT    /users/{id}         # 全量更新
PATCH  /users/{id}         # 部分更新
DELETE /users/{id}         # 删除

GET    /users/{id}/orders  # 子资源列表（嵌套）
POST   /users/{id}/orders  # 在父资源下创建子资源
```

## 强制规则

### 1. 复数名词

```
✅ /users /orders /products
❌ /user /getUser /user_list
```

### 2. kebab-case

```
✅ /user-profiles /order-items
❌ /userProfiles /order_items
```

### 3. 不用动词

```
❌ /getUsers /createOrder /deleteUser
✅ 用 HTTP 动词（GET/POST/DELETE）表达动作
```

### 4. 嵌套 ≤ 2 层

```
✅ /users/{id}/orders
❌ /users/{id}/orders/{oid}/items/{iid}/comments/{cid}
   → /comments/{cid}?orderItemId={iid}（扁平化）
```

### 5. 版本号

```
✅ /api/v1/users        # URL 版本（简单）
✅ Accept: version=1    # Header 版本（复杂但灵活）
推荐：URL 版本（简单直观）
```

### 6. 过滤 / 排序 / 分页用 query string

```
GET /users?status=active&sort=created_at:desc&page=1&size=20
GET /users?cursor=eyJpZCI6MTIzfQ==
```

## HTTP 动词语义

| 动词 | 幂等 | 语义 |
|---|---|---|
| GET | ✅ | 读 |
| POST | ❌ | 创建 |
| PUT | ✅ | 全量替换 |
| PATCH | ❌ | 部分修改（实现可幂等） |
| DELETE | ✅ | 删除 |

## 设计示例

```yaml
# 用户管理
GET    /users                 # 列表（分页）
GET    /users/{id}            # 详情
POST   /users                 # 创建
PUT    /users/{id}            # 全量更新
PATCH  /users/{id}            # 部分更新（昵称 / 头像）
DELETE /users/{id}            # 删除（软删除）

# 订单
GET    /users/{id}/orders     # 某用户的订单
POST   /orders                # 创建订单（带 Idempotency-Key）
GET    /orders/{id}           # 订单详情
POST   /orders/{id}/pay       # 支付（动作）
POST   /orders/{id}/cancel    # 取消（动作）

# 文件
POST   /files                 # 上传（multipart/form-data）
GET    /files/{id}            # 下载
DELETE /files/{id}            # 删除

# 动作类（POST + 名词）
POST   /auth/login
POST   /auth/logout
POST   /auth/refresh
POST   /users/{id}/reset-password
```

## 反模式

- ❌ 用 GET 改数据（GET 应该幂等）
- ❌ URL 里带动词（`/getUser`）
- ❌ 命名用驼峰（`/userProfiles`）
- ❌ 嵌套超过 2 层
- ❌ 单复数混用（`/user` 和 `/users` 共存）
- ❌ 业务状态用 query（`/users?status=deleted` 是 OK 的，但过滤字段过多考虑 query DSL）
