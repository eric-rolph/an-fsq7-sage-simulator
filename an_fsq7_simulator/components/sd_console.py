"""
SD Console Component - Situation Display Console

Authentic reproduction of the AN/FSQ-7 SAGE Situation Display console
based on Figure 9.2 from IBM DSP 1 (Display System Programming) manual
and Computer History Museum photographs.

Console Layout:
    Top: Off-centering pushbuttons
    Left: Feature selection switches (S20-S25), Category switches (S1-S13)
    Center: Large circular SD CRT (main tactical display)
    Right: DD CRT (data display), Telephone key units (3×6 matrix)
    Bottom: Control knobs (options, reset, alarm)
"""

import reflex as rx


def sd_console() -> rx.Component:
    """
    Render the authentic SD (Situation Display) console.
    
    This is the main air defense operator console featuring:
    - Large circular CRT for radar/tactical display
    - Feature and category selection switches
    - Telephone key units for communication
    - Data display CRT for alphanumeric information
    """
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            # Console header
            rx.hstack(
                rx.text(
                    "SD CONSOLE",
                    font_size="16px",
                    font_weight="bold",
                    color="#00FF00",
                    font_family="monospace",
                    text_shadow="0 0 8px #00FF00",
                ),
                rx.badge(
                    "SITUATION DISPLAY",
                    color_scheme="green",
                    size="2",
                ),
                width="100%",
                justify="between",
            ),
            
            rx.divider(border_color="#00FF00", opacity="0.3"),
            
            # Main console area
            rx.hstack(
                # LEFT SIDE - Feature and Category switches
                rx.vstack(
                    # Bright-Dim switches (S20 & S25)
                    rx.vstack(
                        rx.text(
                            "BRIGHT-DIM",
                            color="#888",
                            font_family="monospace",
                            font_size="9px",
                            font_weight="bold",
                        ),
                        rx.text(
                            "(S20 & S25)",
                            color="#666",
                            font_family="monospace",
                            font_size="8px",
                        ),
                        rx.hstack(
                            rx.box(
                                rx.text("S20", color="#00FF00", font_size="8px"),
                                width="30px",
                                height="60px",
                                background="linear-gradient(180deg, #003300 0%, #001100 100%)",
                                border="1px solid #00FF00",
                                border_radius="3px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                cursor="pointer",
                                _hover={"background": "linear-gradient(180deg, #004400 0%, #002200 100%)"},
                            ),
                            rx.box(
                                rx.text("S25", color="#00FF00", font_size="8px"),
                                width="30px",
                                height="60px",
                                background="linear-gradient(180deg, #003300 0%, #001100 100%)",
                                border="1px solid #00FF00",
                                border_radius="3px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                cursor="pointer",
                                _hover={"background": "linear-gradient(180deg, #004400 0%, #002200 100%)"},
                            ),
                            spacing="2",
                        ),
                        spacing="1",
                    ),
                    
                    # Feature selection switches (S20-S24)
                    rx.vstack(
                        rx.text(
                            "FEATURE SELECT",
                            color="#888",
                            font_family="monospace",
                            font_size="9px",
                            font_weight="bold",
                            margin_top="10px",
                        ),
                        rx.text(
                            "(S20-S24)",
                            color="#666",
                            font_family="monospace",
                            font_size="8px",
                        ),
                        *[
                            rx.box(
                                rx.text(f"S{20+i}", color="#00FF00", font_size="8px"),
                                width="50px",
                                height="25px",
                                background="linear-gradient(90deg, #003300 0%, #001100 100%)",
                                border="1px solid #00FF00",
                                border_radius="3px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                cursor="pointer",
                                _hover={"background": "linear-gradient(90deg, #004400 0%, #002200 100%)"},
                            )
                            for i in range(5)
                        ],
                        spacing="1",
                    ),
                    
                    # Category selection switches (S1-S13)
                    rx.vstack(
                        rx.text(
                            "CATEGORY SELECT",
                            color="#888",
                            font_family="monospace",
                            font_size="9px",
                            font_weight="bold",
                            margin_top="10px",
                        ),
                        rx.text(
                            "(S1-S13)",
                            color="#666",
                            font_family="monospace",
                            font_size="8px",
                        ),
                        *[
                            rx.box(
                                rx.text(f"S{i+1}", color="#00FF00", font_size="8px"),
                                width="50px",
                                height="25px",
                                background="linear-gradient(90deg, #003300 0%, #001100 100%)",
                                border="1px solid #00FF00",
                                border_radius="3px",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                cursor="pointer",
                                _hover={"background": "linear-gradient(90deg, #004400 0%, #002200 100%)"},
                            )
                            for i in range(13)
                        ],
                        spacing="1",
                    ),
                    
                    width="80px",
                    spacing="2",
                    align_items="center",
                ),
                
                # CENTER - Main SD CRT and controls
                rx.vstack(
                    # Off-centering pushbuttons (top)
                    rx.hstack(
                        rx.text(
                            "OFF CENTERING PUSHBUTTONS",
                            color="#888",
                            font_family="monospace",
                            font_size="9px",
                        ),
                        *[
                            rx.box(
                                rx.icon(tag="circle", size=12, color="#00FF00"),
                                width="30px",
                                height="30px",
                                background="rgba(0, 50, 0, 0.3)",
                                border="1px solid #00FF00",
                                border_radius="50%",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                cursor="pointer",
                                _hover={"background": "rgba(0, 80, 0, 0.5)"},
                            )
                            for _ in range(7)
                        ],
                        spacing="2",
                        justify="center",
                        width="100%",
                    ),
                    
                    # Large circular SD CRT (main tactical display)
                    rx.box(
                        rx.box(
                            # Radar sweep and targets
                            rx.box(
                                # Radar grid
                                rx.html(
                                    """
                                    <svg width="100%" height="100%" viewBox="0 0 400 400">
                                        <!-- Grid circles -->
                                        <circle cx="200" cy="200" r="150" stroke="#00FF0040" stroke-width="1" fill="none"/>
                                        <circle cx="200" cy="200" r="100" stroke="#00FF0040" stroke-width="1" fill="none"/>
                                        <circle cx="200" cy="200" r="50" stroke="#00FF0040" stroke-width="1" fill="none"/>
                                        
                                        <!-- Crosshairs -->
                                        <line x1="50" y1="200" x2="350" y2="200" stroke="#00FF0040" stroke-width="1"/>
                                        <line x1="200" y1="50" x2="200" y2="350" stroke="#00FF0040" stroke-width="1"/>
                                        
                                        <!-- Sample target tracks -->
                                        <circle cx="150" cy="120" r="8" fill="#00FF00" opacity="0.8"/>
                                        <text x="155" y="118" fill="#00FF00" font-size="10" font-family="monospace">TGT-1</text>
                                        
                                        <circle cx="280" cy="180" r="8" fill="#FF6600" opacity="0.8"/>
                                        <text x="285" y="178" fill="#FF6600" font-size="10" font-family="monospace">TGT-2</text>
                                        
                                        <circle cx="220" cy="290" r="8" fill="#00FF00" opacity="0.8"/>
                                        <text x="225" y="288" fill="#00FF00" font-size="10" font-family="monospace">TGT-3</text>
                                        
                                        <!-- Intercept vector -->
                                        <line x1="150" y1="120" x2="280" y2="180" stroke="#FFFF00" stroke-width="2" stroke-dasharray="5,5"/>
                                    </svg>
                                    """,
                                ),
                                width="100%",
                                height="100%",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                            ),
                            width="400px",
                            height="400px",
                            border_radius="50%",
                            background="radial-gradient(circle at 45% 45%, rgba(0, 80, 0, 0.4), rgba(0, 20, 0, 0.9))",
                            border="4px solid #00FF00",
                            box_shadow="inset 0 0 40px rgba(0, 255, 0, 0.3), 0 0 20px rgba(0, 255, 0, 0.5)",
                            position="relative",
                            overflow="hidden",
                        ),
                        padding="20px",
                    ),
                    
                    # Bottom controls
                    rx.hstack(
                        # Options knob
                        rx.vstack(
                            rx.box(
                                width="50px",
                                height="50px",
                                border_radius="50%",
                                background="radial-gradient(circle, #333, #111)",
                                border="3px solid #666",
                                box_shadow="inset 0 2px 5px rgba(0,0,0,0.5)",
                                cursor="pointer",
                                _hover={"border_color": "#00FF00"},
                            ),
                            rx.text(
                                "OPTIONS",
                                color="#888",
                                font_family="monospace",
                                font_size="9px",
                            ),
                            spacing="1",
                        ),
                        
                        # Reset knob
                        rx.vstack(
                            rx.box(
                                width="50px",
                                height="50px",
                                border_radius="50%",
                                background="radial-gradient(circle, #333, #111)",
                                border="3px solid #666",
                                box_shadow="inset 0 2px 5px rgba(0,0,0,0.5)",
                                cursor="pointer",
                                _hover={"border_color": "#00FF00"},
                            ),
                            rx.text(
                                "RESET",
                                color="#888",
                                font_family="monospace",
                                font_size="9px",
                            ),
                            spacing="1",
                        ),
                        
                        # Alarm knob
                        rx.vstack(
                            rx.box(
                                width="50px",
                                height="50px",
                                border_radius="50%",
                                background="radial-gradient(circle, #442200, #220000)",
                                border="3px solid #FF6600",
                                box_shadow="inset 0 2px 5px rgba(0,0,0,0.5), 0 0 10px rgba(255, 100, 0, 0.3)",
                                cursor="pointer",
                                _hover={"border_color": "#FF9900"},
                            ),
                            rx.text(
                                "ALARM",
                                color="#FF6600",
                                font_family="monospace",
                                font_size="9px",
                            ),
                            spacing="1",
                        ),
                        
                        spacing="4",
                        justify="center",
                        width="100%",
                    ),
                    
                    spacing="3",
                    align_items="center",
                ),
                
                # RIGHT SIDE - DD CRT and Telephone units
                rx.vstack(
                    # Small DD CRT (Data Display)
                    rx.vstack(
                        rx.text(
                            "DD CRT",
                            color="#888",
                            font_family="monospace",
                            font_size="9px",
                            font_weight="bold",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "TGT-1001",
                                    color="#00FF00",
                                    font_family="monospace",
                                    font_size="10px",
                                ),
                                rx.text(
                                    "ALT: 25000",
                                    color="#00FF00",
                                    font_family="monospace",
                                    font_size="10px",
                                ),
                                rx.text(
                                    "SPD: 450 KTS",
                                    color="#00FF00",
                                    font_family="monospace",
                                    font_size="10px",
                                ),
                                rx.text(
                                    "HDG: 270",
                                    color="#00FF00",
                                    font_family="monospace",
                                    font_size="10px",
                                ),
                                spacing="1",
                            ),
                            width="120px",
                            height="120px",
                            background="radial-gradient(circle at 30% 30%, rgba(0, 60, 0, 0.4), rgba(0, 15, 0, 0.9))",
                            border="3px solid #00FF00",
                            border_radius="5px",
                            box_shadow="inset 0 0 20px rgba(0, 255, 0, 0.3)",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            padding="10px",
                        ),
                        spacing="1",
                    ),
                    
                    # Telephone key units (3 rows × 6 buttons)
                    rx.vstack(
                        rx.text(
                            "TELEPHONE UNITS",
                            color="#888",
                            font_family="monospace",
                            font_size="9px",
                            font_weight="bold",
                            margin_top="15px",
                        ),
                        *[
                            rx.hstack(
                                *[
                                    rx.box(
                                        rx.box(
                                            width="8px",
                                            height="8px",
                                            border_radius="50%",
                                            background="#00FF00",
                                            box_shadow="0 0 5px #00FF00",
                                        ),
                                        rx.box(
                                            width="8px",
                                            height="8px",
                                            border_radius="50%",
                                            background="#FF0000",
                                            box_shadow="0 0 5px #FF0000",
                                        ),
                                        width="30px",
                                        height="30px",
                                        background="rgba(0, 30, 0, 0.5)",
                                        border="1px solid #00FF00",
                                        border_radius="3px",
                                        display="flex",
                                        flex_direction="column",
                                        align_items="center",
                                        justify_content="center",
                                        gap="2px",
                                        cursor="pointer",
                                        _hover={"background": "rgba(0, 50, 0, 0.7)"},
                                    )
                                    for _ in range(6)
                                ],
                                spacing="1",
                            )
                            for _ in range(3)
                        ],
                        spacing="1",
                    ),
                    
                    width="140px",
                    spacing="2",
                    align_items="center",
                ),
                
                spacing="4",
                align_items="start",
                width="100%",
                padding="15px",
            ),
            
            # Console info
            rx.text(
                "Authentic SAGE SD console per IBM DSP 1 (Figure 9.2) and Computer History Museum",
                color="#666",
                font_family="monospace",
                font_size="8px",
                margin_top="10px",
            ),
            
            spacing="3",
            width="100%",
        ),
        
        background="linear-gradient(135deg, rgba(20, 30, 20, 0.9) 0%, rgba(10, 20, 10, 0.95) 100%)",
        padding="20px",
        border="3px solid #00FF00",
        border_radius="15px",
        box_shadow="0 0 30px rgba(0, 255, 0, 0.4)",
    )
