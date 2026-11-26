"""契约测试 — session.schema.json 与真实 session.json 必须对得上。

schema 里 additionalProperties 是 false，所以 session.json 少一个字段定义
就是断链（v0.11.0 加 checkpoints 时踩过一次）。
"""

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent.parent
SCHEMA_PATH = ROOT / "schemas" / "session.schema.json"
SESSION_PATH = ROOT / ".idea-hammer" / "session.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def validator():
    """带 format 校验的 session schema 校验器。"""
    from jsonschema import Draft7Validator, FormatChecker

    schema = _load(SCHEMA_PATH)
    Draft7Validator.check_schema(schema)
    return Draft7Validator(schema, format_checker=FormatChecker())


def test_schema_is_valid_json_schema():
    """schema 本身是合法 JSON Schema。"""
    from jsonschema import Draft7Validator

    Draft7Validator.check_schema(_load(SCHEMA_PATH))


def test_real_session_json_validates(validator):
    """仓库里的真实 session.json 必须过 schema（含 format 校验）。"""
    if not SESSION_PATH.exists():
        pytest.skip("无 .idea-hammer/session.json")

    errors = sorted(validator.iter_errors(_load(SESSION_PATH)), key=lambda e: e.path)
    assert not errors, "session.json 不符合 schema:\n" + "\n".join(
        f"  {list(e.path)}: {e.message}" for e in errors
    )


def test_schema_defines_checkpoints():
    """schema 必须定义 checkpoints（v0.11.0 引入的恢复点数组）。"""
    schema = _load(SCHEMA_PATH)
    assert "checkpoints" in schema.get("properties", {}), "schema 缺 checkpoints 定义"

    item = schema["properties"]["checkpoints"]["items"]
    for field in ("phase", "task", "git_commit", "tests", "next_action", "created_at"):
        assert field in item.get("properties", {}), f"checkpoint item 缺字段: {field}"


def test_checkpoint_sample_validates(validator):
    """带 checkpoint 的 session 样例必须过 schema。"""
    sample = {
        "schema_version": "1.0",
        "last_updated": "2026-11-26T15:48:00+08:00",
        "current_phase": "v0.11.0-dev",
        "current_task": "D-016",
        "checkpoints": [
            {
                "id": "cp-20261126-154812",
                "phase": "v0.11.0-dev",
                "task": "D-016",
                "git_commit": "472a946",
                "tests": {"contract_test": "240 passed"},
                "next_action": "commit",
                "artifacts": ["CONTEXT.md"],
                "created_at": "2026-11-26T15:48:00+08:00",
            }
        ],
    }
    errors = sorted(validator.iter_errors(sample), key=lambda e: e.path)
    assert not errors, "checkpoint 样例不符合 schema:\n" + "\n".join(
        f"  {list(e.path)}: {e.message}" for e in errors
    )


def test_schema_rejects_unknown_field(validator):
    """schema 仍然拒绝未知字段（防止字段被随意塞进来）。"""
    sample = {
        "schema_version": "1.0",
        "last_updated": "2026-11-26T15:48:00+08:00",
        "totally_unknown_field": "x",
    }
    assert not validator.is_valid(sample), "schema 不该接受未知字段"

