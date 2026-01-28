@echo off
REM HRSG Weld Management System - Windows Launcher
REM This batch file starts the HRSG Weld Management application on Windows

echo ========================================
echo HRSG Weld Management System
echo Version 2.1
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo Checking dependencies...
pip install -r requirements.txt --quiet
echo.

REM Run the application
echo Starting HRSG Weld Management System...
python run_app.py

REM Deactivate virtual environment
deactivate

pause
