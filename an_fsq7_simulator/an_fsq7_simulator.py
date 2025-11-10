"""
AN/FSQ-7 SAGE Computer Simulator

This module contains the main application logic for simulating the AN/FSQ-7,
the massive vacuum tube computer used in the SAGE (Semi-Automatic Ground Environment)
air defense system during the Cold War era.

Features:
- Vintage CRT display with phosphor glow effects
- Interactive control panels with switches and indicators
- Light gun simulation for display interaction
- Magnetic core memory visualization
- Vacuum tube operation indicators
- Real-time radar tracking simulation
- **AUTHENTIC CPU CORE per Ulmann Chapter 12:**
  * 32-bit words with two 15-bit signed halves
  * Four index registers (ix[0..3])
  * Two memory banks (65K + 4K)
  * Parallel left/right arithmetic
  * Real-time clock (32 Hz)
  * Full instruction set with dispatch table
  * I/O mapped to displays
- **AUTHENTIC SD CONSOLE per IBM DSP 1:**
  * Large circular CRT display
  * Feature and category selection switches
  * Off-centering pushbuttons
  * DD CRT (data display)
  * Telephone key units (3×6 matrix)
"""

import reflex as rx
from typing import List, Dict, Tuple, Optional
import math
import random
from datetime import datetime
import time

# Import custom components
from .components.crt_display import crt_display
from .components.control_panel import control_panel
from .components.system_status import system_status
from .components.memory_banks import memory_banks
from .components.radar_scope import radar_scope
from .components.cpu_panel import cpu_panel
from .components.sd_console import sd_console

# Import AUTHENTIC CPU core and programs (per Ulmann Chapter 12)
from .cpu_core_authentic import FSQ7CPU, FSQ7Word, MemoryBanks, IOHandler
from .sage_programs_authentic import (
    array_sum_authentic,
    coordinate_conversion,
    subroutine_example,
    rtc_delay_loop,
    display_io_example
)


class RadarTarget:
    """Represents a radar target being tracked."""
    def __init__(self, x: float, y: float, heading: float, speed: float, altitude: int, target_id: str):
        self.x = x
        self.y = y
        self.heading = heading
        self.speed = speed
        self.altitude = altitude
        self.target_id = target_id
        self.threat_level = "UNKNOWN"


class FSQ7State(rx.State):
    """Main state management for the AN/FSQ-7 simulator."""
    
    # System power and status
    power_on: bool = False
    system_ready: bool = False
    startup_progress: int = 0
    
    # Vacuum tube statistics
    total_tubes: int = 58000
    active_tubes: int = 0
    failed_tubes: int = 0
    tube_temperature: float = 0.0
    
    # Memory system (TWO BANKS per Wikipedia)
    memory_capacity_bank1: int = 65536  # Bank 1: 65K words (main core)
    memory_capacity_bank2: int = 4096   # Bank 2: 4K words (auxiliary)
    memory_used_bank1: int = 0
    memory_used_bank2: int = 0
    memory_cycles: int = 0
    
    # CPU Core State (AUTHENTIC - per Ulmann Chapter 12)
    cpu_accumulator: int = 0        # A register (32-bit, two halves)
    cpu_ix0: int = 0                # Index register 0
    cpu_ix1: int = 0                # Index register 1
    cpu_ix2: int = 0                # Index register 2
    cpu_ix3: int = 0                # Index register 3
    cpu_program_counter: int = 0    # P register
    cpu_pc_bank: int = 1            # Which bank PC is in (1 or 2)
    cpu_rtc: int = 0                # Real-time clock (16-bit, 32 Hz)
    cpu_instruction_count: int = 0
    cpu_cycle_count: int = 0
    cpu_halted: bool = True
    cpu_running: bool = False
    selected_program: str = "Array Sum (Authentic)"
    
    # Display system
    display_mode: str = "RADAR"  # RADAR, TACTICAL, STATUS, MEMORY
    display_brightness: int = 75
    phosphor_decay: float = 0.85
    
    # Radar tracking
    radar_targets: List[Dict] = []
    tracked_objects: int = 0
    intercept_courses: int = 0
    
    # Control surface states
    master_alarm: bool = False
    manual_override: bool = False
    intercept_mode: bool = False
    
    # Light gun interaction
    light_gun_x: int = 0
    light_gun_y: int = 0
    light_gun_active: bool = False
    selected_target: str = ""
    
    # Console positions
    active_consoles: int = 0
    max_consoles: int = 24
    
    # Mission data
    mission_time: str = "00:00:00"
    alerts_count: int = 0
    successful_intercepts: int = 0
    
    # Animation frame for real-time updates
    animation_frame: int = 0
    
    # CPU instance (AUTHENTIC FSQ7CPU)
    _cpu_core: Optional[FSQ7CPU] = None
    _last_rtc_tick: float = 0.0
    
    def _get_cpu(self) -> FSQ7CPU:
        """Get or create authentic FSQ7CPU core instance."""
        if self._cpu_core is None:
            self._cpu_core = FSQ7CPU()
            self._last_rtc_tick = time.time()
        return self._cpu_core
    
    def power_on_system(self):
        """Initialize system startup sequence."""
        if not self.power_on:
            self.power_on = True
            self.startup_progress = 0
            return FSQ7State.startup_sequence
    
    @rx.event(background=True)
    async def startup_sequence(self):
        """Simulate the vacuum tube warm-up and system initialization."""
        import asyncio
        
        # Warm up vacuum tubes
        for progress in range(0, 101, 5):
            await asyncio.sleep(0.1)
            async with self:
                self.startup_progress = progress
                self.active_tubes = int((self.total_tubes * progress) / 100)
                self.tube_temperature = 20.0 + (progress * 2.5)  # Up to 270°C
        
        async with self:
            self.system_ready = True
            self.mission_time = "00:00:00"
            # Initialize AUTHENTIC CPU
            cpu = self._get_cpu()
            cpu.reset()
            self.cpu_halted = False
            self.sync_cpu_state()
            # Initialize with some sample radar targets
            self.generate_sample_targets()
    
    def power_off_system(self):
        """Shutdown the system."""
        self.power_on = False
        self.system_ready = False
        self.startup_progress = 0
        self.active_tubes = 0
        self.tube_temperature = 20.0
        self.radar_targets = []
        self.tracked_objects = 0
        self.cpu_halted = True
        self.cpu_running = False
    
    def sync_cpu_state(self):
        """Sync AUTHENTIC CPU core state to UI state variables."""
        cpu = self._get_cpu()
        
        # Sync all FOUR index registers (per Ulmann §12.3)
        self.cpu_ix0 = cpu.ix[0]
        self.cpu_ix1 = cpu.ix[1]
        self.cpu_ix2 = cpu.ix[2]
        self.cpu_ix3 = cpu.ix[3]
        
        # Sync accumulator (32-bit with two halves)
        self.cpu_accumulator = cpu.A
        
        # Sync PC and its bank
        self.cpu_program_counter = cpu.P
        self.cpu_pc_bank = cpu.P_bank
        
        # Sync RTC (32 Hz real-time clock)
        self.cpu_rtc = cpu.RTC
        
        # Sync execution stats
        self.cpu_instruction_count = cpu.instruction_count
        self.cpu_cycle_count = cpu.cycle_count
        self.cpu_halted = cpu.halted
        
        # Update memory usage for BOTH banks
        non_zero_bank1 = sum(1 for word in cpu.memory.bank1 if word != 0)
        non_zero_bank2 = sum(1 for word in cpu.memory.bank2 if word != 0)
        self.memory_used_bank1 = non_zero_bank1
        self.memory_used_bank2 = non_zero_bank2
        
        # Sync I/O handler state (for light gun/display)
        self.light_gun_x = cpu.io_handler.light_gun_x
        self.light_gun_y = cpu.io_handler.light_gun_y
    
    def tick_rtc(self):
        """Update the real-time clock at 32 Hz."""
        cpu = self._get_cpu()
        current_time = time.time()
        delta = current_time - self._last_rtc_tick
        cpu.tick_rtc(delta)
        self._last_rtc_tick = current_time
        self.cpu_rtc = cpu.RTC
    
    def load_selected_program(self):
        """Load the selected AUTHENTIC example program into CPU memory."""
        cpu = self._get_cpu()
        cpu.reset()
        
        # Map UI names to AUTHENTIC program functions
        program_map = {
            "Array Sum (Authentic)": array_sum_authentic,
            "Coordinate Conversion": coordinate_conversion,
            "Subroutine Example": subroutine_example,
            "RTC Delay Loop": rtc_delay_loop,
            "Display I/O Example": display_io_example,
        }
        
        program_func = program_map.get(self.selected_program)
        if program_func:
            # Load the authentic program
            loaded_cpu, metadata = program_func()
            
            # Copy memory from BOTH banks
            for i in range(65536):
                cpu.memory.bank1[i] = loaded_cpu.memory.bank1[i]
            for i in range(4096):
                cpu.memory.bank2[i] = loaded_cpu.memory.bank2[i]
            
            # Copy registers (including all 4 index registers)
            cpu.A = loaded_cpu.A
            cpu.ix = loaded_cpu.ix.copy()
            cpu.P = loaded_cpu.P
            cpu.P_bank = loaded_cpu.P_bank
            cpu.RTC = loaded_cpu.RTC
            cpu.halted = False
            
        self.sync_cpu_state()
    
    def cpu_step(self):
        """Execute one CPU instruction."""
        cpu = self._get_cpu()
        if not cpu.halted:
            # Tick RTC before execution
            self.tick_rtc()
            cpu.step()
            self.sync_cpu_state()
    
    def cpu_run(self):
        """Start running CPU in background."""
        if not self.cpu_running:
            self.cpu_running = True
            self._last_rtc_tick = time.time()
            return FSQ7State.cpu_run_background
    
    @rx.event(background=True)
    async def cpu_run_background(self):
        """Background task to execute CPU instructions."""
        import asyncio
        
        cpu = self._get_cpu()
        
        while True:
            await asyncio.sleep(0.01)  # 100 Hz execution rate
            
            async with self:
                if not self.cpu_running or cpu.halted:
                    self.cpu_running = False
                    break
                
                # Tick RTC at 32 Hz
                self.tick_rtc()
                
                # Execute one instruction
                cpu.step()
                self.sync_cpu_state()
    
    def cpu_reset(self):
        """Reset the AUTHENTIC CPU core."""
        cpu = self._get_cpu()
        cpu.reset()
        self.cpu_running = False
        self._last_rtc_tick = time.time()
        self.sync_cpu_state()
    
    def toggle_display_mode(self):
        """Cycle through display modes."""
        modes = ["RADAR", "TACTICAL", "STATUS", "MEMORY"]
        current_index = modes.index(self.display_mode)
        self.display_mode = modes[(current_index + 1) % len(modes)]
    
    def adjust_brightness(self, value: int):
        """Adjust CRT display brightness."""
        self.display_brightness = max(0, min(100, value))
    
    def toggle_manual_override(self):
        """Toggle manual control override."""
        self.manual_override = not self.manual_override
    
    def toggle_intercept_mode(self):
        """Toggle intercept mode."""
        self.intercept_mode = not self.intercept_mode
    
    def light_gun_click(self, x: int, y: int):
        """Handle light gun interaction on display."""
        self.light_gun_x = x
        self.light_gun_y = y
        self.light_gun_active = True
        
        # Update CPU I/O handler
        cpu = self._get_cpu()
        cpu.io_handler.light_gun_x = x
        cpu.io_handler.light_gun_y = y
        
        # Check if a target was selected
        for target in self.radar_targets:
            dist = math.sqrt((target["x"] - x)**2 + (target["y"] - y)**2)
            if dist < 20:  # Selection radius
                self.selected_target = target["target_id"]
                # Write target ID to I/O handler
                cpu.io_handler.selected_track = int(target["target_id"].split("-")[1])
                break
    
    def clear_light_gun(self):
        """Clear light gun selection."""
        self.light_gun_active = False
        self.selected_target = ""
    
    def generate_sample_targets(self):
        """Generate sample radar targets for demonstration."""
        self.radar_targets = []
        target_types = ["AIRCRAFT", "MISSILE", "FRIENDLY", "UNKNOWN"]
        
        for i in range(random.randint(5, 12)):
            self.radar_targets.append({
                "target_id": f"TGT-{1000 + i}",
                "x": random.randint(50, 750),
                "y": random.randint(50, 550),
                "heading": random.randint(0, 359),
                "speed": random.randint(200, 800),
                "altitude": random.randint(5000, 45000),
                "target_type": random.choice(target_types),
                "threat_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
            })
        
        self.tracked_objects = len(self.radar_targets)
    
    def assign_intercept(self):
        """Assign an interceptor to the selected target."""
        if self.selected_target and self.intercept_mode:
            self.intercept_courses += 1
            self.alerts_count += 1
            # In a real system, this would launch interceptor aircraft
    
    @rx.event(background=True)
    async def update_simulation(self):
        """Background task to update simulation in real-time."""
        import asyncio
        
        while True:
            await asyncio.sleep(0.05)  # 20 FPS update rate
            
            async with self:
                if not self.system_ready:
                    continue
                
                self.animation_frame += 1
                
                # Update mission time
                if self.animation_frame % 20 == 0:  # Every second
                    # Parse and increment mission time
                    h, m, s = map(int, self.mission_time.split(":"))
                    s += 1
                    if s >= 60:
                        s = 0
                        m += 1
                    if m >= 60:
                        m = 0
                        h += 1
                    self.mission_time = f"{h:02d}:{m:02d}:{s:02d}"
                
                # Simulate random tube failures (very rare)
                if random.random() < 0.0001:
                    self.failed_tubes += 1
                    self.active_tubes -= 1
                
                # Update memory cycles
                self.memory_cycles += 1
                
                # Tick RTC at 32 Hz (every ~31ms, but check every frame)
                if not self.cpu_running:
                    self.tick_rtc()
                
                # Sync CPU state periodically (if not running continuously)
                if not self.cpu_running and self.animation_frame % 10 == 0:
                    self.sync_cpu_state()
                
                # Move radar targets
                for target in self.radar_targets:
                    # Simple movement simulation
                    heading_rad = math.radians(target["heading"])
                    speed_factor = target["speed"] / 1000.0
                    target["x"] += math.cos(heading_rad) * speed_factor
                    target["y"] += math.sin(heading_rad) * speed_factor
                    
                    # Wrap around screen
                    if target["x"] < 0:
                        target["x"] = 800
                    elif target["x"] > 800:
                        target["x"] = 0
                    if target["y"] < 0:
                        target["y"] = 600
                    elif target["y"] > 600:
                        target["y"] = 0
                    
                    # Random course changes
                    if random.random() < 0.01:
                        target["heading"] = (target["heading"] + random.randint(-15, 15)) % 360


def index() -> rx.Component:
    """Main page layout for the AN/FSQ-7 simulator."""
    return rx.box(
        # Background styling to look like a 1950s computer room
        rx.vstack(
            # Title bar
            rx.hstack(
                rx.heading(
                    "AN/FSQ-7 SAGE COMPUTER SIMULATOR (AUTHENTIC)",
                    size="9",
                    font_family="monospace",
                    color="#00FF00",
                    text_shadow="0 0 10px #00FF00",
                ),
                rx.spacer(),
                rx.badge(
                    rx.cond(
                        FSQ7State.system_ready,
                        "OPERATIONAL",
                        "OFFLINE"
                    ),
                    color_scheme=rx.cond(
                        FSQ7State.system_ready,
                        "green",
                        "red"
                    ),
                    size="3",
                ),
                width="100%",
                padding="20px",
                background="linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%)",
                border_bottom="2px solid #00FF00",
            ),
            
            # Main simulator area
            rx.hstack(
                # Left panel - Control surfaces
                rx.vstack(
                    control_panel(),
                    system_status(),
                    width="300px",
                    spacing="4",
                    padding="10px",
                ),
                
                # Center - CRT Display
                rx.vstack(
                    crt_display(),
                    radar_scope(),
                    flex="1",
                    spacing="4",
                    padding="10px",
                ),
                
                # Right panel - Memory, CPU, and diagnostics
                rx.vstack(
                    memory_banks(),
                    cpu_panel(),
                    width="350px",
                    spacing="4",
                    padding="10px",
                ),
                
                width="100%",
                height="auto",
                align_items="start",
            ),
            
            # SD Console section (full width, below main simulator)
            rx.box(
                rx.divider(border_color="#00FF00", opacity="0.3", margin="20px 0"),
                sd_console(),
                width="100%",
                padding="10px 20px",
            ),
            
            # Status bar at bottom
            rx.box(
                rx.hstack(
                    rx.text(
                        f"MISSION TIME: ",
                        color="#888",
                        font_family="monospace",
                        font_size="12px",
                    ),
                    rx.text(
                        FSQ7State.mission_time,
                        color="#00FF00",
                        font_family="monospace",
                        font_size="12px",
                        font_weight="bold",
                    ),
                    rx.spacer(),
                    rx.text(
                        f"TRACKED: {FSQ7State.tracked_objects}",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="12px",
                    ),
                    rx.spacer(),
                    rx.text(
                        f"INTERCEPTS: {FSQ7State.intercept_courses}",
                        color="#FF6600",
                        font_family="monospace",
                        font_size="12px",
                    ),
                    rx.spacer(),
                    rx.text(
                        f"CPU: IX=[{FSQ7State.cpu_ix0},{FSQ7State.cpu_ix1},{FSQ7State.cpu_ix2},{FSQ7State.cpu_ix3}] RTC={FSQ7State.cpu_rtc}",
                        color="#00FFFF",
                        font_family="monospace",
                        font_size="12px",
                    ),
                    width="100%",
                    padding="10px 20px",
                ),
                background="linear-gradient(180deg, #0a0a0a 0%, #000000 100%)",
                border_top="2px solid #00FF00",
                width="100%",
            ),
            
            spacing="0",
            width="100%",
            height="100vh",
        ),
        
        width="100%",
        height="100%",
        background="radial-gradient(circle at center, #1a1a1a 0%, #000000 100%)",
    )


# Create the Reflex app
app = rx.App(
    style={
        "font_family": "'Courier New', monospace",
        "background": "#000000",
    }
)

# Add the index page
app.add_page(
    index,
    on_load=FSQ7State.update_simulation,
)
