"""
Memory Banks Component

Visualizes the magnetic core memory system.
"""

import reflex as rx


def memory_banks() -> rx.Component:
    """Memory bank visualization."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            rx.heading(
                "MEMORY BANKS",
                size="6",
                color="#00FF00",
                font_family="monospace",
                text_shadow="0 0 10px #00FF00",
            ),
            
            rx.divider(border_color="#00FF00", opacity="0.3"),
            
            rx.vstack(
                rx.text(
                    "MAGNETIC CORE MEMORY",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                
                rx.text(
                    f"Capacity: {FSQ7State.memory_capacity:,} words",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.text(
                    f"In Use: {FSQ7State.memory_used:,} words",
                    color="#00FFFF",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.text(
                    f"Cycles: {FSQ7State.memory_cycles:,}",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.progress(
                    value=FSQ7State.memory_used,
                    max=FSQ7State.memory_capacity,
                    width="100%",
                    color_scheme="cyan",
                    size="3",
                ),
                
                rx.text(
                    f"{(FSQ7State.memory_used/FSQ7State.memory_capacity*100):.1f}% Utilized",
                    color="#00FFFF",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                width="100%",
                spacing="2",
                padding="10px",
                background="rgba(0, 50, 50, 0.3)",
                border="2px solid #00FFFF",
                border_radius="5px",
            ),
            
            # Memory banks grid visualization
            rx.vstack(
                rx.text(
                    "BANK STATUS",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                
                # Grid of 16 memory banks (4x4)
                rx.grid(
                    *[
                        rx.box(
                            rx.text(
                                f"B{i:02d}",
                                color="#00FF00",
                                font_family="monospace",
                                font_size="10px",
                            ),
                            width="60px",
                            height="60px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            background=f"rgba(0, {50 + (i * 10) % 200}, 0, 0.3)",
                            border="1px solid #00FF00",
                            border_radius="3px",
                            box_shadow="inset 0 0 5px rgba(0, 255, 0, 0.5)",
                        )
                        for i in range(16)
                    ],
                    columns="4",
                    spacing="2",
                ),
                
                width="100%",
                spacing="2",
                padding="10px",
                background="rgba(0, 50, 0, 0.2)",
                border="2px solid #00FF00",
                border_radius="5px",
            ),
            
            # Drum storage indicator
            rx.vstack(
                rx.text(
                    "DRUM STORAGE",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                rx.hstack(
                    rx.box(
                        width="20px",
                        height="20px",
                        background="#00FF00",
                        border_radius="50%",
                        box_shadow="0 0 10px #00FF00",
                        animation="pulse 2s infinite",
                    ),
                    rx.text(
                        "ROTATING",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="11px",
                    ),
                    spacing="2",
                ),
                rx.text(
                    "12,000 RPM",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                width="100%",
                spacing="2",
                padding="10px",
                background="rgba(0, 50, 0, 0.2)",
                border="2px solid #00FF00",
                border_radius="5px",
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
