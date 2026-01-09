"""
Tests for Flask routes (HTML pages)
"""

import pytest


class TestIndexRoute:
    """Tests for the index/home page"""
    
    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Race Sessions' in response.data
    
    def test_index_displays_sessions(self, client):
        """Test that sessions are displayed on the index page"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Silverstone' in response.data
        assert b'Spa-Francorchamps' in response.data
    
    def test_index_shows_session_types(self, client):
        """Test that session types are displayed"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Qualifying' in response.data
        assert b'Race' in response.data
    
    def test_index_session_links_clickable(self, client):
        """Test that session links are properly formatted"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'href="/session/1' in response.data or b'href="/session/' in response.data


class TestSessionRoute:
    """Tests for individual session detail pages"""
    
    def test_session_page_loads(self, client):
        """Test that a session detail page loads"""
        response = client.get('/session/1')
        assert response.status_code == 200
        assert b'Qualifying' in response.data
        assert b'Silverstone' in response.data
    
    def test_session_displays_results_table(self, client):
        """Test that results are displayed in a table"""
        response = client.get('/session/2')
        assert response.status_code == 200
        assert b'<table' in response.data
        assert b'Alice Johnson' in response.data
        assert b'Bob Smith' in response.data
    
    def test_session_shows_pole_sitter_badge(self, client):
        """Test that pole sitter badge is shown"""
        response = client.get('/session/2')
        assert response.status_code == 200
        assert b'Pole' in response.data
    
    def test_session_shows_fastest_lap_badge(self, client):
        """Test that fastest lap badge is shown"""
        response = client.get('/session/2')
        assert response.status_code == 200
        assert b'Fastest Lap' in response.data
    
    def test_session_shows_points(self, client):
        """Test that F1 points are displayed"""
        response = client.get('/session/2')
        assert response.status_code == 200
        # Alice finished 1st with 25 points
        assert b'25' in response.data
        # Bob finished 2nd with 18 points
        assert b'18' in response.data
    
    def test_session_displays_lap_times(self, client):
        """Test that lap times are formatted and displayed"""
        response = client.get('/session/2')
        assert response.status_code == 200
        # Should contain formatted time (MM:SS.SSS format)
        assert b':' in response.data  # Time separator
    
    def test_session_not_found_returns_404(self, client):
        """Test that invalid session ID returns 404"""
        response = client.get('/session/9999')
        assert response.status_code == 404
    
    def test_session_shows_metadata(self, client):
        """Test that session metadata is displayed"""
        response = client.get('/session/2')
        assert response.status_code == 200
        assert b'Formula 3' in response.data
        assert b'2025-01-09' in response.data


class TestDriverRoute:
    """Tests for driver detail pages"""
    
    def test_driver_page_loads(self, client):
        """Test that a driver page loads"""
        response = client.get('/driver/Alice%20Johnson')
        assert response.status_code == 200
        assert b'Alice Johnson' in response.data
    
    def test_driver_displays_statistics(self, client):
        """Test that driver statistics are shown"""
        response = client.get('/driver/Alice%20Johnson')
        assert response.status_code == 200
        assert b'Total Points' in response.data
        assert b'Races' in response.data
        assert b'Poles' in response.data
        assert b'Fastest Laps' in response.data
    
    def test_driver_shows_correct_points(self, client):
        """Test that total points are calculated correctly"""
        # Alice: 25 + 18 = 43 points across sessions
        response = client.get('/driver/Alice%20Johnson')
        assert response.status_code == 200
        assert b'43' in response.data
    
    def test_driver_shows_race_history(self, client):
        """Test that race history is displayed"""
        response = client.get('/driver/Bob%20Smith')
        assert response.status_code == 200
        # Should show race history table
        assert b'<table' in response.data
    
    def test_driver_not_found_returns_404(self, client):
        """Test that unknown driver returns 404"""
        response = client.get('/driver/UnknownDriver')
        assert response.status_code == 404
    
    def test_driver_statistics_calculations(self, client):
        """Test that driver statistics are accurate"""
        response = client.get('/driver/Charlie%20Brown')
        assert response.status_code == 200
        # Charlie competed in 3 races
        assert b'Races' in response.data


class TestHealthRoute:
    """Tests for health check endpoint"""
    
    def test_health_check_returns_ok(self, client):
        """Test that health check returns success"""
        response = client.get('/health')
        assert response.status_code == 200
        assert b'ok' in response.data or b'OK' in response.data


class TestNotFoundRoute:
    """Tests for 404 error handling"""
    
    def test_nonexistent_page_returns_404(self, client):
        """Test that non-existent pages return 404"""
        response = client.get('/nonexistent/page')
        assert response.status_code == 404
        assert b'404' in response.data or b'Not Found' in response.data
