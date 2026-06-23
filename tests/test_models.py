from lernatelier_checker.models import CheckboxStats, ComplianceResult, Status


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
        reflection_present=True,
        checkbox_stats=None,
    )
    defaults.update(kwargs)
    return ComplianceResult(**defaults)


def test_status_values():
    assert Status.GREEN.value == "green"
    assert Status.YELLOW.value == "yellow"
    assert Status.RED.value == "red"


def test_checkbox_stats_ratio_zero_total():
    assert CheckboxStats(total=0, checked=0).ratio == 0.0


def test_checkbox_stats_ratio():
    assert CheckboxStats(total=8, checked=2).ratio == 0.25


def test_grobplanung_complete():
    assert _result().grobplanung_complete is True


def test_grobplanung_incomplete_grades():
    assert _result(overview_grades=False).grobplanung_complete is False


def test_grobplanung_incomplete_one_section():
    assert _result(overview_goals=False).grobplanung_complete is False


def test_status_green():
    assert _result().status == Status.GREEN


def test_status_red_name_not_filled():
    assert _result(name_filled=False).status == Status.RED


def test_status_red_no_daily_entries():
    assert _result(daily_entries_count=0).status == Status.RED


def test_status_red_no_zeitraum():
    assert _result(zeitraum_present=False).status == Status.RED


def test_status_red_file_not_found():
    assert _result(file_found=False).status == Status.RED


def test_status_yellow_grobplanung_incomplete():
    assert _result(overview_grades=False).status == Status.YELLOW


def test_status_yellow_no_reflexion():
    assert _result(reflection_present=False).status == Status.YELLOW


def test_status_yellow_all_checkboxes_unchecked():
    cs = CheckboxStats(total=4, checked=0)
    assert _result(checkbox_stats=cs).status == Status.YELLOW


def test_status_green_with_some_checkboxes_checked():
    cs = CheckboxStats(total=4, checked=2)
    assert _result(checkbox_stats=cs).status == Status.GREEN


def test_status_green_no_checkboxes():
    assert _result(checkbox_stats=None).status == Status.GREEN
