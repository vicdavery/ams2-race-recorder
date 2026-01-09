@echo off
REM Test runner for AMS2 web server on Windows

setlocal enabledelayedexpansion

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup.bat first...
    call setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Running AMS2 Web Server Tests...
echo ================================
echo.

REM Run pytest with verbose output
pytest -v

REM Capture exit code
set exit_code=%errorlevel%

echo.
echo ================================
if %exit_code% equ 0 (
    echo All tests passed!
) else (
    echo Some tests failed (exit code: %exit_code%)
)

pause
exit /b %exit_code%
