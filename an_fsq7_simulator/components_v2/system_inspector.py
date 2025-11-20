"""
System Inspector Overlay for Priority 3

Provides transparency into the SAGE computer's internal state:
- CPU registers and execution state
- Memory bank activity
- Processing queues and bottlenecks

Toggle with Shift+I keyboard shortcut
"""

import reflex as rx
from typing import List


def inspector_metric_box(
    label: str,
    value: str,
    color: str = "#00ff00",
    unit: str = ""
) -> rx.Component:
    """
    Single metric display box
    
    Args:
        label: Metric name
        value: Current value (as string or Var)
        color: Text color for value
        unit: Optional unit suffix
    """
    return rx.box(
        rx.text(
            label,
            color="#888888",
            font_size="0.7rem",
            font_family="'Courier New', monospace",
            margin_bottom="0.25rem"
        ),
        rx.text(
            f"{value}{unit}" if unit else value,
            color=color,
            font_size="1rem",
            font_family="'Courier New', monospace",
            font_weight="bold"
        ),
        padding="0.5rem",
        background="rgba(0, 0, 0, 0.8)",
        border="1px solid #00ff00",
        border_radius="4px"
    )


def cpu_state_panel(
    accumulator: int = 0,
    index_register: int = 0,
    program_counter: int = 0,
    current_instruction: str = "IDLE",
    memory_address: int = 0,
    instruction_queue_depth: int = 0
) -> rx.Component:
    """
    CPU State Panel - Shows registers and current execution
    
    Args:
        accumulator: Current value of A register
        index_register: Current value of I register
        program_counter: Current value of P register
        current_instruction: Human-readable current instruction
        memory_address: Memory address being accessed
        instruction_queue_depth: Number of instructions waiting
    """
    return rx.box(
        rx.heading(
            "CPU STATE",
            size="3",
            color="#00ff00",
            font_family="'Courier New', monospace",
            margin_bottom="0.75rem"
        ),
        
        # Registers
        rx.grid(
            inspector_metric_box("ACCUMULATOR (A)", accumulator.to(str)),
            inspector_metric_box("INDEX (I)", index_register.to(str)),
            inspector_metric_box("PC", program_counter.to(str)),
            columns="3",
            spacing="2",
            margin_bottom="0.75rem"
        ),
        
        # Current execution
        rx.box(
            rx.text("CURRENT INSTRUCTION", color="#888888", font_size="0.7rem", margin_bottom="0.25rem"),
            rx.text(
                current_instruction,
                color="#ffff00",
                font_size="1rem",
                font_family="'Courier New', monospace",
                font_weight="bold"
            ),
            padding="0.5rem",
            background="rgba(0, 0, 0, 0.9)",
            border="1px solid #ffff00",
            border_radius="4px",
            margin_bottom="0.75rem"
        ),
        
        # Memory and queue
        rx.grid(
            inspector_metric_box("MEMORY ADDR", memory_address.to(str)),
            inspector_metric_box(
                "INSTR QUEUE",
                instruction_queue_depth.to(str),
                color=rx.cond(instruction_queue_depth > 8, "#ff0000", "#00ff00")
            ),
            columns="2",
            spacing="2"
        ),
        
        padding="1rem",
        background="rgba(0, 20, 0, 0.95)",
        border="2px solid #00ff00",
        border_radius="8px",
        margin_bottom="1rem"
    )


def memory_bank_indicator(
    bank_id: int,
    active: bool = False,
    program_name: str = "",
    access_count: int = 0
) -> rx.Component:
    """
    Individual memory bank visualization
    
    Args:
        bank_id: Bank identifier (0-15)
        active: Currently being accessed
        program_name: Name of loaded program
        access_count: Number of accesses this second
    """
    return rx.box(
        rx.text(
            f"BANK {bank_id}",
            color=rx.cond(active, "#ffff00", "#888888"),
            font_size="0.7rem",
            font_family="'Courier New', monospace",
            font_weight="bold",
            margin_bottom="0.25rem"
        ),
        rx.cond(
            program_name != "",
            rx.text(
                program_name,
                color="#00ff00",
                font_size="0.6rem",
                font_family="'Courier New', monospace"
            ),
            rx.text(
                "EMPTY",
                color="#444444",
                font_size="0.6rem",
                font_family="'Courier New', monospace",
                font_style="italic"
            )
        ),
        rx.cond(
            active,
            rx.text(
                f"{access_count} ops/s",
                color="#ff8800",
                font_size="0.6rem",
                font_family="'Courier New', monospace"
            ),
            rx.box()
        ),
        padding="0.5rem",
        background=rx.cond(active, "rgba(255, 255, 0, 0.2)", "rgba(0, 0, 0, 0.8)"),
        border=rx.cond(active, "2px solid #ffff00", "1px solid #444444"),
        border_radius="4px",
        text_align="center"
    )


def memory_visualization_panel(
    memory_banks: List = []
) -> rx.Component:
    """
    Memory Bank Visualization - Shows which banks are active
    
    Args:
        memory_banks: List of memory bank states
    """
    return rx.box(
        rx.heading(
            "MEMORY BANKS",
            size="3",
            color="#00ff00",
            font_family="'Courier New', monospace",
            margin_bottom="0.75rem"
        ),
        
        rx.text(
            "16 banks × 4K words each = 64K total",
            color="#888888",
            font_size="0.7rem",
            font_family="'Courier New', monospace",
            margin_bottom="0.75rem"
        ),
        
        # Grid of memory banks
        rx.grid(
            *[
                memory_bank_indicator(
                    bank_id=i,
                    active=False,
                    program_name="",
                    access_count=0
                )
                for i in range(16)
            ],
            columns="4",
            spacing="2"
        ),
        
        padding="1rem",
        background="rgba(0, 20, 0, 0.95)",
        border="2px solid #00ff00",
        border_radius="8px",
        margin_bottom="1rem"
    )


def queue_indicator(
    queue_name: str,
    depth: int,
    max_depth: int,
    items_per_second: int = 0
) -> rx.Component:
    """
    Single queue status indicator
    
    Args:
        queue_name: Human-readable queue name
        depth: Current queue depth
        max_depth: Maximum queue capacity
        items_per_second: Processing rate
    """
    # Calculate thresholds for color coding (can't do division with Reflex Vars in template)
    high_threshold = int(max_depth * 0.8)  # 80%
    medium_threshold = int(max_depth * 0.5)  # 50%
    
    return rx.box(
        rx.hstack(
            rx.text(
                queue_name,
                color="#00ff00",
                font_size="0.8rem",
                font_family="'Courier New', monospace",
                font_weight="bold"
            ),
            rx.spacer(),
            rx.text(
                rx.cond(
                    depth > 0,
                    depth.to(str) + f"/{max_depth}",
                    f"0/{max_depth}"
                ),
                color=rx.cond(
                    depth > high_threshold,
                    "#ff0000",
                    rx.cond(depth > medium_threshold, "#ffff00", "#00ff00")
                ),
                font_size="0.8rem",
                font_family="'Courier New', monospace",
                font_weight="bold"
            ),
            width="100%",
            margin_bottom="0.5rem"
        ),
        
        # Progress bar (simplified - just show color based on depth)
        rx.box(
            rx.box(
                width=rx.cond(depth > 0, "100%", "0%"),  # Simplified visualization
                height="100%",
                background=rx.cond(
                    depth > high_threshold,
                    "#ff0000",
                    rx.cond(depth > medium_threshold, "#ffff00", "#00ff00")
                ),
                transition="width 0.3s ease"
            ),
            width="100%",
            height="8px",
            background="rgba(0, 0, 0, 0.5)",
            border="1px solid #444444",
            border_radius="4px",
            margin_bottom="0.5rem"
        ),
        
        rx.text(
            rx.cond(
                items_per_second > 0,
                "Processing: " + items_per_second.to(str) + " items/sec",
                "Processing: 0 items/sec"
            ),
            color="#888888",
            font_size="0.65rem",
            font_family="'Courier New', monospace"
        ),
        
        padding="0.75rem",
        background="rgba(0, 0, 0, 0.8)",
        border="1px solid #00ff00",
        border_radius="4px"
    )


def queue_inspector_panel(
    radar_queue_depth: int = 0,
    track_queue_depth: int = 0,
    display_queue_depth: int = 0,
    radar_processing_rate: int = 0,
    track_processing_rate: int = 0,
    display_processing_rate: int = 0
) -> rx.Component:
    """
    Queue Inspector Panel - Shows processing queues and bottlenecks
    
    Args:
        radar_queue_depth: Radar returns awaiting correlation
        track_queue_depth: Tracks awaiting classification
        display_queue_depth: Screen updates waiting to render
        radar_processing_rate: Radar returns processed per second
        track_processing_rate: Tracks processed per second
        display_processing_rate: Display updates per second
    """
    return rx.box(
        rx.heading(
            "PROCESSING QUEUES",
            size="3",
            color="#00ff00",
            font_family="'Courier New', monospace",
            margin_bottom="0.75rem"
        ),
        
        rx.text(
            "Monitor system bottlenecks",
            color="#888888",
            font_size="0.7rem",
            font_family="'Courier New', monospace",
            margin_bottom="0.75rem"
        ),
        
        # Queue indicators
        rx.vstack(
            queue_indicator(
                "RADAR INPUT",
                radar_queue_depth,
                100,
                radar_processing_rate
            ),
            queue_indicator(
                "TRACK PROCESSING",
                track_queue_depth,
                50,
                track_processing_rate
            ),
            queue_indicator(
                "DISPLAY UPDATE",
                display_queue_depth,
                30,
                display_processing_rate
            ),
            spacing="3",
            width="100%"
        ),
        
        # Warning message
        rx.cond(
            (radar_queue_depth > 80) | (track_queue_depth > 40) | (display_queue_depth > 24),
            rx.box(
                rx.text(
                    "⚠ BOTTLENECK DETECTED",
                    color="#ff0000",
                    font_size="0.9rem",
                    font_family="'Courier New', monospace",
                    font_weight="bold"
                ),
                rx.text(
                    "System processing capacity exceeded. Consider reducing simulation speed.",
                    color="#ffaa00",
                    font_size="0.7rem",
                    font_family="'Courier New', monospace"
                ),
                padding="0.75rem",
                background="rgba(255, 0, 0, 0.2)",
                border="2px solid #ff0000",
                border_radius="4px",
                margin_top="0.75rem"
            ),
            rx.box()
        ),
        
        padding="1rem",
        background="rgba(0, 20, 0, 0.95)",
        border="2px solid #00ff00",
        border_radius="8px"
    )


def simulation_metrics_panel(
    active_tracks: int = 0,
    active_interceptors: int = 0,
    world_time: int = 0,
    speed_multiplier: float = 1.0
) -> rx.Component:
    """
    Real-time Simulation Metrics
    
    Args:
        active_tracks: Number of active radar tracks
        active_interceptors: Number of active interceptors
        world_time: Current simulation time in ms
        speed_multiplier: Current simulation speed
    """
    return rx.box(
        rx.heading(
            "SIMULATION METRICS",
            size="3",
            color="#00ff00",
            font_family="'Courier New', monospace",
            margin_bottom="0.75rem"
        ),
        
        rx.grid(
            inspector_metric_box("ACTIVE TRACKS", active_tracks.to(str)),
            inspector_metric_box("INTERCEPTORS", active_interceptors.to(str)),
            inspector_metric_box("SIM SPEED", speed_multiplier.to(str) + "x"),
            inspector_metric_box("WORLD TIME", (world_time / 1000).to(str) + "s"),
            columns="2",
            spacing="2"
        ),
        
        padding="1rem",
        background="rgba(0, 20, 0, 0.95)",
        border="2px solid #00ff00",
        border_radius="8px",
        margin_bottom="1rem"
    )


def system_inspector_overlay(
    show: bool = False,
    accumulator: int = 0,
    index_register: int = 0,
    program_counter: int = 0,
    current_instruction: str = "IDLE",
    memory_address: int = 0,
    instruction_queue_depth: int = 0,
    radar_queue_depth: int = 0,
    track_queue_depth: int = 0,
    display_queue_depth: int = 0,
    radar_processing_rate: int = 0,
    track_processing_rate: int = 0,
    display_processing_rate: int = 0,
    active_tracks: int = 0,
    active_interceptors: int = 0,
    world_time: int = 0,
    speed_multiplier: float = 1.0,
    on_close = None
) -> rx.Component:
    """
    Complete System Inspector Overlay
    
    Semi-transparent overlay that doesn't block radar view.
    Toggle with Shift+I keyboard shortcut.
    
    Args:
        show: Whether overlay is visible
        accumulator: CPU accumulator value
        index_register: CPU index register value
        program_counter: CPU program counter
        current_instruction: Current CPU instruction
        memory_address: Memory address being accessed
        instruction_queue_depth: Instruction queue depth
        radar_queue_depth: Radar input queue depth
        track_queue_depth: Track processing queue depth
        display_queue_depth: Display update queue depth
        radar_processing_rate: Radar processing rate
        track_processing_rate: Track processing rate
        display_processing_rate: Display processing rate
        active_tracks: Number of active radar tracks
        active_interceptors: Number of active interceptors
        world_time: Current simulation time in ms
        speed_multiplier: Current simulation speed
        on_close: Callback to close overlay
    """
    return rx.cond(
        show,
        rx.box(
            # Header with close button
            rx.hstack(
                rx.heading(
                    "🔍 SYSTEM INSPECTOR",
                    size="4",
                    color="#00ff00",
                    font_family="'Courier New', monospace"
                ),
                rx.spacer(),
                rx.button(
                    "✕ CLOSE (Shift+I)",
                    on_click=on_close if on_close else lambda: None,
                    color_scheme="red",
                    size="2",
                    cursor="pointer"
                ),
                width="100%",
                margin_bottom="1rem"
            ),
            
            # Scrollable content area
            rx.box(
                simulation_metrics_panel(
                    active_tracks=active_tracks,
                    active_interceptors=active_interceptors,
                    world_time=world_time,
                    speed_multiplier=speed_multiplier
                ),

                cpu_state_panel(
                    accumulator=accumulator,
                    index_register=index_register,
                    program_counter=program_counter,
                    current_instruction=current_instruction,
                    memory_address=memory_address,
                    instruction_queue_depth=instruction_queue_depth
                ),
                
                memory_visualization_panel(),
                
                queue_inspector_panel(
                    radar_queue_depth=radar_queue_depth,
                    track_queue_depth=track_queue_depth,
                    display_queue_depth=display_queue_depth,
                    radar_processing_rate=radar_processing_rate,
                    track_processing_rate=track_processing_rate,
                    display_processing_rate=display_processing_rate
                ),
                
                overflow_y="auto",
                max_height="calc(100vh - 100px)"
            ),
            
            # Overlay container
            position="fixed",
            top="20px",
            right="20px",
            width="500px",
            max_height="calc(100vh - 40px)",
            padding="1.5rem",
            background="rgba(0, 10, 0, 0.98)",
            border="3px solid #00ff00",
            border_radius="12px",
            box_shadow="0 0 30px rgba(0, 255, 0, 0.5)",
            z_index="9999"
        ),
        rx.box()  # Empty when not shown
    )
