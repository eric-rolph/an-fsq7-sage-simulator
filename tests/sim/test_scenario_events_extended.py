"""
Additional tests for scenario events - factory functions and event timeline.

Covers remaining uncovered factory functions and EventTimeline class.
"""

import pytest
from an_fsq7_simulator.sim.scenario_events import (
    EventType,
    ScenarioEvent,
    EventTimeline,
    create_spawn_event,
    create_course_change_event,
    create_tube_failure_event,
    create_system_message_event,
    create_threat_escalation_event,
    create_wave_spawn_event,
    get_events_for_scenario
)


@pytest.mark.sim
class TestFactoryFunctions:
    """Test event factory functions."""

    def test_create_spawn_event(self):
        """Verify create_spawn_event factory."""
        event = create_spawn_event(
            trigger_time=10.0,
            track_id="TGT-001",
            x=0.5, y=0.5,
            heading=45, speed=500,
            altitude=30000,
            track_type="HOSTILE",
            threat_level="HIGH",
            message="New hostile detected"
        )
        
        assert event.event_type == EventType.SPAWN_TRACK
        assert event.trigger_time == 10.0
        assert event.data["track_id"] == "TGT-001"
        assert event.data["message"] == "New hostile detected"

    def test_create_course_change_event(self):
        """Verify create_course_change_event factory."""
        event = create_course_change_event(
            trigger_time=20.0,
            track_id="TGT-002",
            new_heading=90,
            new_speed=600,
            message="Target changed course"
        )
        
        assert event.event_type == EventType.COURSE_CHANGE
        assert event.trigger_time == 20.0
        assert event.data["track_id"] == "TGT-002"
        assert event.data["new_heading"] == 90
        assert event.data["new_speed"] == 600

    def test_create_tube_failure_event(self):
        """Verify create_tube_failure_event factory."""
        event = create_tube_failure_event(
            trigger_time=30.0,
            tube_ids=["TUBE-42"],
            count=1,
            message="Tube failure detected"
        )
        
        assert event.event_type == EventType.EQUIPMENT_FAILURE
        assert event.trigger_time == 30.0
        assert event.data["tube_ids"] == ["TUBE-42"]
        assert event.data["count"] == 1

    def test_create_system_message_event(self):
        """Verify create_system_message_event factory."""
        event = create_system_message_event(
            trigger_time=40.0,
            message="System alert",
            category="WARNING",
            details="Test details"
        )
        
        assert event.event_type == EventType.SYSTEM_MESSAGE
        assert event.trigger_time == 40.0
        assert event.data["message"] == "System alert"
        assert event.data["category"] == "WARNING"
        assert event.data["details"] == "Test details"

    def test_create_threat_escalation_event(self):
        """Verify create_threat_escalation_event factory."""
        event = create_threat_escalation_event(
            trigger_time=50.0,
            track_id="TGT-003",
            new_threat_level="CRITICAL",
            message="Threat escalated"
        )
        
        assert event.event_type == EventType.THREAT_ESCALATION
        assert event.trigger_time == 50.0
        assert event.data["track_id"] == "TGT-003"
        assert event.data["new_threat_level"] == "CRITICAL"
        assert event.data["message"] == "Threat escalated"

    def test_create_wave_spawn_event(self):
        """Verify create_wave_spawn_event factory."""
        tracks = [
            {"track_id": "TGT-010", "x": 0.2, "y": 0.3},
            {"track_id": "TGT-011", "x": 0.3, "y": 0.4},
        ]
        
        event = create_wave_spawn_event(
            trigger_time=60.0,
            wave_name="Alpha Wave",
            tracks=tracks,
            message="Wave incoming"
        )
        
        assert event.event_type == EventType.WAVE_SPAWN
        assert event.trigger_time == 60.0
        assert event.data["wave_name"] == "Alpha Wave"
        assert len(event.data["tracks"]) == 2
        assert event.data["message"] == "Wave incoming"

    def test_factory_functions_without_optional_message(self):
        """Verify factory functions handle missing optional message."""
        event1 = create_spawn_event(
            trigger_time=5.0,
            track_id="TGT-999",
            x=0.5, y=0.5,
            heading=0, speed=500,
            altitude=30000,
            track_type="UNKNOWN",
            threat_level="LOW"
        )
        assert event1.data["message"] is None
        
        event2 = create_course_change_event(
            trigger_time=5.0,
            track_id="TGT-999",
            new_heading=90,
            new_speed=600
        )
        assert event2.data["message"] is None
        
        event3 = create_threat_escalation_event(
            trigger_time=5.0,
            track_id="TGT-999",
            new_threat_level="HIGH"
        )
        assert event3.data["message"] is None
        
        event4 = create_wave_spawn_event(
            trigger_time=5.0,
            wave_name="Test Wave",
            tracks=[]
        )
        assert event4.data["message"] is None


@pytest.mark.sim
class TestEventTimeline:
    """Test EventTimeline coordinator."""

    def test_event_timeline_initialization(self):
        """Verify EventTimeline initializes correctly."""
        events = [
            ScenarioEvent(EventType.SPAWN_TRACK, trigger_time=10.0, data={}),
            ScenarioEvent(EventType.SYSTEM_MESSAGE, trigger_time=20.0, data={}),
        ]
        
        timeline = EventTimeline(events)
        
        assert len(timeline.events) == 2
        assert timeline.scenario_start_time == 0.0
        assert timeline.last_check_time == 0.0

    def test_event_timeline_reset(self):
        """Verify reset restarts timeline."""
        events = [
            ScenarioEvent(EventType.SPAWN_TRACK, trigger_time=10.0, data={}),
        ]
        events[0].triggered = True
        
        timeline = EventTimeline(events)
        timeline.reset(start_time=5000.0)
        
        assert timeline.scenario_start_time == 5000.0
        assert timeline.last_check_time == 5000.0
        assert events[0].triggered == False

    def test_event_timeline_get_elapsed_time(self):
        """Verify elapsed time calculation."""
        timeline = EventTimeline([])
        timeline.reset(start_time=1000.0)
        
        elapsed = timeline.get_elapsed_time(current_world_time=3500.0)
        
        # (3500 - 1000) / 1000 = 2.5 seconds
        assert elapsed == 2.5

    def test_event_timeline_check_and_trigger(self):
        """Verify check_and_trigger returns triggered events."""
        event1 = ScenarioEvent(EventType.SPAWN_TRACK, trigger_time=5.0, data={})
        event2 = ScenarioEvent(EventType.SYSTEM_MESSAGE, trigger_time=10.0, data={})
        
        timeline = EventTimeline([event1, event2])
        timeline.reset(start_time=0.0)
        
        # Check at 6 seconds (only event1 should trigger)
        triggered = timeline.check_and_trigger(current_world_time=6000.0, state=None)
        
        assert len(triggered) == 1
        assert triggered[0] == event1
        assert event1.triggered == True
        assert event2.triggered == False

    def test_event_timeline_multiple_triggers(self):
        """Verify multiple events can trigger in one check."""
        event1 = ScenarioEvent(EventType.SPAWN_TRACK, trigger_time=5.0, data={})
        event2 = ScenarioEvent(EventType.SYSTEM_MESSAGE, trigger_time=6.0, data={})
        
        timeline = EventTimeline([event1, event2])
        timeline.reset(start_time=0.0)
        
        # Check at 10 seconds (both should trigger)
        triggered = timeline.check_and_trigger(current_world_time=10000.0, state=None)
        
        assert len(triggered) == 2

    def test_event_timeline_no_triggers(self):
        """Verify check_and_trigger returns empty list when no events ready."""
        event1 = ScenarioEvent(EventType.SPAWN_TRACK, trigger_time=20.0, data={})
        
        timeline = EventTimeline([event1])
        timeline.reset(start_time=0.0)
        
        # Check at 5 seconds (too early)
        triggered = timeline.check_and_trigger(current_world_time=5000.0, state=None)
        
        assert len(triggered) == 0

    def test_event_timeline_updates_last_check_time(self):
        """Verify last_check_time is updated."""
        timeline = EventTimeline([])
        timeline.reset(start_time=0.0)
        
        timeline.check_and_trigger(current_world_time=7500.0, state=None)
        
        assert timeline.last_check_time == 7500.0


@pytest.mark.sim
class TestScenarioEventMapping:
    """Test scenario event mapping."""

    def test_get_events_for_scenario_demo1(self):
        """Verify Demo 1 scenario has events."""
        events = get_events_for_scenario("Demo 1 - Three Inbound")
        
        assert len(events) > 0

    def test_get_events_for_scenario_demo2(self):
        """Verify Demo 2 scenario has events."""
        events = get_events_for_scenario("Demo 2 - Mixed Friendly/Unknown")
        
        assert len(events) > 0

    def test_get_events_for_scenario_demo3(self):
        """Verify Demo 3 scenario has events."""
        events = get_events_for_scenario("Demo 3 - High Threat Saturation")
        
        assert len(events) > 0

    def test_get_events_for_scenario_demo4(self):
        """Verify Demo 4 scenario has no events (observation only)."""
        events = get_events_for_scenario("Demo 4 - Patrol Route")
        
        assert len(events) == 0

    def test_get_events_for_scenario_5(self):
        """Verify Scenario 5 has events."""
        events = get_events_for_scenario("Scenario 5 - Correlation Training")
        
        assert len(events) > 0

    def test_get_events_for_scenario_6(self):
        """Verify Scenario 6 has events."""
        events = get_events_for_scenario("Scenario 6 - Equipment Degradation")
        
        assert len(events) > 0

    def test_get_events_for_scenario_7(self):
        """Verify Scenario 7 has events."""
        events = get_events_for_scenario("Scenario 7 - Saturated Defense")
        
        assert len(events) > 0

    def test_get_events_for_unknown_scenario(self):
        """Verify unknown scenario returns empty list."""
        events = get_events_for_scenario("Unknown Scenario")
        
        assert len(events) == 0
