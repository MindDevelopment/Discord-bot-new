@echo off
D:
cd Github\Discord-bot-new\dashboard
pm2 start app.py --name "flask-dashboard" --interpreter "python"
pause
