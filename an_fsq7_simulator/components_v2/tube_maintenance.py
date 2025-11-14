"""
Vacuum Tube Maintenance Mini-Game Component

Adds maintenance dimension to simulation:
- 8x8 grid of vacuum tubes
- Tubes degrade over time (ok → degrading → failed)
- Failed tubes cause performance penalties
- Click-to-replace interaction with animations
- Visual feedback (blinking, color coding)
- System performance indicator

This ties maintenance to simulation performance, making it meaningful.
"""

import reflex as rx
from typing import List
from ..state_model import TubeState, MaintenanceState


def tube_status_indicator(tube: TubeState, on_click=None) -> rx.Component:
    """
    Single tube status indicator
    
    States:
    - ok (health > 0.7): Green ▓
    - degrading (health 0.3-0.7): Yellow ▒, dimming
    - failed (health = 0): Red ✗, blinking
    - warming_up: Blue animation
    """
    
    # Use rx.cond for all conditional values
    bg_color = rx.cond(
        tube.status == "failed", "#330000",
        rx.cond(tube.status == "degrading", "#332200",
        rx.cond(tube.status == "warming_up", "#001133", "#003300"))
    )
    border_color = rx.cond(
        tube.status == "failed", "#ff0000",
        rx.cond(tube.status == "degrading", "#ffaa00",
        rx.cond(tube.status == "warming_up", "#0088ff", "#00ff00"))
    )
    symbol = rx.cond(
        tube.status == "failed", "✗",
        rx.cond(tube.status == "degrading", "▒",
        rx.cond(tube.status == "warming_up", "◌", "▓"))
    )
    text_color = rx.cond(
        tube.status == "failed", "#ff0000",
        rx.cond(tube.status == "degrading", "#ffaa00",
        rx.cond(tube.status == "warming_up", "#0088ff", "#00ff00"))
    )
    animation = rx.cond(
        tube.status == "failed", "blink 0.5s infinite",
        rx.cond(tube.status == "degrading", "pulse 2s infinite",
        rx.cond(tube.status == "warming_up", "glow 1s infinite", "none"))
    )
    
    return rx.box(
        rx.text(
            symbol,
            font_size="1.2rem",
            color=text_color,
            font_family="'Courier New', monospace",
            font_weight="bold",
        ),
        width="40px",
        height="40px",
        display="flex",
        align_items="center",
        justify_content="center",
        background=bg_color,
        border=f"2px solid {border_color}",
        border_radius="4px",
        cursor=rx.cond((tube.status == "failed") | (tube.status == "degrading"), "pointer", "default"),
        transition="all 0.2s",
        animation=animation,
        # on_click removed for now - TODO: wire up event handler
        # title removed for now - format not supported for Vars
    )


def tube_rack_grid(tubes: List[TubeState]) -> rx.Component:
    """
    8x8 grid of vacuum tubes
    Simplified to use rx.foreach instead of Python iteration
    """
    # Display first 8 tubes only (simplified for State Var compatibility)
    return rx.flex(
        rx.foreach(
            tubes[:8],
            lambda tube: tube_status_indicator(tube)
        ),
        wrap="wrap",
        spacing="1",
        max_width="400px",
    )


def tube_replacement_modal(tube: TubeState, show: bool, on_replace=None, on_cancel=None) -> rx.Component:
    """
    Modal dialog for tube replacement sequence
    Shows: Pull tube → Insert new → Warmup animation
    
    Args:
        tube: Tube to replace
        show: Whether to show modal
        on_replace: Callback for replace button
        on_cancel: Callback for cancel button
    """
    if not show:
        return rx.box()
    
    return rx.box(
        rx.box(
            rx.heading(f"REPLACE TUBE {tube.id}", size="4", color="#ff0000", margin_bottom="1rem"),
            
            rx.vstack(
                # Tube info
                rx.box(
                    rx.text("Current Status:", font_weight="bold", color="#888888"),
                    rx.text(
                        tube.status.upper(),
                        color="#ff0000",
                        font_size="1.2rem",
                        font_family="'Courier New', monospace",
                    ),
                    rx.text(
                        f"Health: {tube.health * 100}%",
                        color="#ff8888",
                    ),
                    padding="1rem",
                    background="#330000",
                    border="1px solid #ff0000",
                    border_radius="4px",
                    margin_bottom="1rem",
                ),
                
                # Replacement steps
                rx.box(
                    rx.text("REPLACEMENT PROCEDURE:", font_weight="bold", color="#00ff00", margin_bottom="0.5rem"),
                    rx.ordered_list(
                        rx.list_item("Power down circuit"),
                        rx.list_item("Pull failed tube from socket"),
                        rx.list_item("Insert new tube"),
                        rx.list_item("Power on and warm up (5 seconds)"),
                        color="#88ff88",
                        spacing="1",
                    ),
                    padding="1rem",
                    background="#001100",
                    border="1px solid #00ff00",
                    border_radius="4px",
                    margin_bottom="1rem",
                ),
                
                # Action buttons
                rx.hstack(
                    rx.button(
                        "🔧 REPLACE TUBE",
                        on_click=on_replace if on_replace else lambda: None,
                        background="#003300",
                        color="#00ff00",
                        border="2px solid #00ff00",
                        size="3",
                        _hover={"background": "#005500"},
                    ),
                    rx.button(
                        "CANCEL",
                        on_click=on_cancel if on_cancel else lambda: None,
                        background="#330000",
                        color="#ff0000",
                        border="1px solid #ff0000",
                        size="2",
                        _hover={"background": "#550000"},
                    ),
                    spacing="2",
                ),
                
                spacing="3",
                width="100%",
            ),
            
            max_width="500px",
            padding="2rem",
            background="#000000",
            border="3px solid #ff0000",
            border_radius="8px",
            box_shadow="0 0 30px rgba(255,0,0,0.5)",
        ),
        
        # Modal overlay
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        height="100vh",
        display="flex",
        align_items="center",
        justify_content="center",
        background="rgba(0,0,0,0.8)",
        z_index="1000",
    )


def performance_gauge(performance: float) -> rx.Component:
    """
    Visual gauge showing system performance (0.0-1.0)
    Affected by failed tubes
    """
    # Use rx.cond for conditional color/status based on State Var
    color = rx.cond(
        performance >= 0.9, "#00ff00",
        rx.cond(
            performance >= 0.7, "#88ff00",
            rx.cond(
                performance >= 0.5, "#ffff00",
                rx.cond(
                    performance >= 0.3, "#ffaa00",
                    "#ff0000"
                )
            )
        )
    )
    
    status = rx.cond(
        performance >= 0.9, "OPTIMAL",
        rx.cond(
            performance >= 0.7, "GOOD",
            rx.cond(
                performance >= 0.5, "DEGRADED",
                rx.cond(
                    performance >= 0.3, "POOR",
                    "CRITICAL"
                )
            )
        )
    )
    
    return rx.box(
        rx.heading("SYSTEM PERFORMANCE", size="3", color="#00ff00", margin_bottom="0.5rem"),
        
        # Progress bar
        rx.box(
            rx.box(
                width=f"{performance * 100}%",
                height="100%",
                background=color,
                border_radius="4px",
                transition="all 0.3s",
            ),
            width="100%",
            height="30px",
            background="#111111",
            border="2px solid #003300",
            border_radius="4px",
            overflow="hidden",
            margin_bottom="0.5rem",
        ),
        
        # Status text
        rx.hstack(
            rx.text(
                f"{performance * 100:.1f}%",
                font_family="'Courier New', monospace",
                font_size="1.5rem",
                color=color,
                font_weight="bold",
            ),
            rx.badge(status, color_scheme=rx.cond(performance >= 0.9, "green", "red"), size="2"),
            justify="between",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def tube_statistics(maintenance: MaintenanceState) -> rx.Component:
    """
    Statistics panel showing tube health overview
    Note: Simplified to avoid iterating over State Var
    """
    # TODO: Implement dynamic counting with rx.foreach or computed vars
    ok_count = 25000  # Placeholder
    degrading_count = 0
    failed_count = 0
    warming_count = 0
    total = 25000
    
    return rx.box(
        rx.heading("TUBE STATUS", size="3", color="#00ff00", margin_bottom="0.5rem"),
        
        rx.grid(
            # OK tubes
            rx.box(
                rx.text("OPERATIONAL", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{ok_count}",
                    font_family="'Courier New', monospace",
                    font_size="1.5rem",
                    color="#00ff00",
                    font_weight="bold",
                ),
            ),
            # Degrading tubes
            rx.box(
                rx.text("DEGRADING", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{degrading_count}",
                    font_family="'Courier New', monospace",
                    font_size="1.5rem",
                    color="#ffaa00",
                    font_weight="bold",
                ),
            ),
            # Failed tubes
            rx.box(
                rx.text("FAILED", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{failed_count}",
                    font_family="'Courier New', monospace",
                    font_size="1.5rem",
                    color="#ff0000",
                    font_weight="bold",
                ),
            ),
            # Warming up
            rx.box(
                rx.text("WARMING UP", font_size="0.8rem", color="#888888"),
                rx.text(
                    f"{warming_count}",
                    font_family="'Courier New', monospace",
                    font_size="1.5rem",
                    color="#0088ff",
                    font_weight="bold",
                ),
            ),
            columns="2",
            spacing="4",
            margin_bottom="1rem",
        ),
        
        # Warning messages
        rx.cond(
            failed_count > 0,
            rx.box(
                rx.text(
                    f"⚠ {failed_count} tube(s) require immediate replacement!",
                    color="#ff0000",
                    font_size="0.9rem",
                    font_weight="bold",
                ),
                padding="0.5rem",
                background="#330000",
                border="1px solid #ff0000",
                border_radius="4px",
                animation="blink 1s infinite",
            ),
            rx.box(),
        ),
        
        rx.cond(
            degrading_count > 0,
            rx.box(
                rx.text(
                    f"⚠ {degrading_count} tube(s) showing wear. Replace soon.",
                    color="#ffaa00",
                    font_size="0.85rem",
                ),
                padding="0.5rem",
                background="#332200",
                border="1px solid #ffaa00",
                border_radius="4px",
                margin_top="0.5rem",
            ),
            rx.box(),
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def tube_maintenance_panel(maintenance: MaintenanceState) -> rx.Component:
    """
    Complete tube maintenance panel
    Shows grid, statistics, performance, and replacement interface
    """
    return rx.box(
        rx.heading(
            "VACUUM TUBE MAINTENANCE",
            size="5",
            color="#00ff00",
            margin_bottom="1rem",
            font_family="'Courier New', monospace",
        ),
        
        # Performance gauge
        performance_gauge(1.0 - maintenance.performance_penalty),
        
        rx.divider(margin_y="1rem"),
        
        # Statistics
        tube_statistics(maintenance),
        
        rx.divider(margin_y="1rem"),
        
        # Tube rack
        rx.box(
            rx.heading("TUBE RACK", size="3", color="#00ff00", margin_bottom="0.5rem"),
            rx.text(
                "Click failed or degrading tubes to replace",
                color="#888888",
                font_size="0.85rem",
                margin_bottom="0.75rem",
            ),
            
            tube_rack_grid(maintenance.tubes),
            
            # Legend
            rx.hstack(
                rx.hstack(
                    rx.text("▓", color="#00ff00", font_weight="bold"),
                    rx.text("OK", color="#888888", font_size="0.8rem"),
                    spacing="1",
                ),
                rx.hstack(
                    rx.text("▒", color="#ffaa00", font_weight="bold"),
                    rx.text("Degrading", color="#888888", font_size="0.8rem"),
                    spacing="1",
                ),
                rx.hstack(
                    rx.text("✗", color="#ff0000", font_weight="bold"),
                    rx.text("Failed", color="#888888", font_size="0.8rem"),
                    spacing="1",
                ),
                rx.hstack(
                    rx.text("◌", color="#0088ff", font_weight="bold"),
                    rx.text("Warming", color="#888888", font_size="0.8rem"),
                    spacing="1",
                ),
                spacing="4",
                margin_top="1rem",
            ),
        ),
        
        # TODO: Add replacement modal when needed
        # tube_replacement_modal(...),
        
        padding="1.5rem",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        max_height="100vh",
        overflow_y="auto",
    )


# CSS animations for tube states
TUBE_ANIMATIONS_CSS = """
<style>
@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.3; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(0,136,255,0.3); }
    50% { box-shadow: 0 0 15px rgba(0,136,255,0.8); }
}
</style>
"""
