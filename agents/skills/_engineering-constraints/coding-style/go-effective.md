# Go 编码规范 — Effective Go + Go Code Review Comments

> 引用 [Effective Go](https://go.dev/doc/effective_go) + [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)。

## 强制条款

### 命名

- 导出 `PascalCase`；非导出 `camelCase`
- 包名小写、简短、单词（`time`、`http`、`bufio`），不要 `time_util`
- 不要用下划线（除测试 / 生成代码）
- 接口名 `-er` 后缀（`Reader`、`Writer`）
- 常量不用 `k` 前缀（`const MaxRetries = 3`）

### 错误处理

- 错误是值，显式返回（不要 panic）
- `if err != nil { return err }`
- 错误 wrap：`fmt.Errorf("read config: %w", err)`（Go 1.13+）
- `errors.Is` / `errors.As` 判断链
- 不要 `log.Fatal`（库函数）
- 自定义错误实现 `Error()` 方法

### 接口设计

- 接受接口，返回结构体
- 小接口（1-3 方法）
- 接口定义在使用方，不是实现方
- 空接口 `interface{}` 慎用（Go 1.18+ 用 `any`）

### 并发

- `goroutine` 生命周期必须明确（谁创建谁负责退出）
- Channel 大小通常 1 或 unbuffered
- 不要共享内存通信（用 channel）
- `sync.Mutex` / `sync.RWMutex` 保护临界区
- `context.Context` 传递取消信号 / 超时

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()
result, err := fetchData(ctx)
```

### 切片 / Map

- `make([]T, len, cap)` 预分配容量
- Map 是无序的，需要顺序用 slice 保存 key
- 遍历用 `for k, v := range m`
- 删除：`delete(m, k)`

### 接口 vs 具体类型

- 参数用接口（小接口），返回具体类型
- 不要因为"灵活"加不必要的接口

## 格式化

- `gofmt` / `goimports` 强制
- 不要自己调格式
- tab 缩进（gofmt 默认）

## 测试

- `_test.go` 同包
- `func TestXxx(t *testing.T)` 命名
- 覆盖率 `go test -cover`
- 基准测试 `func BenchmarkXxx(b *testing.B)`
- 表驱动测试

## 反模式（绝对禁止）

- ❌ `init()` 做业务逻辑（仅注册 / 单例）
- ❌ 忽略 error：`_ = foo()`
- ❌ `panic` 做正常错误处理
- ❌ 全局可变状态（除单例 / config）
- ❌ 长函数（> 50 行）
- ❌ 没有 context.Context 的网络调用
- ❌ `time.Sleep` 在生产代码
- ❌ `os.Exit` 在库函数

## 工具链

- `go vet` / `staticcheck`
- `golangci-lint`（全 lint 一体化）
- `gofumpt`（更严格的 gofmt）
- Go modules（`go.mod` 锁定版本）
