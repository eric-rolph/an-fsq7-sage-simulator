"""
AN/FSQ-7 Simulation Core Package

This package contains the pure simulation logic for the SAGE system,
separated from UI presentation concerns.
"""

from .sim_loop import Simulator
from .models import RadarTarget, VacuumTubeBank, MissionClock
from .scenarios import Scenario, load_scenario, list_scenarios, get_scenario
from .modes import DisplayMode, ConsoleModeInfo, get_mode_info, cycle_mode

__all__ = [
    # Core simulation
    "Simulator", 
    "RadarTarget", 
    "VacuumTubeBank", 
    "MissionClock",
    # Scenarios
    "Scenario",
    "load_scenario",
    "list_scenarios",
    "get_scenario",
    # Modes
    "DisplayMode",
    "ConsoleModeInfo",
    "get_mode_info",
    "cycle_mode",
]
