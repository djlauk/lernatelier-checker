from datetime import date
from pathlib import Path

from lernatelier_checker.models import Status
from lernatelier_checker.parser import (
    NOT_FOUND,
    _checkbox_stats,
    _day_ok,
    _parse_day_sections,
    _real_content,
    _section_content,
    analyse,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_analyse_complete_fixture():
    content = (FIXTURES / "Lernperiode-4-complete.md").read_text(encoding="utf-8")
    result = analyse(content)
    assert result.file_found
    assert result.name_filled
    assert result.zeitraum_present
    assert result.daily_entries_count > 0
    assert result.status == Status.GREEN


def test_analyse_incomplete_fixture():
    content = (FIXTURES / "Lernperiode-4-incomplete.md").read_text(encoding="utf-8")
    result = analyse(content)
    assert not result.name_filled
    assert result.daily_entries_count == 0
    assert result.status == Status.RED


def test_analyse_always_sets_file_found_true():
    assert analyse("").file_found is True


def test_analyse_placeholder_name():
    assert analyse("- Name: Exemplibus Exemplio").name_filled is False


def test_analyse_real_name():
    assert analyse("- Name: Maria Muster").name_filled is True


def test_analyse_empty_name():
    assert analyse("- Name: ").name_filled is False


def test_analyse_no_name_field():
    assert analyse("# Lern-Periode 4\nKein Name hier").name_filled is False


def test_analyse_zeitraum_present():
    content = "- Zeitraum: 03.03.2025 bis 23.05.2025"
    assert analyse(content).zeitraum_present is True


def test_analyse_zeitraum_missing():
    assert analyse("- Name: Maria Muster").zeitraum_present is False


def test_analyse_daily_entries_count():
    content = "## 03.03.2025\nText\n## 04.03.2025\nMehr Text"
    assert analyse(content).daily_entries_count == 2


def test_analyse_planung_heading_counts_as_daily_entry():
    content = "## Planung 03.03.2025\nText"
    assert analyse(content).daily_entries_count == 1


def test_parse_day_sections_extracts_dates():
    content = "## 24.10.2025\n- [x] Task 1\nReflexion\n## 31.10.2025\n- [ ] Task 2\n"
    sections = _parse_day_sections(content)
    assert date(2025, 10, 24) in sections
    assert date(2025, 10, 31) in sections


def test_parse_day_sections_planung_heading():
    content = "## Planung 31.10.2025\n- [ ] Task\n"
    sections = _parse_day_sections(content)
    assert date(2025, 10, 31) in sections


def test_day_ok_all_checked_with_reflection():
    body = """\
- [x] Task 1
- [x] Task 2
- [x] Task 3
Heute habe ich viel über Python gelernt und bin gut vorangekommen.
"""
    assert _day_ok(body) is True


def test_day_ok_too_few_tasks():
    body = "- [x] Task 1\n- [x] Task 2\nGute Reflexion heute.\n"
    assert _day_ok(body) is False


def test_day_ok_too_many_tasks():
    body = "\n".join(f"- [x] Task {i}" for i in range(1, 7)) + "\nReflexion.\n"
    assert _day_ok(body) is False


def test_day_ok_unchecked_tasks():
    body = "- [x] Task 1\n- [ ] Task 2\n- [x] Task 3\nReflexion.\n"
    assert _day_ok(body) is False


def test_day_ok_no_reflection():
    body = "- [x] Task 1\n- [x] Task 2\n- [x] Task 3\n"
    assert _day_ok(body) is False


def test_analyse_days_ok_all_complete():
    period_days = [date(2025, 10, 24), date(2025, 10, 31)]
    today = date(2025, 10, 31)
    content = """\
## 24.10.2025
- [x] T1
- [x] T2
- [x] T3
Heute war ein produktiver Tag mit vielen Erkenntnissen.
## 31.10.2025
- [x] T1
- [x] T2
- [x] T3
Auch heute viel gelernt und die Ziele erreicht.
"""
    result = analyse(content, period_days=period_days, today=today)
    assert result.days_total == 2
    assert result.days_ok == 2


def test_analyse_days_ok_partial():
    period_days = [date(2025, 10, 24), date(2025, 10, 31)]
    today = date(2025, 10, 31)
    content = """\
## 24.10.2025
- [x] T1
- [x] T2
- [x] T3
Reflexion war gut heute, alle Aufgaben erledigt.
## 31.10.2025
- [ ] T1
- [ ] T2
- [ ] T3
"""
    result = analyse(content, period_days=period_days, today=today)
    assert result.days_total == 2
    assert result.days_ok == 1


def test_analyse_days_none_without_period_days():
    result = analyse("## 24.10.2025\n- [x] T1\n- [x] T2\n- [x] T3\nReflexion.\n")
    assert result.days_ok is None
    assert result.days_total is None


def test_not_found_file_found_false():
    assert NOT_FOUND.file_found is False


def test_not_found_status_red():
    assert NOT_FOUND.status == Status.RED


def test_real_content_empty():
    assert _real_content("") is False


def test_real_content_whitespace_only():
    assert _real_content("   \n  ") is False


def test_real_content_too_short():
    assert _real_content("kurz") is False


def test_real_content_placeholder_only():
    assert _real_content("Wo stehen Sie mit Ihren Noten im Vergleich zu letztem Semester?") is False


def test_real_content_real_text():
    text = "Ich möchte meine Noten in Mathematik verbessern und eine 5 erreichen."
    assert _real_content(text) is True


def test_real_content_mixed_placeholder_and_real():
    text = "Wo stehen Sie mit Ihren Noten?\nIch habe sehr gute Noten in Programmierung erzielt."
    assert _real_content(text) is True


def test_section_content_found():
    md = "## Noten\nInhalt hier\n## Nächstes Kapitel"
    assert "Inhalt" in _section_content(md, "Noten")


def test_section_content_missing():
    assert _section_content("## Anderes\nInhalt", "Noten") == ""


def test_section_content_at_end_of_file():
    md = "## Noten\nLetzter Abschnitt ohne nachfolgende Überschrift"
    assert "Letzter" in _section_content(md, "Noten")


def test_checkbox_stats_none_when_no_checkboxes():
    assert _checkbox_stats("Kein Checkbox hier") is None


def test_checkbox_stats_counts_checked_and_unchecked():
    md = "- [x] done\n- [ ] not done\n- [X] also done"
    stats = _checkbox_stats(md)
    assert stats is not None
    assert stats.total == 3
    assert stats.checked == 2


def test_checkbox_stats_all_unchecked():
    md = "- [ ] first\n- [ ] second"
    stats = _checkbox_stats(md)
    assert stats is not None
    assert stats.total == 2
    assert stats.checked == 0
