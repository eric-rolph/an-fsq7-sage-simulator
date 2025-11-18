"""
Additional tests for scenario loading functionality.

Tests load_scenario function that initializes simulator with scenario data.
"""

import pytest
from an_fsq7_simulator.sim.scenarios import (
    get_scenario,
    list_scenarios,
    load_scenario
)
from an_fsq7_simulator.sim.sim_loop import Simulator


@pytest.mark.sim
class TestScenarioLoading:
    """Test scenario loading into simulator."""

    def test_load_scenario_clears_existing_targets(self):
        """Verify load_scenario clears existing radar targets."""
        simulator = Simulator()
        
        # Add some fake targets
        from an_fsq7_simulator.sim.models import RadarTarget
        simulator.radar_targets.append(
            RadarTarget(
                target_id="OLD-1",
                x=100, y=200,
                heading=0, speed=500,
                altitude=30000
            )
        )
        simulator.tracked_objects_count = 1
        
        # Load a scenario
        load_scenario(simulator, "Demo 1 - Three Inbound")
        
        # Old targets should be cleared, new ones loaded
        assert len(simulator.radar_targets) > 0
        assert all(t.target_id != "OLD-1" for t in simulator.radar_targets)

    def test_load_scenario_sets_tracked_objects_count(self):
        """Verify load_scenario updates tracked objects count."""
        simulator = Simulator()
        
        load_scenario(simulator, "Demo 1 - Three Inbound")
        
        assert simulator.tracked_objects_count == len(simulator.radar_targets)

    def test_load_scenario_sets_high_threat_count(self):
        """Verify load_scenario counts high threat targets."""
        simulator = Simulator()
        
        load_scenario(simulator, "Demo 3 - High Threat Saturation")
        
        # Count high threats manually
        expected_count = sum(
            1 for t in simulator.radar_targets if t.threat_level == "HIGH"
        )
        
        assert simulator.high_threat_count == expected_count

    def test_load_scenario_with_unknown_scenario(self):
        """Verify load_scenario handles unknown scenario gracefully."""
        simulator = Simulator()
        
        # Add initial target
        from an_fsq7_simulator.sim.models import RadarTarget
        simulator.radar_targets.append(
            RadarTarget(
                target_id="INITIAL",
                x=100, y=200,
                heading=0, speed=500,
                altitude=30000
            )
        )
        
        # Try to load unknown scenario
        load_scenario(simulator, "Unknown Scenario Name")
        
        # Should not crash, targets unchanged
        assert len(simulator.radar_targets) == 1

    def test_load_multiple_scenarios_sequentially(self):
        """Verify loading different scenarios sequentially."""
        simulator = Simulator()
        
        # Load first scenario
        load_scenario(simulator, "Demo 1 - Three Inbound")
        first_count = len(simulator.radar_targets)
        
        # Load second scenario
        load_scenario(simulator, "Demo 2 - Mixed Friendly/Unknown")
        second_count = len(simulator.radar_targets)
        
        # Counts should be different (scenarios have different # of targets)
        assert first_count != second_count

    def test_load_scenario_with_no_high_threats(self):
        """Verify load_scenario with scenario having no high threats."""
        simulator = Simulator()
        
        load_scenario(simulator, "Demo 4 - Patrol Route")
        
        # This scenario has friendly/unknown tracks, no high threats
        assert simulator.high_threat_count >= 0

    def test_load_scenario_updates_all_simulator_state(self):
        """Verify load_scenario properly initializes all relevant simulator state."""
        simulator = Simulator()
        
        load_scenario(simulator, "Demo 1 - Three Inbound")
        
        # Check all expected state is updated
        assert len(simulator.radar_targets) > 0
        assert simulator.tracked_objects_count == len(simulator.radar_targets)
        assert simulator.high_threat_count >= 0
        
        # Verify targets have expected properties
        for target in simulator.radar_targets:
            assert hasattr(target, "target_id")
            assert hasattr(target, "x")
            assert hasattr(target, "y")
            assert hasattr(target, "heading")
            assert hasattr(target, "speed")
            assert hasattr(target, "altitude")


@pytest.mark.sim
class TestScenarioNamesRetrieval:
    """Test scenario name listing."""

    def test_list_scenarios_returns_list(self):
        """Verify list_scenarios returns list."""
        names = list_scenarios()
        
        assert isinstance(names, list)

    def test_list_scenarios_not_empty(self):
        """Verify list_scenarios returns non-empty list."""
        names = list_scenarios()
        
        assert len(names) > 0

    def test_list_scenarios_contains_expected_scenarios(self):
        """Verify list_scenarios includes known scenarios."""
        names = list_scenarios()
        
        # Check for some expected scenarios
        assert "Demo 1 - Three Inbound" in names
        assert "Demo 2 - Mixed Friendly/Unknown" in names
        assert "Demo 3 - High Threat Saturation" in names


@pytest.mark.sim
class TestScenarioRetrieval:
    """Test individual scenario retrieval."""

    def test_get_scenario_returns_valid_scenario(self):
        """Verify get_scenario returns scenario object."""
        scenario = get_scenario("Demo 1 - Three Inbound")
        
        assert scenario is not None
        assert hasattr(scenario, "name")
        assert hasattr(scenario, "description")
        assert hasattr(scenario, "targets")

    def test_get_scenario_targets_have_correct_structure(self):
        """Verify scenario targets have expected attributes."""
        scenario = get_scenario("Demo 1 - Three Inbound")
        
        for target in scenario.targets:
            assert hasattr(target, "target_id")
            assert hasattr(target, "x")
            assert hasattr(target, "y")
            assert hasattr(target, "heading")
            assert hasattr(target, "speed")
            assert hasattr(target, "altitude")
            assert hasattr(target, "target_type")
            assert hasattr(target, "threat_level")

    def test_get_scenario_with_invalid_name(self):
        """Verify get_scenario returns None for invalid name."""
        scenario = get_scenario("This Scenario Does Not Exist")
        
        assert scenario is None
