"""
Unit tests for scenario event system.

Tests dynamic event triggering and event factory functions.
"""

import pytest
from an_fsq7_simulator.sim import scenario_events


@pytest.mark.sim
class TestEventType:
    """Test EventType enum."""

    def test_event_types_exist(self):
        """Verify all event types are defined."""
        assert scenario_events.EventType.SPAWN_TRACK is not None
        assert scenario_events.EventType.COURSE_CHANGE is not None
        assert scenario_events.EventType.THREAT_ESCALATION is not None
        assert scenario_events.EventType.EQUIPMENT_FAILURE is not None
        assert scenario_events.EventType.SYSTEM_MESSAGE is not None
        assert scenario_events.EventType.INTERCEPTOR_READY is not None
        assert scenario_events.EventType.REMOVE_TRACK is not None
        assert scenario_events.EventType.WAVE_SPAWN is not None


@pytest.mark.sim
class TestScenarioEvent:
    """Test ScenarioEvent dataclass."""

    def test_event_initialization(self):
        """Verify ScenarioEvent can be created."""
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={"track_id": "TEST-001"}
        )
        
        assert event.event_type == scenario_events.EventType.SPAWN_TRACK
        assert event.trigger_time == 30.0
        assert event.data["track_id"] == "TEST-001"
        assert event.triggered == False
        assert event.repeating == False

    def test_should_trigger_before_time(self):
        """Verify event does not trigger before trigger_time."""
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={}
        )
        
        # Check at 20 seconds (before trigger)
        assert event.should_trigger(20.0, None) == False

    def test_should_trigger_at_time(self):
        """Verify event triggers at trigger_time."""
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={}
        )
        
        # Check at 30 seconds (at trigger)
        assert event.should_trigger(30.0, None) == True

    def test_should_trigger_after_time(self):
        """Verify event triggers after trigger_time."""
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={}
        )
        
        # Check at 40 seconds (after trigger)
        assert event.should_trigger(40.0, None) == True

    def test_should_not_trigger_twice_if_not_repeating(self):
        """Verify one-time events only trigger once."""
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={}
        )
        
        # Trigger once
        event.mark_triggered()
        
        # Should not trigger again
        assert event.should_trigger(40.0, None) == False

    def test_repeating_event_triggers_multiple_times(self):
        """Verify repeating events can trigger multiple times."""
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={},
            repeating=True,
            repeat_interval=15.0
        )
        
        # First trigger at 30s
        assert event.should_trigger(30.0, None) == True
        event.mark_triggered()
        
        # Should not trigger at 40s (next is 45s)
        assert event.should_trigger(40.0, None) == False
        
        # Should trigger at 45s
        assert event.should_trigger(45.0, None) == True

    def test_conditional_event_checks_condition(self):
        """Verify conditional events check condition function."""
        # Create event with condition
        event = scenario_events.ScenarioEvent(
            event_type=scenario_events.EventType.SPAWN_TRACK,
            trigger_time=30.0,
            data={},
            condition=lambda state: state["ready"] == True
        )
        
        # Condition not met
        assert event.should_trigger(30.0, {"ready": False}) == False
        
        # Condition met
        assert event.should_trigger(30.0, {"ready": True}) == True


@pytest.mark.sim
class TestSpawnEvent:
    """Test spawn event creation."""

    def test_create_spawn_event(self):
        """Verify create_spawn_event creates correct event."""
        event = scenario_events.create_spawn_event(
            trigger_time=45.0,
            track_id="TRK-001",
            x=0.5,
            y=0.3,
            heading=180,
            speed=600,
            altitude=35000,
            track_type="HOSTILE",
            threat_level="HIGH",
            message="New hostile detected"
        )
        
        assert event.event_type == scenario_events.EventType.SPAWN_TRACK
        assert event.trigger_time == 45.0
        assert event.data["track_id"] == "TRK-001"
        assert event.data["x"] == 0.5
        assert event.data["y"] == 0.3
        assert event.data["heading"] == 180
        assert event.data["speed"] == 600
        assert event.data["altitude"] == 35000
        assert event.data["track_type"] == "HOSTILE"
        assert event.data["threat_level"] == "HIGH"
        assert event.data["message"] == "New hostile detected"


@pytest.mark.sim
class TestCourseChangeEvent:
    """Test course change event creation."""

    def test_create_course_change_event_heading(self):
        """Verify course change with new heading."""
        event = scenario_events.create_course_change_event(
            trigger_time=60.0,
            track_id="TRK-001",
            new_heading=270,
            message="Track turning west"
        )
        
        assert event.event_type == scenario_events.EventType.COURSE_CHANGE
        assert event.trigger_time == 60.0
        assert event.data["track_id"] == "TRK-001"
        assert event.data["new_heading"] == 270
        assert event.data["message"] == "Track turning west"

    def test_create_course_change_event_speed(self):
        """Verify course change with new speed."""
        event = scenario_events.create_course_change_event(
            trigger_time=90.0,
            track_id="TRK-002",
            new_speed=800,
            message="Track accelerating"
        )
        
        assert event.event_type == scenario_events.EventType.COURSE_CHANGE
        assert event.data["track_id"] == "TRK-002"
        assert event.data["new_speed"] == 800
        assert event.data["message"] == "Track accelerating"


@pytest.mark.sim
class TestTubeFailureEvent:
    """Test tube failure event creation."""

    def test_create_tube_failure_event(self):
        """Verify tube failure event creation."""
        event = scenario_events.create_tube_failure_event(
            trigger_time=120.0,
            tube_ids=["TUBE-001", "TUBE-002"],
            count=2,
            message="Vacuum tubes degrading"
        )
        
        assert event.event_type == scenario_events.EventType.EQUIPMENT_FAILURE
        assert event.trigger_time == 120.0
        assert event.data["tube_ids"] == ["TUBE-001", "TUBE-002"]
        assert event.data["count"] == 2
        assert event.data["message"] == "Vacuum tubes degrading"

    def test_create_tube_failure_event_random(self):
        """Verify tube failure with random selection."""
        event = scenario_events.create_tube_failure_event(
            trigger_time=120.0,
            count=3
        )
        
        assert event.data["tube_ids"] is None  # Random selection
        assert event.data["count"] == 3


@pytest.mark.sim
class TestSystemMessageEvent:
    """Test system message event creation."""

    def test_create_system_message_event(self):
        """Verify system message event creation."""
        event = scenario_events.create_system_message_event(
            trigger_time=15.0,
            message="NORAD tracking 12 contacts",
            category="INTELLIGENCE",
            details="Multiple bogeys entering sector 7"
        )
        
        assert event.event_type == scenario_events.EventType.SYSTEM_MESSAGE
        assert event.trigger_time == 15.0
        assert event.data["message"] == "NORAD tracking 12 contacts"
        assert event.data["category"] == "INTELLIGENCE"
        assert event.data["details"] == "Multiple bogeys entering sector 7"


@pytest.mark.sim
class TestThreatEscalationEvent:
    """Test threat escalation event creation."""

    def test_create_threat_escalation_event(self):
        """Verify threat escalation event creation."""
        event = scenario_events.create_threat_escalation_event(
            trigger_time=75.0,
            track_id="TRK-003",
            new_threat_level="CRITICAL",
            message="Threat level upgraded to CRITICAL"
        )
        
        assert event.event_type == scenario_events.EventType.THREAT_ESCALATION
        assert event.trigger_time == 75.0
        assert event.data["track_id"] == "TRK-003"
        assert event.data["new_threat_level"] == "CRITICAL"
        assert event.data["message"] == "Threat level upgraded to CRITICAL"


@pytest.mark.sim
class TestWaveSpawnEvent:
    """Test wave spawn event creation."""

    def test_create_wave_spawn_event(self):
        """Verify wave spawn event creation."""
        tracks = [
            {"track_id": "TRK-101", "x": 0.1, "y": 0.2, "heading": 90},
            {"track_id": "TRK-102", "x": 0.2, "y": 0.3, "heading": 90},
            {"track_id": "TRK-103", "x": 0.3, "y": 0.4, "heading": 90}
        ]
        
        event = scenario_events.create_wave_spawn_event(
            trigger_time=180.0,
            wave_name="Formation Alpha",
            tracks=tracks,
            message="Formation Alpha entering sector"
        )
        
        assert event.event_type == scenario_events.EventType.WAVE_SPAWN
        assert event.trigger_time == 180.0
        assert event.data["wave_name"] == "Formation Alpha"
        assert len(event.data["tracks"]) == 3
        assert event.data["tracks"][0]["track_id"] == "TRK-101"
        assert event.data["message"] == "Formation Alpha entering sector"
