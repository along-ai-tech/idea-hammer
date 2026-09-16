"""共享 fixtures：所有 skill 的路径和元数据。"""

import re
from pathlib import Path

import pytest


SKILLS_ROOT = Path(__file__).parent.parent.parent / "agents" / "skills"


def _all_skills():
    """返回所有 skill 目录名（排除 _template 和 _engineering-constraints）。"""
    if not SKILLS_ROOT.exists():
        return []
    skills = []
    for p in sorted(SKILLS_ROOT.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("_"):
            continue  # _template / _engineering-constraints
        if (p / "SKILL.md").exists():
            skills.append(p.name)
    return skills


ALL_SKILLS = _all_skills()


@pytest.fixture(params=ALL_SKILLS)
def skill_name(request):
    return request.param


@pytest.fixture
def skill_dir(skill_name):
    return SKILLS_ROOT / skill_name


@pytest.fixture
def skill_md(skill_dir):
    return (skill_dir / "SKILL.md").read_text(encoding="utf-8")


@pytest.fixture
def skill_md_lines(skill_md):
    return skill_md.splitlines()


@pytest.fixture
def frontmatter(skill_md):
    """解析 YAML frontmatter。"""
    import yaml
    m = re.match(r"^---\n(.*?)\n---\n", skill_md, re.DOTALL)
    if not m:
        return None
    return yaml.safe_load(m.group(1))
