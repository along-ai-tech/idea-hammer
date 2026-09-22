# 原则：Feature Flag（灰度发布）

> 新功能默认关闭，灰度打开，不全量上线。

## 为什么需要 Feature Flag

- 降低风险：新功能有问题，秒级关闭（不用回滚代码）
- 灰度验证：1% / 10% / 50% / 100% 分批打开
- A/B 测试：50% 用户开 A，50% 开 B，对比效果
- 暗发布：发布代码但不开启，跑 N 天观察指标
- Kill switch：紧急情况远程关闭

## 4 种 Flag 类型

### 1. Release Flag（最常用）

新功能上线用。开到 100% 后清理代码。

### 2. Experiment Flag（A/B 测试）

对比两种实现，长期保留（数据驱动决策）。

### 3. Ops Flag（kill switch）

紧急关闭某个功能 / 服务。长期保留。

### 4. Permission Flag（按用户 / 租户）

白名单 / 黑名单 / 灰度特定用户群。

## 实现

### 配置中心

```python
# 反例：硬编码
if user.id == 123:
    show_new_checkout()


# 正例：feature flag 服务
if feature_flags.is_enabled("new_checkout", user=user):
    show_new_checkout()


# feature_flags 内部
def is_enabled(flag_name, user=None, default=False):
    # 读配置中心（LaunchDarkly / Unleash / 自建）
    return config.get_flag(flag_name, user=user, default=default)
```

### 简单实现（无需配置中心）

```python
# 文件 / 数据库 / 环境变量
FEATURE_FLAGS = {
    "new_checkout": os.getenv("FF_NEW_CHECKOUT", "false") == "true",
    "v2_recommend": os.getenv("FF_V2_RECOMMEND", "false") == "true",
}

def is_enabled(name):
    return FEATURE_FLAGS.get(name, False)
```

## 灰度策略

```
# 阶段 1: 内部测试（5% 内部用户 + 白名单）
# 阶段 2: 小流量（1% 真用户）
# 阶段 3: 中流量（10%）
# 阶段 4: 大流量（50%）
# 阶段 5: 全量（100%）
# 阶段 6: 清理代码（删 flag 代码 + 保留老分支）
```

## Flag 生命周期

```
1. 创建 flag（默认 false）
2. 代码用 flag 包裹新功能（false = 老路径）
3. 内部测试（true 给白名单）
4. 灰度发布（1% → 100%）
5. 稳定期（flag 100% true，但保留 flag 代码）
6. 清理（删 flag 代码，删除老路径）

# 注意：不要急着清理。稳定 1+ 月再清。
```

## 清理

Flag 100% 长期运行的成本：

- 代码复杂度（永远要判断 flag）
- 测试复杂度（两种路径都要测）
- 心智负担（看代码不知道走哪个分支）

清理时机：稳定期 1+ 月 + 业务方同意。

## 检测

- code-review: 新功能必须包在 flag 里
- CI: 检查长期未清理的 flag（> 6 个月）

## 反模式

```python
# 反模式 1：硬编码分支
if datetime.now() > launch_date:
    show_new_ui()  # 发布日自动开，出错回滚 = 重新发布


# 正确：feature flag
if feature_flags.is_enabled("new_ui"):
    show_new_ui()  # 配置中心 1 秒切换


# 反模式 2：flag 命名不清晰
if feature_flags.is_enabled("v2"):  # v2 是啥？
    ...


# 正确：flag 命名说清楚
if feature_flags.is_enabled("use_new_checkout_flow"):
    ...
```
