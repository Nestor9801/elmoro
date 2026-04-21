@echo off
setlocal enabledelayedexpansion

echo =========================
echo INICIO run_elmoro.bat
echo =========================

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set SCRIPT_DIR=%PROJECT_PATH%\scripts
set SCRIPT_PATH=%SCRIPT_DIR%\main.py
set LOG_PATH=%PROJECT_PATH%\logs

echo PROJECT_PATH=%PROJECT_PATH%
echo PYTHON_PATH=%PYTHON_PATH%
echo SCRIPT_DIR=%SCRIPT_DIR%
echo SCRIPT_PATH=%SCRIPT_PATH%
echo LOG_PATH=%LOG_PATH%

if not exist "%PROJECT_PATH%" (
    echo ERROR: No existe PROJECT_PATH
    pause
    exit /b 1
)

if not exist "%PYTHON_PATH%" (
    echo ERROR: No existe PYTHON_PATH
    pause
    exit /b 1
)

if not exist "%SCRIPT_PATH%" (
    echo ERROR: No existe SCRIPT_PATH
    pause
    exit /b 1
)

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

echo ========================= >> "%LOG_PATH%\etl.log"
echo Iniciando proceso %date% %time% >> "%LOG_PATH%\etl.log"

cd /d "%SCRIPT_DIR%"
echo Carpeta actual:
cd

echo Ejecutando Python...
"%PYTHON_PATH%" "%SCRIPT_PATH%" >> "%LOG_PATH%\etl.log" 2>&1

set EXIT_CODE=%ERRORLEVEL%

echo Finalizando proceso %date% %time% >> "%LOG_PATH%\etl.log"
echo Exit code: %EXIT_CODE% >> "%LOG_PATH%\etl.log"
echo ========================= >> "%LOG_PATH%\etl.log"

echo.
echo Proceso terminado con exit code: %EXIT_CODE%
echo Revisa el log en: "%LOG_PATH%\etl.log"
pause
endlocal