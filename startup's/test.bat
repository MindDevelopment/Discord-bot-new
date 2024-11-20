@echo off
:: Ga naar de root van je projectmap
cd /d "C:\Users\Administrator\Desktop\Discord-bot-new"

:: Zorg ervoor dat Python beschikbaar is
echo Checking Python path...
where python

:: Zorg ervoor dat PM2 beschikbaar is
echo Checking PM2 path...
where pm2

:: Controleer of bot.py bestaat
echo Checking if bot.py exists...
if exist "bot.py" (
    echo bot.py found.
) else (
    echo bot.py not found.
)

:: Controleer of app.py bestaat
echo Checking if app.py exists...
if exist "dashboard\app.py" (
    echo app.py found.
) else (
    echo app.py not found.
)

:: Start de bot via PM2 (bot.py bevindt zich in de root folder)
echo Starting bot.py with PM2...
pm2 start "C:\Users\Administrator\Desktop\Discord-bot-new\bot.py" --name "discord-bot" --interpreter "python"

:: Start de Flask-app via PM2 (app.py bevindt zich in de dashboard folder)
echo Starting app.py with PM2...
pm2 start "C:\Users\Administrator\Desktop\Discord-bot-new\dashboard\app.py" --name "flask-dashboard" --interpreter "python" > pm2_flask_log.txt 2>&1

:: Toont de status van alle PM2 processen
pm2 status

:: Houd de batchfile open zodat je logbestanden kunt controleren
pause
