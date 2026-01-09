@echo off
REM Build script for AMS2 Race Recorder on Windows

echo Building AMS2 Race Recorder...

REM Create build directory if it doesn't exist
if not exist "..\build" (
    mkdir ..\build
)

cd ..\build

REM Run CMake configuration for Visual Studio
cmake ..\recorder -G "Visual Studio 17 2022" -A x64

if errorlevel 1 (
    echo CMake configuration failed!
    pause
    exit /b 1
)

REM Build the project in Release mode
cmake --build . --config Release

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Executable: %cd%\bin\Release\ams2_recorder.exe
pause
