"""契约测试 — goal-creator 关键概念必现 + 禁止模式不现。"""

import re
from pathlib import Path

import pytest


SKILL_NAME = "goal-creator"
SKILL_DIR = Path(__file__).parent.parent.parent / "agents" / "skills" / SKILL_NAME


def _all_text():
    """收集 skill 目录下所有 .md 和 .json 文件内容。"""
    texts = []
    for f in SKILL_DIR.rglob("*.md"):
        texts.append(f.read_text(encoding="utf-8"))
    for f in SKILL_DIR.rglob("*.json"):
        texts.append(f.read_text(encoding="utf-8"))
    return "\n".join(texts)


def test_must_concepts_present():
    """关键概念必须出现在 skill 内容里。"""
    text = _all_text()
    missing = []
    for concept in MUST_CONCEPTS:
        if concept not in text:
            missing.append(concept)
    assert not missing, f"{SKILL_NAME} 缺关键概念: {missing}"


def test_must_workflow_keywords_present():
    """工作流关键词必须出现。"""
    text = _all_text().lower()
    missing = []
    for kw in MUST_WORKFLOW_KW:
        if kw.lower() not in text:
            missing.append(kw)
    assert not missing, f"{SKILL_NAME} 缺工作流关键词: {missing}"


def test_no_empty_principles():
    """principles/ 下的 .md 文件不能为空。"""
    p_dir = SKILL_DIR / "principles"
    if not p_dir.exists():
        pytest.skip("无 principles/")
    for f in p_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8").strip()
        assert content, f"{f.relative_name} 是空文件"


def test_no_empty_workflows():
    """workflows/ 下的 .md 文件不能为空。"""
    w_dir = SKILL_DIR / "workflows"
    if not w_dir.exists():
        pytest.skip("无 workflows/")
    for f in w_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8").strip()
        assert content, f"{f.relative_name} 是空文件"


MUST_CONCEPTS = ['目标必达', '可自证', '字数硬限', '边界', '不填形式', '联网优先', '上下文']
MUST_WORKFLOW_KW = [
    '/goal', '上下文', '验证',
]
