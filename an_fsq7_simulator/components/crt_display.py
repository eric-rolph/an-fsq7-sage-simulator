"""
CRT Display Component

The main visual display that simulates a 1950s-era cathode ray tube (CRT) with
phosphor decay, scan lines, and vintage visual effects.
"""

import reflex as rx


def crt_display() -> rx.Component:
    """Main CRT display component with vintage styling."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            # Display mode indicator
            rx.hstack(
                rx.badge(
                    FSQ7State.display_mode,
                    color_scheme="green",
                    size="2",
                ),
                rx.spacer(),
                rx.text(
                    f"BRIGHTNESS: {FSQ7State.display_brightness}%",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                ),
                width="100%",
                padding="10px",
            ),
            
            # Main display area
            rx.box(
                rx.cond(
                    FSQ7State.system_ready,
                    rx.box(
                        # Display content based on mode
                        rx.match(
                            FSQ7State.display_mode,
                            ("RADAR", radar_display_overlay()),
                            ("TACTICAL", tactical_display_overlay()),
                            ("STATUS", status_display_overlay()),
                            ("MEMORY", memory_display_overlay()),
                        ),
                        
                        # CRT effect overlay
                        _before={
                            "content": '""',
                            "position": "absolute",
                            "top": "0",
                            "left": "0",
                            "width": "100%",
                            "height": "100%",
                            "background": "linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06))",
                            "backgroundSize": "100% 2px, 3px 100%",
                            "pointerEvents": "none",
                            "zIndex": "2",
                        },
                        position="relative",
                        on_click=lambda e: FSQ7State.light_gun_click(e.client_x, e.client_y),
                    ),
                    # System offline display
                    rx.center(
                        rx.text(
                            "SYSTEM OFFLINE",
                            color="#004400",
                            font_family="monospace",
                            font_size="40px",
                            font_weight="bold",
                            text_shadow="0 0 20px #004400",
                        ),
                        width="100%",
                        height="100%",
                    ),
                ),
                
                width="800px",
                height="600px",
                background="radial-gradient(ellipse at center, #001100 0%, #000000 70%)",
                border="40px solid #333333",
                border_radius="20px",
                box_shadow="inset 0 0 50px #000000, 0 0 50px rgba(0, 255, 0, 0.3)",
                position="relative",
                overflow="hidden",
                # Vignette effect
                _after={
                    "content": '""',
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "borderRadius": "20px",
                    "boxShadow": "inset 0 0 100px rgba(0,0,0,0.8)",
                    "pointerEvents": "none",
                    "zIndex": "3",
                },
            ),
            
            spacing="0",
        ),
        
        padding="20px",
    )


def radar_display_overlay() -> rx.Component:
    """Radar display mode showing tracked targets."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        # SVG for radar elements
        rx.html(
            f"""
            <svg width="800" height="600" style="position: absolute; top: 0; left: 0;">
                <!-- Radar rings -->
                <circle cx="400" cy="300" r="50" fill="none" stroke="#003300" stroke-width="1"/>
                <circle cx="400" cy="300" r="100" fill="none" stroke="#003300" stroke-width="1"/>
                <circle cx="400" cy="300" r="150" fill="none" stroke="#003300" stroke-width="1"/>
                <circle cx="400" cy="300" r="200" fill="none" stroke="#003300" stroke-width="1"/>
                <circle cx="400" cy="300" r="250" fill="none" stroke="#003300" stroke-width="1"/>
                
                <!-- Crosshair -->
                <line x1="0" y1="300" x2="800" y2="300" stroke="#003300" stroke-width="1"/>
                <line x1="400" y1="0" x2="400" y2="600" stroke="#003300" stroke-width="1"/>
                
                <!-- Range markers -->
                <text x="410" y="105" fill="#00FF00" font-family="monospace" font-size="10">100</text>
                <text x="410" y="155" fill="#00FF00" font-family="monospace" font-size="10">200</text>
                <text x="410" y="205" fill="#00FF00" font-family="monospace" font-size="10">300</text>
            </svg>
            """
        ),
        
        # Radar targets
        rx.foreach(
            FSQ7State.radar_targets,
            lambda target: rx.box(
                # Target blip
                rx.box(
                    width="10px",
                    height="10px",
                    background=rx.match(
                        target["threat_level"],
                        ("HIGH", "#FF0000"),
                        ("MEDIUM", "#FF8800"),
                        ("#00FF00"),
                    ),
                    border_radius="50%",
                    box_shadow=rx.cond(
                        target["target_id"] == FSQ7State.selected_target,
                        "0 0 20px currentColor",
                        "0 0 10px currentColor",
                    ),
                    filter=rx.cond(
                        target["target_id"] == FSQ7State.selected_target,
                        "brightness(2)",
                        "brightness(1)",
                    ),
                ),
                # Target label
                rx.text(
                    target["target_id"],
                    color="#00FF00",
                    font_family="monospace",
                    font_size="9px",
                    position="absolute",
                    top="-15px",
                    left="12px",
                    white_space="nowrap",
                    text_shadow="0 0 5px #00FF00",
                ),
                position="absolute",
                left=f"{target['x']}px",
                top=f"{target['y']}px",
                transform="translate(-50%, -50%)",
            ),
        ),
        
        # Selected target info
        rx.cond(
            FSQ7State.selected_target != "",
            rx.box(
                rx.vstack(
                    rx.text(
                        f"TARGET: {FSQ7State.selected_target}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.button(
                        "ASSIGN INTERCEPT",
                        on_click=FSQ7State.assign_intercept,
                        color_scheme="red",
                        size="2",
                    ),
                    rx.button(
                        "CLEAR",
                        on_click=FSQ7State.clear_light_gun,
                        size="1",
                    ),
                    spacing="2",
                    padding="10px",
                    background="rgba(0, 0, 0, 0.8)",
                    border="2px solid #FFFF00",
                    border_radius="5px",
                ),
                position="absolute",
                top="20px",
                right="20px",
            ),
        ),
        
        position="relative",
        width="100%",
        height="100%",
    )


def tactical_display_overlay() -> rx.Component:
    """Tactical situation display."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.center(
        rx.vstack(
            rx.text(
                "TACTICAL SITUATION",
                color="#00FF00",
                font_family="monospace",
                font_size="24px",
                text_shadow="0 0 10px #00FF00",
            ),
            rx.divider(border_color="#00FF00", width="80%"),
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.text("THREATS", color="#FF0000", font_family="monospace", font_size="16px"),
                        rx.text(
                            f"{FSQ7State.high_threat_count}",
                            color="#FF0000",
                            font_family="monospace",
                            font_size="48px",
                            font_weight="bold",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    padding="20px",
                    border="2px solid #FF0000",
                    border_radius="10px",
                ),
                rx.box(
                    rx.vstack(
                        rx.text("TRACKED", color="#00FF00", font_family="monospace", font_size="16px"),
                        rx.text(
                            f"{FSQ7State.tracked_objects}",
                            color="#00FF00",
                            font_family="monospace",
                            font_size="48px",
                            font_weight="bold",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    padding="20px",
                    border="2px solid #00FF00",
                    border_radius="10px",
                ),
                rx.box(
                    rx.vstack(
                        rx.text("INTERCEPTS", color="#FF8800", font_family="monospace", font_size="16px"),
                        rx.text(
                            f"{FSQ7State.intercept_courses}",
                            color="#FF8800",
                            font_family="monospace",
                            font_size="48px",
                            font_weight="bold",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    padding="20px",
                    border="2px solid #FF8800",
                    border_radius="10px",
                ),
                columns="3",
                spacing="4",
                width="100%",
            ),
            spacing="4",
            width="80%",
        ),
        width="100%",
        height="100%",
    )


def status_display_overlay() -> rx.Component:
    """System status display."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.center(
        rx.vstack(
            rx.text(
                "SYSTEM STATUS",
                color="#00FF00",
                font_family="monospace",
                font_size="24px",
                text_shadow="0 0 10px #00FF00",
            ),
            rx.divider(border_color="#00FF00", width="80%"),
            rx.vstack(
                rx.hstack(
                    rx.text("VACUUM TUBES:", color="#00FF00", font_family="monospace", font_size="16px"),
                    rx.text(
                        f"{FSQ7State.active_tubes:,} / {FSQ7State.total_tubes:,}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="16px",
                    ),
                    width="100%",
                    justify="space-between",
                ),
                rx.hstack(
                    rx.text("TEMPERATURE:", color="#00FF00", font_family="monospace", font_size="16px"),
                    rx.text(
                        f"{FSQ7State.tube_temperature:.1f}°C",
                        color=rx.cond(FSQ7State.tube_temperature > 250, "#FF8800", "#FFFF00"),
                        font_family="monospace",
                        font_size="16px",
                    ),
                    width="100%",
                    justify="space-between",
                ),
                rx.hstack(
                    rx.text("MEMORY:", color="#00FF00", font_family="monospace", font_size="16px"),
                    rx.text(
                        f"{FSQ7State.total_memory_used:,} / {FSQ7State.total_memory_capacity:,}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="16px",
                    ),
                    width="100%",
                    justify="space-between",
                ),
                rx.hstack(
                    rx.text("FAILED TUBES:", color="#00FF00", font_family="monospace", font_size="16px"),
                    rx.text(
                        f"{FSQ7State.failed_tubes}",
                        color=rx.cond(FSQ7State.failed_tubes > 10, "#FF0000", "#FFFF00"),
                        font_family="monospace",
                        font_size="16px",
                    ),
                    width="100%",
                    justify="space-between",
                ),
                spacing="3",
                width="100%",
                padding="20px",
            ),
            spacing="4",
            width="80%",
        ),
        width="100%",
        height="100%",
    )


def memory_display_overlay() -> rx.Component:
    """Memory visualization display."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.center(
        rx.vstack(
            rx.text(
                "MAGNETIC CORE MEMORY",
                color="#00FF00",
                font_family="monospace",
                font_size="24px",
                text_shadow="0 0 10px #00FF00",
            ),
            rx.divider(border_color="#00FF00", width="80%"),
            rx.text(
                f"CAPACITY: {FSQ7State.total_memory_capacity:,} WORDS",
                color="#00FFFF",
                font_family="monospace",
                font_size="16px",
            ),
            rx.text(
                f"IN USE: {FSQ7State.total_memory_used:,} WORDS",
                color="#FFFF00",
                font_family="monospace",
                font_size="16px",
            ),
            rx.progress(
                value=FSQ7State.total_memory_used,
                max=FSQ7State.total_memory_capacity,
                width="80%",
                size="3",
                color_scheme="cyan",
            ),
            rx.text(
                f"{(FSQ7State.total_memory_used/FSQ7State.total_memory_capacity*100):.1f}% UTILIZED",
                color="#00FFFF",
                font_family="monospace",
                font_size="20px",
                font_weight="bold",
            ),
            spacing="4",
            width="80%",
        ),
        width="100%",
        height="100%",
    )
