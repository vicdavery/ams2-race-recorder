@echo off
REM Run script for AMS2 Race Results Web Server on Windows

setlocal enabledelayedexpansion

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup.bat first...
    call setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the Flask app
echo.
echo Starting AMS2 Race Results Web Server...
echo Open http://localhost:5000 in your browser
echo.

python app.py

pause
