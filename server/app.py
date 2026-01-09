#!/usr/bin/env python3
"""
AMS2 Race Results Web Server
Displays race sessions and results from the AMS2 SQLite database
"""

import os
import sys
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database path - look for ams2_races.db in parent directory
DB_PATH = Path(__file__).parent.parent / 'ams2_races.db'


def get_db_connection():
    """Create a database connection"""
    if not DB_PATH.exists():
        return None
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def format_lap_time(ms):
    """Format milliseconds to MM:SS.SSS"""
    if ms is None or ms <= 0:
        return "N/A"
    
    seconds = ms / 1000
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:06.3f}"


def get_sessions():
    """Get all sessions from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, session_type, track_name, car_name, date_time 
            FROM sessions 
            ORDER BY id DESC
        ''')
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': row['id'],
                'session_type': row['session_type'],
                'track_name': row['track_name'],
                'car_name': row['car_name'],
                'date_time': row['date_time']
            })
        return sessions
    finally:
        conn.close()


def get_session_results(session_id):
    """Get results for a specific session"""
    conn = get_db_connection()
    if not conn:
        return None, []
    
    try:
        cursor = conn.cursor()
        
        # Get session info
        cursor.execute('''
            SELECT session_type, track_name, car_name, date_time 
            FROM sessions 
            WHERE id = ?
        ''', (session_id,))
        
        session_row = cursor.fetchone()
        if not session_row:
            return None, []
        
        session_info = {
            'id': session_id,
            'session_type': session_row['session_type'],
            'track_name': session_row['track_name'],
            'car_name': session_row['car_name'],
            'date_time': session_row['date_time']
        }
        
        # Get results
        cursor.execute('''
            SELECT 
                driver_name,
                finish_position,
                points,
                fastest_lap,
                pole_sitter,
                session_best_lap,
                race_best_lap,
                laps_completed
            FROM results
            WHERE session_id = ?
            ORDER BY finish_position
        ''', (session_id,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'driver_name': row['driver_name'],
                'finish_position': row['finish_position'],
                'points': row['points'],
                'fastest_lap': bool(row['fastest_lap']),
                'pole_sitter': bool(row['pole_sitter']),
                'session_best_lap': format_lap_time(row['session_best_lap']),
                'race_best_lap': format_lap_time(row['race_best_lap']),
                'laps_completed': row['laps_completed']
            })
        
        return session_info, results
    finally:
        conn.close()


def get_driver_stats(driver_name):
    """Get statistics for a specific driver"""
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as races,
                SUM(CASE WHEN points > 0 THEN 1 ELSE 0 END) as points_finishes,
                SUM(points) as total_points,
                SUM(CASE WHEN pole_sitter THEN 1 ELSE 0 END) as poles,
                SUM(CASE WHEN fastest_lap THEN 1 ELSE 0 END) as fastest_laps,
                AVG(finish_position) as avg_finish,
                MIN(session_best_lap) as best_lap
            FROM results
            WHERE driver_name = ?
        ''', (driver_name,))
        
        row = cursor.fetchone()
        if not row:
            return {}
        
        return {
            'driver_name': driver_name,
            'races': row['races'],
            'points_finishes': row['points_finishes'] or 0,
            'total_points': row['total_points'] or 0,
            'poles': row['poles'] or 0,
            'fastest_laps': row['fastest_laps'] or 0,
            'avg_finish': f"{row['avg_finish']:.2f}" if row['avg_finish'] else "N/A",
            'best_lap': format_lap_time(row['best_lap'])
        }
    finally:
        conn.close()


# Routes

@app.route('/')
def index():
    """Main page with sessions list"""
    sessions = get_sessions()
    return render_template('index.html', sessions=sessions)


@app.route('/session/<int:session_id>')
def session(session_id):
    """Session details page"""
    session_info, results = get_session_results(session_id)
    if not session_info:
        return "Session not found", 404
    
    return render_template('session.html', session=session_info, results=results)


@app.route('/driver/<driver_name>')
def driver(driver_name):
    """Driver statistics page"""
    stats = get_driver_stats(driver_name)
    if not stats:
        return "Driver not found", 404
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    s.id, s.session_type, s.track_name, s.date_time,
                    r.finish_position, r.points, r.fastest_lap, r.pole_sitter
                FROM results r
                JOIN sessions s ON r.session_id = s.id
                WHERE r.driver_name = ?
                ORDER BY s.id DESC
            ''', (driver_name,))
            
            races = []
            for row in cursor.fetchall():
                races.append({
                    'session_id': row['id'],
                    'session_type': row['session_type'],
                    'track_name': row['track_name'],
                    'date_time': row['date_time'],
                    'finish_position': row['finish_position'],
                    'points': row['points'],
                    'fastest_lap': bool(row['fastest_lap']),
                    'pole_sitter': bool(row['pole_sitter'])
                })
            
            return render_template('driver.html', stats=stats, races=races)
        finally:
            conn.close()
    
    return render_template('driver.html', stats=stats, races=[])


# API Routes

@app.route('/api/sessions')
def api_sessions():
    """API: Get all sessions"""
    sessions = get_sessions()
    return jsonify(sessions)


@app.route('/api/session/<int:session_id>')
def api_session(session_id):
    """API: Get session details"""
    session_info, results = get_session_results(session_id)
    if not session_info:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'session': session_info,
        'results': results
    })


@app.route('/api/drivers')
def api_drivers():
    """API: Get all drivers"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not found'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT driver_name FROM results ORDER BY driver_name')
        drivers = [row['driver_name'] for row in cursor.fetchall()]
        return jsonify(drivers)
    finally:
        conn.close()


@app.route('/api/driver/<driver_name>')
def api_driver(driver_name):
    """API: Get driver statistics"""
    stats = get_driver_stats(driver_name)
    if not stats:
        return jsonify({'error': 'Driver not found'}), 404
    
    return jsonify(stats)


@app.route('/api/standings')
def api_standings():
    """API: Get current championship standings"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database not found'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                driver_name,
                SUM(points) as total_points,
                COUNT(*) as races,
                SUM(CASE WHEN fastest_lap THEN 1 ELSE 0 END) as fastest_laps,
                SUM(CASE WHEN pole_sitter THEN 1 ELSE 0 END) as poles
            FROM results
            GROUP BY driver_name
            ORDER BY total_points DESC
        ''')
        
        standings = []
        position = 1
        for row in cursor.fetchall():
            standings.append({
                'position': position,
                'driver_name': row['driver_name'],
                'points': row['total_points'] or 0,
                'races': row['races'],
                'fastest_laps': row['fastest_laps'] or 0,
                'poles': row['poles'] or 0
            })
            position += 1
        
        return jsonify(standings)
    finally:
        conn.close()


@app.route('/health')
def health():
    """Health check endpoint"""
    db_exists = DB_PATH.exists()
    return jsonify({
        'status': 'ok',
        'database_found': db_exists,
        'database_path': str(DB_PATH)
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


def main():
    """Main entry point for the web server"""
    parser = argparse.ArgumentParser(
        description='AMS2 Race Results Web Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python app.py                    # Run on default port 5000
  python app.py --port 8000        # Run on port 8000
  python app.py -p 3000            # Run on port 3000
  python app.py --host 127.0.0.1   # Listen only on localhost
        '''
    )
    
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port to run the server on (default: 5000)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host address to bind to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    args = parser.parse_args()
    
    print(f"Database path: {DB_PATH}")
    print(f"Database exists: {DB_PATH.exists()}")
    print(f"Starting AMS2 Race Results Web Server...")
    print(f"Listening on http://{args.host}:{args.port}")
    print(f"Press Ctrl+C to stop\n")
    
    app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
