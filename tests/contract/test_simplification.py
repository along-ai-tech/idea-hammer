"""契约测试 — simplification/ 10 条原则 + check_simplicity.py 校验工具。"""

from pathlib import Path

import pytest


SIMPLIFICATION_DIR = Path(__file__).parent.parent.parent / "agents" / "skills" / "_engineering-constraints" / "simplification"


# 10 条原则文件必须存在
REQUIRED_FILES = [
    "single-responsibility.md",
    "yagni.md",
    "abstraction-timing.md",
    "file-and-function-size.md",
    "naming-is-documentation.md",
    "no-comments-by-default.md",
    "dead-code-deletion.md",
    "dependency-minimalism.md",  # 8
    "pure-functions.md",        # 9
    "idempotency.md",            # 10
]


@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_required_principle_file_exists(filename):
    """10 条原则文件必须存在。"""
    path = SIMPLIFICATION_DIR / filename
    assert path.exists(), f"{filename} 不存在"
    content = path.read_text(encoding="utf-8")
    assert len(content) > 100, f"{filename} 内容太短（< 100 字符）"


def test_principle_count_is_10():
    """simplification/ 必须有 10 条原则（不含 README）。"""
    files = [f.name for f in SIMPLIFICATION_DIR.glob("*.md") if f.name != "README.md"]
    assert len(files) == 10, f"应有 10 条，实际 {len(files)} 条：{files}"


def test_readme_mentions_10_principles():
    """README 必须声明 10 条原则。"""
    readme = (SIMPLIFICATION_DIR / "README.md").read_text(encoding="utf-8")
    assert "10 条" in readme or "10 条原则" in readme


def test_ai_specific_antipatterns_in_readme():
    """README 必须包含 AI 写代码特有反模式段。"""
    readme = (SIMPLIFICATION_DIR / "README.md").read_text(encoding="utf-8")
    assert "AI 写代码特有的反模式" in readme


def test_check_simplicity_script_exists():
    """check_simplicity.py 必须存在 + 可执行。"""
    script = Path(__file__).parent.parent.parent / "scripts" / "check_simplicity.py"
    assert script.exists(), "scripts/check_simplicity.py 不存在"


def test_check_simplicity_validates_own_scripts():
    """check_simplicity.py 跑整个 scripts/ 应该没有错误。"""
    import subprocess
    import sys
    script = Path(__file__).parent.parent.parent / "scripts" / "check_simplicity.py"
    scripts_dir = script.parent
    result = subprocess.run(
        [sys.executable, str(script), str(scripts_dir), "--recursive"],
        capture_output=True, text=True,
    )
    # 应通过（0 错误）
    assert result.returncode == 0, f"check_simplicity failed:\n{result.stdout}\n{result.stderr}"


def test_each_principle_has_principle_section():
    """每条原则文件必须有 '## ' 标题段（说明结构完整）。"""
    for filename in REQUIRED_FILES:
        path = SIMPLIFICATION_DIR / filename
        content = path.read_text(encoding="utf-8")
        # 至少 2 个 ## 段
        h2_count = sum(1 for line in content.splitlines() if line.startswith("## "))
        assert h2_count >= 2, f"{filename} 缺 ## 段（只有 {h2_count} 个）"


def test_each_principle_has_antipatterns():
    """每条原则文件必须有"反模式"段（不只是规则）。"""
    for filename in REQUIRED_FILES:
        path = SIMPLIFICATION_DIR / filename
        content = path.read_text(encoding="utf-8")
        assert "反模式" in content or "❌" in content, f"{filename} 缺反模式段"


def test_simplification_files_present():
    """simplification/ 目录有 10 原则 + 1 README（不依赖 git tracked 状态）。"""
    files = list(SIMPLIFICATION_DIR.glob("*.md"))
    assert len(files) == 11, f"应有 11 个 .md（10 原则 + README），实际 {len(files)}"
