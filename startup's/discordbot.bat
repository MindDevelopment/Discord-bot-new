batch
@echo off
REM Change to the specified directory
SET targetDir=C:\Users\Administrator\Discord-bot-new

REM Check if the directory exists
IF EXIST "%targetDir%" (
    cd /d "%targetDir%"
    echo Successfully changed directory to %targetDir%

    REM Start the bot using pm2
    pm2 start bot.py --name "bot"
    IF ERRORLEVEL 1 (
        echo Error: Failed to start bot.py
        pause
        exit /b 1
    ) ELSE (
        echo Successfully started bot.py as "bot"
    )
