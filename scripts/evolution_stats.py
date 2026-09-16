#!/usr/bin/env python3
"""
evolution_stats.py — Evolution 效果统计（effect 层）

跟踪 proposal 落地后的效果指标，验证规则改动是否改善系统。

用法：
  # 初始化
  python3 scripts/evolution_stats.py init

  # 添加 proposal 接受记录
  python3 scripts/evolution_stats.py add-acceptance --proposal_id D-NNN --accepted true

  # 添加效果指标
  python3 scripts/evolution_stats.py add-impact --metric_name "契约测试通过率" --before 0.95 --after 0.99

  # 显示统计
  python3 scripts/evolution_stats.py show

  # 验证
  python3 scripts/evolution_stats.py validate
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

STATS_PATH = Path(".codex/evolution/effect-stats.json")


def load_stats():
    if not STATS_PATH.exists():
        return {"schema_version": "1.0", "metrics": {}}
    return json.loads(STATS_PATH.read_text(encoding="utf-8"))


def save_stats(stats):
    stats["last_updated"] = datetime.now().astimezone().isoformat()
    STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATS_PATH.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_init(args):
    if STATS_PATH.exists() and not args.force:
        print(f"stats 已存在：{STATS_PATH}")
        sys.exit(1)
    save_stats({"schema_version": "1.0", "metrics": {}})
    print(f"✓ 初始化 {STATS_PATH}")


def cmd_add_acceptance(args):
    stats = load_stats()
    churn = stats["metrics"].setdefault("rule_churn", {"added": 0, "retired": 0, "net": 0})
    if args.accepted:
        churn["added"] += 1
    else:
        churn["retired"] += 1
    churn["net"] = churn["added"] - churn["retired"]
    save_stats(stats)
    print(f"✓ 记录 proposal {args.proposal_id}: {'accepted' if args.accepted else 'rejected'}")


def cmd_add_impact(args):
    stats = load_stats()
    impacts = stats["metrics"].setdefault("impact_metrics", [])
    improvement = ((args.after - args.before) / args.before * 100) if args.before != 0 else 0
    impacts.append({
        "metric_name": args.metric_name,
        "before": args.before,
        "after": args.after,
        "improvement_pct": round(improvement, 2),
        "recorded_at": datetime.now().astimezone().isoformat()
    })
    save_stats(stats)
    print(f"✓ 记录影响指标 {args.metric_name}: {args.before} → {args.after} ({improvement:+.1f}%)")


def cmd_add_signal(args):
    stats = load_stats()
    throughput = stats["metrics"].setdefault("signal_throughput", {
        "explicit_count": 0, "implicit_count": 0, "effect_count": 0
    })
    throughput[f"{args.layer}_count"] = throughput.get(f"{args.layer}_count", 0) + 1
    save_stats(stats)
    print(f"✓ 记录 {args.layer} 层信号（累计 {throughput[f'{args.layer}_count']}）")


def cmd_show(args):
    stats = load_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def cmd_validate(args):
    stats = load_stats()
    if "metrics" not in stats:
        print("stats 缺 metrics")
        sys.exit(1)
    print(f"✓ {STATS_PATH} 校验通过")


def main():
    parser = argparse.ArgumentParser(description="Evolution 效果统计")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_acc = sub.add_parser("add-acceptance")
    p_acc.add_argument("--proposal_id", required=True)
    p_acc.add_argument("--accepted", type=lambda v: v.lower() == "true", required=True)
    p_acc.set_defaults(func=cmd_add_acceptance)

    p_imp = sub.add_parser("add-impact")
    p_imp.add_argument("--metric_name", required=True)
    p_imp.add_argument("--before", type=float, required=True)
    p_imp.add_argument("--after", type=float, required=True)
    p_imp.set_defaults(func=cmd_add_impact)

    p_sig = sub.add_parser("add-signal")
    p_sig.add_argument("--layer", choices=["explicit", "implicit", "effect"], required=True)
    p_sig.set_defaults(func=cmd_add_signal)

    p_show = sub.add_parser("show")
    p_show.set_defaults(func=cmd_show)

    p_val = sub.add_parser("validate")
    p_val.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
