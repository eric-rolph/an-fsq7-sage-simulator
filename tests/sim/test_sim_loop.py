"""
Unit tests for simulation loop coordinator.

Tests the Simulator class that coordinates all simulation subsystems.
"""

import pytest
from an_fsq7_simulator.sim import sim_loop, models


@pytest.mark.sim
class TestSimulatorInitialization:
    """Test Simulator initialization and state management."""

    def test_simulator_initializes_with_subsystems(self):
        """Verify Simulator creates all required subsystems."""
        sim = sim_loop.Simulator()
        
        assert sim.tubes is not None
        assert sim.mission_clock is not None
        assert sim.radar_targets == []
        assert sim.powered_on == False
        assert sim.system_ready == False
        assert sim.warming_up == False

    def test_simulator_accepts_cpu_core(self):
        """Verify Simulator can accept CPU core reference."""
        mock_cpu = object()
        sim = sim_loop.Simulator(cpu_core=mock_cpu)
        
        assert sim.cpu_core is mock_cpu

    def test_simulator_initializes_statistics(self):
        """Verify statistics counters initialize to zero."""
        sim = sim_loop.Simulator()
        
        assert sim.tracked_objects_count == 0
        assert sim.high_threat_count == 0
        assert sim.intercept_courses_count == 0
        assert sim.alerts_count == 0
        assert sim.successful_intercepts_count == 0
        assert sim.memory_cycles == 0


@pytest.mark.sim
class TestPowerControl:
    """Test system power control."""

    def test_power_on_sequence(self):
        """Verify power-on initiates warm-up sequence."""
        sim = sim_loop.Simulator()
        
        sim.power_on()
        
        assert sim.powered_on == True
        assert sim.warming_up == True
        assert sim.system_ready == False

    def test_power_off_resets_state(self):
        """Verify power-off resets all state."""
        sim = sim_loop.Simulator()
        
        sim.power_on()
        sim.power_off()
        
        assert sim.powered_on == False
        assert sim.system_ready == False
        assert sim.warming_up == False

    def test_tick_does_nothing_when_powered_off(self):
        """Verify tick() is no-op when system is off."""
        sim = sim_loop.Simulator()
        
        # Don't power on
        sim.tick(1.0)
        
        # Mission clock should not advance
        assert sim.mission_clock.seconds == 0


@pytest.mark.sim
class TestSimulationTick:
    """Test simulation tick updates."""

    def test_tick_advances_mission_clock(self):
        """Verify tick advances mission clock."""
        sim = sim_loop.Simulator()
        sim.power_on()
        
        # Warm up system first
        for _ in range(100):
            sim.tick(0.1)
        
        initial_time = sim.mission_clock.seconds
        sim.tick(1.0)
        
        assert sim.mission_clock.seconds > initial_time

    def test_tick_updates_radar_targets(self):
        """Verify tick updates radar target positions."""
        sim = sim_loop.Simulator()
        sim.power_on()
        
        # Create a target with velocity
        target = models.RadarTarget(
            target_id="TEST-001",
            x=100.0,
            y=100.0,
            heading=0,   # North
            speed=600,   # 600 knots
            altitude=30000,
            target_type="AIRCRAFT",
            threat_level="HIGH"
        )
        sim.radar_targets.append(target)
        
        # Warm up system
        for _ in range(100):
            sim.tick(0.1)
        
        initial_y = target.y
        
        # Tick simulation
        sim.tick(1.0)
        
        # Target should have moved (position changes with movement)
        assert (target.x != 100.0) or (target.y != initial_y)

    def test_tick_updates_statistics(self):
        """Verify tick updates tracked object counts."""
        sim = sim_loop.Simulator()
        sim.power_on()
        
        # Add targets
        sim.radar_targets.append(models.RadarTarget(
            target_id="TEST-001",
            x=100, y=100, heading=0, speed=500, altitude=30000,
            target_type="AIRCRAFT", threat_level="HIGH"
        ))
        sim.radar_targets.append(models.RadarTarget(
            target_id="TEST-002",
            x=200, y=200, heading=0, speed=500, altitude=30000,
            target_type="AIRCRAFT", threat_level="LOW"
        ))
        
        # Warm up and tick
        for _ in range(100):
            sim.tick(0.1)
        
        sim.tick(1.0)
        
        assert sim.tracked_objects_count == 2
        assert sim.high_threat_count == 1

    def test_tick_increments_memory_cycles(self):
        """Verify tick increments memory cycle counter."""
        sim = sim_loop.Simulator()
        sim.power_on()
        
        # Warm up system
        for _ in range(100):
            sim.tick(0.1)
        
        initial_cycles = sim.memory_cycles
        sim.tick(0.05)
        
        assert sim.memory_cycles > initial_cycles


@pytest.mark.sim
class TestTargetManagement:
    """Test radar target management."""

    def test_spawn_radar_targets_creates_targets(self):
        """Verify spawn_radar_targets creates requested count."""
        sim = sim_loop.Simulator()
        
        sim.spawn_radar_targets(count=5)
        
        assert len(sim.radar_targets) == 5
        assert sim.tracked_objects_count == 5

    def test_spawn_radar_targets_assigns_unique_ids(self):
        """Verify spawned targets have unique IDs."""
        sim = sim_loop.Simulator()
        
        sim.spawn_radar_targets(count=10)
        
        target_ids = [t.target_id for t in sim.radar_targets]
        assert len(target_ids) == len(set(target_ids))  # All unique

    def test_spawn_radar_targets_assigns_threat_levels(self):
        """Verify spawned targets have threat levels."""
        sim = sim_loop.Simulator()
        
        sim.spawn_radar_targets(count=10)
        
        for target in sim.radar_targets:
            assert target.threat_level in ["LOW", "MEDIUM", "HIGH"]

    def test_spawn_radar_targets_clears_existing(self):
        """Verify spawn_radar_targets clears previous targets."""
        sim = sim_loop.Simulator()
        
        sim.spawn_radar_targets(count=5)
        sim.spawn_radar_targets(count=3)
        
        assert len(sim.radar_targets) == 3


@pytest.mark.sim
class TestTargetSelection:
    """Test target selection system."""

    def test_select_target_by_position(self):
        """Verify select_target finds nearest target."""
        sim = sim_loop.Simulator()
        
        target1 = models.RadarTarget(
            target_id="TEST-001",
            x=100, y=100, heading=0, speed=500, altitude=30000,
            target_type="AIRCRAFT", threat_level="HIGH"
        )
        target2 = models.RadarTarget(
            target_id="TEST-002",
            x=200, y=200, heading=0, speed=500, altitude=30000,
            target_type="AIRCRAFT", threat_level="LOW"
        )
        sim.radar_targets.extend([target1, target2])
        
        # Select near target1
        selected = sim.select_target(105, 105)
        
        assert selected is not None
        assert selected.target_id == "TEST-001"
        assert sim.selected_target_id == "TEST-001"

    def test_select_target_returns_none_when_too_far(self):
        """Verify select_target returns None if no target in range."""
        sim = sim_loop.Simulator()
        
        target = models.RadarTarget(
            target_id="TEST-001",
            x=100, y=100, heading=0, speed=500, altitude=30000,
            target_type="AIRCRAFT", threat_level="HIGH"
        )
        sim.radar_targets.append(target)
        
        # Select far away
        selected = sim.select_target(500, 500, max_distance=10.0)
        
        assert selected is None
        assert sim.selected_target_id is None

    def test_get_selected_target_returns_target_object(self):
        """Verify get_selected_target returns selected target."""
        sim = sim_loop.Simulator()
        
        target = models.RadarTarget(
            target_id="TEST-001",
            x=100, y=100, heading=0, speed=500, altitude=30000,
            target_type="AIRCRAFT", threat_level="HIGH"
        )
        sim.radar_targets.append(target)
        
        sim.select_target(100, 100)
        selected = sim.get_selected_target()
        
        assert selected is not None
        assert selected.target_id == "TEST-001"

    def test_get_selected_target_returns_none_when_no_selection(self):
        """Verify get_selected_target returns None with no selection."""
        sim = sim_loop.Simulator()
        
        selected = sim.get_selected_target()
        
        assert selected is None


@pytest.mark.sim
class TestInterceptAssignment:
    """Test intercept assignment."""

    def test_assign_intercept_increments_counters(self):
        """Verify assign_intercept updates counters."""
        sim = sim_loop.Simulator()
        
        # Select a target first
        sim.selected_target_id = "TEST-001"
        
        initial_intercepts = sim.intercept_courses_count
        initial_alerts = sim.alerts_count
        
        sim.assign_intercept()
        
        assert sim.intercept_courses_count == initial_intercepts + 1
        assert sim.alerts_count == initial_alerts + 1

    def test_assign_intercept_requires_selection(self):
        """Verify assign_intercept checks for selected target."""
        sim = sim_loop.Simulator()
        
        # No target selected
        sim.selected_target_id = None
        
        sim.assign_intercept()
        
        # Should not increment counters
        assert sim.intercept_courses_count == 0


@pytest.mark.sim
class TestDataConversion:
    """Test data format conversion for UI compatibility."""

    def test_get_radar_targets_as_dicts(self):
        """Verify radar targets can be converted to dict format."""
        sim = sim_loop.Simulator()
        
        target = models.RadarTarget(
            target_id="TEST-001",
            x=100, y=200, heading=45, speed=600, altitude=35000,
            target_type="AIRCRAFT", threat_level="HIGH"
        )
        sim.radar_targets.append(target)
        
        dicts = sim.get_radar_targets_as_dicts()
        
        assert len(dicts) == 1
        assert dicts[0]["target_id"] == "TEST-001"
        assert dicts[0]["x"] == 100
        assert dicts[0]["y"] == 200
        assert dicts[0]["heading"] == 45
        assert dicts[0]["speed"] == 600
        assert dicts[0]["altitude"] == 35000
        assert dicts[0]["target_type"] == "AIRCRAFT"
        assert dicts[0]["threat_level"] == "HIGH"
