@echo off
REM Windows batch script to run the CV Platform application
echo ============================================================
echo CV Platform - Django Application Startup (Windows)
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please run setup_env.bat first to set up the environment
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo.
    echo WARNING: Virtual environment not found!
    echo.
    echo Please run setup_env.bat first to create the environment
    echo.
    pause
    exit /b 1
)

REM Run the main startup script
echo.
echo Starting application...
python run_app.py

pause

