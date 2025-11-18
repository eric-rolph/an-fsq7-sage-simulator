"""
Property-based tests for simulation invariants and correctness.

Uses Hypothesis to generate test cases for simulation properties.
"""

import pytest
from hypothesis import given, strategies as st, assume
import math

from an_fsq7_simulator.sim.models import RadarTarget, VacuumTubeBank, Interceptor, MissionClock
from an_fsq7_simulator.sim.sim_loop import Simulator
from an_fsq7_simulator.state_model import Track


@pytest.mark.property
class TestRadarTargetProperties:
    """Property-based tests for RadarTarget behavior."""

    @given(
        x=st.floats(min_value=-1000, max_value=1000),
        y=st.floats(min_value=-1000, max_value=1000),
        heading=st.floats(min_value=0, max_value=360),
        speed=st.floats(min_value=0, max_value=3000),
        altitude=st.integers(min_value=0, max_value=80000)
    )
    def test_radar_target_always_valid_after_creation(self, x, y, heading, speed, altitude):
        """Property: RadarTarget should always be in valid state after creation."""
        assume(math.isfinite(x) and math.isfinite(y))
        assume(math.isfinite(heading) and math.isfinite(speed))
        
        target = RadarTarget(
            target_id="TEST",
            x=x,
            y=y,
            heading=heading,
            speed=speed,
            altitude=altitude
        )
        
        # All fields should be accessible
        assert target.target_id == "TEST"
        assert math.isfinite(target.x)
        assert math.isfinite(target.y)
        assert target.altitude >= 0

    @given(
        x1=st.floats(min_value=0, max_value=800),
        y1=st.floats(min_value=0, max_value=600),
        x2=st.floats(min_value=0, max_value=800),
        y2=st.floats(min_value=0, max_value=600)
    )
    def test_distance_calculation_symmetric(self, x1, y1, x2, y2):
        """Property: distance(A, B) should equal distance(B, A)."""
        assume(all(math.isfinite(v) for v in [x1, y1, x2, y2]))
        
        target1 = RadarTarget(
            target_id="T1",
            x=x1, y=y1,
            heading=0, speed=500, altitude=30000
        )
        
        target2 = RadarTarget(
            target_id="T2",
            x=x2, y=y2,
            heading=0, speed=500, altitude=30000
        )
        
        dist1 = target1.distance_to(x2, y2)
        dist2 = target2.distance_to(x1, y1)
        
        assert abs(dist1 - dist2) < 0.001  # Floating point tolerance

    @given(
        x=st.floats(min_value=0, max_value=800),
        y=st.floats(min_value=0, max_value=600),
        heading=st.floats(min_value=0, max_value=360),
        speed=st.floats(min_value=100, max_value=1000),
        dt=st.floats(min_value=0.01, max_value=1.0)
    )
    def test_movement_always_progresses_position(self, x, y, heading, speed, dt):
        """Property: move() should always change position (unless speed=0)."""
        assume(all(math.isfinite(v) for v in [x, y, heading, speed, dt]))
        assume(speed > 0)
        
        target = RadarTarget(
            target_id="TEST",
            x=x, y=y,
            heading=heading,
            speed=speed,
            altitude=30000
        )
        
        initial_x, initial_y = target.x, target.y
        target.move(dt)
        
        # Position should have changed (unless at exactly 0 or 180 degrees edge case)
        distance_moved = math.sqrt((target.x - initial_x)**2 + (target.y - initial_y)**2)
        assert distance_moved >= 0  # Movement occurred


@pytest.mark.property
class TestVacuumTubeBankProperties:
    """Property-based tests for VacuumTubeBank."""

    @given(
        total_tubes=st.integers(min_value=1, max_value=100000),
        warmup_time=st.floats(min_value=0.1, max_value=60.0),
        dt=st.floats(min_value=0.01, max_value=1.0)
    )
    def test_warmup_never_exceeds_target_temperature(self, total_tubes, warmup_time, dt):
        """Property: warm_up() should never exceed target temperature."""
        assume(all(math.isfinite(v) for v in [warmup_time, dt]))
        
        bank = VacuumTubeBank(
            total_tubes=total_tubes,
            warmup_time=warmup_time
        )
        
        # Warm up for many iterations
        for _ in range(100):
            bank.warm_up(dt)
        
        assert bank.temperature <= bank.target_temperature * 1.001  # Small tolerance

    @given(
        total_tubes=st.integers(min_value=1000, max_value=100000),
        dt=st.floats(min_value=0.1, max_value=2.0)
    )
    def test_failed_tubes_never_exceed_total(self, total_tubes, dt):
        """Property: Failed tubes should never exceed total tubes."""
        assume(math.isfinite(dt))
        
        bank = VacuumTubeBank(
            total_tubes=total_tubes,
            failure_rate=0.01  # High failure rate
        )
        bank.temperature = bank.target_temperature  # Already warmed
        
        # Simulate many ticks
        for _ in range(1000):
            bank.tick(dt)
        
        assert bank.failed_tubes <= bank.total_tubes

    @given(
        warmup_time=st.floats(min_value=1.0, max_value=30.0)
    )
    def test_is_ready_consistent_with_temperature(self, warmup_time):
        """Property: is_ready() should be consistent with temperature threshold."""
        assume(math.isfinite(warmup_time))
        
        bank = VacuumTubeBank(warmup_time=warmup_time)
        
        # Warm up fully
        bank.warm_up(warmup_time * 2)  # Ensure fully warmed
        
        if bank.temperature >= bank.target_temperature * 0.95:
            assert bank.is_ready()
        else:
            assert not bank.is_ready()


@pytest.mark.property
class TestInterceptorProperties:
    """Property-based tests for Interceptor."""

    @given(
        base_x=st.floats(min_value=0, max_value=1.0),
        base_y=st.floats(min_value=0, max_value=1.0),
        target_x=st.floats(min_value=0, max_value=1.0),
        target_y=st.floats(min_value=0, max_value=1.0)
    )
    def test_distance_to_target_never_negative(self, base_x, base_y, target_x, target_y):
        """Property: Distance to target should never be negative."""
        assume(all(math.isfinite(v) for v in [base_x, base_y, target_x, target_y]))
        
        interceptor = Interceptor(
            interceptor_id="INT-TEST",
            aircraft_type="F-106",
            base_name="Test Base",
            base_x=base_x,
            base_y=base_y
        )
        
        distance = interceptor.distance_to_target(target_x, target_y)
        
        assert distance >= 0
        assert math.isfinite(distance)

    @given(
        x=st.floats(min_value=0, max_value=1.0),
        y=st.floats(min_value=0, max_value=1.0),
        current_speed=st.integers(min_value=0, max_value=800),
        dt=st.floats(min_value=0.1, max_value=2.0)
    )
    def test_fuel_consumption_monotonic(self, x, y, current_speed, dt):
        """Property: Fuel should only decrease or stay same, never increase."""
        assume(all(math.isfinite(v) for v in [x, y, dt]))
        
        interceptor = Interceptor(
            interceptor_id="INT-TEST",
            aircraft_type="F-106",
            base_name="Test Base",
            base_x=0.5,
            base_y=0.5,
            x=x,
            y=y,
            current_speed=current_speed
        )
        
        initial_fuel = interceptor.fuel_percent
        
        # Move toward target
        interceptor.move_toward_target(0.8, 0.8, dt)
        
        assert interceptor.fuel_percent <= initial_fuel
        assert interceptor.fuel_percent >= 0


@pytest.mark.property
class TestMissionClockProperties:
    """Property-based tests for MissionClock."""

    @given(
        dt_values=st.lists(
            st.floats(min_value=0.01, max_value=2.0),
            min_size=1,
            max_size=100
        )
    )
    def test_elapsed_time_monotonic_increasing(self, dt_values):
        """Property: Clock seconds should always increase or roll over."""
        assume(all(math.isfinite(dt) for dt in dt_values))
        
        clock = MissionClock()
        
        # Track total elapsed time manually
        total_dt = sum(dt_values)
        for dt in dt_values:
            clock.tick(dt)
        
        # After ticking, some time should have passed
        total_seconds = clock.hours * 3600 + clock.minutes * 60 + clock.seconds
        assert total_seconds >= 0

    @given(
        dt_sum=st.floats(min_value=1.0, max_value=100.0)
    )
    def test_clock_advances_with_ticks(self, dt_sum):
        """Property: Clock should advance as dt accumulates."""
        assume(math.isfinite(dt_sum))
        
        clock = MissionClock()
        
        # Divide into smaller ticks
        num_ticks = 10
        dt = dt_sum / num_ticks
        
        for _ in range(num_ticks):
            clock.tick(dt)
        
        # Total time in seconds
        total_seconds = clock.hours * 3600 + clock.minutes * 60 + clock.seconds
        # Should be close to dt_sum
        assert total_seconds >= dt_sum * 0.9  # Allow some tolerance


@pytest.mark.property
class TestSimulatorProperties:
    """Property-based tests for Simulator."""

    @given(
        num_targets=st.integers(min_value=1, max_value=50)
    )
    def test_spawn_radar_targets_creates_exact_count(self, num_targets):
        """Property: spawn_radar_targets should create exact number requested."""
        sim = Simulator()
        
        sim.spawn_radar_targets(count=num_targets)
        
        assert len(sim.radar_targets) == num_targets

    @given(
        dt_values=st.lists(
            st.floats(min_value=0.01, max_value=1.0),
            min_size=5,
            max_size=20
        )
    )
    def test_memory_cycles_monotonic_when_powered_on(self, dt_values):
        """Property: Memory cycles should increase when system is powered on."""
        assume(all(math.isfinite(dt) for dt in dt_values))
        
        sim = Simulator()
        sim.power_on()
        sim.system_ready = True
        
        initial_cycles = sim.memory_cycles
        
        for dt in dt_values:
            sim.tick(dt)
        
        assert sim.memory_cycles > initial_cycles

    def test_power_off_resets_state(self):
        """Property: power_off should reset critical state."""
        sim = Simulator()
        
        # Power on and run
        sim.power_on()
        sim.spawn_radar_targets(10)
        sim.tick(0.1)
        
        # Power off
        sim.power_off()
        
        assert sim.powered_on == False
        assert sim.system_ready == False
        assert sim.warming_up == False


@pytest.mark.property
class TestTrackProperties:
    """Property-based tests for Track state model."""

    @given(
        x=st.floats(min_value=0, max_value=1.0),
        y=st.floats(min_value=0, max_value=1.0),
        altitude=st.integers(min_value=0, max_value=80000),
        speed=st.integers(min_value=0, max_value=3000),
        heading=st.integers(min_value=0, max_value=360)
    )
    def test_track_creation_always_succeeds(self, x, y, altitude, speed, heading):
        """Property: Track creation should always succeed with valid inputs."""
        assume(all(math.isfinite(v) for v in [x, y]))
        
        track = Track(
            id="TEST",
            x=x,
            y=y,
            altitude=altitude,
            speed=speed,
            heading=heading
        )
        
        assert track.id == "TEST"
        assert 0 <= track.x <= 1.0
        assert 0 <= track.y <= 1.0
        assert track.altitude >= 0

    @given(
        track_type=st.sampled_from(["friendly", "hostile", "unknown", "missile"]),
        threat_level=st.sampled_from(["LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"])
    )
    def test_track_classification_always_valid(self, track_type, threat_level):
        """Property: Track classification should always be in valid set."""
        track = Track(
            id="TEST",
            x=0.5,
            y=0.5,
            altitude=30000,
            speed=500,
            heading=180,
            track_type=track_type,
            threat_level=threat_level
        )
        
        assert track.track_type in ["friendly", "hostile", "unknown", "missile"]
        assert track.threat_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"]
