"""
Light Gun Target Selection Component

Implements the authentic SAGE light gun metaphor:
1. Press 'D' to arm light gun → crosshair appears
2. Click on radar track → target selected
3. Track info populates Track Detail panel
4. LAUNCH INTERCEPT button becomes enabled

This makes the light gun interaction obvious and satisfying.
"""

import reflex as rx
from typing import Optional
from ..state_model import Track, UIState


def crosshair_cursor() -> rx.Component:
    """SVG crosshair cursor when light gun is armed"""
    return rx.html(
        """
        <svg width="40" height="40" viewBox="0 0 40 40" style="position: fixed; pointer-events: none; z-index: 9999;">
            <circle cx="20" cy="20" r="15" fill="none" stroke="#00ff00" stroke-width="2" opacity="0.8"/>
            <line x1="20" y1="5" x2="20" y2="15" stroke="#00ff00" stroke-width="2" opacity="0.8"/>
            <line x1="20" y1="25" x2="20" y2="35" stroke="#00ff00" stroke-width="2" opacity="0.8"/>
            <line x1="5" y1="20" x2="15" y2="20" stroke="#00ff00" stroke-width="2" opacity="0.8"/>
            <line x1="25" y1="20" x2="35" y2="20" stroke="#00ff00" stroke-width="2" opacity="0.8"/>
            <circle cx="20" cy="20" r="2" fill="#00ff00" opacity="0.8"/>
        </svg>
        """
    )


def track_detail_panel(track: Optional[Track], armed: bool) -> rx.Component:
    """
    Track Detail Panel (DD CRT equivalent)
    Shows selected target information
    """
    # Can't use Python if with Vars - use rx.cond instead
    return rx.cond(
        track != None,
        _track_detail_content(track, armed),
        rx.box(
            rx.heading("TARGET DETAIL", size="4", color="#00ff00", margin_bottom="0.5rem"),
            rx.box(
                rx.text(
                    rx.cond(armed, "LIGHT GUN ARMED - SELECT TARGET", "NO TARGET SELECTED"),
                    color=rx.cond(armed, "#ffff00", "#888888"),
                    font_size="0.9rem",
                    text_align="center",
                    font_style="italic",
                ),
                padding="2rem",
                border="1px dashed #003300",
                border_radius="4px",
            ),
            padding="1rem",
            background="#000000",
            border="1px solid #00ff00",
            border_radius="4px",
        )
    )


def _track_detail_content(track: Track, armed: bool) -> rx.Component:
    """Helper function for track detail content when track exists"""
    # Color coding by hostility - can't use dict.get() with Vars, use rx.match instead
    type_color = rx.match(
        track.track_type,
        ("hostile", "#ff0000"),
        ("friendly", "#00ff00"),
        ("unknown", "#ffff00"),
        ("missile", "#ff00ff"),
        "#888888"  # default
    )
    
    threat_color = rx.match(
        track.threat_level,
        ("CRITICAL", "#ff0000"),
        ("HIGH", "#ff8800"),
        ("MEDIUM", "#ffff00"),
        ("LOW", "#88ff88"),
        ("NONE", "#00ff00"),
        "#888888"  # default
    )
    
    return rx.box(
        # Header with track ID
        rx.hstack(
            rx.heading("TARGET DETAIL", size="4", color="#00ff00"),
            rx.badge("SELECTED", color_scheme="green"),
            justify="between",
            width="100%",
            margin_bottom="1rem",
        ),
        
        # Track ID and Type
        rx.box(
            rx.hstack(
                rx.text("ID:", font_weight="bold", color="#00ff00", width="60px"),
                rx.text(
                    track.id,
                    font_family="'Courier New', monospace",
                    color="#ffff00",
                    font_size="1.2rem",
                ),
                spacing="2",
            ),
            rx.hstack(
                rx.text("TYPE:", font_weight="bold", color="#00ff00", width="60px"),
                rx.badge(
                    track.track_type.upper(),
                    color_scheme=rx.cond(track.track_type == "hostile", "red", "green"),
                    font_size="0.9rem",
                ),
                spacing="2",
            ),
            spacing="3",
            margin_bottom="1rem",
        ),
        
        # Telemetry data
        rx.grid(
            # Altitude
            rx.box(
                rx.text("ALTITUDE", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{track.altitude:,} ft",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                    font_size="1.1rem",
                ),
            ),
            # Speed
            rx.box(
                rx.text("SPEED", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{track.speed:.0f} kts",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                    font_size="1.1rem",
                ),
            ),
            # Heading
            rx.box(
                rx.text("HEADING", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{track.heading:.0f}°",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                    font_size="1.1rem",
                ),
            ),
            # Threat level
            rx.box(
                rx.text("THREAT", font_size="0.8rem", color="#888888"),
                rx.badge(
                    track.threat_level,
                    color_scheme="red" if track.threat_level in ["CRITICAL", "HIGH"] else "yellow",
                    font_size="0.9rem",
                ),
            ),
            columns="2",
            spacing="4",
            margin_bottom="1rem",
        ),
        
        # Position data
        rx.box(
            rx.text("POSITION", font_size="0.8rem", color="#888888", margin_bottom="0.25rem"),
            rx.text(
                f"X: {track.x:.3f}  Y: {track.y:.3f}",
                font_family="'Courier New', monospace",
                color="#88ff88",
                font_size="0.9rem",
            ),
            margin_bottom="1rem",
        ),
        
        # Velocity vector
        rx.box(
            rx.text("VELOCITY", font_size="0.8rem", color="#888888", margin_bottom="0.25rem"),
            rx.text(
                f"VX: {track.vx:.4f}  VY: {track.vy:.4f}",
                font_family="'Courier New', monospace",
                color="#88ff88",
                font_size="0.9rem",
            ),
            margin_bottom="1rem",
        ),
        
        # Special: Missile countdown
        rx.cond(
            (track.track_type == "missile") & (track.t_minus != None),  # Use & instead of 'and' for Vars
            rx.box(
                rx.text("TIME TO IMPACT", font_size="0.8rem", color="#ff0000", margin_bottom="0.25rem"),
                rx.text(
                    f"T-{track.t_minus:.1f}s",
                    font_family="'Courier New', monospace",
                    color="#ff0000",
                    font_size="1.5rem",
                    font_weight="bold",
                ),
                padding="0.5rem",
                background="#330000",
                border="1px solid #ff0000",
                border_radius="4px",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.box(),
        ),
        
        # Action buttons
        rx.vstack(
            rx.button(
                "🚀 LAUNCH INTERCEPT",
                # on_click: TODO: Wire to launch_intercept
                background="#003300",
                color="#00ff00",
                border="2px solid #00ff00",
                width="100%",
                size="3",
                # disabled: TODO - Can't use Python comparison (track.track_type == "friendly")
                _hover={"background": "#005500"},
            ),
            rx.button(
                "✕ CLEAR SELECTION",
                # on_click: TODO: Wire to clear_selection
                background="#330000",
                color="#ff0000",
                border="1px solid #ff0000",
                width="100%",
                size="2",
                _hover={"background": "#550000"},
            ),
            spacing="2",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="4px",
    )


def light_gun_status_indicator(armed: bool, selected_id: Optional[str]) -> rx.Component:
    """Small status indicator for light gun state"""
    if armed and not selected_id:
        return rx.hstack(
            rx.box(
                width="10px",
                height="10px",
                background="#ffff00",
                border_radius="50%",
                animation="pulse 1s infinite",
            ),
            rx.text(
                "LIGHT GUN ARMED",
                color="#ffff00",
                font_size="0.9rem",
                font_weight="bold",
            ),
            spacing="2",
            padding="0.5rem 1rem",
            background="#332200",
            border="1px solid #ffff00",
            border_radius="4px",
        )
    elif selected_id:
        return rx.hstack(
            rx.box(
                width="10px",
                height="10px",
                background="#00ff00",
                border_radius="50%",
            ),
            rx.text(
                f"TARGET {selected_id} SELECTED",
                color="#00ff00",
                font_size="0.9rem",
                font_weight="bold",
            ),
            spacing="2",
            padding="0.5rem 1rem",
            background="#002200",
            border="1px solid #00ff00",
            border_radius="4px",
        )
    else:
        return rx.box()


def light_gun_controls() -> rx.Component:
    """Control panel for light gun"""
    return rx.box(
        rx.heading("LIGHT GUN", size="4", color="#00ff00", margin_bottom="0.5rem"),
        
        rx.vstack(
            # Arm/Disarm button
            rx.button(
                "🎯 ARM LIGHT GUN (D)",
                # on_click: TODO: Wire to toggle_light_gun
                background="#003300",
                color="#00ff00",
                border="2px solid #00ff00",
                width="100%",
                size="3",
                _hover={"background": "#005500"},
            ),
            
            # Instructions
            rx.box(
                rx.text(
                    "INSTRUCTIONS:",
                    font_weight="bold",
                    color="#00ff00",
                    font_size="0.85rem",
                    margin_bottom="0.25rem",
                ),
                rx.text(
                    "1. Press 'D' or click ARM button",
                    color="#88ff88",
                    font_size="0.8rem",
                ),
                rx.text(
                    "2. Crosshair appears over scope",
                    color="#88ff88",
                    font_size="0.8rem",
                ),
                rx.text(
                    "3. Click on radar target",
                    color="#88ff88",
                    font_size="0.8rem",
                ),
                rx.text(
                    "4. Target info displays below",
                    color="#88ff88",
                    font_size="0.8rem",
                ),
                padding="0.75rem",
                background="#001100",
                border="1px solid #003300",
                border_radius="4px",
            ),
            
            spacing="3",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


# Keyboard handler script (to be injected into page)
LIGHT_GUN_KEYBOARD_SCRIPT = """
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'd' || e.key === 'D') {
        // Trigger light gun toggle
        // TODO: Send event to Reflex backend
        console.log('Light gun toggle requested');
    }
    if (e.key === 'Escape') {
        // Clear selection
        // TODO: Send event to Reflex backend
        console.log('Clear selection requested');
    }
});
</script>
"""
