# 原则：Feature Flag（灰度发布）

> 新功能默认关闭，灰度打开，不全量上线。

## 4 种类型

| 类型 | 用法 |
|---|---|
| **Release Flag** | 新功能上线，开到 100% 后清理代码 |
| **Experiment Flag** | A/B 测试，长期保留 |
| **Ops Flag** | kill switch，长期保留 |
| **Permission Flag** | 按用户 / 租户灰度 |

## 灰度策略

```
1. 内部测试（白名单）
2. 小流量（1%）
3. 中流量（10%）
4. 大流量（50%）
5. 全量（100%）
6. 清理（删 flag 代码，1+ 月稳定后）
```

## 实现

```python
# feature_flags 服务（读配置中心）
if feature_flags.is_enabled("new_checkout", user=user):
    show_new_checkout()
```

## 反模式

```python
# 反：硬编码分支
if datetime.now() > launch_date:
    show_new_ui()  # 出错回滚 = 重新发布

# 正：feature flag（配置中心 1 秒切换）
if feature_flags.is_enabled("new_ui"):
    show_new_ui()
```
