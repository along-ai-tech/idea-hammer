#!/usr/bin/env bash
# sdd-workspace <plan-file>
# 创建/解析 .idea-hammer/sdd/<plan-id>/ 目录
# 输出绝对路径
set -euo pipefail

PLAN_FILE="${1:?usage: sdd-workspace <plan-file>}"
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# plan-id = plan 文件 basename 去 .md
PLAN_ID="$(basename "${PLAN_FILE}" .md)"
SDD_DIR="${PROJECT_ROOT}/.idea-hammer/sdd/${PLAN_ID}"

mkdir -p "${SDD_DIR}"
# 加进 gitignore（如未加）
GITIGNORE="${PROJECT_ROOT}/.gitignore"
if [ -f "${GITIGNORE}" ] && ! grep -qF ".idea-hammer/sdd/" "${GITIGNORE}"; then
    echo "" >> "${GITIGNORE}"
    echo "# SDD 工作目录（协调态，不入 git）" >> "${GITIGNORE}"
    echo ".idea-hammer/sdd/" >> "${GITIGNORE}"
fi

echo "${SDD_DIR}"