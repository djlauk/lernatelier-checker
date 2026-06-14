import argparse
import sys
from pathlib import Path

from .formatter import EnglishLinterFormatter, GermanLinterFormatter
from .parser import analyse


def main() -> int:
    """Usage: lernatelier-checker <path-to-markdown-file> [--lang de|en]

    Reads the file, runs analyse(), prints linter output to stdout.
    Returns exit code 0 for green, 1 for yellow or red.
    """
    parser = argparse.ArgumentParser(
        prog="lernatelier-checker",
        description="Check a Lernatelier planning document for completeness.",
    )
    parser.add_argument("file", type=Path, help="Path to the Markdown file")
    parser.add_argument(
        "--lang",
        choices=["de", "en"],
        default="de",
        help="Output language (default: de)",
    )
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    path: Path = args.file
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    content = path.read_text(encoding="utf-8")
    result = analyse(content)
    formatter = GermanLinterFormatter() if args.lang == "de" else EnglishLinterFormatter()
    print(formatter.format(result, path.name))

    return 0 if result.status.value == "green" else 1


if __name__ == "__main__":
    sys.exit(main())
