"""
Operator Goal Flow - Unified Workflow

Requirement #1: Operator Goal Flow

Complete task flow in single screen:
DETECT → INSPECT → DESIGNATE → ASSIGN INTERCEPT → CONFIRM

User stays on main screen from radar contact to intercept launch.
All actions accessible without mode changes or screen navigation.
"""

import reflex as rx
from typing import Optional
from dataclasses import dataclass


@dataclass
class OperatorWorkflowState:
    """
    Current state in the operator workflow
    Tracks progression through detect → intercept cycle
    """
    current_step: str = "detect"  # detect, inspect, designate, assign, confirm
    selected_track_id: str = ""
    selected_track_data: dict = None
    intercept_ready: bool = False
    interceptor_id: str = ""
    action_locked: bool = False  # Prevent accidental double-clicks


# Workflow steps with descriptions
WORKFLOW_STEPS = {
    "detect": {
        "label": "1. DETECT",
        "color": "#ffffff",
        "instruction": "Watch radar scope for new contacts (pulsing white)",
        "action": "Wait for radar contact",
        "icon": "⊕"
    },
    "inspect": {
        "label": "2. INSPECT",
        "color": "#00ff88",
        "instruction": "Press 'D' key → Click target to view details",
        "action": "Select track with light gun",
        "icon": "◎"
    },
    "designate": {
        "label": "3. DESIGNATE",
        "color": "#ffff00",
        "instruction": "Review Track Detail panel → Confirm threat",
        "action": "Verify target is hostile",
        "icon": "◉"
    },
    "assign": {
        "label": "4. ASSIGN INTERCEPT",
        "color": "#00ffff",
        "instruction": "Click 'LAUNCH INTERCEPT' button",
        "action": "Dispatch interceptor",
        "icon": "⚡"
    },
    "confirm": {
        "label": "5. CONFIRM",
        "color": "#00ff00",
        "instruction": "Watch blue interceptor close on target",
        "action": "Monitor intercept progress",
        "icon": "✓"
    }
}


def workflow_progress_bar(current_step: str) -> rx.Component:
    """
    Visual progress bar showing current position in workflow
    Always visible at top of main screen
    """
    steps = ["detect", "inspect", "designate", "assign", "confirm"]
    current_index = steps.index(current_step) if current_step in steps else 0
    
    return rx.hstack(
        *[
            workflow_step_indicator(
                step=step,
                is_current=(step == current_step),
                is_complete=(steps.index(step) < current_index)
            )
            for step in steps
        ],
        spacing="3",
        width="100%",
        padding="10px",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px"
    )


def workflow_step_indicator(step: str, is_current: bool, is_complete: bool) -> rx.Component:
    """Single step in the workflow progress bar"""
    step_info = WORKFLOW_STEPS[step]
    
    # Determine style based on state
    if is_complete:
        color = "#00ff00"
        opacity = 0.5
        icon = "✓"
    elif is_current:
        color = step_info["color"]
        opacity = 1.0
        icon = step_info["icon"]
    else:
        color = "#444444"
        opacity = 0.3
        icon = step_info["icon"]
    
    return rx.vstack(
        # Icon
        rx.text(
            icon,
            font_size="24px",
            color=color,
            style={"opacity": opacity}
        ),
        
        # Label
        rx.text(
            step_info["label"],
            font_family="Courier New",
            font_size="11px",
            font_weight="bold" if is_current else "normal",
            color=color,
            style={"opacity": opacity}
        ),
        
        # Current step gets pulsing border
        rx.cond(
            is_current,
            rx.box(
                width="100%",
                height="3px",
                background=color,
                border_radius="2px",
                style={
                    "animation": "pulse 1s ease-in-out infinite",
                    "@keyframes pulse": {
                        "0%, 100%": {"opacity": 1},
                        "50%": {"opacity": 0.3}
                    }
                }
            )
        ),
        
        align_items="center",
        spacing="1",
        flex="1"
    )


def unified_action_panel(workflow_state: OperatorWorkflowState) -> rx.Component:
    """
    Fixed action panel showing current workflow step and available actions
    Always in same position on screen (right side)
    """
    current_step_info = WORKFLOW_STEPS[workflow_state.current_step]
    
    return rx.box(
        rx.vstack(
            # Current step header
            rx.hstack(
                rx.text(
                    current_step_info["icon"],
                    font_size="32px",
                    color=current_step_info["color"]
                ),
                rx.vstack(
                    rx.heading(
                        current_step_info["label"],
                        size="5",
                        color=current_step_info["color"]
                    ),
                    rx.text(
                        current_step_info["instruction"],
                        font_family="Courier New",
                        font_size="12px",
                        color="#00ff88"
                    ),
                    align_items="start",
                    spacing="1"
                ),
                spacing="3",
                width="100%"
            ),
            
            rx.divider(border_color="#00ff00"),
            
            # Step-specific content
            rx.cond(
                workflow_state.current_step == "detect",
                detect_content()
            ),
            rx.cond(
                workflow_state.current_step == "inspect",
                inspect_content(workflow_state)
            ),
            rx.cond(
                workflow_state.current_step == "designate",
                designate_content(workflow_state)
            ),
            rx.cond(
                workflow_state.current_step == "assign",
                assign_content(workflow_state)
            ),
            rx.cond(
                workflow_state.current_step == "confirm",
                confirm_content(workflow_state)
            ),
            
            spacing="4",
            width="100%"
        ),
        background="#000000",
        border="3px solid #00ff00",
        border_radius="8px",
        padding="20px",
        width="350px",
        min_height="400px"
    )


def detect_content() -> rx.Component:
    """Content for DETECT step"""
    return rx.vstack(
        rx.text(
            "RADAR MONITORING",
            font_weight="bold",
            color="#00ff00"
        ),
        rx.text(
            "New contacts appear as pulsing white dots.",
            font_size="12px",
            color="#888888"
        ),
        rx.text(
            "Wait for track correlation...",
            font_size="12px",
            color="#00ff88",
            font_style="italic"
        ),
        
        # Live track count
        rx.box(
            rx.vstack(
                rx.text("ACTIVE CONTACTS", font_size="10px", color="#888888"),
                rx.text("--", font_size="32px", color="#00ff00", font_family="Courier New"),
                spacing="0"
            ),
            padding="15px",
            background="#001100",
            border="1px solid #00ff00",
            border_radius="4px",
            text_align="center",
            margin_top="20px"
        ),
        
        rx.text(
            "Press 'D' key when ready to inspect a contact.",
            font_size="11px",
            color="#ffff88",
            margin_top="20px",
            padding="10px",
            background="#222200",
            border_radius="4px"
        ),
        
        align_items="start",
        spacing="3",
        width="100%"
    )


def inspect_content(workflow_state: OperatorWorkflowState) -> rx.Component:
    """Content for INSPECT step"""
    return rx.vstack(
        rx.text(
            "LIGHT GUN ACTIVE",
            font_weight="bold",
            color="#00ff88"
        ),
        
        rx.box(
            rx.text(
                "⊕",
                font_size="48px",
                color="#00ff88"
            ),
            text_align="center",
            padding="20px",
            background="#001100",
            border="2px solid #00ff88",
            border_radius="8px",
            margin="10px 0"
        ),
        
        rx.text(
            "Click on any radar contact to inspect.",
            font_size="12px",
            color="#888888"
        ),
        
        rx.cond(
            workflow_state.selected_track_id != "",
            rx.vstack(
                rx.text("SELECTED:", font_size="10px", color="#888888"),
                rx.text(
                    workflow_state.selected_track_id,
                    font_size="18px",
                    color="#ffff00",
                    font_family="Courier New"
                ),
                rx.button(
                    "VIEW DETAILS →",
                    size="2",
                    color_scheme="yellow",
                    on_click=lambda: [],  # TODO: Advance to designate
                    style={"font_family": "Courier New"}
                ),
                spacing="2",
                padding="15px",
                background="#222200",
                border="1px solid #ffff00",
                border_radius="4px",
                margin_top="10px"
            )
        ),
        
        rx.text(
            "Press ESC to cancel selection",
            font_size="10px",
            color="#888888",
            font_style="italic",
            margin_top="20px"
        ),
        
        align_items="start",
        spacing="3",
        width="100%"
    )


def designate_content(workflow_state: OperatorWorkflowState) -> rx.Component:
    """Content for DESIGNATE step - shows track details"""
    return rx.vstack(
        rx.text(
            "TRACK DETAIL",
            font_weight="bold",
            color="#ffff00"
        ),
        
        # Track information card
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("TRACK ID:", color="#888888", font_size="11px"),
                    rx.text(
                        workflow_state.selected_track_id,
                        color="#ffff00",
                        font_family="Courier New",
                        font_weight="bold"
                    ),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("TYPE:", color="#888888", font_size="11px"),
                    rx.badge(
                        "HOSTILE",  # TODO: Real track type
                        color_scheme="red"
                    ),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("ALTITUDE:", color="#888888", font_size="11px"),
                    rx.text("40,000 ft", color="#00ff00", font_family="Courier New"),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("SPEED:", color="#888888", font_size="11px"),
                    rx.text("550 kts", color="#00ff00", font_family="Courier New"),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("HEADING:", color="#888888", font_size="11px"),
                    rx.text("180°", color="#00ff00", font_family="Courier New"),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("THREAT:", color="#888888", font_size="11px"),
                    rx.badge("HIGH", color_scheme="red", size="2"),
                    justify="between",
                    width="100%"
                ),
                spacing="2",
                width="100%"
            ),
            padding="15px",
            background="#110000",
            border="2px solid #ff0000",
            border_radius="4px"
        ),
        
        # Confirmation question
        rx.text(
            "CONFIRM HOSTILE TARGET?",
            font_weight="bold",
            color="#ff0000",
            margin_top="20px"
        ),
        
        # Action buttons
        rx.hstack(
            rx.button(
                "✓ CONFIRM",
                size="3",
                color_scheme="red",
                on_click=lambda: [],  # TODO: Advance to assign
                style={"font_family": "Courier New", "flex": 1}
            ),
            rx.button(
                "✗ CANCEL",
                size="3",
                variant="soft",
                color_scheme="gray",
                on_click=lambda: [],  # TODO: Back to inspect
                style={"font_family": "Courier New", "flex": 1}
            ),
            spacing="3",
            width="100%"
        ),
        
        align_items="start",
        spacing="3",
        width="100%"
    )


def assign_content(workflow_state: OperatorWorkflowState) -> rx.Component:
    """Content for ASSIGN step - launch interceptor"""
    return rx.vstack(
        rx.text(
            "INTERCEPT ASSIGNMENT",
            font_weight="bold",
            color="#00ffff"
        ),
        
        # Target summary
        rx.box(
            rx.vstack(
                rx.text("TARGET", font_size="10px", color="#888888"),
                rx.text(
                    workflow_state.selected_track_id,
                    font_size="24px",
                    color="#ff0000",
                    font_family="Courier New"
                ),
                spacing="0"
            ),
            padding="15px",
            background="#110000",
            border="2px solid #ff0000",
            border_radius="4px",
            text_align="center"
        ),
        
        # Launch button (BIG and obvious)
        rx.button(
            rx.vstack(
                rx.text("⚡", font_size="48px"),
                rx.text(
                    "LAUNCH INTERCEPT",
                    font_size="18px",
                    font_weight="bold"
                ),
                spacing="1"
            ),
            size="4",
            color_scheme="cyan",
            width="100%",
            padding="30px",
            on_click=lambda: [],  # TODO: Launch interceptor
            disabled=workflow_state.action_locked,
            style={
                "font_family": "Courier New",
                "cursor": "pointer" if not workflow_state.action_locked else "not-allowed"
            }
        ),
        
        # Warning
        rx.text(
            "⚠ This action cannot be undone",
            font_size="11px",
            color="#ffff00",
            font_style="italic",
            text_align="center"
        ),
        
        # Cancel option
        rx.button(
            "CANCEL",
            size="2",
            variant="soft",
            color_scheme="gray",
            width="100%",
            on_click=lambda: [],  # TODO: Back to designate
            style={"font_family": "Courier New"}
        ),
        
        align_items="center",
        spacing="4",
        width="100%"
    )


def confirm_content(workflow_state: OperatorWorkflowState) -> rx.Component:
    """Content for CONFIRM step - monitor intercept"""
    return rx.vstack(
        rx.text(
            "INTERCEPT IN PROGRESS",
            font_weight="bold",
            color="#00ff00"
        ),
        
        # Interceptor info
        rx.box(
            rx.vstack(
                rx.text("INTERCEPTOR", font_size="10px", color="#888888"),
                rx.text(
                    workflow_state.interceptor_id,
                    font_size="20px",
                    color="#00ffff",
                    font_family="Courier New"
                ),
                rx.text("→", font_size="24px", color="#888888"),
                rx.text("TARGET", font_size="10px", color="#888888"),
                rx.text(
                    workflow_state.selected_track_id,
                    font_size="20px",
                    color="#ff0000",
                    font_family="Courier New"
                ),
                spacing="2"
            ),
            padding="20px",
            background="#001111",
            border="2px solid #00ffff",
            border_radius="4px",
            text_align="center"
        ),
        
        # Status
        rx.text(
            "Monitoring intercept progress...",
            font_size="12px",
            color="#00ff88",
            font_style="italic"
        ),
        
        # Progress indicator (would animate)
        rx.progress(
            value=50,  # TODO: Real progress
            color_scheme="cyan",
            width="100%"
        ),
        
        # Time to intercept
        rx.box(
            rx.vstack(
                rx.text("TIME TO INTERCEPT", font_size="10px", color="#888888"),
                rx.text("00:45", font_size="32px", color="#00ffff", font_family="Courier New"),
                spacing="0"
            ),
            padding="15px",
            background="#001100",
            border="1px solid #00ffff",
            border_radius="4px",
            text_align="center",
            margin_top="10px"
        ),
        
        # Reset button
        rx.button(
            "NEW CONTACT",
            size="2",
            color_scheme="green",
            width="100%",
            on_click=lambda: [],  # TODO: Reset to detect
            style={"font_family": "Courier New"},
            margin_top="20px"
        ),
        
        align_items="center",
        spacing="3",
        width="100%"
    )


# CSS for workflow animations
WORKFLOW_CSS = """
<style>
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px currentColor; }
    50% { box-shadow: 0 0 20px currentColor; }
}

.workflow-current-step {
    animation: glow 2s ease-in-out infinite;
}
</style>
"""
