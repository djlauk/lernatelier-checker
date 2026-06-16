# lernatelier-checker

Checks a Lernatelier planning document (`Lernperiode-N.md`) for completeness and returns a traffic-light status.

## Installation (Python)

```bash
pip install git+https://github.com/TEACHER/lernatelier-checker.git
```

## Installation (Windows, no Python)

Download `lernatelier-checker.exe` from the [Releases](../../releases) page and place it anywhere on your computer.

## Usage

```bash
lernatelier-checker Lernperiode-4.md
```

With English output:

```bash
lernatelier-checker Lernperiode-4.md --lang en
```

With an explicit config file:

```bash
lernatelier-checker Lernperiode-4.md --learning-period lernperiode.json
```

Exit code `0` = green (document complete), `1` = yellow or red (action needed).

### Config file (`lernperiode.json`)

The checker looks for `lernperiode.json` next to the document file. If found, it validates daily entries against the actual school days and checks the reflection deadline.

```json
{
  "learningperiod": 4,
  "days": [
    "2026-04-24",
    "2026-05-08",
    "2026-05-22",
    "2026-05-29",
    "2026-06-05",
    "2026-06-12",
    "2026-06-19",
    "2026-06-26"
  ]
}
```

`--learning-period <path>` overrides the default location. If no config is found (and none was explicitly given), date-based checks are skipped with a notice.

## Example output

```
Lernperiode-4.md

  FEHLER   Name nicht ausgefüllt – Platzhalter „Exemplibus Exemplio" entfernen
  FEHLER   Keine Tageseinträge gefunden
  WARNUNG  Abschnitt „Veränderungen" enthält nur Hilfsfragen
  WARNUNG  0 von 8 Checkboxen abgehakt

  ✓  Datei-Struktur erkannt
  ✓  Zeitraum gesetzt
  ✓  Grobplanung: Noten, Projekte, Ziele

2 Fehler, 2 Warnungen → 🔴 Handlungsbedarf
```

## Windows executable

The `.exe` must be built on Windows (PyInstaller does not cross-compile):

```bash
pip install pyinstaller
python build_exe.py
# Output: dist/lernatelier-checker.exe
```

Usage: run from cmd or drag a `Lernperiode-N.md` file onto the `.exe`:

```
lernatelier-checker.exe Lernperiode-4.md
```

A pre-built `.exe` can be attached to a GitHub Release for direct download — no installation needed.

## Source code

Source is open. Students are welcome to read it.
