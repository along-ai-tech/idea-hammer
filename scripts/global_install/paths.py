"""全局安装器的常量与路径模型。"""

from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_CODEX_HOME = Path.home() / ".codex"
DEFAULT_FRAMEWORK_HOME = DEFAULT_CODEX_HOME / "idea-hammer"
DEFAULT_SKILLS_DIR = Path.home() / ".agents" / "skills"

BLOCK_START = "<!-- idea-hammer:global:start -->"
BLOCK_END = "<!-- idea-hammer:global:end -->"
MANIFEST_NAME = ".install-manifest.json"

# 同步框架时跳过的路径：版本控制、虚拟环境、缓存、本框架自身的会话状态。
EXCLUDE_NAMES = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".screenshots", ".idea-hammer", ".DS_Store",
    ".ruff_cache", ".mypy_cache", "dist", "build",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".log"}

# 共享资料目录：不含技能入口，但被其他技能用 ../ 相对路径引用，必须一起装，
# 否则 code-review 等技能读不到工程约束。
SHARED_SKILL_DIRS = {"_engineering-constraints", "_traceability"}

# _template 是新技能的脚手架，frontmatter 是占位符（name: <skill-name>），
# 装进技能目录会被当成真技能列进目录表，污染触发匹配，不装。
SKIP_SKILL_DIRS = {"_template"}

GLOBAL_AGENT_FILES = ["code-reviewer.toml", "evolution-runner.toml"]

# ------------------------------------------------- hook 信任（Codex 的硬性要求）

# Codex 对用户级 hooks.json 的 handler 默认判 Untrusted，不会执行。必须在
# config.toml 里写 [hooks.state."<key>"] trusted_hash 才生效（Codex 桌面端弹的
# "hook 审阅"框，批准后落的就是这个值）。
#
#   key  = <hooks.json 绝对路径>:<事件 snake_case>:<组序号>:<handler 序号>
#   hash = sha256(规范化后的 hook 身份 → 递归排序键的紧凑 JSON)

HOOK_EVENT_LABELS = {
    "PreModelRequest": "pre_model_request",
    "PostModelRequest": "post_model_request",
    "PreToolUse": "pre_tool_use",
    "PermissionRequest": "permission_request",
    "PostToolUse": "post_tool_use",
    "PreCompact": "pre_compact",
    "PostCompact": "post_compact",
    "SessionStart": "session_start",
    "SessionEnd": "session_end",
    "UserPromptSubmit": "user_prompt_submit",
    "SubagentStart": "subagent_start",
    "SubagentStop": "subagent_stop",
    "Stop": "stop",
    "Interrupt": "interrupt",
}

# 事件顺序即 HOOK_EVENT_LABELS 的插入顺序，hooks.json 里的事件顺序依赖它。
HOOK_EVENTS = tuple(HOOK_EVENT_LABELS)

# 只有这些事件能发 additionalContext，其余事件的 additionalContextLimit 会被 Codex 丢掉
HOOK_CONTEXT_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "SessionStart",
    "UserPromptSubmit",
    "SubagentStart",
}

DEFAULT_HOOK_TIMEOUT_SEC = 600
DEFAULT_HOOK_OUTPUT_TOKEN_LIMIT = 2500
SESSION_END_DEFAULT_TIMEOUT_SEC = 1
SESSION_END_MAX_TIMEOUT_SEC = 3

# Codex hook v1 schema（openai/codex rust-v0.171.0，见 codex-rs/protocol/src/hooks.rs）：
#   顶层只允许 description / hooks 两个字段（deny_unknown_fields）
#   hooks 是 事件名 -> [MatcherGroup] 的映射
#   MatcherGroup = { matcher?: string, hooks: [HookHandlerConfig] }
#   HookHandlerConfig(command) = { type:"command", command, commandWindows?, timeout?, async?,
#                                 statusMessage?, additionalContextLimit? }
# 不存在 mode / $version / events 这些自造字段，写了 Codex 直接拒绝整个文件。
HOOK_COMMAND_FIELDS = (
    "type",
    "command",
    "commandWindows",
    "timeout",
    "async",
    "statusMessage",
    "additionalContextLimit",
)


class InstallPaths(NamedTuple):
    """一次安装涉及的所有路径。"""

    framework_home: Path
    skills_dir: Path
    codex_home: Path
    source: Path


def paths_from_args(args):
    """从命令行参数解析出路径集合（source 默认取本仓库）。"""
    source = Path(args.source).expanduser().resolve() if args.source else REPO_ROOT
    return InstallPaths(
        Path(args.framework_home).expanduser().resolve(),
        Path(args.skills_dir).expanduser(),
        Path(args.codex_home).expanduser().resolve(),
        source,
    )
