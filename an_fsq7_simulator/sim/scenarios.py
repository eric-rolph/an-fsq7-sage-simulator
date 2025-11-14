"""
Scenario definitions for the AN/FSQ-7 SAGE simulator.

Each scenario defines initial conditions (target positions, headings, threats)
to allow quick testing and demonstration of different operational situations.

Updated for Priority 4: Scenario System Enhancement
- Learning objectives for educational value
- Success criteria for mission completion
- Difficulty ratings
"""

from typing import List, Dict, Any
from .models import RadarTarget


class Scenario:
    """Defines a mission scenario with initial conditions and learning objectives."""
    
    def __init__(
        self,
        name: str,
        description: str,
        targets: List[RadarTarget],
        learning_objectives: List[str] = None,
        success_criteria: str = "Complete all objectives",
        difficulty: str = "beginner",  # "beginner", "intermediate", "advanced", "expert"
        objectives: List[str] = None
    ):
        self.name = name
        self.description = description
        self.targets = targets
        self.learning_objectives = learning_objectives or []
        self.success_criteria = success_criteria
        self.difficulty = difficulty
        self.objectives = objectives or ["Detect and track all targets", "Classify threats correctly", "Assign interceptors"]


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
        ],
        learning_objectives=[
            "Practice basic track detection and identification",
            "Learn to prioritize threats by level",
            "Master light gun selection and track detail viewing"
        ],
        success_criteria="Detect all 3 tracks and correctly identify threat levels",
        difficulty="beginner",
        objectives=[
            "Detect all 3 inbound tracks",
            "Classify each track by threat level",
            "Assign interceptors to HIGH threats first"
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
    
    # ========================================
    # EDUCATIONAL SCENARIOS (Priority 4)
    # ========================================
    
    "Scenario 5 - Correlation Training": Scenario(
        name="Scenario 5 - Correlation Training",
        description="Learn manual track classification with ambiguous targets requiring operator judgment",
        targets=[
            # Unknown aircraft with unclear IFF
            RadarTarget(
                target_id="TGT-5001",
                x=150, y=200,
                heading=90,
                speed=420,
                altitude=28000,
                target_type="UNKNOWN",
                threat_level="UNKNOWN"
            ),
            # Friendly with intermittent IFF
            RadarTarget(
                target_id="TGT-5002",
                x=650, y=350,
                heading=270,
                speed=380,
                altitude=22000,
                target_type="UNKNOWN",  # Should be classified as FRIENDLY
                threat_level="UNKNOWN"
            ),
            # Hostile with no IFF response
            RadarTarget(
                target_id="TGT-5003",
                x=400, y=100,
                heading=180,
                speed=550,
                altitude=35000,
                target_type="UNKNOWN",  # Should be classified as HOSTILE
                threat_level="UNKNOWN"
            ),
            # Commercial airliner off-course
            RadarTarget(
                target_id="TGT-5004",
                x=200, y=500,
                heading=45,
                speed=320,
                altitude=31000,
                target_type="UNKNOWN",  # Should be classified as FRIENDLY
                threat_level="UNKNOWN"
            ),
        ],
        learning_objectives=[
            "Practice manual track correlation when IFF is ambiguous",
            "Learn to use speed, altitude, and heading to infer track type",
            "Master light gun selection for detailed track inspection",
            "Understand when to escalate uncertain tracks to higher authority"
        ],
        success_criteria="Correctly classify all 4 tracks using manual correlation within 3 minutes",
        difficulty="intermediate",
        objectives=[
            "Select each uncorrelated track with light gun",
            "Analyze speed, altitude, heading patterns",
            "Manually classify all tracks correctly",
            "Complete within 180 seconds"
        ]
    ),
    
    "Scenario 6 - Equipment Degradation": Scenario(
        name="Scenario 6 - Equipment Degradation",
        description="Handle vacuum tube failures while maintaining air defense during active threats",
        targets=[
            # Wave 1: Initial hostiles
            RadarTarget(
                target_id="TGT-6001",
                x=100, y=150,
                heading=60,
                speed=480,
                altitude=26000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-6002",
                x=700, y=200,
                heading=120,
                speed=500,
                altitude=29000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            # Friendlies that need routing
            RadarTarget(
                target_id="TGT-6003",
                x=300, y=450,
                heading=0,
                speed=340,
                altitude=18000,
                target_type="FRIENDLY",
                threat_level="LOW"
            ),
            # Additional hostile during tube failures
            RadarTarget(
                target_id="TGT-6004",
                x=500, y=100,
                heading=150,
                speed=520,
                altitude=32000,
                target_type="AIRCRAFT",
                threat_level="CRITICAL"
            ),
        ],
        learning_objectives=[
            "Learn to prioritize critical targets during system degradation",
            "Practice rapid tube replacement under pressure",
            "Understand how performance penalty affects processing rates",
            "Master decision-making when system capacity is reduced"
        ],
        success_criteria="Maintain 70%+ system performance and intercept all CRITICAL threats",
        difficulty="advanced",
        objectives=[
            "Replace failed tubes within 30 seconds of failure",
            "Keep system performance above 70%",
            "Assign interceptors to all CRITICAL threats",
            "Complete scenario without missing high-priority targets"
        ]
    ),
    
    "Scenario 7 - Saturated Defense": Scenario(
        name="Scenario 7 - Saturated Defense",
        description="Defend against overwhelming attack with limited interceptor resources - prioritization is key",
        targets=[
            # Bomber wave - high priority
            RadarTarget(
                target_id="TGT-7001",
                x=100, y=100,
                heading=45,
                speed=420,
                altitude=28000,
                target_type="AIRCRAFT",
                threat_level="CRITICAL"
            ),
            RadarTarget(
                target_id="TGT-7002",
                x=150, y=250,
                heading=60,
                speed=410,
                altitude=26000,
                target_type="AIRCRAFT",
                threat_level="CRITICAL"
            ),
            # Fighter escorts - medium priority
            RadarTarget(
                target_id="TGT-7003",
                x=200, y=150,
                heading=50,
                speed=580,
                altitude=32000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            RadarTarget(
                target_id="TGT-7004",
                x=250, y=300,
                heading=55,
                speed=590,
                altitude=31000,
                target_type="AIRCRAFT",
                threat_level="HIGH"
            ),
            # Reconnaissance aircraft - lower priority
            RadarTarget(
                target_id="TGT-7005",
                x=650, y=400,
                heading=270,
                speed=350,
                altitude=42000,
                target_type="AIRCRAFT",
                threat_level="MEDIUM"
            ),
            # Decoy drones - distraction
            RadarTarget(
                target_id="TGT-7006",
                x=500, y=150,
                heading=135,
                speed=280,
                altitude=15000,
                target_type="UNKNOWN",
                threat_level="LOW"
            ),
            RadarTarget(
                target_id="TGT-7007",
                x=550, y=200,
                heading=140,
                speed=290,
                altitude=16000,
                target_type="UNKNOWN",
                threat_level="LOW"
            ),
            # Missile launch platform - CRITICAL
            RadarTarget(
                target_id="TGT-7008",
                x=300, y=100,
                heading=90,
                speed=460,
                altitude=24000,
                target_type="AIRCRAFT",
                threat_level="CRITICAL"
            ),
        ],
        learning_objectives=[
            "Learn strategic prioritization when overwhelmed",
            "Practice rapid threat assessment under time pressure",
            "Master interceptor resource allocation",
            "Understand the cost of engaging low-priority targets"
        ],
        success_criteria="Intercept all 3 CRITICAL threats before they penetrate defensive perimeter",
        difficulty="expert",
        objectives=[
            "Identify all CRITICAL threats (bombers and missile platform)",
            "Assign all 3 available interceptors to CRITICAL targets only",
            "Ignore or defer LOW and MEDIUM threats",
            "Achieve intercept before targets reach 200-mile range"
        ]
    ),
}


def get_scenario(name: str) -> Scenario:
    """Get a scenario by name."""
    return SCENARIOS.get(name)


def list_scenarios() -> List[str]:
    """Get list of available scenario names."""
    return list(SCENARIOS.keys())


def load_scenario(simulator, name: str):
    """
    Load a scenario into the simulator.
    Clears existing targets and spawns scenario targets.
    """
    scenario = get_scenario(name)
    if scenario:
        simulator.radar_targets.clear()
        simulator.radar_targets.extend(scenario.targets)
        simulator.tracked_objects_count = len(scenario.targets)
        simulator.high_threat_count = sum(1 for t in scenario.targets 
                                          if t.threat_level == "HIGH")

