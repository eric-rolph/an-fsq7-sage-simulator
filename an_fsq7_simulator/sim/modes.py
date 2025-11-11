"""
Console mode definitions for the AN/FSQ-7 SAGE operator console.

Defines the distinct operational modes that SAGE operators used,
with metadata about what each mode displays and what actions are available.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List


class DisplayMode(Enum):
    """Operator console display modes matching historical SAGE operation."""
    RADAR = "RADAR"
    TACTICAL = "TACTICAL"
    STATUS = "STATUS"
    MEMORY = "MEMORY"


@dataclass
class ConsoleModeInfo:
    """
    Metadata about a console display mode.
    
    Describes what the operator sees and can do in this mode.
    """
    mode: DisplayMode
    title: str
    description: str
    allowed_actions: List[str]
    shows_radar: bool = False
    shows_cpu: bool = False
    shows_memory: bool = False
    allows_light_gun: bool = False


# Mode definitions
MODE_INFO = {
    DisplayMode.RADAR: ConsoleModeInfo(
        mode=DisplayMode.RADAR,
        title="RADAR SURVEILLANCE",
        description="Air surveillance display showing tracked targets with threat assessment",
        allowed_actions=[
            "Light gun target selection",
            "Assign intercept course",
            "View target details",
            "Update threat assessment",
        ],
        shows_radar=True,
        allows_light_gun=True,
    ),
    
    DisplayMode.TACTICAL: ConsoleModeInfo(
        mode=DisplayMode.TACTICAL,
        title="TACTICAL SITUATION",
        description="Tactical overview with intercept courses and friendly aircraft",
        allowed_actions=[
            "View intercept assignments",
            "Monitor friendly positions",
            "Track engagement zones",
        ],
        shows_radar=True,
        allows_light_gun=False,
    ),
    
    DisplayMode.STATUS: ConsoleModeInfo(
        mode=DisplayMode.STATUS,
        title="SYSTEM STATUS",
        description="Computer system health: tubes, temperature, memory, CPU state",
        allowed_actions=[
            "Monitor tube failures",
            "Check memory capacity",
            "View CPU registers",
            "System diagnostics",
        ],
        shows_radar=False,
        shows_cpu=True,
        shows_memory=True,
        allows_light_gun=False,
    ),
    
    DisplayMode.MEMORY: ConsoleModeInfo(
        mode=DisplayMode.MEMORY,
        title="MEMORY VISUALIZATION",
        description="Magnetic core memory contents and program execution",
        allowed_actions=[
            "View memory banks",
            "Monitor program execution",
            "Inspect memory addresses",
        ],
        shows_radar=False,
        shows_cpu=True,
        shows_memory=True,
        allows_light_gun=False,
    ),
}


def get_mode_info(mode: DisplayMode) -> ConsoleModeInfo:
    """Get metadata for a display mode."""
    return MODE_INFO[mode]


def cycle_mode(current: DisplayMode) -> DisplayMode:
    """Get next mode in sequence."""
    modes = list(DisplayMode)
    current_idx = modes.index(current)
    next_idx = (current_idx + 1) % len(modes)
    return modes[next_idx]

