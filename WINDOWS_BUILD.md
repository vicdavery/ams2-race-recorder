# Building on Windows

Complete guide for building and running the AMS2 Race Recorder on Windows.

## Prerequisites

### 1. Install CMake
Download and install CMake 3.15 or later from: https://cmake.org/download/

Make sure to add CMake to your system PATH during installation.

### 2. Install Visual Studio
Download and install **Visual Studio 2022 Community Edition** from: https://visualstudio.microsoft.com/vs/community/

During installation, select:
- **Desktop development with C++**
- This includes MSVC compiler and necessary tools

### 3. Install Python
Download and install **Python 3.7+** from: https://www.python.org/

During installation:
- Check "Add Python to PATH"
- Check "Install pip"

### 4. Install SQLite3 Development Libraries

#### Option A: Using vcpkg (Recommended)

```bash
# Install vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# Install SQLite3
.\vcpkg install sqlite3:x64-windows

# Set environment variable for CMake
# Add to your system environment or use in CMake:
set(CMAKE_TOOLCHAIN_FILE "C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake")
```

#### Option B: Using Chocolatey

```bash
choco install sqlite
```

#### Option C: Pre-built binaries

Download SQLite pre-built binaries from: https://www.sqlite.org/download.html

Extract and add the directory to your system PATH.

## Building the Project

### Method 1: Using Batch Files (Easiest)

1. Open **Command Prompt** in the project root directory
2. Run:
```bash
build_all.bat
```

This will:
- Build the C++ recorder
- Setup the Python web server
- Create all necessary files

### Method 2: Manual Build

#### Build the C++ Recorder

1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project directory
3. Run:
```bash
cd recorder
build.bat
```

The executable will be created at: `../build/bin/Release/ams2_recorder.exe`

#### Setup the Web Server

1. Open **Command Prompt**
2. Navigate to the server directory:
```bash
cd server
setup.bat
```

This creates a Python virtual environment and installs dependencies.

### Method 3: Using CMake Directly

If you prefer to use CMake GUI or command line:

```bash
mkdir build
cd build
cmake ..\recorder -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
```

## Running the Application

### Step 1: Start the Race Recorder

1. Open **Command Prompt**
2. Start Automobilista 2 and enable Shared Memory:
   - In AMS2 settings, look for "Shared Memory" or "Project CARS 2 telemetry"
   - Set it to enabled

3. Run the recorder:
```bash
cd recorder
..\build\bin\Release\ams2_recorder.exe
```

You should see:
```
AMS2 Race Recorder
==================
Connected to AMS2. Waiting for race data...
```

### Step 2: Start the Web Server (In Another Command Prompt)

1. Open a **new Command Prompt window**
2. Run:
```bash
cd server
run.bat
```

You should see:
```
Starting AMS2 Race Results Web Server...
Open http://localhost:5000 in your browser
```

### Step 3: View Results

Open your web browser and go to: **http://localhost:5000**

## Troubleshooting

### CMake not found
**Solution:** Ensure CMake is installed and added to PATH. Restart Command Prompt after installation.

### Visual Studio compiler not found
**Solution:** Make sure Visual Studio 2022 with C++ tools is installed. You may need to install the "Desktop development with C++" workload.

### SQLite3 not found
**Solution:** 
- If using vcpkg, ensure you set the CMAKE_TOOLCHAIN_FILE
- If using Chocolatey or manual installation, add SQLite to PATH
- Alternatively, edit CMakeLists.txt to specify the SQLite3 location manually

### Python not found when running setup.bat
**Solution:** Ensure Python 3.7+ is installed and added to PATH. Test with:
```bash
python --version
```

### Port 5000 already in use
**Solution:** The web server will try alternative ports. Check console output for the actual port, or modify the port in `server/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### AMS2 shared memory connection fails
**Reasons:**
1. AMS2 is not running
2. Shared Memory is not enabled in AMS2 settings
3. Another application is already reading shared memory (e.g., SimHub)

**Solution:** 
- Start AMS2 first
- Enable Shared Memory in settings (Project CARS 2 mode)
- Disable other telemetry applications temporarily

## Database Location

The SQLite database is created in the project root as: **ams2_races.db**

You can move it or specify a custom path by editing `recorder/src/main.cpp`.

## Performance Notes

- The recorder polls shared memory ~60 times per second
- Minimal CPU usage (typically <1%)
- Web server runs on port 5000 by default
- Database queries are optimized for typical usage patterns

## Next Steps

After building and running:
1. Race in Automobilista 2 with shared memory enabled
2. The recorder will automatically capture sessions
3. View results in the web interface at http://localhost:5000
4. Analyze driver statistics and championship standings

## Support

For issues or questions:
- Check the main README.md
- Review CMakeLists.txt for configuration options
- Ensure all prerequisites are installed correctly
