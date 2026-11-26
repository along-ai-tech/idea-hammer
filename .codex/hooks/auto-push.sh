#!/bin/bash
# Hook: PostToolUse（命令工具）— commit 后自动 push，保护分支不自动推
# Codex 的 matcher 只过滤 tool name，git commit 判断在脚本里。
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"tool_name":"Bash","tool_input":{"command":"<命令行字符串>"},...}
#   本 hook 无需 stdout（留空即视为无输出）

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.cmd // .command // empty' 2>/dev/null)
echo "$CMD" | grep -qE "git commit" || exit 0

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] || exit 0
BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null)

case "$BRANCH" in
  main|master)
    echo "⚠️ 当前在 $BRANCH 分支，已跳过自动 push。保护分支需手动 push 或走 PR。" >&2
    exit 0
    ;;
  "")
    exit 0
    ;;
esac

if ! PUSH_OUT=$(git -C "$ROOT" push 2>&1); then
  echo "❌ 自动 push 失败，请手动检查：" >&2
  echo "$PUSH_OUT" >&2
fi

exit 0
