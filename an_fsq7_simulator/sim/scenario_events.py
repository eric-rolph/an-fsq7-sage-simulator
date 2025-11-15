"""
Scenario event system for dynamic mission scenarios.

Defines timed events that occur during scenarios to create realistic, dynamic
air defense situations. Events can:
- Spawn new tracks (reinforcements, new waves)
- Change track behavior (course changes, speed adjustments)
- Trigger equipment failures (tube degradation)
- Update threat levels (escalation)
- Provide narrative context (system messages)

Event Timeline System:
- Events are scheduled based on scenario_elapsed_time
- Multiple events can trigger simultaneously
- Events can be one-time or repeating
- Some events are conditional (e.g., "spawn wave 2 if wave 1 not intercepted")
"""

from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import math


class EventType(Enum):
    """Types of scenario events"""
    SPAWN_TRACK = "spawn_track"           # Spawn new radar target
    COURSE_CHANGE = "course_change"        # Target changes heading/speed
    THREAT_ESCALATION = "threat_escalation"  # Threat level increases
    EQUIPMENT_FAILURE = "equipment_failure"  # Tube failure
    SYSTEM_MESSAGE = "system_message"      # Display message to operator
    INTERCEPTOR_READY = "interceptor_ready"  # Interceptor becomes available
    REMOVE_TRACK = "remove_track"          # Track leaves scope or is destroyed
    WAVE_SPAWN = "wave_spawn"              # Spawn multiple tracks as wave


@dataclass
class ScenarioEvent:
    """
    A timed event within a scenario.
    
    Attributes:
        event_type: Type of event
        trigger_time: Time in seconds after scenario start when event triggers
        data: Event-specific data (track params, message text, etc.)
        condition: Optional condition function to check before triggering
        triggered: Whether event has already been triggered
        repeating: If True, event resets after triggering
        repeat_interval: Seconds between repeats (if repeating=True)
    """
    event_type: EventType
    trigger_time: float  # Seconds after scenario start
    data: Dict[str, Any]
    condition: Optional[Callable] = None
    triggered: bool = False
    repeating: bool = False
    repeat_interval: float = 0.0
    
    def should_trigger(self, elapsed_time: float, state: Any) -> bool:
        """Check if event should trigger now"""
        if self.triggered and not self.repeating:
            return False
        
        if elapsed_time < self.trigger_time:
            return False
        
        if self.condition and not self.condition(state):
            return False
        
        return True
    
    def mark_triggered(self):
        """Mark event as triggered, schedule next repeat if applicable"""
        self.triggered = True
        if self.repeating:
            self.trigger_time += self.repeat_interval


# ============================================================================
# EVENT FACTORY FUNCTIONS - Create common event patterns
# ============================================================================

def create_spawn_event(
    trigger_time: float,
    track_id: str,
    x: float,
    y: float,
    heading: float,
    speed: float,
    altitude: float,
    track_type: str = "AIRCRAFT",
    threat_level: str = "MEDIUM",
    message: Optional[str] = None
) -> ScenarioEvent:
    """Create a track spawn event"""
    return ScenarioEvent(
        event_type=EventType.SPAWN_TRACK,
        trigger_time=trigger_time,
        data={
            "track_id": track_id,
            "x": x,
            "y": y,
            "heading": heading,
            "speed": speed,
            "altitude": altitude,
            "track_type": track_type,
            "threat_level": threat_level,
            "message": message
        }
    )


def create_course_change_event(
    trigger_time: float,
    track_id: str,
    new_heading: Optional[float] = None,
    new_speed: Optional[float] = None,
    message: Optional[str] = None
) -> ScenarioEvent:
    """Create a course change event for existing track"""
    return ScenarioEvent(
        event_type=EventType.COURSE_CHANGE,
        trigger_time=trigger_time,
        data={
            "track_id": track_id,
            "new_heading": new_heading,
            "new_speed": new_speed,
            "message": message
        }
    )


def create_tube_failure_event(
    trigger_time: float,
    tube_ids: Optional[List[str]] = None,
    count: int = 1,
    message: Optional[str] = None
) -> ScenarioEvent:
    """Create equipment failure event"""
    return ScenarioEvent(
        event_type=EventType.EQUIPMENT_FAILURE,
        trigger_time=trigger_time,
        data={
            "tube_ids": tube_ids,  # Specific tubes, or None for random
            "count": count,
            "message": message
        }
    )


def create_system_message_event(
    trigger_time: float,
    message: str,
    category: str = "SCENARIO",
    details: Optional[str] = None
) -> ScenarioEvent:
    """Create system message event"""
    return ScenarioEvent(
        event_type=EventType.SYSTEM_MESSAGE,
        trigger_time=trigger_time,
        data={
            "message": message,
            "category": category,
            "details": details
        }
    )


def create_threat_escalation_event(
    trigger_time: float,
    track_id: str,
    new_threat_level: str,
    message: Optional[str] = None
) -> ScenarioEvent:
    """Create threat escalation event"""
    return ScenarioEvent(
        event_type=EventType.THREAT_ESCALATION,
        trigger_time=trigger_time,
        data={
            "track_id": track_id,
            "new_threat_level": new_threat_level,
            "message": message
        }
    )


def create_wave_spawn_event(
    trigger_time: float,
    wave_name: str,
    tracks: List[Dict[str, Any]],
    message: Optional[str] = None
) -> ScenarioEvent:
    """Create wave spawn event (multiple tracks at once)"""
    return ScenarioEvent(
        event_type=EventType.WAVE_SPAWN,
        trigger_time=trigger_time,
        data={
            "wave_name": wave_name,
            "tracks": tracks,
            "message": message
        }
    )


# ============================================================================
# EVENT TIMELINE MANAGER
# ============================================================================

class EventTimeline:
    """Manages event timeline for a scenario"""
    
    def __init__(self, events: List[ScenarioEvent]):
        self.events = events
        self.scenario_start_time = 0.0
        self.last_check_time = 0.0
    
    def reset(self, start_time: float):
        """Reset timeline to beginning"""
        self.scenario_start_time = start_time
        self.last_check_time = start_time
        for event in self.events:
            event.triggered = False
    
    def get_elapsed_time(self, current_world_time: float) -> float:
        """Get time elapsed since scenario start"""
        return (current_world_time - self.scenario_start_time) / 1000.0
    
    def check_and_trigger(self, current_world_time: float, state: Any) -> List[ScenarioEvent]:
        """
        Check for events that should trigger and return them.
        
        Args:
            current_world_time: Current simulation time in milliseconds
            state: Simulator state (for condition checking)
        
        Returns:
            List of events that triggered
        """
        elapsed = self.get_elapsed_time(current_world_time)
        triggered_events = []
        
        for event in self.events:
            if event.should_trigger(elapsed, state):
                triggered_events.append(event)
                event.mark_triggered()
        
        self.last_check_time = current_world_time
        return triggered_events


# ============================================================================
# SCENARIO-SPECIFIC EVENT DEFINITIONS
# ============================================================================

def get_scenario_1_events() -> List[ScenarioEvent]:
    """Demo 1 - Three Inbound: Simple introduction with message prompts"""
    return [
        create_system_message_event(
            5.0,
            "THREE INBOUND CONTACTS DETECTED",
            category="DETECTION",
            details="Evaluate threat levels and prioritize HIGH threats"
        ),
        create_system_message_event(
            30.0,
            "REMINDER: Use light gun to select tracks",
            category="TUTORIAL",
            details="Press D key, then click on track to view details"
        ),
    ]


def get_scenario_2_events() -> List[ScenarioEvent]:
    """Demo 2 - Mixed Friendly/Unknown: Course changes and IFF updates"""
    return [
        create_system_message_event(
            5.0,
            "MIXED AIR PICTURE - VERIFY IFF",
            category="DETECTION",
            details="5 contacts detected. Classify before engaging."
        ),
        # Unknown turns toward defensive perimeter
        create_course_change_event(
            20.0,
            "TGT-2002",
            new_heading=180,  # Turn south toward targets
            message="TGT-2002 COURSE CHANGE - Now heading 180"
        ),
        # Missile accelerates
        create_course_change_event(
            15.0,
            "TGT-2005",
            new_speed=950,
            message="TGT-2005 ACCELERATING - Speed now 950 knots"
        ),
        create_threat_escalation_event(
            25.0,
            "TGT-2002",
            "CRITICAL",
            message="TGT-2002 ESCALATED TO CRITICAL"
        ),
    ]


def get_scenario_3_events() -> List[ScenarioEvent]:
    """Demo 3 - High Threat Saturation: Additional wave arrives"""
    return [
        create_system_message_event(
            5.0,
            "MULTIPLE HIGH THREATS - SATURATION ATTACK",
            category="WARNING",
            details="6 hostile contacts inbound. Prioritize intercepts."
        ),
        # Second wave spawns after 30 seconds
        create_wave_spawn_event(
            30.0,
            "Wave 2",
            [
                {
                    "track_id": "TGT-3007",
                    "x": 0.1, "y": 0.5,
                    "heading": 90, "speed": 720,
                    "altitude": 43000,
                    "track_type": "MISSILE",
                    "threat_level": "HIGH"
                },
                {
                    "track_id": "TGT-3008",
                    "x": 0.9, "y": 0.5,
                    "heading": 270, "speed": 700,
                    "altitude": 44000,
                    "track_type": "AIRCRAFT",
                    "threat_level": "HIGH"
                }
            ],
            message="SECOND WAVE DETECTED - 2 additional HIGH threats"
        ),
    ]


def get_scenario_5_events() -> List[ScenarioEvent]:
    """Scenario 5 - Correlation Training: Clues revealed over time"""
    return [
        create_system_message_event(
            5.0,
            "IFF AMBIGUOUS - Manual correlation required",
            category="CORRELATION",
            details="Use speed, altitude, heading to classify tracks"
        ),
        # TGT-5002 shows friendly IFF after 20 seconds
        create_system_message_event(
            20.0,
            "IFF RESPONSE: TGT-5002 transmitting friendly codes",
            category="IFF",
            details="Suggest classify as FRIENDLY"
        ),
        # TGT-5003 makes aggressive turn toward airspace
        create_course_change_event(
            25.0,
            "TGT-5003",
            new_heading=135,
            new_speed=600,
            message="TGT-5003 AGGRESSIVE MANEUVER - heading toward airspace"
        ),
        # TGT-5004 contacts tower
        create_system_message_event(
            35.0,
            "TGT-5004 RADIO CONTACT: Commercial flight requesting clearance",
            category="COMMS",
            details="Suggest classify as FRIENDLY"
        ),
    ]


def get_scenario_6_events() -> List[ScenarioEvent]:
    """Scenario 6 - Equipment Degradation: Tube failures during mission"""
    return [
        create_system_message_event(
            5.0,
            "NORMAL OPERATIONS - All systems green",
            category="STATUS"
        ),
        # First tube failure at 15 seconds
        create_tube_failure_event(
            15.0,
            tube_ids=None,  # Random tube
            count=2,
            message="TUBE FAILURE DETECTED - Performance degraded"
        ),
        # Critical target spawns during degradation
        create_spawn_event(
            25.0,
            track_id="TGT-6005",
            x=0.2, y=0.8,
            heading=45, speed=580,
            altitude=28000,
            track_type="MISSILE",
            threat_level="CRITICAL",
            message="CRITICAL THREAT INBOUND - Intercept immediately"
        ),
        # Second tube failure cascade
        create_tube_failure_event(
            40.0,
            count=3,
            message="MULTIPLE TUBE FAILURES - System performance <70%"
        ),
        # Friendly needs emergency routing during crisis
        create_spawn_event(
            50.0,
            track_id="TGT-6006",
            x=0.5, y=0.1,
            heading=180, speed=320,
            altitude=15000,
            track_type="FRIENDLY",
            threat_level="LOW",
            message="FRIENDLY declaring emergency - requesting safe routing"
        ),
    ]


def get_scenario_7_events() -> List[ScenarioEvent]:
    """Scenario 7 - Saturated Defense: Overwhelming multi-wave attack"""
    return [
        create_system_message_event(
            5.0,
            "LARGE RAID DETECTED - Multiple formations",
            category="WARNING",
            details="8 hostiles inbound. You have 3 interceptors. PRIORITIZE."
        ),
        # Decoys reveal themselves
        create_system_message_event(
            20.0,
            "TGT-7006 and TGT-7007 assessed as DECOYS",
            category="INTEL",
            details="Low altitude, slow speed. Do not waste interceptors."
        ),
        # Third wave - additional bomber
        create_spawn_event(
            35.0,
            track_id="TGT-7009",
            x=0.15, y=0.15,
            heading=60, speed=430,
            altitude=27000,
            track_type="AIRCRAFT",
            threat_level="CRITICAL",
            message="FOURTH BOMBER DETECTED - Total 4 CRITICAL threats"
        ),
        # Missile platform launches
        create_spawn_event(
            50.0,
            track_id="TGT-7010",
            x=0.35, y=0.12,  # Spawn near TGT-7008 (missile platform)
            heading=90, speed=850,
            altitude=60000,
            track_type="MISSILE",
            threat_level="CRITICAL",
            message="MISSILE LAUNCH DETECTED from TGT-7008"
        ),
        # Time pressure reminder
        create_system_message_event(
            60.0,
            "CRITICAL: Bombers approaching 200-mile perimeter",
            category="WARNING",
            details="Intercept window closing in 60 seconds"
        ),
    ]


# Mapping of scenario names to event lists
SCENARIO_EVENTS = {
    "Demo 1 - Three Inbound": get_scenario_1_events(),
    "Demo 2 - Mixed Friendly/Unknown": get_scenario_2_events(),
    "Demo 3 - High Threat Saturation": get_scenario_3_events(),
    "Demo 4 - Patrol Route": [],  # No special events, just observation
    "Scenario 5 - Correlation Training": get_scenario_5_events(),
    "Scenario 6 - Equipment Degradation": get_scenario_6_events(),
    "Scenario 7 - Saturated Defense": get_scenario_7_events(),
}


def get_events_for_scenario(scenario_name: str) -> List[ScenarioEvent]:
    """Get event list for a scenario"""
    return SCENARIO_EVENTS.get(scenario_name, [])
