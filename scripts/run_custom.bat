@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

set FECHA_INICIO=2026/04/01
set FECHA_FIN=2026/04/30

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\custom.log"
echo Inicio custom %date% %time% >> "%LOG_PATH%\custom.log"
echo Rango %FECHA_INICIO% a %FECHA_FIN% >> "%LOG_PATH%\custom.log"

"%PYTHON_PATH%" scripts\main.py --mode custom --fecha-inicio %FECHA_INICIO% --fecha-fin %FECHA_FIN% >> "%LOG_PATH%\custom.log" 2>&1

echo Fin custom %date% %time% >> "%LOG_PATH%\custom.log"
echo ========================================= >> "%LOG_PATH%\custom.log"

endlocal
pause