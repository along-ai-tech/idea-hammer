#!/usr/bin/env python3
"""
install_global.py — IdeaHammer 全局安装器

把框架装到 Codex 的全局位置，让所有项目都能用上这套方法论：
  - 框架主体   → ~/.codex/idea-hammer/      稳定副本，不受源码目录移动影响
  - 技能       → ~/.agents/skills/<skill>     Codex 全局技能根目录
  - 方法论入口 → ~/.codex/AGENTS.md           全局 AGENTS.md，所有项目自动生效
  - 子 Agent   → ~/.codex/agents/*.toml       code-reviewer / evolution-runner
  - 进化 hook  → ~/.codex/hooks.json          只装安全的信号捕获

用法：
  python3 scripts/install_global.py install     # 首次安装
  python3 scripts/install_global.py sync        # 源码更新后同步到全局副本
  python3 scripts/install_global.py status      # 查看安装状态
  python3 scripts/install_global.py uninstall   # 卸载
  python3 scripts/install_global.py project DIR # 给单个项目装全套门禁 hook（可选）

实现见 global_install/ 包；本文件只保留入口。
"""

from global_install.cli import main

if __name__ == "__main__":
    main()
