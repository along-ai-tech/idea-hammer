"""契约测试 — session.py 的 checkpoint / restore 能力。

Checkpoint ≠ Git Commit：前者是任务恢复信息，后者是代码版本快照。
restore 必须输出"需要重新核实什么"，因为 State 只能定位恢复位置，
不能代替对真实代码与执行结果的核查。
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent.parent
SCRIPT = ROOT / "scripts" / "session.py"


def _run(*args, path):
    """跑 session.py，返回 (returncode, stdout)。"""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args, "--path", str(path)],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip()


@pytest.fixture
def session_path(tmp_path):
    """一个空的 session.json 路径。"""
    p = tmp_path / "session.json"
    p.write_text(
        json.dumps(
            {"schema_version": "1.0", "current_phase": "phase_1", "current_task": "DT-001"},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return p


def test_session_script_exists():
    """session.py 必须存在。"""
    assert SCRIPT.exists(), "scripts/session.py 不存在"


def test_checkpoint_appends_record(session_path):
    """checkpoint 把恢复点追加进 checkpoints 数组。"""
    code, out = _run(
        "checkpoint",
        "--phase",
        "phase_3",
        "--task",
        "DT-004",
        "--commit",
        "abc1234",
        "--tests",
        '{"unit_test": "passed"}',
        "--next",
        "完成授权 API 集成测试",
        path=session_path,
    )
    assert code == 0, f"checkpoint 退出码 {code}: {out}"

    data = json.loads(session_path.read_text(encoding="utf-8"))
    cps = data.get("checkpoints")
    assert isinstance(cps, list) and len(cps) == 1, f"checkpoints 未写入: {cps}"

    cp = cps[0]
    assert cp["phase"] == "phase_3"
    assert cp["task"] == "DT-004"
    assert cp["git_commit"] == "abc1234"
    assert cp["tests"]["unit_test"] == "passed"
    assert cp["next_action"] == "完成授权 API 集成测试"
    assert cp.get("created_at"), "checkpoint 缺 created_at"


def test_checkpoint_appends_not_overwrites(session_path):
    """连续两次 checkpoint 不互相覆盖。"""
    for task in ("DT-001", "DT-002"):
        code, _ = _run("checkpoint", "--task", task, path=session_path)
        assert code == 0

    data = json.loads(session_path.read_text(encoding="utf-8"))
    assert len(data["checkpoints"]) == 2, "checkpoint 覆盖了历史记录"
    assert data["checkpoints"][0]["task"] == "DT-001"
    assert data["checkpoints"][1]["task"] == "DT-002"


def test_checkpoint_ids_are_unique(session_path):
    """同秒内连续 checkpoint 的 id 不能撞（id 是 schema 的 required 字段）。"""
    for task in ("DT-001", "DT-002"):
        code, _ = _run("checkpoint", "--task", task, path=session_path)
        assert code == 0

    data = json.loads(session_path.read_text(encoding="utf-8"))
    ids = [cp["id"] for cp in data["checkpoints"]]
    assert len(set(ids)) == len(ids), f"checkpoint id 冲突: {ids}"


def test_checkpoint_preserves_existing_fields(session_path):
    """checkpoint 不破坏 session 里已有的字段。"""
    _run("checkpoint", "--task", "DT-004", path=session_path)
    data = json.loads(session_path.read_text(encoding="utf-8"))
    assert data["current_phase"] == "phase_1"
    assert data["current_task"] == "DT-001"


def test_checkpoint_rejects_invalid_tests_json(session_path):
    """--tests 非法 JSON 时给可读提示，不吐裸 traceback。"""
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "checkpoint",
            "--task",
            "DT-004",
            "--tests",
            "not-json",
            "--path",
            str(session_path),
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0, "非法 --tests 应以非零码退出"
    assert "Traceback" not in proc.stderr, f"吐了裸 traceback:\n{proc.stderr}"
    assert "JSON" in proc.stdout or "JSON" in proc.stderr, "错误提示没说要什么格式"


def test_restore_returns_latest_checkpoint(session_path):
    """restore 返回最近一个 checkpoint 和恢复位置。"""
    _run("checkpoint", "--task", "DT-001", path=session_path)
    _run("checkpoint", "--task", "DT-002", path=session_path)

    code, out = _run("restore", path=session_path)
    assert code == 0, f"restore 退出码 {code}: {out}"

    data = json.loads(out)
    assert data["checkpoint"]["task"] == "DT-002"
    assert data["resume_at"] == "DT-002"


def test_restore_requires_verification_steps(session_path):
    """restore 必须输出需要重新核实的步骤（State 不代替核查）。"""
    _run("checkpoint", "--task", "DT-002", path=session_path)
    code, out = _run("restore", path=session_path)
    assert code == 0

    data = json.loads(out)
    steps = data.get("verify_required")
    assert isinstance(steps, list) and len(steps) >= 3, (
        f"restore 未给出核实清单: {steps}"
    )
    joined = " ".join(steps)
    assert "测试" in joined, "核实清单未提测试结果需重跑"


def test_restore_without_checkpoint_is_graceful(session_path):
    """没有 checkpoint 时 restore 不报错，给出降级指引。"""
    code, out = _run("restore", path=session_path)
    assert code == 0, f"restore 无 checkpoint 时应优雅退出: {out}"

    data = json.loads(out)
    assert data["checkpoint"] is None
    assert data.get("verify_required"), "无 checkpoint 时也应给核实清单"


def test_restore_without_session_file_fails_loudly(tmp_path):
    """session.json 整个不存在时 restore 要非零退出，否则 CI 冒烟会假绿。"""
    missing = tmp_path / "nope.json"
    code, out = _run("restore", path=missing)
    assert code != 0, "session.json 丢失时 restore 不该以 0 退出"
    assert "session.json" in out, f"提示没点明缺什么: {out}"


def test_restore_falls_back_to_session_task(session_path):
    """checkpoint 没带 task 时，resume_at 回落 session.current_task。"""
    _run("checkpoint", path=session_path)  # 不传 --task

    code, out = _run("restore", path=session_path)
    assert code == 0, f"restore 退出码 {code}: {out}"

    data = json.loads(out)
    assert data["resume_at"] == "DT-001", (
        f"恢复位置丢失，应回落到 session.current_task: {data['resume_at']}"
    )


def test_context_view_includes_latest_checkpoint(session_path):
    """启动精简版要带最近 checkpoint，否则恢复点丢失。"""
    _run("checkpoint", "--task", "DT-004", path=session_path)
    code, out = _run("context", path=session_path)
    assert code == 0

    data = json.loads(out)
    latest = data.get("latest_checkpoint")
    assert latest, "精简版缺 latest_checkpoint"
    assert latest["task"] == "DT-004"


def test_validate_still_passes_with_checkpoints(session_path):
    """加 checkpoint 后 validate 仍通过。"""
    _run("checkpoint", "--task", "DT-004", path=session_path)
    code, out = _run("validate", path=session_path)
    assert code == 0, f"validate 失败: {out}"

