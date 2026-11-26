#!/bin/bash
# Hook 示例: UserPromptSubmit — 检出明文密钥就拦下这次提交
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"session_id":...,"cwd":...,"hook_event_name":"UserPromptSubmit","prompt":"..."}
#   stdout = JSON；拦截写 {"decision":"block","reason":"..."}
#
# 注意：Codex 没有 "transform"（改写输入）模式，prompt 只能原样送出或整条拦下。
# 本 hook 默认不挂进 hooks.json，需要的项目自行 opt-in。

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)
[ -n "$PROMPT" ] || exit 0

HITS=$(echo "$PROMPT" | grep -oE "sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}" | sort -u)
[ -n "$HITS" ] || exit 0

REASON=$(printf '检测到疑似明文密钥（%s 处），已拦截本次提交。请改用环境变量或密钥管理，不要把凭据写进 prompt。' "$(echo "$HITS" | wc -l | tr -d ' ')")
jq -nc --arg r "$REASON" '{decision:"block", reason:$r}' 2>/dev/null
exit 0
