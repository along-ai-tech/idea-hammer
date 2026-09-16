#!/bin/bash
# Hook 示例: PostToolUse (retry 模式)
# 检测到 .py / .ts 编辑后自动跑 linter
# retry 模式：返回 JSON {"retry": "命令"} 触发自动 retry

set -e

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // empty' 2>/dev/null)

# 只对文件编辑类操作
if [ -z "$FILE_PATH" ] || [ -z "$TOOL_NAME" ]; then
  exit 0
fi

# 只对 Python / TS 文件
case "$FILE_PATH" in
  *.py) CMD="ruff check --fix $FILE_PATH" ;;
  *.ts|*.tsx|*.js|*.vue) CMD="npx eslint --fix $FILE_PATH" ;;
  *) exit 0 ;;
esac

# 返回 retry 指令（实际框架会解析执行）
cat <<JSON
{
  "retry": "$CMD",
  "reason": "auto-lint after edit",
  "max_retries": 1
}
JSON

exit 0
