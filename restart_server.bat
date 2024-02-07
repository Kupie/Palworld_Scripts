@echo off
"C:\Users\Admin\Desktop\PALWORLD_SCRIPTS\stop_server.py"

set oldCD=%cd%
cd C:\steamcmd\steamapps\common\PalServer

taskkill /IM PalServer-Win64-Test-Cmd.exe /F 2>nul >nul
taskkill /IM PalServer.exe /F 2>nul >nul
taskkill /IM python.exe /F 2>nul >nul
taskkill /IM py.exe /F 2>nul >nul


start "" PalServer.exe -port=8211 -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS

REM nosteam version below. Might bork saves though!
REM start "" PalServer.exe -port=8211 -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS -nosteam

timeout /t 10 /nobreak >nul 2>nul

start "" "C:\Users\Admin\Desktop\PALWORLD_SCRIPTS\watchdog.py"

cd "%oldCD%"
