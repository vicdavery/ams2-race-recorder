@echo off
REM Build script for entire AMS2 project on Windows (recorder + server)

echo Building AMS2 Race Recorder System...
echo ======================================
echo.

REM Build C++ recorder
echo 1. Building C++ Race Recorder...
cd recorder
call build.bat

if errorlevel 1 (
    echo Failed to build recorder!
    pause
    exit /b 1
)

cd ..
echo.

REM Setup Python server
echo 2. Setting up Python Web Server...
cd server
call setup.bat

if errorlevel 1 (
    echo Failed to setup server!
    pause
    exit /b 1
)

cd ..
echo.
echo ======================================
echo Build complete!
echo.
echo Next steps:
echo 1. Start the recorder:
echo    cd recorder && ..\build\bin\Release\ams2_recorder.exe
echo.
echo 2. In another terminal, start the web server:
echo    cd server && run.bat
echo.
echo 3. Open http://localhost:5000 in your browser
pause
