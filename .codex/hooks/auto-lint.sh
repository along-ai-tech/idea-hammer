#!/bin/bash
# Hook 示例: PostToolUse — 编辑代码后自动跑 linter，把失败原因回灌给模型
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"tool_name":"apply_patch","tool_input":{"command":"<补丁原文>"},...}
#   stdout = JSON；回灌上下文写
#   {"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}
#
# 注意：本 hook 会改用户文件，默认不挂进 hooks.json，需要的项目自行 opt-in。

INPUT=$(cat)
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] || exit 0

FILES=$(echo "$INPUT" | jq -r '
  (
    [ (.tool_input.file_path // empty) ]
    + ((.tool_input.command // "")
       | [ split("\n")[]
         | (try capture("^\\*\\*\\* (Add|Update|Delete) File: (?<p>.+)$") catch empty) | .p ])
  )
  | .[] | select(type == "string" and length > 0)
' 2>/dev/null)

[ -n "$FILES" ] || exit 0

REPORT=""
# 用 here-string 而不是管道，避免 while 跑在子 shell 里丢掉 REPORT 变量
while IFS= read -r FILE_PATH; do
  [ -n "$FILE_PATH" ] || continue
  case "$FILE_PATH" in
    /*) ;;
    *) FILE_PATH="$ROOT/$FILE_PATH" ;;
  esac
  case "$FILE_PATH" in
    "$ROOT"/*) ;;
    *) continue ;;
  esac

  case "$FILE_PATH" in
    *.py)
      if command -v ruff >/dev/null 2>&1; then
        if ! OUT=$(cd "$ROOT" && ruff check --fix "$FILE_PATH" 2>&1); then
          printf -v REPORT '%s\n%s\n%s' "$REPORT" "$FILE_PATH" "$OUT"
        fi
      fi
      ;;
    *.ts|*.tsx|*.js|*.vue)
      if command -v npx >/dev/null 2>&1; then
        if ! OUT=$(cd "$ROOT" && npx eslint --fix "$FILE_PATH" 2>&1); then
          printf -v REPORT '%s\n%s\n%s' "$REPORT" "$FILE_PATH" "$OUT"
        fi
      fi
      ;;
  esac
done <<< "$FILES"

[ -n "$REPORT" ] || exit 0

CTX=$(printf 'lint 未通过，请修复：\n%s' "$REPORT")
jq -nc --arg c "$CTX" \
  '{hookSpecificOutput:{hookEventName:"PostToolUse", additionalContext:$c}}' 2>/dev/null
exit 0
