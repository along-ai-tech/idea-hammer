"""全局 AGENTS.md、全局子 Agent 与项目级门禁 hook。"""

import json
import os
import shutil

from .console import die, warn
from .paths import BLOCK_END, BLOCK_START, GLOBAL_AGENT_FILES


def write_global_agents(codex_home, framework_home, template_path):
    """把方法论入口写进 ~/.codex/AGENTS.md，保留用户原有内容。"""
    target = codex_home / "AGENTS.md"
    block = template_path.read_text(encoding="utf-8").replace(
        "{{IDEA_HAMMER_HOME}}", str(framework_home)
    )

    existing = target.read_text(encoding="utf-8") if target.exists() else ""

    if BLOCK_START in existing and BLOCK_END in existing:
        head = existing.split(BLOCK_START)[0]
        tail = existing.split(BLOCK_END, 1)[1]
        updated = f"{head}{block}{tail}"
        action = "已更新"
    else:
        prefix = existing.rstrip() + "\n\n" if existing.strip() else ""
        updated = prefix + block
        action = "已追加" if existing.strip() else "已创建"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(updated, encoding="utf-8")
    return target, action


def install_global_agents(codex_home, framework_home, force=False):
    src_dir = framework_home / ".codex" / "agents"
    dst_dir = codex_home / "agents"
    dst_dir.mkdir(parents=True, exist_ok=True)

    installed = []
    for name in GLOBAL_AGENT_FILES:
        src = src_dir / name
        if not src.is_file():
            warn(f"缺少 {src}，跳过")
            continue
        dst = dst_dir / name
        if dst.exists() and not force:
            if dst.read_bytes() == src.read_bytes():
                installed.append(name)
                continue
            warn(f"{dst} 已存在且内容不同，跳过（要覆盖用 --force）")
            continue
        shutil.copy2(src, dst)
        installed.append(name)
    return dst_dir, installed


def remove_global_agents(codex_home):
    dst_dir = codex_home / "agents"
    removed = []
    for name in GLOBAL_AGENT_FILES:
        dst = dst_dir / name
        if dst.is_file():
            dst.unlink()
            removed.append(name)
    return removed


def _copy_project_scripts(framework_home, hooks_dst, force):
    if hooks_dst.exists() and force:
        shutil.rmtree(hooks_dst)
    hooks_dst.mkdir(parents=True, exist_ok=True)
    for script in (framework_home / ".codex" / "hooks").glob("*.sh"):
        shutil.copy2(script, hooks_dst / script.name)
        os.chmod(hooks_dst / script.name, 0o755)


def _copy_project_agents(framework_home, agents_dst):
    agents_dst.mkdir(parents=True, exist_ok=True)
    for name in GLOBAL_AGENT_FILES:
        src = framework_home / ".codex" / "agents" / name
        if src.is_file():
            shutil.copy2(src, agents_dst / name)


def _write_project_hooks_json(framework_home, dst):
    hooks_json = json.loads(
        (framework_home / ".codex" / "hooks.json").read_text(encoding="utf-8")
    )
    (dst / "hooks.json").write_text(
        json.dumps(hooks_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _ensure_evolution_files(dst):
    evolution = dst / "evolution"
    evolution.mkdir(parents=True, exist_ok=True)
    signals = evolution / "signals.jsonl"
    if not signals.exists():
        signals.touch()
    proposals = evolution / "proposals.md"
    if not proposals.exists():
        proposals.write_text(
            "# 进化建议\n\n## 待审阅\n\n## 已消化日志\n", encoding="utf-8"
        )


def install_project_hooks(project_dir, framework_home, force=False):
    """把全套门禁 hook 装进单个项目：stop-gate 拦截未审代码、auto-push、
    pre-tool-shell 编译门禁、auto-lint。这些会改变项目行为，必须显式开启。"""
    project_dir = project_dir.resolve()
    if not project_dir.is_dir():
        die(f"项目目录不存在：{project_dir}")

    dst = project_dir / ".codex"
    dst.mkdir(parents=True, exist_ok=True)
    _copy_project_scripts(framework_home, dst / "hooks", force)
    _copy_project_agents(framework_home, dst / "agents")
    # 项目级 hook 的进化目录属于项目自己，不注入 IDEA_HAMMER_ROOT，
    # 让脚本用 git 根定位 <项目>/.codex/evolution。
    _write_project_hooks_json(framework_home, dst)
    _ensure_evolution_files(dst)
    return dst
