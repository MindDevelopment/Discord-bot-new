@echo off
REM Start de Discord bot met PM2
pm2 start "%cd%\bot.py" --name "discord-bot" --interpreter "python"

REM Start het dashboard met PM2
pm2 start "%cd%\dashboard\app.py" --name "discord-dashboard" --interpreter "python"

REM Toon de status van alle processen
pm2 status

REM Laat het script draaien
pause
