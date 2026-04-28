@echo off
setlocal

set PROJECT_PATH=C:\Users\nesto\Desktop\ElMoroNestor\elmoro
set PYTHON_PATH=%PROJECT_PATH%\.venv\Scripts\python.exe
set LOG_PATH=%PROJECT_PATH%\logs

if not exist "%LOG_PATH%" mkdir "%LOG_PATH%"

cd /d "%PROJECT_PATH%"

echo ========================================= >> "%LOG_PATH%\auth_playwright.log"
echo Inicio auth_playwright %date% %time% >> "%LOG_PATH%\auth_playwright.log"

"%PYTHON_PATH%" scripts\auth_playwright.py >> "%LOG_PATH%\auth_playwright.log" 2>&1

echo Fin auth_playwright %date% %time% >> "%LOG_PATH%\auth_playwright.log"
echo ========================================= >> "%LOG_PATH%\auth_playwright.log"

endlocal
pause