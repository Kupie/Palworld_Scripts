@echo OFF
cd /D "%~dp0"
NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO.
) ELSE (
   echo ######## ########  ########   #######  ########  
   echo ##       ##     ## ##     ## ##     ## ##     ## 
   echo ##       ##     ## ##     ## ##     ## ##     ## 
   echo ######   ########  ########  ##     ## ########  
   echo ##       ##   ##   ##   ##   ##     ## ##   ##   
   echo ##       ##    ##  ##    ##  ##     ## ##    ##  
   echo ######## ##     ## ##     ##  #######  ##     ## 
   echo.
   echo.
   echo ####### ERROR: ADMINISTRATOR PRIVILEGES REQUIRED #########
   echo This script must be run as administrator to work properly!  
   echo If you're seeing this, you did not right click and select "Run As Administrator".
   echo ##########################################################
   echo.
   PAUSE
   EXIT /B 1
)
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

set FOLDER_TO_BACKUP=C:\steamcmd\steamapps\common\PalServer\Pal\Saved\SaveGames\0\D8B256124C7CD756E1075F989F820327
set FOLDER_TO_BACKUP_TO=C:\Users\Admin\Desktop\SAVE_BACKUP\

FOR /F "skip=1" %%A IN ('WMIC OS GET LOCALDATETIME') DO (SET "t=%%A" & GOTO break_1)
:break_1
SET "m=%t:~10,2%" & SET "h=%t:~8,2%" & SET "d=%t:~6,2%" & SET "z=%t:~4,2%" & SET "y=%t:~0,4%"
IF !h! GTR 11 (SET /A "h-=12" & SET "ap=P" & IF "!h!"=="0" (SET "h=00") ELSE (IF !h! LEQ 9 (SET "h=0!h!"))) ELSE (SET "ap=A")

set filename=PALWORLD_BACKUP_%z%-%d%-%y%_%h%%m%%ap%M.zip

echo BACKING UP "%FOLDER_TO_BACKUP%" TO:
echo "%FOLDER_TO_BACKUP_TO%%filename%"

mkdir "%FOLDER_TO_BACKUP_TO%"  >nul 2>nul

tar.exe -a -c -f "%FOLDER_TO_BACKUP_TO%%filename%" "%FOLDER_TO_BACKUP%" >nul 2>nul

echo.
echo BACKUP COMPLETE
