"""路由引擎单元测试。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pojia import Router, Registry


def test_route_reverse():
    r = Router(Registry.load())
    res = r.route("帮我逆向这个 exe 找注册逻辑")
    assert res.workflow == "reverse"
    assert "preserve" in res.stages
    assert not res.fallback


def test_route_pentest():
    r = Router(Registry.load())
    res = r.route("这个网站有 sql 注入吗")
    assert res.workflow == "pentest"
    assert "enumerate" in res.stages


def test_route_pojia():
    r = Router(Registry.load())
    res = r.route("帮我做破甲，绕过安装目录守卫")
    assert res.workflow == "pojia"


def test_route_crack():
    r = Router(Registry.load())
    res = r.route("这个 crackme 怎么破解序列号")
    assert res.workflow == "crack"


def test_route_fallback():
    r = Router(Registry.load())
    res = r.route("今天天气不错")
    assert res.fallback
    assert res.workflow == "universal"


def test_short_token_boundary():
    # "exe" 不应命中 "execute"
    r = Router(Registry.load())
    res = r.route("execute the plan")
    assert res.workflow != "reverse"


def test_receipt_format():
    r = Router(Registry.load())
    res = r.route("逆向")
    assert res.receipt.startswith("[POJIA ROUTE]")


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
