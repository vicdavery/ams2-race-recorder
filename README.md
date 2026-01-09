# AMS2 Race Recorder

A complete race recording and analysis system for Automobilista 2 with a C++ shared memory reader and Python web interface.

## Project Structure

```
ams2/
├── recorder/          # C++ race recorder (reads AMS2 shared memory)
│   ├── src/
│   ├── include/
│   ├── CMakeLists.txt
│   └── build.sh
├── server/            # Python Flask web server
│   ├── app.py
│   ├── templates/
│   ├── requirements.txt
│   ├── setup.sh
│   └── run.sh
└── README.md
```

## Components

### 1. Race Recorder (C++)

Records race telemetry and results from Automobilista 2's shared memory.

**Features:**
- Real-time shared memory reading
- Automatic session detection (Qualifying/Race)
- Pole position tracking
- Fastest lap detection
- F1 2024 points calculation (25-18-15-12-10-8-6-4-2-1)
- SQLite database persistence

**Building on Windows:**
```bash
cd recorder
build.bat
```

The executable will be at: `../build/bin/Release/ams2_recorder.exe`

**Running:**
1. Start Automobilista 2
2. Enable Shared Memory in settings (Project CARS 2 mode)
3. Run: `..\build\bin\Release\ams2_recorder.exe`

See [WINDOWS_BUILD.md](WINDOWS_BUILD.md) for detailed instructions.

### 2. Web Server (Python)

Flask-based web interface to view race results and driver statistics.

**Features:**
- Session history browser
- Driver statistics and race history
- Championship standings
- RESTful API endpoints
- Responsive design

**Setup on Windows:**
```bash
cd server
setup.bat
```

**Running on Windows:**
```bash
cd server
run.bat
```

Access the web server at `http://localhost:5000`

## Database Schema

### Sessions Table
- `id`: Unique session identifier
- `session_type`: "Qualifying" or "Race"
- `track_name`: Track name
- `car_name`: Car class/name
- `date_time`: Timestamp

### Results Table
- `id`: Result identifier
- `session_id`: Foreign key to session
- `driver_name`: Driver name
- `finish_position`: Finishing position
- `points`: F1 points awarded
- `fastest_lap`: Boolean flag
- `pole_sitter`: Boolean flag
- `session_best_lap`: Best lap time (ms)
- `race_best_lap`: Personal best lap (ms)
- `laps_completed`: Total laps

## API Endpoints

- `GET /api/sessions` - All sessions
- `GET /api/session/<id>` - Specific session
- `GET /api/drivers` - All drivers
- `GET /api/driver/<name>` - Driver stats
- `GET /api/standings` - Championship standings
- `GET /health` - Database status

## Requirements

### Recorder (C++)
- **Windows 10/11** (AMS2 shared memory is Windows-only)
- CMake 3.15+
- Visual Studio 2022 (with C++ tools)
- SQLite3 development libraries
- C++17 compiler

See [WINDOWS_BUILD.md](WINDOWS_BUILD.md) for detailed Windows setup instructions.

### Server (Python)
- Python 3.7+
- Flask 2.3+
- CORS support

## Quick Start (Windows)

1. Install prerequisites (see [WINDOWS_BUILD.md](WINDOWS_BUILD.md))
2. Run build script:
   ```bash
   build_all.bat
   ```
3. Start the recorder:
   ```bash
   cd recorder
   ..\build\bin\Release\ams2_recorder.exe
   ```
4. In another terminal, start the web server:
   ```bash
   cd server
   run.bat
   ```
5. Open http://localhost:5000

## Workflow

1. **During Race:**
   - Start AMS2 with shared memory enabled
   - Run the race recorder (.exe)
   - Recorder captures telemetry and stores to database

2. **After Racing:**
   - Start the web server (run.bat)
   - View results through web interface at http://localhost:5000
   - Analyze driver stats and standings

## Notes

- Database file: `ams2_races.db` (in project root)
- Recorder runs continuously; press Ctrl+C to stop
- Web server default port: 5000 (configurable)
- API responses available in JSON format
- Lap times stored in milliseconds
