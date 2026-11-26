"""契约测试 — Context Engineering 域 + 跨 Session 恢复协议。

Day9 第四模块要求把上下文质量变成可检查的工程纪律：
上下文分类、Context Selection、三种加载技术、Memory/State/Checkpoint 分工、
以及"State 只定位不代替核查"的恢复原则。
"""

from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent.parent
CONTEXT_DOC = ROOT / "CONTEXT.md"
AGENTS_MD = ROOT / "AGENTS.md"
WORKFLOW_MD = ROOT / "WORKFLOW.md"
STATE_ROUTING = ROOT / "STATE-ROUTING.md"
DEV_BUILDER = ROOT / "agents" / "skills" / "dev-builder"
CODE_REVIEW = ROOT / "agents" / "skills" / "code-review"


def _read(path):
    return path.read_text(encoding="utf-8")


def test_context_doc_exists():
    """CONTEXT.md 域文件必须存在。"""
    assert CONTEXT_DOC.exists(), "CONTEXT.md 不存在（上下文工程域缺失）"
    assert len(_read(CONTEXT_DOC).strip()) > 500, "CONTEXT.md 内容过短"


@pytest.mark.parametrize(
    "context_type",
    [
        "Task Context",
        "Product Context",
        "Technical Context",
        "Code Context",
        "Engineering Context",
        "Execution Context",
        "Session Context",
    ],
)
def test_seven_context_types_documented(context_type):
    """7 类上下文必须被显式定义。"""
    assert context_type in _read(CONTEXT_DOC), f"CONTEXT.md 缺上下文类型: {context_type}"


@pytest.mark.parametrize(
    "technique",
    ["Context Retrieval", "Progressive Disclosure", "Context Compression"],
)
def test_three_context_techniques_documented(technique):
    """三种上下文技术必须出现。"""
    assert technique in _read(CONTEXT_DOC), f"CONTEXT.md 缺上下文技术: {technique}"


@pytest.mark.parametrize("concept", ["Memory", "State", "Checkpoint"])
def test_memory_state_checkpoint_documented(concept):
    """Memory / State / Checkpoint 三分工必须出现。"""
    assert concept in _read(CONTEXT_DOC), f"CONTEXT.md 缺概念: {concept}"


def test_checkpoint_not_equal_git_commit():
    """Checkpoint ≠ Git Commit 必须点明（两者职责不同）。"""
    text = _read(CONTEXT_DOC)
    assert "Checkpoint ≠ Git Commit" in text or "Checkpoint 不等于 Git Commit" in text, (
        "CONTEXT.md 未区分 Checkpoint 与 Git Commit"
    )


def test_state_does_not_replace_verification():
    """核心原则：State 只定位恢复位置，不代替对真实代码与执行结果的核查。"""
    text = _read(CONTEXT_DOC)
    assert "不代替" in text, "CONTEXT.md 缺'State 不代替核查'原则"
    assert "核查" in text or "核实" in text, "CONTEXT.md 缺核查要求"


def test_agents_md_references_context_doc():
    """AGENTS.md 必须把 CONTEXT.md 列进域文件与启动顺序。"""
    text = _read(AGENTS_MD)
    assert "CONTEXT.md" in text, "AGENTS.md 未引用 CONTEXT.md"


def test_state_routing_has_restore_verification():
    """STATE-ROUTING 必须含恢复时核实真实代码/测试的步骤。"""
    text = _read(STATE_ROUTING)
    assert "核实" in text or "核查" in text, "STATE-ROUTING 缺恢复核实步骤"


def test_workflow_has_mode_routing():
    """WORKFLOW 必须含 Plan / Agent 模式分流判据。"""
    text = _read(WORKFLOW_MD)
    assert "模式分流" in text or "规划模式" in text, "WORKFLOW 缺 Plan/Agent 模式分流"


def test_dev_builder_has_context_principle():
    """dev-builder 必须有上下文装配原则文件。"""
    path = DEV_BUILDER / "principles" / "context-engineering.md"
    assert path.exists(), "dev-builder/principles/context-engineering.md 不存在"
    assert len(_read(path).strip()) > 300, "context-engineering.md 内容过短"


def test_dev_builder_has_test_pyramid_principle():
    """dev-builder 必须有测试金字塔分层原则文件。"""
    path = DEV_BUILDER / "principles" / "test-pyramid.md"
    assert path.exists(), "dev-builder/principles/test-pyramid.md 不存在"
    assert len(_read(path).strip()) > 300, "test-pyramid.md 内容过短"


def test_dev_builder_skill_md_references_new_principles():
    """dev-builder SKILL.md 必须引用两个新原则。"""
    text = _read(DEV_BUILDER / "SKILL.md")
    assert "context-engineering.md" in text, "SKILL.md 未引用 context-engineering.md"
    assert "test-pyramid.md" in text, "SKILL.md 未引用 test-pyramid.md"


def test_stage2_checks_test_layers_and_invariants():
    """Stage 2 必须检查测试层级与并发不变量门禁。"""
    text = _read(CODE_REVIEW / "principles" / "stage2-checklist.md")
    assert "不变量" in text, "Stage 2 缺业务不变量检查"
    assert "并发" in text, "Stage 2 缺并发竞态检查"
    assert "Contract" in text or "契约测试" in text, "Stage 2 缺契约测试检查"


def test_task_loop_has_context_assembly_step():
    """Task 循环必须显式做上下文装配，不能只说'读原文'。"""
    text = _read(DEV_BUILDER / "workflows" / "workflow-task-loop.md")
    assert "上下文" in text, "task-loop 缺上下文装配步骤"

