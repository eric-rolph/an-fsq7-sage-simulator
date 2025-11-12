from typing import List, Dict, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
import time

# ============================================================================
# Core Data Models for Interactive SAGE Simulator
# ============================================================================

class TrackType(str, Enum):
    FRIENDLY = "friendly"
    HOSTILE = "hostile"
    UNKNOWN = "unknown"
    MISSILE = "missile"
    INTERCEPTOR = "interceptor"

class TrackStatus(str, Enum):
    ACTIVE = "active"
    INTERCEPTED = "intercepted"
    DEPARTED = "departed"

@dataclass
class Track:
    """Represents a radar track (aircraft, missile, etc.)"""
    id: str
    type: TrackType
    x: float  # Normalized 0.0-1.0
    y: float  # Normalized 0.0-1.0
    vx: float  # Velocity in normalized units/sec
    vy: float
    altitude: int  # feet
    speed: int  # knots
    heading: int  # degrees 0-359
    status: TrackStatus = TrackStatus.ACTIVE
    selected: bool = False
    trail: List[tuple[float, float]] = field(default_factory=list)
    t_minus: Optional[int] = None  # For missiles: seconds to impact
    target_id: Optional[str] = None  # For interceptors

@dataclass
class CpuStep:
    """Single CPU execution step"""
    n: int
    instruction: str
    regs: Dict[str, int]
    memory_access: Optional[str] = None

@dataclass
class CpuTrace:
    """CPU program execution trace"""
    program_name: str
    status: Literal["Idle", "Running", "Done", "Error"]
    steps: List[CpuStep] = field(default_factory=list)
    final_result: Optional[Dict] = None
    elapsed_ms: int = 0
    speed: Literal["realtime", "slow", "step"] = "realtime"

@dataclass
class TubeState:
    """Individual vacuum tube state"""
    id: str
    row: int
    col: int
    health: float  # 0.0-1.0
    status: Literal["ok", "degrading", "failed", "warming_up"]
    warmup_progress: float = 0.0

@dataclass
class MaintenanceState:
    """Computer maintenance system state"""
    tubes: List[TubeState] = field(default_factory=list)
    performance_penalty: float = 0.0  # 0.0-1.0
    replacing_tube_id: Optional[str] = None

@dataclass
class MissionStep:
    """Single step in a tutorial mission"""
    text: str
    check: str  # Python expression to evaluate
    completed: bool = False

@dataclass
class Mission:
    """Tutorial mission"""
    id: str
    title: str
    steps: List[MissionStep]
    current_step: int = 0
    completed: bool = False

@dataclass
class UIState:
    """UI interaction state"""
    # Light gun
    lightgun_armed: bool = False
    lightgun_x: int = 0
    lightgun_y: int = 0
    
    # Selection
    selected_track_id: Optional[str] = None
    
    # Filters (S1-S13)
    active_filters: List[str] = field(default_factory=list)
    
    # Overlays (S20-S24)
    active_overlays: Dict[str, bool] = field(default_factory=lambda: {
        "flight_paths": False,
        "range_circles": True,
        "callsigns": True,
        "sector_boundaries": False,
        "coastlines": True
    })
    
    # Scope view
    scope_center: tuple[float, float] = (0.5, 0.5)
    scope_zoom: float = 1.0
    
    # Panels
    show_cpu_trace: bool = False
    show_maintenance: bool = False
    show_tutorial: bool = True

@dataclass
class SimulatorState:
    """Complete simulator state - single source of truth"""
    tracks: List[Track] = field(default_factory=list)
    ui: UIState = field(default_factory=UIState)
    cpu_trace: CpuTrace = field(default_factory=lambda: CpuTrace("", "Idle"))
    maintenance: MaintenanceState = field(default_factory=MaintenanceState)
    missions: List[Mission] = field(default_factory=list)
    current_mission_idx: int = 0
    
    # Timing
    last_tick: float = field(default_factory=time.time)
    paused: bool = False
    
    # System status
    powered_on: bool = False
    warmup_progress: float = 0.0

# ============================================================================
# Helper Functions
# ============================================================================

def create_initial_tubes() -> List[TubeState]:
    """Create 8x8 grid of vacuum tubes"""
    tubes = []
    for row in range(8):
        for col in range(8):
            tubes.append(TubeState(
                id=f"T{row}{col}",
                row=row,
                col=col,
                health=1.0,
                status="ok"
            ))
    return tubes

# Commented out - tutorial_system.py has its own mission definitions
# This version causes Reflex errors due to comparison operators in condition strings
def create_tutorial_missions() -> List[Mission]:
    """Create the 6 tutorial missions - DISABLED for now"""
    return []
    # return [
    #     Mission(
    #         id="mission_1",
    #         title="Power-On & Scope Basics",
    #         steps=[
    #             MissionStep("Power on the system", "state.powered_on"),
    #             MissionStep("Toggle range circles overlay", "'range_circles' in state.ui.active_overlays"),
    #             MissionStep("Toggle coastlines overlay", "state.ui.active_overlays.get('coastlines', False)")
    #         ]
    #     ),
    #     Mission(
    #         id="mission_2",
    #         title="Target Selection with Light Gun",
    #         steps=[
    #             MissionStep("Arm light gun (press D)", "state.ui.lightgun_armed"),
    #             MissionStep("Select any track", "state.ui.selected_track_id is not None")
    #         ]
    #     ),
    #     Mission(
    #         id="mission_3",
    #         title="Launch Intercept",
    #         steps=[
    #             MissionStep("Select a hostile track", "any(t.selected and t.type == 'hostile' for t in state.tracks)"),
    #             MissionStep("Launch intercept", "any(t.type == 'interceptor' for t in state.tracks)")
    #         ]
    #     ),
    #     Mission(
    #         id="mission_4",
    #         title="Use Console Filters",
    #         steps=[
    #             MissionStep("Show hostiles only (press S1)", "'hostile' in state.ui.active_filters"),
    #             MissionStep("Clear all filters", "len(state.ui.active_filters) == 0")
    #         ]
    #     ),
    #     Mission(
    #         id="mission_5",
    #         title="Computer Maintenance",
    #         steps=[
    #             MissionStep("Open maintenance panel", "state.ui.show_maintenance"),
    #             MissionStep("Replace a failed tube", "state.maintenance.replacing_tube_id is not None")
    #         ]
    #     ),
    # ]
