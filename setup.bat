@echo off
title Ghost Tab Cycler - Setup
echo ===================================================
echo   Ghost Tab Cycler - First Time Setup
echo ===================================================
echo.

:: Check for py or python launcher
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=py
    goto :found_python
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=python
    goto :found_python
)

echo [!] Python is not installed or not added to PATH!
echo.
echo Please install Python first:
echo   1. Download Python from: https://www.python.org/downloads/
echo   2. Run the installer
echo   3. CRITICAL: Check the box "Add python.exe to PATH" before clicking Install!
echo   4. Once installed, double-click setup.bat again.
echo.
pause
exit /b 1

:found_python
echo [OK] Python detected: %PY_CMD%
echo.

if not exist "venv" (
    echo [1/2] Creating virtual environment...
    %PY_CMD% -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [X] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment already exists.
)

echo.
echo [2/2] Installing requirements...
venv\Scripts\pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [X] Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   Setup Completed Successfully!
echo   You can now double-click START_GHOST.vbs to launch.
echo ===================================================
echo.
pause
