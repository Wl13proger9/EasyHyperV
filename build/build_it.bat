@echo off


python --version >nul 2>&1

if %errorlevel% equ 0 (
    python build.py
) else (
    echo Unfortunately, you don't have Python. Download it from the official website.
)

PAUSE