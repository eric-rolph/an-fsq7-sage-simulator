"""
Safe Actions & Undo System

Requirement #8: Undo / Safe Actions

For critical actions (assign, launch, delete track), provide:
- Confirmation dialogs
- Undo capability (time-limited)
- Cancel options
- Visual feedback

Prevents mis-click disasters and accidental engagements.
"""

import reflex as rx
from dataclasses import dataclass
from typing import Optional, Callable
from datetime import datetime, timedelta


@dataclass
class PendingAction:
    """Action waiting for confirmation or undo window"""
    action_type: str  # "launch", "delete", "assign", "filter_clear"
    timestamp: float
    description: str
    undo_data: dict  # Data needed to reverse action
    can_undo: bool = True
    undo_expires_at: float = 0.0


# Action types that require confirmation
CRITICAL_ACTIONS = {
    "launch_intercept": {
        "title": "LAUNCH INTERCEPTOR",
        "icon": "⚡",
        "color": "#ff0000",
        "warning": "This will dispatch an interceptor to engage the target.",
        "confirm_text": "CONFIRM LAUNCH",
        "cancel_text": "CANCEL",
        "undo_window": 5.0,  # 5 seconds to undo
        "severity": "high"
    },
    "delete_track": {
        "title": "DELETE TRACK",
        "icon": "✗",
        "color": "#ff00ff",
        "warning": "This will remove the track from the system.",
        "confirm_text": "CONFIRM DELETE",
        "cancel_text": "CANCEL",
        "undo_window": 10.0,  # 10 seconds to undo
        "severity": "medium"
    },
    "clear_all_filters": {
        "title": "CLEAR ALL FILTERS",
        "icon": "⚙",
        "color": "#ffff00",
        "warning": "This will reset all active filters and show all tracks.",
        "confirm_text": "CONFIRM",
        "cancel_text": "CANCEL",
        "undo_window": 5.0,
        "severity": "low"
    },
    "designation_override": {
        "title": "OVERRIDE DESIGNATION",
        "icon": "⚠",
        "color": "#ff8800",
        "warning": "This track is already designated by another operator.",
        "confirm_text": "OVERRIDE",
        "cancel_text": "CANCEL",
        "undo_window": 0.0,  # No undo for overrides
        "severity": "high"
    },
    "friendly_engage": {
        "title": "⚠ FRIENDLY FIRE WARNING ⚠",
        "icon": "⚠",
        "color": "#ff0000",
        "warning": "WARNING: Target is marked as FRIENDLY. Engaging will cause friendly casualty!",
        "confirm_text": "ENGAGE ANYWAY (UNSAFE)",
        "cancel_text": "CANCEL (SAFE)",
        "undo_window": 0.0,  # No undo for friendly fire
        "severity": "critical"
    }
}


def confirmation_dialog(
    action_type: str,
    target_id: str,
    on_confirm: Callable,
    on_cancel: Callable
) -> rx.Component:
    """
    Confirmation dialog for critical actions
    Appears as modal overlay
    """
    action_config = CRITICAL_ACTIONS.get(action_type, CRITICAL_ACTIONS["launch_intercept"])
    
    # Severity colors
    severity_styles = {
        "low": {"bg": "#222200", "border": "#ffff00"},
        "medium": {"bg": "#220022", "border": "#ff00ff"},
        "high": {"bg": "#220000", "border": "#ff8800"},
        "critical": {"bg": "#330000", "border": "#ff0000"}
    }
    style = severity_styles[action_config["severity"]]
    
    return rx.box(
        # Overlay backdrop
        rx.box(
            # Dialog box
            rx.box(
                rx.vstack(
                    # Header with icon
                    rx.hstack(
                        rx.text(
                            action_config["icon"],
                            font_size="48px",
                            color=action_config["color"]
                        ),
                        rx.vstack(
                            rx.heading(
                                action_config["title"],
                                size="6",
                                color=action_config["color"]
                            ),
                            rx.text(
                                f"Target: {target_id}",
                                font_family="Courier New",
                                font_size="14px",
                                color="#00ff88"
                            ),
                            align_items="start",
                            spacing="1"
                        ),
                        spacing="4",
                        width="100%"
                    ),
                    
                    rx.divider(border_color=action_config["color"]),
                    
                    # Warning message
                    rx.box(
                        rx.text(
                            action_config["warning"],
                            font_family="Courier New",
                            font_size="13px",
                            color="#ffff00" if action_config["severity"] != "critical" else "#ff0000",
                            text_align="center"
                        ),
                        padding="20px",
                        background=style["bg"],
                        border=f"2px solid {style['border']}",
                        border_radius="4px"
                    ),
                    
                    # Critical warning for friendly fire
                    rx.cond(
                        action_type == "friendly_engage",
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "⚠ ⚠ ⚠ DANGER ⚠ ⚠ ⚠",
                                    font_weight="bold",
                                    font_size="18px",
                                    color="#ff0000"
                                ),
                                rx.text(
                                    "You are about to engage a FRIENDLY aircraft!",
                                    font_size="14px",
                                    color="#ff0000"
                                ),
                                rx.text(
                                    "This is almost certainly a mistake!",
                                    font_size="12px",
                                    color="#ff8800"
                                ),
                                spacing="2",
                                text_align="center"
                            ),
                            padding="15px",
                            background="#330000",
                            border="3px solid #ff0000",
                            border_radius="4px",
                            style={"animation": "blink-warning 1s step-end infinite"}
                        )
                    ),
                    
                    # Undo info
                    rx.cond(
                        action_config["undo_window"] > 0,
                        rx.text(
                            f"You will have {int(action_config['undo_window'])} seconds to undo this action.",
                            font_size="11px",
                            color="#00ff88",
                            font_style="italic",
                            text_align="center"
                        )
                    ),
                    
                    # Action buttons
                    rx.hstack(
                        rx.button(
                            action_config["cancel_text"],
                            size="4",
                            color_scheme="gray",
                            variant="soft",
                            on_click=on_cancel,
                            style={
                                "font_family": "Courier New",
                                "flex": 1,
                                "font_size": "16px"
                            }
                        ),
                        rx.button(
                            action_config["confirm_text"],
                            size="4",
                            color_scheme="red",
                            on_click=on_confirm,
                            style={
                                "font_family": "Courier New",
                                "flex": 1,
                                "font_size": "16px"
                            }
                        ),
                        spacing="4",
                        width="100%"
                    ),
                    
                    spacing="5",
                    width="100%"
                ),
                background="#000000",
                border=f"4px solid {action_config['color']}",
                border_radius="12px",
                padding="30px",
                max_width="600px",
                box_shadow="0 0 50px rgba(0, 0, 0, 0.9)"
            ),
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            z_index="1000"
        ),
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        background="rgba(0, 0, 0, 0.85)",
        backdrop_filter="blur(5px)",
        z_index="999",
        display="flex",
        align_items="center",
        justify_content="center"
    )


def undo_toast(pending_action: PendingAction, on_undo: Callable) -> rx.Component:
    """
    Undo notification that appears after action is executed
    Shows countdown timer and UNDO button
    """
    return rx.box(
        rx.hstack(
            # Icon and message
            rx.hstack(
                rx.text("✓", font_size="24px", color="#00ff00"),
                rx.vstack(
                    rx.text(
                        "ACTION COMPLETED",
                        font_weight="bold",
                        font_size="12px",
                        color="#00ff00"
                    ),
                    rx.text(
                        pending_action.description,
                        font_size="11px",
                        color="#888888"
                    ),
                    align_items="start",
                    spacing="0"
                ),
                spacing="3"
            ),
            
            # Countdown timer
            rx.cond(
                pending_action.can_undo,
                rx.vstack(
                    rx.text(
                        "UNDO IN",
                        font_size="9px",
                        color="#888888"
                    ),
                    rx.text(
                        "5s",  # TODO: Real countdown
                        font_size="18px",
                        font_weight="bold",
                        color="#ffff00",
                        font_family="Courier New"
                    ),
                    spacing="0",
                    align_items="center"
                )
            ),
            
            # Undo button
            rx.cond(
                pending_action.can_undo,
                rx.button(
                    "UNDO",
                    size="2",
                    color_scheme="yellow",
                    on_click=on_undo,
                    style={
                        "font_family": "Courier New",
                        "font_weight": "bold"
                    }
                )
            ),
            
            justify="between",
            align="center",
            width="100%",
            spacing="4"
        ),
        position="fixed",
        bottom="20px",
        right="20px",
        width="400px",
        padding="15px",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        box_shadow="0 4px 20px rgba(0, 255, 0, 0.3)",
        z_index="900",
        style={
            "animation": "slide-in 0.3s ease-out"
        }
    )


def undo_history_panel(actions: list[PendingAction]) -> rx.Component:
    """
    Panel showing recent actions with undo capability
    Appears in sidebar or as dropdown
    """
    return rx.box(
        rx.vstack(
            rx.heading(
                "ACTION HISTORY",
                size="4",
                color="#00ff00",
                font_family="Courier New"
            ),
            
            rx.divider(border_color="#00ff00"),
            
            # Action list
            rx.vstack(
                rx.foreach(
                    actions,
                    lambda action: undo_history_row(action)
                ),
                spacing="2",
                width="100%",
                max_height="300px",
                overflow_y="auto"
            ),
            
            # Footer
            rx.text(
                f"{len(actions)} recent actions",
                font_size="10px",
                color="#888888",
                margin_top="10px"
            ),
            
            spacing="3",
            width="100%"
        ),
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        padding="15px",
        width="350px"
    )


def undo_history_row(action: PendingAction) -> rx.Component:
    """Single row in undo history"""
    return rx.hstack(
        # Timestamp
        rx.text(
            datetime.fromtimestamp(action.timestamp).strftime("%H:%M:%S"),
            font_family="Courier New",
            font_size="10px",
            color="#888888",
            width="70px",
            flex_shrink="0"
        ),
        
        # Description
        rx.text(
            action.description,
            font_size="11px",
            color="#00ff88",
            flex_grow="1"
        ),
        
        # Undo button (if still available)
        rx.cond(
            action.can_undo and (datetime.now().timestamp() < action.undo_expires_at),
            rx.button(
                "UNDO",
                size="1",
                color_scheme="yellow",
                variant="soft",
                on_click=lambda: [],  # TODO: Wire undo
                style={"font_family": "Courier New", "font_size": "9px"}
            ),
            rx.text(
                "—",
                font_size="10px",
                color="#444444"
            )
        ),
        
        spacing="3",
        padding="8px",
        background="#001100" if action.can_undo else "#111111",
        border="1px solid #003300" if action.can_undo else "1px solid #222222",
        border_radius="4px",
        width="100%",
        _hover={"background": "#002200" if action.can_undo else "#111111"}
    )


def safe_action_wrapper(
    action_type: str,
    target_id: str,
    action_func: Callable,
    undo_func: Optional[Callable] = None
) -> dict:
    """
    Wrapper function that adds confirmation and undo to any critical action
    
    Returns: dict with show_confirmation, execute, undo functions
    """
    return {
        "needs_confirmation": action_type in CRITICAL_ACTIONS,
        "action_config": CRITICAL_ACTIONS.get(action_type),
        "execute": action_func,
        "undo": undo_func,
        "target_id": target_id
    }


# CSS for safe actions animations
SAFE_ACTIONS_CSS = """
<style>
@keyframes slide-in {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes blink-warning {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0.5; }
}

@keyframes countdown-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.2); }
}

.undo-countdown {
    animation: countdown-pulse 1s ease-in-out infinite;
}
</style>
"""


# Example usage patterns
def example_safe_launch():
    """
    Example of how to use safe action wrapper
    
    # In your component:
    safe_launch = safe_action_wrapper(
        action_type="launch_intercept",
        target_id="B-001",
        action_func=lambda: launch_interceptor("B-001", "I-001"),
        undo_func=lambda: cancel_interceptor("I-001")
    )
    
    # Show confirmation dialog
    if safe_launch["needs_confirmation"]:
        show_dialog(confirmation_dialog(
            "launch_intercept",
            "B-001",
            on_confirm=safe_launch["execute"],
            on_cancel=close_dialog
        ))
    
    # After execution, show undo toast
    pending = PendingAction(
        action_type="launch_intercept",
        timestamp=time.time(),
        description="Interceptor I-001 → Target B-001",
        undo_data={"interceptor_id": "I-001"},
        can_undo=True,
        undo_expires_at=time.time() + 5.0
    )
    show_toast(undo_toast(pending, safe_launch["undo"]))
    """
    pass
