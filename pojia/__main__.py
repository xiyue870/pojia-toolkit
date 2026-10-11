"""PoJia-Toolkit 破甲工具箱入口。

用法：
    python -m pojia route "帮我逆向这个 exe"
    python -m pojia repl
"""
from .cli.main import main

if __name__ == "__main__":
    raise SystemExit(main())
