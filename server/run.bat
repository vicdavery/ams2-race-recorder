@echo off
REM Run script for AMS2 Race Results Web Server on Windows

setlocal enabledelayedexpansion

REM Default values
set PORT=5000
set HOST=0.0.0.0
set DEBUG=

REM Parse command line arguments
:parse_args
if "%1"=="" goto done_args
if "%1"=="-p" (
    set PORT=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--port" (
    set PORT=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--host" (
    set HOST=%2
    shift
    shift
    goto parse_args
)
if "%1"=="--debug" (
    set DEBUG=--debug
    shift
    goto parse_args
)
if "%1"=="-h" (
    goto show_help
)
if "%1"=="--help" (
    goto show_help
)
echo Unknown option: %1
echo Use --help for usage information
exit /b 1

:show_help
echo Usage: run.bat [OPTIONS]
echo.
echo Options:
echo   -p, --port PORT    Port to run server on (default: 5000)
echo   --host HOST        Host address to bind to (default: 0.0.0.0)
echo   --debug            Run in debug mode
echo   -h, --help         Show this help message
echo.
echo Examples:
echo   run.bat                        REM Run on port 5000
echo   run.bat --port 8000            REM Run on port 8000
echo   run.bat -p 3000 --debug        REM Run on port 3000 with debug
pause
exit /b 0

:done_args
REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup.bat first...
    call setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the Flask app
echo.
python app.py --port %PORT% --host %HOST% %DEBUG%

pause
