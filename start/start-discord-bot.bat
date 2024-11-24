@echo off
REM Start de Discord bot met PM2
pm2 start bot.py --name "discord-bot" --interpreter "python" --cwd "D:/Github/Discord-bot-new"

REM Toon de status van alle processen
pm2 status

REM Laat het script draaien
pause