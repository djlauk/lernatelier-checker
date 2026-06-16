from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Status(str, Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


@dataclass
class CheckboxStats:
    total: int
    checked: int

    @property
    def ratio(self) -> float:
        return self.checked / self.total if self.total > 0 else 0.0


@dataclass
class ComplianceResult:
    file_found: bool
    name_filled: bool
    zeitraum_present: bool
    overview_grades: bool
    overview_changes: bool
    overview_projects: bool
    overview_goals: bool
    daily_entries_count: int
    reflexion_present: bool
    checkbox_stats: Optional[CheckboxStats]
    days_ok: Optional[int] = None
    days_total: Optional[int] = None
    next_day_planned: Optional[bool] = None

    @property
    def grobplanung_complete(self) -> bool:
        return all(
            [
                self.overview_grades,
                self.overview_changes,
                self.overview_projects,
                self.overview_goals,
            ]
        )

    @property
    def status(self) -> Status:
        if not self.file_found:
            return Status.RED
        if not self.name_filled:
            return Status.RED
        if self.daily_entries_count == 0:
            return Status.RED
        if not self.zeitraum_present:
            return Status.RED
        if not self.grobplanung_complete:
            return Status.YELLOW
        if not self.reflexion_present:
            return Status.YELLOW
        if self.checkbox_stats is not None and self.checkbox_stats.checked == 0:
            return Status.YELLOW
        if self.days_total is not None and self.days_ok < self.days_total:
            return Status.YELLOW
        if self.next_day_planned is False:
            return Status.YELLOW
        return Status.GREEN
