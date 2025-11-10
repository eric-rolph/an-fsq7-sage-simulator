"""
System Status Component

Displays real-time system health and performance metrics.
"""

import reflex as rx


def system_status() -> rx.Component:
    """System status display panel."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            rx.heading(
                "SYSTEM STATUS",
                size="6",
                color="#00FF00",
                font_family="monospace",
                text_shadow="0 0 10px #00FF00",
            ),
            
            rx.divider(border_color="#00FF00", opacity="0.3"),
            
            # Vacuum tube status
            rx.vstack(
                rx.text(
                    "VACUUM TUBES",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                rx.hstack(
                    rx.text("Active:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.active_tubes:,}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Failed:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.failed_tubes}",
                        color=rx.cond(FSQ7State.failed_tubes > 10, "#FF0000", "#FFFF00"),
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Temp:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.tube_temperature:.1f}°C",
                        color=rx.cond(FSQ7State.tube_temperature > 250, "#FF8800", "#FFFF00"),
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                width="100%",
                spacing="1",
                padding="8px",
                background="rgba(0, 50, 0, 0.2)",
                border="1px solid #00FF00",
                border_radius="3px",
            ),
            
            # Memory status (TWO BANKS)
            rx.vstack(
                rx.text(
                    "CORE MEMORY",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                rx.hstack(
                    rx.text("Used:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.memory_used_bank1 + FSQ7State.memory_used_bank2:,}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Total:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.memory_capacity_bank1 + FSQ7State.memory_capacity_bank2:,}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                rx.progress(
                    value=FSQ7State.memory_used_bank1 + FSQ7State.memory_used_bank2,
                    max=FSQ7State.memory_capacity_bank1 + FSQ7State.memory_capacity_bank2,
                    width="100%",
                    color_scheme="cyan",
                    size="1",
                ),
                width="100%",
                spacing="1",
                padding="8px",
                background="rgba(0, 50, 50, 0.2)",
                border="1px solid #00FFFF",
                border_radius="3px",
            ),
            
            # Mission statistics
            rx.vstack(
                rx.text(
                    "MISSION DATA",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                rx.hstack(
                    rx.text("Alerts:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.alerts_count}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Intercepts:", color="#00FF00", font_family="monospace", font_size="11px"),
                    rx.text(
                        f"{FSQ7State.successful_intercepts}",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                width="100%",
                spacing="1",
                padding="8px",
                background="rgba(50, 0, 50, 0.2)",
                border="1px solid #FF00FF",
                border_radius="3px",
            ),
            
            spacing="3",
            width="100%",
        ),
        
        background="rgba(0, 20, 0, 0.5)",
        padding="15px",
        border="3px solid #00FF00",
        border_radius="10px",
        box_shadow="0 0 20px rgba(0, 255, 0, 0.3)",
    )
