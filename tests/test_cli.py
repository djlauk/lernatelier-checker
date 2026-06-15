import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "lernatelier_checker", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_complete_fixture_exits_zero():
    assert _run(str(FIXTURES / "Lernperiode-4-complete.md")).returncode == 0


def test_incomplete_fixture_exits_one():
    assert _run(str(FIXTURES / "Lernperiode-4-incomplete.md")).returncode == 1


def test_default_language_is_german():
    result = _run(str(FIXTURES / "Lernperiode-4-incomplete.md"))
    assert "FEHLER" in result.stdout


def test_lang_de_shows_german():
    result = _run(str(FIXTURES / "Lernperiode-4-incomplete.md"), "--lang", "de")
    assert "FEHLER" in result.stdout
    assert "ERROR" not in result.stdout


def test_lang_en_shows_english():
    result = _run(str(FIXTURES / "Lernperiode-4-incomplete.md"), "--lang", "en")
    assert "ERROR" in result.stdout
    assert "FEHLER" not in result.stdout


def test_output_contains_filename():
    result = _run(str(FIXTURES / "Lernperiode-4-complete.md"))
    assert "Lernperiode-4-complete.md" in result.stdout


def test_missing_file_exits_one_and_stderr():
    result = _run("nonexistent.md")
    assert result.returncode == 1
    assert result.stderr != ""
