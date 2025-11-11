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
from typing import List, Set
from datetime import datetime
import asyncio

# Import all our component modules
from .components_v2 import (
    state_model,
    scenarios,
    execution_trace_panel,
    light_gun,
    sd_console,
    geographic_overlays,
    tube_maintenance,
    tutorial_system,
    radar_scope
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
    
    # ===== CPU STATE =====
    current_program: str = ""
    cpu_trace: state_model.CpuTrace = None
    execution_speed: str = "realtime"  # realtime | slow | step
    
    # ===== LIGHT GUN STATE =====
    lightgun_armed: bool = False
    selected_track_id: str = ""
    
    # ===== SD CONSOLE STATE =====
    active_filters: Set[str] = set()
    active_overlays: Set[str] = {"range_rings", "coastlines"}
    scope_center_x: float = 0.0
    scope_center_y: float = 0.0
    scope_zoom: float = 1.0
    brightness: float = 0.75
    
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
    
    # ===== GEOGRAPHIC DATA =====
    geo_overlays: geographic_overlays.GeographicOverlays = geographic_overlays.GeographicOverlays()
    
    
    # ========================
    # SIMULATION CONTROL
    # ========================
    
    def start_simulation(self):
        """Start the 500ms world tick loop"""
        self.is_running = True
        # TODO: Start asyncio task for tick loop
        # asyncio.create_task(self.tick_loop())
    
    def stop_simulation(self):
        """Pause simulation"""
        self.is_running = False
    
    async def tick_loop(self):
        """Main simulation loop - runs every 500ms"""
        while self.is_running:
            await asyncio.sleep(0.5)
            self.world_time += 500
            
            # Advance world (move tracks, spawn scenarios, resolve intercepts)
            updated_tracks = scenarios.advance_world(500, self.tracks, self.maintenance)
            self.tracks = updated_tracks
            
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
        interceptor = scenarios.spawn_interceptor(target)
        self.tracks.append(interceptor)
    
    
    # ========================
    # SD CONSOLE
    # ========================
    
    def toggle_filter(self, filter_name: str):
        """Toggle a category filter (S1-S13 buttons)"""
        if filter_name in self.active_filters:
            self.active_filters.remove(filter_name)
        else:
            self.active_filters.add(filter_name)
    
    def toggle_overlay(self, overlay_name: str):
        """Toggle a feature overlay (S20-S24 buttons)"""
        if overlay_name in self.active_overlays:
            self.active_overlays.remove(overlay_name)
        else:
            self.active_overlays.add(overlay_name)
    
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
    
    def center_scope(self):
        """Reset scope to center (⊙ button)"""
        self.scope_center_x = 0.0
        self.scope_center_y = 0.0
    
    def zoom_scope(self, direction: str):
        """Zoom in/out (+/- buttons)"""
        if direction == "in":
            self.scope_zoom = min(3.0, self.scope_zoom * 1.2)
        elif direction == "out":
            self.scope_zoom = max(0.5, self.scope_zoom / 1.2)
        elif direction == "fit":
            self.scope_zoom = 1.0
    
    def set_brightness(self, value: float):
        """Set scope brightness (slider)"""
        self.brightness = max(0.2, min(1.0, value))
    
    
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
            "vx": t.vx,
            "vy": t.vy,
            "altitude": t.altitude,
            "speed": t.speed,
            "heading": t.heading,
            "track_type": t.track_type,
            "threat_level": t.threat_level,
            "selected": t.selected,
            "t_minus": t.t_minus,
            "target_id": getattr(t, 'target_id', None)
        } for t in filtered_tracks])
    
    def get_overlays_json(self) -> str:
        """Serialize active overlays"""
        return json.dumps(list(self.active_overlays))
    
    def get_geo_json(self) -> str:
        """Serialize geographic data"""
        return self.geo_overlays.to_json()
    
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
    
    def get_selected_track(self) -> state_model.Track:
        """Get currently selected track for detail panel"""
        if not self.selected_track_id:
            return None
        return next((t for t in self.tracks if t.id == self.selected_track_id), None)


# ========================
# MAIN PAGE LAYOUT
# ========================

def index() -> rx.Component:
    """Main SAGE simulator page"""
    return rx.container(
        # Welcome modal (first visit)
        rx.cond(
            InteractiveSageState.show_welcome,
            tutorial_system.welcome_modal()
        ),
        
        rx.vstack(
            # Header
            rx.heading("AN/FSQ-7 SAGE Simulator", size="9", color="#00ff00"),
            rx.text("Interactive Cold War Air Defense System", color="#88ff88"),
            
            # Main layout: 3 columns
            rx.hstack(
                # LEFT COLUMN: SD Console + Maintenance
                rx.vstack(
                    sd_console.sd_console_master_panel(),
                    tube_maintenance.tube_maintenance_panel(),
                    width="300px",
                    spacing="4"
                ),
                
                # CENTER COLUMN: Radar Scope + Tutorial
                rx.vstack(
                    # Radar scope (main display)
                    rx.box(
                        rx.html(radar_scope.create_radar_scope_component()),
                        width="800px",
                        height="800px",
                        border="2px solid #00ff00",
                        border_radius="8px"
                    ),
                    
                    # Tutorial sidebar (collapsible)
                    rx.cond(
                        InteractiveSageState.tutorial_active,
                        tutorial_system.tutorial_sidebar_compact()
                    ),
                    
                    width="820px",
                    spacing="4"
                ),
                
                # RIGHT COLUMN: CPU Trace + Light Gun
                rx.vstack(
                    execution_trace_panel.execution_trace_panel_compact(),
                    light_gun.track_detail_panel(),
                    light_gun.light_gun_controls(),
                    width="350px",
                    spacing="4"
                ),
                
                spacing="5",
                align="start"
            ),
            
            spacing="5",
            padding="20px"
        ),
        
        # Inject radar update script
        rx.html(radar_scope.radar_update_script(
            InteractiveSageState.get_tracks_json(),
            InteractiveSageState.get_overlays_json(),
            InteractiveSageState.get_geo_json()
        )),
        
        # Inject CSS
        rx.html(radar_scope.RADAR_SCOPE_CSS),
        rx.html(tube_maintenance.TUBE_ANIMATIONS_CSS),
        rx.html(light_gun.LIGHT_GUN_KEYBOARD_SCRIPT),
        
        max_width="100%",
        background="#000000"
    )


# Create the Reflex app
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Courier+New:wght@400;700&display=swap"
    ]
)
app.add_page(index, route="/")
