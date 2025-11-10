"""
Memory Banks Component - AUTHENTIC TWO-BANK SYSTEM

Visualizes the TWO separate magnetic core memory banks per Wikipedia:
- Bank 1: 65,536 words (main core) - Octal: 1.00000-1.77777
- Bank 2: 4,096 words (auxiliary core) - Octal: 2.00000-2.07777
"""

import reflex as rx


def memory_banks() -> rx.Component:
    """Memory bank visualization showing AUTHENTIC two-bank architecture."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            rx.heading(
                "MEMORY BANKS (AUTHENTIC)",
                size="6",
                color="#00FF00",
                font_family="monospace",
                text_shadow="0 0 10px #00FF00",
            ),
            
            rx.divider(border_color="#00FF00", opacity="0.3"),
            
            # BANK 1 - Main Core (65,536 words)
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "BANK 1",
                        color="#00FFFF",
                        font_family="monospace",
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.badge(
                        "MAIN CORE",
                        color_scheme="cyan",
                        size="2",
                    ),
                    rx.spacer(),
                    rx.text(
                        "1.00000-1.77777",
                        color="#888",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    width="100%",
                ),
                
                rx.text(
                    f"Capacity: {FSQ7State.memory_capacity_bank1:,} words (64K)",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.text(
                    f"In Use: {FSQ7State.memory_used_bank1:,} words",
                    color="#00FFFF",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.progress(
                    value=FSQ7State.memory_used_bank1,
                    max=FSQ7State.memory_capacity_bank1,
                    width="100%",
                    color_scheme="cyan",
                    size="3",
                ),
                
                rx.text(
                    f"{(FSQ7State.memory_used_bank1/rx.cond(FSQ7State.memory_capacity_bank1 > 0, FSQ7State.memory_capacity_bank1, 1)*100):.1f}% Utilized",
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
            
            # BANK 2 - Auxiliary Core (4,096 words)
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "BANK 2",
                        color="#FFA500",
                        font_family="monospace",
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.badge(
                        "AUX CORE",
                        color_scheme="orange",
                        size="2",
                    ),
                    rx.spacer(),
                    rx.text(
                        "2.00000-2.07777",
                        color="#888",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    width="100%",
                ),
                
                rx.text(
                    f"Capacity: {FSQ7State.memory_capacity_bank2:,} words (4K)",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.text(
                    f"In Use: {FSQ7State.memory_used_bank2:,} words",
                    color="#FFA500",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.progress(
                    value=FSQ7State.memory_used_bank2,
                    max=FSQ7State.memory_capacity_bank2,
                    width="100%",
                    color_scheme="orange",
                    size="3",
                ),
                
                rx.text(
                    f"{(FSQ7State.memory_used_bank2/rx.cond(FSQ7State.memory_capacity_bank2 > 0, FSQ7State.memory_capacity_bank2, 1)*100):.1f}% Utilized",
                    color="#FFA500",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                width="100%",
                spacing="2",
                padding="10px",
                background="rgba(50, 30, 0, 0.3)",
                border="2px solid #FFA500",
                border_radius="5px",
            ),
            
            # Total Memory Statistics
            rx.vstack(
                rx.text(
                    "TOTAL SYSTEM MEMORY",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                
                rx.text(
                    f"Total: {FSQ7State.memory_capacity_bank1 + FSQ7State.memory_capacity_bank2:,} words",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.text(
                    f"Used: {FSQ7State.memory_used_bank1 + FSQ7State.memory_used_bank2:,} words",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                
                rx.text(
                    f"Memory Cycles: {FSQ7State.memory_cycles:,}",
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
            
            # Bank architecture visualization
            rx.vstack(
                rx.text(
                    "BANK ARCHITECTURE",
                    color="#00FF00",
                    font_family="monospace",
                    font_size="12px",
                    font_weight="bold",
                ),
                
                rx.hstack(
                    # Bank 1 visual (larger)
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "BANK 1",
                                color="#00FFFF",
                                font_family="monospace",
                                font_size="9px",
                                font_weight="bold",
                            ),
                            rx.text(
                                "65K",
                                color="#00FFFF",
                                font_family="monospace",
                                font_size="12px",
                            ),
                            spacing="1",
                        ),
                        width="70%",
                        height="80px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="rgba(0, 100, 100, 0.3)",
                        border="2px solid #00FFFF",
                        border_radius="5px",
                        box_shadow="inset 0 0 10px rgba(0, 255, 255, 0.3)",
                    ),
                    
                    # Bank 2 visual (smaller)
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "BANK 2",
                                color="#FFA500",
                                font_family="monospace",
                                font_size="9px",
                                font_weight="bold",
                            ),
                            rx.text(
                                "4K",
                                color="#FFA500",
                                font_family="monospace",
                                font_size="12px",
                            ),
                            spacing="1",
                        ),
                        width="25%",
                        height="80px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background="rgba(100, 50, 0, 0.3)",
                        border="2px solid #FFA500",
                        border_radius="5px",
                        box_shadow="inset 0 0 10px rgba(255, 165, 0, 0.3)",
                    ),
                    
                    width="100%",
                    spacing="2",
                ),
                
                rx.text(
                    "Relative size visualization (Bank 1 is 16× larger)",
                    color="#888",
                    font_family="monospace",
                    font_size="9px",
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
                    "12,000 RPM • ~10ms avg access",
                    color="#FFFF00",
                    font_family="monospace",
                    font_size="11px",
                ),
                rx.text(
                    "Per Chapter 7: CD/OD transfers",
                    color="#888",
                    font_family="monospace",
                    font_size="9px",
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
