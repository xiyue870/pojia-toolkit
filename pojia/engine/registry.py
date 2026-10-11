"""规则与工作流注册表。

数据通过 load() 从内置 JSON 加载，也可通过 register_rule() /
register_workflow() 动态扩展。引擎与数据分离：改规则不动引擎。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


class Registry:
    """持有路由规则、工作流阶段、默认回退配置。"""

    def __init__(
        self,
        rules: Optional[List[dict]] = None,
        workflows: Optional[Dict[str, List[str]]] = None,
        default_workflow: str = "universal",
        default_skill: str = "universal-workflow",
    ):
        self.rules = rules or []
        self.workflows = workflows or {}
        self.default_workflow = default_workflow
        self.default_skill = default_skill
        self.default_rule_id = "default"

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Registry":
        """从 JSON 数据文件加载注册表。默认加载内置 rules.json / workflows.json。"""
        if path is None:
            path = Path(__file__).resolve().parent.parent / "data"

        rules_file = path / "rules.json"
        workflows_file = path / "workflows.json"

        rules = json.loads(rules_file.read_text(encoding="utf-8-sig"))
        wf_data = json.loads(workflows_file.read_text(encoding="utf-8-sig"))

        return cls(
            rules=rules.get("rules", rules) if isinstance(rules, dict) else rules,
            workflows=wf_data.get("workflows", wf_data),
            default_workflow=wf_data.get("default_workflow", "universal"),
            default_skill=wf_data.get("default_skill", "universal-workflow"),
        )

    def register_rule(self, rule: dict) -> None:
        self.rules.append(rule)

    def register_workflow(self, name: str, stages: List[str]) -> None:
        self.workflows[name] = stages
