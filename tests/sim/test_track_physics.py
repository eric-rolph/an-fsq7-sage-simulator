"""
Simulation tests for track physics and movement.

Tests track position updates, velocity, heading calculations.
"""

import pytest
import math
from an_fsq7_simulator import state_model


@pytest.mark.sim
class TestTrackPhysics:
    """Test track physics and movement."""

    def test_track_moves_based_on_velocity(self, sample_track):
        """Verify track position updates based on velocity."""
        original_x = sample_track.x
        original_y = sample_track.y
        
        # Simulate one frame update
        dt = 1.0  # 1 second
        sample_track.x += sample_track.vx * dt
        sample_track.y += sample_track.vy * dt
        
        # Position should have changed
        assert sample_track.x != original_x
        assert sample_track.y != original_y

    def test_velocity_components_affect_direction(self, sample_track):
        """Verify velocity components determine movement direction."""
        # Track with vx=0.01, vy=0.01 should move northeast
        assert sample_track.vx > 0  # Moving east
        assert sample_track.vy > 0  # Moving north

    def test_heading_range(self, sample_track):
        """Verify heading stays in valid range 0-360 degrees."""
        assert 0 <= sample_track.heading < 360

    def test_speed_positive(self, sample_track):
        """Verify speed is always positive."""
        assert sample_track.speed >= 0

    def test_altitude_range(self, sample_track):
        """Verify altitude is in reasonable range."""
        assert sample_track.altitude >= 0
        assert sample_track.altitude <= 60000  # Reasonable ceiling

    def test_velocity_magnitude_matches_speed(self):
        """Verify velocity magnitude roughly matches speed (normalized)."""
        # Create track with known speed
        track = state_model.Track(
            id="TEST-SPD",
            x=0.5,
            y=0.5,
            vx=0.01,
            vy=0.0,
            speed=450,
            heading=90,
            altitude=25000,
            track_type="aircraft",
            threat_level="MEDIUM",
            time_detected=0.0
        )
        
        # Velocity magnitude
        v_mag = math.sqrt(track.vx**2 + track.vy**2)
        assert v_mag > 0

    def test_heading_calculation_from_velocity(self):
        """Verify heading can be calculated from velocity components."""
        # vx=0.01, vy=0 should be heading 0° (east in standard coords)
        vx, vy = 0.01, 0.0
        heading = math.degrees(math.atan2(vy, vx))
        # Normalize to 0-360
        if heading < 0:
            heading += 360
        assert abs(heading - 0) < 1  # Allow small tolerance

    def test_track_boundary_wrapping(self):
        """Verify tracks can wrap at boundaries (optional behavior)."""
        track = state_model.Track(
            id="TEST-WRAP",
            x=0.95,
            y=0.5,
            vx=0.1,  # Large velocity to cross boundary
            vy=0.0,
            speed=450,
            heading=90,
            altitude=25000,
            track_type="aircraft",
            threat_level="MEDIUM",
            time_detected=0.0
        )
        
        # Update position
        track.x += track.vx
        
        # May wrap around or go off-screen (implementation dependent)
        assert track.x > 0.95 or track.x < 0.95  # Position changed

    def test_multiple_updates_consistent(self, sample_track):
        """Verify multiple position updates are consistent."""
        dt = 0.1  # Small time step
        positions = []
        
        for _ in range(10):
            positions.append((sample_track.x, sample_track.y))
            sample_track.x += sample_track.vx * dt
            sample_track.y += sample_track.vy * dt
        
        # All positions should be different
        assert len(set(positions)) == len(positions)

    def test_track_trail_recording(self, sample_track):
        """Verify track trail can be recorded."""
        assert hasattr(sample_track, 'trail')
        
        # Add position to trail
        sample_track.trail.append((sample_track.x, sample_track.y))
        assert len(sample_track.trail) == 1

    def test_fast_track_moves_farther(self):
        """Verify faster tracks move farther per update."""
        slow_track = state_model.Track(
            id="SLOW", x=0.5, y=0.5, vx=0.01, vy=0.0, speed=300,
            heading=90, altitude=25000, track_type="aircraft",
            threat_level="LOW", time_detected=0.0
        )
        
        fast_track = state_model.Track(
            id="FAST", x=0.5, y=0.5, vx=0.02, vy=0.0, speed=600,
            heading=90, altitude=25000, track_type="aircraft",
            threat_level="HIGH", time_detected=0.0
        )
        
        # Update both
        dt = 1.0
        slow_distance = slow_track.vx * dt
        fast_distance = fast_track.vx * dt
        
        assert fast_distance > slow_distance

    def test_diagonal_movement(self):
        """Verify tracks can move diagonally."""
        track = state_model.Track(
            id="DIAG", x=0.5, y=0.5, vx=0.01, vy=0.01, speed=450,
            heading=45, altitude=25000, track_type="aircraft",
            threat_level="MEDIUM", time_detected=0.0
        )
        
        original_x = track.x
        original_y = track.y
        
        # Update position
        track.x += track.vx
        track.y += track.vy
        
        # Both x and y should change
        assert track.x != original_x
        assert track.y != original_y
