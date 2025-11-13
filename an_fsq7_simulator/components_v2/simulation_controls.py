"""
Simulation Control Panel

Provides pause/resume and speed multiplier controls for the simulation.
"""

import reflex as rx


def simulation_control_panel(
    is_paused: bool,
    speed_multiplier: float,
    world_time: int,
    on_pause,
    on_resume,
    on_set_speed
) -> rx.Component:
    """
    Control panel for simulation pause/resume and speed adjustment.
    
    Args:
        is_paused: Whether simulation is currently paused
        speed_multiplier: Current speed multiplier (0.5x, 1x, 2x, 5x)
        world_time: World time in milliseconds
        on_pause: Callback to pause simulation
        on_resume: Callback to resume simulation
        on_set_speed: Callback to set speed multiplier
    """
    
    # Calculate world time in seconds for display
    world_time_seconds = world_time // 1000
    
    return rx.box(
        rx.vstack(
            # Header
            rx.heading("SIMULATION CONTROLS", size="5", color="#00ff00"
            ),
            
            # Status indicator
            # Status indicators
            rx.hstack(
                rx.vstack(
                    rx.text("STATUS:", font_size="12px", color="#88ff88"),
                    rx.cond(
                        is_paused,
                        rx.text("PAUSED", font_size="16px", color="#ffaa00", font_weight="bold"),
                        rx.text("RUNNING", font_size="16px", color="#00ff00", font_weight="bold")
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.vstack(
                    rx.text("SPEED:", font_size="12px", color="#88ff88"),
                    rx.text(
                        f"{speed_multiplier}x",
                        font_size="16px",
                        color="#00ff00",
                        font_weight="bold"
                    ),
                    spacing="1",
                    align="start"
                ),
                rx.vstack(
                    rx.text("TIME:", font_size="12px", color="#88ff88"),
                    rx.text(
                        f"{world_time_seconds}s",
                        font_size="16px",
                        color="#00ff00",
                        font_weight="bold"
                    ),
                    spacing="1",
                    align="start"
                ),
                spacing="4",
                width="100%",
                justify="between"
            ),
            
            # Pause/Resume button
            rx.cond(
                is_paused,
                rx.button(
                    "▶ RESUME",
                    on_click=on_resume,
                    width="100%",
                    background="#006600",
                    color="#00ff00",
                    border="1px solid #00ff00",
                    _hover={"background": "#008800"},
                    cursor="pointer",
                    font_weight="bold",
                    font_size="16px",
                    padding="10px"
                ),
                rx.button(
                    "⏸ PAUSE",
                    on_click=on_pause,
                    width="100%",
                    background="#664400",
                    color="#ffaa00",
                    border="1px solid #ffaa00",
                    _hover={"background": "#886600"},
                    cursor="pointer",
                    font_weight="bold",
                    font_size="16px",
                    padding="10px"
                )
            ),
            
            # Speed multiplier buttons
            rx.vstack(
                rx.text("SPEED MULTIPLIER", font_size="12px", color="#88ff88"),
                rx.hstack(
                    rx.button(
                        "0.5x",
                        on_click=lambda: on_set_speed(0.5),
                        background=rx.cond(
                            speed_multiplier == 0.5,
                            "#006600",
                            "#003300"
                        ),
                        color=rx.cond(
                            speed_multiplier == 0.5,
                            "#00ff00",
                            "#88ff88"
                        ),
                        border=rx.cond(
                            speed_multiplier == 0.5,
                            "2px solid #00ff00",
                            "1px solid #00ff00"
                        ),
                        _hover={"background": "#004400"},
                        cursor="pointer",
                        flex="1",
                        padding="8px"
                    ),
                    rx.button(
                        "1x",
                        on_click=lambda: on_set_speed(1.0),
                        background=rx.cond(
                            speed_multiplier == 1.0,
                            "#006600",
                            "#003300"
                        ),
                        color=rx.cond(
                            speed_multiplier == 1.0,
                            "#00ff00",
                            "#88ff88"
                        ),
                        border=rx.cond(
                            speed_multiplier == 1.0,
                            "2px solid #00ff00",
                            "1px solid #00ff00"
                        ),
                        _hover={"background": "#004400"},
                        cursor="pointer",
                        flex="1",
                        padding="8px"
                    ),
                    rx.button(
                        "2x",
                        on_click=lambda: on_set_speed(2.0),
                        background=rx.cond(
                            speed_multiplier == 2.0,
                            "#006600",
                            "#003300"
                        ),
                        color=rx.cond(
                            speed_multiplier == 2.0,
                            "#00ff00",
                            "#88ff88"
                        ),
                        border=rx.cond(
                            speed_multiplier == 2.0,
                            "2px solid #00ff00",
                            "1px solid #00ff00"
                        ),
                        _hover={"background": "#004400"},
                        cursor="pointer",
                        flex="1",
                        padding="8px"
                    ),
                    rx.button(
                        "5x",
                        on_click=lambda: on_set_speed(5.0),
                        background=rx.cond(
                            speed_multiplier == 5.0,
                            "#006600",
                            "#003300"
                        ),
                        color=rx.cond(
                            speed_multiplier == 5.0,
                            "#00ff00",
                            "#88ff88"
                        ),
                        border=rx.cond(
                            speed_multiplier == 5.0,
                            "2px solid #00ff00",
                            "1px solid #00ff00"
                        ),
                        _hover={"background": "#004400"},
                        cursor="pointer",
                        flex="1",
                        padding="8px"
                    ),
                    spacing="2",
                    width="100%"
                ),
                spacing="2",
                width="100%",
                align="start"
            ),
            
            spacing="3",
            align="start",
            width="100%"
        ),
        padding="15px",
        background="#001100",
        border="2px solid #00ff00",
        border_radius="8px",
        width="100%"
    )
