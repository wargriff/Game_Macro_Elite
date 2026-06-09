@echo off
title Game XClicker Elite — Sanctuary Edition
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" Xmacro_main.py
) else if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" Xmacro_main.py
) else (
    python Xmacro_main.py
)

if errorlevel 1 pause
