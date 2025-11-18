"""
Unit tests for state model feature generation functions.

Tests generate_feature_* functions that format track data for tabular display.
"""

import pytest
from an_fsq7_simulator.state_model import (
    Track,
    generate_feature_a,
    generate_feature_b,
    generate_feature_c,
    generate_feature_d,
    calculate_position_mode
)


@pytest.mark.unit
class TestFeatureGeneration:
    """Test feature generation for tabular track display."""

    def test_feature_a_full_id(self):
        """Verify feature A handles full track ID."""
        track = Track(
            id="TK1234",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_a(track)
        
        assert result == "1234"

    def test_feature_a_strips_tk_prefix(self):
        """Verify feature A strips TK prefix."""
        track = Track(
            id="TK99",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_a(track)
        
        assert result == "99  "  # Padded to 4 chars

    def test_feature_a_strips_track_prefix(self):
        """Verify feature A strips TRACK prefix."""
        track = Track(
            id="TRACK007",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_a(track)
        
        assert result == "007 "

    def test_feature_a_truncates_long_ids(self):
        """Verify feature A truncates IDs longer than 4 chars."""
        track = Track(
            id="VERYLONGID",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_a(track)
        
        assert len(result) == 4

    def test_feature_a_pads_short_ids(self):
        """Verify feature A pads short IDs."""
        track = Track(
            id="X",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_a(track)
        
        assert result == "X   "

    def test_feature_b_altitude_and_speed_slow(self):
        """Verify feature B formats altitude and slow speed."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=250, altitude=8000,
            track_type="unknown"
        )
        
        result = generate_feature_b(track)
        
        assert result == " 8SL"

    def test_feature_b_medium_speed(self):
        """Verify feature B identifies medium speed."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=450, altitude=35000,
            track_type="unknown"
        )
        
        result = generate_feature_b(track)
        
        assert result == "35MD"

    def test_feature_b_fast_speed(self):
        """Verify feature B identifies fast speed."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=700, altitude=42000,
            track_type="unknown"
        )
        
        result = generate_feature_b(track)
        
        assert result == "42FS"

    def test_feature_b_supersonic_speed(self):
        """Verify feature B identifies supersonic speed."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=1200, altitude=50000,
            track_type="unknown"
        )
        
        result = generate_feature_b(track)
        
        assert result == "50SS"

    def test_feature_c_friendly_low(self):
        """Verify feature C formats friendly low threat."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="friendly",
            threat_level="low"
        )
        
        result = generate_feature_c(track)
        
        assert result == "FR L"

    def test_feature_c_hostile_high(self):
        """Verify feature C formats hostile high threat."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="hostile",
            threat_level="high"
        )
        
        result = generate_feature_c(track)
        
        assert result == "HS H"

    def test_feature_c_unknown_medium(self):
        """Verify feature C formats unknown medium threat."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown",
            threat_level="medium"
        )
        
        result = generate_feature_c(track)
        
        assert result == "UN M"

    def test_feature_c_missile_critical(self):
        """Verify feature C formats missile critical threat."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=1500, altitude=20000,
            track_type="missile",
            threat_level="critical"
        )
        
        result = generate_feature_c(track)
        
        assert result == "MS C"

    def test_feature_c_bomber(self):
        """Verify feature C formats bomber track type."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="bomber",
            threat_level="high"
        )
        
        result = generate_feature_c(track)
        
        assert result == "BM H"

    def test_feature_c_fighter(self):
        """Verify feature C formats fighter track type."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=600, altitude=35000,
            track_type="fighter",
            threat_level="medium"
        )
        
        result = generate_feature_c(track)
        
        assert result == "FT M"

    def test_feature_d_north(self):
        """Verify feature D identifies north heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "N "

    def test_feature_d_northeast(self):
        """Verify feature D identifies northeast heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=45, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "NE"

    def test_feature_d_east(self):
        """Verify feature D identifies east heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=90, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "E "

    def test_feature_d_southeast(self):
        """Verify feature D identifies southeast heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=135, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "SE"

    def test_feature_d_south(self):
        """Verify feature D identifies south heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=180, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "S "

    def test_feature_d_southwest(self):
        """Verify feature D identifies southwest heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=225, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "SW"

    def test_feature_d_west(self):
        """Verify feature D identifies west heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=270, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "W "

    def test_feature_d_northwest(self):
        """Verify feature D identifies northwest heading."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=315, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "NW"

    def test_feature_d_wraps_heading(self):
        """Verify feature D handles heading > 360."""
        track = Track(
            id="TEST",
            x=0.5, y=0.5,
            heading=405,  # 405 % 360 = 45 (NE)
            speed=500, altitude=30000,
            track_type="unknown"
        )
        
        result = generate_feature_d(track)
        
        assert result == "NE"

    def test_calculate_position_mode_top_left(self):
        """Verify position mode for top-left quadrant."""
        track = Track(
            id="TEST",
            x=0.2, y=0.3,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        mode = calculate_position_mode(track)
        
        assert mode == 0  # RIGHT

    def test_calculate_position_mode_top_right(self):
        """Verify position mode for top-right quadrant."""
        track = Track(
            id="TEST",
            x=0.8, y=0.3,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        mode = calculate_position_mode(track)
        
        assert mode == 1  # LEFT

    def test_calculate_position_mode_bottom_left(self):
        """Verify position mode for bottom-left quadrant."""
        track = Track(
            id="TEST",
            x=0.2, y=0.8,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        mode = calculate_position_mode(track)
        
        assert mode == 0  # RIGHT

    def test_calculate_position_mode_bottom_right(self):
        """Verify position mode for bottom-right quadrant."""
        track = Track(
            id="TEST",
            x=0.8, y=0.8,
            heading=0, speed=500, altitude=30000,
            track_type="unknown"
        )
        
        mode = calculate_position_mode(track)
        
        assert mode == 1  # LEFT
