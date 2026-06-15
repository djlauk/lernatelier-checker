"""
Build script for a standalone Windows executable.

Usage:
    pip install pyinstaller
    python build_exe.py

Output: dist/lernatelier-checker.exe
"""

import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "_entry.py",
        "--name=lernatelier-checker",
        "--onefile",
        "--console",
    ]
)
