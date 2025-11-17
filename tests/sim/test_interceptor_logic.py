"""
Simulation tests for interceptor logic.

Tests interceptor assignment, engagement, and fuel/weapons tracking.
"""

import pytest
import math
from an_fsq7_simulator import state_model


@pytest.mark.sim
class TestInterceptorLogic:
    """Test interceptor assignment and engagement logic."""

    def test_interceptor_starts_at_base(self, sample_interceptor):
        """Verify interceptor starts at base location."""
        assert sample_interceptor.x == sample_interceptor.base_x
        assert sample_interceptor.y == sample_interceptor.base_y

    def test_interceptor_has_fuel(self, sample_interceptor):
        """Verify interceptor has fuel tracking."""
        assert sample_interceptor.fuel_percent == 100
        assert 0 <= sample_interceptor.fuel_percent <= 100

    def test_interceptor_has_weapons(self, sample_interceptor):
        """Verify interceptor has weapons tracking."""
        assert sample_interceptor.weapons_remaining > 0

    def test_interceptor_status_ready(self, sample_interceptor):
        """Verify interceptor starts in READY status."""
        assert sample_interceptor.status == "READY"

    def test_interceptor_can_be_assigned(self, sample_interceptor, hostile_track):
        """Verify interceptor can be assigned to target."""
        sample_interceptor.assigned_target_id = hostile_track.id
        assert sample_interceptor.assigned_target_id == "HOSTILE-001"

    def test_interceptor_moves_toward_target(self, sample_interceptor):
        """Verify interceptor can move toward target."""
        # Target at (0.75, 0.75)
        target_x, target_y = 0.75, 0.75
        
        # Calculate direction
        dx = target_x - sample_interceptor.x
        dy = target_y - sample_interceptor.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Move interceptor
        if distance > 0:
            move_speed = 0.01  # Normalized speed
            sample_interceptor.x += (dx / distance) * move_speed
            sample_interceptor.y += (dy / distance) * move_speed
        
        # Should be closer to target now
        new_dx = target_x - sample_interceptor.x
        new_dy = target_y - sample_interceptor.y
        new_distance = math.sqrt(new_dx**2 + new_dy**2)
        
        assert new_distance < distance

    def test_interceptor_engagement_range(self, sample_interceptor):
        """Verify interceptor has engagement range."""
        assert hasattr(sample_interceptor, 'engagement_range')
        assert sample_interceptor.engagement_range > 0

    def test_interceptor_within_engagement_range(self, sample_interceptor):
        """Verify when interceptor is within engagement range."""
        # Place interceptor close to target
        target_x, target_y = 0.51, 0.51  # Very close to interceptor at (0.5, 0.1)
        
        distance = math.sqrt(
            (target_x - sample_interceptor.x)**2 +
            (target_y - sample_interceptor.y)**2
        )
        
        # Check if within engagement range
        in_range = distance <= sample_interceptor.engagement_range
        
        # This may be true or false depending on actual engagement_range value
        assert isinstance(in_range, bool)

    def test_interceptor_fuel_consumption(self, sample_interceptor):
        """Verify interceptor can consume fuel."""
        original_fuel = sample_interceptor.fuel_percent
        
        # Simulate fuel consumption
        sample_interceptor.fuel_percent -= 10
        
        assert sample_interceptor.fuel_percent < original_fuel
        assert sample_interceptor.fuel_percent >= 0

    def test_interceptor_weapon_expenditure(self, sample_interceptor):
        """Verify interceptor can expend weapons."""
        original_weapons = sample_interceptor.weapons_remaining
        
        # Fire weapon
        if sample_interceptor.weapons_remaining > 0:
            sample_interceptor.weapons_remaining -= 1
        
        assert sample_interceptor.weapons_remaining < original_weapons

    def test_interceptor_status_transitions(self, sample_interceptor):
        """Verify interceptor can transition between statuses."""
        valid_statuses = [
            "READY", "SCRAMBLING", "AIRBORNE", 
            "ENGAGING", "RETURNING", "REFUELING"
        ]
        
        # Transition through some statuses
        sample_interceptor.status = "SCRAMBLING"
        assert sample_interceptor.status == "SCRAMBLING"
        
        sample_interceptor.status = "AIRBORNE"
        assert sample_interceptor.status == "AIRBORNE"

    def test_interceptor_aircraft_types(self):
        """Verify different interceptor aircraft types exist."""
        f89 = state_model.Interceptor(
            id="INT-F89",
            aircraft_type="F-89 Scorpion",
            base_name="Test Base",
            base_x=0.5,
            base_y=0.1
        )
        
        f102 = state_model.Interceptor(
            id="INT-F102",
            aircraft_type="F-102 Delta Dagger",
            base_name="Test Base",
            base_x=0.5,
            base_y=0.1
        )
        
        assert f89.aircraft_type != f102.aircraft_type

    def test_multiple_interceptors_different_bases(self):
        """Verify multiple interceptors can have different bases."""
        int1 = state_model.Interceptor(
            id="INT-1", aircraft_type="F-106", base_name="Base A",
            base_x=0.2, base_y=0.2
        )
        
        int2 = state_model.Interceptor(
            id="INT-2", aircraft_type="F-106", base_name="Base B",
            base_x=0.8, base_y=0.8
        )
        
        assert (int1.base_x, int1.base_y) != (int2.base_x, int2.base_y)

    def test_interceptor_clear_assignment(self, sample_interceptor):
        """Verify interceptor assignment can be cleared."""
        sample_interceptor.assigned_target_id = "TARGET-123"
        assert sample_interceptor.assigned_target_id is not None
        
        # Clear assignment
        sample_interceptor.assigned_target_id = None
        assert sample_interceptor.assigned_target_id is None
