#!/usr/bin/env bash
# task-brief <plan-file> <N>
# 抽 plan 第 N 个 task 的 brief 到 .idea-hammer/sdd/<plan-id>/task-N-brief.md
# 输出 brief 文件路径
set -euo pipefail

PLAN_FILE="${1:?usage: task-brief <plan-file> <N>}"
TASK_NUM="${2:?usage: task-brief <plan-file> <N>}"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
PLAN_ID="$(basename "${PLAN_FILE}" .md)"
SDD_DIR="${PROJECT_ROOT}/.idea-hammer/sdd/${PLAN_ID}"
BRIEF="${SDD_DIR}/task-${TASK_NUM}-brief.md"

# awk 抽 Task N 段到下一个 Task N+1 或文件尾
# POSIX 兼容：用 sed 抽取头部，awk 读取到下一个 Task 退出
awk -v n="${TASK_NUM}" '
    /^### Task [0-9]+:/ {
        # 提取当前 Task 编号
        h = $0
        sub(/^### Task /, "", h)
        sub(/:.*$/, "", h)
        cur = h + 0
        if (cur == n + 0) { in_task = 1; print; next }
        if (in_task) exit
    }
    in_task { print }
' "${PLAN_FILE}" > "${BRIEF}"

# 同时建 report 文件占位
REPORT="${SDD_DIR}/task-${TASK_NUM}-report.md"
[ -f "${REPORT}" ] || touch "${REPORT}"

echo "${BRIEF}"