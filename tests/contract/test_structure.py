"""通用结构契约 — 每个 skill 必须满足。"""

import json
import re
from pathlib import Path

import pytest
import yaml


MAX_SKILL_MD_LINES = 50


def test_skill_md_exists(skill_dir):
    """SKILL.md 存在。"""
    assert (skill_dir / "SKILL.md").exists(), f"{skill_dir.name}/SKILL.md 不存在"


def test_skill_md_max_lines(skill_md_lines, skill_name):
    """SKILL.md ≤ 50 行。"""
    assert len(skill_md_lines) <= MAX_SKILL_MD_LINES, (
        f"{skill_name}/SKILL.md 有 {len(skill_md_lines)} 行（> {MAX_SKILL_MD_LINES}）"
    )


def test_frontmatter_exists(frontmatter, skill_name):
    """YAML frontmatter 存在且是 dict。"""
    assert frontmatter is not None, f"{skill_name} 缺 frontmatter（需要 --- 包裹）"
    assert isinstance(frontmatter, dict), f"{skill_name} frontmatter 不是 dict"


def test_frontmatter_required_fields(frontmatter, skill_name):
    """name + description 非空。"""
    assert "name" in frontmatter and frontmatter["name"], f"{skill_name} 缺 name"
    assert "description" in frontmatter and frontmatter["description"], (
        f"{skill_name} 缺 description"
    )


def test_principles_dir_has_content(skill_dir, skill_name):
    """principles/ 存在且有内容。"""
    p_dir = skill_dir / "principles"
    if not p_dir.exists():
        pytest.skip(f"{skill_name} 无 principles/（允许：内容少不需要拆）")
    files = list(p_dir.iterdir())
    assert any(f.suffix == ".md" for f in files), (
        f"{skill_name}/principles/ 无 .md 文件"
    )


def test_workflows_dir_has_content(skill_dir, skill_name):
    """workflows/ 存在且有内容。"""
    w_dir = skill_dir / "workflows"
    if not w_dir.exists():
        pytest.skip(f"{skill_name} 无 workflows/")
    files = list(w_dir.iterdir())
    assert any(f.suffix == ".md" for f in files), (
        f"{skill_name}/workflows/ 无 .md 文件"
    )


def test_contracts_json_valid(skill_dir, skill_name):
    """contracts/*.json 是合法 JSON。"""
    c_dir = skill_dir / "contracts"
    if not c_dir.exists():
        pytest.skip(f"{skill_name} 无 contracts/")
    for f in c_dir.glob("*.json"):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            pytest.fail(f"{skill_name}/contracts/{f.name} 不是合法 JSON: {e}")


def test_contracts_json_valid_schema(skill_dir, skill_name):
    """contracts/*.schema.json 是合法 JSON Schema（用 jsonschema 库校验）。"""
    from jsonschema import Draft7Validator
    c_dir = skill_dir / "contracts"
    if not c_dir.exists():
        pytest.skip(f"{skill_name} 无 contracts/")
    for f in c_dir.glob("*.schema.json"):
        try:
            schema = json.loads(f.read_text(encoding="utf-8"))
            Draft7Validator.check_schema(schema)
        except Exception as e:
            pytest.fail(f"{skill_name}/contracts/{f.name} 不是合法 JSON Schema: {e}")
