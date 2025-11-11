"""
Status Bar Component

Top-of-screen status bar showing:
- Current console mode
- Mission elapsed time
- Quick CPU status (PC, A register)
- System health (tubes, temperature)
"""

import reflex as rx


def status_bar() -> rx.Component:
    """Status bar showing current operational mode and key metrics."""
    
    # Import here to avoid circular dependency
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.hstack(
            # Left: Mode indicator
            rx.hstack(
                rx.text("MODE:", font_weight="bold", color="#00FFFF", font_size="14px"),
                rx.text(
                    rx.cond(
                        FSQ7State.display_mode == "RADAR",
                        "RADAR SURVEILLANCE",
                        rx.cond(
                            FSQ7State.display_mode == "TACTICAL",
                            "TACTICAL SITUATION",
                            rx.cond(
                                FSQ7State.display_mode == "STATUS",
                                "SYSTEM STATUS",
                                "MEMORY VISUALIZATION"
                            )
                        )
                    ),
                    color="#FFFF00",
                    font_size="14px",
                    font_weight="bold",
                ),
                spacing="2",
            ),
            
            # Center: Mission time
            rx.hstack(
                rx.text("MISSION:", font_weight="bold", color="#00FFFF", font_size="14px"),
                rx.text(
                    FSQ7State.mission_time, 
                    color="#00FF00", 
                    font_family="monospace",
                    font_size="16px",
                    font_weight="bold",
                ),
                spacing="2",
            ),
            
            # Right: Quick stats
            rx.hstack(
                rx.text(
                    f"PC: {FSQ7State.cpu_program_counter_hex}", 
                    font_family="monospace", 
                    color="#FFFF00",
                    font_size="13px",
                ),
                rx.text(
                    f"A: {FSQ7State.cpu_accumulator_hex}", 
                    font_family="monospace", 
                    color="#FFFF00",
                    font_size="13px",
                ),
                rx.text(
                    f"TUBES: {FSQ7State.active_tubes}", 
                    color=rx.cond(FSQ7State.active_tubes > 57000, "#00FF00", "#FF8800"),
                    font_size="13px",
                ),
                rx.text(
                    f"{FSQ7State.tube_temperature:.0f}°C", 
                    color=rx.cond(FSQ7State.tube_temperature > 250, "#00FF00", "#FFFF00"),
                    font_size="13px",
                ),
                spacing="3",
            ),
            
            justify="between",
            align="center",
            width="100%",
            padding="0.5em 1em",
        ),
        background="linear-gradient(to bottom, #1a1a2e, #0f0f1e)",
        border_bottom="2px solid #00FFFF",
        width="100%",
    )
