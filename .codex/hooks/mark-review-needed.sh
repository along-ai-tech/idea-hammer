#!/bin/bash
# PostToolUse hook: 代码文件被编辑/创建后标记需要 review
# 排除已知的非代码文件，其余都触发
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"tool_name":"apply_patch","tool_input":{"command":"<补丁原文>"},...}
#   apply_patch 是 freeform 工具，tool_input.command 是补丁原文而不是参数对象，
#   文件路径要从 "*** Add File:" / "*** Update File:" / "*** Delete File:" / "*** Move to:" 行里抽；
#   其他编辑类工具直接给 tool_input.file_path。

INPUT=$(cat)
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] || exit 0

FILES=$(echo "$INPUT" | jq -r '
  (
    [ (.tool_input.file_path // empty) ]
    + ((.tool_input.command // "")
       | [ split("\n")[]
         | (try capture("^\\*\\*\\* (Add|Update|Delete) File: (?<p>.+)$") catch empty) | .p ])
    + ((.tool_input.command // "")
       | [ split("\n")[]
         | (try capture("^\\*\\*\\* Move to: (?<p>.+)$") catch empty) | .p ])
  )
  | .[] | select(type == "string" and length > 0)
' 2>/dev/null)

[ -n "$FILES" ] || exit 0

MARK="$ROOT/.codex/.needs-review"

echo "$FILES" | while IFS= read -r FILE_PATH; do
  [ -n "$FILE_PATH" ] || continue

  # apply_patch 给的是相对 cwd 的路径，补成绝对路径
  case "$FILE_PATH" in
    /*) ;;
    *) FILE_PATH="$ROOT/$FILE_PATH" ;;
  esac

  # 只管项目目录内的文件，/tmp 等外部路径不触发
  case "$FILE_PATH" in
    "$ROOT"/*) ;;
    *) continue ;;
  esac

  # 无扩展名的文件（脚本草稿、数据、内容稿等）不是项目代码，不触发
  case "$(basename "$FILE_PATH")" in
    *.*) ;;
    *) continue ;;
  esac

  # 排除框架元目录和非代码文件，其余才标记需要 review
  case "$FILE_PATH" in
    */.claude/*|*/.codex/*|*/.agents/*|*.md|*.txt|*.json|*.yaml|*.yml|*.toml|*.lock|*.log|*.env|*.env.*|*.gitignore|*.prettierrc|*.eslintrc)
      ;;
    *)
      mkdir -p "$(dirname "$MARK")" 2>/dev/null
      echo "needs_review" > "$MARK"
      ;;
  esac
done

exit 0
