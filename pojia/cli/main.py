"""命令行入口。

两种模式：
1. 单次路由：  pojia route "帮我逆向这个 exe"
2. 交互面板：  pojia repl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..engine.router import Router
from ..engine.registry import Registry
from .. import __version__


def _load_router() -> Router:
    return Router(Registry.load())


def cmd_route(prompt: str, as_json: bool = False) -> int:
    router = _load_router()
    result = router.route(prompt)
    if as_json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.receipt)
        print(f"命中关键词: {result.matched_terms or '(无，走默认链路)'}")
        print(f"阶段链 ({len(result.stages)}):")
        for i, s in enumerate(result.stages, 1):
            print(f"  [{i}] {s}")
    return 0


def cmd_list() -> int:
    router = _load_router()
    print("已注册工作流与阶段链：")
    for name, stages in router.registry.workflows.items():
        print(f"  {name:<16} -> {' → '.join(stages)}")
    print(f"\n规则总数: {len(router.registry.rules)}")
    return 0


def cmd_repl() -> int:
    router = _load_router()
    print(f"PoJia-Toolkit 破甲工具箱 v{__version__}")
    print("输入描述自动路由；输入 :list 查看全部链路；:quit 退出。")
    while True:
        try:
            raw = input("pojia> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        if raw in (":quit", ":q", "exit"):
            break
        if raw in (":list", ":ls"):
            cmd_list()
            continue
        result = router.route(raw)
        print(result.receipt)
        print(f"  命中: {result.matched_terms or '(默认)'} | 阶段: {' → '.join(result.stages)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pojia", description="破甲工具箱 — 确定性路由安全研究框架")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")

    r = sub.add_parser("route", help="单次路由")
    r.add_argument("prompt", help="任务描述")
    r.add_argument("--json", action="store_true", help="以 JSON 输出")

    sub.add_parser("list", help="列出全部工作流")

    sub.add_parser("repl", help="进入交互面板")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "route":
        return cmd_route(args.prompt, as_json=args.json)
    if args.command == "list":
        return cmd_list()
    if args.command == "repl":
        return cmd_repl()
    # 无子命令：若有位置参数则当作 route 的 prompt，否则进入 repl
    if args.command is None:
        return cmd_repl()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
