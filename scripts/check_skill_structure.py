#!/usr/bin/env python3
"""
check_skill_structure.py — 校验 IdeaHammer skill 结构

用法：
  python3 scripts/check_skill_structure.py [选项] [skill-root]

选项：
  --strict    三层目录（principles/ workflows/ contracts/）必须都存在
  --help      显示本帮助

不传参数默认校验 agents/skills/ 下所有 skill（排除 _template/）。
默认模式只校验必备项；--strict 才要求三层完整。

必备校验：
  1. SKILL.md 存在
  2. SKILL.md ≤ 50 行
  3. YAML frontmatter 合法（含 name + description）

触发性校验（条件存在时）：
  4. contracts/*.schema.json 是合法 JSON

返回：0 = 全过；1 = 有错误。
"""

import sys
import json
import re
from pathlib import Path

SKILL_ROOT = "agents/skills"
STRICT = False


def parse_args():
    global STRICT, SKILL_ROOT
    args = sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--strict":
            STRICT = True
        elif a in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            SKILL_ROOT = a


def check_frontmatter(path: Path, name: str):
    """校验 YAML frontmatter，返回 (errors_list, warn_list)。"""
    errors = []
    warns = []
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        errors.append(f"[FAIL] {name}: frontmatter 缺失或不闭合（需要 --- 包裹）")
        return errors, warns
    try:
        import yaml
    except ImportError:
        warns.append(f"[WARN] {name}: PyYAML 未装，跳过 frontmatter 字段校验（pip install pyyaml）")
        return errors, warns
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"[FAIL] {name}: YAML 解析失败：{e}")
        return errors, warns
    if not isinstance(data, dict):
        errors.append(f"[FAIL] {name}: frontmatter 不是 dict")
    elif "name" not in data or not data["name"]:
        errors.append(f"[FAIL] {name}: frontmatter 缺 name")
    elif "description" not in data or not data["description"]:
        errors.append(f"[FAIL] {name}: frontmatter 缺 description")
    return errors, warns


def check_skill(skill_dir: Path):
    """校验单个 skill 目录，返回 errors 列表。"""
    name = skill_dir.name
    errors = []
    warns = []
    skill_md = skill_dir / "SKILL.md"

    # 1. SKILL.md 存在
    if not skill_md.exists():
        return [f"[FAIL] {name}: 缺 SKILL.md"], []

    # 2. SKILL.md ≤ 50 行
    lines = len(skill_md.read_text(encoding="utf-8").splitlines())
    if lines > 50:
        errors.append(f"[FAIL] {name}: SKILL.md 有 {lines} 行（>50，需重构）")

    # 3. frontmatter
    fm_errors, fm_warns = check_frontmatter(skill_md, name)
    errors.extend(fm_errors)
    warns.extend(fm_warns)

    # 4. contracts/*.json 合法性
    contracts_dir = skill_dir / "contracts"
    if contracts_dir.is_dir():
        for f in sorted(contracts_dir.glob("*.json")):
            try:
                json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                errors.append(f"[FAIL] {name}: {f.name} 不是合法 JSON：{e}")

    # 5. --strict 模式
    if STRICT:
        for d in ("principles", "workflows", "contracts"):
            if not (skill_dir / d).is_dir():
                errors.append(f"[FAIL] {name}: --strict 模式下 {d}/ 必须存在")

    return errors, warns


def _extras_str(skill_dir):
    """生成 PWC 三层标记。"""
    extras = ""
    if (skill_dir / "principles").is_dir() and any((skill_dir / "principles").iterdir()):
        extras += "P"
    if (skill_dir / "workflows").is_dir() and any((skill_dir / "workflows").iterdir()):
        extras += "W"
    if (skill_dir / "contracts").is_dir() and any((skill_dir / "contracts").iterdir()):
        extras += "C"
    return f" [{extras}]" if extras else ""


def _print_template(skill_dir):
    """打印 _template 目录结果。"""
    lines = len((skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines())
    print(f"[TEMPLATE] {skill_dir.name} ({lines} 行){_extras_str(skill_dir)}")


def _print_skill_result(skill_dir, errors, warns):
    """打印单个 skill 的校验结果。"""
    for w in warns:
        print(w)
    if errors:
        for e in errors:
            print(e)
        return len(errors)
    lines = len((skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines())
    print(f"[OK   ] {skill_dir.name} ({lines} 行){_extras_str(skill_dir)}")
    return 0


def _print_summary(checked, total_errors):
    """打印最终 summary + 设置 exit code。"""
    print("---")
    print(f"📊 检查 {checked} 个 skill，错误 {total_errors} 个")
    if total_errors == 0:
        print("✅ 全部 OK")
    else:
        print("❌ 有失败项，需修复")


def _iter_skill_dirs(root):
    """迭代所有 skill 目录（排除无 SKILL.md 的目录）。"""
    for skill_dir in sorted(root.iterdir()):
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue
        yield skill_dir


def main():
    parse_args()
    root = Path(SKILL_ROOT)
    if not root.is_dir():
        print(f"[FATAL] skill 根目录不存在：{SKILL_ROOT}", file=sys.stderr)
        sys.exit(2)

    mode = "STRICT" if STRICT else "default"
    print(f"🔍 校验 {SKILL_ROOT}（模式：{mode}）")
    print("---")

    checked = 0
    total_errors = 0
    for skill_dir in _iter_skill_dirs(root):
        if skill_dir.name == "_template":
            _print_template(skill_dir)
            continue
        checked += 1
        errors, warns = check_skill(skill_dir)
        total_errors += _print_skill_result(skill_dir, errors, warns)

    _print_summary(checked, total_errors)
    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
