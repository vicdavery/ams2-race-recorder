# Sample Racing Season Database

## Overview

A fictional F1 racing season database is provided to test and demonstrate the web server without needing to record actual races with the C++ recorder.

## Features

- **10 Races** across iconic F1 tracks
- **20 Sessions** (10 qualifying + 10 races)
- **8 Drivers** with realistic performance characteristics
- **160 Results** with pole positions, fastest laps, and F1 2024 points
- **Championship Standings** showing competitive dynamics

## Quick Start

### Generate Sample Database

```bash
cd server
python3 create_sample_database.py
```

This creates `sample_races.db` in the current directory.

### Run Web Server with Sample Data

```bash
# Linux/Mac
./run.sh -db sample_races.db

# Windows
run.bat -db sample_races.db

# Or specify full path
./run.sh --database /path/to/sample_races.db
```

### Direct Python

```bash
python3 app.py --database sample_races.db
python3 app.py -db sample_races.db
```

## Database Content

### Tracks (10)
- Bahrain
- Saudi Arabia
- Australia
- Japan
- China
- Monaco
- Canada
- Silverstone
- Hungary
- Spa-Francorchamps

### Drivers (8)
1. **Max Verstappen** - Pace: 1.0 (reference)
2. **Lewis Hamilton** - Pace: 0.998
3. **Carlos Sainz** - Pace: 1.002
4. **Lando Norris** - Pace: 1.005
5. **Charles Leclerc** - Pace: 1.003
6. **George Russell** - Pace: 1.001
7. **Fernando Alonso** - Pace: 1.006
8. **Oscar Piastri** - Pace: 1.004

### Championship Standings

| Position | Driver | Points | Races |
|----------|--------|--------|-------|
| 1 | Max Verstappen | 148 | 10 |
| 2 | Lewis Hamilton | 143 | 10 |
| 3 | Carlos Sainz | 132 | 10 |
| 4 | Lando Norris | 130 | 10 |
| 5 | Oscar Piastri | 126 | 10 |
| 6 | Charles Leclerc | 104 | 10 |
| 7 | Fernando Alonso | 103 | 10 |
| 8 | George Russell | 94 | 10 |

## Creating Custom Databases

### Using the Generator Script

```bash
python3 create_sample_database.py -o custom_races.db
```

The script generates:
- Realistic qualifying times based on track characteristics
- Race results with random variations (upsets, different strategies)
- Fastest lap awards distributed among competitive drivers
- Pole positions from qualifying sessions
- F1 2024 points (25-18-15-12-10-8-6-4-2-1)

### Customizing the Generator

Edit `create_sample_database.py` to modify:

```python
# Change driver list
drivers = [
    {'name': 'Your Driver', 'pace': 1.0},
    ...
]

# Change tracks
races = [
    {'track': 'Your Track', 'quali_base': 80000, 'race_base': 80500, 'laps': 52},
    ...
]

# Change points system
f1_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
```

## Features Demonstrated

The sample database showcases:

### Web Features
- ✅ Session listing and filtering
- ✅ Qualifying session results
- ✅ Race session results with points
- ✅ Pole position tracking (badge)
- ✅ Fastest lap identification (badge)
- ✅ Driver profiles and statistics
- ✅ Championship standings
- ✅ Historical data queries
- ✅ REST API endpoints

### Data Integrity
- ✅ Foreign key relationships
- ✅ Proper point distribution
- ✅ Multi-lap race tracking
- ✅ Lap time formatting
- ✅ No orphaned records

## Database Files

### Default Location
```
server/sample_races.db     (5 KB, pre-generated)
```

### Generate New Database
```bash
python3 create_sample_database.py -o my_races.db
```

## Testing the Web Server

With the sample database, you can test:

### Routes
- Session listing: http://localhost:5000/
- Session details: http://localhost:5000/session/1
- Driver profiles: http://localhost:5000/driver/Max%20Verstappen

### API Endpoints
- Sessions: http://localhost:5000/api/sessions
- Session details: http://localhost:5000/api/session/1
- Drivers: http://localhost:5000/api/drivers
- Driver stats: http://localhost:5000/api/driver/Lewis%20Hamilton
- Standings: http://localhost:5000/api/standings

## Running Tests with Sample Database

The test suite uses its own test database but you can manually verify the sample database:

```bash
python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('sample_races.db')
cursor = conn.cursor()

# Get standings
cursor.execute('''
    SELECT driver_name, SUM(points) as pts FROM results
    GROUP BY driver_name ORDER BY pts DESC
''')

print("Championship Standings:")
for driver, points in cursor.fetchall():
    print(f"  {driver:20} {points} pts")

conn.close()
EOF
```

## Use Cases

### Development
Use the sample database to develop new features without recording actual races.

### Testing
Test the web server thoroughly with realistic data.

### Demonstrations
Show the application to others with real-looking race data.

### Training
Learn the system without running the C++ recorder.

## Regenerating the Database

If you want a fresh sample database:

```bash
# Delete old database
rm sample_races.db

# Generate new one (races will be different due to random variation)
python3 create_sample_database.py
```

Each run generates slightly different race results due to randomization, so you get variety while maintaining realistic data.

## Multiple Databases

You can create multiple databases for different scenarios:

```bash
python3 create_sample_database.py -o season_2025.db
python3 create_sample_database.py -o season_test.db
python3 create_sample_database.py -o season_demo.db

# Run with different databases
./run.sh -db season_2025.db
./run.sh -db season_test.db
./run.sh -db season_demo.db
```

## Notes

- Sample data is fictional and does not represent real race results
- Lap times are realistic but randomly generated
- Driver pace values create competitive but varied outcomes
- Each database generation creates different race outcomes
- Databases can be used simultaneously (on different ports)

## File Size

- Sample database: ~5-10 KB
- 10 races × 2 sessions × 8 drivers = 160 results
- Highly compressed SQLite format

## Next Steps

1. **Generate database**: `python3 create_sample_database.py`
2. **Start server**: `./run.sh -db sample_races.db`
3. **Open browser**: http://localhost:5000
4. **Explore data**: Browse races, drivers, and standings
5. **Test API**: Visit API endpoints for JSON data

---

**Sample Database Features:**
- ✅ 10 iconic F1 tracks
- ✅ 8 competitive drivers
- ✅ 20 complete sessions
- ✅ Realistic lap times
- ✅ Proper F1 points system
- ✅ Pole position tracking
- ✅ Fastest lap awards
