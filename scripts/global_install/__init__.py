"""IdeaHammer 全局安装器：把框架装到 Codex 全局位置。

模块划分：
  paths     常量与路径模型
  console   终端输出
  trust     hook 信任登记（config.toml）
  framework 框架副本同步与技能安装
  hooks     全局 hooks.json 构建 / 合并 / 移除
  agents    全局 AGENTS.md、子 Agent、项目级门禁 hook
  commands  install / sync / status / uninstall / project
  cli       argparse 与入口
"""
