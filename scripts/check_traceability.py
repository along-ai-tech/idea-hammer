#!/usr/bin/env python3
"""
check_traceability.py — 校验 需求 → 任务 → 测试 → 版本 链路

用法：--project DIR [--strict] [--write FILE] [--impact ID] [--json]
约定详见 agents/skills/_traceability/README.md。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

REQ_RE = re.compile(r"\bREQ-\d{3}\b")
AC_RE = re.compile(r"\bAC-\d{3}-\d{2}\b")
DT_RE = re.compile(r"^###\s+((?:DT|WI)-\d{1,3})\b")
TEST_RE = re.compile(r"@trace\s+(TEST-\d{3})\s+([^\n]+)")
TEST_FILE_RE = re.compile(
    r"^(test_.*\.py|.*_test\.py|.*\.test\.(ts|tsx|js|jsx)|.*\.spec\.(ts|tsx|js|jsx)"
    r"|.*_test\.go|.*Test\.java|.*Tests\.cs|.*\.test\.dart)$"
)
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
             "dist", "build", "target", ".tox", ".mypy_cache", ".idea"}
TEST_MARKERS = ("def test_", "it(", "test(", "func Test", "@Test", "TEST(")
REQ_HEAD = re.compile(r"^###\s+(REQ-\d{3})\s*[:：]\s*(.*)$")
FLOW_HEAD = re.compile(r"^###\s+(FLOW-\d{3})\s*[:：]\s*(.*)$")


def _read(path):
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def _block_end(lines, start, level):
    prefix = "#" * level + " "
    for i in range(start + 1, len(lines)):
        if lines[i].startswith(prefix) and not lines[i].startswith(prefix + "#"):
            return i
    return len(lines)


def parse_refs(raw):
    acs = set(AC_RE.findall(raw))
    return set(REQ_RE.findall(raw)) | {"REQ-" + a.split("-")[1] for a in acs}, acs


def parse_spec(text):
    lines = text.splitlines()
    spec = {"reqs": {}, "flows": {}, "tasks": {}, "ac_req": {}, "dup": []}
    for i, line in enumerate(lines):
        block = "\n".join(lines[i:_block_end(lines, i, 3)])
        m = REQ_HEAD.match(line)
        if m:
            rid = m.group(1)
            if rid in spec["reqs"]:
                spec["dup"].append(rid)
            acs = sorted(set(AC_RE.findall(block)))
            pm = re.search(r"\*\*优先级[：:]\*\*\s*(P\d)", block)
            spec["reqs"][rid] = {
                "name": m.group(2).strip(),
                "priority": pm.group(1) if pm else "P1",
                "tasks": sorted(set(re.findall(r"TASK-\d{3}", block))),
                "flows": sorted(set(re.findall(r"FLOW-\d{3}", block))),
                "acs": acs,
            }
            spec["ac_req"].update({ac: rid for ac in acs})
        f = FLOW_HEAD.match(line)
        if f:
            spec["flows"][f.group(1)] = {
                "name": f.group(2).strip(),
                "tasks": sorted(set(re.findall(r"TASK-\d{3}", block))),
            }
        t = re.match(r"^\|\s*(TASK-\d{3})\s*\|", line)
        if t:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            spec["tasks"][t.group(1)] = {"priority": cells[-1]}
    return spec


def parse_plan(text):
    plan = {"tasks": {}, "dup": []}
    current = None
    for n, line in enumerate(text.splitlines(), 1):
        m = DT_RE.match(line)
        if m:
            tid = "DT-" + re.sub(r"\D", "", m.group(1)).zfill(3)
            if tid in plan["tasks"]:
                plan["dup"].append(tid)
            current = {"id": tid, "line": n, "reqs": set(), "acs": set(), "exempt": False}
            plan["tasks"][tid] = current
            continue
        if current is not None and "关联需求" in line:
            current["reqs"].update(REQ_RE.findall(line))
            current["acs"].update(AC_RE.findall(line))
            current["exempt"] = "范围外" in line or "不涉及" in line
        elif line.startswith("## ") or line.startswith("# "):
            current = None
    return plan


def iter_test_files(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if TEST_FILE_RE.match(name):
                yield Path(base) / name


def parse_tests(root):
    found, dup, loose = {}, [], []
    for path in sorted(iter_test_files(root)):
        lines = _read(path).splitlines()
        for n, line in enumerate(lines):
            m = TEST_RE.search(line)
            if not m:
                continue
            tid = m.group(1)
            if tid in found:
                dup.append(tid)
            reqs, acs = parse_refs(m.group(2))
            found[tid] = {"id": tid, "path": str(path.relative_to(root)),
                          "line": n + 1, "reqs": sorted(reqs), "acs": sorted(acs)}
            window = lines[max(0, n - 1):n + 6]
            if not any(marker in row for row in window for marker in TEST_MARKERS):
                loose.append(tid)
    return {"tests": found, "dup": dup, "unattached": loose}


def _load_graph(root, args):
    spec = parse_spec(_read(root / args.spec))
    plan = parse_plan(_read(root / args.plan))
    path = root / args.release
    try:
        release = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    except json.JSONDecodeError as exc:
        release = {"_error": str(exc)}
    return spec, {"plan": plan, "tests": parse_tests(root), "release": release}


def _check_reqs(spec, graph, out):
    plan, tests = graph["plan"]["tasks"].values(), graph["tests"]["tests"].values()
    for rid, req in spec["reqs"].items():
        sink = out["errors"] if req["priority"] == "P0" else out["warnings"]
        checks = (
            (f"{rid} 未关联任何用户任务 TASK", req["tasks"]),
            (f"{rid} 缺验收标准 AC", req["acs"]),
            (f"{rid} 未被任何开发任务 DT 覆盖", [t for t in plan if rid in t["reqs"]]),
            (f"{rid} 未被任何测试 TEST 覆盖", [t for t in tests if rid in t["reqs"]]),
        )
        sink += [msg for msg, ok in checks if not ok]


def _check_refs(spec, out):
    tasks, flows = set(spec["tasks"]), set(spec["flows"])
    for rid, req in spec["reqs"].items():
        out["errors"] += [f"{rid} 引用了不存在的 {x}" for x in sorted(set(req["tasks"]) - tasks)]
        out["errors"] += [f"{rid} 引用了不存在的 {x}" for x in sorted(set(req["flows"]) - flows)]


def _check_plan(spec, graph, out):
    known = set(spec["ac_req"])
    for tid, task in graph["plan"]["tasks"].items():
        if not task["reqs"] and not task.get("exempt"):
            out["warnings"].append(f"{tid} 未关联任何 REQ（范围外任务需在 DEV-PLAN 说明）")
        out["errors"] += [f"{tid} 引用了不存在的 {r}" for r in sorted(task["reqs"] - set(spec["reqs"]))]
        out["errors"] += [f"{tid} 引用了不存在的 {ac}" for ac in sorted(task["acs"] - known)]
        out["errors"] += [f"{ac} 前缀与所属 {spec['ac_req'][ac]} 不一致"
                          for ac in sorted(task["acs"] & known)
                          if spec["ac_req"][ac] != "REQ-" + ac.split("-")[1]]


def _check_tests(spec, graph, out):
    tests = graph["tests"]["tests"]
    covered = {ac for t in tests.values() for ac in t["acs"]}
    for tid, test in tests.items():
        out["errors"] += [f"{tid} 引用了不存在的 {r}" for r in sorted(set(test["reqs"]) - set(spec["reqs"]))]
        out["errors"] += [f"{tid} 引用了不存在的 {ac}" for ac in test["acs"] if ac not in spec["ac_req"]]
    out["warnings"] += [f"{ac} 未被任何测试引用" for ac in sorted(set(spec["ac_req"]) - covered)]


def _check_release(spec, graph, out):
    release = graph["release"]
    if release is None:
        out["warnings"].append("未提供 RELEASE.json，版本链路未校验")
        return
    if "_error" in release:
        out["errors"].append(f"RELEASE.json 不是合法 JSON: {release['_error']}")
        return
    version = str(release.get("version", ""))
    if not re.fullmatch(r"v\d+\.\d+\.\d+", version):
        out["errors"].append(f"RELEASE.json 版本号非法: {version!r}（需 vX.Y.Z）")
    req_ids = set(release.get("requirements", []))
    out["errors"] += [f"RELEASE.json 引用了不存在的 {r}" for r in sorted(req_ids - set(spec["reqs"]))]
    p0 = {r for r, v in spec["reqs"].items() if v["priority"] == "P0"}
    out["errors"] += [f"P0 {r} 未进入发布清单 {version}" for r in sorted(p0 - req_ids)]
    info = release.get("tests", {})
    if not isinstance(info.get("total"), int) or info.get("passed") != info.get("total"):
        out["errors"].append(f"发布测试未全通过: {info.get('passed')}/{info.get('total')}")
    ids = set(info.get("ids", []))
    out["errors"] += [f"RELEASE.json 引用了不存在的 {t}" for t in sorted(ids - set(graph["tests"]["tests"]))]
    for rid in sorted(p0 & req_ids):
        related = {t["id"] for t in graph["tests"]["tests"].values() if rid in t["reqs"]}
        if related and not related & ids:
            out["errors"].append(f"P0 {rid} 的测试未列入 {version} 发布清单")


def build_report(spec, graph, strict):
    out = {
        "errors": [f"REQ 重复定义: {x}" for x in spec["dup"]]
        + [f"DT 重复定义: {x}" for x in graph["plan"]["dup"]]
        + [f"TEST 重复定义: {x}" for x in graph["tests"]["dup"]]
        + [f"{x} 的 @trace 未紧邻测试代码" for x in graph["tests"]["unattached"]],
        "warnings": [],
    }
    _check_reqs(spec, graph, out)
    _check_refs(spec, out)
    _check_plan(spec, graph, out)
    _check_tests(spec, graph, out)
    _check_release(spec, graph, out)
    if strict:
        out["errors"] += [f"[strict] {w}" for w in out["warnings"]]
    return out


def render_matrix(spec, graph):
    release = (graph["release"] or {}).get("version", "-")
    rows = ["# TRACEABILITY", "", "> 由 `scripts/check_traceability.py --write` 生成，勿手改。", "",
            "| 需求 | 优先级 | 用户任务 | 开发任务 | 测试 | 发布 |",
            "|------|--------|----------|----------|------|------|"]
    for rid, req in sorted(spec["reqs"].items()):
        dts = [t["id"] for t in graph["plan"]["tasks"].values() if rid in t["reqs"]]
        tids = [t["id"] for t in graph["tests"]["tests"].values() if rid in t["reqs"]]
        rows.append(f"| {rid} | {req['priority']} | {', '.join(req['tasks']) or '-'} | "
                    f"{', '.join(dts) or '-'} | {', '.join(tids) or '-'} | {release} |")
    rows += ["", "## 验收标准覆盖", "", "| AC | 所属需求 | 测试 |", "|----|----------|------|"]
    for ac, rid in sorted(spec["ac_req"].items()):
        tids = [t["id"] for t in graph["tests"]["tests"].values() if ac in t["acs"]]
        rows.append(f"| {ac} | {rid} | {', '.join(tids) or '-'} |")
    return "\n".join(rows) + "\n"


def print_impact(target, spec, graph, root):
    acs = {target} if target.startswith("AC-") else set()
    if target.startswith("AC-"):
        req_ids = {spec["ac_req"].get(target, "REQ-" + target.split("-")[1])}
    else:
        req_ids = {target} if target.startswith("REQ-") else set()
    def hit(item):
        return bool(set(item["reqs"]) & req_ids or set(item["acs"]) & acs)
    dts = sorted(t["id"] for t in graph["plan"]["tasks"].values() if hit(t))
    tids = sorted(t["id"] for t in graph["tests"]["tests"].values() if hit(t))
    changelog = _read(root / "Product-Spec-CHANGELOG.md")
    hits = ["[" + s.strip().splitlines()[0] for s in changelog.split("## [")[1:] if target in s]
    tasks = [", ".join(spec["reqs"].get(r, {}).get("tasks", [])) for r in sorted(req_ids)]
    print("\n".join([
        f"影响面 {target}:", f"  需求: {', '.join(sorted(req_ids))}",
        f"  用户任务: {'; '.join(tasks) or '-'}", f"  开发任务: {', '.join(dts) or '-'}",
        f"  测试: {', '.join(tids) or '-'}",
        f"  发布版本: {(graph['release'] or {}).get('version', '-')}",
        f"  变更记录: {'; '.join(hits) or '-'}",
    ]))


def main():
    parser = argparse.ArgumentParser(description="需求追踪链路校验")
    parser.add_argument("--project", default=".", help="项目根目录")
    parser.add_argument("--spec", default="Product-Spec.md")
    parser.add_argument("--plan", default="DEV-PLAN.md")
    parser.add_argument("--release", default="RELEASE.json")
    parser.add_argument("--strict", action="store_true", help="警告升级为失败")
    parser.add_argument("--write", metavar="FILE", help="生成追踪矩阵")
    parser.add_argument("--impact", metavar="ID", help="查询 REQ/AC 影响面")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not (root / args.spec).exists():
        print(f"[FATAL] 缺 {root / args.spec}", file=sys.stderr)
        return 2
    spec, graph = _load_graph(root, args)
    if args.impact:
        print_impact(args.impact, spec, graph, root)
        return 0
    report = build_report(spec, graph, args.strict)
    if args.write:
        Path(args.write).write_text(render_matrix(spec, graph), encoding="utf-8")
        print(f"已生成 {args.write}")
    for w in report["warnings"]:
        print(f"[WARN] {w}")
    for e in report["errors"]:
        print(f"[FAIL] {e}")
    print("---")
    if report["errors"]:
        print(f"❌ 追踪校验失败：{len(report['errors'])} 个错误 / {len(report['warnings'])} 个警告")
        return 1
    print(f"✅ 追踪链路通过（{'strict' if args.strict else 'default'}），警告 {len(report['warnings'])} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
