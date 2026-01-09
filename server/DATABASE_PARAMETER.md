# Database Parameter Guide

The web server supports specifying a custom database file via command-line parameter.

## Basic Usage

### Default Database
If no database is specified, the server looks for:
1. `../ams2_races.db` (in parent directory)
2. `./ams2_races.db` (in current directory)

```bash
./run.sh
# Uses: ../ams2_races.db
```

### Custom Database

```bash
# Linux/Mac - Short form
./run.sh -db custom_database.db

# Linux/Mac - Long form
./run.sh --database /path/to/my_races.db

# Windows - Short form
run.bat -db custom_database.db

# Windows - Long form
run.bat --database C:\path\to\my_races.db

# Direct Python
python3 app.py --database sample_races.db
python3 app.py -db races.db
```

## Examples

### Use Sample Database
```bash
# Generate sample database (if not exists)
python3 create_sample_database.py

# Run server with sample data
./run.sh -db sample_races.db
```

### Use Specific Path
```bash
# Absolute path
./run.sh --database /home/user/racing_data/season_2025.db

# Relative path
./run.sh -db ../databases/my_races.db

# Current directory
./run.sh -db ./races.db
```

### Combine with Other Parameters
```bash
# Custom database and custom port
./run.sh -db sample_races.db --port 8000

# Custom database, host, and debug mode
./run.sh --database races.db --host 127.0.0.1 --debug

# All parameters
./run.sh -p 3000 --host 0.0.0.0 -db races.db --debug
```

## Database Parameter Syntax

### Command-Line Format

```
-db FILE              Short form
--database FILE       Long form
```

### Values

- `FILE` - Path to SQLite database file
- Can be relative: `sample_races.db`, `./data/races.db`, `../races.db`
- Can be absolute: `/home/user/races.db`, `C:\Users\me\races.db`
- File must exist (will not auto-create)

## Creating Databases

### Using the Generator
```bash
# Generate sample database
python3 create_sample_database.py

# Generate with custom output name
python3 create_sample_database.py -o my_season.db
```

### From AMS2 Recorder
```bash
# Run the C++ recorder to create ams2_races.db
cd recorder
..\build\bin\Release\ams2_recorder.exe

# Then run server (will use ams2_races.db automatically)
cd ../server
./run.sh
```

## Error Handling

### Database Not Found
```
Database path: sample_races.db
Database exists: False
ERROR: Database file not found: sample_races.db
```

**Solution**: Ensure the file exists or generate it first.

### Database Locked
```
Error: Database is locked
```

**Cause**: Another application is using the database.

**Solutions**:
- Close other instances of the server
- Use a different database file
- Wait for the lock to be released

### Invalid Path
```
Error: Permission denied
```

**Cause**: No permission to read the database file.

**Solution**: Check file permissions or use a different path.

## Database Locations

### Typical Setups

**Production (with AMS2 recorder)**
```
ams2/
├── ams2_races.db          ← Created by recorder
├── recorder/
└── server/
    └── run.sh             ← Uses ../ams2_races.db automatically
```

**Development (with sample data)**
```
ams2/
└── server/
    ├── sample_races.db    ← Sample database
    └── run.sh -db sample_races.db
```

**Multiple Databases**
```
ams2/
├── databases/
│   ├── season_2024.db
│   ├── season_2025.db
│   └── test_data.db
└── server/
    └── run.sh -db ../databases/season_2025.db
```

## Script Usage

### Linux/Mac run.sh

```bash
./run.sh -db database.db
./run.sh --database /path/to/database.db
./run.sh -p 8000 -db sample_races.db --debug
```

### Windows run.bat

```bash
run.bat -db database.db
run.bat --database C:\path\to\database.db
run.bat -p 8000 -db sample_races.db --debug
```

### Direct Python

```bash
python3 app.py -db database.db
python3 app.py --database /path/to/database.db
python3 app.py -p 8000 -db sample_races.db --debug
```

## Testing with Different Databases

### Test Multiple Seasons
```bash
# Terminal 1 - 2024 Season
./run.sh -p 5000 -db season_2024.db

# Terminal 2 - 2025 Season
./run.sh -p 5001 -db season_2025.db

# Terminal 3 - Test Data
./run.sh -p 5002 -db test_data.db
```

### Compare Performance
```bash
# Generate multiple databases
python3 create_sample_database.py -o races_run1.db
python3 create_sample_database.py -o races_run2.db

# Run server with each
./run.sh -db races_run1.db -p 5000
./run.sh -db races_run2.db -p 5001

# Compare results
curl http://localhost:5000/api/standings
curl http://localhost:5001/api/standings
```

## File Format

### SQLite Database
- Format: SQLite 3
- Extension: `.db`, `.sqlite`, `.sqlite3`
- Size: Typically 5-100 KB per season
- Platform: Works on Windows, Linux, macOS

### Creating from Recorder Output
The C++ recorder automatically creates `ams2_races.db`:

```bash
# Run recorder to create database
cd recorder
../build/bin/Release/ams2_recorder.exe
# Creates: ../ams2_races.db

# Use in server
cd ../server
./run.sh
# Automatically uses: ../ams2_races.db
```

## Workflow

### Standard Workflow
1. **Record races** with C++ recorder
   - Creates `ams2_races.db`
2. **View results** with web server
   ```bash
   cd server
   ./run.sh
   ```

### Testing Workflow
1. **Generate sample data**
   ```bash
   python3 create_sample_database.py -o test.db
   ```
2. **Run server with test data**
   ```bash
   ./run.sh -db test.db
   ```
3. **Test web server features**
   - Browse sessions
   - Check standings
   - Test API endpoints

### Multi-Database Workflow
1. **Create multiple databases**
   ```bash
   python3 create_sample_database.py -o season_a.db
   python3 create_sample_database.py -o season_b.db
   ```
2. **Run servers on different ports**
   ```bash
   ./run.sh -db season_a.db -p 5000 &
   ./run.sh -db season_b.db -p 5001 &
   ```

## Help

To see all options:

```bash
./run.sh --help
python3 app.py --help
```

Output includes:
- All available parameters
- Default values
- Usage examples

## Environment Variables

Currently not supported, but can be added. Use command-line parameters instead:

```bash
# Current way (recommended)
./run.sh -db custom.db

# Could add environment variables in future
export AMS2_DATABASE=custom.db
./run.sh
```

## Permissions

Ensure the database file is readable:

```bash
# Linux/Mac - Make readable
chmod 644 my_races.db

# Windows - Check file properties
# Right-click → Properties → Security
```

## Backup and Copy

### Backup Database
```bash
cp ams2_races.db ams2_races.backup.db
```

### Copy to External Storage
```bash
cp ams2_races.db /mnt/usb/racing_data.db
./run.sh -db /mnt/usb/racing_data.db
```

### Import to Web Server
```bash
# Copy database to server directory
cp /backup/races.db ./races.db

# Run server with imported data
./run.sh -db races.db
```

---

**Summary:**
- Use `-db` or `--database` to specify custom database
- Default database: `../ams2_races.db`
- Works with absolute and relative paths
- Generate sample databases with `create_sample_database.py`
- Combine with other parameters (port, host, debug)
