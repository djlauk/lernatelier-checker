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

Exit code `0` = green (document complete), `1` = yellow or red (action needed).

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
