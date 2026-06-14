from pathlib import Path

from lernatelier_checker.models import Status
from lernatelier_checker.parser import NOT_FOUND, _checkbox_stats, _real_content, _section_content, analyse

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


def test_analyse_planning_entries_counted():
    content = "## Planung 03.03.2025\nText"
    assert analyse(content).daily_entries_count == 1


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
    assert _real_content("Ich möchte meine Noten in Mathematik verbessern und eine 5 erreichen.") is True


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
