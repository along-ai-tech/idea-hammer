#!/bin/bash
# Hook 示例: PreToolUse (transform 模式)
# 过滤敏感信息（API key / password / token）从 prompt 中
# transform 模式：返回 JSON {"transform": "新内容"} 替换输入

set -e

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# 仅对 UserPrompt 处理
if [ "$TOOL_NAME" != "user_prompt" ]; then
  exit 0
fi

PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)
if [ -z "$PROMPT" ]; then
  exit 0
fi

# 检测敏感词（演示用：sk-、password、token）
SANITIZED=$(echo "$PROMPT" | sed -E 's/(sk-[a-zA-Z0-9-]{20,})/[REDACTED-SK-KEY]/g; s/(password[ =:][ ]*["'\'']?)[^[:space:]"'\'',}]+/\1[REDACTED]/gi')

# 如果有替换，输出 transform
if [ "$SANITIZED" != "$PROMPT" ]; then
  # 注意：实际框架应解析这个 JSON
  echo "{\"transform\": $(echo "$SANITIZED" | jq -Rs .)}"
fi

exit 0
