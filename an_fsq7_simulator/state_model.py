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
from typing import List, Optional, Dict, Any
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
    
    # Correlation state (for system transparency and learning)
    correlation_state: str = "uncorrelated"  # "uncorrelated", "correlating", "correlated"
    confidence_level: str = "unknown"  # "low", "medium", "high", "unknown"
    correlation_reason: str = ""  # Why classified: "auto_iff", "auto_velocity", "manual", "visual"
    classification_time: Optional[float] = None  # When track was classified


@dataclass
class Interceptor:
    """Interceptor aircraft available for assignment"""
    id: str
    aircraft_type: str  # "F-89 Scorpion", "F-102 Delta Dagger", "F-106 Delta Dart"
    base_name: str      # "Otis AFB", "Hanscom Field", "McGuire AFB"
    base_x: float       # Base location in normalized coordinates (0.0-1.0)
    base_y: float
    x: float = 0.0      # Current position (starts at base)
    y: float = 0.0
    status: str = "READY"  # READY, SCRAMBLING, AIRBORNE, ENGAGING, RETURNING, REFUELING
    fuel_percent: int = 100
    max_speed: int = 600  # knots
    current_speed: int = 0
    altitude: int = 0
    heading: int = 0  # degrees
    weapon_type: str = "AIM-4 Falcon"
    weapons_remaining: int = 4
    assigned_target_id: Optional[str] = None
    engagement_range: float = 10.0 / 600.0  # 10 nautical miles in normalized units
    
    def __post_init__(self):
        """Initialize position at base if not set"""
        if self.x == 0.0 and self.y == 0.0:
            self.x = self.base_x
            self.y = self.base_y


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
    success_criteria: Dict[str, Any]
    special_conditions: List[str]
    briefing: str


@dataclass
class ScenarioMetrics:
    """Performance metrics tracked during scenario execution"""
    # Detection metrics
    tracks_detected: int = 0
    tracks_total: int = 0
    
    # Classification metrics
    correct_classifications: int = 0
    total_classifications: int = 0
    
    # Intercept metrics
    successful_intercepts: int = 0
    attempted_intercepts: int = 0
    
    # Timing
    scenario_start_time: float = 0.0
    scenario_duration: float = 0.0
    
    # Objectives
    objectives: List[str] = field(default_factory=list)
    completed_objectives: List[bool] = field(default_factory=list)
    success_criteria: str = ""
    
    # Learning moments (mistakes/warnings)
    learning_moments: List[Dict[str, str]] = field(default_factory=list)
    
    # Overall score (0-100)
    overall_score: float = 0.0
    
    def calculate_overall_score(self) -> float:
        """Calculate overall performance score"""
        detection_score = (self.tracks_detected / self.tracks_total * 100) if self.tracks_total > 0 else 0
        classification_score = (self.correct_classifications / self.total_classifications * 100) if self.total_classifications > 0 else 0
        intercept_score = (self.successful_intercepts / self.attempted_intercepts * 100) if self.attempted_intercepts > 0 else 0
        
        # Weighted average: 30% detection, 40% classification, 30% intercepts
        self.overall_score = (detection_score * 0.3 + classification_score * 0.4 + intercept_score * 0.3)
        return self.overall_score
    
    def add_learning_moment(self, severity: str, title: str, description: str, tip: str):
        """Add a learning moment (mistake or warning)"""
        self.learning_moments.append({
            "severity": severity,  # "warning" or "error"
            "title": title,
            "description": description,
            "tip": tip
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Reflex state"""
        return {
            "tracks_detected": self.tracks_detected,
            "tracks_total": self.tracks_total,
            "correct_classifications": self.correct_classifications,
            "total_classifications": self.total_classifications,
            "successful_intercepts": self.successful_intercepts,
            "attempted_intercepts": self.attempted_intercepts,
            "scenario_duration": self.scenario_duration,
            "objectives": self.objectives,
            "completed_objectives": self.completed_objectives,
            "success_criteria": self.success_criteria,
            "learning_moments": self.learning_moments,
            "overall_score": self.overall_score
        }
