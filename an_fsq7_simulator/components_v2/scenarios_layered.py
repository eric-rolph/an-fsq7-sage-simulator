"""
Skill-Layered Scenarios

Requirement #5: Skill-Layered Scenarios

Create 4 scenario tiers:
1. BASIC - Single track, straightforward intercept
2. INTERMEDIATE - Multiple tracks (3-5), friend/foe identification
3. ADVANCED - High-density (10-20 tracks), prioritization required
4. EXPERT - Abnormal/spoof (jammer, chaff, decoys, coordinated attack)

All scenarios use same UI, menu-loadable.
Progressive difficulty for operator training.
"""

import reflex as rx
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Callable
import random


class ScenarioTier(Enum):
    """Difficulty tiers for scenarios"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Scenario:
    """
    Complete scenario definition
    """
    id: str
    name: str
    tier: ScenarioTier
    description: str
    objectives: List[str]
    initial_tracks: int
    spawn_rate: float  # Tracks per minute
    duration: int  # Seconds
    success_criteria: Dict[str, any]
    special_conditions: List[str]
    briefing: str
    

# ==========================================
# TIER 1: BASIC SCENARIOS
# ==========================================

SCENARIO_BASIC_SINGLE_BOMBER = Scenario(
    id="basic_001",
    name="Single Bomber Intercept",
    tier=ScenarioTier.BASIC,
    description="One hostile bomber inbound from Arctic. Simple detection and intercept.",
    objectives=[
        "Detect the inbound bomber",
        "Designate target with light gun",
        "Launch interceptor",
        "Confirm successful intercept"
    ],
    initial_tracks=1,
    spawn_rate=0.0,  # No additional spawns
    duration=300,  # 5 minutes
    success_criteria={
        "tracks_intercepted": 1,
        "time_limit": 300,
        "false_positives": 0  # Don't engage friendlies
    },
    special_conditions=[],
    briefing="""
TRAINING SCENARIO 001: BASIC INTERCEPT

SITUATION:
Single hostile bomber detected inbound from Arctic region.
Speed: 500 knots, Altitude: 40,000 feet.
Heading: 180° (due south toward NYC).

YOUR TASK:
1. Wait for radar contact to appear (white pulsing dot)
2. Press 'D' key to arm light gun
3. Click on the bomber to designate
4. Click "LAUNCH INTERCEPT" button
5. Watch interceptor (blue) close on target

SUCCESS:
Hostile neutralized before reaching defended area.

This is a straightforward scenario. Take your time and learn the controls.
"""
)


SCENARIO_BASIC_MISSILE_DEFENSE = Scenario(
    id="basic_002",
    name="Single Missile Defense",
    tier=ScenarioTier.BASIC,
    description="ICBM launch detected. Track and intercept incoming missile.",
    objectives=[
        "Detect missile launch",
        "Track high-speed target",
        "Launch interceptor quickly (time critical)",
        "Neutralize before impact"
    ],
    initial_tracks=1,
    spawn_rate=0.0,
    duration=180,  # 3 minutes (time pressure!)
    success_criteria={
        "tracks_intercepted": 1,
        "time_limit": 120,  # Must intercept within 2 minutes
        "false_positives": 0
    },
    special_conditions=["time_critical"],
    briefing="""
TRAINING SCENARIO 002: MISSILE DEFENSE

SITUATION:
ICBM launch detected from hostile territory.
Speed: 1,500 knots (Mach 2+), Altitude: 65,000 feet.
Trajectory: Ballistic arc toward East Coast.

YOUR TASK:
1. Locate fast-moving magenta track (missile)
2. Designate immediately (time is critical!)
3. Launch interceptor
4. Monitor T-minus countdown in Track Detail panel

SUCCESS:
Intercept before T-00:00 (impact).

WARNING: Missiles move FAST. You have less than 2 minutes!
"""
)


# ==========================================
# TIER 2: INTERMEDIATE SCENARIOS
# ==========================================

SCENARIO_INTER_MIXED_TRAFFIC = Scenario(
    id="inter_001",
    name="Mixed Traffic Identification",
    tier=ScenarioTier.INTERMEDIATE,
    description="Multiple tracks: 2 hostile, 2 friendly, 1 unknown. Identify and engage only hostiles.",
    objectives=[
        "Identify all 5 tracks correctly",
        "Engage only hostile targets (2)",
        "Do NOT engage friendlies",
        "Investigate unknown contact"
    ],
    initial_tracks=5,
    spawn_rate=0.0,
    duration=600,  # 10 minutes
    success_criteria={
        "tracks_intercepted": 2,  # Both hostiles
        "false_positives": 0,      # No friendlies hit
        "correct_ids": 5           # All tracks ID'd
    },
    special_conditions=["friend_or_foe"],
    briefing="""
TRAINING SCENARIO 003: FRIEND OR FOE

SITUATION:
Multiple radar contacts in defended airspace.
- 2 Hostile bombers (RED) inbound
- 2 Friendly CAP patrol (GREEN) on station
- 1 Unknown aircraft (YELLOW) loitering

YOUR TASK:
1. Use SD Console S2/S3/S4 buttons to filter by type
2. Designate and engage ONLY hostile tracks (red)
3. Monitor friendly tracks but do not engage
4. Investigate unknown track (may be civilian)

SUCCESS:
Both hostiles neutralized, zero friendly casualties.

TIP: Use the console filter buttons to isolate hostiles!
"""
)


SCENARIO_INTER_BOMBER_STREAM = Scenario(
    id="inter_002",
    name="Bomber Stream",
    tier=ScenarioTier.INTERMEDIATE,
    description="Formation of 5 bombers in tight formation. Intercept priority targets.",
    objectives=[
        "Detect bomber formation",
        "Prioritize lead bomber",
        "Engage all 5 bombers",
        "Minimize response time"
    ],
    initial_tracks=5,
    spawn_rate=0.5,  # One more every 2 minutes (reinforcements)
    duration=900,  # 15 minutes
    success_criteria={
        "tracks_intercepted": 5,
        "lead_bomber_first": True,  # Must hit lead bomber first
        "time_limit": 900
    },
    special_conditions=["formation_flying", "priority_targets"],
    briefing="""
TRAINING SCENARIO 004: BOMBER STREAM

SITUATION:
Enemy bomber formation detected: 5 aircraft in tight stream.
Lead bomber (B-001) coordinates formation.
Speed: 550 knots, Altitude: 38,000 feet.

YOUR TASK:
1. Identify the lead bomber (first in formation)
2. Engage lead bomber FIRST (breaks formation)
3. Then engage remaining bombers
4. Expect reinforcements (additional bombers may appear)

SUCCESS:
All bombers neutralized, lead bomber hit first.

TIP: Breaking the formation makes remaining bombers easier targets!
"""
)


# ==========================================
# TIER 3: ADVANCED SCENARIOS
# ==========================================

SCENARIO_ADV_HIGH_DENSITY = Scenario(
    id="adv_001",
    name="High-Density Airspace",
    tier=ScenarioTier.ADVANCED,
    description="15-20 tracks: hostiles, friendlies, unknowns. Prioritize threats.",
    objectives=[
        "Track 15-20 simultaneous contacts",
        "Prioritize high-threat targets",
        "Engage 8+ hostile targets",
        "Maintain situational awareness"
    ],
    initial_tracks=15,
    spawn_rate=2.0,  # 2 per minute
    duration=1200,  # 20 minutes
    success_criteria={
        "tracks_intercepted": 8,
        "high_threats_first": True,
        "false_positives": 0,
        "response_time_avg": 30  # Avg 30 sec per engagement
    },
    special_conditions=["high_density", "prioritization"],
    briefing="""
TRAINING SCENARIO 005: MASS RAID

SITUATION:
SATURATION ATTACK in progress!
15-20 contacts detected with more inbound.
Mix of hostiles, friendlies, and unknowns.

YOUR TASK:
1. Use altitude filters (S8/S9/S10) to separate by altitude
2. Use HOSTILE filter (S4) to isolate threats
3. Engage HIGH THREAT bombers and missiles first
4. Maintain formation awareness

SUCCESS:
8+ hostiles neutralized, no friendlies engaged, <30 sec avg response.

TIP: This is OVERWHELMING. Use filters aggressively!
Practice: Pan (arrows), Zoom (+/-), Filters (S buttons)
"""
)


SCENARIO_ADV_LAYERED_DEFENSE = Scenario(
    id="adv_002",
    name="Layered Defense",
    tier=ScenarioTier.ADVANCED,
    description="Multiple altitude bands: low (cruise missiles), med (bombers), high (recon).",
    objectives=[
        "Defend against 3 altitude bands",
        "Prioritize cruise missiles (low, fast)",
        "Engage bombers (medium altitude)",
        "Monitor high-altitude recon"
    ],
    initial_tracks=12,
    spawn_rate=1.5,
    duration=900,  # 15 minutes
    success_criteria={
        "low_alt_intercepted": 4,   # All cruise missiles
        "med_alt_intercepted": 6,   # Most bombers
        "layered_defense": True     # Engage by altitude priority
    },
    special_conditions=["altitude_separation", "cruise_missiles"],
    briefing="""
TRAINING SCENARIO 006: LAYERED ATTACK

SITUATION:
Enemy using layered attack strategy:
- LOW (<10K ft): 4 cruise missiles, 600 kts
- MEDIUM (10-30K ft): 6 bombers, 500 kts  
- HIGH (>30K ft): 2 recon aircraft, 400 kts

YOUR TASK:
1. Use altitude filters: S8 (LOW), S9 (MED), S10 (HIGH)
2. PRIORITY 1: Engage ALL cruise missiles (fastest threat)
3. PRIORITY 2: Engage bombers
4. PRIORITY 3: Monitor recon (no engagement unless hostile act)

SUCCESS:
All cruise missiles down, 6+ bombers intercepted.

TIP: Altitude separation is KEY. Filter aggressively!
"""
)


# ==========================================
# TIER 4: EXPERT SCENARIOS
# ==========================================

SCENARIO_EXPERT_ELECTRONIC_WARFARE = Scenario(
    id="expert_001",
    name="Electronic Warfare / Jamming",
    tier=ScenarioTier.EXPERT,
    description="Enemy using jammers and chaff. Tracks appear/disappear. Identify real targets.",
    objectives=[
        "Identify jammer aircraft (causes false tracks)",
        "Distinguish real targets from chaff",
        "Engage real bomber targets",
        "Neutralize jammer first"
    ],
    initial_tracks=8,
    spawn_rate=1.0,
    duration=900,
    success_criteria={
        "jammer_neutralized": True,
        "real_targets_hit": 5,
        "chaff_ignored": True  # Don't waste interceptors on chaff
    },
    special_conditions=["jamming", "chaff", "false_contacts"],
    briefing="""
TRAINING SCENARIO 007: ELECTRONIC WARFARE

SITUATION:
ADVANCED THREAT detected!
Enemy using electronic countermeasures:
- Jammer aircraft (J-001) creating false tracks
- Chaff clouds (C-xxx) appearing as targets
- Real bombers (B-xxx) mixed with decoys

YOUR TASK:
1. Identify jammer (look for tracks appearing near it)
2. PRIORITY: Neutralize jammer FIRST
3. Real targets move smoothly; chaff drifts/fades
4. Use FLIGHT PATHS overlay (S20) to see movement patterns

SUCCESS:
Jammer down first, 5 real bombers neutralized, no chaff engagements.

WARNING: This is EXPERT level. Expect confusion!
"""
)


SCENARIO_EXPERT_COORDINATED_ATTACK = Scenario(
    id="expert_002",
    name="Coordinated Multi-Vector Attack",
    tier=ScenarioTier.EXPERT,
    description="Simultaneous attack from multiple directions: Arctic, Atlantic, and ICBM launch.",
    objectives=[
        "Defend against 3 attack vectors simultaneously",
        "Arctic bomber stream (6 bombers)",
        "Atlantic cruise missiles (4 missiles)",
        "ICBM launch (2 missiles, time critical)",
        "Coordinate defense across all vectors"
    ],
    initial_tracks=12,
    spawn_rate=2.0,
    duration=600,
    success_criteria={
        "icbms_intercepted": 2,      # CRITICAL
        "cruise_missiles_intercepted": 3,  # 75%+
        "bombers_intercepted": 4,    # 66%+
        "coordination_bonus": True   # Engage all vectors within 5 min
    },
    special_conditions=["multi_vector", "time_critical", "coordination"],
    briefing="""
TRAINING SCENARIO 008: DOOMSDAY

SITUATION:
MAXIMUM THREAT LEVEL!
Coordinated attack from multiple vectors:

VECTOR 1 (North): 6 bombers from Arctic, 40K ft, 500 kts
VECTOR 2 (East): 4 cruise missiles from Atlantic, 5K ft, 600 kts  
VECTOR 3 (ICBM): 2 ballistic missiles, 65K ft, Mach 2+

YOUR TASK:
1. PRIORITY 1: ICBMs (time critical! <2 min each)
2. PRIORITY 2: Cruise missiles (fast, low altitude)
3. PRIORITY 3: Bombers (slower, more time)
4. Use pan controls to see all vectors
5. Work FAST - coordinate defense

SUCCESS:
Both ICBMs down, 3+ cruise missiles down, 4+ bombers down.

THIS IS THE FINAL EXAM. Everything you've learned applies here!
"""
)


SCENARIO_EXPERT_SPOOF_ATTACK = Scenario(
    id="expert_003",
    name="Spoof & Decoy Attack",
    tier=ScenarioTier.EXPERT,
    description="Enemy using decoys that mimic real bombers. Identify and engage only real targets.",
    objectives=[
        "Identify real bombers vs decoys",
        "Decoys: lower altitude, erratic movement, slower",
        "Real bombers: high altitude, steady course, formation",
        "Engage 6 real bombers, ignore 10 decoys"
    ],
    initial_tracks=16,  # 6 real + 10 decoys
    spawn_rate=0.5,
    duration=900,
    success_criteria={
        "real_bombers_hit": 6,
        "decoys_ignored": 10,
        "accuracy": 100  # 6/6, no decoy hits
    },
    special_conditions=["decoys", "identification"],
    briefing="""
TRAINING SCENARIO 009: DECOY SWARM

SITUATION:
DECEPTION ATTACK in progress!
16 contacts detected: mix of real bombers and decoys.

REAL BOMBERS:
- Altitude: 35-45K ft (S9/S10 filters)
- Speed: 500-600 kts (steady)
- Heading: Straight line toward target
- Formation: Tight groups

DECOYS:
- Altitude: 15-25K ft (S9 filter)
- Speed: 300-400 kts (erratic)
- Heading: Wandering/zigzag
- Formation: Random

YOUR TASK:
1. Use altitude filter S10 (>30K ft) to isolate high-altitude targets
2. Watch Track Detail panel: speed should be 500-600 kts
3. Use FLIGHT PATHS (S20) to see steady vs erratic movement
4. Engage ONLY confirmed real bombers

SUCCESS:
All 6 real bombers neutralized, ZERO decoys engaged (100% accuracy).

TIP: Patience! Observe movement before engaging!
"""
)


# ==========================================
# SCENARIO REGISTRY
# ==========================================

ALL_SCENARIOS = [
    # Tier 1: Basic
    SCENARIO_BASIC_SINGLE_BOMBER,
    SCENARIO_BASIC_MISSILE_DEFENSE,
    
    # Tier 2: Intermediate
    SCENARIO_INTER_MIXED_TRAFFIC,
    SCENARIO_INTER_BOMBER_STREAM,
    
    # Tier 3: Advanced
    SCENARIO_ADV_HIGH_DENSITY,
    SCENARIO_ADV_LAYERED_DEFENSE,
    
    # Tier 4: Expert
    SCENARIO_EXPERT_ELECTRONIC_WARFARE,
    SCENARIO_EXPERT_COORDINATED_ATTACK,
    SCENARIO_EXPERT_SPOOF_ATTACK,
]


def get_scenarios_by_tier(tier: ScenarioTier) -> List[Scenario]:
    """Get all scenarios for a difficulty tier"""
    return [s for s in ALL_SCENARIOS if s.tier == tier]


def get_scenario_by_id(scenario_id: str) -> Scenario:
    """Get scenario by ID"""
    for scenario in ALL_SCENARIOS:
        if scenario.id == scenario_id:
            return scenario
    return None


# Reflex component for scenario selection menu
def scenario_menu() -> rx.Component:
    """
    Scenario selection menu grouped by difficulty tier
    """
    return rx.box(
        rx.vstack(
            rx.heading("SELECT SCENARIO", size="6", color="#00ff00"),
            
            # Basic tier
            rx.text("TIER 1: BASIC", color="#00ff88", font_weight="bold"),
            rx.vstack(
                *[scenario_button(s) for s in get_scenarios_by_tier(ScenarioTier.BASIC)],
                spacing="2"
            ),
            
            # Intermediate tier
            rx.text("TIER 2: INTERMEDIATE", color="#ffff00", font_weight="bold"),
            rx.vstack(
                *[scenario_button(s) for s in get_scenarios_by_tier(ScenarioTier.INTERMEDIATE)],
                spacing="2"
            ),
            
            # Advanced tier
            rx.text("TIER 3: ADVANCED", color="#ff8800", font_weight="bold"),
            rx.vstack(
                *[scenario_button(s) for s in get_scenarios_by_tier(ScenarioTier.ADVANCED)],
                spacing="2"
            ),
            
            # Expert tier
            rx.text("TIER 4: EXPERT", color="#ff0000", font_weight="bold"),
            rx.vstack(
                *[scenario_button(s) for s in get_scenarios_by_tier(ScenarioTier.EXPERT)],
                spacing="2"
            ),
            
            spacing="4"
        ),
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        padding="20px",
        max_height="600px",
        overflow_y="auto"
    )


def scenario_button(scenario: Scenario) -> rx.Component:
    """Button for loading a scenario"""
    tier_colors = {
        ScenarioTier.BASIC: "#00ff88",
        ScenarioTier.INTERMEDIATE: "#ffff00",
        ScenarioTier.ADVANCED: "#ff8800",
        ScenarioTier.EXPERT: "#ff0000"
    }
    
    return rx.button(
        rx.hstack(
            rx.text(scenario.name, font_weight="bold"),
            rx.spacer(),
            rx.badge(
                scenario.tier.value.upper(),
                color_scheme="gray",
                style={"background": tier_colors[scenario.tier] + "22"}
            ),
            width="100%"
        ),
        width="100%",
        variant="soft",
        color_scheme="gray",
        on_click=lambda: [],  # TODO: Wire to load_scenario(scenario.id)
        style={
            "font_family": "Courier New",
            "border": f"1px solid {tier_colors[scenario.tier]}"
        }
    )


def scenario_briefing(scenario: Scenario) -> rx.Component:
    """Display scenario briefing before start"""
    return rx.box(
        rx.vstack(
            rx.heading(scenario.name, size="7", color="#ffff00"),
            rx.badge(f"TIER: {scenario.tier.value.upper()}", size="2", color_scheme="yellow"),
            
            rx.text("BRIEFING", color="#00ff88", font_weight="bold", margin_top="20px"),
            rx.text(
                scenario.briefing,
                font_family="Courier New",
                font_size="12px",
                color="#00ff00",
                white_space="pre-wrap"
            ),
            
            rx.text("OBJECTIVES", color="#00ff88", font_weight="bold", margin_top="20px"),
            rx.vstack(
                *[rx.text(f"• {obj}", color="#00ff00") for obj in scenario.objectives],
                align_items="start",
                spacing="1"
            ),
            
            rx.hstack(
                rx.button(
                    "START SCENARIO",
                    size="3",
                    color_scheme="green",
                    on_click=lambda: [],  # TODO: Wire to start_scenario()
                    style={"font_family": "Courier New"}
                ),
                rx.button(
                    "CANCEL",
                    size="3",
                    variant="soft",
                    color_scheme="gray",
                    on_click=lambda: [],  # TODO: Wire to close_briefing()
                    style={"font_family": "Courier New"}
                ),
                margin_top="20px",
                spacing="4"
            ),
            
            spacing="3"
        ),
        background="#000000",
        border="3px solid #ffff00",
        border_radius="8px",
        padding="30px",
        max_width="800px"
    )
