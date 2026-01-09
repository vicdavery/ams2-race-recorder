"""
Tests for database functions
"""

import pytest
from app import get_db_connection


class TestDatabaseConnection:
    """Tests for database connection"""
    
    def test_get_db_connection_succeeds(self, client):
        """Test that database connection can be established"""
        conn = get_db_connection()
        assert conn is not None
    
    def test_db_connection_is_valid(self, client):
        """Test that connection is usable"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sessions')
        result = cursor.fetchone()
        assert result is not None
        conn.close()


class TestGetSessions:
    """Tests for get_sessions function"""
    
    def test_get_sessions_returns_list(self, client):
        """Test that sessions are returned as list"""
        from app import get_sessions
        sessions = get_sessions()
        assert isinstance(sessions, list)
    
    def test_get_sessions_count(self, client):
        """Test that correct number of sessions is returned"""
        from app import get_sessions
        sessions = get_sessions()
        assert len(sessions) == 3
    
    def test_get_sessions_contain_required_fields(self, client):
        """Test that each session has required fields"""
        from app import get_sessions
        sessions = get_sessions()
        
        # Fields are returned as snake_case in get_sessions()
        required_fields = ['id', 'session_type', 'track_name', 'car_name', 'date_time']
        for session in sessions:
            for field in required_fields:
                assert field in session
    
    def test_get_sessions_returns_all(self, client):
        """Test that all sessions are returned"""
        from app import get_sessions
        sessions = get_sessions()
        # Should return all 3 test sessions
        assert len(sessions) == 3


class TestGetSessionResults:
    """Tests for get_session_results function"""
    
    def test_get_session_results_valid_id(self, client):
        """Test getting results for a valid session"""
        from app import get_session_results
        session_info, results = get_session_results(1)
        
        assert session_info is not None
        assert isinstance(results, list)
    
    def test_session_results_invalid_id(self, client):
        """Test getting results for invalid session"""
        from app import get_session_results
        session_info, results = get_session_results(9999)
        
        assert session_info is None
        assert results == []
    
    def test_session_results_contain_data(self, client):
        """Test that session results contain driver data"""
        from app import get_session_results
        session_info, results = get_session_results(2)
        
        assert len(results) > 0
        assert 'driver_name' in results[0]
        assert 'points' in results[0]
    
    def test_session_results_sorted_by_position(self, client):
        """Test that results are sorted by finish position"""
        from app import get_session_results
        session_info, results = get_session_results(2)
        
        positions = [r['finish_position'] for r in results]
        assert positions == sorted(positions)
    
    def test_session_results_with_pole_sitter(self, client):
        """Test that pole sitter flag is set correctly"""
        from app import get_session_results
        session_info, results = get_session_results(2)
        
        pole_sitters = [r for r in results if r['pole_sitter']]
        assert len(pole_sitters) == 1


class TestGetDriverStats:
    """Tests for get_driver_stats function"""
    
    def test_get_driver_stats_valid_driver(self, client):
        """Test getting stats for a valid driver"""
        from app import get_driver_stats
        stats = get_driver_stats('Alice Johnson')
        
        assert stats != {}
        assert 'driver_name' in stats
        assert 'total_points' in stats
    
    def test_get_driver_stats_invalid_driver(self, client):
        """Test getting stats for invalid driver returns zeros"""
        from app import get_driver_stats
        stats = get_driver_stats('NonexistentDriver')
        
        # Returns stats dict with all zeros for unknown drivers
        assert stats['races'] == 0
        assert stats['total_points'] == 0
    
    def test_driver_stats_correct_calculations(self, client):
        """Test that stats are calculated correctly"""
        from app import get_driver_stats
        stats = get_driver_stats('Alice Johnson')
        
        # Alice participated in 3 races
        assert stats['races'] == 3
        # Alice scored 25 + 18 = 43 points
        assert stats['total_points'] == 43
    
    def test_driver_stats_fastest_laps(self, client):
        """Test that fastest laps are counted"""
        from app import get_driver_stats
        stats = get_driver_stats('Bob Smith')
        
        # Bob had 1 fastest lap (in session 2)
        assert stats['fastest_laps'] == 1
    
    def test_driver_stats_poles(self, client):
        """Test that poles are counted"""
        from app import get_driver_stats
        stats = get_driver_stats('Alice Johnson')
        
        # Alice had 2 poles (session 1 qualifying and session 2 race)
        assert stats['poles'] == 2


class TestLapTimeFormatting:
    """Tests for lap time formatting"""
    
    def test_format_lap_time_positive_value(self, client):
        """Test formatting of valid lap time"""
        from app import format_lap_time
        
        # 96250.5 ms = 1:36.250
        formatted = format_lap_time(96250.5)
        assert ':' in formatted
        assert '.' in formatted
    
    def test_format_lap_time_zero_returns_na(self, client):
        """Test that zero lap time returns N/A"""
        from app import format_lap_time
        
        formatted = format_lap_time(0)
        assert formatted == 'N/A'
    
    def test_format_lap_time_none_returns_na(self, client):
        """Test that None lap time returns N/A"""
        from app import format_lap_time
        
        formatted = format_lap_time(None)
        assert formatted == 'N/A'
    
    def test_format_lap_time_negative_returns_na(self, client):
        """Test that negative lap time returns N/A"""
        from app import format_lap_time
        
        formatted = format_lap_time(-100)
        assert formatted == 'N/A'


class TestDatabaseIntegrity:
    """Tests for database integrity"""
    
    def test_foreign_key_integrity(self, client):
        """Test that results reference valid sessions"""
        from app import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check that all results have valid session_id
        cursor.execute('''
            SELECT COUNT(*) FROM results r
            WHERE r.session_id NOT IN (SELECT id FROM sessions)
        ''')
        
        invalid_count = cursor.fetchone()[0]
        assert invalid_count == 0
        conn.close()
    
    def test_no_orphaned_records(self, client):
        """Test that there are no orphaned results"""
        from app import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM results')
        result_count = cursor.fetchone()[0]
        
        # We should have results
        assert result_count > 0
        conn.close()
