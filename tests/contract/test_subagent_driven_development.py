"""契约测试 — subagent-driven-development skill。

SDD 是 dev-builder 之外的第二条执行路径：切任务循环 + 任务级两段 review + judgment ledger。
它的行为契约必须和代码一样被锁住，否则会被当成"另一份文档"慢慢腐化。
"""

import json
import os
from pathlib import Path

import pytest
from jsonschema import Draft7Validator


ROOT = Path(__file__).parent.parent.parent
SDD_DIR = ROOT / "agents" / "skills" / "subagent-driven-development"


def _read(rel):
    return (SDD_DIR / rel).read_text(encoding="utf-8")


def test_skill_md_frontmatter():
    """SKILL.md 有合法 frontmatter。"""
    import yaml

    text = _read("SKILL.md")
    assert text.startswith("---\n"), "SKILL.md 缺 frontmatter"
    fm = yaml.safe_load(text.split("---")[1])
    assert fm.get("name") == "subagent-driven-development"
    assert fm.get("description"), "SDD description 为空"


@pytest.mark.parametrize(
    "concept",
    [
        "两段",
        "ledger",
        "breaker",
        "fix",
        "fresh",
    ],
)
def test_key_concepts_present(concept):
    """关键机制词必须出现在 skill 内容里。"""
    text = "\n".join(
        p.read_text(encoding="utf-8")
        for p in SDD_DIR.rglob("*.md")
    )
    assert concept in text, f"SDD 缺关键机制: {concept}"


def test_principles_file_exists():
    """principles/ 必须有内容（--strict 门禁要求）。"""
    p_dir = SDD_DIR / "principles"
    assert p_dir.is_dir(), "SDD 缺 principles/"
    assert any(f.suffix == ".md" for f in p_dir.iterdir()), "SDD principles/ 无 .md"


@pytest.mark.parametrize("name", ["input.schema.json", "output.schema.json"])
def test_contracts_valid_schema(name):
    """contracts/ 必须是合法 JSON Schema（--strict 门禁要求）。"""
    path = SDD_DIR / "contracts" / name
    assert path.exists(), f"SDD 缺 contracts/{name}"
    Draft7Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_input_schema_requires_plan_file():
    """输入契约必须要求 DEV-PLAN 路径。"""
    schema = json.loads(_read("contracts/input.schema.json"))
    assert "plan_file" in schema["required"], "input schema 未要求 plan_file"


def test_input_schema_required_matches_skill_dependencies():
    """input schema 的 required 必须与 SKILL.md 的依赖检测一致。

    SKILL.md 写"必需：DEV-PLAN.md、Product-Spec.md"，
    schema 只 required plan_file 会让缺 Product-Spec 的输入通过校验。
    """
    schema = json.loads(_read("contracts/input.schema.json"))
    required = set(schema["required"])
    assert {"plan_file", "product_spec_path"} <= required, (
        f"input schema required 与 SKILL.md 依赖检测不一致: {required}"
    )

    for prop in ("plan_file", "product_spec_path"):
        assert "必填" in schema["properties"][prop].get("description", ""), (
            f"{prop} 的 description 应标明必填"
        )


def test_input_schema_covers_mode_routing():
    """输入契约要能表达 sdd / dev-builder 两种模式与任务数。"""
    schema = json.loads(_read("contracts/input.schema.json"))
    props = schema["properties"]
    assert props["mode"]["enum"] == ["sdd", "dev-builder"]
    assert "task_count" in props


def test_output_schema_has_tasks_and_verification():
    """输出契约必须有任务列表与验证证据。"""
    schema = json.loads(_read("contracts/output.schema.json"))
    assert "tasks" in schema["required"], "output schema 未要求 tasks"
    assert "verification" in schema["required"], "output schema 未要求 verification"

    task_props = schema["properties"]["tasks"]["items"]["properties"]
    assert {"task_id", "status", "review_clean"} <= set(task_props)


def test_output_schema_models_breakers_and_rulings():
    """输出契约要能记 breaker 与仲裁结论（不靠聊天记录）。"""
    schema = json.loads(_read("contracts/output.schema.json"))
    assert "breakers" in schema["properties"]
    assert "rulings" in schema["properties"]
    resolution = schema["properties"]["breakers"]["items"]["properties"]["resolution"]
    assert set(resolution["enum"]) == {"park", "rule", "stop"}


@pytest.mark.parametrize(
    "script", ["sdd-workspace.sh", "task-brief.sh", "review-package.sh"]
)
def test_scripts_exist_and_executable(script):
    """三个工具脚本必须在且可执行。"""
    path = SDD_DIR / "scripts" / script
    assert path.exists(), f"SDD 缺 scripts/{script}"
    assert os.access(path, os.X_OK), f"scripts/{script} 不可执行"


def test_workflow_covers_four_phases():
    """执行流程必须覆盖 Phase 0-3。"""
    text = _read("workflows/execute.md")
    for phase in ("Phase 0", "Phase 1", "Phase 2", "Phase 3"):
        assert phase in text, f"execute.md 缺 {phase}"

