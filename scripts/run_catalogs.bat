@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\catalogs.log"
echo Inicio catalogs %date% %time% >> "%LOG_PATH%\catalogs.log"

"%PYTHON_PATH%" scripts\main.py --mode catalogs >> "%LOG_PATH%\catalogs.log" 2>&1

echo Fin catalogs %date% %time% >> "%LOG_PATH%\catalogs.log"
echo ========================================= >> "%LOG_PATH%\catalogs.log"

endlocal
pause