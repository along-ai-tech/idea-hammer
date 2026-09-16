# Hook 协议 v2 — advisory / transform / retry

> `.codex/hooks.json` 协议规范。三模式让 hook 从"只通知"升级为"可干预"。

## 三种模式对比

|模式 | 用途 | 输出 | 阻塞？ |
|---|---|---|---|
| **advisory** | 单向通知（如 detect-feedback-signal） | stdout 文本 | 否 |
| **transform** | 改写输入（如 prompt 敏感词过滤） | JSON `{"transform": "新内容"}` | 否（替换输入） |
| **retry** | 失败自动重试（如 auto-format） | JSON `{"retry": "命令", "reason": "...", "max_retries": N}` | 否（异步执行） |

## 协议结构

```json
{
  "$version": "2.0",
  "$comment": "...",
  "events": {
    "PreToolUse": [
      {
        "matcher": "user_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "mode": "transform",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## 字段说明

| 字段 | 必 | 说明 |
|---|---|---|
| `$version` | ✅ | 协议版本（v2） |
| `events` | ✅ | 事件 → hook 列表 |
| `matcher` | ❌ | regex 过滤（PreToolUse / PostToolUse 用 tool name） |
| `mode` | ❌ | advisory（默认）/ transform / retry |
| `timeout` | ❌ | 超时（秒），默认 10 |
| `max_retries` | ❌ | retry 模式最大重试次数，默认 3 |

## 三种模式详解

### advisory（默认）

```bash
#!/bin/bash
# Hook 输出任何 stdout 文本作为提示，但不阻塞 / 修改
exit 0
```

**适用**：检测修正信号、状态通知、健康检查。

### transform

```bash
#!/bin/bash
INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt')

SANITIZED=$(echo "$PROMPT" | sed -E 's/(sk-[a-zA-Z0-9-]{20,})/[REDACTED]/g')

# 只有要改写时才输出 JSON
if [ "$SANITIZED" != "$PROMPT" ]; then
  echo "{\"transform\": $(echo "$SANITIZED" | jq -Rs .)}"
fi
exit 0
```

**返回格式**：`{"transform": "替换后的内容"}`（被 JSON 编码的字符串）

**适用**：敏感词过滤 / prompt 注入防护 / 自动补全 prompt。

### retry

```bash
#!/bin/bash
FILE_PATH=$(cat | jq -r '.file_path')

cat <<JSON
{
  "retry": "ruff check --fix $FILE_PATH",
  "reason": "auto-lint after edit",
  "max_retries": 1
}
JSON
exit 0
```

**返回格式**：`{"retry": "命令", "reason": "...", "max_retries": N}`

**适用**：编辑后自动 lint / 自动 format / 自动测试。

## 事件清单

| 事件 | 时机 | 典型用途 |
|---|---|---|
| `UserPromptSubmit` | 用户提交 prompt | detect-feedback-signal（advisory） |
| `SessionStart` | session 启动 | check-evolution（advisory） |
| `PreToolUse` | 工具调用前 | sanitize-prompt（transform） |
| `PostToolUse` | 工具调用后 | auto-lint（retry）、mark-review-needed（advisory）、auto-push（advisory） |
| `Stop` | 主 Agent 停止 | stop-gate（advisory） |

## 安全沙箱

- transform / retry 模式必须用 JSON 输出（不是 stdout 文本）
- transform 模式：脚本异常时 fallback 到原输入（不阻塞）
- retry 模式：超时 / 失败时记日志，不无限重试

## 迁移指南

从 v1 → v2：

1. 每个 hook 加 `mode` 字段（默认 advisory）
2. 顶层加 `$version: "2.0"`
3. 顶层加 `events` 包装：

```diff
 {
+  "$version": "2.0",
+  "events": {
-  "UserPromptSubmit": [...],
+  "UserPromptSubmit": [...]
+  }
 }
```

## 已实现示例

- `sanitize-prompt.sh` — PreToolUse transform（敏感词过滤）
- `auto-lint.sh` — PostToolUse retry（编辑后自动 lint）

## 验收

- [x] schemas/hook-protocol.schema.json — JSON Schema 校验合法
- [x] .codex/hooks.json — 所有现有 hook 加 mode: advisory
- [x] 示例 hook 脚本（transform + retry）
- [x] 文档（本文）
