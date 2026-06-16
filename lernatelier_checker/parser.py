import re
from datetime import date
from typing import Optional

from .models import CheckboxStats, ComplianceResult

_PLACEHOLDER_NAME = "Exemplibus Exemplio"

# Whole-line placeholders: lines containing these are entirely template prompt text
_PLACEHOLDER_SENTENCES = [
    "Wo stehen Sie mit Ihren Noten",
    "Was möchten Sie generell im Vergleich",
    "Was für Projekte/neue Technologien",
    "Was haben Sie für klare und messbare Ziele",
]

# Sentence-starter placeholders: only the fragment itself is template text; student content follows
_PLACEHOLDER_STARTERS = [
    "In dieser Lernperiode habe ich",
    "Heute habe ich",
]

_PLACEHOLDER_FRAGMENTS = _PLACEHOLDER_SENTENCES + _PLACEHOLDER_STARTERS

_MIN_REAL_CHARS = 20

_DATE_HEADING = re.compile(r"^#+\s+(?:Planung\s+)?(\d{1,2})\.(\d{1,2})\.(\d{4})\s*$", re.MULTILINE)
_ANY_HEADING = re.compile(r"^#+\s+", re.MULTILINE)


def _real_content(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    has_placeholder = any(f.lower() in stripped.lower() for f in _PLACEHOLDER_FRAGMENTS)
    if not has_placeholder:
        return len(stripped) >= _MIN_REAL_CHARS
    lines = [
        line
        for line in stripped.splitlines()
        if not any(s.lower() in line.lower() for s in _PLACEHOLDER_SENTENCES)
    ]
    cleaned = "\n".join(lines)
    for f in _PLACEHOLDER_STARTERS:
        cleaned = re.sub(re.escape(f), "", cleaned, flags=re.IGNORECASE)
    return len(cleaned.strip()) >= _MIN_REAL_CHARS


def _section_content(md: str, heading: str) -> str:
    pattern = rf"#+\s+{re.escape(heading)}\s*\n(.*?)(?=\n#+|\Z)"
    m = re.search(pattern, md, re.DOTALL)
    return m.group(1) if m else ""


def _checkbox_stats(md: str) -> Optional[CheckboxStats]:
    checked = len(re.findall(r"-\s+\[x\]", md, re.IGNORECASE))
    unchecked = len(re.findall(r"-\s+\[ \]", md))
    total = checked + unchecked
    return CheckboxStats(total=total, checked=checked) if total > 0 else None


def _parse_day_sections(content: str) -> dict[date, str]:
    """Extract body text of each date-headed section, keyed by date."""
    sections: dict[date, str] = {}
    matches = list(_DATE_HEADING.finditer(content))
    for i, m in enumerate(matches):
        try:
            d = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            continue
        body_start = m.end()
        next_h = _ANY_HEADING.search(content, body_start)
        body_end = next_h.start() if next_h else len(content)
        sections[d] = content[body_start:body_end]
    return sections


def _day_ok(body: str) -> bool:
    """True if section has 3-5 checkboxes, all checked, and real reflection text."""
    checked = len(re.findall(r"-\s+\[x\]", body, re.IGNORECASE))
    unchecked = len(re.findall(r"-\s+\[ \]", body))
    total = checked + unchecked
    if not (3 <= total <= 5):
        return False
    if checked < total:
        return False
    non_checkbox = "\n".join(
        line for line in body.splitlines() if not re.match(r"\s*-\s+\[.\]", line, re.IGNORECASE)
    )
    return _real_content(non_checkbox)


def _compute_day_compliance(content: str, period_days: list[date], today: date) -> tuple[int, int]:
    sections = _parse_day_sections(content)
    past_and_today = [d for d in period_days if d <= today]
    days_total = len(past_and_today)
    days_ok = sum(1 for d in past_and_today if d in sections and _day_ok(sections[d]))
    return days_ok, days_total


def analyse(
    content: str,
    period_days: Optional[list[date]] = None,
    today: Optional[date] = None,
) -> ComplianceResult:
    name_m = re.search(r"^(?:\s*-\s+)?Name:\s*(.+)$", content, re.MULTILINE)
    name_filled = bool(name_m) and name_m.group(1).strip() not in ("", _PLACEHOLDER_NAME)

    zeitraum_present = bool(
        re.search(
            r"(?:\s*-\s+)?(?:Zeitraum:\s*)?.+\d{1,2}\.\d{1,2}\.\d{4}\s*(?:bis|-)\s*\d{1,2}\.\d{1,2}\.\d{4}",
            content,
        )
    )

    daily_count = len(_DATE_HEADING.findall(content))

    reflexion_m = re.search(r"#+\s+Lernperiode Reflexion\s*\n(.*?)(?=\n#+|\Z)", content, re.DOTALL)
    reflexion_text = reflexion_m.group(1) if reflexion_m else ""
    reflexion_present = _real_content(reflexion_text)

    days_ok, days_total = None, None
    if period_days and today is not None:
        days_ok, days_total = _compute_day_compliance(content, period_days, today)

    return ComplianceResult(
        file_found=True,
        name_filled=name_filled,
        zeitraum_present=zeitraum_present,
        overview_grades=_real_content(_section_content(content, "Noten")),
        overview_changes=_real_content(_section_content(content, "Veränderungen")),
        overview_projects=_real_content(_section_content(content, "Projekte / neue Technologien")),
        overview_goals=_real_content(_section_content(content, "Generelle Ziele")),
        daily_entries_count=daily_count,
        reflexion_present=reflexion_present,
        checkbox_stats=_checkbox_stats(content),
        days_ok=days_ok,
        days_total=days_total,
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
    reflexion_present=False,
    checkbox_stats=None,
)
