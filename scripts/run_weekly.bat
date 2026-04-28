@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\weekly.log"
echo Inicio weekly %date% %time% >> "%LOG_PATH%\weekly.log"

"%PYTHON_PATH%" scripts\main.py --mode weekly >> "%LOG_PATH%\weekly.log" 2>&1

echo Fin weekly %date% %time% >> "%LOG_PATH%\weekly.log"
echo ========================================= >> "%LOG_PATH%\weekly.log"

endlocal