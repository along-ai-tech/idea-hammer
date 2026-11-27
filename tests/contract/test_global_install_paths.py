"""契约测试 — 全局安装器的路径推导与卸载。

路径推导是本次改动最容易出错、后果最静默的地方：装错位置不报错，
只是"用不上"。所以按 Codex 自己的规则逐条锁住。

卸载同理——框架副本删了但全局入口区块还在，等于让每个新会话去读一个空指针。
"""

from pathlib import Path

from _install_fixtures import BLOCK_START, empty_args, home, source  # noqa: F401
from _install_fixtures import run_installer


def test_default_paths_follow_codex_rules(monkeypatch, home):
    """默认路径必须与 Codex 自己的规则一致——对不上就静默失效。"""
    from global_install.paths import paths_from_args

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("CODEX_HOME", raising=False)

    p = paths_from_args(empty_args())
    assert p.codex_home == home / ".codex"
    assert p.framework_home == home / ".codex" / "idea-hammer"
    assert p.skills_dir == home / ".agents" / "skills"


def test_codex_home_env_moves_config_but_not_skills(monkeypatch, home, tmp_path):
    """CODEX_HOME 决定配置目录；技能目录仍按 Codex 的规则留在 $HOME/.agents/skills。

    Codex 只读 $HOME/.agents/skills。若把技能跟着 CODEX_HOME 走，
    用自定义 CODEX_HOME 的用户会整套技能静默失效。
    """
    from global_install.paths import paths_from_args

    custom = tmp_path / "custom-codex"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("CODEX_HOME", str(custom))

    p = paths_from_args(empty_args())
    assert p.codex_home == custom.resolve()
    assert p.framework_home == custom.resolve() / "idea-hammer"
    assert p.skills_dir == home / ".agents" / "skills"


def test_explicit_codex_home_overrides_env(monkeypatch, home, tmp_path):
    """显式 --codex-home 优先于 CODEX_HOME 环境变量。"""
    from global_install.paths import paths_from_args

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "ignored"))
    explicit = tmp_path / "explicit"

    p = paths_from_args(empty_args(codex_home=str(explicit)))
    assert p.codex_home == explicit.resolve()


def test_explicit_framework_home_overrides_anchor(source, home, tmp_path):
    """显式 --framework-home 优先于推导值。"""
    codex_home = tmp_path / "codex"
    framework_home = tmp_path / "elsewhere" / "framework"
    code, out, err = run_installer(
        source, home, "--framework-home", str(framework_home), codex_home=codex_home
    )
    assert code == 0, out + err
    assert (framework_home / "AGENTS.md").is_file()
    assert not (codex_home / "idea-hammer").exists()


def test_isolated_install_lands_only_under_fake_home(source, home):
    """隔离安装不许在 Codex 家目录之外落任何东西。"""
    codex_home = home / ".codex"
    code, out, err = run_installer(source, home, codex_home=codex_home)
    assert code == 0, out + err

    landed = sorted(p.name for p in home.iterdir() if p.name != "Library")
    assert landed == [".agents", ".codex"]
    assert (home / ".codex" / "idea-hammer" / "AGENTS.md").is_file()
    assert (home / ".agents" / "skills" / "demo-skill").is_dir()

    # 安装器自报的框架副本路径必须落在假 HOME 里
    reported = next(
        line for line in out.splitlines() if line.startswith("框架副本：")
    ).split("：", 1)[1]
    assert Path(reported).is_relative_to(home), reported


def test_uninstall_removes_framework_and_agents_block(source, home):
    """卸载要连框架副本和全局入口区块一起摘掉，用户的自有内容保留。"""
    code, out, err = run_installer(source, home)
    assert code == 0, out + err

    agents_md = home / ".codex" / "AGENTS.md"
    agents_md.write_text(
        "# 我自己的偏好\n\n" + agents_md.read_text(encoding="utf-8"), encoding="utf-8"
    )

    code, out, err = run_installer(source, home, command="uninstall")
    assert code == 0, out + err

    assert not (home / ".codex" / "idea-hammer").exists(), "框架副本没删"
    text = agents_md.read_text(encoding="utf-8")
    assert BLOCK_START not in text, "全局入口区块没摘，指向已不存在的框架路径"
    assert "我自己的偏好" in text


def test_uninstall_strips_our_hooks_but_keeps_user_hooks(source, home):
    """卸载只摘 IdeaHammer 的 hook，用户自己写的 hook 保留。"""
    import json

    code, out, err = run_installer(source, home)
    assert code == 0, out + err

    hooks_path = home / ".codex" / "hooks.json"
    data = json.loads(hooks_path.read_text(encoding="utf-8"))
    data["hooks"]["SessionStart"].append(
        {"hooks": [{"type": "command", "command": "/usr/local/bin/my-own-hook.sh"}]}
    )
    hooks_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    code, out, err = run_installer(source, home, command="uninstall")
    assert code == 0, out + err

    left = json.loads(hooks_path.read_text(encoding="utf-8"))
    commands = [
        handler["command"]
        for groups in left.get("hooks", {}).values()
        for group in groups
        for handler in group["hooks"]
    ]
    assert "/usr/local/bin/my-own-hook.sh" in commands, "用户自己的 hook 被误删"
    assert not any("idea-hammer" in cmd for cmd in commands), "IdeaHammer 的 hook 没摘干净"


def test_uninstall_without_manifest_says_so_instead_of_pretending(source, home):
    """找不到安装清单要说清楚，不能静默什么都没删还报"已卸载"。"""
    code, out, err = run_installer(source, home, command="uninstall")
    assert code == 0, out + err
    assert "找不到安装清单" in out
    assert "已卸载" not in out
