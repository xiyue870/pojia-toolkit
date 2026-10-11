"""工作流执行器。

每个工作流是一组有序阶段，执行器按顺序推进，逐阶段产出进度日志。
执行器本身不绑定具体安全能力，只负责「阶段编排 + 进度可见」，
具体动作由外部 skill / 工具接入。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class StageReport:
    """单个阶段的执行报告。"""

    name: str
    status: str  # pending | running | done | skipped | failed
    note: str = ""


@dataclass
class RunReport:
    """一次工作流执行的完整报告。"""

    workflow: str
    stages: List[StageReport] = field(default_factory=list)
    ok: bool = True

    def add(self, stage: str, status: str, note: str = "") -> None:
        self.stages.append(StageReport(stage, status, note))
        if status in ("failed",):
            self.ok = False

    def to_dict(self) -> dict:
        return {
            "workflow": self.workflow,
            "ok": self.ok,
            "stages": [s.__dict__ for s in self.stages],
        }


class Executor:
    """顺序执行工作流阶段。

    handler 是可选回调：handler(stage_name, ctx) -> str（备注）。
    若某阶段 handler 抛异常，该阶段标记 failed，后续阶段标记 skipped。
    """

    def __init__(
        self,
        handler: Optional[Callable[[str, dict], str]] = None,
    ):
        self.handler = handler

    def run(self, workflow: str, stages: List[str], ctx: Optional[dict] = None) -> RunReport:
        ctx = ctx or {}
        report = RunReport(workflow=workflow)
        failed = False
        for stage in stages:
            if failed:
                report.add(stage, "skipped", "上游阶段失败，跳过")
                continue
            report.add(stage, "running")
            if self.handler is None:
                report.stages[-1].status = "done"
                continue
            try:
                note = self.handler(stage, ctx)
                report.stages[-1].status = "done"
                report.stages[-1].note = note or ""
            except Exception as exc:  # noqa: BLE001
                report.add(stage, "failed", str(exc))
                failed = True
        return report
