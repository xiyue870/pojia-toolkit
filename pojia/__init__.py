"""PoJia-Toolkit — 破甲工具箱.

一个确定性路由的通用安全研究框架：口语输入 → 关键词分流 →
匹配到一条工作流（阶段链 + 主 skill）→ 输出可执行的路由回执与阶段计划。

本项目是方法论与工具骨架，面向安全研究、逆向分析、CTF、SRC 众测、
自有样本分析等场景。作者：曦月 (xiyue870)。
"""

__version__ = "1.0.0"
__author__ = "曦月 (xiyue870)"

from .engine.router import Router, RouteResult
from .engine.registry import Registry

__all__ = ["Router", "RouteResult", "Registry", "__version__"]
