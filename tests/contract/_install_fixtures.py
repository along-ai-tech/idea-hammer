"""全局安装器契约测试的共享 fixture 与 helper。

单独抽出来是为了让各测试文件守住 ≤300 行纪律。
所有用例都把 HOME 指向临时目录：万一路径推导回归，测试应该红在测试里，
而不是往用户真实的 ~/.agents/skills 里写。
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent.parent
INSTALLER = ROOT / "scripts" / "install_global.py"

BLOCK_START = "<!-- idea-hammer:global:start -->"
BLOCK_END = "<!-- idea-hammer:global:end -->"

sys.path.insert(0, str(ROOT / "scripts"))


def empty_args(**overrides):
    """构造一份全空的命令行参数集，供 paths_from_args 用。"""
    base = {"source": None, "codex_home": None, "framework_home": None, "skills_dir": None}
    base.update(overrides)
    return type("Args", (), base)()


def hooks_doc(script_a: str, script_b: str) -> dict:
    """一份最小但合法的 Codex hooks.json（两个事件各一条 handler）。"""
    return {
        "description": "测试用 hook",
        "hooks": {
            "UserPromptSubmit": [
                {"hooks": [{"type": "command", "command": script_a, "timeout": 5}]}
            ],
            "SessionStart": [
                {"hooks": [{"type": "command", "command": script_b, "timeout": 10}]}
            ],
        },
    }


@pytest.fixture
def home(tmp_path):
    """假的用户家目录。安装器的三条默认路径都从这里推导。"""
    h = tmp_path / "home"
    h.mkdir()
    return h


@pytest.fixture
def source(tmp_path):
    """一份最小可安装的源码树：模板 + 1 个真技能 + 1 个模板技能 + 2 个 hook。"""
    root = tmp_path / "src"
    root.mkdir()

    (root / "AGENTS.md").write_text("# 框架入口\n", encoding="utf-8")

    docs = root / "docs"
    docs.mkdir()
    (docs / "global-agents.template.md").write_text(
        f"{BLOCK_START}\nIDEA_HAMMER_HOME = {{{{IDEA_HAMMER_HOME}}}}\n{BLOCK_END}\n",
        encoding="utf-8",
    )

    skill = root / "agents" / "skills" / "demo-skill"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo-skill\n---\n", encoding="utf-8")

    template = root / "agents" / "skills" / "_template"
    template.mkdir(parents=True)
    (template / "SKILL.md").write_text("---\nname: <skill-name>\n---\n", encoding="utf-8")

    hooks_dir = root / ".codex" / "hooks"
    hooks_dir.mkdir(parents=True)
    for name in ("check-evolution.sh", "detect-feedback-signal.sh"):
        (hooks_dir / name).write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    (root / ".codex" / "hooks.json").write_text(
        json.dumps(
            hooks_doc(
                '"$ROOT/.codex/hooks/detect-feedback-signal.sh"',
                '"$ROOT/.codex/hooks/check-evolution.sh"',
            ),
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    agents_dir = root / ".codex" / "agents"
    agents_dir.mkdir(parents=True)
    for name in ("code-reviewer.toml", "evolution-runner.toml"):
        (agents_dir / name).write_text(f"# {name}\n", encoding="utf-8")

    scripts = root / "scripts"
    scripts.mkdir()
    (scripts / "session.py").write_text("print('ok')\n", encoding="utf-8")
    return root


def run_installer(source, home, *extra, command="install", codex_home=None):
    """跑安装器，返回 (returncode, stdout, stderr)。HOME 已被隔离到临时目录。"""
    env = dict(os.environ)
    env["HOME"] = str(home)
    env.pop("CODEX_HOME", None)
    cmd = [sys.executable, str(INSTALLER), command, "--source", str(source)]
    if codex_home is not None:
        cmd += ["--codex-home", str(codex_home)]
    cmd += list(extra)
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return proc.returncode, proc.stdout, proc.stderr


def trust_entries(config_path: Path) -> list:
    """从 config.toml 里读出所有 hook 信任表头。"""
    if not config_path.is_file():
        return []
    return [
        line.strip()
        for line in config_path.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("[hooks.state.")
    ]


def handler_count(hooks_path: Path) -> int:
    """数一份 hooks.json 里有多少条 handler。"""
    data = json.loads(hooks_path.read_text(encoding="utf-8"))
    return sum(
        len(group["hooks"]) for groups in data.get("hooks", {}).values() for group in groups
    )
