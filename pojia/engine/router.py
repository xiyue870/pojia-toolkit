"""确定性路由引擎。

设计原则（第一性原理）：
1. 路由是纯函数：输入 prompt，输出唯一的 (workflow, stages, skill)。
   没有随机性、没有隐式回退，结果可复现。
2. 关键词命中按「优先级 + 命中数量 + 规则 id」三级排序，取唯一胜者。
3. 无命中时回退到 default workflow（universal），并显式标记 fallback=True，
   绝不静默吞掉。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class RouteResult:
    """一次路由的完整结果。"""

    workflow: str
    stages: List[str]
    skill: str
    matched_terms: List[str]
    priority: int
    rule_id: str
    fallback: bool
    all_matches: List[dict] = field(default_factory=list)

    @property
    def receipt(self) -> str:
        """路由回执，约定作为可见回复的第一行。"""
        return (
            f"[POJIA ROUTE] workflow={self.workflow} | "
            f"stages={'→'.join(self.stages)} | skill={self.skill}"
        )

    def to_dict(self) -> dict:
        return {
            "workflow": self.workflow,
            "stages": self.stages,
            "skill": self.skill,
            "matched_terms": self.matched_terms,
            "priority": self.priority,
            "rule_id": self.rule_id,
            "fallback": self.fallback,
            "all_matches": self.all_matches,
            "receipt": self.receipt,
        }


class Router:
    """确定性单匹配路由器。

    数据来源是 Registry（rules + workflows），二者解耦，方便扩展规则
    而不动引擎逻辑。
    """

    # 短 token（<=4 个字母数字）走词边界匹配，避免 "pe" 误命中 "open"。
    _SHORT_TOKEN_RE = re.compile(r"[a-z0-9-]+", re.I)

    def __init__(self, registry: "Registry"):
        self.registry = registry

    @staticmethod
    def _hit(term: str, prompt: str) -> bool:
        term = term.casefold()
        prompt = prompt.casefold()
        if Router._SHORT_TOKEN_RE.fullmatch(term) and len(term) <= 4:
            # 词边界匹配，防止 "exe" 命中 "execute"
            return bool(
                re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", prompt)
            )
        return term in prompt

    def _match_rule(self, rule: dict, prompt: str) -> Tuple[List[str], int]:
        hits = [term for term in rule["terms"] if self._hit(term, prompt)]
        return hits, int(rule.get("priority", 0))

    def route(self, prompt: str) -> RouteResult:
        rules = self.registry.rules
        workflows = self.registry.workflows

        matches: List[dict] = []
        for rule in rules:
            hits, priority = self._match_rule(rule, prompt)
            if hits:
                matches.append({**rule, "hits": hits, "priority": priority})

        # 排序：优先级降序 → 命中数量降序 → 规则 id 升序（确定性）
        matches.sort(key=lambda x: (-x["priority"], -len(x["hits"]), x["id"]))

        if matches:
            selected = matches[0]
            fallback = False
        else:
            selected = {
                "id": self.registry.default_rule_id,
                "priority": 0,
                "workflow": self.registry.default_workflow,
                "primary_skill": self.registry.default_skill,
                "hits": [],
            }
            fallback = True

        workflow = selected["workflow"]
        stages = workflows.get(workflow, workflows.get(self.registry.default_workflow, []))
        skill = selected["primary_skill"]

        return RouteResult(
            workflow=workflow,
            stages=list(stages),
            skill=skill,
            matched_terms=selected.get("hits", []),
            priority=selected.get("priority", 0),
            rule_id=selected["id"],
            fallback=fallback,
            all_matches=[
                {"workflow": m["workflow"], "hits": m["hits"]} for m in matches
            ],
        )
