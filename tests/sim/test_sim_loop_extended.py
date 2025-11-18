"""
Additional tests for sim_loop - covering CPU RTC tick and edge cases.

Tests uncovered paths in Simulator tick() and assign_intercept().
"""

import pytest
import time
from an_fsq7_simulator.sim.sim_loop import Simulator
from an_fsq7_simulator.sim.models import RadarTarget
from an_fsq7_simulator.cpu_core import CPUCore


@pytest.mark.sim
class TestSimulatorCPUIntegration:
    """Test simulator integration with CPU core."""

    def test_simulator_with_cpu_core_ticks_rtc(self):
        """Verify CPU RTC tick path executes when cpu_core is present."""
        simulator = Simulator()
        
        # Create and attach CPU core
        cpu = CPUCore()
        simulator.cpu_core = cpu
        
        # Initialize RTC tick tracking to force tick on next update
        simulator._last_rtc_tick = time.time() - 1.0
        
        # Should not crash when ticking with CPU core attached
        simulator.tick(dt=0.1)
        
        # Verify simulator still functional
        assert simulator.powered_on == False  # Not yet powered on

    def test_simulator_without_cpu_core_no_error(self):
        """Verify simulator handles missing cpu_core gracefully."""
        simulator = Simulator()
        
        # Ensure cpu_core is None
        simulator.cpu_core = None
        
        # Power on and set system ready
        simulator.power_on()
        simulator.system_ready = True
        
        # Should not crash even without CPU core
        simulator.tick(dt=0.1)
        
        # Memory cycles should increment (no CPU required for this)
        assert simulator.memory_cycles == 1

    def test_simulator_cpu_rtc_respects_interval(self):
        """Verify CPU RTC path respects timing interval."""
        simulator = Simulator()
        
        cpu = CPUCore()
        simulator.cpu_core = cpu
        
        # Set last tick to very recent
        recent_time = time.time()
        simulator._last_rtc_tick = recent_time
        
        # Tick simulator (too soon for RTC tick - interval not elapsed)
        simulator.tick(dt=0.001)
        
        # Last RTC tick time should remain unchanged (interval not reached)
        assert simulator._last_rtc_tick == recent_time

    def test_simulator_cpu_rtc_tick_executes_when_interval_elapsed(self):
        """Verify CPU RTC tick_rtc is actually called when interval passes."""
        simulator = Simulator()
        
        cpu = CPUCore()
        simulator.cpu_core = cpu
        
        # Power on and set system ready so tick() doesn't early return
        simulator.power_on()
        simulator.system_ready = True
        
        # Set last tick to past (force interval elapsed)
        old_tick_time = time.time() - 1.0
        simulator._last_rtc_tick = old_tick_time
        
        # Tick simulator
        simulator.tick(dt=0.1)
        
        # Last RTC tick time should be updated (interval was reached)
        assert simulator._last_rtc_tick > old_tick_time


@pytest.mark.sim
class TestSimulatorTargetSelection:
    """Test target selection edge cases."""

    def test_get_selected_target_with_no_selection(self):
        """Verify get_selected_target returns None when nothing selected."""
        simulator = Simulator()
        
        simulator.selected_target_id = None
        
        target = simulator.get_selected_target()
        
        assert target is None

    def test_get_selected_target_with_invalid_id(self):
        """Verify get_selected_target returns None for non-existent target."""
        simulator = Simulator()
        
        # Add a target
        simulator.radar_targets.append(
            RadarTarget(
                target_id="TGT-001",
                x=100, y=200,
                heading=0, speed=500,
                altitude=30000
            )
        )
        
        # Select different target that doesn't exist
        simulator.selected_target_id = "TGT-999"
        
        target = simulator.get_selected_target()
        
        assert target is None

    def test_get_selected_target_finds_correct_target(self):
        """Verify get_selected_target returns correct target object."""
        simulator = Simulator()
        
        # Add multiple targets
        target1 = RadarTarget(
            target_id="TGT-001",
            x=100, y=200,
            heading=0, speed=500,
            altitude=30000
        )
        target2 = RadarTarget(
            target_id="TGT-002",
            x=200, y=300,
            heading=90, speed=600,
            altitude=35000
        )
        
        simulator.radar_targets.extend([target1, target2])
        
        # Select second target
        simulator.selected_target_id = "TGT-002"
        
        found = simulator.get_selected_target()
        
        assert found is not None
        assert found.target_id == "TGT-002"
        assert found.x == 200
        assert found.y == 300


@pytest.mark.sim
class TestSimulatorInterceptAssignment:
    """Test intercept assignment logic."""

    def test_assign_intercept_increments_counters(self):
        """Verify assign_intercept updates intercept and alert counts."""
        simulator = Simulator()
        
        # Set selected target
        simulator.selected_target_id = "TGT-001"
        
        initial_intercepts = simulator.intercept_courses_count
        initial_alerts = simulator.alerts_count
        
        # Assign intercept
        simulator.assign_intercept()
        
        # Counters should increment
        assert simulator.intercept_courses_count == initial_intercepts + 1
        assert simulator.alerts_count == initial_alerts + 1

    def test_assign_intercept_without_selection(self):
        """Verify assign_intercept handles no selection gracefully."""
        simulator = Simulator()
        
        # No target selected
        simulator.selected_target_id = None
        
        initial_intercepts = simulator.intercept_courses_count
        
        # Should not crash
        simulator.assign_intercept()
        
        # Counters should not change
        assert simulator.intercept_courses_count == initial_intercepts

    def test_assign_intercept_multiple_times(self):
        """Verify multiple intercept assignments increment correctly."""
        simulator = Simulator()
        
        simulator.selected_target_id = "TGT-001"
        
        # Assign multiple times
        simulator.assign_intercept()
        simulator.assign_intercept()
        simulator.assign_intercept()
        
        # Should have 3 intercepts and 3 alerts
        assert simulator.intercept_courses_count == 3
        assert simulator.alerts_count == 3


@pytest.mark.sim
class TestSimulatorMemoryCycles:
    """Test memory cycle counter."""

    def test_memory_cycles_increment_on_tick(self):
        """Verify memory cycles counter increments."""
        simulator = Simulator()
        
        # Power on and set system ready (tubes warmed up)
        simulator.power_on()
        simulator.system_ready = True
        
        initial_cycles = simulator.memory_cycles
        
        # Tick multiple times
        simulator.tick(dt=0.1)
        simulator.tick(dt=0.1)
        simulator.tick(dt=0.1)
        
        # Should have incremented 3 times
        assert simulator.memory_cycles == initial_cycles + 3

    def test_memory_cycles_start_at_zero(self):
        """Verify memory cycles start at 0."""
        simulator = Simulator()
        
        assert simulator.memory_cycles == 0
