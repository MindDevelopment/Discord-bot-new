@echo off
REM Start de Discord bot met PM2
pm2 start "D:\Github\Discord-bot-new\dashboard\app.py" --name "dashboard" --interpreter "python"

REM Toon de status van alle processen
pm2 status

REM Laat het script draaien
pause
