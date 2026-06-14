import re
from typing import Optional

from .models import CheckboxStats, ComplianceResult

_PLACEHOLDER_NAME = "Exemplibus Exemplio"

_PLACEHOLDER_FRAGMENTS = [
    "Wo stehen Sie mit Ihren Noten",
    "Was möchten Sie generell im Vergleich",
    "Was für Projekte/neue Technologien",
    "Was haben Sie für klare und messbare Ziele",
    "In dieser Lernperiode habe ich",
    "Heute habe ich",
]

_MIN_REAL_CHARS = 20


def _real_content(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    for fragment in _PLACEHOLDER_FRAGMENTS:
        if fragment.lower() in stripped.lower():
            real = " ".join(
                line for line in stripped.splitlines()
                if not any(f.lower() in line.lower() for f in _PLACEHOLDER_FRAGMENTS)
            )
            return len(real.strip()) >= _MIN_REAL_CHARS
    return len(stripped) >= _MIN_REAL_CHARS


def _section_content(md: str, heading: str) -> str:
    pattern = rf"#+\s+{re.escape(heading)}\s*\n(.*?)(?=\n#+|\Z)"
    m = re.search(pattern, md, re.DOTALL)
    return m.group(1) if m else ""


def _checkbox_stats(md: str) -> Optional[CheckboxStats]:
    checked = len(re.findall(r"-\s+\[x\]", md, re.IGNORECASE))
    unchecked = len(re.findall(r"-\s+\[ \]", md))
    total = checked + unchecked
    return CheckboxStats(total=total, checked=checked) if total > 0 else None


def analyse(content: str) -> ComplianceResult:
    name_m = re.search(r"^(?:\s*-\s+)?Name:\s*(.+)$", content, re.MULTILINE)
    name_filled = bool(name_m) and name_m.group(1).strip() not in ("", _PLACEHOLDER_NAME)

    zeitraum_present = bool(
        re.search(
            r"(?:\s*-\s+)?(?:Zeitraum:\s*)?.+\d{1,2}\.\d{1,2}\.\d{4}\s*(?:bis|-)\s*\d{1,2}\.\d{1,2}\.\d{4}",
            content,
        )
    )

    daily_count = len(
        re.findall(r"^#+\s+(?:Planung\s+)?\d{1,2}\.\d{1,2}\.\d{4}$", content, re.MULTILINE)
    )

    reflexion_m = re.search(
        r"#+\s+Lernperiode Reflexion\s*\n(.*?)(?=\n#+|\Z)", content, re.DOTALL
    )
    reflexion_text = reflexion_m.group(1) if reflexion_m else ""
    reflexion_present = _real_content(reflexion_text)

    return ComplianceResult(
        file_found=True,
        name_filled=name_filled,
        zeitraum_present=zeitraum_present,
        overview_grades=_real_content(_section_content(content, "Noten")),
        overview_changes=_real_content(_section_content(content, "Veränderungen")),
        overview_projects=_real_content(
            _section_content(content, "Projekte / neue Technologien")
        ),
        overview_goals=_real_content(_section_content(content, "Generelle Ziele")),
        daily_entries_count=daily_count,
        planning_entries_count=0,
        reflexion_present=reflexion_present,
        checkbox_stats=_checkbox_stats(content),
    )


NOT_FOUND = ComplianceResult(
    file_found=False,
    name_filled=False,
    zeitraum_present=False,
    overview_grades=False,
    overview_changes=False,
    overview_projects=False,
    overview_goals=False,
    daily_entries_count=0,
    planning_entries_count=0,
    reflexion_present=False,
    checkbox_stats=None,
)
