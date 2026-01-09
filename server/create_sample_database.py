#!/usr/bin/env python3
"""
Create a fictional racing season database for testing the web server.
Generates realistic race data with multiple drivers and tracks.
"""

import sqlite3
from datetime import datetime, timedelta
import random
from pathlib import Path


def create_database(db_path):
    """Create and populate a sample racing season database"""
    
    # Remove existing database if it exists
    if Path(db_path).exists():
        Path(db_path).unlink()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_type TEXT NOT NULL,
            track_name TEXT NOT NULL,
            car_name TEXT NOT NULL,
            date_time TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            driver_name TEXT NOT NULL,
            finish_position INTEGER NOT NULL,
            points INTEGER NOT NULL DEFAULT 0,
            fastest_lap BOOLEAN DEFAULT 0,
            pole_sitter BOOLEAN DEFAULT 0,
            session_best_lap REAL,
            race_best_lap REAL,
            laps_completed INTEGER,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    
    # Insert sample racing season data
    _insert_season_data(cursor)
    
    conn.commit()
    conn.close()
    
    print(f"✓ Sample database created: {db_path}")


def _insert_season_data(cursor):
    """Insert a complete fictional racing season"""
    
    # Define drivers for the season
    drivers = [
        {'name': 'Max Verstappen', 'pace': 1.0},      # Reference pace
        {'name': 'Lewis Hamilton', 'pace': 0.998},
        {'name': 'Carlos Sainz', 'pace': 1.002},
        {'name': 'Lando Norris', 'pace': 1.005},
        {'name': 'Charles Leclerc', 'pace': 1.003},
        {'name': 'George Russell', 'pace': 1.001},
        {'name': 'Fernando Alonso', 'pace': 1.006},
        {'name': 'Oscar Piastri', 'pace': 1.004},
    ]
    
    # Define races with track names and qualifying times
    races = [
        {'track': 'Bahrain', 'quali_base': 88000, 'race_base': 88500, 'laps': 57},
        {'track': 'Saudi Arabia', 'quali_base': 92000, 'race_base': 92500, 'laps': 50},
        {'track': 'Australia', 'quali_base': 80000, 'race_base': 80500, 'laps': 58},
        {'track': 'Japan', 'quali_base': 82000, 'race_base': 82500, 'laps': 53},
        {'track': 'China', 'quali_base': 95000, 'race_base': 95500, 'laps': 56},
        {'track': 'Monaco', 'quali_base': 61000, 'race_base': 61500, 'laps': 78},
        {'track': 'Canada', 'quali_base': 73000, 'race_base': 73500, 'laps': 70},
        {'track': 'Silverstone', 'quali_base': 82000, 'race_base': 82500, 'laps': 52},
        {'track': 'Hungary', 'quali_base': 85000, 'race_base': 85500, 'laps': 70},
        {'track': 'Spa', 'quali_base': 105000, 'race_base': 105500, 'laps': 44},
    ]
    
    # F1 2024 points table
    f1_points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    
    # Generate qualifying and race for each round
    start_date = datetime(2025, 3, 16)
    
    for round_num, race_info in enumerate(races, 1):
        race_date = start_date + timedelta(days=round_num * 14)
        track = race_info['track']
        quali_base = race_info['quali_base']
        race_base = race_info['race_base']
        laps = race_info['laps']
        
        # === QUALIFYING SESSION ===
        quali_date = race_date.strftime('%Y-%m-%d 14:00:00')
        cursor.execute('''
            INSERT INTO sessions (session_type, track_name, car_name, date_time)
            VALUES (?, ?, ?, ?)
        ''', ('Qualifying', track, 'Formula 1', quali_date))
        
        quali_session_id = cursor.lastrowid
        
        # Generate qualifying results (sorted by time)
        quali_results = []
        for driver in drivers:
            quali_time = quali_base + random.randint(-500, 500)
            # Adjust for driver pace
            quali_time = int(quali_time * driver['pace'])
            quali_results.append((driver['name'], quali_time))
        
        # Sort by time to get positions
        quali_results.sort(key=lambda x: x[1])
        
        for pos, (driver_name, quali_time) in enumerate(quali_results, 1):
            pole = (pos == 1)
            cursor.execute('''
                INSERT INTO results
                (session_id, driver_name, finish_position, points, fastest_lap, pole_sitter,
                 session_best_lap, race_best_lap, laps_completed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (quali_session_id, driver_name, pos, 0, False, pole, quali_time, quali_time, 4))
        
        # === RACE SESSION ===
        race_time = race_date.strftime('%Y-%m-%d 15:00:00')
        cursor.execute('''
            INSERT INTO sessions (session_type, track_name, car_name, date_time)
            VALUES (?, ?, ?, ?)
        ''', ('Race', track, 'Formula 1', race_time))
        
        race_session_id = cursor.lastrowid
        
        # Generate race results
        # Start order based on qualifying, but races are unpredictable
        race_results = []
        for driver in drivers:
            race_time = race_base + random.randint(-1000, 1000)
            race_time = int(race_time * driver['pace'])
            race_results.append((driver['name'], race_time))
        
        # Add some randomness to create different race outcomes
        race_results = sorted(race_results, key=lambda x: x[1] + random.randint(-2000, 2000))
        
        # Find fastest lap (usually a top finisher but not always)
        fastest_lap_driver = race_results[0][0]
        if random.random() > 0.7:  # 30% chance fastest lap goes to someone else
            fastest_lap_idx = random.randint(0, min(4, len(race_results)-1))
            fastest_lap_driver = race_results[fastest_lap_idx][0]
        
        for pos, (driver_name, best_lap_time) in enumerate(race_results, 1):
            points = f1_points[pos-1] if pos <= 10 else 0
            fastest = (driver_name == fastest_lap_driver)
            
            cursor.execute('''
                INSERT INTO results
                (session_id, driver_name, finish_position, points, fastest_lap, pole_sitter,
                 session_best_lap, race_best_lap, laps_completed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (race_session_id, driver_name, pos, points, fastest, False,
                  best_lap_time, best_lap_time - random.randint(0, 500), laps))


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Create a fictional F1 racing season database for testing'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='sample_races.db',
        help='Output database file path (default: sample_races.db)'
    )
    
    args = parser.parse_args()
    
    print(f"Creating fictional racing season database...")
    print(f"Tracks: 10")
    print(f"Drivers: 8")
    print(f"Sessions: 20 (10 qualifying + 10 races)")
    print()
    
    create_database(args.output)
    print()
    print(f"✓ Database created successfully!")
    print(f"✓ File: {args.output}")
    print()
    print("Usage with web server:")
    print(f"  python3 app.py --database {args.output}")
    print(f"  python3 app.py -db {args.output}")


if __name__ == '__main__':
    main()
