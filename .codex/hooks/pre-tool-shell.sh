#!/bin/bash
# Hook: PreToolUse（命令工具）— 合并 Claude 版的 pre-commit-check 与 pnpm-dev 清端口
# Codex 的 matcher 只过滤 tool name，命令内容判断在脚本里做。
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"tool_name":"Bash","tool_input":{"command":"<命令行字符串>"},...}
#   stdout = JSON；拦截写 {"decision":"block","reason":"..."}
#   注意：stdout 非 JSON 会被判为无效输出，诊断信息一律写 stderr

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // .tool_input.cmd // .command // empty' 2>/dev/null)
[ -n "$CMD" ] || exit 0
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"

block() {
  jq -nc --arg r "$1" '{decision:"block", reason:$r}' 2>/dev/null
  exit 0
}

# git commit 前：编译检查，不过则阻止
if echo "$CMD" | grep -qE "git commit" && [ -n "$ROOT" ]; then
  TSCONFIG=$(find "$ROOT" -maxdepth 3 -name "tsconfig.json" -not -path "*/node_modules/*" -not -path "*/.next/*" 2>/dev/null | head -1)
  if [ -n "$TSCONFIG" ]; then
    if ! TSC_OUTPUT=$(cd "$(dirname "$TSCONFIG")" && npx tsc --noEmit 2>&1); then
      TSC_MSG=$(printf '编译检查未通过，commit 被阻止。请修复以下错误：\n%s' "$TSC_OUTPUT")
      block "$TSC_MSG"
    fi
  fi
fi

# pnpm dev 前：清占用端口，避免端口被占导致启动失败
if echo "$CMD" | grep -qE "pnpm dev|npm run dev|yarn dev"; then
  for port in 3000 3001 4173 5173 8080; do kill -9 "$(lsof -ti:$port)" 2>/dev/null; done
fi

exit 0
