"""argparse 定义与安装器入口。"""

import argparse

from .commands import do_install, do_project, do_status, do_uninstall
from .console import die
from .paths import DEFAULT_CODEX_HOME, DEFAULT_FRAMEWORK_HOME, DEFAULT_SKILLS_DIR

COMMANDS = {
    "install": do_install,
    "sync": do_install,
    "status": do_status,
    "uninstall": do_uninstall,
    "project": do_project,
}


def build_parser():
    parser = argparse.ArgumentParser(
        description="IdeaHammer 全局安装器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="install",
        choices=["install", "sync", "status", "uninstall", "project"],
        help="要执行的操作（默认 install）",
    )
    parser.add_argument("--framework-home", default=str(DEFAULT_FRAMEWORK_HOME),
                        help=f"框架副本位置（默认 {DEFAULT_FRAMEWORK_HOME}）")
    parser.add_argument("--skills-dir", default=str(DEFAULT_SKILLS_DIR),
                        help=f"全局技能目录（默认 {DEFAULT_SKILLS_DIR}）")
    parser.add_argument("--codex-home", default=str(DEFAULT_CODEX_HOME),
                        help=f"Codex 配置目录（默认 {DEFAULT_CODEX_HOME}）")
    parser.add_argument("--source", default=None,
                        help="框架源码目录（默认用本脚本所在的仓库）")
    parser.add_argument("--no-hooks", action="store_true", help="不写全局 hooks.json")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的同名文件")
    parser.add_argument("--project-dir", default=None, help="project 命令的目标项目目录")
    return parser


def run(args):
    if args.command == "project" and not args.project_dir:
        die("project 命令需要 --project-dir")
    COMMANDS[args.command](args)


def main():
    run(build_parser().parse_args())
