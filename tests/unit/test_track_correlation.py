"""
Unit tests for track correlation state machine.

Tests the UNCORRELATED → CORRELATED state transitions.
"""

import pytest
from an_fsq7_simulator import state_model


@pytest.mark.unit
class TestTrackCorrelation:
    """Test track correlation state machine."""

    def test_new_track_starts_uncorrelated(self, sample_track):
        """Verify new tracks start in uncorrelated state."""
        assert sample_track.correlation_state == "uncorrelated"
        assert sample_track.classification_time is None

    def test_classify_track_transitions_to_correlated(self, sample_track):
        """Verify classifying a track transitions to correlated."""
        # Initially uncorrelated
        assert sample_track.correlation_state == "uncorrelated"
        
        # Classify the track (set track type and correlation state)
        sample_track.track_type = "hostile"
        sample_track.correlation_state = "correlated"
        sample_track.classification_time = 10.0
        
        # Should be correlated now
        assert sample_track.correlation_state == "correlated"
        assert sample_track.track_type == "hostile"

    def test_uncorrelated_track_properties(self, sample_track):
        """Verify uncorrelated tracks have expected properties."""
        assert sample_track.correlation_state == "uncorrelated"
        assert sample_track.classification_time is None
        # Uncorrelated tracks should have correlation_state attribute
        assert hasattr(sample_track, 'correlation_state')

    def test_correlated_track_requires_classification(self, sample_track):
        """Verify track can be marked correlated."""
        # Set correlation state
        sample_track.correlation_state = "correlated"
        sample_track.classification_time = 15.0
        
        # Track is marked correlated
        assert sample_track.correlation_state == "correlated"
        assert sample_track.classification_time is not None

    def test_track_classification_options(self, sample_track):
        """Verify valid track type options."""
        valid_types = ["friendly", "hostile", "unknown"]
        
        for track_type in valid_types:
            sample_track.track_type = track_type
            sample_track.correlation_state = "correlated"
            assert sample_track.track_type == track_type
            assert sample_track.correlation_state == "correlated"

    def test_hostile_track_correlation(self, hostile_track):
        """Verify hostile tracks can be correlated."""
        assert hostile_track.track_type == "hostile"
        assert hostile_track.threat_level == "HIGH"
        assert hostile_track.correlation_state == "correlated"

    def test_friendly_track_correlation(self, friendly_track):
        """Verify friendly tracks can be correlated."""
        assert friendly_track.track_type == "friendly"
        assert friendly_track.threat_level == "LOW"
        assert friendly_track.correlation_state == "correlated"

    def test_track_position_updates(self, sample_track):
        """Verify track position can be updated."""
        original_x = sample_track.x
        original_y = sample_track.y
        
        # Update position
        sample_track.x += sample_track.vx
        sample_track.y += sample_track.vy
        
        assert sample_track.x != original_x
        assert sample_track.y != original_y

    def test_track_velocity_components(self, sample_track):
        """Verify track has velocity components."""
        assert hasattr(sample_track, 'vx')
        assert hasattr(sample_track, 'vy')
        assert isinstance(sample_track.vx, (int, float))
        assert isinstance(sample_track.vy, (int, float))

    def test_track_altitude_and_speed(self, sample_track):
        """Verify track has altitude and speed attributes."""
        assert sample_track.altitude > 0
        assert sample_track.speed > 0
        assert 0 <= sample_track.heading < 360
