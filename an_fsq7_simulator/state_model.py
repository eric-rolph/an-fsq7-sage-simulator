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
    
    # Tabular display features (authentic SAGE format - C702-416L-ST Manual Figure 4-5)
    # These are generated from track data and displayed as 5x7 dot-matrix characters
    feature_a: str = ""  # Track identification (4 chars) - track ID/designation
    feature_b: str = ""  # Altitude & speed data (4 chars) - e.g., "35MD" = 35,000ft Medium speed
    feature_c: str = ""  # Classification & threat (4 chars) - e.g., "HS H" = Hostile High threat
    feature_d: str = ""  # Heading quadrant (2 chars) - e.g., "W " = Westbound
    position_mode: int = 0  # 0=RIGHT, 1=LEFT, 2=ABOVE, 3=BELOW (determines feature layout)


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


# ==========================================
# TABULAR DISPLAY FEATURE GENERATION
# ==========================================
# Based on C702-416L-ST Manual Figure 4-5 (authentic SAGE display format)

def generate_track_features(track: Track) -> Dict[str, str]:
    """
    Generate the 5-feature tabular display format for a track.
    Returns dict with keys: feature_a, feature_b, feature_c, feature_d
    
    Format per SAGE manual:
    - Feature A: Track identification (4 chars)
    - Feature B: Altitude & speed category (4 chars)
    - Feature C: Classification & threat level (4 chars)
    - Feature D: Heading quadrant (2 chars)
    - Feature E: Central point marker (rendered separately)
    """
    return {
        "feature_a": generate_feature_a(track),
        "feature_b": generate_feature_b(track),
        "feature_c": generate_feature_c(track),
        "feature_d": generate_feature_d(track)
    }


def generate_feature_a(track: Track) -> str:
    """
    Feature A: Track identification
    Format: 4 characters (alphanumeric)
    
    Examples from manual:
    - "FPTKG" (truncated to 4: "FPTK")
    - "GRB "
    - "C 6 "
    """
    # Use track ID, pad or truncate to 4 chars
    id_str = track.id or "UNK"
    
    # Remove common prefixes for cleaner display
    if id_str.startswith("TK"):
        id_str = id_str[2:]
    elif id_str.startswith("TRACK"):
        id_str = id_str[5:]
    
    # Truncate to 4 chars, pad with spaces if needed
    result = id_str[:4].ljust(4)
    return result


def generate_feature_b(track: Track) -> str:
    """
    Feature B: Altitude and speed data
    Format: 4 characters
    
    Encoding:
    - First 2 chars: Altitude in thousands of feet (e.g., "35" = 35,000ft)
    - Last 2 chars: Speed category
      * "SL" = Slow (< 300 knots)
      * "MD" = Medium (300-600 knots)
      * "FS" = Fast (600-800 knots)
      * "SS" = Supersonic (> 800 knots)
    
    Examples:
    - "35MD" = 35,000 feet, medium speed
    - "42FS" = 42,000 feet, fast
    - " 8SL" = 8,000 feet, slow
    """
    # Altitude in thousands of feet
    alt_thousands = track.altitude // 1000
    alt_str = str(alt_thousands).rjust(2)[:2]  # Right-justify, max 2 chars
    
    # Speed category
    speed = track.speed
    if speed < 300:
        speed_cat = "SL"
    elif speed < 600:
        speed_cat = "MD"
    elif speed < 800:
        speed_cat = "FS"
    else:
        speed_cat = "SS"
    
    return alt_str + speed_cat


def generate_feature_c(track: Track) -> str:
    """
    Feature C: Classification and threat level
    Format: 4 characters
    
    Encoding:
    - First 2 chars: Track type
      * "FR" = Friendly
      * "HS" = Hostile
      * "UN" = Unknown
      * "MS" = Missile
      * "BM" = Bomber
      * "FT" = Fighter
    - Last 2 chars: Threat level
      * " L" = Low
      * " M" = Medium
      * " H" = High
      * " C" = Critical
    
    Examples:
    - "HS H" = Hostile, High threat
    - "FR L" = Friendly, Low threat
    - "UN M" = Unknown, Medium threat
    """
    # Track type
    track_type = track.track_type.lower()
    if track_type == "friendly":
        type_str = "FR"
    elif track_type == "hostile":
        type_str = "HS"
    elif track_type == "unknown":
        type_str = "UN"
    elif track_type == "missile":
        type_str = "MS"
    elif track_type == "bomber":
        type_str = "BM"
    elif track_type == "fighter":
        type_str = "FT"
    else:
        type_str = "  "
    
    # Threat level
    threat = track.threat_level.upper()
    if threat == "CRITICAL":
        threat_str = " C"
    elif threat == "HIGH":
        threat_str = " H"
    elif threat == "MEDIUM":
        threat_str = " M"
    elif threat == "LOW":
        threat_str = " L"
    else:
        threat_str = "  "
    
    return type_str + threat_str


def generate_feature_d(track: Track) -> str:
    """
    Feature D: Heading quadrant
    Format: 2 characters
    
    Encoding (8 compass directions):
    - "N " = North (337.5° - 22.5°)
    - "NE" = Northeast (22.5° - 67.5°)
    - "E " = East (67.5° - 112.5°)
    - "SE" = Southeast (112.5° - 157.5°)
    - "S " = South (157.5° - 202.5°)
    - "SW" = Southwest (202.5° - 247.5°)
    - "W " = West (247.5° - 292.5°)
    - "NW" = Northwest (292.5° - 337.5°)
    
    Examples:
    - "W " = Westbound
    - "NE" = Northeast bound
    """
    heading = track.heading
    
    # Normalize heading to 0-360 range
    heading = heading % 360
    
    # Determine compass direction
    if heading >= 337.5 or heading < 22.5:
        return "N "
    elif heading >= 22.5 and heading < 67.5:
        return "NE"
    elif heading >= 67.5 and heading < 112.5:
        return "E "
    elif heading >= 112.5 and heading < 157.5:
        return "SE"
    elif heading >= 157.5 and heading < 202.5:
        return "S "
    elif heading >= 202.5 and heading < 247.5:
        return "SW"
    elif heading >= 247.5 and heading < 292.5:
        return "W "
    elif heading >= 292.5 and heading < 337.5:
        return "NW"
    else:
        return "  "


def calculate_position_mode(track: Track) -> int:
    """
    Determine best position mode for tabular display to avoid clutter.
    
    Position modes:
    - 0: RIGHT - Format to right of central point (E feature)
    - 1: LEFT - Format to left of central point
    - 2: ABOVE - Format above central point
    - 3: BELOW - Format below central point
    
    Simple heuristic based on screen quadrant:
    - Top-left quadrant (x < 0.5, y < 0.5): RIGHT
    - Top-right quadrant (x >= 0.5, y < 0.5): LEFT
    - Bottom-left quadrant (x < 0.5, y >= 0.5): RIGHT
    - Bottom-right quadrant (x >= 0.5, y >= 0.5): LEFT
    
    This prevents formats from running off screen edges.
    """
    x, y = track.x, track.y
    
    if x < 0.5 and y < 0.5:
        return 0  # RIGHT
    elif x >= 0.5 and y < 0.5:
        return 1  # LEFT
    elif x < 0.5 and y >= 0.5:
        return 0  # RIGHT
    else:
        return 1  # LEFT


def update_track_display_features(track: Track) -> None:
    """
    Update all tabular display features for a track in-place.
    Call this after track data changes (position, heading, altitude, etc.)
    """
    features = generate_track_features(track)
    track.feature_a = features["feature_a"]
    track.feature_b = features["feature_b"]
    track.feature_c = features["feature_c"]
    track.feature_d = features["feature_d"]
    track.position_mode = calculate_position_mode(track)
