@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\monthly.log"
echo Inicio monthly %date% %time% >> "%LOG_PATH%\monthly.log"

"%PYTHON_PATH%" scripts\main.py --mode monthly >> "%LOG_PATH%\monthly.log" 2>&1

echo Fin monthly %date% %time% >> "%LOG_PATH%\monthly.log"
echo ========================================= >> "%LOG_PATH%\monthly.log"

endlocal