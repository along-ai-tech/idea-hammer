"""全局 hooks.json 构建 / 合并 / 移除。"""

import json
import shutil
import time

from .console import warn
from .paths import HOOK_COMMAND_FIELDS, HOOK_EVENTS


def _dump(doc):
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


def _backup_path(target):
    return target.with_name(f"hooks.json.bak.{int(time.time())}")


def _clean_hook_handler(handler):
    """丢掉 Codex 不认的字段（如自造的 mode），保证 hooks.json 能被解析。"""
    if not isinstance(handler, dict) or handler.get("type") != "command":
        return handler
    return {k: v for k, v in handler.items() if k in HOOK_COMMAND_FIELDS}


def _clean_matcher_groups(groups):
    if not isinstance(groups, list):
        return []
    cleaned = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        entry = {}
        if isinstance(group.get("matcher"), str):
            entry["matcher"] = group["matcher"]
        hooks = [
            _clean_hook_handler(h) for h in group.get("hooks", []) if isinstance(h, dict)
        ]
        if hooks:
            entry["hooks"] = hooks
            cleaned.append(entry)
    return cleaned


def _normalize_events(events):
    """把任意来源的 事件名 -> groups 映射洗成 Codex 认的形状。"""
    out = {}
    if not isinstance(events, dict):
        return out
    for event in HOOK_EVENTS:
        groups = _clean_matcher_groups(events.get(event))
        if groups:
            out[event] = groups
    return out


def build_global_hooks(framework_home):
    """只装两条进化相关的 hook。

    项目级门禁（stop-gate 拦截停止、auto-push 自动推送、pre-tool-shell 杀端口、
    auto-lint 改用户文件）全局启用会误伤用户所有仓库，所以不装；
    需要时用 `project <dir>` 给单个项目装。
    """
    hooks_dir = framework_home / ".codex" / "hooks"
    root = str(framework_home)

    def cmd(script):
        return f'IDEA_HAMMER_ROOT="{root}" "{hooks_dir / script}"'

    return {
        "description": "IdeaHammer 全局 hook：只捕获进化信号，不含项目级门禁",
        "hooks": {
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": cmd("detect-feedback-signal.sh"),
                            "timeout": 5,
                            "statusMessage": "IdeaHammer 进化信号扫描",
                        }
                    ]
                }
            ],
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": cmd("check-evolution.sh"),
                            "timeout": 10,
                            "statusMessage": "IdeaHammer 进化检查",
                        }
                    ]
                }
            ],
        },
    }


def _events_of(data):
    events = data.get("hooks")
    if not isinstance(events, dict):
        events = data.get("events") if isinstance(data.get("events"), dict) else {}
    return events


def _find_our_group(groups, marker):
    return next(
        (
            index
            for index, group in enumerate(groups)
            if any(marker in h.get("command", "") for h in group.get("hooks", []))
        ),
        None,
    )


def _merge_events(events, ours, marker):
    """把 ours 的事件合并进 events：同名 hook 就地替换，其余追加。"""
    added = 0
    replaced = 0
    for event, entries in ours["hooks"].items():
        existing = events.setdefault(event, [])
        for entry in entries:
            hit = _find_our_group(existing, marker)
            if hit is None:
                existing.append(entry)
                added += 1
            else:
                existing[hit] = entry
                replaced += 1
    return added, replaced


def _merged_description(data):
    description = data.get("description") or ""
    note = "含 IdeaHammer 全局进化 hook"
    if note not in description:
        description = (description + " | " if description else "") + note
    return description


def _merge_into(target, ours, marker):
    """读取已有 hooks.json，合并 ours 后写回；返回 (新增数, 更新数)。"""
    data = json.loads(target.read_text(encoding="utf-8"))
    events = _normalize_events(_events_of(data))
    added, replaced = _merge_events(events, ours, marker)
    merged = {"description": _merged_description(data), "hooks": events}
    shutil.copy2(target, _backup_path(target))
    target.write_text(_dump(merged), encoding="utf-8")
    return added, replaced


def write_global_hooks(codex_home, framework_home):
    target = codex_home / "hooks.json"
    ours = build_global_hooks(framework_home)

    if not target.exists():
        target.write_text(_dump(ours), encoding="utf-8")
        return target, "已创建"

    try:
        added, replaced = _merge_into(target, ours, str(framework_home))
    except json.JSONDecodeError as exc:
        backup = _backup_path(target)
        shutil.copy2(target, backup)
        warn(f"原 hooks.json 解析失败（{exc}），已备份到 {backup.name}，改用全新文件")
        target.write_text(_dump(ours), encoding="utf-8")
        return target, "已替换"

    parts = []
    if added:
        parts.append(f"+{added}")
    if replaced:
        parts.append(f"更新{replaced}")
    return target, f"已合并（{'，'.join(parts) if parts else '无变化'}）"


def _strip_ours(groups):
    kept = []
    removed = 0
    for group in groups:
        hooks = [
            h for h in group.get("hooks", [])
            if "/idea-hammer/" not in h.get("command", "")
        ]
        removed += len(group.get("hooks", [])) - len(hooks)
        if hooks:
            kept.append(dict(group, hooks=hooks))
    return kept, removed


def remove_global_hooks(codex_home):
    target = codex_home / "hooks.json"
    if not target.exists():
        return False
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False

    events = _events_of(data)
    removed = 0
    for event in list(events):
        kept, count = _strip_ours(events[event])
        removed += count
        if kept:
            events[event] = kept
        else:
            del events[event]

    if not removed:
        return False
    merged = {"description": data.get("description", ""), "hooks": events}
    target.write_text(_dump(merged), encoding="utf-8")
    return True
