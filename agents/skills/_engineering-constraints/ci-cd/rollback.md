# 回滚策略

## 三种发布模式

### 1. Blue / Green（蓝绿）

```yaml
# 蓝 = 当前版本（流量 100%）
# 绿 = 新版本（流量 0%）

# 切换（瞬间原子）
kubectl patch service my-app -p '{"spec":{"selector":{"version":"green"}}}'
```

**优势**：
- 0 downtime
- 回滚 = 切回蓝（秒级）
- 验证后才切流量

**劣势**：
- 2 倍资源
- DB migration 兼容

### 2. Canary（金丝雀）

```yaml
# 阶段 1：新版本 5% 流量
# 阶段 2：观察 30 分钟
# 阶段 3：新版本 25%
# 阶段 4：观察 30 分钟
# 阶段 5：新版本 100%

# Istio 路由
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
spec:
  hosts:
  - my-app
  http:
  - route:
    - destination:
        host: my-app-v1  # 老版本
      weight: 95
    - destination:
        host: my-app-v2  # 新版本
      weight: 5
```

**优势**：
- 渐进暴露风险
- 错误率上升立即回滚

**劣势**：
- 慢（需要观察期）
- DB schema 必须兼容

### 3. Feature Flag

```java
if (featureFlag.isEnabled("new-checkout", userId)) {
    return newCheckoutFlow();
} else {
    return oldCheckoutFlow();
}
```

**优势**：
- 不部署就能开关
- 用户维度控制
- 即时回滚（改配置）

**工具**：LaunchDarkly / Unleash / 自建

## 回滚检查清单

发布前必须准备：

- [ ] 老版本镜像保留（不删）
- [ ] DB migration 向下兼容
- [ ] 监控告警就绪
- [ ] 回滚命令准备好（文档化）
- [ ] 回滚演练（每季度一次）

## 回滚触发条件

- 错误率 > 5%（持续 5 分钟）
- P99 延迟 > 3 倍基线
- 关键业务功能故障
- 监控告警（如 CPU / 内存异常）

## 回滚流程

```bash
# 1. 确认问题（不是抖动）
kubectl logs my-app-v2 --tail=100

# 2. 切回老版本
kubectl rollout undo deployment/my-app
# 或
kubectl set image deployment/my-app my-app=my-app:v1.2.3

# 3. 验证回滚
curl https://api.example.com/health

# 4. 通知团队
slack-notify "回滚完成：my-app v1.2.3 → v1.2.2"

# 5. 后续：复盘 + 修复 + 重新发布
```

## DB Migration 回滚

如果 migration 已执行：

```sql
-- Flyway: flyway undo
-- 或手写 down migration
ALTER TABLE users DROP COLUMN phone;
```

**强制规则**：
- migration 必须有 down
- 大变更不立即 down（数据丢失风险）→ 写修复 migration

## 反模式

- ❌ 没有回滚计划
- ❌ 发布完就删老版本镜像
- ❌ DB migration 不向前兼容（发布期间崩）
- ❌ 监控告警没就绪就发布
- ❌ 回滚不通知团队
- ❌ 回滚后不复盘
