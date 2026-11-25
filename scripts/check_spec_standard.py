"""Spec 标准校验：PRD / FRD / User Story / AC 四要素 + Phase 0 缺口门禁

用法：
    python3 scripts/check_spec_standard.py --project examples/personal-blog
    python3 scripts/check_spec_standard.py --file path/to/Product-Spec.md

退出码：0 = 通过；1 = 存在缺口（Phase 0 不能出关）
"""
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------- 常量 ----------

REQ_HEAD = re.compile(r"^###\s+(REQ-\d{3}):", re.M)
HEADING = re.compile(r"^(#{2,3})\s+(.+)$", re.M)
AC_ID = re.compile(r"AC-(\d{3})-(\d{2})")
PLACEHOLDER = re.compile(r"\{\{|\}\}|\[待补充\]|\bTODO\b|\bTBD\b")

PRD_SECTIONS = [
    "1.1 产品背景与目标",
    "1.2 用户角色与画像",
    "1.3 用户核心问题",
    "1.4 核心价值",
    "1.6 业务指标",
    "2.1 本版本范围",
    "2.2 不在本版本范围",
    "4. 产品优先级",
]

FRD_FIELDS = ["目标", "行为", "规则", "状态"]
FRD_ONE_OF = ["输入", "展示字段"]  # 查询类可只填展示字段


# ---------- 解析 ----------

def split_sections(text: str) -> Dict[str, str]:
    """按二/三级标题切段，键为标题文字。"""
    sections: Dict[str, str] = {}
    matches = list(HEADING.finditer(text))
    for i, m in enumerate(matches):
        title = m.group(2).strip()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[title] = text[m.end():end].strip()
    return sections


def find_section(sections: Dict[str, str], prefix: str) -> Optional[str]:
    for title, body in sections.items():
        if title.startswith(prefix):
            return body
    return None


def table_rows(body: str) -> int:
    """返回表格数据行数（排除表头与分隔行）。"""
    rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
    return max(0, len(rows) - 2)


def req_blocks(text: str) -> List[Tuple[str, str]]:
    heads = list(REQ_HEAD.finditer(text))
    blocks = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        blocks.append((m.group(1), text[m.end():end]))
    return blocks


def field_text(block: str, label: str) -> Optional[str]:
    """取 **label：** 到下一个 **字段** 之间的内容；不存在返回 None。"""
    pattern = re.compile(
        rf"\*\*{re.escape(label)}[^\n]*\*\*(.*?)(?=\n\*\*[^\n]+\*\*|\n###|\Z)", re.S
    )
    m = pattern.search(block)
    return m.group(1).strip() if m else None


# ---------- 规则 ----------

def check_prd_sections(sections: Dict[str, str]) -> List[str]:
    errors = []
    for title in PRD_SECTIONS:
        body = find_section(sections, title)
        if body is None:
            errors.append(f"[PRD] 缺少章节：{title}")
        elif not body.strip() or PLACEHOLDER.search(body):
            errors.append(f"[PRD] 章节未补齐：{title}")
    return errors


def check_prd_rows(sections: Dict[str, str]) -> List[str]:
    errors = []
    roles = find_section(sections, "1.2 用户角色与画像")
    if roles and table_rows(roles) < 1:
        errors.append("[PRD] 1.2 至少需要 1 个用户角色行")
    metrics = find_section(sections, "1.6 业务指标")
    if metrics and table_rows(metrics) < 1:
        errors.append("[PRD] 1.6 至少需要 1 个业务指标")
    scope = find_section(sections, "2.1 本版本范围")
    if scope and "P0" not in scope:
        errors.append("[PRD] 2.1 没有 P0 范围条目")
    return errors


def check_prd_flows(text: str) -> List[str]:
    errors = []
    if not re.search(r"\|?\s*TASK-\d{3}\s*\|?", text):
        errors.append("[PRD] §3 缺少用户任务（TASK-###）")
    if not re.search(r"^###\s+FLOW-\d{3}", text, re.M):
        errors.append("[PRD] §3 缺少用户流程（FLOW-###）")
    return errors


def check_prd(text: str, sections: Dict[str, str]) -> List[str]:
    return check_prd_sections(sections) + check_prd_rows(sections) + check_prd_flows(text)


def check_user_story(req_id: str, block: str) -> List[str]:
    us = field_text(block, "用户故事")
    if not us:
        return [f"[US] {req_id} 缺少用户故事"]
    return [
        f"[US] {req_id} 用户故事缺少「{part}」"
        for part in ("作为一个", "我希望", "以便于")
        if part not in us
    ]


def check_frd(req_id: str, block: str) -> List[str]:
    contents = {}
    for label in FRD_FIELDS + FRD_ONE_OF:
        body = field_text(block, label)
        if body is not None:
            contents[label] = body
    errors = [f"[FRD] {req_id} 缺少「{label}」" for label in FRD_FIELDS if not contents.get(label)]
    if not any(contents.get(k) for k in FRD_ONE_OF):
        errors.append(f"[FRD] {req_id} 输入与展示字段不能同时为空")
    if not field_text(block, "输出 / 结果"):
        errors.append(f"[FRD] {req_id} 缺少「输出 / 结果」")
    errors += [
        f"[FRD] {req_id}「{label}」仍是占位内容"
        for label, body in contents.items()
        if PLACEHOLDER.search(body)
    ]
    return errors


def check_acs(req_id: str, block: str, ac_seen: Dict[str, str]) -> List[str]:
    errors = []
    acs = AC_ID.findall(block)
    req_num = req_id.split("-")[1]
    if len(acs) < 3:
        errors.append(f"[AC] {req_id} 至少需要 3 条 AC（当前 {len(acs)} 条）")
    for num, seq in acs:
        ac_id = f"AC-{num}-{seq}"
        if num != req_num:
            errors.append(f"[AC] {ac_id} 编号与所属 {req_id} 不一致")
        if ac_id in ac_seen:
            errors.append(f"[AC] {ac_id} 重复定义（另见 {ac_seen[ac_id]}）")
        ac_seen[ac_id] = req_id
    return errors


def check_req(req_id: str, block: str, ac_seen: Dict[str, str]) -> List[str]:
    return (
        check_user_story(req_id, block)
        + check_frd(req_id, block)
        + check_acs(req_id, block, ac_seen)
    )


def check_spec(text: str) -> List[str]:
    sections = split_sections(text)
    errors = check_prd(text, sections)

    blocks = req_blocks(text)
    if not blocks:
        return errors + ["[FRD] 没有找到任何 REQ-### 功能需求"]

    ac_seen: Dict[str, str] = {}
    for req_id, block in blocks:
        if "优先级：** P1" in block:
            continue  # P1 允许留待后续补齐
        errors.extend(check_req(req_id, block, ac_seen))
    return errors


# ---------- CLI ----------

def resolve_spec(project: Optional[str], file: Optional[str]) -> Path:
    if file:
        return Path(file)
    if project:
        return Path(project) / "Product-Spec.md"
    return Path("examples/personal-blog/Product-Spec.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 Product-Spec 是否满足四要素标准")
    parser.add_argument("--project", help="项目目录（读取其中的 Product-Spec.md）")
    parser.add_argument("--file", help="直接指定 Product-Spec.md 路径")
    args = parser.parse_args()

    spec = resolve_spec(args.project, args.file)
    if not spec.exists():
        print(f"❌ 找不到 Spec 文件：{spec}")
        return 1

    errors = check_spec(spec.read_text(encoding="utf-8"))
    if errors:
        print(f"❌ Spec 标准未通过（{len(errors)} 项缺口）：")
        for err in errors:
            print(f"  - {err}")
        print("\nPhase 0 不能出关：请把缺口变成具体追问，或写成显式假设（§10.1）/ 开放问题（§10.2）。")
        return 1

    print("✅ Spec 标准通过：PRD / FRD / User Story / AC 四要素齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
