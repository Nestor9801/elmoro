@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\daily_yesterday.log"
echo Inicio daily_minus_1 %date% %time% >> "%LOG_PATH%\daily_yesterday.log"

"%PYTHON_PATH%" scripts\main.py --mode daily_yesterday >> "%LOG_PATH%\daily_yesterday.log" 2>&1

echo Fin daily_minus_1 %date% %time% >> "%LOG_PATH%\daily_yesterday.log"
echo ========================================= >> "%LOG_PATH%\daily_yesterday.log"

endlocal