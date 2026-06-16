import argparse
import json
import sys
from datetime import date
from importlib.metadata import version
from pathlib import Path

from .formatter import EnglishLinterFormatter, GermanLinterFormatter
from .parser import analyse

_CONFIG_NAME = "lernperiode.json"

_WARN_NO_CONFIG = {
    "de": (
        f"Hinweis: {_CONFIG_NAME} nicht gefunden – "
        "Tageseinträge und Reflexionsfrist werden nicht geprüft."
    ),
    "en": (
        f"Note: No {_CONFIG_NAME} found – "
        "daily entries and reflection deadline will not be checked."
    ),
}


def _load_learning_period_config(path: Path) -> list[date]:
    """Return config details, i.e. the list of days."""
    data = json.loads(path.read_text(encoding="utf-8"))
    days = [date.fromisoformat(d) for d in data.get("days", [])]
    return days


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="lernatelier-checker",
        description="Check a Lernatelier planning document for completeness.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('lernatelier-checker')}"
    )
    parser.add_argument("file", type=Path, help="Path to the Markdown file")
    parser.add_argument(
        "--lang",
        choices=["de", "en"],
        default="de",
        help="Output language (default: de)",
    )
    parser.add_argument("--learning-period", type=Path, help="Path to lernperiode.json")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    path: Path = args.file
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    lp_cfg = args.learning_period if args.learning_period else path.parent / _CONFIG_NAME
    if not lp_cfg.exists():
        if args.learning_period:  # explicitly given, but not present --> hard fail
            print(f"Config not found: {lp_cfg}", file=sys.stderr)
            return 1
        print(_WARN_NO_CONFIG[args.lang])
        print()
        period_days = None
    else:
        period_days = _load_learning_period_config(lp_cfg)

    content = path.read_text(encoding="utf-8")
    result = analyse(content, period_days=period_days, today=date.today())
    formatter = GermanLinterFormatter() if args.lang == "de" else EnglishLinterFormatter()
    print(formatter.format(result, path.name))

    return 0 if result.status.value == "green" else 1


if __name__ == "__main__":
    sys.exit(main())
