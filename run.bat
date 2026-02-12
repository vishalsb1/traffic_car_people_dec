@echo off
title Car Color Detection System

echo ========================================
echo Car Color Detection System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [INFO] Python detected
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
    echo.
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo [INFO] Checking dependencies...
pip show opencv-python >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    echo [SUCCESS] Dependencies installed
    echo.
) else (
    echo [SUCCESS] Dependencies already installed
    echo.
)

echo ========================================
echo Starting Car Color Detection System...
echo ========================================
echo.

REM Run the application
python main.py

REM Deactivate virtual environment when app closes
deactivate

echo.
echo ========================================
echo Application closed
echo ========================================
pause
