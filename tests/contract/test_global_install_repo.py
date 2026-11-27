"""契约测试 — 真实仓库里跟全局安装相关的静态资产。

安装器把仓库当源用：模板、hook 协议、子 Agent 定义都从这里取。
这些资产坏了，装出去就是一份死配置——所以单独锁一份静态契约。
"""

import json
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).parent.parent.parent
HOOK_SCHEMA = ROOT / "schemas" / "hook-protocol.schema.json"

BLOCK_START = "<!-- idea-hammer:global:start -->"
BLOCK_END = "<!-- idea-hammer:global:end -->"


def test_real_repo_source_has_required_layout():
    """真实仓库必须备齐安装器依赖的四样东西。"""
    assert (ROOT / "docs" / "global-agents.template.md").is_file()
    assert (ROOT / ".codex" / "hooks.json").is_file()
    for name in ("code-reviewer.toml", "evolution-runner.toml"):
        assert (ROOT / ".codex" / "agents" / name).is_file(), name
    assert list((ROOT / "agents" / "skills").glob("*/SKILL.md"))


def test_real_repo_hooks_json_matches_protocol_schema():
    """仓库自带的 hooks.json 也必须过 schema，否则装出去就是死配置。"""
    schema = json.loads(HOOK_SCHEMA.read_text(encoding="utf-8"))
    hooks = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    Draft7Validator(schema).validate(hooks)


def test_hook_schema_is_stricter_than_codex():
    """schema 顶层只允许 description / hooks，未知字段必须判错。"""
    schema = json.loads(HOOK_SCHEMA.read_text(encoding="utf-8"))
    assert schema.get("additionalProperties") is False
    assert set(schema["properties"]) == {"description", "hooks"}


def test_real_global_template_carries_markers_and_placeholder():
    """全局入口模板要带标记块与路径占位符，缺一个就装不出可用的入口。"""
    text = (ROOT / "docs" / "global-agents.template.md").read_text(encoding="utf-8")
    assert BLOCK_START in text
    assert BLOCK_END in text
    assert "{{IDEA_HAMMER_HOME}}" in text


def test_real_repo_hooks_have_no_self_invented_fields():
    """框架自造的 $version / events / mode 协议 Codex 从来不加载，必须彻底清掉。"""
    text = (ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8")
    for banned in ('"$version"', '"events"', '"mode"'):
        assert banned not in text, f"hooks.json 里还有 Codex 不认的字段 {banned}"


def test_installed_skill_count_matches_repo():
    """仓库里能装成技能的目录数，与文档里宣称的数字要对得上。"""
    skills = [
        p
        for p in (ROOT / "agents" / "skills").iterdir()
        if p.is_dir()
        and p.name != "_template"
        and (p / "SKILL.md").is_file()
    ]
    assert len(skills) == 12, f"实际 {len(skills)} 个 skill，README 写的是 12"
