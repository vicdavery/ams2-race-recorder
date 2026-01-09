# AMS2 Race Recorder - Feature Summary

## Core Features

### 1. C++ Race Recorder
- **Shared Memory Integration**: Reads real-time telemetry from Automobilista 2
- **Automatic Session Detection**: Detects qualifying and race sessions
- **Live Data Capture**: Continuous recording at ~60 FPS
- **Pole Position Tracking**: Records fastest qualifying lap
- **Fastest Lap Detection**: Identifies fastest race lap
- **F1 2024 Points**: Awards points based on official F1 system (25-18-15-12-10-8-6-4-2-1)
- **SQLite Database**: Persistent storage with proper schema

### 2. Python Web Server
- **Session Browsing**: View all recorded sessions
- **Session Details**: See results with times and points
- **Driver Profiles**: Individual driver statistics and history
- **Championship Standings**: View current championship points
- **Responsive Design**: Works on desktop and mobile
- **REST API**: JSON endpoints for programmatic access

### 3. Database Features
- **Multi-session Tracking**: Support for unlimited sessions
- **Multi-driver Support**: Track multiple drivers across sessions
- **Data Integrity**: Foreign keys and constraints
- **Normalized Schema**: Efficient data storage
- **Historical Data**: Permanent race record

### 4. Configuration Options
- **Configurable Port**: Run on any port (default 5000)
- **Configurable Host**: Bind to specific network interface
- **Debug Mode**: Enable Flask debug features
- **Custom Database Path**: Store database anywhere

### 5. Testing Infrastructure
- **66 Unit Tests**: Comprehensive test coverage
- **Test Data**: Realistic sample data included
- **Fixtures**: Automatic test database setup
- **API Tests**: REST endpoint validation
- **Route Tests**: HTML page rendering
- **Database Tests**: Data integrity checks

### 6. Documentation
- **Windows Build Guide**: Step-by-step setup (WINDOWS_BUILD.md)
- **Testing Guide**: How to run and write tests (TESTING.md)
- **Test Data Reference**: Sample data documentation (TEST_DATA.md)
- **Port Configuration**: Detailed port setup (PORT_CONFIGURATION.md)
- **Quick Start**: Fast getting started guide (QUICK_START.md)
- **Test Results**: Test execution summary (TEST_RESULTS.md)

## Technical Specifications

### Architecture
```
AMS2 Shared Memory → C++ Recorder → SQLite DB ← Python Web Server
                                                ↓
                                            Web Browser
```

### Supported Features
- ✅ Qualifying sessions
- ✅ Race sessions
- ✅ Multi-lap races
- ✅ Multiple drivers
- ✅ Pole position
- ✅ Fastest lap
- ✅ Lap times (millisecond precision)
- ✅ F1 2024 points
- ✅ Driver statistics
- ✅ Championship standings
- ✅ Historical data

### Performance
- **Recorder**: <1% CPU usage, real-time processing
- **Web Server**: <100ms response times
- **Database**: Optimized queries, indexed fields
- **Tests**: 66 tests in ~0.17 seconds

### Platform Support
- **Recorder**: Windows 10/11 only (AMS2 requirement)
- **Web Server**: Windows, Linux, macOS
- **Database**: Platform-agnostic SQLite

## API Endpoints

### Session Management
- `GET /` - Session list page
- `GET /session/<id>` - Session details page
- `GET /api/sessions` - All sessions JSON
- `GET /api/session/<id>` - Session JSON

### Driver Management
- `GET /driver/<name>` - Driver profile page
- `GET /api/drivers` - All drivers list
- `GET /api/driver/<name>` - Driver stats JSON

### Championships
- `GET /api/standings` - Championship standings JSON

### Utilities
- `GET /health` - Database status check
- `GET /api/standings` - Current championship

## Command-Line Options

### Web Server
```
--port PORT       Port to run on (default: 5000)
--host HOST       Network address (default: 0.0.0.0)
--debug           Enable debug mode
```

### Race Recorder
Runs automatically, connects to AMS2 shared memory.

## File Structure
```
ams2/
├── recorder/          # C++ race recorder
│   ├── src/          # Source files
│   ├── include/      # Header files
│   ├── build.sh      # Linux build script
│   ├── build.bat     # Windows build script
│   └── CMakeLists.txt
│
├── server/           # Python web server
│   ├── app.py        # Flask application
│   ├── conftest.py   # Test configuration
│   ├── run.sh        # Linux startup
│   ├── run.bat       # Windows startup
│   ├── tests/        # Unit tests (66 tests)
│   ├── templates/    # HTML templates
│   ├── requirements.txt
│   ├── TESTING.md
│   ├── TEST_DATA.md
│   ├── TEST_RESULTS.md
│   ├── PORT_CONFIGURATION.md
│   └── QUICK_START.md
│
├── build_all.sh      # Full build script (Linux)
├── build_all.bat     # Full build script (Windows)
├── README.md         # Main documentation
└── WINDOWS_BUILD.md  # Windows setup guide
```

## Getting Started

### Quick Setup
```bash
# Windows: Full build
build_all.bat

# Linux/Mac: Full build
./build_all.sh
```

### Run Recorder
```bash
cd recorder
..\build\bin\Release\ams2_recorder.exe  # Windows
```

### Run Web Server
```bash
cd server
run.bat --port 5000      # Windows
./run.sh --port 5000     # Linux/Mac
```

### Run Tests
```bash
cd server
run_tests.bat            # Windows
./run_tests.sh           # Linux/Mac
```

## Database Schema

### Sessions Table
- id (PK)
- session_type (Qualifying/Race)
- track_name
- car_name
- date_time

### Results Table
- id (PK)
- session_id (FK)
- driver_name
- finish_position
- points
- fastest_lap (boolean)
- pole_sitter (boolean)
- session_best_lap (ms)
- race_best_lap (ms)
- laps_completed

## Future Enhancements
- Real-time race updates
- Driver comparison tools
- Season statistics
- Telemetry graphs
- Replay integration
- Multi-circuit statistics
- Damage analysis
- Fuel consumption tracking
- Tire wear analysis

## License
MIT License - See repository for details

## Support
- GitHub: https://github.com/vicdavery/ams2-race-recorder
- Documentation: See README.md and included guides
- Tests: Run test suite with `pytest`

---
Last Updated: 2025-01-09
Version: 1.0.0
