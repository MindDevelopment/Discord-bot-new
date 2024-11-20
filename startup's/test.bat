@echo off
:: Ga naar de root van je projectmap
cd /d "C:\Users\Administrator\Desktop\Discord-bot-new"

:: Start de bot via PM2
pm2 start bot.py --name "discord-bot" --interpreter python

:: Start de Flask-app via PM2
pm2 start dashboard\app.py --name "flask-dashboard" --interpreter python

:: Toont de status van alle PM2 processen
pm2 status

pause
