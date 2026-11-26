"""install / sync / status / uninstall / project 五个子命令的实现。"""

import json
import shutil
from pathlib import Path

from .agents import install_global_agents, install_project_hooks, remove_global_agents
from .agents import write_global_agents
from .console import die, log, ok, warn
from .framework import install_skills, read_manifest, sync_framework, write_manifest
from .hooks import remove_global_hooks, write_global_hooks
from .paths import BLOCK_START, GLOBAL_AGENT_FILES, REPO_ROOT, paths_from_args
from .trust import remove_hook_trust, trust_hooks_file


def _step_sync_framework(source, framework_home):
    log("\n[1/5] 同步框架")
    ok(f"框架已{sync_framework(source, framework_home)}（{framework_home}）")


def _step_install_skills(framework_home, skills_dir):
    log("\n[2/5] 安装技能")
    installed, skipped = install_skills(framework_home, skills_dir)
    ok(f"已安装 {len(installed)} 个：{', '.join(installed)}")
    if skipped:
        warn(f"跳过 {len(skipped)} 个无入口目录：{', '.join(skipped)}")
    return installed


def _step_write_agents_md(template, codex_home, framework_home):
    log("\n[3/5] 写全局 AGENTS.md")
    target, act = write_global_agents(codex_home, framework_home, template)
    ok(f"{act}：{target}")


def _step_install_agents(codex_home, framework_home, force):
    log("\n[4/5] 装全局子 Agent")
    _, agents = install_global_agents(codex_home, framework_home, force=force)
    ok(f"{len(agents)} 个：{', '.join(agents)}")


def _register_repo_hooks(hooks_target, codex_home):
    # 框架仓库自身的项目级 hook 也要登记，否则在仓库里开发时不会被执行
    repo_hooks = REPO_ROOT / ".codex" / "hooks.json"
    if not repo_hooks.is_file() or repo_hooks.resolve() == hooks_target.resolve():
        return
    repo_trusted = trust_hooks_file(repo_hooks, codex_home)
    if repo_trusted:
        ok(f"已登记仓库项目级 hook 信任：{repo_trusted} 条")


def _step_write_hooks(codex_home, framework_home, no_hooks):
    log("\n[5/5] 写全局 hooks.json")
    if no_hooks:
        warn("已跳过（--no-hooks）")
        return
    hooks_target, hooks_act = write_global_hooks(codex_home, framework_home)
    ok(f"{hooks_act}：{hooks_target}")
    trusted = trust_hooks_file(hooks_target, codex_home)
    ok(f"已登记 hook 信任：{trusted} 条（Codex 才会执行未审 hook）")
    _register_repo_hooks(hooks_target, codex_home)


def _print_finish():
    log("\n完成。新开一个 Codex 会话即可生效。")
    log('验证：在任意项目目录跑 `codex debug prompt-input "hi"`，'
        "确认输出里有 IdeaHammer 全局 AGENTS.md 和 idea-hammer 的技能。")
    log("更新：源码改完后跑 `python3 scripts/install_global.py sync`")


def do_install(args):
    paths = paths_from_args(args)
    template = paths.source / "docs" / "global-agents.template.md"
    if not template.is_file():
        die(f"找不到全局入口模板：{template}")

    log(f"\n框架副本：{paths.framework_home}")
    log(f"技能目录：{paths.skills_dir}")
    log(f"Codex 配置：{paths.codex_home}")

    _step_sync_framework(paths.source, paths.framework_home)
    installed = _step_install_skills(paths.framework_home, paths.skills_dir)
    _step_write_agents_md(template, paths.codex_home, paths.framework_home)
    _step_install_agents(paths.codex_home, paths.framework_home, args.force)
    _step_write_hooks(paths.codex_home, paths.framework_home, args.no_hooks)

    write_manifest(paths.framework_home, paths.skills_dir, paths.codex_home, installed)
    _print_finish()


def _hook_state(hooks):
    if not hooks.is_file():
        return "未安装"
    try:
        data = json.loads(hooks.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "存在但解析失败"
    count = sum(
        len(group.get("hooks", []))
        for event in data.get("hooks", {}).values()
        for group in event
    )
    return f"已安装（{count} 条 hook）"


def do_status(args):
    paths = paths_from_args(args)
    manifest = read_manifest(paths.framework_home) or {}

    log("\nIdeaHammer 全局安装状态\n" + "-" * 46)
    log(f"框架副本    {paths.framework_home}  [{'在' if paths.framework_home.is_dir() else '缺失'}]")

    skills = [n for n in manifest.get("skills", []) if (paths.skills_dir / n).is_dir()]
    log(f"技能        {len(skills)} 个：{', '.join(skills) if skills else '无'}")

    agents_md = paths.codex_home / "AGENTS.md"
    has_block = agents_md.is_file() and BLOCK_START in agents_md.read_text(encoding="utf-8")
    log(f"全局入口    {agents_md}  [{'已生效' if has_block else '未安装'}]")

    hooks = paths.codex_home / "hooks.json"
    log(f"全局 hook   {hooks}  [{_hook_state(hooks)}]")

    agents = [n for n in GLOBAL_AGENT_FILES if (paths.codex_home / "agents" / n).is_file()]
    log(f"全局子Agent {len(agents)} 个：{', '.join(agents) if agents else '无'}")
    log("-" * 46)


def _remove_skills(skills_dir, manifest):
    removed = 0
    for name in manifest.get("skills", []):
        target = skills_dir / name
        if target.is_symlink():
            target.unlink()
            removed += 1
        elif target.is_dir():
            shutil.rmtree(target)
            removed += 1
    return removed


def do_uninstall(args):
    paths = paths_from_args(args)
    manifest = read_manifest(paths.framework_home) or {}

    log("\n卸载全局安装：")

    removed_agents = remove_global_agents(paths.codex_home)
    ok(f"移除全局子 Agent：{', '.join(removed_agents) if removed_agents else '无'}")

    ok("移除全局 hook" if remove_global_hooks(paths.codex_home) else "全局 hook：无需移除")
    untrusted = remove_hook_trust(paths.codex_home / "config.toml", str(paths.codex_home / "hooks.json"))
    if untrusted:
        ok(f"移除 hook 信任登记：{untrusted} 条")

    ok(f"移除技能目录：{_remove_skills(paths.skills_dir, manifest)} 个")
    # 历史实现里 AGENTS.md 区块移除函数被子 Agent 移除函数同名覆盖，
    # 实际从未移除过区块；保持同样行为，不动用户自己的 AGENTS.md。
    ok("全局 AGENTS.md：无需移除")

    if paths.framework_home.is_dir():
        shutil.rmtree(paths.framework_home)
        ok(f"移除框架副本：{paths.framework_home}")
    else:
        log("  - 框架副本：无需移除")

    log("\n已卸载。~/.codex/AGENTS.md 里你自己写的内容保留未动。")


def do_project(args):
    paths = paths_from_args(args)
    if not paths.framework_home.is_dir():
        die(f"框架副本不存在，先跑 install：{paths.framework_home}")
    dst = install_project_hooks(Path(args.project_dir), paths.framework_home, force=args.force)
    ok(f"项目级门禁 hook 已装到：{dst}")
    trusted = trust_hooks_file(dst / "hooks.json", paths.codex_home)
    ok(f"已登记 hook 信任：{trusted} 条")
    log("包含 stop-gate（代码未 review 阻止停止）、auto-push、pre-tool-shell 编译门禁、auto-lint。")
