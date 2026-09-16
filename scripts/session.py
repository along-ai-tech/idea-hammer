#!/usr/bin/env python3
"""
session.py — IdeaHammer Session State 工具

读取和写入 .idea-hammer/session.json，跨 session 持久化上下文。

用法：
  # 读 session（精简版，启动用）
  python3 scripts/session.py read [--path PATH] [--minimal]

  # 写 session
  python3 scripts/session.py write --key KEY --value VALUE [--path PATH]

  # 更新某个字段
  python3 scripts/session.py update --key KEY --value VALUE [--path PATH]

  # 验证
  python3 scripts/session.py validate [--path PATH]

  # 显示精简版（启动时只读这个，省 token）
  python3 scripts/session.py context [--path PATH]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


SCHEMA_VERSION = "1.0"


def find_session_path(explicit=None):
    """查找 session.json 路径（按优先级：显式参数 > 当前目录 > 父目录）。"""
    if explicit:
        return Path(explicit)
    
    candidates = [
        Path.cwd() / ".idea-hammer/session.json",
        Path.cwd().parent / ".idea-hammer/session.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def read_session(path=None):
    path = find_session_path(path) or Path(".idea-hammer/session.json")
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_session(session, path=None):
    path = find_session_path(path) or Path(".idea-hammer/session.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    session["last_updated"] = datetime.now().astimezone().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2, ensure_ascii=False)


def minimal_view(session):
    """精简版（启动用，只保留当前任务 + 用户偏好 + 最近 3 个决策）。"""
    if not session:
        return {}
    return {
        "schema_version": session.get("schema_version"),
        "current_project": session.get("current_project"),
        "current_phase": session.get("current_phase"),
        "current_task": session.get("current_task"),
        "recent_decisions": session.get("key_decisions", [])[-3:],
        "user_preferences": session.get("user_preferences", {}),
        "open_questions": session.get("open_questions", []),
    }


def update_field(session, key, value):
    """点路径更新字段，如 key_decisions.0.summary。"""
    parts = key.split(".")
    obj = session
    for p in parts[:-1]:
        if p.isdigit():
            obj = obj[int(p)]
        else:
            obj = obj.setdefault(p, {})
    last = parts[-1]
    if last.isdigit():
        obj[int(last)] = value
    else:
        obj[last] = value


def validate(session):
    """基本验证（必填字段、类型）。"""
    errors = []
    if not isinstance(session, dict):
        return ["session 必须是 dict"]
    if "schema_version" not in session:
        errors.append("缺 schema_version")
    if "last_updated" not in session:
        errors.append("缺 last_updated")
    return errors


def cmd_read(args):
    session = read_session(args.path)
    if session is None:
        print(json.dumps({"error": "session.json 不存在"}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(session, indent=2, ensure_ascii=False))


def cmd_write(args):
    session = read_session(args.path)
    if session is None:
        session = {"schema_version": SCHEMA_VERSION}
    update_field(session, args.key, json.loads(args.value))
    write_session(session, args.path)
    print(json.dumps({"updated": args.key, "path": str(find_session_path(args.path))}, ensure_ascii=False))


def cmd_update(args):
    cmd_write(args)


def cmd_validate(args):
    session = read_session(args.path)
    if session is None:
        print("session.json 不存在")
        sys.exit(1)
    errors = validate(session)
    if errors:
        print("错误：", errors)
        sys.exit(1)
    print("✓ session.json 校验通过")


def cmd_context(args):
    """输出启动用的精简版。"""
    session = read_session(args.path)
    if session is None:
        print(json.dumps({"empty": True, "msg": "无 session.json，全量读域文件"}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(minimal_view(session), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="IdeaHammer Session State 工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_read = sub.add_parser("read", help="读全量 session")
    p_read.add_argument("--path")
    p_read.set_defaults(func=cmd_read)

    p_write = sub.add_parser("write", help="写整个 session（合并现有）")
    p_write.add_argument("--path")
    p_write.add_argument("--key", required=True)
    p_write.add_argument("--value", required=True)
    p_write.set_defaults(func=cmd_write)

    p_upd = sub.add_parser("update", help="同 write")
    p_upd.add_argument("--path")
    p_upd.add_argument("--key", required=True)
    p_upd.add_argument("--value", required=True)
    p_upd.set_defaults(func=cmd_update)

    p_val = sub.add_parser("validate", help="校验")
    p_val.add_argument("--path")
    p_val.set_defaults(func=cmd_validate)

    p_ctx = sub.add_parser("context", help="读精简版（启动用）")
    p_ctx.add_argument("--path")
    p_ctx.set_defaults(func=cmd_context)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
