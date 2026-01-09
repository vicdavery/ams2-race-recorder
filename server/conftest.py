"""
Pytest configuration and fixtures for AMS2 web server tests
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from app import app, get_db_connection
import os


@pytest.fixture
def client():
    """Create a test client with a temporary database"""
    # Create temporary database
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db_path = temp_db.name
    temp_db.close()
    
    # Update app config to use temp database
    app.config['TESTING'] = True
    
    # Mock the database path
    import app as app_module
    original_db_path = app_module.DB_PATH
    app_module.DB_PATH = Path(temp_db_path)
    
    # Initialize database with test data
    _init_test_database(temp_db_path)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    app_module.DB_PATH = original_db_path
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)


def _init_test_database(db_path):
    """Initialize test database with sample data"""
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
    
    # Insert test data
    _insert_test_data(cursor)
    
    conn.commit()
    conn.close()


def _insert_test_data(cursor):
    """Insert sample race data for testing"""
    
    # Session 1: Qualifying at Silverstone
    cursor.execute('''
        INSERT INTO sessions (session_type, track_name, car_name, date_time)
        VALUES (?, ?, ?, ?)
    ''', ('Qualifying', 'Silverstone', 'Formula 3', '2025-01-09 14:30:00'))
    
    session1_id = cursor.lastrowid
    
    # Session 1 Results
    session1_results = [
        ('Alice Johnson', 1, 0, False, True, 96250.5, 96250.5, 4),
        ('Bob Smith', 2, 0, False, False, 96400.2, 96400.2, 4),
        ('Charlie Brown', 3, 0, False, False, 96550.8, 96550.8, 4),
    ]
    
    for driver, pos, points, fastest, pole, session_best, race_best, laps in session1_results:
        cursor.execute('''
            INSERT INTO results 
            (session_id, driver_name, finish_position, points, fastest_lap, pole_sitter, 
             session_best_lap, race_best_lap, laps_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session1_id, driver, pos, points, fastest, pole, session_best, race_best, laps))
    
    # Session 2: Race at Silverstone
    cursor.execute('''
        INSERT INTO sessions (session_type, track_name, car_name, date_time)
        VALUES (?, ?, ?, ?)
    ''', ('Race', 'Silverstone', 'Formula 3', '2025-01-09 15:00:00'))
    
    session2_id = cursor.lastrowid
    
    # Session 2 Results (with F1 points)
    session2_results = [
        ('Alice Johnson', 1, 25, False, True, 96200.3, 96100.5, 20),
        ('Bob Smith', 2, 18, True, False, 96350.1, 96280.2, 20),
        ('Charlie Brown', 3, 15, False, False, 96500.4, 96400.8, 20),
    ]
    
    for driver, pos, points, fastest, pole, session_best, race_best, laps in session2_results:
        cursor.execute('''
            INSERT INTO results 
            (session_id, driver_name, finish_position, points, fastest_lap, pole_sitter, 
             session_best_lap, race_best_lap, laps_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session2_id, driver, pos, points, fastest, pole, session_best, race_best, laps))
    
    # Session 3: Race at Spa
    cursor.execute('''
        INSERT INTO sessions (session_type, track_name, car_name, date_time)
        VALUES (?, ?, ?, ?)
    ''', ('Race', 'Spa-Francorchamps', 'Formula 3', '2025-01-10 14:00:00'))
    
    session3_id = cursor.lastrowid
    
    # Session 3 Results
    session3_results = [
        ('Charlie Brown', 1, 25, True, True, 115200.2, 115050.3, 10),
        ('Alice Johnson', 2, 18, False, False, 115400.5, 115200.1, 10),
        ('Bob Smith', 3, 15, False, False, 115600.8, 115350.4, 10),
    ]
    
    for driver, pos, points, fastest, pole, session_best, race_best, laps in session3_results:
        cursor.execute('''
            INSERT INTO results 
            (session_id, driver_name, finish_position, points, fastest_lap, pole_sitter, 
             session_best_lap, race_best_lap, laps_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session3_id, driver, pos, points, fastest, pole, session_best, race_best, laps))
