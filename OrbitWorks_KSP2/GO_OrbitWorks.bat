@echo off
cd /d "%~dp0"
python python\generate_crafts.py
cd flutter_app
flutter pub get
flutter run -d windows
if errorlevel 1 flutter run -d chrome
pause
