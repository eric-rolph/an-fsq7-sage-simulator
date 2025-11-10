"""
CPU Control Panel Component

Displays the CPU core state and provides controls for program execution.
Shows the critical registers including the Index Register (I) for indexed addressing.
"""

import reflex as rx


def cpu_panel() -> rx.Component:
    """
    Render the CPU control panel showing registers and execution controls.
    
    This panel displays:
        - Accumulator (A): Main computation register
        - Index Register (I): Used for indexed addressing (Chapter 12.3)
        - Program Counter (P): Current instruction address
        - Execution controls: Load, Step, Run, Reset
    """
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            # Panel header
            rx.hstack(
                rx.text(
                    "CPU CORE",
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
            
            # Register Display
            rx.vstack(
                rx.text(
                    "REGISTERS",
                    font_size="12px",
                    font_weight="bold",
                    color="#888",
                    font_family="monospace",
                    margin_bottom="5px",
                ),
                
                # Accumulator (A)
                rx.hstack(
                    rx.text(
                        "A:",
                        font_family="monospace",
                        color="#00FF00",
                        width="30px",
                    ),
                    rx.text(
                        f"{FSQ7State.cpu_accumulator:08X}",
                        font_family="monospace",
                        color="#00FF00",
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_accumulator})",
                        font_family="monospace",
                        color="#888",
                        font_size="11px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Index Register (I) - CRITICAL for Chapter 12.5!
                rx.hstack(
                    rx.text(
                        "I:",
                        font_family="monospace",
                        color="#00FFFF",  # Cyan to highlight
                        width="30px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"{FSQ7State.cpu_index_reg:04X}",
                        font_family="monospace",
                        color="#00FFFF",
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_index_reg})",
                        font_family="monospace",
                        color="#888",
                        font_size="11px",
                    ),
                    width="100%",
                    spacing="2",
                ),
                
                # Program Counter (P)
                rx.hstack(
                    rx.text(
                        "P:",
                        font_family="monospace",
                        color="#00FF00",
                        width="30px",
                    ),
                    rx.text(
                        f"{FSQ7State.cpu_program_counter:04X}",
                        font_family="monospace",
                        color="#00FF00",
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.text(
                        f"({FSQ7State.cpu_program_counter})",
                        font_family="monospace",
                        color="#888",
                        font_size="11px",
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
                
                rx.hstack(
                    rx.text("Cycles:", font_family="monospace", color="#888", font_size="11px"),
                    rx.spacer(),
                    rx.text(
                        f"{FSQ7State.cpu_cycle_count}",
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
            
            # Program Selection
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
                        "Array Sum (Ch 12.5)",
                        "Array Search (Ch 12.5)",
                        "Array Copy (Ch 12.5)",
                        "Matrix Init (Ch 12.5)",
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
            
            # Indexed Addressing Indicator
            rx.box(
                rx.hstack(
                    rx.text(
                        "⚡",
                        font_size="16px",
                    ),
                    rx.text(
                        "INDEXED ADDRESSING ENABLED",
                        font_size="10px",
                        font_family="monospace",
                        color="#00FFFF",
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
                "Index Register (I) implements Chapter 12.3 indexed addressing: effective_addr = base + I",
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
