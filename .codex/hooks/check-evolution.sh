#!/bin/bash
# Hook: SessionStart
# 有待确认的进化建议，或有待消化的信号时，把提示注入 session 上下文。
# 只提示，绝不阻塞。
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"session_id":...,"cwd":...,"hook_event_name":"SessionStart","source":...}
#   stdout = JSON；纯文本会被判为无效输出
#   {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"..."}}

ROOT="${IDEA_HAMMER_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$ROOT" ] || exit 0
EVO="$ROOT/.codex/evolution"
PROPOSALS="$EVO/proposals.md"
SIGNALS="$EVO/signals.jsonl"

MSG=""

# 只数 ## 待审阅 区的建议，不误数 ## 已消化日志 等其他区的 - 行
if [ -f "$PROPOSALS" ]; then
  N=$(awk '/^## 待审阅/{f=1;next} /^## /{f=0} f&&/^- /{c++} END{print c+0}' "$PROPOSALS" 2>/dev/null)
  if [ "${N:-0}" -gt 0 ] 2>/dev/null; then
    MSG="📋 有 ${N} 条进化建议待拍板，session 启动我会逐条摆给你问同不同意。"
  fi
fi

if [ -f "$SIGNALS" ] && [ -s "$SIGNALS" ]; then
  MSG="${MSG} 🔄 有新进化信号，session 启动我会扫一遍、消化成建议并逐条问你。"
fi

[ -n "$MSG" ] || exit 0

jq -nc --arg ctx "$MSG" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$ctx}}' 2>/dev/null
exit 0
