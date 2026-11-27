#!/usr/bin/env bash
# review-package <plan-file> <N> <base> <head>
# 抽 task N 在 base..head 范围的 diff 到 .idea-hammer/sdd/<plan-id>/task-N-review-pkg.txt
# 输出 package 文件路径
set -euo pipefail

PLAN_FILE="${1:?usage: review-package <plan-file> <N> <base> <head>}"
TASK_NUM="${2:?usage: review-package <plan-file> <N> <base> <head>}"
BASE="${3:?usage: review-package <plan-file> <N> <base> <head>}"
HEAD="${4:?usage: review-package <plan-file> <N> <base> <head>}"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
PLAN_ID="$(basename "${PLAN_FILE}" .md)"
SDD_DIR="${PROJECT_ROOT}/.idea-hammer/sdd/${PLAN_ID}"
PKG="${SDD_DIR}/task-${TASK_NUM}-review-pkg.txt"

{
    echo "=== git log for ${BASE}..${HEAD} ==="
    git log --oneline "${BASE}..${HEAD}" 2>/dev/null || echo "(no git or empty range)"
    echo ""
    echo "=== git diff --stat ${BASE}..${HEAD} ==="
    git diff --stat "${BASE}..${HEAD}" 2>/dev/null || echo "(no diff)"
    echo ""
    echo "=== git diff -U10 ${BASE}..${HEAD} ==="
    git diff -U10 "${BASE}..${HEAD}" 2>/dev/null || echo "(no diff)"
} > "${PKG}"

echo "${PKG}"