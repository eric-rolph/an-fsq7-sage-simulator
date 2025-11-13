"""
Interactive SAGE Simulator - Main Integration

Wires together all interactive components:
- Radar scope with WebGL rendering
- CPU execution trace panel
- Light gun selection system
- SD Console controls
- Geographic overlays
- Tube maintenance mini-game
- Tutorial/mission system

Runs 500ms tick loop for realistic scenario advancement.
"""

import reflex as rx
import json
from typing import List, Set, Optional
from datetime import datetime
import asyncio
import time
from .components_v2 import script_loader

# Import state model
from . import state_model

# Import simulation models and scenarios
from .sim import models as sim_models
from .sim import scenarios as sim_scenarios

# Import all our component modules
from .components_v2 import (
    scenarios_layered,
    execution_trace_panel,
    light_gun,
    sd_console,
    geographic_overlays,
    tube_maintenance,
    tutorial_system,
    radar_scope,
    system_messages,  # NEW: Operator goal flow requirement #2
    scenario_selector,  # NEW: Scenario switching UI
    simulation_controls,  # NEW: Pause/play/speed controls
)


class InteractiveSageState(rx.State):
    """
    Main state container for the interactive SAGE simulator
    Single source of truth for all UI and simulation state
    """
    
    # ===== SIMULATION STATE =====
    tracks: List[state_model.Track] = []
    world_time: int = 0  # milliseconds since start
    is_running: bool = False
    current_scenario_name: str = "Demo 1 - Three Inbound"
    is_paused: bool = False
    speed_multiplier: float = 1.0
    _background_task_started: bool = False  # Track if simulation loop is running
    
    # ===== CPU STATE =====
    current_program: str = ""
    cpu_trace: state_model.CpuTrace = None
    execution_speed: str = "realtime"  # realtime | slow | step
    
    # ===== LIGHT GUN STATE =====
    lightgun_armed: bool = False
    selected_track_id: str = ""
    
    # ===== SD CONSOLE STATE =====
    active_filters: Set[str] = set()
    active_overlays: Set[str] = {"range_rings", "coastlines", "flight_paths"}
    scope_center_x: float = 0.0
    scope_center_y: float = 0.0
    scope_zoom: float = 1.0
    brightness: float = 0.75
    
    # ===== SYSTEM MESSAGES STATE =====
    system_messages_log: List[system_messages.SystemMessage] = []
    
    # ===== MAINTENANCE STATE =====
    maintenance: state_model.MaintenanceState = state_model.MaintenanceState(
        tubes=[state_model.TubeState(id=i, health=100, status="ok") for i in range(64)],
        performance_penalty=0.0
    )
    replacing_tube_id: int = -1
    
    # ===== TUTORIAL STATE =====
    current_mission_id: int = 0
    current_step_num: int = 0
    completed_missions: Set[int] = set()
    show_welcome: bool = True
    tutorial_active: bool = False
    
    # Note: geo_overlays removed from state - use geographic_overlays module directly in views
    
    
    # ========================
    # SIMULATION CONTROL
    # ========================
    
    def start_simulation(self):
        """Resume simulation"""
        self.is_running = True
    
    def stop_simulation(self):
        """Pause simulation"""
        self.is_running = False
    
    @rx.event(background=True)
    async def simulation_tick_loop(self):
        """
        Background task that updates track positions.
        Respects pause flag and speed multiplier.
        """
        while True:
            await asyncio.sleep(1.0)  # Always sleep 1 second
            
            async with self:
                # Skip update if paused
                if self.is_paused:
                    continue
                
                # Update positions with speed multiplier applied
                dt = 1.0 * self.speed_multiplier
                self.update_track_positions(dt=dt)
                
                # Increment world time (milliseconds)
                self.world_time += int(1000 * self.speed_multiplier)
                
                # Check tube degradation periodically
                if self.world_time % 10000 == 0:  # Every 10 seconds
                    self.degrade_tubes()
    
    async def tick_loop(self):
        """Legacy main simulation loop - replaced by simulation_tick_loop"""
        while self.is_running:
            await asyncio.sleep(0.5)
            self.world_time += 500
            
            # Advance world (move tracks, spawn scenarios, resolve intercepts)
            # updated_tracks = scenarios_layered.advance_world(500, self.tracks, self.maintenance)
            # self.tracks = updated_tracks
            # TODO: Implement advance_world in scenarios_layered.py
            pass
            
            # Check tube degradation
            self.degrade_tubes()
            
            # Check mission progress
            if self.tutorial_active:
                self.check_mission_step()
    
    def degrade_tubes(self):
        """Random tube failures over time"""
        import random
        if random.random() < 0.001:  # 0.1% chance per tick
            healthy_tubes = [t for t in self.maintenance.tubes if t.status == "ok"]
            if healthy_tubes:
                tube = random.choice(healthy_tubes)
                tube.status = "degrading"
                tube.health = 50
    
    def update_track_positions(self, dt: float = 1.0):
        """
        Update all track positions based on velocity.
        
        Args:
            dt: Time delta in seconds (default 1.0 second per update)
        """
        for track in self.tracks:
            # Save current position to trail (keep last 20 positions)
            track.trail.append((track.x, track.y))
            if len(track.trail) > 20:
                track.trail = track.trail[-20:]
            
            # Update position based on velocity
            track.x += track.vx * dt
            track.y += track.vy * dt
            
            # Wrap around boundaries (0.0 to 1.0 normalized space)
            if track.x < 0.0:
                track.x += 1.0
            elif track.x > 1.0:
                track.x -= 1.0
                
            if track.y < 0.0:
                track.y += 1.0
            elif track.y > 1.0:
                track.y -= 1.0
    
    def load_scenario(self, scenario_name: str):
        """Load a scenario and convert RadarTarget objects to Track objects"""
        if scenario_name not in sim_scenarios.SCENARIOS:
            return
        
        self.current_scenario_name = scenario_name
        scenario = sim_scenarios.SCENARIOS[scenario_name]
        
        # Convert RadarTarget to Track
        self.tracks = []
        for rt in scenario.targets:
            # Calculate velocity components from speed and heading
            # Speed in knots, heading in degrees (0=East, 90=North in radar coords)
            # Convert to normalized screen units per second
            import math
            heading_rad = math.radians(rt.heading)
            # Scale factor: knots to normalized coords/sec (tuned for visual effect)
            # 1 knot ≈ 0.00005 normalized units/sec for reasonable on-screen movement
            speed_scale = 0.00005
            vx = math.cos(heading_rad) * rt.speed * speed_scale
            vy = math.sin(heading_rad) * rt.speed * speed_scale
            
            track = state_model.Track(
                id=rt.target_id,
                x=rt.x / 800.0,  # Normalize to 0.0-1.0 for radar scope renderer
                y=rt.y / 800.0,  # Normalize to 0.0-1.0 for radar scope renderer
                vx=vx,
                vy=vy,
                altitude=rt.altitude,
                speed=int(rt.speed),
                heading=int(rt.heading),
                track_type=rt.target_type.lower(),
                threat_level=rt.threat_level,
                time_detected=self.world_time / 1000.0
            )
            self.tracks.append(track)
        
        # Log scenario load
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="SCENARIO",
                message=f"Loaded: {scenario.name}",
                details=f"{len(self.tracks)} tracks initialized"
            )
        )
    
    def change_scenario(self, scenario_name: str):
        """Change to a different scenario"""
        self.load_scenario(scenario_name)
        # Log scenario change
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="SCENARIO",
                message=f"Scenario changed to: {scenario_name}",
                details=f"{len(self.tracks)} tracks loaded"
            )
        )
    
    def pause_simulation(self):
        """Pause the simulation loop"""
        self.is_paused = True
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="SIMULATION",
                message="Simulation PAUSED",
                details=""
            )
        )
    
    def resume_simulation(self):
        """Resume the simulation loop"""
        self.is_paused = False
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="SIMULATION",
                message="Simulation RESUMED",
                details=""
            )
        )
    
    def set_speed_multiplier(self, speed: float):
        """Set simulation speed multiplier"""
        self.speed_multiplier = speed
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="SIMULATION",
                message=f"Speed set to {speed}x",
                details=""
            )
        )
    
    def on_page_load(self):
        """Called when the page loads - initialize demo scenario"""
        self.load_scenario("Demo 1 - Three Inbound")
        # Start the simulation tick loop only if not already running
        if not self._background_task_started:
            self._background_task_started = True
            return InteractiveSageState.simulation_tick_loop
        return None
    
    
    # ========================
    # CPU EXECUTION
    # ========================
    
    def load_cpu_program(self, program_name: str):
        """Load a CPU program (from existing SAGE program list)"""
        self.current_program = program_name
        self.cpu_trace = state_model.CpuTrace(
            program_name=program_name,
            status="loaded",
            steps=[],
            final_result=None,
            elapsed_ms=0
        )
    
    def run_cpu_program(self):
        """Execute the loaded CPU program with trace"""
        if not self.current_program:
            return
        
        # TODO: Actually run the SAGE CPU emulator and capture trace
        # For now, mock execution
        self.cpu_trace.status = "running"
        
        # Simulate some execution steps
        self.cpu_trace.steps = [
            state_model.ExecutionStep(
                step_num=1,
                instruction_text="LOAD A, [0x100]",
                result_text="A = 42",
                registers=state_model.CpuRegisters(A=42, B=0, PC=1, FLAGS=0)
            ),
            state_model.ExecutionStep(
                step_num=2,
                instruction_text="LOAD B, [0x101]",
                result_text="B = 17",
                registers=state_model.CpuRegisters(A=42, B=17, PC=2, FLAGS=0)
            ),
            state_model.ExecutionStep(
                step_num=3,
                instruction_text="ADD A, B",
                result_text="A = 59",
                registers=state_model.CpuRegisters(A=59, B=17, PC=3, FLAGS=0)
            )
        ]
        
        self.cpu_trace.status = "completed"
        self.cpu_trace.final_result = "59"
        self.cpu_trace.elapsed_ms = 150
    
    def set_execution_speed(self, speed: str):
        """Change CPU execution speed (realtime, slow, or step)"""
        if speed in ["realtime", "slow", "step"]:
            self.execution_speed = speed
            self.add_system_message(f"CPU execution speed: {speed.upper()}")
        else:
            self.add_system_message(f"Invalid speed: {speed}")
    
    
    # ========================
    # LIGHT GUN
    # ========================
    
    def arm_lightgun(self):
        """Activate light gun (press D key)"""
        self.lightgun_armed = True
    
    def disarm_lightgun(self):
        """Deactivate light gun (press ESC key)"""
        self.lightgun_armed = False
        self.selected_track_id = ""
    
    def select_track(self, track_id: str):
        """User clicked a track with armed light gun"""
        if not self.lightgun_armed:
            return
        
        self.selected_track_id = track_id
        
        # Mark track as selected in state
        for track in self.tracks:
            track.selected = (track.id == track_id)
    
    def launch_intercept(self):
        """Launch interceptor at selected hostile track"""
        if not self.selected_track_id:
            return
        
        target = next((t for t in self.tracks if t.id == self.selected_track_id), None)
        if not target or target.track_type not in ["hostile", "missile"]:
            return
        
        # Spawn interceptor
        # interceptor = scenarios_layered.spawn_interceptor(target)
        # self.tracks.append(interceptor)
        # TODO: Implement spawn_interceptor in scenarios_layered.py
        
        # For now, log the action
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                level="info",
                category="intercept",
                message=f"INTERCEPT LAUNCHED: Target {target.id}",
                details=f"Interceptor dispatched toward {target.track_type} at {target.altitude} ft"
            )
        )
    
    
    # ========================
    # SD CONSOLE
    # ========================
    
    def toggle_filter(self, filter_name: str):
        """Toggle a category filter (S1-S13 buttons)"""
        #  Known issue: Reflex passes event dict, needs investigation
        if filter_name in self.active_filters:
            self.active_filters.remove(filter_name)
            action = "disabled"
        else:
            self.active_filters.add(filter_name)
            action = "enabled"
        
        # Log the filter change
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="FILTER",
                message=f"Filter {action.upper()}",
                details=f"Category: {filter_name.upper()}"
            )
        )
    
    def toggle_overlay(self, overlay_name: str):
        """Toggle a feature overlay (S20-S24 buttons)"""
        if overlay_name in self.active_overlays:
            self.active_overlays.remove(overlay_name)
            action = "disabled"
        else:
            self.active_overlays.add(overlay_name)
            action = "enabled"
        
        # Log the overlay change
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="INFO",
                message=f"Overlay {action.upper()}",
                details=f"Display: {overlay_name.replace('_', ' ').upper()}"
            )
        )
    
    def pan_scope(self, direction: str):
        """Pan scope view (arrow buttons)"""
        step = 0.05
        if direction == "up":
            self.scope_center_y -= step
        elif direction == "down":
            self.scope_center_y += step
        elif direction == "left":
            self.scope_center_x -= step
        elif direction == "right":
            self.scope_center_x += step
        
        # Log pan action
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="ACTION",
                message="Scope Panned",
                details=f"Direction: {direction.upper()}"
            )
        )
    
    def center_scope(self):
        """Reset scope to center (⊙ button)"""
        self.scope_center_x = 0.0
        self.scope_center_y = 0.0
        
        # Log center action
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="ACTION",
                message="Scope Centered",
                details="View reset to origin"
            )
        )
    
    def zoom_scope(self, direction: str):
        """Zoom in/out (+/- buttons)"""
        if direction == "in":
            self.scope_zoom = min(3.0, self.scope_zoom * 1.2)
        elif direction == "out":
            self.scope_zoom = max(0.5, self.scope_zoom / 1.2)
        elif direction == "fit":
            self.scope_zoom = 1.0
        
        # Log zoom action
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="ACTION",
                message="Zoom Changed",
                details=f"{direction.upper()} (zoom: {self.scope_zoom:.2f}x)"
            )
        )
    
    def set_brightness(self, value: float):
        """Set scope brightness (slider)"""
        old_brightness = self.brightness
        self.brightness = max(0.2, min(1.0, value))
        
        # Only log if changed significantly (avoid spam from slider)
        if abs(self.brightness - old_brightness) > 0.05:
            self.system_messages_log.append(
                system_messages.SystemMessage(
                    timestamp=datetime.now(),
                    category="ACTION",
                    message="Brightness Adjusted",
                    details=f"{int(self.brightness * 100)}%"
                )
            )
    
    def set_brightness_percent(self, percent: list[float]):
        """Set brightness from percentage (0-100) - rx.slider passes list"""
        value = percent[0] if percent else 75.0
        self.brightness = max(0.2, min(1.0, value / 100.0))
        
        # Log brightness change
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="ACTION",
                message="Brightness Set",
                details=f"{int(value)}%"
            )
        )
    
    def set_brightness_preset(self, value: float):
        """Set brightness to preset value"""
        self.brightness = value
        
        # Log preset selection
        preset_name = "DIM" if value <= 0.4 else "MEDIUM" if value <= 0.7 else "BRIGHT"
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="ACTION",
                message=f"Brightness: {preset_name}",
                details=f"{int(value * 100)}%"
            )
        )
    
    def rotate_scope(self, direction: str):
        """Rotate scope view (bonus feature - not yet implemented)"""
        # TODO: Implement scope rotation
        # For now, this is a placeholder for future rotation feature
        pass
    
    def clear_system_messages(self):
        """Clear all system messages from the log"""
        self.system_messages_log = []
    
    
    # ========================
    # TUBE MAINTENANCE
    # ========================
    
    def start_tube_replacement(self, tube_id: int):
        """Begin 4-step tube replacement procedure"""
        self.replacing_tube_id = tube_id
        tube = self.maintenance.tubes[tube_id]
        tube.status = "warming_up"
        tube.health = 0
        
        # TODO: Start 5-second warmup timer
        # After 5 seconds: tube.status = "ok", tube.health = 100
    
    def complete_tube_replacement(self, tube_id: int):
        """Finish tube warmup"""
        tube = self.maintenance.tubes[tube_id]
        tube.status = "ok"
        tube.health = 100
        self.replacing_tube_id = -1
        
        # Recalculate performance penalty
        failed_count = sum(1 for t in self.maintenance.tubes if t.status == "failed")
        self.maintenance.performance_penalty = failed_count / 64.0
    
    def close_tube_modal(self):
        """Close the tube replacement modal without replacing"""
        self.replacing_tube_id = -1
        self.add_system_message("Tube replacement cancelled")
    
    
    # ========================
    # TUTORIAL SYSTEM
    # ========================
    
    def start_mission(self, mission_id: int):
        """Begin a tutorial mission"""
        self.current_mission_id = mission_id
        self.current_step_num = 0
        self.tutorial_active = True
        self.show_welcome = False
    
    def skip_tutorial(self):
        """User chose to skip tutorial"""
        self.tutorial_active = False
        self.show_welcome = False
    
    def check_mission_step(self):
        """Check if current mission step is completed"""
        if not self.tutorial_active:
            return
        
        mission = tutorial_system.TRAINING_MISSIONS[self.current_mission_id]
        if self.current_step_num >= len(mission.steps):
            # Mission complete!
            self.completed_missions.add(self.current_mission_id)
            self.tutorial_active = False
            return
        
        step = mission.steps[self.current_step_num]
        
        # TODO: Actually evaluate step.check_condition
        # For now, auto-advance on any action
        # if step.check_condition(self):
        #     self.current_step_num += 1
    
    def previous_mission(self):
        """Navigate to the previous tutorial mission"""
        if self.current_mission_id > 0:
            self.current_mission_id -= 1
            self.current_step_num = 0
            self.add_system_message(f"Mission {self.current_mission_id + 1}: {tutorial_system.TRAINING_MISSIONS[self.current_mission_id].title}")
    
    def next_mission(self):
        """Navigate to the next tutorial mission"""
        if self.current_mission_id < len(tutorial_system.TRAINING_MISSIONS) - 1:
            self.current_mission_id += 1
            self.current_step_num = 0
            self.add_system_message(f"Mission {self.current_mission_id + 1}: {tutorial_system.TRAINING_MISSIONS[self.current_mission_id].title}")
    
    def open_full_tutorial(self):
        """Open the full tutorial view"""
        self.tutorial_active = True
        self.show_welcome = False
        self.add_system_message("Tutorial opened")
    
    def next_mission_step(self):
        """Manually advance to next step (for testing)"""
        mission = tutorial_system.TRAINING_MISSIONS[self.current_mission_id]
        if self.current_step_num < len(mission.steps) - 1:
            self.current_step_num += 1
        else:
            self.completed_missions.add(self.current_mission_id)
            self.tutorial_active = False
    
    
    # ========================
    # DATA SERIALIZATION
    # ========================
    
    def get_tracks_json(self) -> str:
        """Serialize tracks for WebGL renderer"""
        filtered_tracks = self.apply_filters(self.tracks)
        return json.dumps([{
            "id": t.id,
            "x": t.x,
            "y": t.y,
            "altitude": t.altitude,
            "speed": t.speed,
            "heading": t.heading,
            "track_type": t.track_type,
            "threat_level": t.threat_level,
            "selected": getattr(t, 'selected', False),
            "designation": getattr(t, 'designation', ''),
            "trail": getattr(t, 'trail', [])  # Include trail history for rendering
        } for t in filtered_tracks])
    
    def get_overlays_json(self) -> str:
        """Serialize active overlays"""
        return json.dumps(list(self.active_overlays))
    
    def get_geo_json(self) -> str:
        """Serialize geographic data"""
        # Return basic GeoJSON structure for now
        return json.dumps({
            "coastlines": [],
            "cities": [],
            "range_rings": []
        })
    
    def apply_filters(self, tracks: List[state_model.Track]) -> List[state_model.Track]:
        """Apply active filters to track list"""
        if not self.active_filters:
            return tracks
        
        filtered = []
        for track in tracks:
            # Check each filter
            if "hostile" in self.active_filters and track.track_type != "hostile":
                continue
            if "friendly" in self.active_filters and track.track_type != "friendly":
                continue
            if "unknown" in self.active_filters and track.track_type != "unknown":
                continue
            if "missile" in self.active_filters and track.track_type != "missile":
                continue
            if "alt_low" in self.active_filters and track.altitude > 10000:
                continue
            if "alt_med" in self.active_filters and (track.altitude < 10000 or track.altitude > 30000):
                continue
            if "alt_high" in self.active_filters and track.altitude < 30000:
                continue
            
            filtered.append(track)
        
        return filtered
    
    @rx.var
    def selected_track(self) -> Optional[state_model.Track]:
        """Get currently selected track for detail panel (computed var)"""
        for track in self.tracks:
            if track.id == self.selected_track_id:
                return track
        return None
    
    @rx.var
    def tracks_json_var(self) -> str:
        """Embed filtered tracks as JSON for JavaScript access (computed var)"""
        return self.get_tracks_json()
    
    @rx.var
    def world_time_seconds(self) -> float:
        """Convert world_time from milliseconds to seconds for UI display"""
        return self.world_time / 1000.0


# ========================
# MAIN PAGE LAYOUT
# ========================

def index() -> rx.Component:
    """Main SAGE simulator page"""
    return rx.container(
        # Welcome modal (first visit) - Temporarily disabled due to lambda event handler issues
        # rx.cond(
        #     InteractiveSageState.show_welcome,
        #     tutorial_system.welcome_modal(True)
        # ),
        
        rx.vstack(
            # Header
            rx.heading("AN/FSQ-7 SAGE Simulator", size="9", color="#00ff00"),
            rx.text("Interactive Cold War Air Defense System", color="#88ff88"),
            
            # Main layout: 3 columns
            rx.hstack(
                # LEFT COLUMN: Scenario + Simulation Controls + SD Console + Maintenance
                rx.vstack(
                    scenario_selector.scenario_selector_panel(
                        InteractiveSageState.current_scenario_name,
                        InteractiveSageState.change_scenario
                    ),
                    sd_console.sd_console_master_panel(
                        InteractiveSageState.active_filters,
                        InteractiveSageState.active_overlays,
                        InteractiveSageState.brightness,
                        InteractiveSageState,
                    ),
                    tube_maintenance.tube_maintenance_panel(
                        InteractiveSageState.maintenance
                    ),
                    width="300px",
                    spacing="4"
                ),
                
                # CENTER COLUMN: Radar Scope + Tutorial
                rx.vstack(
                    # Radar scope (main display)
                    rx.box(
                        rx.html(radar_scope.get_radar_scope_html()),
                        width="800px",
                        height="800px",
                        border="2px solid #00ff00",
                        border_radius="8px"
                    ),
                    
                    # Tutorial sidebar (collapsible)
                    rx.cond(
                        InteractiveSageState.tutorial_active,
                        tutorial_system.tutorial_sidebar_compact(
                            on_open=InteractiveSageState.open_full_tutorial
                        )
                    ),
                    
                    width="820px",
                    spacing="4"
                ),
                
                # RIGHT COLUMN: Simulation Controls + CPU Trace + Light Gun
                rx.vstack(
                    simulation_controls.simulation_control_panel(
                        InteractiveSageState.is_paused,
                        InteractiveSageState.speed_multiplier,
                        InteractiveSageState.world_time,
                        InteractiveSageState.pause_simulation,
                        InteractiveSageState.resume_simulation,
                        InteractiveSageState.set_speed_multiplier
                    ),
                    execution_trace_panel.execution_trace_panel_compact(
                        InteractiveSageState.cpu_trace
                    ),
                    light_gun.track_detail_panel(
                        InteractiveSageState.selected_track,
                        InteractiveSageState.lightgun_armed,
                        on_launch=InteractiveSageState.launch_intercept,
                        on_clear=InteractiveSageState.disarm_lightgun
                    ),
                    light_gun.light_gun_controls(
                        on_arm=InteractiveSageState.arm_lightgun
                    ),
                    width="350px",
                    spacing="4"
                ),
                
                spacing="5",
                align="start"
            ),
            
            spacing="5",
            padding="20px"
        ),
        
        # Embed track data as hidden div with data attribute (reactive)
        rx.el.div(
            id="sage-track-data",
            data_tracks=InteractiveSageState.tracks_json_var,
            style={"display": "none"}
        ),
        
        # Load and initialize radar scope using proper dynamic script loading
        script_loader.load_radar_scope(),
        
        # Inject CSS and scripts
        rx.html(radar_scope.RADAR_SCOPE_CSS),
        rx.html(tube_maintenance.TUBE_ANIMATIONS_CSS),
        rx.html(light_gun.LIGHT_GUN_KEYBOARD_SCRIPT),
        
        max_width="100%",
        background="#000000",
        on_mount=InteractiveSageState.on_page_load
    )


# Create the Reflex app
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Courier+New:wght@400;700&display=swap"
    ]
)
app.add_page(index, route="/")
