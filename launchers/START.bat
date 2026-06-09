@echo off
REM Raccourci — lance START.bat a la racine du projet
cd /d "%~dp0.."
call START.bat %*
