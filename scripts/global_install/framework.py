"""框架副本同步、技能安装与安装清单。"""

import json
import shutil
import time
from pathlib import Path

from .console import die
from .paths import (
    EXCLUDE_NAMES,
    EXCLUDE_SUFFIXES,
    MANIFEST_NAME,
    SHARED_SKILL_DIRS,
    SKIP_SKILL_DIRS,
)


def _is_excluded(item):
    return item.name in EXCLUDE_NAMES or item.suffix in EXCLUDE_SUFFIXES


def _ignore(_dirpath, names):
    ignored = set()
    for name in names:
        if name in EXCLUDE_NAMES or Path(name).suffix in EXCLUDE_SUFFIXES:
            ignored.add(name)
    return ignored


def _copy_entry(src_item, dst_item):
    if src_item.is_dir():
        dst_item.mkdir(exist_ok=True)
        _walk(src_item, dst_item)
        return
    if dst_item.is_symlink():
        dst_item.unlink()
    shutil.copy2(src_item, dst_item, follow_symlinks=False)


def _prune_extras(dst_dir, kept):
    """删掉目标目录里源码已经没有了的文件。"""
    for item in dst_dir.iterdir():
        if item.name in kept or item.name in EXCLUDE_NAMES:
            continue
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()


def _walk(src_dir, dst_dir):
    kept = set()
    for item in src_dir.iterdir():
        if _is_excluded(item):
            continue
        kept.add(item.name)
        _copy_entry(item, dst_dir / item.name)
    _prune_extras(dst_dir, kept)


def sync_framework(src, dest):
    """把源码目录同步到框架副本，删除源码里已删掉的内容。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copytree(src, dest, ignore=_ignore, symlinks=True)
        return "copied"
    _walk(src, dest)
    return "synced"


def _is_shared_or_skill(entry):
    return (entry / "SKILL.md").is_file() or entry.name in SHARED_SKILL_DIRS


def _clear_dest(dest):
    if dest.is_symlink():
        dest.unlink()
    elif dest.exists():
        shutil.rmtree(dest)


def _link_framework_scripts(skill_scripts, framework_scripts):
    """在技能目录里补上框架脚本的软链。"""
    if not framework_scripts.is_dir():
        return
    for script in framework_scripts.iterdir():
        if not script.is_file():
            continue
        link = skill_scripts / script.name
        if link.exists() or link.is_symlink():
            continue
        link.symlink_to(script)


def _install_skill(entry, dest, framework_scripts):
    _clear_dest(dest)
    shutil.copytree(entry, dest, ignore=_ignore, symlinks=True)
    skill_scripts = dest / "scripts"
    skill_scripts.mkdir(exist_ok=True)
    _link_framework_scripts(skill_scripts, framework_scripts)


def install_skills(framework_home, skills_dir):
    """把技能目录复制到 Codex 全局技能根目录。

    用复制而不是符号链接：技能之间有跨目录相对引用
    （code-review/principles/ 里 ../../dev-builder/... 、../../_engineering-constraints/...），
    链接安装后这些路径在推理层会解析到别处。整棵 skills 目录一起复制，
    相对引用的解析结果与源码仓库里完全一致。

    每个技能目录内补上框架脚本的软链，这样 "scripts/xxx.py" 无论按技能目录解析
    还是按项目根解析都找得到。技能自带的 scripts/（如 subagent-driven-development）
    原样保留，它自己的脚本优先。
    """
    skills_src = framework_home / "agents" / "skills"
    if not skills_src.is_dir():
        die(f"找不到技能目录：{skills_src}")

    framework_scripts = framework_home / "scripts"
    skills_dir.mkdir(parents=True, exist_ok=True)

    installed, skipped = [], []
    for entry in sorted(skills_src.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_SKILL_DIRS:
            continue
        if not _is_shared_or_skill(entry):
            skipped.append(entry.name)
            continue
        _install_skill(entry, skills_dir / entry.name, framework_scripts)
        installed.append(entry.name)

    return installed, skipped


def write_manifest(framework_home, skills_dir, codex_home, installed):
    manifest = {
        "framework_home": str(framework_home),
        "skills_dir": str(skills_dir),
        "codex_home": str(codex_home),
        "skills": installed,
        "installed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    path = framework_home / MANIFEST_NAME
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def read_manifest(framework_home):
    path = framework_home / MANIFEST_NAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
