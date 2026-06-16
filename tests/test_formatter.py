from lernatelier_checker.formatter import (
    EnglishLinterFormatter,
    GermanLinterFormatter,
    JsonFormatter,
)
from lernatelier_checker.models import CheckboxStats, ComplianceResult


def _result(**kwargs) -> ComplianceResult:
    defaults = dict(
        file_found=True,
        name_filled=True,
        zeitraum_present=True,
        overview_grades=True,
        overview_changes=True,
        overview_projects=True,
        overview_goals=True,
        daily_entries_count=3,
        reflexion_present=True,
        checkbox_stats=None,
    )
    defaults.update(kwargs)
    return ComplianceResult(**defaults)


def _red_result() -> ComplianceResult:
    return _result(name_filled=False, daily_entries_count=0)


class TestGermanLinterFormatter:
    def test_output_starts_with_filename(self):
        out = GermanLinterFormatter().format(_result(), "test.md")
        assert out.startswith("test.md")

    def test_green_no_fehler_no_warnung(self):
        out = GermanLinterFormatter().format(_result(), "test.md")
        assert "FEHLER" not in out
        assert "WARNUNG" not in out

    def test_green_shows_green_emoji(self):
        out = GermanLinterFormatter().format(_result(), "test.md")
        assert "🟢" in out

    def test_red_shows_fehler(self):
        out = GermanLinterFormatter().format(_red_result(), "test.md")
        assert "FEHLER" in out

    def test_red_shows_red_emoji(self):
        out = GermanLinterFormatter().format(_red_result(), "test.md")
        assert "🔴" in out

    def test_warning_for_missing_reflexion(self):
        out = GermanLinterFormatter().format(_result(reflexion_present=False), "test.md")
        assert "WARNUNG" in out
        assert "🟡" in out

    def test_checkbox_warning_shows_count(self):
        cs = CheckboxStats(total=4, checked=0)
        out = GermanLinterFormatter().format(_result(checkbox_stats=cs), "test.md")
        assert "WARNUNG" in out
        assert "0 von 4" in out

    def test_passes_shown_with_checkmark(self):
        out = GermanLinterFormatter().format(_result(), "test.md")
        assert "✓" in out

    def test_name_error_message(self):
        out = GermanLinterFormatter().format(_result(name_filled=False), "test.md")
        assert "Exemplibus Exemplio" in out

    def test_summary_line_present(self):
        out = GermanLinterFormatter().format(_red_result(), "test.md")
        assert "Fehler" in out
        assert "Warnungen" in out


class TestEnglishLinterFormatter:
    def test_error_not_fehler(self):
        out = EnglishLinterFormatter().format(_red_result(), "test.md")
        assert "ERROR" in out
        assert "FEHLER" not in out

    def test_warning_not_warnung(self):
        out = EnglishLinterFormatter().format(_result(reflexion_present=False), "test.md")
        assert "WARNING" in out
        assert "WARNUNG" not in out

    def test_green_message_english(self):
        out = EnglishLinterFormatter().format(_result(), "test.md")
        assert "all good" in out

    def test_red_message_english(self):
        out = EnglishLinterFormatter().format(_red_result(), "test.md")
        assert "action needed" in out

    def test_yellow_message_english(self):
        out = EnglishLinterFormatter().format(_result(reflexion_present=False), "test.md")
        assert "improvements needed" in out


class TestJsonFormatter:
    def test_returns_dict(self):
        assert isinstance(JsonFormatter().format(_result()), dict)

    def test_status_green(self):
        assert JsonFormatter().format(_result())["status"] == "green"

    def test_status_red(self):
        assert JsonFormatter().format(_red_result())["status"] == "red"

    def test_all_fields_present(self):
        data = JsonFormatter().format(_result())
        for field in [
            "status",
            "file_found",
            "name_filled",
            "zeitraum_present",
            "overview_grades",
            "overview_changes",
            "overview_projects",
            "overview_goals",
            "daily_entries_count",
            "reflexion_present",
            "checkbox_stats",
            "days_ok",
            "days_total",
        ]:
            assert field in data

    def test_checkbox_stats_serialized(self):
        cs = CheckboxStats(total=4, checked=2)
        data = JsonFormatter().format(_result(checkbox_stats=cs))
        assert data["checkbox_stats"] == {"total": 4, "checked": 2}

    def test_no_checkbox_stats_is_none(self):
        assert JsonFormatter().format(_result(checkbox_stats=None))["checkbox_stats"] is None
