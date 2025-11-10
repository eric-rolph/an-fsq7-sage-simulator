"""
Control Panel Component

Simulates the physical control surfaces including switches, buttons, and indicators.
"""

import reflex as rx


def control_panel() -> rx.Component:
    """Control panel with power and operational controls."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            rx.heading(
                "CONTROL PANEL",
                size="6",
                color="#00FF00",
                font_family="monospace",
                text_shadow="0 0 10px #00FF00",
            ),
            
            rx.divider(border_color="#00FF00", opacity="0.3"),
            
            # Power control
            rx.vstack(
                rx.text(
                    "POWER",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                rx.cond(
                    ~FSQ7State.power_on,
                    rx.button(
                        "POWER ON",
                        on_click=FSQ7State.power_on_system,
                        color_scheme="green",
                        size="3",
                        width="100%",
                    ),
                    rx.button(
                        "POWER OFF",
                        on_click=FSQ7State.power_off_system,
                        color_scheme="red",
                        size="3",
                        width="100%",
                    ),
                ),
                width="100%",
                spacing="2",
                padding="10px",
                background="rgba(0, 50, 0, 0.2)",
                border="2px solid #00FF00",
                border_radius="5px",
            ),
            
            # Startup progress
            rx.cond(
                FSQ7State.power_on & ~FSQ7State.system_ready,
                rx.vstack(
                    rx.text(
                        "SYSTEM INITIALIZATION",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    rx.progress(
                        value=FSQ7State.startup_progress,
                        max=100,
                        width="100%",
                        color_scheme="yellow",
                        size="2",
                    ),
                    rx.text(
                        f"{FSQ7State.startup_progress}%",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    width="100%",
                    spacing="1",
                    padding="10px",
                    background="rgba(50, 50, 0, 0.2)",
                    border="2px solid #FFFF00",
                    border_radius="5px",
                ),
            ),
            
            # Operational controls (only visible when system is ready)
            rx.cond(
                FSQ7State.system_ready,
                rx.vstack(
                    # Manual Override
                    rx.vstack(
                        rx.text(
                            "MANUAL OVERRIDE",
                            color="#00FF00",
                            font_family="monospace",
                            font_size="12px",
                            font_weight="bold",
                        ),
                        rx.switch(
                            checked=FSQ7State.manual_override,
                            on_change=FSQ7State.toggle_manual_override,
                            color_scheme="orange",
                            size="3",
                        ),
                        rx.text(
                            rx.cond(
                                FSQ7State.manual_override,
                                "ENGAGED",
                                "AUTOMATIC"
                            ),
                            color=rx.cond(
                                FSQ7State.manual_override,
                                "#FF8800",
                                "#00FF00"
                            ),
                            font_family="monospace",
                            font_size="10px",
                        ),
                        width="100%",
                        spacing="2",
                        padding="10px",
                        background="rgba(50, 25, 0, 0.2)",
                        border="2px solid #FF8800",
                        border_radius="5px",
                    ),
                    
                    # Intercept Mode
                    rx.vstack(
                        rx.text(
                            "INTERCEPT MODE",
                            color="#00FF00",
                            font_family="monospace",
                            font_size="12px",
                            font_weight="bold",
                        ),
                        rx.switch(
                            checked=FSQ7State.intercept_mode,
                            on_change=FSQ7State.toggle_intercept_mode,
                            color_scheme="red",
                            size="3",
                        ),
                        rx.text(
                            rx.cond(
                                FSQ7State.intercept_mode,
                                "ACTIVE",
                                "STANDBY"
                            ),
                            color=rx.cond(
                                FSQ7State.intercept_mode,
                                "#FF0000",
                                "#00FF00"
                            ),
                            font_family="monospace",
                            font_size="10px",
                        ),
                        width="100%",
                        spacing="2",
                        padding="10px",
                        background="rgba(50, 0, 0, 0.2)",
                        border="2px solid #FF0000",
                        border_radius="5px",
                    ),
                    
                    # Display Mode Selection
                    rx.vstack(
                        rx.text(
                            "DISPLAY MODE",
                            color="#00FF00",
                            font_family="monospace",
                            font_size="12px",
                            font_weight="bold",
                        ),
                        rx.button(
                            rx.text(
                                FSQ7State.display_mode,
                                font_family="monospace",
                            ),
                            on_click=FSQ7State.toggle_display_mode,
                            color_scheme="cyan",
                            size="2",
                            width="100%",
                        ),
                        width="100%",
                        spacing="2",
                        padding="10px",
                        background="rgba(0, 25, 50, 0.2)",
                        border="2px solid #00FFFF",
                        border_radius="5px",
                    ),
                    
                    # Brightness Control
                    rx.vstack(
                        rx.text(
                            "DISPLAY BRIGHTNESS",
                            color="#00FF00",
                            font_family="monospace",
                            font_size="12px",
                            font_weight="bold",
                        ),
                        rx.slider(
                            default_value=FSQ7State.display_brightness,
                            on_change=FSQ7State.adjust_brightness,
                            min=0,
                            max=100,
                            width="100%",
                            color_scheme="green",
                        ),
                        rx.text(
                            f"{FSQ7State.display_brightness}%",
                            color="#FFFF00",
                            font_family="monospace",
                            font_size="10px",
                        ),
                        width="100%",
                        spacing="2",
                        padding="10px",
                        background="rgba(0, 50, 0, 0.2)",
                        border="2px solid #00FF00",
                        border_radius="5px",
                    ),
                    
                    width="100%",
                    spacing="3",
                ),
            ),
            
            spacing="4",
            width="100%",
        ),
        
        background="rgba(0, 20, 0, 0.5)",
        padding="15px",
        border="3px solid #00FF00",
        border_radius="10px",
        box_shadow="0 0 20px rgba(0, 255, 0, 0.3)",
    )
