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
"""

import reflex as rx
from typing import List, Dict, Tuple
import math
import random
from datetime import datetime

# Import custom components
from .components.crt_display import crt_display
from .components.control_panel import control_panel
from .components.system_status import system_status
from .components.memory_banks import memory_banks
from .components.radar_scope import radar_scope


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
    
    # Memory system (magnetic core memory)
    memory_capacity: int = 65536  # 64K words
    memory_used: int = 0
    memory_cycles: int = 0
    
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
        
        # Check if a target was selected
        for target in self.radar_targets:
            dist = math.sqrt((target["x"] - x)**2 + (target["y"] - y)**2)
            if dist < 20:  # Selection radius
                self.selected_target = target["target_id"]
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
                self.memory_used = min(self.memory_capacity, 
                                       int(self.memory_capacity * 0.45 + random.randint(-100, 100)))
                
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
                    "AN/FSQ-7 SAGE COMPUTER SIMULATOR",
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
                
                # Right panel - Memory and diagnostics
                rx.vstack(
                    memory_banks(),
                    width="300px",
                    spacing="4",
                    padding="10px",
                ),
                
                width="100%",
                spacing="4",
                align_items="start",
            ),
            
            # Status bar at bottom
            rx.hstack(
                rx.text(
                    f"MISSION TIME: {FSQ7State.mission_time}",
                    font_family="monospace",
                    color="#00FF00",
                ),
                rx.spacer(),
                rx.text(
                    f"TUBES: {FSQ7State.active_tubes}/{FSQ7State.total_tubes}",
                    font_family="monospace",
                    color="#00FF00",
                ),
                rx.spacer(),
                rx.text(
                    f"TARGETS: {FSQ7State.tracked_objects}",
                    font_family="monospace",
                    color="#00FF00",
                ),
                rx.spacer(),
                rx.text(
                    f"INTERCEPTS: {FSQ7State.intercept_courses}",
                    font_family="monospace",
                    color="#00FF00",
                ),
                width="100%",
                padding="10px",
                background="#0a0a0a",
                border_top="2px solid #00FF00",
            ),
            
            width="100%",
            height="100vh",
            spacing="0",
        ),
        
        background="#000000",
        width="100%",
        height="100vh",
        on_mount=FSQ7State.update_simulation,
    )


# Initialize the app
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="green",
    ),
    style={
        "font_family": "Courier New, monospace",
    },
)

app.add_page(index, title="AN/FSQ-7 SAGE Simulator", route="/")
