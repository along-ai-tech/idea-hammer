"""契约测试 — intent_classifier.py 的核心行为。"""

import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parent.parent.parent / "scripts" / "intent_classifier.py"


def run_classify(prompt):
    """运行意图分类器并解析 stdout。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "classify", "--prompt", prompt, "--top", "5"],
        capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent,
    )
    return result.stdout


def test_list_includes_all_skills():
    """list 应输出 11 个 skill。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "list"],
        capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent,
    )
    skill_names = ["bug-fixer", "code-review", "design-brief-builder", "design-maker",
                   "dev-builder", "dev-planner", "evolution-engine", "goal-creator",
                   "product-spec-builder", "release-builder", "skill-builder"]
    for name in skill_names:
        assert name in result.stdout, f"{name} 缺"


def test_product_intent_matches_spec_builder():
    """'我想做一个产品' 应匹配 product-spec-builder（最高分）。"""
    out = run_classify("我想做一个产品")
    assert "product-spec-builder" in out


def test_bug_intent_matches_bug_fixer():
    """'这个功能报错了' 应匹配 bug-fixer（最高分）。"""
    out = run_classify("这个功能报错了")
    assert "bug-fixer" in out


def test_review_intent_matches_code_review():
    """'帮我审查代码质量' 应匹配 code-review。"""
    out = run_classify("帮我审查代码质量")
    assert "code-review" in out


def test_release_intent_matches_release_builder():
    """'打包发布我的应用' 应匹配 release-builder。"""
    out = run_classify("打包发布我的应用")
    assert "release-builder" in out


def test_design_intent_matches_design_brief_builder():
    """'设计风格' 应匹配 design-brief-builder。"""
    out = run_classify("我要定设计风格，想要高级感")
    assert "design-brief-builder" in out
