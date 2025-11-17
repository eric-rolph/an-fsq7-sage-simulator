"""
Simulation tests for SAGE scenarios.

Tests scenario loading, initialization, and execution.
"""

import pytest
from an_fsq7_simulator.sim import scenarios


@pytest.mark.sim
class TestScenarios:
    """Test SAGE scenario system."""

    def test_get_demo1_scenario(self):
        """Verify Demo 1 scenario loads correctly."""
        scenario = scenarios.get_scenario("Demo 1 - Three Inbound")
        assert scenario is not None
        assert scenario.name == "Demo 1 - Three Inbound"
        assert scenario.difficulty == "beginner"

    def test_get_demo2_scenario(self):
        """Verify Demo 2 scenario loads correctly."""
        scenario = scenarios.get_scenario("Demo 2 - Mixed Friendly/Unknown")
        assert scenario is not None
        assert scenario.name == "Demo 2 - Mixed Friendly/Unknown"
        assert scenario.difficulty == "beginner"

    def test_get_demo3_scenario(self):
        """Verify Demo 3 scenario loads correctly."""
        scenario = scenarios.get_scenario("Demo 3 - High Threat Saturation")
        assert scenario is not None
        assert scenario.name == "Demo 3 - High Threat Saturation"
        # Demo 3 doesn't specify difficulty, uses default "beginner"
        assert scenario.difficulty == "beginner"

    def test_scenario_has_targets(self):
        """Verify scenarios initialize with targets."""
        scenario = scenarios.get_scenario("Demo 1 - Three Inbound")
        assert hasattr(scenario, "targets")
        assert len(scenario.targets) > 0

    def test_scenario_has_learning_objectives(self):
        """Verify scenarios have learning objectives."""
        scenario = scenarios.get_scenario("Demo 1 - Three Inbound")
        assert hasattr(scenario, "learning_objectives")
        assert len(scenario.learning_objectives) > 0

    def test_scenario_has_objectives(self):
        """Verify scenarios have objectives."""
        scenario = scenarios.get_scenario("Demo 1 - Three Inbound")
        assert hasattr(scenario, "objectives")
        assert len(scenario.objectives) > 0

    def test_scenario_difficulty_levels(self):
        """Verify different difficulty levels exist."""
        demo1 = scenarios.get_scenario("Demo 1 - Three Inbound")
        demo3 = scenarios.get_scenario("Demo 3 - High Threat Saturation")
        scenario5 = scenarios.get_scenario("Scenario 5 - Correlation Training")
        
        difficulties = [demo1.difficulty, demo3.difficulty, scenario5.difficulty]
        assert "beginner" in difficulties
        assert "intermediate" in difficulties

    def test_scenario_has_description(self):
        """Verify scenarios have descriptions."""
        scenario = scenarios.get_scenario("Demo 1 - Three Inbound")
        assert hasattr(scenario, "description")
        assert len(scenario.description) > 0

    def test_invalid_scenario_name(self):
        """Verify handling of invalid scenario name."""
        scenario = scenarios.get_scenario("nonexistent_scenario")
        assert scenario is None

    def test_all_scenarios_loadable(self):
        """Verify all scenarios can be loaded."""
        all_scenarios = scenarios.list_scenarios()
        assert len(all_scenarios) > 0
        
        for name in all_scenarios:
            scenario = scenarios.get_scenario(name)
            assert scenario is not None
            assert scenario.name == name
            assert hasattr(scenario, "targets")
            assert hasattr(scenario, "objectives")
