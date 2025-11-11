"""
CPU Control Panel Component - AUTHENTIC AN/FSQ-7 Architecture

Displays the AUTHENTIC CPU core state as per AN/FSQ-7 specification:
- 32-bit accumulator with two 15-bit signed halves
- FOUR index registers (ix[0..3]) per §12.3
- Program counter with bank indicator
- Real-time clock (32 Hz) per Wikipedia
- Two memory banks system
"""

import reflex as rx


def cpu_panel() -> rx.Component:
    """
    Render the AUTHENTIC CPU control panel showing registers and execution controls.
    
    This panel displays the REAL AN/FSQ-7 architecture:
        - Accumulator (A): 32-bit word with left/right halves
        - Four Index Registers (ix[0..3]): as per AN/FSQ-7 specification
        - Program Counter (P): With bank indicator (Bank 1 or 2)
        - Real-Time Clock (RTC): 16-bit, 32 Hz
        - Execution controls: Load, Step, Run, Reset
    """
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            # Panel header with authentic badge
            rx.hstack(
                rx.text(
                    "CPU CORE (AUTHENTIC)",
                    font_size="18px",
                    font_weight="bold",
                    color="#00FF00",
                    font_family="monospace",
                    text_shadow="0 0 5px #00FF00",
                ),
                rx.spacer(),
                rx.badge(
                    rx.cond(
                        FSQ7State.cpu_running,
                        "RUNNING",
                        rx.cond(
                            FSQ7State.cpu_halted,
                            "HALTED",
                            "READY"
                        )
                    ),
                    color_scheme=rx.cond(
                        FSQ7State.cpu_running,
                        "green",
                        rx.cond(
                            FSQ7State.cpu_halted,
                            "red",
                            "yellow"
                        )
                    ),
                ),
                width="100%",
                margin_bottom="10px",
            ),
            
            # Register Display - AUTHENTIC ARCHITECTURE
            rx.vstack(
                rx.text(
                    "REGISTERS (Ch. 12)",
                    font_size="12px",
                    font_weight="bold",
                    color="#888",
                    font_family="monospace",
                    margin_bottom="5px",
                ),
                
                # Accumulator (A) - 32-bit with two halves
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "A:",
                            font_family="monospace",
                            color="#00FF00",
                            width="30px",
                            font_weight="bold",
                        ),
                        rx.text(
                            FSQ7State.cpu_accumulator_hex,
                            font_family="monospace",
                            color="#00FF00",
                            font_size="14px",
                            font_weight="bold",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    # Show left and right halves separately
                    rx.hstack(
                        rx.text("", width="30px"),  # Indent
                        rx.text(
                            f"L={FSQ7State.cpu_accumulator_left_hex}",
                            font_family="monospace",
                            color="#888",
                            font_size="10px",
                        ),
                        rx.text(
                            f"R={FSQ7State.cpu_accumulator_right_hex}",
                            font_family="monospace",
                            color="#888",
                            font_size="10px",
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    spacing="1",
                    width="100%",
                ),
                
                # FOUR Index Registers (as per AN/FSQ-7 specification)
                rx.text(
                    "INDEX REGISTERS (§12.3):",
                    font_family="monospace",
                    color="#00FFFF",
                    font_size="11px",
                    font_weight="bold",
                    margin_top="8px",
                ),
                
                # ix[0]
                rx.hstack(
                    rx.text(
                        "ix[0]:",
                        font_family="monospace",
                        color="#00FFFF",
                        width="50px",
                    ),
                    rx.text(
                        FSQ7State.cpu_ix0_hex,
                        font_family="monospace",
                        color="#00FFFF",
                        font_size="13px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_ix0})",
                        font_family="monospace",
                        color="#888",
                        font_size="10px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # ix[1]
                rx.hstack(
                    rx.text(
                        "ix[1]:",
                        font_family="monospace",
                        color="#00FFFF",
                        width="50px",
                    ),
                    rx.text(
                        FSQ7State.cpu_ix1_hex,
                        font_family="monospace",
                        color="#00FFFF",
                        font_size="13px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_ix1})",
                        font_family="monospace",
                        color="#888",
                        font_size="10px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # ix[2]
                rx.hstack(
                    rx.text(
                        "ix[2]:",
                        font_family="monospace",
                        color="#00FFFF",
                        width="50px",
                    ),
                    rx.text(
                        FSQ7State.cpu_ix2_hex,
                        font_family="monospace",
                        color="#00FFFF",
                        font_size="13px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_ix2})",
                        font_family="monospace",
                        color="#888",
                        font_size="10px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # ix[3]
                rx.hstack(
                    rx.text(
                        "ix[3]:",
                        font_family="monospace",
                        color="#00FFFF",
                        width="50px",
                    ),
                    rx.text(
                        FSQ7State.cpu_ix3_hex,
                        font_family="monospace",
                        color="#00FFFF",
                        font_size="13px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_ix3})",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Program Counter (P) with bank indicator
                rx.hstack(
                    rx.text(
                        "P:",
                        font_family="monospace",
                        color="#00FF00",
                        width="30px",
                        margin_top="8px",
                    ),
                    rx.text(
                        FSQ7State.cpu_program_counter_hex,
                        font_family="monospace",
                        color="#00FF00",
                        font_size="14px",
                        font_weight="bold",
                        margin_top="8px",
                    ),
                    rx.badge(
                        f"Bank {FSQ7State.cpu_pc_bank}",
                        color_scheme=rx.cond(FSQ7State.cpu_pc_bank == 1, "green", "orange"),
                        size="1",
                        margin_top="8px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Real-Time Clock (32 Hz)
                rx.hstack(
                    rx.text(
                        "RTC:",
                        font_family="monospace",
                        color="#FFFF00",
                        width="30px",
                        font_weight="bold",
                    ),
                    rx.text(
                        FSQ7State.cpu_rtc_hex,
                        font_family="monospace",
                        color="#FFFF00",
                        font_size="13px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"(32 Hz)",
                        font_family="monospace",
                        color="#888",
                        font_size="10px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                width="100%",
                spacing="1",
                padding="10px",
                background="#0a0a0a",
                border="1px solid #00FF00",
                border_radius="5px",
            ),
            
            # Execution Statistics
            rx.vstack(
                rx.text(
                    "EXECUTION",
                    font_size="12px",
                    font_weight="bold",
                    color="#888",
                    font_family="monospace",
                    margin_bottom="5px",
                    margin_top="10px",
                ),
                
                rx.hstack(
                    rx.text("Instructions:", font_family="monospace", color="#888", font_size="11px"),
                    rx.spacer(),
                    rx.text(
                        f"{FSQ7State.cpu_instruction_count}",
                        font_family="monospace",
                        color="#00FF00",
                        font_size="11px",
                    ),
                    width="100%",
                ),
                
width="100%",
                spacing="1",
                padding="10px",
                background="#0a0a0a",
                border="1px solid #00FF00",
                border_radius="5px",
            ),
            
            # Program Selection - AUTHENTIC PROGRAMS
            rx.vstack(
                rx.text(
                    "PROGRAM SELECT",
                    font_size="12px",
                    font_weight="bold",
                    color="#888",
                    font_family="monospace",
                    margin_bottom="5px",
                    margin_top="10px",
                ),
                
                rx.select(
                    [
                        "Array Sum (Authentic)",
                        "Coordinate Conversion",
                        "Subroutine Example",
                        "RTC Delay Loop",
                        "Display I/O Example",
                    ],
                    value=FSQ7State.selected_program,
                    on_change=FSQ7State.set_selected_program,
                    size="2",
                ),
                
                rx.button(
                    "LOAD PROGRAM",
                    on_click=FSQ7State.load_selected_program,
                    width="100%",
                    color_scheme="green",
                    size="2",
                    disabled=~FSQ7State.system_ready,
                ),
                
                width="100%",
            ),
            
            # Execution Controls
            rx.vstack(
                rx.text(
                    "CONTROLS",
                    font_size="12px",
                    font_weight="bold",
                    color="#888",
                    font_family="monospace",
                    margin_bottom="5px",
                    margin_top="10px",
                ),
                
                rx.hstack(
                    rx.button(
                        "STEP",
                        on_click=FSQ7State.cpu_step,
                        width="48%",
                        color_scheme="blue",
                        size="2",
                        disabled=FSQ7State.cpu_halted | FSQ7State.cpu_running | ~FSQ7State.system_ready,
                    ),
                    rx.button(
                        "RUN",
                        on_click=FSQ7State.cpu_run,
                        width="48%",
                        color_scheme="green",
                        size="2",
                        disabled=FSQ7State.cpu_halted | FSQ7State.cpu_running | ~FSQ7State.system_ready,
                    ),
                    width="100%",
                    justify="between",
                ),
                
                rx.button(
                    "RESET CPU",
                    on_click=FSQ7State.cpu_reset,
                    width="100%",
                    color_scheme="red",
                    size="2",
                    variant="outline",
                    disabled=~FSQ7State.system_ready,
                ),
                
                width="100%",
            ),
            
            # Authentic Architecture Indicator
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "✓",
                            font_size="16px",
                            color="#00FF00",
                        ),
                        rx.text(
                            "AUTHENTIC Q-7 ARCHITECTURE",
                            font_size="10px",
                            font_family="monospace",
                            color="#00FFFF",
                            font_weight="bold",
                        ),
                        spacing="1",
                    ),
                    rx.text(
                        "• 4 Index Registers (§12.3)",
                        font_size="9px",
                        font_family="monospace",
                        color="#888",
                    ),
                    rx.text(
                        "• Two-half arithmetic (§12.1)",
                        font_size="9px",
                        font_family="monospace",
                        color="#888",
                    ),
                    rx.text(
                        "• 2 Memory Banks (65K+4K)",
                        font_size="9px",
                        font_family="monospace",
                        color="#888",
                    ),
                    rx.text(
                        "• Real-time clock (32 Hz)",
                        font_size="9px",
                        font_family="monospace",
                        color="#888",
                    ),
                    spacing="1",
                ),
                padding="8px",
                margin_top="10px",
                background="linear-gradient(90deg, #001a1a 0%, #003333 100%)",
                border="1px solid #00FFFF",
                border_radius="5px",
            ),
            
            # Info text
            rx.text(
                "Implements AN/FSQ-7 specification architecture: effective_addr = instr.addr + ix[instr.ix_sel]",
                font_size="9px",
                font_family="monospace",
                color="#666",
                margin_top="10px",
                line_height="1.3",
            ),
            
            width="100%",
            spacing="2",
        ),
        padding="15px",
        background="#1a1a1a",
        border="2px solid #00FF00",
        border_radius="10px",
        box_shadow="0 0 20px rgba(0, 255, 0, 0.3)",
    )
