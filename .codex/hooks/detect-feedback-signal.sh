#!/bin/bash
# Hook: UserPromptSubmit
# 检测修正信号，即时入队，不阻塞用户。消化由 evolution-runner 在 session 启动同步消化。
# 采集偏召回：宁可多抓，evolution-runner 在 session 启动同步消化用语义判断滤噪。
# hook 只抓措辞明显的；措辞平和、隐晦的修正由主 Agent 识别后补记一条（见 AGENTS.md）。
#
# Codex hook 协议（openai/codex rust-v0.171.0）：
#   stdin  = {"session_id":...,"cwd":...,"hook_event_name":"UserPromptSubmit","prompt":"..."}
#   本 hook 不产生 stdout（留空即视为无输出，不阻塞用户）

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)

[ -n "$PROMPT" ] || exit 0

echo "$PROMPT" | grep -qE "不是这样|不是这个意思|不应该|搞错|你错|又错|理解错|弄错|不合理|不通用|不对劲|这不对|完全不对|去掉|删掉|删除|改成|换成|改为|不需要|没必要|多余|你漏|漏掉|漏了|你忘|忘了|没提到|没有提到|你没提|少了|每次都|怎么又|怎么还|我说过|说过了|提醒过|强调过|不是让你|没复用|你没按|没生效|没有生效|没执行|不喜欢|不太喜欢|我的意思是|我是说|其实应该|应该是|应该写" || exit 0

ROOT="${IDEA_HAMMER_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$ROOT" ] || exit 0
QUEUE="$ROOT/.codex/evolution/signals.jsonl"
mkdir -p "$(dirname "$QUEUE")" 2>/dev/null || exit 0

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
ID=$(uuidgen 2>/dev/null | tr 'A-Z' 'a-z')
[ -n "$ID" ] || ID=$(openssl rand -hex 16 2>/dev/null)

# 按 schemas/evolution-signal.schema.json 的 EvolutionSignal 结构落一条 explicit 层修正信号
jq -nc \
  --arg id "$ID" \
  --arg now "$NOW" \
  --arg prompt "$PROMPT" \
  --arg context "UserPromptSubmit hook 捕获" \
  '{id:$id, type:"correction", layer:"explicit", created_at:$now, prompt:$prompt, context:$context, tags:["hook"]}' \
  >> "$QUEUE" 2>/dev/null

exit 0
