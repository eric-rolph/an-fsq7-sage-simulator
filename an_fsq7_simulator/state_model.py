"""
State Model - Data Classes for SAGE Simulator

Defines all data structures used by components:
- Track data (radar targets)
- CPU execution trace
- Vacuum tube state
- Tutorial missions
- UI state
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


# ==========================================
# RADAR / TRACK DATA
# ==========================================

@dataclass
class Track:
    """Radar track (target) information"""
    id: str
    x: float  # Position in normalized coordinates (0.0-1.0)
    y: float  # Position in normalized coordinates (0.0-1.0)
    vx: float = 0.0  # Velocity X component (normalized units/sec)
    vy: float = 0.0  # Velocity Y component (normalized units/sec)
    altitude: int = 0  # Feet
    speed: int = 0  # Knots
    heading: int = 0  # Degrees (0-359)
    track_type: str = "unknown"  # "hostile", "friendly", "unknown", "missile"
    threat_level: str = "UNKNOWN"  # "CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"
    designation: str = ""  # Operator designation
    interceptor_assigned: bool = False
    time_detected: float = 0.0  # Seconds since scenario start
    selected: bool = False  # Light gun selection state
    trail: List[tuple[float, float]] = field(default_factory=list)  # Position history for trail rendering


@dataclass
class UIState:
    """UI interaction state"""
    lightgun_armed: bool = False
    selected_track_id: str = ""
    active_filters: List[str] = field(default_factory=list)
    active_overlays: List[str] = field(default_factory=list)


# ==========================================
# CPU EXECUTION TRACE
# ==========================================

@dataclass
class CpuRegisters:
    """CPU register state at a point in time"""
    A: int = 0  # Accumulator
    B: int = 0  # B register
    PC: int = 0  # Program counter
    FLAGS: int = 0  # Status flags


@dataclass
class ExecutionStep:
    """Single instruction execution"""
    step_number: int
    instruction: str
    description: str
    registers: CpuRegisters
    memory_access: Optional[str] = None


@dataclass
class CpuTrace:
    """Complete program execution trace"""
    program_name: str
    status: str  # "loaded", "running", "complete", "error"
    steps: List[ExecutionStep]
    final_result: Optional[int] = None
    elapsed_ms: int = 0


# ==========================================
# VACUUM TUBE MAINTENANCE
# ==========================================

@dataclass
class TubeState:
    """Individual vacuum tube status"""
    id: int
    health: int  # 0-100
    status: str  # "ok", "degrading", "failed", "warming"
    temperature: int = 0  # Celsius
    hours_used: int = 0


@dataclass
class MaintenanceState:
    """System maintenance status"""
    tubes: List[TubeState]
    performance_penalty: float = 0.0  # 0.0-1.0 (system slowdown)
    failed_tube_count: int = 0
    last_maintenance: float = 0.0


# ==========================================
# TUTORIAL SYSTEM
# ==========================================

@dataclass
class MissionStep:
    """Single step in a tutorial mission"""
    text: str
    check_condition: str  # State condition to check (e.g., "lightgun_armed")
    hint: str = ""
    highlight_element: str = ""  # CSS selector to highlight


@dataclass
class Mission:
    """Tutorial mission definition"""
    id: str
    title: str
    description: str
    steps: List[MissionStep]
    reward_message: str = ""


# ==========================================
# SYSTEM MESSAGES
# ==========================================

@dataclass
class SystemMessage:
    """Operator action log message"""
    timestamp: str
    level: str  # "info", "warning", "critical"
    category: str  # "operator", "system", "intercept", "maintenance"
    message: str
    details: str = ""


# ==========================================
# GEOGRAPHIC DATA
# ==========================================

@dataclass
class GeographicFeature:
    """Coastline or border feature"""
    name: str
    points: List[tuple]  # List of (lat, lon) coordinates
    feature_type: str  # "coastline", "border", "airbase"


# ==========================================
# SCENARIO DATA
# ==========================================

@dataclass
class ScenarioDefinition:
    """Scenario configuration"""
    id: str
    name: str
    tier: str  # "basic", "intermediate", "advanced", "expert"
    description: str
    objectives: List[str]
    initial_tracks: int
    spawn_rate: float  # Tracks per minute
    duration: int  # Seconds
    success_criteria: Dict[str, any]
    special_conditions: List[str]
    briefing: str
