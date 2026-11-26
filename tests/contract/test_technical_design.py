"""契约测试 — dev-planner 的技术设计阶段必须可发现、结构完整、与 DEV-PLAN 衔接。"""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent.parent
SKILL_DIR = REPO_ROOT / "agents" / "skills" / "dev-planner"
EXAMPLE = REPO_ROOT / "examples" / "personal-blog"

REQUIRED_DOCS = [
    SKILL_DIR / "principles" / "technical-design.md",
    SKILL_DIR / "templates" / "technical-design-template.md",
    SKILL_DIR / "workflows" / "workflow-technical-design.md",
]

REQUIRED_CONCEPTS = [
    "架构模式",
    "ADR",
    "限界上下文",
    "聚合",
    "不变量",
    "唯一约束",
    "索引",
    "API Contract",
    "OpenAPI",
    "契约测试",
    "风险",
]


@pytest.mark.parametrize("doc", REQUIRED_DOCS)
def test_technical_design_docs_exist_and_not_empty(doc):
    assert doc.exists(), f"缺少 {doc.relative_to(REPO_ROOT)}"
    assert doc.read_text(encoding="utf-8").strip(), f"{doc.name} 为空"


def test_technical_design_concepts_present():
    text = "\n".join(d.read_text(encoding="utf-8") for d in REQUIRED_DOCS)
    missing = [c for c in REQUIRED_CONCEPTS if c not in text]
    assert not missing, f"技术设计文档缺关键概念: {missing}"


def test_dev_planner_skill_requires_technical_design():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "Technical-Design.md" in skill
    assert "workflow-technical-design.md" in skill

    workflow = (SKILL_DIR / "workflows" / "workflow-generate.md").read_text(
        encoding="utf-8"
    )
    assert "技术设计" in workflow, "生成 DEV-PLAN 前应有技术设计门禁"


def test_output_schema_requires_technical_design():
    schema = json.loads(
        (SKILL_DIR / "contracts" / "output.schema.json").read_text(encoding="utf-8")
    )
    assert "technical_design" in schema["required"]

    td = schema["properties"]["technical_design"]
    for field in ["architecture_pattern", "domain_model", "data_model", "api_contract", "adrs"]:
        assert field in td["required"], f"technical_design 缺必填字段 {field}"

    patterns = td["properties"]["architecture_pattern"]["enum"]
    assert {"monolith", "modular_monolith", "microservices"} <= set(patterns)


def test_dev_builder_consumes_technical_design():
    text = (REPO_ROOT / "agents" / "skills" / "dev-builder" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Technical-Design.md" in text


def test_example_has_technical_design():
    doc = EXAMPLE / "Technical-Design.md"
    assert doc.exists(), "示例项目缺 Technical-Design.md"

    text = doc.read_text(encoding="utf-8")
    for heading in ["架构决策", "ADR", "领域模型", "数据库设计", "API Contract", "风险"]:
        assert heading in text, f"示例技术设计缺「{heading}」"

    assert "EP-9" in text
    assert "UNIQUE(post_id, ip)" in text
