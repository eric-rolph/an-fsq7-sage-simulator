"""
Operator Goal Flow - Unified Workflow

Requirement #1: Operator Goal Flow

Complete task flow in single screen:
DETECT → INSPECT → DESIGNATE → ASSIGN INTERCEPT → CONFIRM

User stays on main screen from radar contact to intercept launch.
All actions accessible without mode changes or screen navigation.
"""

import reflex as rx
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from ..state_model import Track
from . import system_messages

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


class OperatorWorkflowStateMixin(rx.State):
    """
    Mixin for InteractiveSageState to handle operator workflow logic.
    Allows parallel tasking by maintaining workflow state on each track.
    """
    
    def advance_workflow(self, track_id: str):
        """Advance the workflow for a specific track to the next step"""
        # This method assumes self.tracks exists (provided by InteractiveSageState)
        for track in self.tracks:
            if track.id == track_id:
                current = track.workflow_step
                if current == "detect":
                    track.workflow_step = "inspect"
                elif current == "inspect":
                    track.workflow_step = "designate"
                elif current == "designate":
                    track.workflow_step = "assign"
                elif current == "assign":
                    # Launch interceptor logic
                    # Find available interceptor
                    # This assumes self.interceptors exists
                    available_interceptor = None
                    if hasattr(self, 'interceptors'):
                        for interceptor in self.interceptors:
                            if interceptor.status == "READY":
                                available_interceptor = interceptor
                                break
                    
                    if available_interceptor:
                        available_interceptor.status = "SCRAMBLING"
                        available_interceptor.assigned_target_id = track.id
                        track.interceptor_assigned = True
                        track.workflow_interceptor_id = available_interceptor.id
                        track.workflow_step = "confirm"
                        
                        # Add system message
                        if hasattr(self, 'system_messages_log'):
                             self.system_messages_log.append(
                                 system_messages.log_intercept_launched(track.id, available_interceptor.id)
                             )
                    else:
                        # No interceptors available - maybe show error?
                        # For now, just advance state but with no interceptor ID (simulation logic might fail)
                        track.workflow_step = "confirm"
                        track.workflow_interceptor_id = "NONE"
                        
                        if hasattr(self, 'system_messages_log'):
                             self.system_messages_log.append(
                                 system_messages.log_warning(f"No interceptors available for {track.id}")
                             )

                # confirm is the last step
                return

    def reset_workflow(self, track_id: str):
        """Reset workflow for a track (e.g. if lost or re-evaluated)"""
        for track in self.tracks:
            if track.id == track_id:
                track.workflow_step = "detect"
                track.workflow_interceptor_id = ""
                return

    def confirm_hostile(self, track_id: str):
        """Operator confirms track is hostile"""
        for track in self.tracks:
            if track.id == track_id:
                track.workflow_step = "assign"
                # Also update the track classification if needed
                if track.track_type == "unknown":
                    track.track_type = "hostile"  # Operator judgment
                    track.threat_level = "HIGH"
                return

    def cancel_designation(self, track_id: str):
        """Operator cancels designation, goes back to inspect"""
        for track in self.tracks:
            if track.id == track_id:
                track.workflow_step = "inspect"
                return


def workflow_progress_bar(current_step: str) -> rx.Component:
    """
    Visual progress bar showing current position in workflow
    Always visible at top of main screen
    """
    steps = ["detect", "inspect", "designate", "assign", "confirm"]
    
    def is_step_complete(step_name):
        # A step is complete if the current_step is one of the subsequent steps
        step_index = steps.index(step_name)
        subsequent_steps = steps[step_index+1:]
        if not subsequent_steps:
            return False
        
        # Build OR condition: current_step == next1 | current_step == next2 ...
        condition = (current_step == subsequent_steps[0])
        for s in subsequent_steps[1:]:
            condition = condition | (current_step == s)
        return condition

    return rx.hstack(
        *[
            workflow_step_indicator(
                step=step,
                is_current=(current_step == step),
                is_complete=is_step_complete(step)
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
    
    # Determine style based on state using rx.cond for Vars
    color = rx.cond(
        is_complete,
        "#00ff00",
        rx.cond(is_current, step_info["color"], "#444444")
    )
    
    opacity = rx.cond(
        is_complete,
        0.5,
        rx.cond(is_current, 1.0, 0.3)
    )
    
    icon = rx.cond(
        is_complete,
        "✓",
        step_info["icon"]
    )
    
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
            font_weight=rx.cond(is_current, "bold", "normal"),
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


def unified_action_panel(track: Optional[Track], state_class) -> rx.Component:
    """
    Fixed action panel showing current workflow step and available actions
    Always in same position on screen (right side)
    
    Args:
        track: The currently selected track (can be None)
        state_class: The main state class (InteractiveSageState) to bind events to
    """
    # If no track selected, we are in DETECT mode
    current_step = rx.cond(track != None, track.workflow_step, "detect")
    
    # We need to access properties of the step info dynamically based on current_step
    # But rx.cond is better for high-level switching
    
    return rx.box(
        rx.vstack(
            # Header is dynamic based on step
            rx.cond(
                track == None,
                # DETECT Header
                _step_header("detect"),
                # Track-specific Header
                rx.match(
                    track.workflow_step,
                    ("inspect", _step_header("inspect")),
                    ("designate", _step_header("designate")),
                    ("assign", _step_header("assign")),
                    ("confirm", _step_header("confirm")),
                    _step_header("detect") # Fallback
                )
            ),
            
            rx.divider(border_color="#00ff00"),
            
            # Step-specific content
            rx.cond(
                track == None,
                detect_content(),
                rx.match(
                    track.workflow_step,
                    ("inspect", inspect_content(track, state_class)),
                    ("designate", designate_content(track, state_class)),
                    ("assign", assign_content(track, state_class)),
                    ("confirm", confirm_content(track, state_class)),
                    detect_content() # Fallback
                )
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


def _step_header(step_name: str) -> rx.Component:
    """Helper to render header for a specific step"""
    # We can't easily use WORKFLOW_STEPS[step_name] inside rx.cond/match if step_name is a Var
    # But here step_name is a python string because we call this from python logic inside rx.match
    
    info = WORKFLOW_STEPS[step_name]
    return rx.hstack(
        rx.text(
            info["icon"],
            font_size="32px",
            color=info["color"]
        ),
        rx.vstack(
            rx.heading(
                info["label"],
                size="5",
                color=info["color"]
            ),
            rx.text(
                info["instruction"],
                font_family="Courier New",
                font_size="12px",
                color="#00ff88"
            ),
            align_items="start",
            spacing="1"
        ),
        spacing="3",
        width="100%"
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


def inspect_content(track: Track, state_class) -> rx.Component:
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
        
        rx.vstack(
            rx.text("SELECTED:", font_size="10px", color="#888888"),
            rx.text(
                track.id,
                font_size="18px",
                color="#ffff00",
                font_family="Courier New"
            ),
            rx.button(
                "VIEW DETAILS →",
                size="2",
                color_scheme="yellow",
                on_click=lambda: state_class.advance_workflow(track.id),
                style={"font_family": "Courier New"}
            ),
            spacing="2",
            padding="15px",
            background="#222200",
            border="1px solid #ffff00",
            border_radius="4px",
            margin_top="10px",
            width="100%"
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


def designate_content(track: Track, state_class) -> rx.Component:
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
                        track.id,
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
                        track.track_type.upper(),
                        color_scheme=rx.cond(track.track_type == "hostile", "red", "green")
                    ),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("ALTITUDE:", color="#888888", font_size="11px"),
                    rx.text(f"{track.altitude} ft", color="#00ff00", font_family="Courier New"),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("SPEED:", color="#888888", font_size="11px"),
                    rx.text(f"{track.speed} kts", color="#00ff00", font_family="Courier New"),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("HEADING:", color="#888888", font_size="11px"),
                    rx.text(f"{track.heading}°", color="#00ff00", font_family="Courier New"),
                    justify="between",
                    width="100%"
                ),
                rx.hstack(
                    rx.text("THREAT:", color="#888888", font_size="11px"),
                    rx.badge(track.threat_level, color_scheme="red", size="2"),
                    justify="between",
                    width="100%"
                ),
                spacing="2",
                width="100%"
            ),
            padding="15px",
            background="#110000",
            border="2px solid #ff0000",
            border_radius="4px",
            width="100%"
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
                on_click=lambda: state_class.confirm_hostile(track.id),
                style={"font_family": "Courier New", "flex": 1}
            ),
            rx.button(
                "✗ CANCEL",
                size="3",
                variant="soft",
                color_scheme="gray",
                on_click=lambda: state_class.cancel_designation(track.id),
                style={"font_family": "Courier New", "flex": 1}
            ),
            spacing="3",
            width="100%"
        ),
        
        align_items="start",
        spacing="3",
        width="100%"
    )


def assign_content(track: Track, state_class) -> rx.Component:
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
                    track.id,
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
            text_align="center",
            width="100%"
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
            on_click=lambda: state_class.advance_workflow(track.id), # TODO: Trigger actual launch logic
            style={
                "font_family": "Courier New",
                "cursor": "pointer"
            }
        ),
        
        # Warning
        rx.text(
            "⚠ This action cannot be undone",
            font_size="11px",
            color="#ffff00",
            font_style="italic",
            text_align="center",
            width="100%"
        ),
        
        # Cancel option
        rx.button(
            "CANCEL",
            size="2",
            variant="soft",
            color_scheme="gray",
            width="100%",
            on_click=lambda: state_class.cancel_designation(track.id),
            style={"font_family": "Courier New"}
        ),
        
        align_items="center",
        spacing="4",
        width="100%"
    )


def confirm_content(track: Track, state_class) -> rx.Component:
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
                    track.workflow_interceptor_id, # This needs to be set during assign
                    font_size="20px",
                    color="#00ffff",
                    font_family="Courier New"
                ),
                rx.text("→", font_size="24px", color="#888888"),
                rx.text("TARGET", font_size="10px", color="#888888"),
                rx.text(
                    track.id,
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
            text_align="center",
            width="100%"
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
            margin_top="10px",
            width="100%"
        ),
        
        # Reset button
        rx.button(
            "NEW CONTACT",
            size="2",
            color_scheme="green",
            width="100%",
            on_click=lambda: state_class.reset_workflow(track.id),
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
