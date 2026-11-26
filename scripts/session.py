#!/usr/bin/env python3
"""
session.py — IdeaHammer Session State 工具

读写 .idea-hammer/session.json，跨 session 持久化上下文。

用法：
  read [--path P] | write --key K --value V | update --key K --value V
  validate [--path P] | append <key> <value> | context [--path P]
  checkpoint --phase P --task T [--commit SHA] [--tests JSON] [--next TEXT] [--artifacts A,B]
  restore [--path P]

  context = 精简版（启动时只读这个，省 token）；checkpoint = 记录恢复点（≠ Git Commit）
  restore = 读最近恢复点 + 需要重新核实的清单
"""

import argparse
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path


SCHEMA_VERSION = "1.0"

# 恢复时必须重新核实的事：State 只定位恢复位置，不代替对真实代码与执行结果的核查。
VERIFY_STEPS = [
    "git 工作区是否与 checkpoint 记录的 commit 一致（不一致说明中途有改动）",
    "checkpoint 记录的测试结果是否仍成立（代码变了必须重跑，不能沿用旧结论）",
    "checkpoint 之后的未提交改动属于哪个 Task，是否保留或回滚",
    "checkpoint 引用的产物（Spec / Plan / Design）是否还在原位且未被改动",
]


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


def emit(payload, indent=None):
    """统一 JSON 输出。"""
    print(json.dumps(payload, ensure_ascii=False, indent=indent))


def parse_json_arg(raw, label):
    """解析 JSON 参数；非法时给可读提示，不吐裸 traceback。"""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        emit({"error": f"--{label} 必须是合法 JSON"})
        sys.exit(1)


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
    checkpoints = session.get("checkpoints") or []
    return {
        "schema_version": session.get("schema_version"),
        "current_project": session.get("current_project"),
        "current_phase": session.get("current_phase"),
        "current_task": session.get("current_task"),
        "latest_checkpoint": checkpoints[-1] if checkpoints else None,
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


def append_to_array(session, key, value):
    """往 JSON 数组 key 追加一条；key 不存在则建空数组再追加。

    只支持顶层数组 key（key 中点号视为字面量）。
    必须先读后写，避免覆盖并发写丢数据（调用方负责）。
    """
    if key in session and not isinstance(session[key], list):
        raise ValueError(f"key {key!r} 已存在但不是数组（type={type(session[key]).__name__}）")
    if key not in session:
        session[key] = []
    session[key].append(value)


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
        emit({"error": "session.json 不存在"})
        sys.exit(1)
    emit(session, indent=2)


def cmd_write(args):
    session = read_session(args.path)
    if session is None:
        session = {"schema_version": SCHEMA_VERSION}
    update_field(session, args.key, parse_json_arg(args.value, "value"))
    write_session(session, args.path)
    emit({"updated": args.key, "path": str(find_session_path(args.path))})


def cmd_update(args):
    cmd_write(args)


def cmd_append(args):
    session = read_session(args.path)
    if session is None:
        session = {"schema_version": SCHEMA_VERSION}
    append_to_array(session, args.key, parse_json_arg(args.value, "value"))
    write_session(session, args.path)
    emit({"appended": args.key, "path": str(find_session_path(args.path))})


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
        emit({"empty": True, "msg": "无 session.json，全量读域文件"})
        sys.exit(1)
    emit(minimal_view(session), indent=2)


def build_checkpoint(args):
    """从命令行参数构造一条 checkpoint 记录。"""
    now = datetime.now().astimezone()
    artifacts = [a.strip() for a in args.artifacts.split(",") if a.strip()] if args.artifacts else []
    return {
        "id": f"cp-{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}",
        "phase": args.phase,
        "task": args.task,
        "git_commit": args.commit,
        "tests": parse_json_arg(args.tests, "tests") if args.tests else {},
        "next_action": args.next_action,
        "artifacts": artifacts,
        "created_at": now.isoformat(),
    }


def cmd_checkpoint(args):
    """记录一个任务恢复点（追加，不覆盖历史）。"""
    session = read_session(args.path) or {"schema_version": SCHEMA_VERSION}
    cp = build_checkpoint(args)
    append_to_array(session, "checkpoints", cp)
    write_session(session, args.path)
    emit(
        {
            "checkpointed": cp["id"],
            "task": cp["task"],
            "path": str(find_session_path(args.path)),
        }
    )


def cmd_restore(args):
    """输出最近 checkpoint + 恢复位置 + 必须重新核实的清单。"""
    session = read_session(args.path)
    if not session:
        emit(
            {
                "checkpoint": None,
                "resume_at": None,
                "verify_required": VERIFY_STEPS,
                "msg": "无 session.json，按 STATE-ROUTING 全量检测项目状态",
            }
        )
        sys.exit(1)
    checkpoints = session.get("checkpoints") or []
    cp = checkpoints[-1] if checkpoints else None
    emit(
        {
            "checkpoint": cp,
            "resume_at": (cp.get("task") if cp else None) or session.get("current_task"),
            "verify_required": VERIFY_STEPS,
        }
    )


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

    p_app = sub.add_parser("append", help="往 JSON 数组 key 追加一条（key 不存在则建空数组）")
    p_app.add_argument("--path")
    p_app.add_argument("key", help="顶层数组 key 名（key 含点号视为字面量）")
    p_app.add_argument("value", help="JSON 字面量")
    p_app.set_defaults(func=cmd_append)

    p_val = sub.add_parser("validate", help="校验")
    p_val.add_argument("--path")
    p_val.set_defaults(func=cmd_validate)

    p_ctx = sub.add_parser("context", help="读精简版（启动用）")
    p_ctx.add_argument("--path")
    p_ctx.set_defaults(func=cmd_context)

    p_cp = sub.add_parser("checkpoint", help="记录任务恢复点（Checkpoint）")
    p_cp.add_argument("--phase", help="当前 Phase")
    p_cp.add_argument("--task", help="当前 Task 标识")
    p_cp.add_argument("--commit", help="对应 git commit（可选）")
    p_cp.add_argument("--tests", help='测试证据 JSON，如 {"unit_test":"passed"}')
    p_cp.add_argument("--next", dest="next_action", help="下一步动作")
    p_cp.add_argument("--artifacts", help="关联产物路径，逗号分隔")
    p_cp.add_argument("--path")
    p_cp.set_defaults(func=cmd_checkpoint)

    p_res = sub.add_parser("restore", help="读最近 checkpoint + 需核实清单")
    p_res.add_argument("--path")
    p_res.set_defaults(func=cmd_restore)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
