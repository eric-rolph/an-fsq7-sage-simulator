"""
Execution Trace Panel Component - Shows CPU program execution in real-time

This panel answers the question: "Did the CPU run? What did it do?"

Features:
- Program header with status (Idle/Running/Done/Error)
- Step-by-step instruction trace
- Register state after each step
- Final result banner
- Speed controls (Real-time/Slow/Step)
"""

import reflex as rx
from typing import List, Dict, Optional
from ..state_model import CpuTrace, ExecutionStep, CpuRegisters


def execution_step_row(step: ExecutionStep, index: int) -> rx.Component:
    """Render a single execution step"""
    return rx.box(
        rx.hstack(
            # Step number
            rx.text(
                f"#{step.step_num}",
                font_family="'Courier New', monospace",
                color="#00ff00",
                width="40px",
                font_size="0.9rem",
            ),
            # Instruction text
            rx.text(
                step.instruction_text,
                font_family="'Courier New', monospace",
                color="#88ff88",
                flex="1",
                font_size="0.9rem",
            ),
            spacing="2",
            width="100%",
        ),
        # Result text (indented)
        rx.box(
            rx.text(
                f"→ {step.result_text}",
                font_family="'Courier New', monospace",
                color="#ffff88",
                font_size="0.85rem",
                padding_left="50px",
            ),
            padding_y="0.25rem",
        ),
        padding_y="0.5rem",
        border_bottom="1px solid #003300",
        _hover={
            "background": "#001100",
        },
    )


def register_view(registers: CpuRegisters) -> rx.Component:
    """Display current register state"""
    return rx.box(
        rx.heading("REGISTERS", size="3", color="#00ff00", margin_bottom="0.5rem"),
        rx.grid(
            # Accumulator
            rx.box(
                rx.text("A:", font_weight="bold", color="#00ff00"),
                rx.text(
                    f"{registers.A:08X}",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                ),
            ),
            # B register
            rx.box(
                rx.text("B:", font_weight="bold", color="#00ff00"),
                rx.text(
                    f"{registers.B:08X}",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                ),
            ),
            # Program counter
            rx.box(
                rx.text("PC:", font_weight="bold", color="#00ff00"),
                rx.text(
                    f"{registers.PC:04X}",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                ),
            ),
            # Flags
            rx.box(
                rx.text("FLAGS:", font_weight="bold", color="#00ff00"),
                rx.text(
                    f"{registers.FLAGS:02X}",
                    font_family="'Courier New', monospace",
                    color="#88ff88",
                ),
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def speed_controls() -> rx.Component:
    """Speed control buttons for execution"""
    return rx.hstack(
        rx.text("SPEED:", color="#00ff00", font_weight="bold"),
        rx.button(
            "Real-time",
            on_click=lambda: None,  # TODO: Wire to state
            background="#003300",
            color="#00ff00",
            border="1px solid #00ff00",
            _hover={"background": "#005500"},
            size="1",
        ),
        rx.button(
            "Slow",
            on_click=lambda: None,  # TODO: Wire to state
            background="#003300",
            color="#00ff00",
            border="1px solid #00ff00",
            _hover={"background": "#005500"},
            size="1",
        ),
        rx.button(
            "Step",
            on_click=lambda: None,  # TODO: Wire to state
            background="#003300",
            color="#00ff00",
            border="1px solid #00ff00",
            _hover={"background": "#005500"},
            size="1",
        ),
        spacing="2",
        margin_bottom="1rem",
    )


def program_header(trace: CpuTrace) -> rx.Component:
    """Program info header"""
    status_colors = {
        "Idle": "#888888",
        "Running": "#ffff00",
        "Done": "#00ff00",
        "Error": "#ff0000",
    }
    
    status_color = status_colors.get(trace.status, "#888888")
    
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text("PROGRAM", font_size="0.8rem", color="#888888"),
                rx.text(
                    trace.program_name,
                    font_size="1.1rem",
                    font_weight="bold",
                    color="#00ff00",
                    font_family="'Courier New', monospace",
                ),
                spacing="0",
                align_items="start",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text("STATUS", font_size="0.8rem", color="#888888"),
                rx.badge(
                    trace.status,
                    color_scheme="green" if trace.status == "Done" else "yellow",
                    font_size="0.9rem",
                ),
                spacing="0",
                align_items="end",
            ),
            width="100%",
            align_items="start",
        ),
        rx.text(
            f"Runtime: {trace.elapsed_ms}ms" if trace.elapsed_ms else "Not started",
            font_size="0.85rem",
            color="#888888",
            margin_top="0.5rem",
        ),
        padding="1rem",
        background="#001100",
        border="1px solid #00ff00",
        border_radius="4px",
        margin_bottom="1rem",
    )


def final_result_banner(trace: CpuTrace) -> rx.Component:
    """Show final computation result"""
    if trace.status != "Done" or not trace.final_result:
        return rx.box()  # Empty if not done
    
    return rx.box(
        rx.heading("✓ EXECUTION COMPLETE", size="4", color="#00ff00"),
        rx.text(
            f"Final result: {trace.final_result.get('value', 'N/A')}",
            font_size="1.2rem",
            color="#ffff00",
            font_family="'Courier New', monospace",
            margin_y="0.5rem",
        ),
        rx.text(
            f"Stored at address: {trace.final_result.get('address', 'N/A')}",
            font_size="0.9rem",
            color="#88ff88",
            font_family="'Courier New', monospace",
        ),
        padding="1.5rem",
        background="#002200",
        border="2px solid #00ff00",
        border_radius="4px",
        text_align="center",
        margin_top="1rem",
    )


def execution_trace_panel(trace: CpuTrace) -> rx.Component:
    """
    Main Execution Trace Panel
    
    Shows real-time CPU execution with:
    - Program header (name, status, elapsed time)
    - Scrollable step list
    - Register state
    - Final result banner
    - Speed controls
    """
    return rx.box(
        # Panel header
        rx.heading(
            "EXECUTION TRACE",
            size="5",
            color="#00ff00",
            margin_bottom="1rem",
            font_family="'Courier New', monospace",
        ),
        
        # Program header
        program_header(trace),
        
        # Speed controls
        speed_controls(),
        
        # Step list (scrollable)
        rx.box(
            rx.heading("INSTRUCTION TRACE", size="3", color="#00ff00", margin_bottom="0.5rem"),
            rx.box(
                # Render all steps
                rx.cond(
                    len(trace.steps) > 0,
                    rx.vstack(
                        *[execution_step_row(step, i) for i, step in enumerate(trace.steps)],
                        spacing="0",
                        width="100%",
                    ),
                    rx.text(
                        "No execution steps yet. Load and run a program.",
                        color="#888888",
                        font_style="italic",
                        padding="1rem",
                    ),
                ),
                max_height="300px",
                overflow_y="auto",
                background="#000000",
                border="1px solid #003300",
                border_radius="4px",
                padding="0.5rem",
            ),
            margin_bottom="1rem",
        ),
        
        # Register view
        rx.cond(
            len(trace.steps) > 0,
            register_view(trace.steps[-1].registers if trace.steps else CpuRegisters()),
            rx.box(),
        ),
        
        # Final result banner
        final_result_banner(trace),
        
        # Test button (TODO: Wire to actual CPU execution)
        rx.button(
            "▶ Run Test Program",
            on_click=lambda: None,  # TODO: Wire to run_cpu_program
            background="#003300",
            color="#00ff00",
            border="2px solid #00ff00",
            width="100%",
            margin_top="1rem",
            size="3",
            _hover={"background": "#005500"},
        ),
        
        # Panel styling
        width="100%",
        max_width="500px",
        padding="1.5rem",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        height="100vh",
        overflow_y="auto",
    )


def execution_trace_panel_compact(trace: CpuTrace) -> rx.Component:
    """Compact version for embedding in main layout"""
    return rx.box(
        rx.heading("CPU TRACE", size="4", color="#00ff00", margin_bottom="0.5rem"),
        
        # Status indicator
        rx.hstack(
            rx.text("Status:", color="#888888", font_size="0.9rem"),
            rx.badge(trace.status, color_scheme="green" if trace.status == "Done" else "yellow"),
            spacing="2",
        ),
        
        # Last few steps only
        rx.box(
            rx.vstack(
                *[execution_step_row(step, i) for i, step in enumerate(trace.steps[-5:])],
                spacing="0",
                width="100%",
            ) if trace.steps else rx.text("Idle", color="#888888"),
            max_height="200px",
            overflow_y="auto",
            background="#000000",
            border="1px solid #003300",
            border_radius="4px",
            padding="0.5rem",
            margin_y="0.5rem",
        ),
        
        # Quick result
        rx.cond(
            trace.status == "Done",
            rx.text(
                f"Result: {trace.final_result.get('value', 'N/A')}",
                color="#ffff00",
                font_family="'Courier New', monospace",
            ),
            rx.box(),
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )
