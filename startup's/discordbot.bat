@echo off
REM Start de Discord bot met PM2
pm2 start "C:\Users\Administrator\Desktop\Discord-bot-new\bot.py" --name "discord-bot" --interpreter "python"

REM Toon de status van alle processen
pm2 status

REM Laat het script draaien
pause
