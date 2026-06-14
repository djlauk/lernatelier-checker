"""
Build script for a standalone Windows executable.

Usage:
    pip install pyinstaller
    python build_exe.py

Output: dist/lernatelier-checker.exe
"""
import PyInstaller.__main__

PyInstaller.__main__.run([
    "lernatelier_checker/__main__.py",
    "--name=lernatelier-checker",
    "--onefile",
    "--console",
])
