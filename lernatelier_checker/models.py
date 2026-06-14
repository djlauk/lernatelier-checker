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
    planning_entries_count: int
    reflexion_present: bool
    checkbox_stats: Optional[CheckboxStats]

    @property
    def grobplanung_complete(self) -> bool:
        return all([
            self.overview_grades,
            self.overview_changes,
            self.overview_projects,
            self.overview_goals,
        ])

    @property
    def status(self) -> Status:
        if not self.file_found:
            return Status.RED
        if not self.name_filled or self.daily_entries_count == 0 or not self.zeitraum_present:
            return Status.RED
        if (
            not self.grobplanung_complete
            or not self.reflexion_present
            or (self.checkbox_stats is not None and self.checkbox_stats.checked == 0)
        ):
            return Status.YELLOW
        return Status.GREEN
