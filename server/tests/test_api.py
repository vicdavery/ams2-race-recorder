"""
Tests for REST API endpoints
"""

import pytest
import json


class TestSessionsAPI:
    """Tests for the sessions API endpoint"""
    
    def test_get_all_sessions(self, client):
        """Test retrieving all sessions"""
        response = client.get('/api/sessions')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_sessions_contain_required_fields(self, client):
        """Test that sessions have all required fields"""
        response = client.get('/api/sessions')
        data = json.loads(response.data)
        
        required_fields = ['id', 'session_type', 'track_name', 'car_name', 'date_time']
        for session in data:
            for field in required_fields:
                assert field in session
    
    def test_sessions_ordered_by_id_desc(self, client):
        """Test that sessions are ordered newest first"""
        response = client.get('/api/sessions')
        data = json.loads(response.data)
        
        # Sessions should be in descending order by ID
        ids = [s['id'] for s in data]
        assert ids == sorted(ids, reverse=True)


class TestSessionDetailAPI:
    """Tests for individual session API endpoint"""
    
    def test_get_session_details(self, client):
        """Test retrieving details for a specific session"""
        response = client.get('/api/session/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'session' in data
        assert 'results' in data
    
    def test_session_detail_contains_metadata(self, client):
        """Test that session details contain metadata"""
        response = client.get('/api/session/2')
        data = json.loads(response.data)
        
        session = data['session']
        assert session['id'] == 2
        assert session['track_name'] == 'Silverstone'
        assert session['session_type'] == 'Race'
    
    def test_session_detail_contains_results(self, client):
        """Test that session details include all results"""
        response = client.get('/api/session/2')
        data = json.loads(response.data)
        
        results = data['results']
        assert len(results) == 3
    
    def test_session_results_contain_driver_info(self, client):
        """Test that results include driver information"""
        response = client.get('/api/session/2')
        data = json.loads(response.data)
        
        result = data['results'][0]
        assert 'driver_name' in result
        assert 'finish_position' in result
        assert 'points' in result
    
    def test_session_not_found_returns_error(self, client):
        """Test that invalid session ID returns error"""
        response = client.get('/api/session/9999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data


class TestDriversAPI:
    """Tests for the drivers list API endpoint"""
    
    def test_get_all_drivers(self, client):
        """Test retrieving all drivers"""
        response = client.get('/api/drivers')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_drivers_are_sorted(self, client):
        """Test that drivers are sorted alphabetically"""
        response = client.get('/api/drivers')
        data = json.loads(response.data)
        
        # Should be sorted alphabetically
        assert data == sorted(data)
    
    def test_drivers_list_contains_expected_names(self, client):
        """Test that driver list contains expected names"""
        response = client.get('/api/drivers')
        data = json.loads(response.data)
        
        assert 'Alice Johnson' in data
        assert 'Bob Smith' in data
        assert 'Charlie Brown' in data


class TestDriverStatsAPI:
    """Tests for driver statistics API endpoint"""
    
    def test_get_driver_stats(self, client):
        """Test retrieving driver statistics"""
        response = client.get('/api/driver/Alice%20Johnson')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'driver_name' in data
        assert 'total_points' in data
    
    def test_driver_stats_contain_all_fields(self, client):
        """Test that driver stats include all required fields"""
        response = client.get('/api/driver/Bob%20Smith')
        data = json.loads(response.data)
        
        required_fields = [
            'driver_name', 'races', 'points_finishes', 
            'total_points', 'poles', 'fastest_laps', 'avg_finish'
        ]
        for field in required_fields:
            assert field in data
    
    def test_driver_stats_accurate_for_alice(self, client):
        """Test that Alice's stats are calculated correctly"""
        response = client.get('/api/driver/Alice%20Johnson')
        data = json.loads(response.data)
        
        # Alice: 3 races, 43 total points, 1 pole
        assert data['races'] == 3
        assert data['total_points'] == 43
        assert data['poles'] == 1
    
    def test_driver_stats_accurate_for_charlie(self, client):
        """Test that Charlie's stats are calculated correctly"""
        response = client.get('/api/driver/Charlie%20Brown')
        data = json.loads(response.data)
        
        # Charlie: 3 races, 40 total points, 1 fastest lap, 1 pole
        assert data['races'] == 3
        assert data['total_points'] == 40
        assert data['fastest_laps'] == 1
        assert data['poles'] == 1
    
    def test_driver_not_found_returns_error(self, client):
        """Test that unknown driver returns error"""
        response = client.get('/api/driver/UnknownDriver')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data


class TestStandingsAPI:
    """Tests for championship standings API endpoint"""
    
    def test_get_standings(self, client):
        """Test retrieving championship standings"""
        response = client.get('/api/standings')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 3
    
    def test_standings_ordered_by_points(self, client):
        """Test that standings are ordered by points"""
        response = client.get('/api/standings')
        data = json.loads(response.data)
        
        # Should be ordered by points descending
        points = [d['points'] for d in data]
        assert points == sorted(points, reverse=True)
    
    def test_standings_contain_position(self, client):
        """Test that standings include position field"""
        response = client.get('/api/standings')
        data = json.loads(response.data)
        
        for i, driver in enumerate(data, 1):
            assert driver['position'] == i
    
    def test_standings_show_correct_leaders(self, client):
        """Test that standings show correct leader"""
        response = client.get('/api/standings')
        data = json.loads(response.data)
        
        # Alice should be leading with 43 points
        # Charlie has 40, Bob has 33
        assert data[0]['driver_name'] == 'Alice Johnson'
        assert data[0]['points'] == 43
    
    def test_standings_include_stats(self, client):
        """Test that standings include race statistics"""
        response = client.get('/api/standings')
        data = json.loads(response.data)
        
        for driver in data:
            assert 'races' in driver
            assert 'fastest_laps' in driver
            assert 'poles' in driver


class TestAPIResponseFormat:
    """Tests for API response format consistency"""
    
    def test_json_content_type(self, client):
        """Test that API responses are JSON"""
        response = client.get('/api/sessions')
        assert response.content_type == 'application/json'
    
    def test_api_error_format(self, client):
        """Test that API errors follow expected format"""
        response = client.get('/api/session/9999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert 'error' in data
    
    def test_empty_list_response(self, client):
        """Test that empty responses return valid JSON arrays"""
        response = client.get('/api/sessions')
        data = json.loads(response.data)
        
        # Should be valid JSON array even if empty
        assert isinstance(data, list)
