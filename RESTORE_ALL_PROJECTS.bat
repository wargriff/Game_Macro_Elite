@echo off
title RESTAURATION TOUS LES PROJETS
echo.
echo Lance le script PowerShell de restauration...
echo NE PAS lancer git clean depuis ce dossier parent !
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0RESTORE_ALL_PROJECTS.ps1"

pause
