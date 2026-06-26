from dataclasses import dataclass
from enum import Enum

from .models import ComplianceResult, Status


class _Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    OK = "ok"


@dataclass
class _CheckItem:
    severity: _Severity
    message_de: str
    message_en: str


def _compute_checks(result: ComplianceResult) -> list[_CheckItem]:
    items: list[_CheckItem] = []

    if not result.file_found:
        items.append(
            _CheckItem(
                _Severity.ERROR, "Datei-Struktur nicht erkannt", "File structure not recognized"
            )
        )
        return items

    items.append(_CheckItem(_Severity.OK, "Datei-Struktur erkannt", "File structure recognized"))

    if result.name_filled:
        items.append(_CheckItem(_Severity.OK, "Name ausgefüllt", "Name filled"))
    else:
        items.append(
            _CheckItem(
                _Severity.ERROR,
                "Name nicht ausgefüllt – Platzhalter „Exemplibus Exemplio“ entfernen",
                "Name not filled – remove placeholder “Exemplibus Exemplio”",
            )
        )

    if result.zeitraum_present:
        items.append(_CheckItem(_Severity.OK, "Zeitraum gesetzt", "Time range set"))
    else:
        items.append(_CheckItem(_Severity.ERROR, "Zeitraum nicht gesetzt", "Time range not set"))

    grobplanung_ok: list[str] = []
    if result.overview_grades:
        grobplanung_ok.append("Noten")
    else:
        items.append(
            _CheckItem(
                _Severity.WARNING,
                "Abschnitt „Noten“ enthält nur Hilfsfragen",
                "Section “Noten” contains only placeholder text",
            )
        )
    if result.overview_changes:
        grobplanung_ok.append("Veränderungen")
    else:
        items.append(
            _CheckItem(
                _Severity.WARNING,
                "Abschnitt „Veränderungen“ enthält nur Hilfsfragen",
                "Section “Veränderungen” contains only placeholder text",
            )
        )
    if result.overview_projects:
        grobplanung_ok.append("Projekte")
    else:
        items.append(
            _CheckItem(
                _Severity.WARNING,
                "Abschnitt „Projekte / neue Technologien“ enthält nur Hilfsfragen",
                "Section “Projekte / neue Technologien” contains only placeholder text",
            )
        )
    if result.overview_goals:
        grobplanung_ok.append("Ziele")
    else:
        items.append(
            _CheckItem(
                _Severity.WARNING,
                "Abschnitt „Generelle Ziele“ enthält nur Hilfsfragen",
                "Section “Generelle Ziele” contains only placeholder text",
            )
        )
    if grobplanung_ok:
        sections = ", ".join(grobplanung_ok)
        items.append(_CheckItem(_Severity.OK, f"Grobplanung: {sections}", f"Overview: {sections}"))

    n = result.daily_entries_count
    if n > 0:
        de = f"{n} Tageseintrag" if n == 1 else f"{n} Tageseinträge"
        en = f"{n} daily entry" if n == 1 else f"{n} daily entries"
        items.append(_CheckItem(_Severity.OK, de, en))
    else:
        items.append(
            _CheckItem(_Severity.ERROR, "Keine Tageseinträge gefunden", "No daily entries found")
        )

    cs = result.checkbox_stats
    if cs is not None:
        if cs.checked == 0:
            items.append(
                _CheckItem(
                    _Severity.WARNING,
                    f"0 von {cs.total} Checkboxen abgehakt",
                    f"0 of {cs.total} checkboxes checked",
                )
            )
        else:
            items.append(
                _CheckItem(
                    _Severity.OK,
                    f"{cs.checked} von {cs.total} Checkboxen abgehakt",
                    f"{cs.checked} of {cs.total} checkboxes checked",
                )
            )

    if result.reflection_pending:
        due = result.reflection_due.strftime("%d.%m.%Y") if result.reflection_due else "?"
        items.append(
            _CheckItem(
                _Severity.OK,
                f"Reflexion ausstehend (fällig {due})",
                f"Reflection pending (due {due})",
            )
        )
    elif result.reflection_present:
        items.append(_CheckItem(_Severity.OK, "Reflexion vorhanden", "Reflection present"))
    else:
        items.append(
            _CheckItem(
                _Severity.WARNING,
                "Reflexion fehlt oder enthält nur Hilfsfragen",
                "Reflection missing or contains only placeholder text",
            )
        )

    if result.days_total is not None:
        ok, total = result.days_ok, result.days_total
        sev = _Severity.OK if ok == total else _Severity.WARNING
        items.append(
            _CheckItem(sev, f"Tage vollständig: {ok}/{total}", f"Days complete: {ok}/{total}")
        )
        absent = result.days_absent or 0
        if absent > 0:
            day_de = "Tag" if absent == 1 else "Tage"
            day_en = "day" if absent == 1 else "days"
            items.append(
                _CheckItem(_Severity.OK, f"{absent} {day_de} abwesend", f"{absent} {day_en} absent")
            )

    if result.next_day_planned is True:
        items.append(
            _CheckItem(
                _Severity.OK,
                "Nächster Kurstag geplant",
                "Next school day planned",
            )
        )
    elif result.next_day_planned is False:
        items.append(
            _CheckItem(
                _Severity.WARNING,
                "Nächster Kurstag nicht geplant – Arbeitspakete fehlen",
                "Next school day not planned – work packages missing",
            )
        )

    return items


def _render_linter(
    result: ComplianceResult, filename: str, items: list[_CheckItem], lang: str
) -> str:
    errors = [
        item.message_de if lang == "de" else item.message_en
        for item in items
        if item.severity == _Severity.ERROR
    ]
    warnings = [
        item.message_de if lang == "de" else item.message_en
        for item in items
        if item.severity == _Severity.WARNING
    ]
    passes = [
        item.message_de if lang == "de" else item.message_en
        for item in items
        if item.severity == _Severity.OK
    ]

    error_label = "FEHLER" if lang == "de" else "ERROR"
    warning_label = "WARNUNG" if lang == "de" else "WARNING"

    lines = [filename, ""]
    for msg in errors:
        lines.append(f"  {error_label:<8} {msg}")
    for msg in warnings:
        lines.append(f"  {warning_label:<8} {msg}")
    if errors or warnings:
        lines.append("")
    for msg in passes:
        lines.append(f"  ✓  {msg}")
    lines.append("")

    n_errors = len(errors)
    n_warnings = len(warnings)
    status = result.status

    if lang == "de":
        count_str = f"{n_errors} Fehler, {n_warnings} Warnungen"
        phrase = {
            Status.RED: "\U0001f534 Handlungsbedarf",
            Status.YELLOW: "\U0001f7e1 Verbesserungsbedarf",
            Status.GREEN: "\U0001f7e2 Alles in Ordnung",
        }[status]
    else:
        count_str = (
            f"{n_errors} error{'s' if n_errors != 1 else ''}, "
            f"{n_warnings} warning{'s' if n_warnings != 1 else ''}"
        )
        phrase = {
            Status.RED: "\U0001f534 action needed",
            Status.YELLOW: "\U0001f7e1 improvements needed",
            Status.GREEN: "\U0001f7e2 all good",
        }[status]

    lines.append(f"{count_str} → {phrase}")
    return "\n".join(lines)


class GermanLinterFormatter:
    """Console output in the style of a linter, German messages."""

    def format(self, result: ComplianceResult, filename: str) -> str:
        return _render_linter(result, filename, _compute_checks(result), "de")


class EnglishLinterFormatter:
    """Console output in the style of a linter, English messages."""

    def format(self, result: ComplianceResult, filename: str) -> str:
        return _render_linter(result, filename, _compute_checks(result), "en")


class JsonFormatter:
    """JSON-serializable dict representation of a ComplianceResult."""

    def format(self, result: ComplianceResult) -> dict:
        return {
            "status": result.status.value,
            "file_found": result.file_found,
            "name_filled": result.name_filled,
            "zeitraum_present": result.zeitraum_present,
            "overview_grades": result.overview_grades,
            "overview_changes": result.overview_changes,
            "overview_projects": result.overview_projects,
            "overview_goals": result.overview_goals,
            "daily_entries_count": result.daily_entries_count,
            "reflection_present": result.reflection_present,
            "checkbox_stats": (
                {"total": result.checkbox_stats.total, "checked": result.checkbox_stats.checked}
                if result.checkbox_stats is not None
                else None
            ),
            "days_ok": result.days_ok,
            "days_absent": result.days_absent,
            "days_total": result.days_total,
            "next_day_planned": result.next_day_planned,
            "reflection_due": result.reflection_due,
            "reflection_pending": result.reflection_pending,
        }
