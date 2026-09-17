#!/usr/bin/env python3
"""
intent_classifier.py — IdeaHammer 意图分类器

基于 skill description 关键词 + 规则启发式，对用户 prompt 分类到最匹配的 skill。
骨架版本（不调 LLM），后续可升级到 LLM-based 或 embedding-based。

用法：
  python3 scripts/intent_classifier.py classify --prompt "我想做一个 X"
  python3 scripts/intent_classifier.py classify --prompt "我改个需求" --top 3
  python3 scripts/intent_classifier.py list    # 列出所有 skill 的 description
"""

import argparse
import re
from pathlib import Path


SKILLS_ROOT = Path("agents/skills")


def load_skills():
    """加载所有 skill 的 name + description。"""
    skills = []
    for p in sorted(SKILLS_ROOT.iterdir()):
        if not p.is_dir() or p.name.startswith("_"):
            continue
        skill_md = p / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8")
        m = re.match(r"^---\n.*?name:\s*(\S+).*?description:\s*(.+?)\n---", text, re.DOTALL)
        if m:
            skills.append({
                "name": m.group(1),
                "description": m.group(2).strip(),
                "triggers": extract_triggers(m.group(2)),
            })
    return skills


def extract_triggers(description):
    """从 description 提取触发关键词。

    规则：
    - 中文 2-4 字短语
    - 引号内的具体场景
    """
    triggers = set()
    # 引号内
    for m in re.finditer(r"'([^']{2,12})'", description):
        triggers.add(m.group(1))
    for m in re.finditer(r'"([^"]{2,12})"', description):
        triggers.add(m.group(1))
    # 中文 2-4 字词（启发式）
    for m in re.finditer(r'[一-龥]{2,4}', description):
        triggers.add(m.group(0))
    return list(triggers)[:20]  # 限 20 个


def classify(prompt, skills, top=3):
    """对 prompt 分类，返回 top N 候选 skill。"""
    # 1. 关键词匹配
    candidates = []
    for skill in skills:
        score = 0
        matches = []
        for trigger in skill["triggers"]:
            if trigger in prompt:
                score += 2
                matches.append(trigger)
        # 名字本身也算触发
        if skill["name"] in prompt:
            score += 5
            matches.append(skill["name"])
        # 描述里的核心动词
        for kw in ["写代码", "做应用", "改需求", "加功能", "调 UI", "部署", "发布", "打包",
                  "测试", "审查", "修 bug", "调错误", "报错", "设计", "定方向",
                  "规划", "分阶段", "创建", "新技能", "进化", "消化"]:
            if kw in prompt and kw in skill["description"]:
                score += 1
                matches.append(kw)
        if score > 0:
            candidates.append({
                "skill": skill["name"],
                "score": score,
                "matches": matches,
            })

    # 2. 排序
    candidates.sort(key=lambda x: -x["score"])
    return candidates[:top]


def cmd_classify(args):
    skills = load_skills()
    candidates = classify(args.prompt, skills, args.top)
    if not candidates:
        print("没有匹配的 skill，请确认 prompt 表述")
        return
    print(f"Prompt: {args.prompt}")
    print(f"Top {args.top} 候选：")
    for c in candidates:
        print(f"  {c['score']:3d}  {c['skill']:25s}  触发: {c['matches'][:5]}")


def cmd_list(args):
    skills = load_skills()
    print(f"{'Skill':25s} {'Description (截断)'}")
    print("-" * 80)
    for s in skills:
        desc = s["description"][:60]
        print(f"  {s['name']:23s}  {desc}...")


def main():
    parser = argparse.ArgumentParser(description="IdeaHammer 意图分类器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cl = sub.add_parser("classify", help="分类用户 prompt")
    p_cl.add_argument("--prompt", required=True)
    p_cl.add_argument("--top", type=int, default=3)
    p_cl.set_defaults(func=cmd_classify)

    p_ls = sub.add_parser("list", help="列出所有 skill")
    p_ls.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
