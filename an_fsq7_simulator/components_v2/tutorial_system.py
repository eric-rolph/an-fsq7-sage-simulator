"""
Interactive Tutorial and Mission System

Guides new users through SAGE simulator operations:
- 6 training missions with objectives
- Step-by-step instructions
- Automatic progress checking
- Visual hints and highlights
- Launch automatically on first visit

Transforms the simulator into a self-teaching experience.
"""

import reflex as rx
from typing import List, Dict, Callable
from ..state_model import Mission, MissionStep


# Define 6 training missions
TRAINING_MISSIONS: List[Mission] = [
    Mission(
        id="mission_1",
        title="Power-On and Scope Basics",
        description="Learn to start the computer and understand the radar display",
        steps=[
            MissionStep(
                text="Click the POWER ON button to boot the computer",
                check_condition="system_powered_on",
                hint="Look for the large red POWER ON button in the control panel",
            ),
            MissionStep(
                text="Wait for vacuum tubes to warm up (reaches OPERATIONAL status)",
                check_condition="system_operational",
                hint="Watch the tube count and temperature rise. This takes about 5 seconds.",
            ),
            MissionStep(
                text="Toggle RANGE RINGS overlay on",
                check_condition="overlay_range_rings_active",
                hint="Find the Feature Select panel and press the S22 RANGE RINGS button",
            ),
            MissionStep(
                text="Toggle COASTLINES overlay on",
                check_condition="overlay_coastlines_active",
                hint="Press the S24 COASTLINES button to see geographic context",
            ),
        ],
        reward_message="✓ Mission Complete! You've powered on the SAGE computer and enabled basic overlays.",
    ),
    
    Mission(
        id="mission_2",
        title="Target Selection with Light Gun",
        description="Learn to use the authentic SAGE light gun to select radar targets",
        steps=[
            MissionStep(
                text="Press 'D' key or click ARM LIGHT GUN button",
                check_condition="lightgun_armed",
                hint="The 'D' key arms the light gun. You'll see a crosshair cursor.",
            ),
            MissionStep(
                text="Click on any radar target to select it",
                check_condition="target_selected",
                hint="Click on one of the moving blips on the radar scope. The target will highlight.",
            ),
            MissionStep(
                text="View target details in the Track Detail panel",
                check_condition="target_detail_visible",
                hint="The selected target's altitude, speed, heading, and threat level now display.",
            ),
        ],
        reward_message="✓ Mission Complete! You can now designate targets using the light gun.",
    ),
    
    Mission(
        id="mission_3",
        title="Launch an Intercept",
        description="Identify a hostile target and launch an interceptor missile",
        steps=[
            MissionStep(
                text="Arm the light gun (press 'D')",
                check_condition="lightgun_armed",
                hint="Press the 'D' key to activate target selection mode.",
            ),
            MissionStep(
                text="Select a HOSTILE target (red colored)",
                check_condition="hostile_target_selected",
                hint="Look for red targets on the scope. These are threats that need to be intercepted.",
            ),
            MissionStep(
                text="Click LAUNCH INTERCEPT button",
                check_condition="intercept_launched",
                hint="The LAUNCH INTERCEPT button appears in the Track Detail panel when a hostile is selected.",
            ),
            MissionStep(
                text="Watch the intercept missile track toward the target",
                check_condition="intercept_success",
                hint="The interceptor will appear as a blue track homing in on the hostile. Wait for impact.",
            ),
        ],
        reward_message="✓ Mission Complete! Target eliminated. You've successfully protected your sector.",
    ),
    
    Mission(
        id="mission_4",
        title="Console Filter Operations",
        description="Use SD Console buttons to filter and organize the radar display",
        steps=[
            MissionStep(
                text="Press S4 to show HOSTILE targets only",
                check_condition="filter_hostile_active",
                hint="In the Category Select panel, click the S4 HOSTILE button. All friendly tracks will hide.",
            ),
            MissionStep(
                text="Press S2 to show FRIENDLY targets only",
                check_condition="filter_friendly_active",
                hint="Click S2 FRIENDLY to switch filters. Now only green (friendly) tracks display.",
            ),
            MissionStep(
                text="Press S1 to show ALL targets again",
                check_condition="filter_all_active",
                hint="Click S1 ALL to clear filters and see the complete air picture.",
            ),
            MissionStep(
                text="Toggle FLIGHT PATHS overlay (S20)",
                check_condition="overlay_flight_paths_active",
                hint="In Feature Select, press S20 to see trailing paths behind each target.",
            ),
        ],
        reward_message="✓ Mission Complete! You can now efficiently filter and view the tactical situation.",
    ),
    
    Mission(
        id="mission_5",
        title="Vacuum Tube Maintenance",
        description="Replace failed vacuum tubes to maintain system performance",
        steps=[
            MissionStep(
                text="Wait for a tube to fail (or skip forward)",
                check_condition="tube_failure_detected",
                hint="Tubes fail randomly over time. Failed tubes blink red with an ✗ symbol.",
            ),
            MissionStep(
                text="Click on the failed tube in the Tube Rack",
                check_condition="tube_selected_for_replacement",
                hint="Failed tubes are marked in red. Click one to open the replacement dialog.",
            ),
            MissionStep(
                text="Click REPLACE TUBE button",
                check_condition="tube_replacement_started",
                hint="Confirm the replacement. The system will pull the old tube and insert a new one.",
            ),
            MissionStep(
                text="Wait for new tube to warm up",
                check_condition="tube_replacement_complete",
                hint="New tubes glow blue while warming up (5 seconds). System performance will improve.",
            ),
        ],
        reward_message="✓ Mission Complete! You've mastered tube maintenance. Keep those tubes healthy!",
    ),
    
    Mission(
        id="mission_6",
        title="CPU Program Execution",
        description="Load and run a CPU program, and view its execution trace",
        steps=[
            MissionStep(
                text="Select a program from the dropdown",
                check_condition="program_selected",
                hint="In the CPU Core panel, click the Program Select dropdown and choose 'Array Sum (Authentic)'.",
            ),
            MissionStep(
                text="Click LOAD PROGRAM button",
                check_condition="program_loaded",
                hint="The LOAD PROGRAM button loads the selected program into memory.",
            ),
            MissionStep(
                text="Click RUN button to execute",
                check_condition="program_running",
                hint="The RUN button starts program execution. Watch the Execution Trace panel.",
            ),
            MissionStep(
                text="View the final result in the trace panel",
                check_condition="program_complete",
                hint="The trace shows each instruction executed and the final computed result.",
            ),
        ],
        reward_message="✓ Mission Complete! You can now run CPU programs and understand their output.",
    ),
]


def mission_step_indicator(step: MissionStep, index: int, is_current: bool, is_complete: bool) -> rx.Component:
    """
    Visual indicator for a single mission step
    """
    if is_complete:
        icon = "✓"
        color = "#00ff00"
        bg = "#002200"
    elif is_current:
        icon = "→"
        color = "#ffff00"
        bg = "#332200"
    else:
        icon = f"{index + 1}"
        color = "#666666"
        bg = "#111111"
    
    return rx.box(
        rx.hstack(
            # Step number/icon
            rx.box(
                rx.text(
                    icon,
                    font_size="1.2rem",
                    font_weight="bold",
                    color=color,
                ),
                width="30px",
                height="30px",
                display="flex",
                align_items="center",
                justify_content="center",
                background=bg,
                border=f"2px solid {color}",
                border_radius="4px",
            ),
            
            # Step text
            rx.vstack(
                rx.text(
                    step.text,
                    color=color if is_current else "#888888",
                    font_size="0.9rem",
                    font_weight="bold" if is_current else "normal",
                ),
                rx.cond(
                    is_current and step.hint,
                    rx.text(
                        f"💡 Hint: {step.hint}",
                        color="#88ff88",
                        font_size="0.8rem",
                        font_style="italic",
                        margin_top="0.25rem",
                    ),
                    rx.box(),
                ),
                spacing="0",
                align_items="start",
                flex="1",
            ),
            
            spacing="3",
            width="100%",
            align_items="start",
        ),
        
        padding="0.75rem",
        background=bg if is_current else "transparent",
        border_left=f"3px solid {color}" if is_current else "3px solid transparent",
        border_radius="4px",
        transition="all 0.3s",
    )


def mission_progress_bar(current_step: int, total_steps: int) -> rx.Component:
    """Progress bar for mission completion"""
    progress = (current_step / total_steps) * 100 if total_steps > 0 else 0
    
    return rx.box(
        rx.box(
            width=f"{progress}%",
            height="100%",
            background="linear-gradient(90deg, #00ff00, #88ff00)",
            border_radius="4px",
            transition="width 0.5s ease",
        ),
        width="100%",
        height="8px",
        background="#111111",
        border="1px solid #003300",
        border_radius="4px",
        overflow="hidden",
        margin_bottom="0.5rem",
    )


def mission_panel(mission: Mission, current_step_index: int, completed_steps: List[int]) -> rx.Component:
    """
    Tutorial mission panel showing objectives and progress
    """
    is_complete = current_step_index >= len(mission.steps)
    
    return rx.box(
        # Header
        rx.hstack(
            rx.heading(
                f"MISSION {mission.id.split('_')[1]}",
                size="4",
                color="#00ff00",
                font_family="'Courier New', monospace",
            ),
            rx.badge(
                "COMPLETE" if is_complete else "IN PROGRESS",
                color_scheme="green" if is_complete else "yellow",
            ),
            justify="between",
            width="100%",
            margin_bottom="0.5rem",
        ),
        
        # Mission title and description
        rx.box(
            rx.text(
                mission.title,
                font_size="1.1rem",
                font_weight="bold",
                color="#88ff88",
                margin_bottom="0.25rem",
            ),
            rx.text(
                mission.description,
                font_size="0.85rem",
                color="#888888",
                font_style="italic",
            ),
            margin_bottom="1rem",
        ),
        
        # Progress bar
        mission_progress_bar(len(completed_steps), len(mission.steps)),
        
        # Steps list
        rx.vstack(
            *[
                mission_step_indicator(
                    step,
                    idx,
                    is_current=(idx == current_step_index),
                    is_complete=(idx in completed_steps),
                )
                for idx, step in enumerate(mission.steps)
            ],
            spacing="2",
            width="100%",
            margin_bottom="1rem",
        ),
        
        # Completion message
        rx.cond(
            is_complete,
            rx.box(
                rx.text(
                    mission.reward_message,
                    color="#00ff00",
                    font_size="1.1rem",
                    font_weight="bold",
                    text_align="center",
                ),
                padding="1rem",
                background="#002200",
                border="2px solid #00ff00",
                border_radius="4px",
                margin_bottom="1rem",
            ),
            rx.box(),
        ),
        
        # Navigation buttons
        rx.hstack(
            rx.button(
                "← Previous Mission",
                on_click=lambda: None,  # TODO: Wire to previous_mission
                background="#003300",
                color="#00ff00",
                border="1px solid #00ff00",
                size="2",
                disabled=(mission.id == "mission_1"),
                _hover={"background": "#005500"},
            ),
            rx.button(
                "Next Mission →" if not is_complete else "✓ Continue",
                on_click=lambda: None,  # TODO: Wire to next_mission
                background="#003300",
                color="#00ff00",
                border="1px solid #00ff00",
                size="2",
                _hover={"background": "#005500"},
            ),
            rx.button(
                "Skip Tutorial",
                on_click=lambda: None,  # TODO: Wire to skip_tutorial
                background="#330000",
                color="#ff8888",
                border="1px solid #ff0000",
                size="2",
                _hover={"background": "#550000"},
            ),
            spacing="2",
            justify="between",
            width="100%",
        ),
        
        padding="1.5rem",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        max_width="600px",
    )


def tutorial_sidebar_compact() -> rx.Component:
    """
    Compact tutorial sidebar for main layout
    Shows current objective without taking much space
    """
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text(
                    "?",
                    font_size="1.5rem",
                    font_weight="bold",
                    color="#00ff00",
                ),
                width="30px",
                height="30px",
                display="flex",
                align_items="center",
                justify_content="center",
                background="#003300",
                border="2px solid #00ff00",
                border_radius="50%",
            ),
            rx.vstack(
                rx.text(
                    "TRAINING MISSION 1",
                    font_size="0.75rem",
                    color="#888888",
                    text_transform="uppercase",
                ),
                rx.text(
                    "Click POWER ON to start the computer",
                    font_size="0.9rem",
                    color="#00ff00",
                    font_weight="bold",
                ),
                spacing="0",
                align_items="start",
            ),
            spacing="2",
            width="100%",
        ),
        padding="0.75rem",
        background="#001100",
        border="1px solid #00ff00",
        border_radius="4px",
        cursor="pointer",
        _hover={
            "background": "#002200",
            "border_color": "#00ff00",
        },
        on_click=lambda: None,  # TODO: Wire to open_full_tutorial
    )


def welcome_modal(show: bool) -> rx.Component:
    """
    Welcome modal on first visit
    Offers to start tutorial or skip to operation
    """
    if not show:
        return rx.box()
    
    return rx.box(
        rx.box(
            rx.heading(
                "WELCOME TO AN/FSQ-7 SAGE SIMULATOR",
                size="5",
                color="#00ff00",
                margin_bottom="1rem",
                text_align="center",
                font_family="'Courier New', monospace",
            ),
            
            rx.text(
                "This is a historically accurate simulation of the 1950s SAGE (Semi-Automatic Ground Environment) air defense computer system.",
                color="#88ff88",
                text_align="center",
                margin_bottom="1.5rem",
                line_height="1.6",
            ),
            
            rx.vstack(
                rx.box(
                    rx.text(
                        "🎓 RECOMMENDED FOR NEW OPERATORS:",
                        font_weight="bold",
                        color="#ffff00",
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "Complete 6 interactive training missions to learn:",
                        color="#88ff88",
                        margin_bottom="0.5rem",
                    ),
                    rx.unordered_list(
                        rx.list_item("Power-on procedures and scope basics"),
                        rx.list_item("Light gun target selection"),
                        rx.list_item("Interceptor launch operations"),
                        rx.list_item("Console filter controls"),
                        rx.list_item("Vacuum tube maintenance"),
                        rx.list_item("CPU program execution"),
                        color="#88ff88",
                        spacing="1",
                    ),
                    padding="1rem",
                    background="#001100",
                    border="1px solid #00ff00",
                    border_radius="4px",
                    margin_bottom="1rem",
                ),
                
                rx.hstack(
                    rx.button(
                        "▶ START TRAINING MODE",
                        on_click=lambda: None,  # TODO: Wire to start_tutorial
                        background="#003300",
                        color="#00ff00",
                        border="2px solid #00ff00",
                        size="3",
                        width="100%",
                        _hover={"background": "#005500"},
                    ),
                    rx.button(
                        "SKIP TO OPERATION",
                        on_click=lambda: None,  # TODO: Wire to skip_tutorial
                        background="#111111",
                        color="#888888",
                        border="1px solid #444444",
                        size="3",
                        width="100%",
                        _hover={"background": "#222222", "color": "#ffffff"},
                    ),
                    spacing="3",
                    width="100%",
                ),
                
                spacing="3",
                width="100%",
            ),
            
            max_width="600px",
            padding="2rem",
            background="#000000",
            border="3px solid #00ff00",
            border_radius="8px",
            box_shadow="0 0 40px rgba(0,255,0,0.3)",
        ),
        
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        display="flex",
        align_items="center",
        justify_content="center",
        background="rgba(0,0,0,0.95)",
        z_index="2000",
    )
