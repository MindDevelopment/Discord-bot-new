@echo off
D:
cd Github\Discord-bot-new
pm2 start bot.py --name "discord-bot" --interpreter "python"
pause
