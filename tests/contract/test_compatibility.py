"""契约测试 — compatibility/ 6 条原则 + 接入检查。"""

import re
import subprocess
import sys
from pathlib import Path

import pytest


COMPAT_DIR = Path(__file__).parent.parent.parent / "agents" / "skills" / "_engineering-constraints" / "compatibility"


REQUIRED_FILES = [
    "blast-radius.md",
    "backward-compatibility.md",
    "feature-flag.md",
    "data-migration.md",
    "api-versioning.md",
    "completeness-delivery.md",
]


@pytest.mark.parametrize("filename", REQUIRED_FILES)
def test_required_principle_file_exists(filename):
    """6 条原则文件必须存在。"""
    path = COMPAT_DIR / filename
    assert path.exists(), f"{filename} 不存在"
    content = path.read_text(encoding="utf-8")
    assert len(content) > 100, f"{filename} 内容太短"


def test_compat_files_present():
    """compatibility/ 必须有 6 原则 + README。"""
    files = list(COMPAT_DIR.glob("*.md"))
    assert len(files) == 7, f"应有 7 个 .md（6 原则 + README），实际 {len(files)}"


def test_readme_links_to_6_principles():
    """README 必须列出全部 6 个原则文件。"""
    readme = (COMPAT_DIR / "README.md").read_text(encoding="utf-8")
    for f in ["blast-radius.md", "completeness-delivery.md", "backward-compatibility.md",
              "data-migration.md", "api-versioning.md", "feature-flag.md"]:
        assert f in readme, f"README 未引用 {f}"


def test_blast_radius_covers_4_categories():
    """blast-radius 必须涵盖 4 类外部世界。"""
    content = (COMPAT_DIR / "blast-radius.md").read_text(encoding="utf-8")
    for cat in ["数据", "API", "用户", "依赖"]:
        assert cat in content, f"blast-radius 缺 {cat}"


def test_data_migration_covers_snapshot_pattern():
    """data-migration 必须含 snapshot 模式（订单场景核心）。"""
    content = (COMPAT_DIR / "data-migration.md").read_text(encoding="utf-8")
    assert "Snapshot" in content or "snapshot" in content
    assert "order_items" in content or "订单" in content


def test_completeness_delivery_has_8_checklist_items():
    """completeness-delivery 必须有 8 项 Checklist。"""
    content = (COMPAT_DIR / "completeness-delivery.md").read_text(encoding="utf-8")
    # 8 项: 1. 代码 2. 数据 3. API 4. 用户 5. 依赖 6. 文档 7. 测试 8. 监控+回滚
    for cat in ["代码", "数据", "API", "用户", "依赖", "文档", "测试", "监控"]:
        assert cat in content, f"completeness-delivery 缺 {cat} 项"


def test_backward_compatibility_has_expand_contract():
    """backward-compatibility 必须含 Expand-Contract 模式。"""
    content = (COMPAT_DIR / "backward-compatibility.md").read_text(encoding="utf-8")
    assert "Expand-Contract" in content or "Expand" in content


def test_api_versioning_has_3_options():
    """api-versioning 必须含 3 种版本控制方式。"""
    content = (COMPAT_DIR / "api-versioning.md").read_text(encoding="utf-8")
    assert "URL" in content
    assert "Header" in content
    assert "无版本" in content


def test_feature_flag_has_4_types():
    """feature-flag 必须含 4 种 Flag 类型。"""
    content = (COMPAT_DIR / "feature-flag.md").read_text(encoding="utf-8")
    for ftype in ["Release Flag", "Experiment Flag", "Ops Flag", "Permission Flag"]:
        assert ftype in content, f"feature-flag 缺 {ftype}"


def test_dev_builder_links_compatibility():
    """dev-builder scope-and-modification.md 必须引用 compatibility/。"""
    sm = Path(__file__).parent.parent.parent / "agents" / "skills" / "dev-builder" / "principles" / "scope-and-modification.md"
    content = sm.read_text(encoding="utf-8")
    assert "compatibility" in content
    assert "blast-radius" in content


def test_code_review_checks_compatibility():
    """code-review stage2-checklist.md 必须加兼容性检查项。"""
    cl = Path(__file__).parent.parent.parent / "agents" / "skills" / "code-review" / "principles" / "stage2-checklist.md"
    content = cl.read_text(encoding="utf-8")
    assert "compatibility" in content
    assert "完整性交付" in content
    assert "Blast Radius" in content
