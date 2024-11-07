@echo off
cd "C:\Users\Administrator\Discord-bot-new"  REM Pad naar je bot-directory
git checkout development
git pull origin development
git checkout main
git merge development
git push origin main
