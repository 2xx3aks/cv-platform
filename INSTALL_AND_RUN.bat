@echo off
REM Complete installation and run script for Windows
echo ============================================================
echo CV Platform - Complete Setup and Run (Windows)
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Step 1: Installing Python Dependencies...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may have failed to install
    echo You may need to install them manually
    pause
)

echo.
echo Step 2: Checking for .env file...
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env.example...
    echo.
    echo Please create a .env file with:
    echo   COHERE_API_KEY=your-key-here
    echo   MONGODB_URI=mongodb://localhost:27017/
    echo   MONGODB_DB_NAME=cv_platform
    echo   DJANGO_SECRET_KEY=your-secret-key
    echo.
    pause
)

echo.
echo Step 3: Starting Application...
echo.
python run_app.py

pause

