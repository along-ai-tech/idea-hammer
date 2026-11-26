"""hook 信任登记：Codex 只执行 config.toml 里登记过 trusted_hash 的 handler。"""

import hashlib
import json
from pathlib import Path

from .paths import (
    DEFAULT_HOOK_OUTPUT_TOKEN_LIMIT,
    DEFAULT_HOOK_TIMEOUT_SEC,
    HOOK_CONTEXT_EVENTS,
    HOOK_EVENT_LABELS,
    SESSION_END_DEFAULT_TIMEOUT_SEC,
    SESSION_END_MAX_TIMEOUT_SEC,
)


def _resolve_timeout(event, timeout):
    """算出 handler 的生效 timeout（Codex 对不同事件有上下限）。"""
    if event in ("SessionEnd", "Interrupt"):
        if timeout is None:
            return SESSION_END_DEFAULT_TIMEOUT_SEC
        return min(timeout, SESSION_END_MAX_TIMEOUT_SEC)
    if timeout is None:
        return DEFAULT_HOOK_TIMEOUT_SEC
    return max(timeout, 1)


def hook_hash(event, matcher, handler):
    """复刻 Codex 的 hook_hash（codex-rs/hooks/src/engine/discovery.rs）。"""
    normalized = {
        "type": "command",
        "command": handler.get("command", ""),
        "timeout": _resolve_timeout(event, handler.get("timeout")),
        "async": bool(handler.get("async", False)),
    }
    status = handler.get("statusMessage")
    if status:
        normalized["statusMessage"] = status
    limit = handler.get("additionalContextLimit")
    if (
        event in HOOK_CONTEXT_EVENTS
        and limit is not None
        and limit != DEFAULT_HOOK_OUTPUT_TOKEN_LIMIT
    ):
        normalized["additionalContextLimit"] = limit

    identity = {"event_name": HOOK_EVENT_LABELS[event], "hooks": [normalized]}
    if matcher:
        identity["matcher"] = matcher
    blob = json.dumps(
        identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(blob).hexdigest()


def _iter_command_handlers(groups):
    """产出一个事件里所有 command 型 handler 的 (组序号, matcher, 序号, handler)。"""
    for group_index, group in enumerate(groups):
        if not isinstance(group, dict):
            continue
        matcher = group.get("matcher")
        for handler_index, handler in enumerate(group.get("hooks") or []):
            if not isinstance(handler, dict) or handler.get("type") != "command":
                continue
            yield group_index, matcher, handler_index, handler


def _iter_trust_candidates(hooks_doc):
    """产出 hooks 文档里所有可登记的 (event, label, 组序号, matcher, 序号, handler)。"""
    for event, groups in (hooks_doc.get("hooks") or {}).items():
        label = HOOK_EVENT_LABELS.get(event)
        if not label or not isinstance(groups, list):
            continue
        for group_index, matcher, handler_index, handler in _iter_command_handlers(groups):
            yield event, label, group_index, matcher, handler_index, handler


def collect_hook_trust(hooks_path, hooks_doc):
    """算出 hooks.json 里每个 handler 的 (信任 key, trusted_hash)。"""
    entries = []
    for event, label, group_index, matcher, handler_index, handler in (
        _iter_trust_candidates(hooks_doc)
    ):
        key = f"{hooks_path}:{label}:{group_index}:{handler_index}"
        entries.append((key, hook_hash(event, matcher, handler)))
    return entries


def _toml_quote_key(key):
    return '"' + key.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _find_table(lines, header):
    return next((i for i, line in enumerate(lines) if line.strip() == header), None)


def _table_end(lines, index):
    """表体结束于下一个表头。"""
    end = index + 1
    while end < len(lines) and not lines[end].lstrip().startswith("["):
        end += 1
    return end


def _append_table(lines, header, digest):
    if lines and lines[-1].strip():
        lines.append("")
    lines.append(header)
    lines.append(f'trusted_hash = "{digest}"')
    lines.append("")


def _set_table_hash(lines, index, digest):
    """就地更新表里的 trusted_hash，没有就插到表头下面。"""
    for i in range(index + 1, _table_end(lines, index)):
        if lines[i].strip().startswith("trusted_hash"):
            lines[i] = f'trusted_hash = "{digest}"'
            return
    lines.insert(index + 1, f'trusted_hash = "{digest}"')


def write_hook_trust(config_path, entries):
    """把 hook 的 trusted_hash 写进 config.toml 的 [hooks.state."<key>"] 表。"""
    if not entries:
        return 0
    path = Path(config_path)
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    lines = text.splitlines()

    for key, digest in entries:
        header = f"[hooks.state.{_toml_quote_key(key)}]"
        index = _find_table(lines, header)
        if index is None:
            _append_table(lines, header, digest)
        else:
            _set_table_hash(lines, index, digest)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8")
    return len(entries)


def _state_table_key(line):
    """认出一行是不是 [hooks.state."..."] 表头，是就返回 key。"""
    stripped = line.strip()
    if not stripped.startswith("[hooks.state.") or not stripped.endswith("]"):
        return None
    key = stripped[len("[hooks.state.") : -1].strip()
    if key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    return key


def _skip_table_body(lines, index):
    """从表头下一行开始，跳到下一个表头（表体结束）。"""
    i = index + 1
    while i < len(lines) and not lines[i].lstrip().startswith("["):
        i += 1
    return i


def remove_hook_trust(config_path, path_prefix):
    """删掉属于某个 hooks.json 的所有 [hooks.state."..."] 表。"""
    path = Path(config_path)
    if not path.is_file():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    removed = 0
    i = 0
    while i < len(lines):
        key = _state_table_key(lines[i])
        if key is not None and key.startswith(path_prefix):
            i = _skip_table_body(lines, i)
            removed += 1
            continue
        out.append(lines[i])
        i += 1
    if removed:
        path.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")
    return removed


def trust_hooks_file(hooks_path, codex_home):
    """把 hooks.json 里的 handler 登记为已信任。

    Codex 对用户级 hook 默认判 Untrusted，不登记就不会执行。信任状态写在
    Codex home 的 config.toml 里（只读 User 层），所以项目级 hook 也写同一处。
    """
    hooks_path = Path(hooks_path)
    if not hooks_path.is_file():
        return 0
    try:
        doc = json.loads(hooks_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0
    entries = collect_hook_trust(str(hooks_path), doc)
    return write_hook_trust(codex_home / "config.toml", entries)
