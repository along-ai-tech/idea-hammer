# Codex Hook 协议

> 本文描述的是 **Codex 真实加载的 hook 协议**，逐条核对自 `openai/codex` `rust-v0.171.0` 源码。
> 对应的机器可校验版本：[`schemas/hook-protocol.schema.json`](../schemas/hook-protocol.schema.json)。

## 为什么重写

框架早期自造过一套 "Hook 协议 v2"：顶层 `$version` / `$comment` / `events`，handler 带 `mode: advisory|transform|retry`，输出 `{"retry":...}` / `{"transform":...}`。

**Codex 从来没加载过这套格式。** 它解析时直接报 `unknown field '$version', expected 'description' or 'hooks'`，然后丢弃整个文件——所有 hook 静默失效，不报错、不提示。

那套格式已废弃。本文和 `schemas/hook-protocol.schema.json` 是唯一事实源。

---

## 1. 配置文件位置与优先级

| 层级 | 路径 | 说明 |
|---|---|---|
| 全局 | `~/.codex/hooks.json` | 即 `$CODEX_HOME/hooks.json`，对所有项目生效 |
| 项目 | `<项目根>/.codex/hooks.json` | 随项目走，提交进仓库后团队共享 |

Codex 也支持 TOML 形式（写在 `.codex/config.toml` 的 `[hooks]` 表里），但**本框架只用 JSON**。

优先级与叠加规则（来自 Codex 配置层栈行为）：

1. Codex 按配置层栈**从低到高**扫描。每一层只要有自己的 `.codex` 目录，就在该目录里找 `hooks.json`。项目根与 cwd 之间的嵌套 `.codex` 目录各算独立一层。
2. 同一事件在多层都定义 → **handler 叠加，不是覆盖**。层优先级越高的越晚执行（display_order 更大）。
3. 某一层的 `hooks.json` **解析失败 → 该层 hook 全部丢弃**，其他层不受影响。启动时打 warning：`failed to parse hooks config <path>: <err>`。
4. 同一层里同时写了 `config.toml` 的 `[hooks]` 和 `hooks.json` → 两个都会加载，并给 warning：`loading hooks from both ...; prefer a single representation for this layer`。
5. 链接的 git worktree 场景下，hook 发现可能指向主 checkout 的 `.codex` 目录。

实践建议：全局层只放"跟项目无关"的能力（如进化信号扫描），项目层放"跟代码库绑定"的门禁（如 review 门禁）。这样同一事件在两层都有定义时，行为是可预期的。

---

## 2. 信任机制：hook 装了不一定跑

**这是最容易踩的坑。** 用户级（`~/.codex/hooks.json`）和项目级（`<项目>/.codex/hooks.json`）的 hook，Codex 一律先判为**未信任（Untrusted）**——不写入信任状态，就一条都不会执行。没有报错、没有提示，hook 就是静默不跑。

Codex 桌面端启动时会弹"hook 审阅"框，批准后把信任状态写进 `~/.codex/config.toml`。命令行没有这个框，得自己写。

### 2.1 信任状态写在 config.toml 的哪里

```toml
[hooks.state."<hooks.json 绝对路径>:<事件 snake_case>:<组序号>:<handler 序号>"]
trusted_hash = "sha256:..."
```

例：

```toml
[hooks.state."/Users/me/.codex/hooks.json:session_start:0:0"]
trusted_hash = "sha256:4217e1d1d58a040d01875ecdf8f5ddf03efce3a46702a9544a5981eb0e19a28b"
```

注意：

- 路径是**绝对路径**，写错匹配不上。
- `hooks.state` 只从**用户层**（`~/.codex/config.toml`）和会话 flag 层读，项目层不能给自己写信任状态。所有 hook（包括项目级的）的信任都落在 `~/.codex/config.toml` 这一处。
- 声明一变（改 command、改 timeout、改 statusMessage）hash 就变，旧信任立刻失效，hook 重新变成不执行。改完 `hooks.json` 要重新登记。
- managed / builtin 来源的 hook 不需要登记：`hooks.managed_dir` 指向的目录和内置 hook 直接是 `Managed` / `Trusted`。

### 2.2 trusted_hash 怎么算

算法在 `codex-rs/hooks/src/engine/discovery.rs` 的 `hook_hash`：

1. handler 规范化：`timeout` 缺省补 600（`SessionEnd` / `Interrupt` 缺省 1、上限 3）；`commandWindows` 置空；`additionalContextLimit` 只在能发上下文的事件（`PreToolUse` / `PostToolUse` / `SessionStart` / `UserPromptSubmit` / `SubagentStart`）保留，且等于默认值 2500 时也置空
2. 组装身份对象：`{"event_name": <事件 snake_case>, "matcher": <没有就省略>, "hooks": [<规范化后的 handler>]}`
3. 递归排序所有对象键，序列化成**紧凑 JSON**（非 ASCII 不转义）
4. `sha256` 取十六进制，拼成 `sha256:<hex>`

等价的 Python 实现（框架安装器 `scripts/install_global.py` 用的就是它）：

```python
import hashlib, json

def hook_hash(event, matcher, handler):
    timeout = handler.get("timeout") or 600
    normalized = {
        "type": "command",
        "command": handler["command"],
        "timeout": timeout,
        "async": bool(handler.get("async", False)),
    }
    if handler.get("statusMessage"):
        normalized["statusMessage"] = handler["statusMessage"]
    identity = {"event_name": EVENT_LABEL[event], "hooks": [normalized]}
    if matcher:
        identity["matcher"] = matcher
    blob = json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()
```

### 2.3 怎么查当前状态

`hooks/list` RPC（app-server）能列出所有 hook 的 `key`、`currentHash`、`trustStatus`、`enabled`：

```bash
codex app-server
# 发 {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"x","title":"x","version":"1"}}}
# 再发 {"jsonrpc":"2.0","method":"initialized","params":{}}
# 再发 {"jsonrpc":"2.0","id":2,"method":"hooks/list","params":{"cwds":["/你的/项目"]}}
```

`trustStatus` 为 `trusted` 才会执行；`untrusted` 就是没登记。

本框架的安装器 `python3 scripts/install_global.py install` 会自动完成登记（写 `~/.codex/config.toml`），不用手动操作。改了 `hooks.json` 后重跑一次即可续期。

---

## 3. 配置结构

### 3.1 顶层

```json
{
  "description": "可选说明文字",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "./scripts/check.sh" } ]
      }
    ]
  }
}
```

顶层是 `deny_unknown_fields` 的：**只允许 `description` 和 `hooks` 两个字段**。多写任何一个（`$version`、`$comment`、`events`、`mode`……）→ 整个文件解析失败 → 该文件里所有 hook 全部失效。

### 3.2 事件名（14 个）

`hooks` 下的键必须是下面 14 个事件名之一。**不在这列表里的键会被 Codex 静默忽略**（本仓库的 schema 会直接判错，用来抓拼写错误）。

| 事件名 | 触发时机 | 额外 stdin 字段 | matcher 生效 |
|---|---|---|---|
| `PreModelRequest` | 发给模型之前 | — | ❌ |
| `PostModelRequest` | 模型响应之后 | — | ❌ |
| `PreToolUse` | 工具调用之前 | `tool_name` `tool_input` `tool_use_id` | ✅ |
| `PermissionRequest` | 请求提权之前 | `tool_name` `tool_input` | ✅ |
| `PostToolUse` | 工具调用之后 | 同上 + `tool_response` | ✅ |
| `PreCompact` | 压缩上下文之前 | `trigger` | ✅ |
| `PostCompact` | 压缩上下文之后 | `trigger` | ✅ |
| `SessionStart` | 会话启动 | `source` | ✅（匹配 `source`，不是工具名） |
| `SessionEnd` | 会话结束 | `reason` | ✅（匹配 `reason`） |
| `UserPromptSubmit` | 用户提交 prompt | `prompt` | ❌ |
| `SubagentStart` | 子 Agent 启动 | `agent_id` `agent_type` | ✅（匹配 `agent_type`） |
| `SubagentStop` | 子 Agent 结束 | `agent_id` `agent_type` `agent_transcript_path` `stop_hook_active` `last_assistant_message` | ✅（匹配 `agent_type`） |
| `Stop` | 主 Agent 停下 | `stop_hook_active` `last_assistant_message` | ❌ |
| `Interrupt` | 用户打断 | — | ❌ |

### 3.3 MatcherGroup

```json
{
  "matcher": "可选字符串",
  "hooks": [ { "type": "command", "command": "./scripts/check.sh" } ]
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `matcher` | ❌ | 匹配表达式，语义见 [§6](#6-matcher-匹配规则)。在 `UserPromptSubmit` / `Stop` / `Interrupt` / `PreModelRequest` / `PostModelRequest` 会被忽略 |
| `hooks` | ✅ | 该分组下的 handler 数组，按数组顺序执行 |

### 3.4 command handler

Codex 的 handler 是 `type` 标签的枚举，一共 4 种：`command` / `mcp_tool` / `prompt` / `agent`。
**后三种在 rust-v0.171.0 的运行时全部被跳过**（`prompt hooks are not supported yet` 等），本框架只用 `command`。

```json
{
  "type": "command",
  "command": "必填，交给 shell 执行（$SHELL -lc \"<command>\"）",
  "commandWindows": "可选",
  "timeout": 5,
  "async": false,
  "statusMessage": "可选",
  "additionalContextLimit": 2500
}
```

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `type` | string | ✅ | — | 固定 `"command"` |
| `command` | string | ✅ | — | 交给 shell 执行的命令，Codex 用 `$SHELL -lc "<command>"` 启动（`$SHELL` 缺省 `/bin/sh`） |
| `commandWindows` | string | ❌ | — | Windows 专用命令；不填则 `command` 全平台生效 |
| `timeout` | integer | ❌ | `600` | **超时秒数**（不是毫秒）。`SessionEnd` / `Interrupt` 默认 `1`、上限 `3` |
| `async` | boolean | ❌ | `false` | `true` = 异步执行。异步 hook **没有控制效果**：不能拦截、不能改写输入、不能终止本轮，但仍可注入 `additionalContext` |
| `statusMessage` | string | ❌ | — | 运行期间展示的状态提示 |
| `additionalContextLimit` | integer | ❌ | `2500` | 该 hook 注入上下文溢写到磁盘的近似 token 阈值；`0` 表示关闭溢写 |

> **没有** `onFailure` 字段，**没有** `mode` 字段，也**没有** `max_retries` 字段。这三个都是旧自造协议的产物。

### 3.5 完整示例

```json
{
  "description": "IdeaHammer 项目级 hook",
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$(git rev-parse --show-toplevel)/.codex/hooks/detect-feedback-signal.sh\"",
            "timeout": 5,
            "statusMessage": "IdeaHammer 进化信号扫描"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$(git rev-parse --show-toplevel)/.codex/hooks/pre-tool-shell.sh\"",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$(git rev-parse --show-toplevel)/.codex/hooks/stop-gate.sh\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

---

## 4. stdin 输入

hook 进程从 stdin 读一段 JSON。字段名是 **snake_case**。

### 4.1 通用字段

几乎所有事件都有：

| 字段 | 说明 |
|---|---|
| `session_id` | 会话 ID |
| `turn_id` | 当前轮次 ID（`SessionStart` / `SessionEnd` 没有） |
| `transcript_path` | 会话记录文件路径，可能为 `null` |
| `cwd` | 工作目录 |
| `hook_event_name` | 事件名，与配置里的键一致 |
| `model` | 当前模型 |
| `permission_mode` | 当前提权模式（`PreCompact` / `PostCompact` / `SessionEnd` 没有） |

### 4.2 各事件的额外字段

见 [§3.2](#32-事件名14-个) 的表格。几个用得上的：

- `UserPromptSubmit` → `prompt`（用户原始输入）
- `Stop` → `stop_hook_active`（bool）、`last_assistant_message`（可为 `null`）
- `PreToolUse` / `PostToolUse` → `tool_name`、`tool_input`、`tool_use_id`；`PostToolUse` 另有 `tool_response`

### 4.3 `tool_input` 的形状与坑

**shell 工具**（`tool_name` = `Bash`）：

```json
{ "command": "git commit -m 'wip'" }
```

**`apply_patch`**（`tool_name` = `apply_patch`）：它是 **freeform 工具**，模型直接吐补丁原文，Codex 把它塞进 `command` 字段：

```json
{ "command": "*** Begin Patch\n*** Add File: src/a.py\n+print(1)\n*** End Patch" }
```

⚠️ **最大的坑**：freeform 工具**没有** `file_path` 字段。想拿被改动的文件路径，只能从补丁原文里抽 `*** Add File:` / `*** Update File:` / `*** Delete File:` / `*** Move to:` 这几行。

```bash
# 抽 apply_patch 改动的文件路径
echo "$INPUT" | jq -r '
  [ (.tool_input.file_path // empty) ]
  + [ ((.tool_input.command // "")
       | [ split("\n")[]
         | (try capture("^\\*\\*\\* (Add|Update|Delete) File: (?<p>.+)$") catch empty) | .p ] ) ]
  | .[] | select(type == "string" and length > 0)
'
```

（`.tool_input.file_path` 那条是为普通函数型编辑工具留的兜底，Codex 的 `apply_patch` 走不到。）

---

## 5. stdout 输出

### 5.1 通用字段

**stdout 必须是合法 JSON 对象**。所有输出类型都接受这几个通用字段（camelCase）：

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `continue` | bool | `true` | `false` = 停止当前流程（可用的事件受限，见下） |
| `stopReason` | string | — | 停止理由 |
| `suppressOutput` | bool | `false` | 抑制 hook 输出展示 |
| `systemMessage` | string | — | 以警告形式展示给用户 |

输出对象同样带 `deny_unknown_fields`：**多写一个字段 → 整份输出判为无效**。

### 5.2 各事件的输出形状

**`SessionStart`** — 注入上下文：

```json
{ "hookSpecificOutput": { "hookEventName": "SessionStart", "additionalContext": "要注入的上下文" } }
```

**`UserPromptSubmit`** — 注入上下文，或整条拦下：

```json
{ "hookSpecificOutput": { "hookEventName": "UserPromptSubmit", "additionalContext": "..." } }
```

```json
{ "decision": "block", "reason": "拦截理由" }
```

**`PreToolUse`** — 两种写法，**不要混用**：

```json
{ "decision": "block", "reason": "为什么拦" }
```

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "为什么拦"
  }
}
```

`hookSpecificOutput` 里可用的字段：`hookEventName`、`permissionDecision`（`allow` / `deny` / `ask`）、`permissionDecisionReason`、`updatedInput`、`additionalContext`。

⚠️ 一旦 `hookSpecificOutput` 里出现了 `permissionDecision` / `permissionDecisionReason` / `updatedInput` 任意一个，顶层的 `decision` / `reason` 就**被完全忽略**。

`PreToolUse` 的完整判定矩阵：

| 输出 | 结果 |
|---|---|
| `{"decision":"block","reason":"非空"}` | ✅ 拦截 |
| `{"decision":"block"}`（reason 为空或缺失） | ❌ 无效输出 |
| `{"decision":"approve"}` | ❌ 无效输出（unsupported decision:approve） |
| `hookSpecificOutput.permissionDecision = "deny"` + `permissionDecisionReason` | ✅ 拦截 |
| `hookSpecificOutput.permissionDecision = "allow"` + `updatedInput` | ✅ 放行并改写工具入参 |
| `hookSpecificOutput.permissionDecision = "allow"`（不带 `updatedInput`） | ❌ 无效输出 |
| `hookSpecificOutput.permissionDecision = "ask"` | ❌ 无效输出 |
| `updatedInput` 不配 `permissionDecision:"allow"` | ❌ 无效输出 |

**`PostToolUse`**：

```json
{ "decision": "block", "reason": "..." }
```

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "回灌给模型的上下文",
    "updatedMCPToolOutput": { }
  }
}
```

**`Stop`** — 只能拦，没有 `hookSpecificOutput`：

```json
{ "decision": "block", "reason": "..." }
```

### 5.3 退出码语义

| 退出码 | 语义 |
|---|---|
| `0` | 正常。按 stdout 的 JSON 处理；stdout 为空 = 无输出 |
| `2` | **拦截**。拦截理由取 **stderr**（stdout 被忽略）。stderr 为空 → 判为失败，不是拦截 |
| 其他非 0 | 判为失败（`hook exited with code N`），不拦截 |
| 无退出码 | 判为失败（`hook exited without a status code`） |

`PreToolUse` 的额外限制：输出里写 `continue:false`、`stopReason` 或 `suppressOutput` 都会被判为**不支持**（unsupported continue:false / stopReason / suppressOutput）。

`Stop` 反过来是支持 `continue:false` + `stopReason` 的：`{"decision":"block","reason":"..."}` 是"打回并把理由喂回给模型继续干"，`{"continue":false,"stopReason":"..."}` 是"这一轮到此为止"。

### 5.4 stdout 是纯文本时会怎样（很容易踩）

| 情况 | 结果 |
|---|---|
| 以 `{` 或 `[` 开头、但结构不合法 | 一律判为**无效输出** → hook 失败 |
| 纯文本，且事件是 `UserPromptSubmit` | **当成 `additionalContext` 注入模型上下文**（不是错误） |
| 纯文本，且事件是 `Stop` / `SubagentStop` | 判为**无效输出** → hook 失败 |
| 纯文本，且事件是 `PreToolUse` / `PostToolUse` / `SessionStart` / `SubagentStart` | 静默忽略，无输出、无报错 |

结论：**别用纯文本当输出通道**。要提示就写合法 JSON，要诊断信息就写 stderr。

---

## 6. matcher 匹配规则

### 6.1 匹配算法

matcher 匹配的是 hook payload 里的 `tool_name`（`SessionStart` / `SessionEnd` / `SubagentStart` / `SubagentStop` 匹配的是各自对应的字符串，见 §3.2）。

| matcher 写法 | 语义 |
|---|---|
| `""`（空串）或 `"*"` | 匹配全部 |
| 只含字母数字 / 下划线 / 竖线（如 `"Bash"`、`"Edit|Write"`） | **精确匹配**，竖线是「或」 |
| 含正则字符（如 `"^Bash$"`、`".*patch.*"`） | 当**正则**跑（`regex` crate） |

匹配失败 → 该 handler 不执行（不是错误）。matcher 本身编译失败（正则非法）→ 记一条 `invalid matcher ... in ...` 警告，该 handler 不执行。

### 6.2 哪些事件忽略 matcher

| matcher 生效 ✅ | matcher 被忽略 ❌ |
|---|---|
| `PreToolUse` `PermissionRequest` `PostToolUse` `SessionStart` `SessionEnd` `SubagentStart` `SubagentStop` `PreCompact` `PostCompact` | `UserPromptSubmit` `Stop` `Interrupt` `PreModelRequest` `PostModelRequest` |

### 6.3 工具规范名与别名

| 工具 | stdin 里的 `tool_name` | matcher 额外接受的别名 |
|---|---|---|
| shell 工具 | `Bash` | 无 |
| `apply_patch` | `apply_patch` | `Write`、`Edit` |
| `spawn_agent` | `spawn_agent` | `Agent` |

别名只用于 **matcher 选 handler**；stdin 里看到的永远是规范名。别名是为了兼容 Claude Code 风格的配置而存在的。

⚠️ `exec_command` / `shell` / `local_shell` 这些名字 **Codex 里不存在**，写在 matcher 里匹配不到任何东西。

---

## 7. 常见错误清单

| 写法 | 后果 |
|---|---|
| hook 写好了但没登记信任（`config.toml` 里没有对应的 `[hooks.state."..."]`） | **静默不执行**。用户级/项目级 hook 默认 `Untrusted`，不报错、不提示，Codex 只是不跑它。见 §2 |
| 顶层写 `$version` / `$comment` / `events` | **整个文件解析失败** → 该文件里所有 hook 全部失效（warning: `failed to parse hooks config ...`） |
| 顶层写成 `{"events": {...}}` | 同上，整个文件失效 |
| handler 里写 `mode` / `max_retries` / `onFailure` | 这些字段不存在。Codex 会忽略 handler 层的未知字段（本仓库 schema 会判错）；`mode` 的三模式语义完全不存在 |
| stdout 输出纯文本 | 行为随事件而变，见 §5.4 |
| `{"decision":"approve"}` | 判为**无效输出**。`Stop` / `UserPromptSubmit` / `PostToolUse` 的 `decision` 枚举里根本没有 `approve`；`PreToolUse` 虽然有，但运行时判为 unsupported。`approve` 只在 `hookSpecificOutput.permissionDecision` 里、且必须同时带 `updatedInput` 才成立 |
| `{"decision":"block"}` 不带 `reason` | 判为**无效输出**（decision:block without a non-empty reason） |
| `Stop` 输出里写 `hookSpecificOutput` | `Stop` 的输出结构没这个字段 → 判为**无效输出** |
| `{"permissionDecision":"ask"}` | 判为**无效输出**（unsupported permissionDecision:ask） |
| `{"permissionDecision":"allow"}` 不带 `updatedInput` | 判为**无效输出**（unsupported permissionDecision:allow） |
| `updatedInput` 不配 `permissionDecision:"allow"` | 判为**无效输出** |
| `async: true` 想拦一刀 | 异步 hook 没有控制效果，拦截**不生效**（退出码 2 也会变成"失败"） |
| `timeout: 5000` 想写 5 秒 | `timeout` 单位是**秒**，5000 = 83 分钟 |
| matcher 写 `exec_command` / `shell` | 匹配不到，handler 永远不执行。shell 工具的规范名是 `Bash` |
| 在 `UserPromptSubmit` / `Stop` 里写 matcher | 被忽略，这个字段不起作用 |
| `command` 里期望自己拿到 stdin JSON | stdin 是 hook 进程独占的；`command` 走 shell，`$(...)` 由 shell 展开 |
| 退出码和输出方式搞混 | 两种拦截写法二选一：**退出码 `0` + stdout 写 `{"decision":"block","reason":"..."}`**，或**退出码 `2` + stderr 写理由**（此时 stdout 被忽略）。退出码 `2` 但 stderr 为空 = 判失败，不是拦截 |

---

## 8. 本框架实际用到的 hook

现状以仓库根目录的 `.codex/hooks.json` 为准，脚本在 `.codex/hooks/`。

| 事件（matcher） | 脚本 | 用途 | stdout |
|---|---|---|---|
| `UserPromptSubmit` | `detect-feedback-signal.sh` | 关键词命中修正信号 → 写 `.codex/evolution/signals.jsonl` | 无（留空即无输出，不打扰用户） |
| `SessionStart` | `check-evolution.sh` | 有待审建议 / 新信号时，注入一条"该逐条拍板"的提示 | `hookSpecificOutput.additionalContext` |
| `PreToolUse`（`Bash\|exec_command`） | `pre-tool-shell.sh` | `git commit` 前跑 `tsc --noEmit`，不过则拦截；dev 启动前清占用端口 | 拦截时 `{"decision":"block","reason":...}` |
| `PostToolUse`（`Bash\|exec_command`） | `auto-push.sh` | 命令含 `git commit` → 自动 push（保护分支跳过） | 无 |
| `PostToolUse`（`apply_patch\|Write\|Edit`） | `mark-review-needed.sh` | 从补丁原文抽文件路径 → 写 `.codex/.needs-review` 标记 | 无 |
| `Stop` | `stop-gate.sh` | 标记存在且不是 `clean` → 拦停，逼走 code review | `{"decision":"block","reason":...}` |

> matcher 写成 `Bash|exec_command` 这种形式是安全的：竖线分隔的纯字面量走**精确匹配**，`Bash` 命中 Codex 的规范名，`exec_command` 命中不了也不报错。`apply_patch|Write|Edit` 里 `apply_patch` 是规范名，`Write` / `Edit` 是 Codex 官方承认的别名。

**全局层 vs 项目层**：全局只装 `UserPromptSubmit` + `SessionStart` 两条（跟项目无关的进化信号捕获）；`PreToolUse` / `PostToolUse` / `Stop` 三条门禁会改变项目行为，只在单个项目里 opt-in（`python3 scripts/install_global.py project <目录>`）。两层的信任登记都写进 `~/.codex/config.toml`，由安装器自动完成，见 §2。

**未挂载的示例脚本**（需要时自行 opt-in）：

- `auto-lint.sh`（`PostToolUse`）— 编辑后跑 ruff / eslint，失败用 `additionalContext` 回灌给模型。会改用户文件，所以默认不挂。
- `sanitize-prompt.sh`（`UserPromptSubmit`）— 检出明文密钥就拦下这次提交。注意 Codex 没有 "transform"（改写输入）模式，prompt 只能原样送出或整条拦下。

---

## 9. 校验

`schemas/hook-protocol.schema.json` 是 draft-07 JSON Schema，覆盖顶层结构、14 个事件名、MatcherGroup 和 command handler。

```bash
# 1. schema 自身是不是合法 JSON
python3 -m json.tool schemas/hook-protocol.schema.json > /dev/null

# 2. 用 jsonschema 校验 hooks.json
python3 - <<'PY'
import json, os
from jsonschema import Draft7Validator

schema = json.load(open("schemas/hook-protocol.schema.json"))
Draft7Validator.check_schema(schema)

targets = ["~/.codex/hooks.json", ".codex/hooks.json"]
for raw in targets:
    path = os.path.expanduser(raw)
    if not os.path.isfile(path):
        print(f"{path}: SKIP (不存在)")
        continue
    inst = json.load(open(path))
    errs = sorted(Draft7Validator(schema).iter_errors(inst), key=lambda e: list(e.path))
    print(f"{path}: {'OK' if not errs else 'FAIL'}")
    for e in errs:
        print("   ", list(e.path), e.message)
PY
```

比 Codex 本身更严的三处（都是故意的，为了抓错）：

1. `hooks` 下出现 14 个事件名以外的键 → 判错。Codex 只是静默忽略。
2. MatcherGroup 里出现未知字段 → 判错。Codex 只是静默忽略。
3. handler 里出现未知字段 → 判错。Codex 只是静默忽略。

顶层字段规则和 Codex 完全一致：多一个字段 → 整个文件失效。
