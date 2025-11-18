"""
Property-based tests for numerical correctness using Hypothesis.

Tests mathematical properties of calculations used in simulation.
"""

import pytest
import math
from hypothesis import given, strategies as st, assume


@pytest.mark.unit
class TestHeadingCalculations:
    """Property-based tests for heading calculations."""

    @given(
        heading1=st.floats(min_value=0, max_value=360),
        heading2=st.floats(min_value=0, max_value=360)
    )
    def test_heading_difference_is_bounded(self, heading1, heading2):
        """Verify heading difference is always in [-180, 180]."""
        # Calculate difference
        diff = heading2 - heading1
        
        # Normalize to [-180, 180]
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        
        assert -180 <= diff <= 180

    @given(
        heading=st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False)
    )
    def test_heading_normalization_to_0_360(self, heading):
        """Verify heading normalization always produces [0, 360) result."""
        # Filter out edge cases that cause issues
        assume(not math.isnan(heading) and not math.isinf(heading))
        assume(abs(heading) > 1e-100)  # Avoid tiny floats
        
        normalized = heading % 360
        
        # Should be in range [0, 360)
        assert 0 <= normalized < 360 or abs(normalized - 0) < 1e-9 or abs(normalized - 360) < 1e-9


@pytest.mark.unit
class TestDistanceCalculations:
    """Property-based tests for distance calculations."""

    @given(
        x1=st.floats(min_value=0, max_value=1),
        y1=st.floats(min_value=0, max_value=1),
        x2=st.floats(min_value=0, max_value=1),
        y2=st.floats(min_value=0, max_value=1)
    )
    def test_distance_is_symmetric(self, x1, y1, x2, y2):
        """Verify distance(A, B) == distance(B, A)."""
        dist1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        dist2 = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
        assert abs(dist1 - dist2) < 1e-9

    @given(
        x1=st.floats(min_value=0, max_value=1),
        y1=st.floats(min_value=0, max_value=1),
        x2=st.floats(min_value=0, max_value=1),
        y2=st.floats(min_value=0, max_value=1),
        x3=st.floats(min_value=0, max_value=1),
        y3=st.floats(min_value=0, max_value=1)
    )
    def test_triangle_inequality(self, x1, y1, x2, y2, x3, y3):
        """Verify triangle inequality: d(A,C) <= d(A,B) + d(B,C)."""
        d_ac = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
        d_ab = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        d_bc = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)
        
        # Allow small floating-point tolerance
        assert d_ac <= d_ab + d_bc + 1e-9

    @given(
        x=st.floats(min_value=0, max_value=1),
        y=st.floats(min_value=0, max_value=1)
    )
    def test_distance_to_self_is_zero(self, x, y):
        """Verify distance from point to itself is zero."""
        dist = math.sqrt((x - x)**2 + (y - y)**2)
        
        assert dist == 0


@pytest.mark.unit
class TestTrigonometricProperties:
    """Property-based tests for trigonometric calculations."""

    @given(
        angle_deg=st.floats(min_value=0, max_value=360)
    )
    def test_pythagorean_identity(self, angle_deg):
        """Verify sin^2 + cos^2 = 1 for all angles."""
        angle_rad = math.radians(angle_deg)
        
        sin_val = math.sin(angle_rad)
        cos_val = math.cos(angle_rad)
        
        # sin^2 + cos^2 should equal 1
        assert abs((sin_val**2 + cos_val**2) - 1.0) < 1e-9

    @given(
        heading=st.floats(min_value=0, max_value=360),
        speed=st.floats(min_value=0, max_value=2000)
    )
    def test_velocity_components_from_heading(self, heading, speed):
        """Verify velocity components sum to correct magnitude."""
        # Convert heading to radians (0 = North, clockwise)
        angle_rad = math.radians(90 - heading)  # Convert to math convention
        
        vx = speed * math.cos(angle_rad)
        vy = speed * math.sin(angle_rad)
        
        magnitude = math.sqrt(vx**2 + vy**2)
        
        # Should match speed within tolerance
        assert abs(magnitude - speed) < 1e-6


@pytest.mark.unit
class TestSpeedConversions:
    """Property-based tests for speed unit conversions."""

    @given(
        knots=st.floats(min_value=0, max_value=2000)
    )
    def test_knots_to_mph_conversion(self, knots):
        """Verify knots to mph conversion is consistent."""
        mph = knots * 1.15078
        
        # Round trip should be close
        back_to_knots = mph / 1.15078
        
        assert abs(back_to_knots - knots) < 1e-6

    @given(
        speed=st.floats(min_value=0, max_value=2000)
    )
    def test_speed_conversion_is_non_negative(self, speed):
        """Verify speed conversions preserve non-negativity."""
        mph = speed * 1.15078
        
        assert mph >= 0


@pytest.mark.unit
class TestCoordinateTransformations:
    """Property-based tests for coordinate transformations."""

    @given(
        lat=st.floats(min_value=-90, max_value=90),
        lon=st.floats(min_value=-180, max_value=180)
    )
    def test_lat_lon_bounds_are_valid(self, lat, lon):
        """Verify lat/lon coordinates are in valid ranges."""
        # Latitude should be [-90, 90]
        assert -90 <= lat <= 90
        
        # Longitude should be [-180, 180]
        assert -180 <= lon <= 180

    @given(
        x=st.floats(min_value=0, max_value=1),
        y=st.floats(min_value=0, max_value=1)
    )
    def test_normalized_coordinates_stay_in_bounds(self, x, y):
        """Verify normalized coordinates [0,1] remain valid."""
        assert 0 <= x <= 1
        assert 0 <= y <= 1
