@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\biweekly.log"
echo Inicio biweekly %date% %time% >> "%LOG_PATH%\biweekly.log"

"%PYTHON_PATH%" scripts\main.py --mode biweekly >> "%LOG_PATH%\biweekly.log" 2>&1

echo Fin biweekly %date% %time% >> "%LOG_PATH%\biweekly.log"
echo ========================================= >> "%LOG_PATH%\biweekly.log"

endlocal