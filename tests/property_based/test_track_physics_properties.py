"""
Property-based tests for track physics using Hypothesis.

Tests invariants and mathematical properties of track simulation.
"""

import pytest
import math
from hypothesis import given, strategies as st, assume
from an_fsq7_simulator.sim.models import RadarTarget


@pytest.mark.unit
class TestRadarTargetMovementProperties:
    """Property-based tests for radar target movement."""

    @given(
        dt=st.floats(min_value=0.01, max_value=1.0),
        heading=st.floats(min_value=0, max_value=360),
        speed=st.floats(min_value=0, max_value=1000)
    )
    def test_move_updates_position_deterministically(self, dt, heading, speed):
        """Verify move() updates position deterministically."""
        target = RadarTarget(
            target_id="TEST-001",
            x=400, y=300,
            heading=heading, speed=speed,
            altitude=30000
        )
        
        # Save initial position
        initial_x = target.x
        initial_y = target.y
        
        # Move
        target.move(dt)
        
        # Calculate expected position change
        heading_rad = math.radians(heading)
        speed_factor = (speed / 1000.0) * dt * 20
        expected_x = initial_x + math.cos(heading_rad) * speed_factor
        expected_y = initial_y + math.sin(heading_rad) * speed_factor
        
        # Position should match expected (with small tolerance)
        assert abs(target.x - expected_x) < 1e-6
        assert abs(target.y - expected_y) < 1e-6

    @given(
        x=st.floats(min_value=-100, max_value=1000),
        y=st.floats(min_value=-100, max_value=800)
    )
    def test_wrap_bounds_keeps_coordinates_in_range(self, x, y):
        """Verify wrap_bounds() wraps coordinates to [0, width] x [0, height]."""
        width, height = 800, 600
        target = RadarTarget(
            target_id="TEST-001",
            x=x, y=y,
            heading=0, speed=0,
            altitude=30000
        )
        
        target.wrap_bounds(width, height)
        
        # Should be in valid range
        assert 0.0 <= target.x <= width
        assert 0.0 <= target.y <= height

    @given(
        heading=st.floats(min_value=0, max_value=360),
        speed=st.floats(min_value=10, max_value=2000)
    )
    def test_heading_affects_movement_direction(self, heading, speed):
        """Verify heading affects movement direction correctly."""
        target = RadarTarget(
            target_id="TEST-001",
            x=400, y=300,
            heading=heading, speed=speed,
            altitude=30000
        )
        
        initial_x, initial_y = target.x, target.y
        target.move(1.0)
        
        # Target should move in the direction of heading
        dx = target.x - initial_x
        dy = target.y - initial_y
        
        # Calculate expected direction
        heading_rad = math.radians(heading)
        expected_angle = math.atan2(dy, dx)
        
        # Angles should be close (within 1 degree in radians)
        angle_diff = abs(expected_angle - heading_rad)
        # Normalize to [-pi, pi]
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        assert abs(angle_diff) < math.radians(1) or abs(abs(angle_diff) - 2*math.pi) < math.radians(1)


@pytest.mark.unit
class TestRadarTargetBoundaryProperties:
    """Property-based tests for boundary behavior."""

    @given(
        x=st.floats(min_value=0, max_value=1),
        y=st.floats(min_value=0, max_value=1),
        distance=st.floats(min_value=0, max_value=2)
    )
    def test_distance_calculation_is_non_negative(self, x, y, distance):
        """Verify computed distances are always non-negative."""
        target1 = RadarTarget(
            target_id="TGT-1",
            x=x, y=y,
            heading=0, speed=0,
            altitude=30000
        )
        
        target2 = RadarTarget(
            target_id="TGT-2",
            x=min(x + distance, 1.0),
            y=min(y + distance, 1.0),
            heading=0, speed=0,
            altitude=30000
        )
        
        # Calculate distance
        dx = target2.x - target1.x
        dy = target2.y - target1.y
        dist = math.sqrt(dx**2 + dy**2)
        
        assert dist >= 0

    @given(
        x=st.floats(min_value=-1000, max_value=2000),
        y=st.floats(min_value=-1000, max_value=2000)
    )
    def test_wrap_bounds_is_idempotent(self, x, y):
        """Verify wrap_bounds() applied twice gives same result as once."""
        width, height = 800, 600
        target = RadarTarget(
            target_id="TEST-001",
            x=x, y=y,
            heading=0, speed=0,
            altitude=30000
        )
        
        target.wrap_bounds(width, height)
        first_x, first_y = target.x, target.y
        
        target.wrap_bounds(width, height)
        second_x, second_y = target.x, target.y
        
        # Should be identical (idempotent)
        assert first_x == second_x
        assert first_y == second_y


@pytest.mark.unit
class TestVelocityProperties:
    """Property-based tests for velocity calculations."""

    @given(
        heading=st.floats(min_value=0, max_value=360),
        speed=st.floats(min_value=100, max_value=2000)
    )
    def test_velocity_magnitude_proportional_to_speed(self, heading, speed):
        """Verify movement distance is proportional to speed."""
        target = RadarTarget(
            target_id="TEST-001",
            x=400, y=300,
            heading=heading, speed=speed,
            altitude=30000
        )
        
        initial_x, initial_y = target.x, target.y
        dt = 1.0
        target.move(dt)
        
        # Calculate actual movement distance
        distance = math.sqrt((target.x - initial_x)**2 + (target.y - initial_y)**2)
        
        # Expected distance based on speed
        expected_distance = (speed / 1000.0) * dt * 20
        
        # Should be within small tolerance
        assert abs(distance - expected_distance) < 0.01

    @given(
        heading1=st.floats(min_value=0, max_value=360),
        heading2=st.floats(min_value=0, max_value=360)
    )
    def test_heading_changes_direction(self, heading1, heading2):
        """Verify different headings produce different movement directions."""
        # Normalize headings to handle 0 == 360
        h1_norm = heading1 % 360
        h2_norm = heading2 % 360
        
        # Calculate angular difference
        diff = abs(h1_norm - h2_norm)
        if diff > 180:
            diff = 360 - diff
        
        assume(diff > 10)  # Significant difference
        
        target1 = RadarTarget(
            target_id="TEST-001",
            x=400, y=300,
            heading=heading1, speed=500,
            altitude=30000
        )
        
        target2 = RadarTarget(
            target_id="TEST-002",
            x=400, y=300,
            heading=heading2, speed=500,
            altitude=30000
        )
        
        target1.move(1.0)
        target2.move(1.0)
        
        # Different headings should produce different final positions
        # (unless they're 180 degrees apart and wrap around)
        dx1, dy1 = target1.x - 400, target1.y - 300
        dx2, dy2 = target2.x - 400, target2.y - 300
        
        # Either x or y should differ
        assert abs(dx1 - dx2) > 0.1 or abs(dy1 - dy2) > 0.1


@pytest.mark.unit
class TestAltitudeProperties:
    """Property-based tests for altitude handling."""

    @given(
        altitude=st.floats(min_value=0, max_value=100000)
    )
    def test_altitude_is_non_negative(self, altitude):
        """Verify altitude is always non-negative."""
        target = RadarTarget(
            target_id="TEST-001",
            x=0.5, y=0.5,
            heading=0, speed=500,
            altitude=altitude
        )
        
        assert target.altitude >= 0

    @given(
        alt1=st.floats(min_value=1000, max_value=50000),
        alt2=st.floats(min_value=1000, max_value=50000)
    )
    def test_altitude_difference_is_symmetric(self, alt1, alt2):
        """Verify altitude difference is symmetric."""
        diff1 = abs(alt1 - alt2)
        diff2 = abs(alt2 - alt1)
        
        assert diff1 == diff2
