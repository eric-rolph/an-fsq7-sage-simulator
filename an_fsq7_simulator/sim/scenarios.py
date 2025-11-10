"""
Scenario definitions for the AN/FSQ-7 SAGE simulator.

Each scenario defines initial conditions (target positions, headings, threats)
to allow quick testing and demonstration of different operational situations.
"""

from typing import List
from .models import RadarTarget


class Scenario:
    ""`Defines a mission scenario with initial conditions.`""
    
    def __init__(self, name: str, description: str, targets: List[RadarTarget]):
        self.name = name
        self.description = description
        self.targets = targets


# Pre-defined scenarios
SCENARIOS = {
    "Demo 1 - Three Inbound": Scenario(
        name="Demo 1 - Three Inbound",
        description="3 inbound aircraft from different headings, mixed threat levels",
        targets=[
            RadarTarget(
                target_id="TGT-1001",
                x=100, y=100,
                heading=45,
                speed=450,
                altitude=25000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-1002",
                x=700, y=100,
                heading=135,
                speed=380,
                altitude=30000,
                target_type="AIRCRAFT",
                threat_level="MEDIUM"
            ),
            RadarTarget(
                target_id="TGT-1003",
                x=400, y=500,
                heading=0,
                speed=520,
                altitude=35000,
                target_type="AIRCRAFT",
                threat_level="LOW"
            ),
        ]
    ),
    
    "Demo 2 - Mixed Friendly/Unknown": Scenario(
        name="Demo 2 - Mixed Friendly/Unknown",
        description="Mix of friendly, unknown, and hostile aircraft",
        targets=[
            RadarTarget(
                target_id="TGT-2001",
                x=200, y=300,
                heading=90,
                speed=300,
                altitude=15000,
                target_type="FRIENDLY",
                threat_level="LOW"
            ),
            RadarTarget(
                target_id="TGT-2002",
                x=600, y=400,
                heading=270,
                speed=600,
                altitude=40000,
                target_type="UNKNOWN",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-2003",
                x=400, y=200,
                heading=180,
                speed=450,
                altitude=28000,
                target_type="AIRCRAFT",
                threat_level="MEDIUM"
            ),
            RadarTarget(
                target_id="TGT-2004",
                x=100, y=500,
                heading=45,
                speed=350,
                altitude=20000,
                target_type="FRIENDLY",
                threat_level="LOW"
            ),
            RadarTarget(
                target_id="TGT-2005",
                x=700, y=300,
                heading=225,
                speed=750,
                altitude=50000,
                target_type="MISSILE",
                threat_level="HIGH"
            ),
        ]
    ),
    
    "Demo 3 - High Threat Saturation": Scenario(
        name="Demo 3 - High Threat Saturation",
        description="Multiple high-threat targets approaching simultaneously",
        targets=[
            RadarTarget(
                target_id="TGT-3001",
                x=50, y=50,
                heading=45,
                speed=800,
                altitude=45000,
                target_type="MISSILE",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-3002",
                x=750, y=50,
                heading=135,
                speed=750,
                altitude=42000,
                target_type="MISSILE",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-3003",
                x=50, y=550,
                heading=315,
                speed=700,
                altitude=48000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-3004",
                x=750, y=550,
                heading=225,
                speed=720,
                altitude=46000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-3005",
                x=400, y=100,
                heading=180,
                speed=680,
                altitude=44000,
                target_type="MISSILE",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-3006",
                x=400, y=500,
                heading=0,
                speed=690,
                altitude=47000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
        ]
    ),
    
    "Demo 4 - Patrol Route": Scenario(
        name="Demo 4 - Patrol Route",
        description="Friendly patrol aircraft with unknown contacts",
        targets=[
            RadarTarget(
                target_id="TGT-4001",
                x=150, y=300,
                heading=90,
                speed=280,
                altitude=18000,
                target_type="FRIENDLY",
                threat_level="LOW"
            ),
            RadarTarget(
                target_id="TGT-4002",
                x=650, y=300,
                heading=270,
                speed=280,
                altitude=18000,
                target_type="FRIENDLY",
                threat_level="LOW"
            ),
            RadarTarget(
                target_id="TGT-4003",
                x=400, y=400,
                heading=0,
                speed=450,
                altitude=32000,
                target_type="UNKNOWN",
                threat_level="MEDIUM"
            ),
            RadarTarget(
                target_id="TGT-4004",
                x=300, y=150,
                heading=135,
                speed=380,
                altitude=25000,
                target_type="UNKNOWN",
                threat_level="MEDIUM"
            ),
        ]
    ),
}


def get_scenario(name: str) -> Scenario:
    ""`Get a scenario by name.`""
    return SCENARIOS.get(name)


def list_scenarios() -> List[str]:
    ""`Get list of available scenario names.`""
    return list(SCENARIOS.keys())


def load_scenario(simulator, name: str):
    ""`
    Load a scenario into the simulator.
    Clears existing targets and spawns scenario targets.
    `""
    scenario = get_scenario(name)
    if scenario:
        simulator.radar_targets.clear()
        simulator.radar_targets.extend(scenario.targets)
        simulator.tracked_objects_count = len(scenario.targets)
        simulator.high_threat_count = sum(1 for t in scenario.targets 
                                          if t.threat_level == "HIGH")
