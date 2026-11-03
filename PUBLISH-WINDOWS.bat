@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0publish-github.ps1"
echo.
echo See the messages above for the repository URL and any required sign-in.
pause
