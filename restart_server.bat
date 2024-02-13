@echo off
REM we just do this twice cuz thing's dumb and rewrites the INI when server is stopped.
REM Palworld for some reason needs a "worldoptions.sav" to apply some settings instead of the .ini. This converts the .ini into said worldoptions.sav for us, then kills the converter EXE after.
"C:\Users\Admin\Desktop\PALWORLD_SCRIPTS\palworld-worldoptions.exe" --output "C:\steamcmd\steamapps\common\PalServer\Pal\Saved\SaveGames\0\D8B256124C7CD756E1075F989F820327" "C:\steamcmd\steamapps\common\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini"

"C:\Users\Admin\Desktop\PALWORLD_SCRIPTS\stop_server.py"

set oldCD=%cd%
cd C:\steamcmd\steamapps\common\PalServer

taskkill /IM PalServer-Win64-Test-Cmd.exe /F 2>nul >nul
taskkill /IM PalServer.exe /F 2>nul >nul
taskkill /IM python.exe /F 2>nul >nul
taskkill /IM py.exe /F 2>nul >nul

REM Palworld for some reason needs a "worldoptions.sav" to apply some settings instead of the .ini. This converts the .ini into said worldoptions.sav for us, then kills the converter EXE after.
start "" "C:\Users\Admin\Desktop\PALWORLD_SCRIPTS\palworld-worldoptions.exe" --output "C:\steamcmd\steamapps\common\PalServer\Pal\Saved\SaveGames\0\D8B256124C7CD756E1075F989F820327" "C:\steamcmd\steamapps\common\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini"
timeout /t 2 /nobreak >nul 2>nul
taskkill /IM palworld-worldoptions.exe /F

start "" PalServer.exe -port=8211 -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS

REM nosteam version below. Might bork saves though!
REM start "" PalServer.exe -port=8211 -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS -nosteam

timeout /t 10 /nobreak >nul 2>nul

start "" "C:\Users\Admin\Desktop\PALWORLD_SCRIPTS\watchdog.py"

cd "%oldCD%"