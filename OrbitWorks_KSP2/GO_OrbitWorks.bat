@echo off
cd /d "%~dp0"
python python\generate_crafts.py
python python\web_server.py
pause
