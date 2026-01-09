# AMS2 Race Results Web Server

Complete documentation for the Python Flask web server component.

## Quick Start

### 1. Install Dependencies
```bash
cd server
bash setup.sh          # Linux/Mac
setup.bat             # Windows
```

### 2. Generate Sample Database
```bash
python3 create_sample_database.py
```

### 3. Run Server
```bash
./run.sh -db sample_races.db     # Linux/Mac
run.bat -db sample_races.db      # Windows
```

### 4. Access Web Interface
Open browser: **http://localhost:5000**

## Features

### Web Interface
- 🏠 **Home Page** - Browse all sessions
- 🏁 **Session Details** - View qualifying and race results
- 👤 **Driver Profiles** - Individual statistics and history
- 🏆 **Standings Page** - Championship points table

### API Endpoints
- `GET /api/sessions` - All sessions (JSON)
- `GET /api/session/<id>` - Session details (JSON)
- `GET /api/drivers` - All drivers list (JSON)
- `GET /api/driver/<name>` - Driver statistics (JSON)
- `GET /api/standings` - Championship standings (JSON)
- `GET /health` - Database status check

### Data Support
- ✅ Multiple sessions (qualifying + races)
- ✅ Multiple drivers and teams
- ✅ F1 2024 points system
- ✅ Pole position tracking
- ✅ Fastest lap identification
- ✅ Lap time formatting
- ✅ Historical data queries

## Configuration Options

### Port
```bash
./run.sh --port 8000       # Default: 5000
./run.sh -p 3000           # Short form
```

### Host/Interface
```bash
./run.sh --host 127.0.0.1  # Localhost only
./run.sh --host 0.0.0.0    # All interfaces (default)
```

### Database
```bash
./run.sh -db sample_races.db           # By filename
./run.sh --database /path/to/races.db  # Full path
```

### Debug Mode
```bash
./run.sh --debug           # Enable Flask debug features
```

### Combine Options
```bash
./run.sh -p 8000 --host 127.0.0.1 -db sample_races.db --debug
```

## Database

### Default Database
```
Location: ../ams2_races.db
Created by: C++ race recorder
```

### Sample Database
```bash
# Generate sample data
python3 create_sample_database.py

# Use with server
./run.sh -db sample_races.db
```

### Custom Database
```bash
# Specify any database file
./run.sh --database /path/to/custom.db
```

## File Structure

```
server/
├── app.py                      # Flask application
├── conftest.py                 # Test fixtures
├── create_sample_database.py   # Sample data generator
├── run.sh                      # Linux/Mac startup script
├── run.bat                     # Windows startup script
├── setup.sh                    # Linux/Mac setup script
├── setup.bat                   # Windows setup script
├── run_tests.sh                # Linux/Mac test runner
├── run_tests.bat               # Windows test runner
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── session.html
│   ├── driver.html
│   └── 404.html
├── tests/                      # Unit tests (66 tests)
│   ├── test_api.py
│   ├── test_routes.py
│   └── test_database.py
├── venv/                       # Virtual environment (created by setup)
└── [Documentation Files]
    ├── QUICK_START.md
    ├── PORT_CONFIGURATION.md
    ├── DATABASE_PARAMETER.md
    ├── SAMPLE_DATABASE.md
    ├── TESTING.md
    ├── TEST_DATA.md
    ├── TEST_RESULTS.md
    └── README_SERVER.md        # This file
```

## Testing

### Run All Tests
```bash
./run_tests.sh          # Linux/Mac
run_tests.bat           # Windows
```

### Run Specific Tests
```bash
pytest tests/test_api.py -v          # API tests only
pytest tests/test_routes.py -v       # Route tests only
pytest tests/test_database.py -v     # Database tests only
```

### Run Single Test
```bash
pytest tests/test_api.py::TestSessionsAPI::test_get_all_sessions -v
```

### Test Coverage
- 66 total tests
- All passing ✅
- ~0.13 seconds execution
- 15 route tests
- 24 API tests
- 27 database tests

## Documentation

### Quick References
- **QUICK_START.md** - Fast getting started guide
- **PORT_CONFIGURATION.md** - Detailed port setup
- **DATABASE_PARAMETER.md** - Database file options
- **SAMPLE_DATABASE.md** - Sample data features

### Complete Guides
- **TESTING.md** - Full testing documentation
- **TEST_DATA.md** - Test data reference
- **TEST_RESULTS.md** - Test execution summary
- **README_SERVER.md** - This file

## API Examples

### Get All Sessions
```bash
curl http://localhost:5000/api/sessions
```

### Get Session Details
```bash
curl http://localhost:5000/api/session/1
```

### Get All Drivers
```bash
curl http://localhost:5000/api/drivers
```

### Get Driver Stats
```bash
curl http://localhost:5000/api/driver/Max%20Verstappen
```

### Get Championship Standings
```bash
curl http://localhost:5000/api/standings
```

## Browser Usage

### Home Page
```
http://localhost:5000/
```
Browse all sessions with links to details.

### Session Details
```
http://localhost:5000/session/1
http://localhost:5000/session/2
```
View qualifying/race results with points and badges.

### Driver Profile
```
http://localhost:5000/driver/Lewis%20Hamilton
http://localhost:5000/driver/Max%20Verstappen
```
View driver statistics and race history.

## Troubleshooting

### Port Already in Use
```bash
./run.sh --port 5001      # Try different port
lsof -i :5000             # Find what's using port
```

### Database Not Found
```bash
python3 create_sample_database.py    # Generate sample data
./run.sh -db sample_races.db         # Use it
```

### Import Error
```bash
source venv/bin/activate   # Activate venv (Linux/Mac)
venv\Scripts\activate.bat  # Activate venv (Windows)
pip install -r requirements.txt
```

### Tests Failing
```bash
source venv/bin/activate   # Activate venv
pytest tests/ -v --tb=short
```

## Development

### Enable Debug Mode
```bash
./run.sh --debug
```
- Auto-reloads on code changes
- Better error pages
- Debugger enabled

### Test with Sample Data
```bash
python3 create_sample_database.py -o test.db
./run.sh -db test.db
```

### Run with Multiple Databases
```bash
# Terminal 1
./run.sh -p 5000 -db season_a.db

# Terminal 2
./run.sh -p 5001 -db season_b.db
```

## Performance

### Response Times
- Static pages: <10ms
- API endpoints: <50ms
- Complex queries: <100ms

### Database
- SQLite (fast, embedded)
- No external database needed
- File-based storage

### Server
- Flask development server
- Suitable for testing/demo
- Use WSGI server for production

## Production Deployment

For production, consider:

### Use WSGI Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Use Reverse Proxy
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

### Enable HTTPS
```bash
# Using Let's Encrypt
certbot certonly --standalone -d example.com
```

### Run as Service
```bash
# Create systemd service file
# for automatic startup
```

## Security Notes

### Development Only
- Default configuration not suitable for production
- Debug mode should be disabled
- Use HTTPS for public access

### File Permissions
```bash
chmod 644 ams2_races.db    # Readable
chmod 755 /var/www/app     # Executable directory
```

### Database Security
- SQLite not suitable for high-concurrency
- Backup database regularly
- Restrict file access

## Maintenance

### Backup Database
```bash
cp ams2_races.db ams2_races.backup.db
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clear Cache
```bash
rm -rf __pycache__
rm -rf .pytest_cache
```

## Support

### Getting Help
- Check documentation files
- Review test files for examples
- Run tests to verify setup
- Check app logs for errors

### Reporting Issues
- Include error messages
- Provide database info
- Describe what you were doing
- Include console output

## Summary

✅ **Fast Setup** - 3 commands to run
✅ **Sample Data** - Test without recorder
✅ **Configurable** - Port, host, database
✅ **Well Tested** - 66 tests passing
✅ **Well Documented** - Multiple guides
✅ **API Ready** - REST endpoints available

---

**Version**: 1.0.0  
**Python**: 3.7+  
**Framework**: Flask 2.3.3  
**Status**: Ready for Production Demo
