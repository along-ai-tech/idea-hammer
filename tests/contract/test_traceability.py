"""契约测试 — 需求追踪规范、模板与校验脚本。"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SCRIPT = ROOT / "scripts" / "check_traceability.py"
TRACE_DOC = ROOT / "agents" / "skills" / "_traceability" / "README.md"
SKILLS = ROOT / "agents" / "skills"

SPEC = """# Product Spec

## 3. 用户任务

| 编号 | 用户任务 | 用户类型 | 优先级 |
|---|---|---|---|
| TASK-001 | 发布文章 | 作者 | P0 |

## 5. 功能需求

### REQ-001: 发布文章

**优先级：** P0
**关联任务：** TASK-001
**关联流程：** FLOW-001

**验收标准：**
- [ ] AC-001-01: 提交后文章可见
- [ ] AC-001-02: 空标题返回 422

## 4. 用户流程

### FLOW-001: 发布文章

**关联任务：** TASK-001
"""

PLAN = """# DEV-PLAN

## Phase 1: 文章创建

### DT-001 · 文章 API

**关联需求：** REQ-001 / AC-001-01 / AC-001-02
"""

TESTS = """# @trace TEST-001 REQ-001/AC-001-01
def test_create_post():
    assert True

# @trace TEST-002 REQ-001/AC-001-02
def test_reject_empty_title():
    assert True
"""

RELEASE = """{
  "version": "v1.0.0",
  "requirements": ["REQ-001"],
  "tests": {"total": 2, "passed": 2, "ids": ["TEST-001", "TEST-002"]}
}"""


def _project(tmp_path, tests=TESTS, release=RELEASE, plan=PLAN):
    (tmp_path / "Product-Spec.md").write_text(SPEC, encoding="utf-8")
    (tmp_path / "DEV-PLAN.md").write_text(plan, encoding="utf-8")
    (tmp_path / "tests").mkdir()
    if tests is not None:
        (tmp_path / "tests" / "test_posts.py").write_text(tests, encoding="utf-8")
    if release is not None:
        (tmp_path / "RELEASE.json").write_text(release, encoding="utf-8")
    return tmp_path


def _run(project, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--project", str(project), *args],
        capture_output=True, text=True,
    )


def test_trace_doc_covers_chain():
    text = TRACE_DOC.read_text(encoding="utf-8")
    for token in ("REQ-", "AC-", "DT-", "TEST-", "RELEASE.json", "--impact"):
        assert token in text, f"追踪规范缺 {token}"


def test_valid_project_passes(tmp_path):
    result = _run(_project(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "追踪链路通过" in result.stdout


def test_missing_test_mapping_fails(tmp_path):
    result = _run(_project(tmp_path, tests=None))
    assert result.returncode == 1
    assert "REQ-001 未被任何测试 TEST 覆盖" in result.stdout


def test_p0_requirement_missing_from_release_fails(tmp_path):
    release = RELEASE.replace('"REQ-001"', "")
    result = _run(_project(tmp_path, release=release))
    assert result.returncode == 1
    assert "REQ-001 未进入发布清单" in result.stdout


def test_impact_lists_tasks_and_tests(tmp_path):
    result = _run(_project(tmp_path), "--impact", "REQ-001")
    assert result.returncode == 0
    assert "DT-001" in result.stdout and "TEST-001" in result.stdout


def test_write_matrix(tmp_path):
    matrix = tmp_path / "TRACEABILITY.md"
    result = _run(_project(tmp_path), "--write", str(matrix))
    assert result.returncode == 0
    text = matrix.read_text(encoding="utf-8")
    assert "| REQ-001 | P0 | TASK-001 | DT-001 |" in text
    assert "AC-001-01" in text


def test_scope_exempt_task_passes_strict(tmp_path):
    plan = PLAN + "\n### DT-002 · 项目脚手架\n\n**关联需求：** 无（范围外：脚手架）\n"
    result = _run(_project(tmp_path, plan=plan), "--strict")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "未关联任何 REQ" not in result.stdout


def test_templates_and_ci_are_wired():
    spec_tpl = (SKILLS / "product-spec-builder" / "templates" / "product-spec-template.md").read_text(encoding="utf-8")
    plan_tpl = (SKILLS / "dev-planner" / "templates" / "dev-plan-template.md").read_text(encoding="utf-8")
    changelog = (SKILLS / "product-spec-builder" / "templates" / "changelog-template.md").read_text(encoding="utf-8")
    release = (SKILLS / "release-builder" / "contracts" / "output.schema.json").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "AC-001-01" in spec_tpl
    assert "DT-001" in plan_tpl and "关联需求" in plan_tpl
    assert "影响追踪" in changelog
    assert '"requirements"' in release and "TEST-" in release
    assert "check_traceability.py" in ci
