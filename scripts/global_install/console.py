"""终端输出助手：安装器的所有文案都从这里走。"""

import sys


def log(msg):
    print(msg, flush=True)


def ok(msg):
    print(f"  ✓ {msg}", flush=True)


def warn(msg):
    print(f"  ! {msg}", flush=True)


def die(msg):
    print(f"\n✗ {msg}", file=sys.stderr)
    raise SystemExit(1)
