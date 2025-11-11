"""
System Messages / Execution Trace Panel

Requirement #2: Explicit Execution Feedback

Persistent log showing ALL user actions:
- Button presses with timestamps
- Track selections and locks
- Program execution starts/completions
- Filter changes and toggles
- Intercept launches
- System state changes

User never has to guess "did it run?"
"""

import reflex as rx
from typing import List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class SystemMessage:
    """Single log entry in the system messages panel"""
    timestamp: str
    category: str  # INFO, ACTION, WARNING, ERROR, SUCCESS
    message: str
    details: str = ""


# Message categories with colors
MESSAGE_STYLES = {
    "INFO": {"color": "#00ff00", "icon": "ℹ"},
    "ACTION": {"color": "#00ffff", "icon": "▶"},
    "WARNING": {"color": "#ffff00", "icon": "⚠"},
    "ERROR": {"color": "#ff0000", "icon": "✗"},
    "SUCCESS": {"color": "#00ff88", "icon": "✓"},
    "TRACK": {"color": "#88ffff", "icon": "◉"},
    "INTERCEPT": {"color": "#ff00ff", "icon": "⚡"},
    "FILTER": {"color": "#ffaa00", "icon": "⚙"},
    "CPU": {"color": "#aaffff", "icon": "⚙"},
}


def format_timestamp() -> str:
    """Generate timestamp for log entry"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def message_row(msg: SystemMessage) -> rx.Component:
    """Single message row in the log"""
    style = MESSAGE_STYLES.get(msg.category, MESSAGE_STYLES["INFO"])
    
    return rx.hstack(
        # Timestamp
        rx.text(
            msg.timestamp,
            font_family="Courier New",
            font_size="10px",
            color="#888888",
            width="80px",
            flex_shrink="0"
        ),
        
        # Icon
        rx.text(
            style["icon"],
            font_size="12px",
            color=style["color"],
            width="20px",
            flex_shrink="0"
        ),
        
        # Category badge
        rx.badge(
            msg.category,
            color_scheme="gray",
            variant="soft",
            size="1",
            style={
                "background": f"{style['color']}22",
                "color": style["color"],
                "border": f"1px solid {style['color']}44"
            }
        ),
        
        # Message text
        rx.text(
            msg.message,
            font_family="Courier New",
            font_size="11px",
            color="#00ff00",
            flex_grow="1"
        ),
        
        # Details (if any)
        rx.cond(
            msg.details != "",
            rx.text(
                msg.details,
                font_family="Courier New",
                font_size="10px",
                color="#88ff88",
                font_style="italic"
            )
        ),
        
        spacing="2",
        padding="4px 8px",
        border_bottom="1px solid #003300",
        _hover={"background": "#001100"},
        width="100%",
        align="center"
    )


def system_messages_panel(messages: List[SystemMessage], max_height: str = "300px") -> rx.Component:
    """
    Complete system messages panel with scrollable log
    
    Shows chronological log of all user actions and system events.
    Auto-scrolls to bottom on new messages.
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "SYSTEM MESSAGES",
                    size="4",
                    color="#00ff00",
                    font_family="Courier New"
                ),
                rx.badge(
                    f"{len(messages)} entries",
                    color_scheme="green",
                    variant="soft"
                ),
                rx.spacer(),
                rx.button(
                    "CLEAR LOG",
                    size="1",
                    variant="soft",
                    color_scheme="red",
                    on_click=lambda: [],  # TODO: Wire to clear_messages()
                    style={
                        "font_family": "Courier New",
                        "font_size": "10px"
                    }
                ),
                justify="between",
                width="100%",
                padding="8px",
                border_bottom="2px solid #00ff00"
            ),
            
            # Message log (scrollable)
            rx.box(
                rx.vstack(
                    rx.foreach(
                        messages,
                        message_row
                    ),
                    spacing="0",
                    width="100%"
                ),
                overflow_y="auto",
                max_height=max_height,
                width="100%",
                style={
                    "scrollbar-width": "thin",
                    "scrollbar-color": "#00ff00 #000000"
                }
            ),
            
            # Footer with statistics
            rx.hstack(
                rx.text(
                    f"Last update: {messages[-1].timestamp if messages else '--:--:--'}",
                    font_family="Courier New",
                    font_size="10px",
                    color="#888888"
                ),
                rx.spacer(),
                rx.text(
                    "Auto-scroll: ON",
                    font_family="Courier New",
                    font_size="10px",
                    color="#00ff88"
                ),
                padding="8px",
                width="100%",
                border_top="1px solid #003300"
            ),
            
            spacing="0",
            width="100%"
        ),
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        width="100%"
    )


def system_messages_compact(messages: List[SystemMessage], max_entries: int = 5) -> rx.Component:
    """
    Compact version showing only recent messages
    For embedding in other panels
    """
    recent_messages = messages[-max_entries:] if len(messages) > max_entries else messages
    
    return rx.box(
        rx.vstack(
            rx.text(
                "RECENT ACTIVITY",
                font_family="Courier New",
                font_size="11px",
                font_weight="bold",
                color="#00ff00",
                padding="4px"
            ),
            rx.vstack(
                rx.foreach(
                    recent_messages,
                    lambda msg: message_row(msg)
                ),
                spacing="0",
                width="100%"
            ),
            spacing="2",
            width="100%"
        ),
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
        padding="4px",
        width="100%"
    )


# Helper functions to create common message types

def log_track_selected(track_id: str, track_type: str) -> SystemMessage:
    """Log track selection"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="TRACK",
        message=f"Track {track_id} selected",
        details=f"Type: {track_type}"
    )


def log_intercept_launched(track_id: str, interceptor_id: str) -> SystemMessage:
    """Log intercept launch"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="INTERCEPT",
        message=f"Interceptor {interceptor_id} launched",
        details=f"Target: {track_id}"
    )


def log_filter_changed(filter_name: str, enabled: bool) -> SystemMessage:
    """Log filter toggle"""
    state = "ENABLED" if enabled else "DISABLED"
    return SystemMessage(
        timestamp=format_timestamp(),
        category="FILTER",
        message=f"Filter {filter_name} {state}",
        details=""
    )


def log_overlay_toggled(overlay_name: str, enabled: bool) -> SystemMessage:
    """Log overlay toggle"""
    state = "ON" if enabled else "OFF"
    return SystemMessage(
        timestamp=format_timestamp(),
        category="FILTER",
        message=f"Overlay {overlay_name} {state}",
        details=""
    )


def log_program_loaded(program_name: str) -> SystemMessage:
    """Log CPU program load"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="CPU",
        message=f"Program loaded: {program_name}",
        details="Ready to execute"
    )


def log_program_executed(program_name: str, result: str) -> SystemMessage:
    """Log CPU program execution"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="SUCCESS",
        message=f"Program completed: {program_name}",
        details=f"Result: {result}"
    )


def log_button_pressed(button_name: str, action: str) -> SystemMessage:
    """Log button press"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="ACTION",
        message=f"Button pressed: {button_name}",
        details=action
    )


def log_error(error_message: str) -> SystemMessage:
    """Log error"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="ERROR",
        message=error_message,
        details="Check system status"
    )


def log_warning(warning_message: str) -> SystemMessage:
    """Log warning"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="WARNING",
        message=warning_message,
        details=""
    )


def log_info(info_message: str, details: str = "") -> SystemMessage:
    """Log general info"""
    return SystemMessage(
        timestamp=format_timestamp(),
        category="INFO",
        message=info_message,
        details=details
    )


# Example usage for testing
EXAMPLE_MESSAGES = [
    SystemMessage("09:15:23.145", "INFO", "System powered on", "All subsystems operational"),
    SystemMessage("09:15:25.892", "ACTION", "Button pressed: POWER ON", "Vacuum tube warmup initiated"),
    SystemMessage("09:15:30.234", "SUCCESS", "System ready", "All tubes operational"),
    SystemMessage("09:16:12.456", "TRACK", "Track B-001 detected", "Type: BOMBER, Alt: 35000ft"),
    SystemMessage("09:16:15.789", "TRACK", "Track B-001 selected", "Light gun lock acquired"),
    SystemMessage("09:16:18.123", "ACTION", "Button pressed: LAUNCH INTERCEPT", "Target: B-001"),
    SystemMessage("09:16:18.234", "INTERCEPT", "Interceptor I-001 launched", "Target: B-001"),
    SystemMessage("09:16:20.567", "FILTER", "Filter HOSTILE ENABLED", "Showing only hostile tracks"),
    SystemMessage("09:17:45.890", "SUCCESS", "Intercept successful", "Track B-001 neutralized"),
    SystemMessage("09:18:02.345", "WARNING", "Vacuum tube T-042 degrading", "Replacement recommended"),
]
