"""契约测试：product-spec-builder 输出 schema 必须强制四要素。

确认 Spec 的输出结构不是 AI 自由发挥：PRD 字段、User Story 三句、AC ≥ 3 且编号可追溯。
"""
import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "agents"
    / "skills"
    / "product-spec-builder"
    / "contracts"
    / "output.schema.json"
)


def base_payload():
    return {
        "phases_complete": [1, 2, 3, 4, 5, 6, 7],
        "target_user": "有长期写作需求的独立作者",
        "job_to_be_done": "把文章发布出去并收到反馈",
        "success_metrics": ["发布闭环 100%"],
        "features": [
            {
                "id": "REQ-001",
                "name": "发布文章",
                "user_value": "从两天缩短到五分钟",
                "user_story": "作为一个 作者，我希望 发布文章，以便于 沉淀长期资产",
                "acceptance_criteria": [
                    "AC-001-01 Given 合法输入 when 提交 then 201",
                    "AC-001-02 Given 空标题 when 提交 then 422",
                    "AC-001-03 Given 超长标题 when 提交 then 422",
                ],
                "delete_path": "DELETE /api/posts/{id}",
            }
        ],
        "non_goals": ["多用户协作"],
        "ai_capabilities": [],
        "assumptions": [
            {
                "id": "ASM-001",
                "statement": "单作者自用",
                "basis": "只有作者发布",
                "risk_if_wrong": "需要补权限体系",
            }
        ],
        "open_questions": [{"id": "Q-001", "question": "是否需要草稿", "blocking": False}],
    }


def validate(payload):
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return list(Draft7Validator(schema).iter_errors(payload))


def test_schema_is_valid():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)


def test_complete_payload_passes():
    assert validate(base_payload()) == []


def test_missing_target_user_fails():
    payload = base_payload()
    del payload["target_user"]
    assert validate(payload)


def test_feature_without_user_story_fails():
    payload = base_payload()
    del payload["features"][0]["user_story"]
    assert validate(payload)


def test_feature_with_less_than_three_ac_fails():
    payload = base_payload()
    payload["features"][0]["acceptance_criteria"] = ["AC-001-01 Given x when y then z"]
    assert validate(payload)


def test_ac_id_must_match_pattern():
    payload = base_payload()
    payload["features"][0]["acceptance_criteria"][0] = "验收条件 1"
    assert validate(payload)


@pytest.mark.parametrize("field", ["non_goals", "success_metrics", "open_questions"])
def test_prd_and_gate_fields_are_required(field):
    payload = base_payload()
    del payload[field]
    assert validate(payload)
