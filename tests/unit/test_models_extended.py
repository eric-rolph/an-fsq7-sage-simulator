"""
Additional unit tests for simulation models - expanding coverage.

Tests VacuumTubeBank, Interceptor, and edge cases.
"""

import pytest
import math
from an_fsq7_simulator.sim import models


@pytest.mark.unit
class TestVacuumTubeBankWarmup:
    """Test vacuum tube warmup simulation."""

    def test_vacuum_tube_bank_initialization(self):
        """Verify VacuumTubeBank initializes correctly."""
        bank = models.VacuumTubeBank()
        
        assert bank.total_tubes == 58000
        assert bank.active_tubes == 0
        assert bank.failed_tubes == 0
        assert bank.temperature == 20.0

    def test_warmup_increases_temperature(self):
        """Verify warm_up increases temperature."""
        bank = models.VacuumTubeBank()
        
        initial_temp = bank.temperature
        bank.warm_up(dt=1.0)
        
        assert bank.temperature > initial_temp

    def test_warmup_activates_tubes_proportionally(self):
        """Verify tubes activate as temperature rises."""
        bank = models.VacuumTubeBank()
        
        # Warm up halfway
        for _ in range(25):
            bank.warm_up(dt=0.1)
        
        # Should have some tubes active
        assert bank.active_tubes > 0
        assert bank.active_tubes < bank.total_tubes

    def test_warmup_caps_at_target_temperature(self):
        """Verify temperature doesn't exceed target."""
        bank = models.VacuumTubeBank()
        
        # Warm up for a long time
        for _ in range(100):
            bank.warm_up(dt=1.0)
        
        assert bank.temperature <= bank.target_temperature

    def test_is_ready_when_warmed_up(self):
        """Verify is_ready returns True when warmed up."""
        bank = models.VacuumTubeBank()
        
        # Initially not ready
        assert bank.is_ready() == False
        
        # Warm up completely
        for _ in range(60):
            bank.warm_up(dt=0.1)
        
        # Should be ready
        assert bank.is_ready() == True

    def test_tick_can_cause_failures(self):
        """Verify tick can simulate tube failures."""
        import random
        
        bank = models.VacuumTubeBank()
        
        # Activate all tubes
        bank.active_tubes = 58000
        bank.temperature = bank.target_temperature
        
        # Mock random to force failure
        original_random = random.random
        random.random = lambda: 0.0  # Always triggers failure
        
        try:
            bank.tick(dt=0.05)
            
            # Should have decremented active tubes
            assert bank.active_tubes == 57999
            assert bank.failed_tubes == 1
        finally:
            random.random = original_random

    def test_shutdown_resets_temperature(self):
        """Verify shutdown cools down tubes."""
        bank = models.VacuumTubeBank()
        
        # Warm up first
        bank.temperature = 270.0
        bank.active_tubes = 58000
        
        bank.shutdown()
        
        assert bank.temperature == 20.0
        assert bank.active_tubes == 0


@pytest.mark.unit
class TestInterceptorMovement:
    """Test interceptor aircraft movement."""

    def test_interceptor_initialization_at_base(self):
        """Verify interceptor starts at base location."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.3,
            base_y=0.8
        )
        
        assert interceptor.x == 0.3
        assert interceptor.y == 0.8

    def test_interceptor_custom_position(self):
        """Verify interceptor can have custom initial position."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.3,
            base_y=0.8,
            x=0.5,
            y=0.5
        )
        
        assert interceptor.x == 0.5
        assert interceptor.y == 0.5

    def test_distance_to_target(self):
        """Verify distance calculation."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.0,
            base_y=0.0,
            x=0.0,
            y=0.0
        )
        
        # Distance to (3,4) should be 5 (3-4-5 triangle)
        distance = interceptor.distance_to_target(3.0, 4.0)
        assert abs(distance - 5.0) < 0.001

    def test_move_toward_target_changes_position(self):
        """Verify move_toward_target updates position."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.2,
            base_y=0.2,
            current_speed=600
        )
        
        initial_x = interceptor.x
        initial_y = interceptor.y
        
        # Move toward target
        interceptor.move_toward_target(0.8, 0.8, dt=1.0)
        
        # Position should change
        assert interceptor.x != initial_x or interceptor.y != initial_y

    def test_move_toward_target_updates_heading(self):
        """Verify move_toward_target updates heading."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.0,
            base_y=0.0,
            current_speed=600
        )
        
        # Move toward northeast target
        interceptor.move_toward_target(1.0, 1.0, dt=0.1)
        
        # Heading should be roughly 45 degrees
        assert 30 <= interceptor.heading <= 60

    def test_move_toward_target_consumes_fuel(self):
        """Verify movement consumes fuel."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.2,
            base_y=0.2,
            current_speed=600,
            fuel_percent=100
        )
        
        initial_fuel = interceptor.fuel_percent
        
        # Move for a while
        for _ in range(100):
            interceptor.move_toward_target(0.8, 0.8, dt=0.1)
        
        # Fuel should decrease
        assert interceptor.fuel_percent < initial_fuel

    def test_move_toward_target_at_target(self):
        """Verify move_toward_target handles already at target."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.5,
            base_y=0.5,
            current_speed=600
        )
        
        # Already at target
        interceptor.move_toward_target(0.5, 0.5, dt=1.0)
        
        # Position shouldn't change significantly
        assert abs(interceptor.x - 0.5) < 0.01
        assert abs(interceptor.y - 0.5) < 0.01

    def test_is_in_weapon_range_when_close(self):
        """Verify weapon range detection when close."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.5,
            base_y=0.5
        )
        
        # Target very close
        assert interceptor.is_in_weapon_range(0.501, 0.501) == True

    def test_is_in_weapon_range_when_far(self):
        """Verify weapon range detection when far."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.1,
            base_y=0.1
        )
        
        # Target far away
        assert interceptor.is_in_weapon_range(0.9, 0.9) == False

    def test_fuel_doesnt_go_negative(self):
        """Verify fuel consumption stops at zero."""
        interceptor = models.Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.2,
            base_y=0.2,
            current_speed=600,
            fuel_percent=1  # Start with very low fuel
        )
        
        # Move until fuel depleted
        for _ in range(1000):
            interceptor.move_toward_target(0.8, 0.8, dt=1.0)
        
        # Fuel should be 0, not negative
        assert interceptor.fuel_percent >= 0


@pytest.mark.unit
class TestMissionClockAdvanced:
    """Additional tests for MissionClock."""

    def test_mission_clock_minute_rollover(self):
        """Verify minutes roll over to hours."""
        clock = models.MissionClock()
        
        clock.seconds = 59
        clock.minutes = 59
        
        # Advance past hour boundary
        clock.tick(dt=2.0)
        
        assert clock.hours == 1
        assert clock.minutes == 0

    def test_mission_clock_large_dt(self):
        """Verify clock handles large time jumps."""
        clock = models.MissionClock()
        
        # Jump forward by many seconds
        clock.tick(dt=125.5)  # 2 minutes, 5.5 seconds
        
        assert clock.minutes == 2
        assert clock.seconds >= 5

    def test_mission_clock_to_string_format(self):
        """Verify to_string formats correctly."""
        clock = models.MissionClock()
        
        clock.hours = 1
        clock.minutes = 23
        clock.seconds = 45
        
        result = clock.to_string()
        
        assert result == "01:23:45"

    def test_mission_clock_to_string_zero_padding(self):
        """Verify to_string zero-pads single digits."""
        clock = models.MissionClock()
        
        clock.hours = 0
        clock.minutes = 5
        clock.seconds = 9
        
        result = clock.to_string()
        
        assert result == "00:05:09"


@pytest.mark.unit
class TestRadarTargetAdvanced:
    """Additional tests for RadarTarget."""

    def test_radar_target_wrap_left_boundary(self):
        """Verify wrap_bounds handles left edge."""
        target = models.RadarTarget(
            target_id="TEST-001",
            x=-10,
            y=300,
            heading=270,
            speed=500,
            altitude=30000
        )
        
        target.wrap_bounds(width=800, height=600)
        
        # Should wrap to right side
        assert target.x == 800

    def test_radar_target_wrap_right_boundary(self):
        """Verify wrap_bounds handles right edge."""
        target = models.RadarTarget(
            target_id="TEST-001",
            x=810,
            y=300,
            heading=90,
            speed=500,
            altitude=30000
        )
        
        target.wrap_bounds(width=800, height=600)
        
        # Should wrap to left side
        assert target.x == 0

    def test_radar_target_wrap_top_boundary(self):
        """Verify wrap_bounds handles top edge."""
        target = models.RadarTarget(
            target_id="TEST-001",
            x=400,
            y=-10,
            heading=0,
            speed=500,
            altitude=30000
        )
        
        target.wrap_bounds(width=800, height=600)
        
        # Should wrap to bottom
        assert target.y == 600

    def test_radar_target_wrap_bottom_boundary(self):
        """Verify wrap_bounds handles bottom edge."""
        target = models.RadarTarget(
            target_id="TEST-001",
            x=400,
            y=610,
            heading=180,
            speed=500,
            altitude=30000
        )
        
        target.wrap_bounds(width=800, height=600)
        
        # Should wrap to top
        assert target.y == 0

    def test_radar_target_distance_to_self(self):
        """Verify distance_to returns 0 for same position."""
        target = models.RadarTarget(
            target_id="TEST-001",
            x=100,
            y=200,
            heading=0,
            speed=500,
            altitude=30000
        )
        
        distance = target.distance_to(100, 200)
        
        assert distance == 0.0
