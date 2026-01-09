# Test Data Reference

Complete reference for test data used in the test suite.

## Test Database Structure

The test database contains two tables:

### Sessions Table
| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER (PK) | Auto-increment |
| session_type | TEXT | "Qualifying" or "Race" |
| track_name | TEXT | Circuit name |
| car_name | TEXT | Vehicle class |
| date_time | TEXT | ISO format timestamp |

### Results Table
| Field | Type | Notes |
|-------|------|-------|
| id | INTEGER (PK) | Auto-increment |
| session_id | INTEGER (FK) | References sessions.id |
| driver_name | TEXT | Driver name |
| finish_position | INTEGER | Final position in session |
| points | INTEGER | F1 2024 points (0-25) |
| fastest_lap | BOOLEAN | Had fastest lap (0-1) |
| pole_sitter | BOOLEAN | Had pole position (0-1) |
| session_best_lap | REAL | Best lap time in milliseconds |
| race_best_lap | REAL | Personal best lap (ms) |
| laps_completed | INTEGER | Number of laps driven |

## Test Sessions

### Session 1: Silverstone Qualifying
```
ID: 1
Type: Qualifying
Track: Silverstone
Car: Formula 3
Date: 2025-01-09 14:30:00
```

**Lap Times**
| Position | Driver | Time (ms) | Laps |
|----------|--------|-----------|------|
| 1 | Alice Johnson | 96250.5 | 4 |
| 2 | Bob Smith | 96400.2 | 4 |
| 3 | Charlie Brown | 96550.8 | 4 |

### Session 2: Silverstone Race
```
ID: 2
Type: Race
Track: Silverstone
Car: Formula 3
Date: 2025-01-09 15:00:00
```

**Results with F1 Points**
| Pos | Driver | Points | Fastest Lap | Pole | Best Lap (ms) | Laps |
|-----|--------|--------|-------------|------|---------------|------|
| 1 | Alice Johnson | 25 | No | Yes | 96100.5 | 20 |
| 2 | Bob Smith | 18 | Yes | No | 96280.2 | 20 |
| 3 | Charlie Brown | 15 | No | No | 96400.8 | 20 |

**Pole Sitter**: Alice Johnson (from qualifying)
**Fastest Lap**: Bob Smith

### Session 3: Spa-Francorchamps Race
```
ID: 3
Type: Race
Track: Spa-Francorchamps
Car: Formula 3
Date: 2025-01-10 14:00:00
```

**Results with F1 Points**
| Pos | Driver | Points | Fastest Lap | Pole | Best Lap (ms) | Laps |
|-----|--------|--------|-------------|------|---------------|------|
| 1 | Charlie Brown | 25 | Yes | Yes | 115050.3 | 10 |
| 2 | Alice Johnson | 18 | No | No | 115200.1 | 10 |
| 3 | Bob Smith | 15 | No | No | 115350.4 | 10 |

**Pole Sitter**: Charlie Brown
**Fastest Lap**: Charlie Brown

## Test Drivers

### Alice Johnson
**Profile**
- Total Races: 3
- Points Finishes: 3
- Total Points: 43
- Pole Positions: 1 (Silverstone)
- Fastest Laps: 0
- Average Finish: 1.67

**Race-by-Race**
1. Silverstone Qualifying: 1st (pole)
2. Silverstone Race: 1st (25 pts)
3. Spa Race: 2nd (18 pts)

**Lap Times**
- Best: 96100.5 ms (1:36.100)
- Worst: 96400.8 ms (1:36.400)

### Bob Smith
**Profile**
- Total Races: 3
- Points Finishes: 3
- Total Points: 33
- Pole Positions: 0
- Fastest Laps: 1 (Silverstone)
- Average Finish: 2.33

**Race-by-Race**
1. Silverstone Qualifying: 2nd
2. Silverstone Race: 2nd (18 pts, fastest lap)
3. Spa Race: 3rd (15 pts)

**Lap Times**
- Best: 96280.2 ms (1:36.280)
- Worst: 115350.4 ms (1:55.350)

### Charlie Brown
**Profile**
- Total Races: 3
- Points Finishes: 3
- Total Points: 40
- Pole Positions: 1 (Spa)
- Fastest Laps: 1 (Spa)
- Average Finish: 1.67

**Race-by-Race**
1. Silverstone Qualifying: 3rd
2. Silverstone Race: 3rd (15 pts)
3. Spa Race: 1st (25 pts, pole, fastest lap)

**Lap Times**
- Best: 115050.3 ms (1:55.050)
- Worst: 96550.8 ms (1:36.550)

## Championship Standing (After All Sessions)

**Final Standings**
| Pos | Driver | Points | Races | Poles | Fastest |
|-----|--------|--------|-------|-------|---------|
| 1 | Alice Johnson | 43 | 3 | 1 | 0 |
| 2 | Charlie Brown | 40 | 3 | 1 | 1 |
| 3 | Bob Smith | 33 | 3 | 0 | 1 |

## Test Scenarios Covered

### Qualifying Session
- Pole position tracking
- Best lap times
- Multiple participants

### Race Sessions
- F1 points assignment (25-18-15-12-10-8-6-4-2-1)
- Fastest lap tracking
- Race results ordering
- Lap count tracking

### Driver Statistics
- Points accumulation
- Multiple race participation
- Best lap calculation
- Pole position counting
- Fastest lap counting
- Average finish position

### Data Integrity
- Foreign key relationships
- No orphaned records
- Valid lap times
- Correct point awards
- Position consistency

## Using Test Data in Tests

### Access Current Test Data

In test files, data is automatically loaded via the `client` fixture:

```python
def test_something(self, client):
    # Database is pre-populated with test data
    response = client.get('/api/sessions')
    # Returns 3 sessions
```

### Add More Test Data

To add data to tests, modify the `_insert_test_data()` function in `conftest.py`:

```python
def _insert_test_data(cursor):
    # Insert your additional data here
    cursor.execute('''
        INSERT INTO sessions (session_type, track_name, car_name, date_time)
        VALUES (?, ?, ?, ?)
    ''', ('Race', 'New Track', 'Formula 3', '2025-01-11 10:00:00'))
```

## Test Data Characteristics

### Realistic Values
- Lap times are realistic (94-117 seconds for typical tracks)
- F1 2024 points system used (25-18-15-12-10-8-6-4-2-1)
- Multiple sessions show driver progression

### Comprehensive Coverage
- Tests pole position tracking
- Tests fastest lap identification
- Tests F1 points calculation
- Tests multi-session statistics

### Deterministic
- Same data loaded for every test run
- No randomization
- Consistent results across multiple runs

## Lap Time Format Reference

Lap times are stored in milliseconds:

| Time (ms) | Formatted | Track Type |
|-----------|-----------|-----------|
| 96100.5 | 1:36.100 | Short circuit (Silverstone) |
| 115050.3 | 1:55.050 | High-speed circuit (Spa) |

### Formatting Rules
- MM:SS.SSS format
- Minutes from integer division
- Remaining milliseconds calculated from modulo

Example: 96250.5 ms
- Minutes: 96250.5 / 60000 = 1 minute
- Seconds: (96250.5 % 60000) / 1000 = 36.250 seconds
- Result: 1:36.250
