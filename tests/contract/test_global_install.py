"""契约测试 — 全局安装器：装齐 / 可重复。

安装器是"所有项目都能用上这套方法论"的落地入口。这里锁两条：

  1. 装齐 —— 框架副本 / 技能 / 全局入口 / 子 Agent / hook 五类产物一个不少
  2. 可重复 —— 重复安装不产生重复内容，sync 会剪掉源码已删掉的文件

路径推导见 test_global_install_paths.py，卸载见同文件，真实仓库静态资产见
test_global_install_repo.py。
"""

import json

from _install_fixtures import BLOCK_END, BLOCK_START, home, source  # noqa: F401
from _install_fixtures import handler_count, run_installer, trust_entries


def test_install_writes_all_five_artifacts(source, home):
    """五类产物必须一个不少：框架副本、技能、全局入口、子 Agent、hook。"""
    codex_home = home / ".codex"
    code, out, err = run_installer(source, home, codex_home=codex_home)
    assert code == 0, out + err

    assert (codex_home / "idea-hammer" / "AGENTS.md").is_file(), "框架副本没同步"
    assert (home / ".agents" / "skills" / "demo-skill" / "SKILL.md").is_file(), "技能没装"
    assert (codex_home / "AGENTS.md").is_file(), "全局入口没写"
    assert (codex_home / "agents" / "code-reviewer.toml").is_file(), "子 Agent 没装"
    assert (codex_home / "hooks.json").is_file(), "全局 hook 没写"
    assert (codex_home / "config.toml").is_file(), "hook 信任没登记"


def test_every_hook_handler_is_trusted(source, home):
    """Codex 只执行登记过 trusted_hash 的 handler，少一条就少一条能力。"""
    codex_home = home / ".codex"
    code, out, err = run_installer(source, home, codex_home=codex_home)
    assert code == 0, out + err

    global_handlers = handler_count(codex_home / "hooks.json")
    source_handlers = handler_count(source / ".codex" / "hooks.json")
    entries = trust_entries(codex_home / "config.toml")
    assert len(entries) == global_handlers + source_handlers


def test_template_skill_is_not_installed(source, home):
    """_template 是脚手架，装进去会被当成真技能，污染触发匹配。"""
    code, out, err = run_installer(source, home)
    assert code == 0, out + err
    assert not (home / ".agents" / "skills" / "_template").exists()


def test_framework_scripts_are_linked_into_skills(source, home):
    """技能里的 scripts/xxx.py 要能找到框架脚本，无论按技能目录还是项目根解析。"""
    code, out, err = run_installer(source, home)
    assert code == 0, out + err
    link = home / ".agents" / "skills" / "demo-skill" / "scripts" / "session.py"
    assert link.is_symlink()


def test_manifest_lists_installed_skills(source, home):
    """安装清单要记下装了什么，status / uninstall 都靠它。"""
    code, out, err = run_installer(source, home)
    assert code == 0, out + err
    manifest = json.loads(
        (home / ".codex" / "idea-hammer" / ".install-manifest.json").read_text(encoding="utf-8")
    )
    assert "demo-skill" in manifest["skills"]
    assert "_template" not in manifest["skills"]


def test_reinstall_does_not_duplicate_agents_block(source, home):
    """重复安装不能让全局入口的方法论区块变成两份。"""
    code, out, err = run_installer(source, home)
    assert code == 0, out + err
    code, out, err = run_installer(source, home)
    assert code == 0, out + err

    text = (home / ".codex" / "AGENTS.md").read_text(encoding="utf-8")
    assert text.count(BLOCK_START) == 1
    assert text.count(BLOCK_END) == 1


def test_reinstall_preserves_user_content_in_agents_md(source, home):
    """用户自己写的全局 AGENTS.md 内容不能被安装器吃掉。"""
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    agents_md = codex_home / "AGENTS.md"
    agents_md.write_text("# 我自己的偏好\n\n始终用中文。\n", encoding="utf-8")

    code, out, err = run_installer(source, home, codex_home=codex_home)
    assert code == 0, out + err

    text = agents_md.read_text(encoding="utf-8")
    assert "始终用中文。" in text
    assert BLOCK_START in text


def test_sync_prunes_files_removed_from_source(source, home):
    """sync 的语义是镜像源码：源码删掉的文件，副本里也必须消失。"""
    code, out, err = run_installer(source, home)
    assert code == 0, out + err

    framework_home = home / ".codex" / "idea-hammer"
    orphan = framework_home / "docs" / "orphan.md"
    orphan.write_text("旧文件\n", encoding="utf-8")
    assert orphan.is_file()

    code, out, err = run_installer(source, home)
    assert code == 0, out + err
    assert not orphan.exists(), "sync 没剪掉源码已无的文件"
