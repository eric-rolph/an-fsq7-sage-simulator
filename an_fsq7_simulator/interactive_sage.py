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
from typing import List, Set, Optional, Dict, Any
from datetime import datetime
import asyncio
import time
from .components_v2 import script_loader

# Import state model
from . import state_model

# Import simulation models and scenarios
from .sim import models as sim_models
from .sim import scenarios as sim_scenarios
from .sim import scenario_events  # NEW: Dynamic scenario events

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
    network_stations,
    system_messages,  # NEW: Operator goal flow requirement #2
    scenario_selector,  # NEW: Scenario switching UI
    simulation_controls,  # NEW: Pause/play/speed controls
    crt_effects,  # NEW: Authentic P7 phosphor CRT display effects
    track_classification_panel,  # NEW: Manual track classification UI
    interceptor_panel,  # NEW: Interceptor assignment system
    system_inspector,  # NEW: System Inspector Overlay (Priority 3)
    scenario_debrief,  # NEW: Scenario Debrief Panel (Priority 4)
    sound_effects,  # NEW: Sound Effects & Audio Feedback (Priority 5)
)
from .components_v2.radar_scope_native import radar_scope_with_init
from .components_v2.radar_inline_js import RADAR_SCOPE_INLINE_JS


class InteractiveSageState(rx.State):
    """
    Main state container for the interactive SAGE simulator
    Single source of truth for all UI and simulation state
    """
    
    # ===== SIMULATION STATE =====
    tracks: List[state_model.Track] = []
    interceptors: List[state_model.Interceptor] = []
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
    
    # ===== TRACK CLASSIFICATION PANEL STATE =====
    show_classification_panel: bool = False
    classifying_track_id: str = ""
    show_correlation_help: bool = False
    
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
    
    # ===== SYSTEM INSPECTOR STATE (Priority 3) =====
    show_system_inspector: bool = False
    # CPU State
    cpu_accumulator: int = 0
    cpu_index_register: int = 0
    cpu_program_counter: int = 0
    cpu_current_instruction: str = "IDLE"
    cpu_memory_address: int = 0
    cpu_instruction_queue_depth: int = 0
    # Queue State
    radar_queue_depth: int = 0
    track_queue_depth: int = 0
    display_queue_depth: int = 0
    radar_processing_rate: int = 0
    track_processing_rate: int = 0
    display_processing_rate: int = 0
    
    # ===== SCENARIO DEBRIEF STATE (Priority 4) =====
    scenario_complete: bool = False
    scenario_start_time: float = 0.0
    scenario_metrics: Dict[str, Any] = {}
    
    # ===== SOUND EFFECTS STATE (Priority 5) =====
    ambient_volume: float = 0.3
    effects_volume: float = 0.7
    alerts_volume: float = 0.8
    mute_all: bool = False
    sound_enabled: bool = True
    
    # ===== NETWORK STATION VIEW STATE (Priority 6) =====
    show_network_view: bool = False
    selected_station_id: str = ""
    network_stations_data: str = "[]"  # JSON of all stations
    
    # ===== 7x7 SECTOR GRID STATE (IBM DSP Authentic Feature) =====
    show_sector_grid: bool = False
    expansion_level: int = 1  # 1x, 2x, 4x, 8x magnification
    selected_sector_row: int = 3  # 0-6 (center = 3)
    selected_sector_col: int = 3  # 0-6 (center = 3)
    
    # ===== SCENARIO EVENT SYSTEM STATE (Dynamic Scenarios) =====
    _event_timeline: Optional[scenario_events.EventTimeline] = None  # Private - not serialized
    scenario_elapsed_time: float = 0.0  # Seconds since scenario start
    active_events_count: int = 0  # Count of events that have triggered
    
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
                
                # Update interceptor positions and status
                self.update_interceptor_positions(dt=dt)
                
                # Increment world time (milliseconds)
                self.world_time += int(1000 * self.speed_multiplier)
                
                # Process track correlation
                self.process_track_correlation(dt=dt)
                
                # Check tube degradation periodically
                if self.world_time % 10000 == 0:  # Every 10 seconds
                    self.degrade_tubes()
                
                # Update system inspector metrics (Priority 3)
                self.update_system_inspector_metrics()
                
                # Process scenario events (Dynamic scenario system)
                self.process_scenario_events()
    
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
            # Save current position to trail (keep last 7 scans - IBM DSP authentic)
            # IBM Documentation: "the last seven scans were always shown"
            # At 2.5-second refresh cycle: 7 scans = 17.5 seconds of history
            track.trail.append((track.x, track.y))
            if len(track.trail) > 7:
                track.trail = track.trail[-7:]
            
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
    
    def update_interceptor_positions(self, dt: float = 1.0):
        """
        Update interceptor positions, handle status transitions, check for engagements.
        
        Args:
            dt: Time delta in seconds
        """
        import math
        
        for interceptor in self.interceptors:
            # Skip if at base or refueling
            if interceptor.status in ["READY", "REFUELING"]:
                continue
            
            # Find assigned target
            if not interceptor.assigned_target_id:
                continue
            
            target = next((t for t in self.tracks if t.id == interceptor.assigned_target_id), None)
            if not target:
                # Target lost, return to base
                interceptor.status = "RETURNING"
                interceptor.assigned_target_id = None
                continue
            
            # Handle status transitions
            if interceptor.status == "SCRAMBLING":
                # Accelerate to cruise speed
                interceptor.current_speed = min(interceptor.current_speed + 50 * dt, interceptor.max_speed * 0.8)
                interceptor.altitude = min(interceptor.altitude + 500 * dt, 40000)  # Climb to 40k ft
                
                # Transition to AIRBORNE after 10 seconds (rough simulation)
                if interceptor.current_speed >= interceptor.max_speed * 0.5:
                    interceptor.status = "AIRBORNE"
                    self.system_messages_log.append(
                        system_messages.SystemMessage(
                            timestamp=datetime.now().strftime("%H:%M:%S"),
                            category="INTERCEPT",
                            message=f"{interceptor.id} AIRBORNE",
                            details=f"Proceeding to intercept {target.id}"
                        )
                    )
            
            elif interceptor.status == "AIRBORNE":
                # Move toward target
                dx = target.x - interceptor.x
                dy = target.y - interceptor.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < 0.001:  # Already at target
                    continue
                
                # Update heading
                interceptor.heading = int(math.degrees(math.atan2(dy, dx)))
                
                # Speed in knots, dt in seconds, convert to normalized screen units
                # Screen is 0-1 normalized, roughly represents 600 nautical miles
                speed_factor = (interceptor.current_speed / 600.0) * dt
                
                # Move toward target
                heading_rad = math.radians(interceptor.heading)
                interceptor.x += math.cos(heading_rad) * speed_factor
                interceptor.y += math.sin(heading_rad) * speed_factor
                
                # Consume fuel (rough approximation)
                fuel_consumption = 0.1 * dt  # 0.1% per second at full speed
                interceptor.fuel_percent = max(0, interceptor.fuel_percent - fuel_consumption)
                
                # Check weapon range
                if distance <= interceptor.engagement_range:
                    interceptor.status = "ENGAGING"
                    self.system_messages_log.append(
                        system_messages.SystemMessage(
                            timestamp=datetime.now().strftime("%H:%M:%S"),
                            category="INTERCEPT",
                            message=f"{interceptor.id} ENGAGING {target.id}",
                            details=f"Target in weapon range. Distance: {distance * 600:.1f} nm"
                        )
                    )
            
            elif interceptor.status == "ENGAGING":
                # Simulate engagement (simplified)
                # In real system this would involve weapons release, tracking, etc.
                if interceptor.weapons_remaining > 0:
                    # Fire weapon (simplified)
                    import random
                    hit_probability = 0.7  # 70% hit rate
                    if random.random() < hit_probability:
                        # Hit! Remove target
                        self.tracks = [t for t in self.tracks if t.id != target.id]
                        self.system_messages_log.append(
                            system_messages.SystemMessage(
                                timestamp=datetime.now().strftime("%H:%M:%S"),
                                category="INTERCEPT",
                                message=f"SPLASH ONE: {target.id} DESTROYED",
                                details=f"{interceptor.id} successful engagement"
                            )
                        )
                        interceptor.status = "RETURNING"
                        interceptor.assigned_target_id = None
                        interceptor.weapons_remaining -= 1
                    else:
                        # Miss, try again
                        self.system_messages_log.append(
                            system_messages.SystemMessage(
                                timestamp=datetime.now().strftime("%H:%M:%S"),
                                category="INTERCEPT",
                                message=f"{interceptor.id} WEAPON MISS",
                                details=f"Re-engaging {target.id}"
                            )
                        )
                        interceptor.weapons_remaining -= 1
                        if interceptor.weapons_remaining == 0:
                            interceptor.status = "RETURNING"
                            interceptor.assigned_target_id = None
                else:
                    # Out of weapons
                    interceptor.status = "RETURNING"
                    interceptor.assigned_target_id = None
            
            elif interceptor.status == "RETURNING":
                # Return to base
                dx = interceptor.base_x - interceptor.x
                dy = interceptor.base_y - interceptor.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < 0.01:  # Close to base
                    interceptor.status = "REFUELING"
                    interceptor.current_speed = 0
                    interceptor.altitude = 0
                    interceptor.x = interceptor.base_x
                    interceptor.y = interceptor.base_y
                    self.system_messages_log.append(
                        system_messages.SystemMessage(
                            timestamp=datetime.now().strftime("%H:%M:%S"),
                            category="INTERCEPT",
                            message=f"{interceptor.id} LANDED",
                            details=f"Returned to {interceptor.base_name}"
                        )
                    )
                else:
                    # Fly home
                    heading_rad = math.atan2(dy, dx)
                    interceptor.heading = int(math.degrees(heading_rad))
                    speed_factor = (interceptor.current_speed / 600.0) * dt
                    interceptor.x += math.cos(heading_rad) * speed_factor
                    interceptor.y += math.sin(heading_rad) * speed_factor
    
    def process_track_correlation(self, dt: float = 1.0):
        """
        Auto-correlation timer: uncorrelated → correlating → correlated.
        Simulates SAGE correlation subsystem processing radar returns.
        
        Real SAGE used:
        - IFF (Identify Friend or Foe) transponder responses
        - Velocity profile matching (compare to known aircraft)
        - Flight plan database lookup
        
        For educational simulation, we auto-correlate after 2-3 seconds
        unless track has anomalous characteristics requiring manual classification.
        """
        import random
        
        current_time = self.world_time / 1000.0  # Convert ms to seconds
        
        for track in self.tracks:
            # Skip already correlated tracks
            if track.correlation_state == "correlated":
                continue
            
            # New track: Start as uncorrelated
            if track.correlation_state == "" or track.correlation_state == "uncorrelated":
                # Check if enough time has passed to start correlating (0.5-1 second delay)
                time_since_detection = current_time - track.time_detected
                if time_since_detection > 0.5:
                    # Start correlation process
                    track.correlation_state = "correlating"
            
            # Correlating: Attempt auto-classification after 2-3 seconds
            elif track.correlation_state == "correlating":
                time_since_detection = current_time - track.time_detected
                
                # Determine if auto-correlation succeeds or fails
                # Success criteria (simulated):
                can_auto_classify = True
                confidence = "high"
                reason = "auto_iff"
                
                # Anomalous characteristics requiring manual classification:
                if track.speed > 600:  # Hypersonic (likely missile)
                    can_auto_classify = False
                    confidence = "low"
                elif track.altitude > 60000:  # Extreme altitude
                    can_auto_classify = False
                    confidence = "low"
                elif track.track_type == "unknown":  # No IFF response
                    # 50% chance manual classification required
                    if random.random() < 0.5:
                        can_auto_classify = False
                        confidence = "medium"
                
                # Auto-correlate after 2-3 seconds if possible
                if time_since_detection > (2.0 + random.random()):
                    if can_auto_classify:
                        track.correlation_state = "correlated"
                        track.confidence_level = confidence
                        track.correlation_reason = reason
                        track.classification_time = current_time
                    else:
                        # Stays in correlating or goes back to uncorrelated
                        # (operator must manually classify)
                        track.correlation_state = "uncorrelated"
                        track.confidence_level = confidence
    
    def update_system_inspector_metrics(self):
        """
        Update System Inspector metrics (Priority 3)
        Simulates SAGE computer internal state for educational transparency
        """
        import random
        
        # Simulate CPU state (mock values for now - can integrate real CPU core later)
        self.cpu_accumulator = random.randint(0, 0xFFFFFFFF)
        self.cpu_index_register = len(self.tracks)  # Use track count as index
        self.cpu_program_counter = self.world_time % 0xFFFF
        
        # Current instruction based on what the simulation is doing
        if len(self.tracks) > 0:
            uncorrelated_count = sum(1 for t in self.tracks if t.correlation_state == "uncorrelated")
            if uncorrelated_count > 0:
                self.cpu_current_instruction = f"CORRELATE_TRACK ({uncorrelated_count} pending)"
            else:
                self.cpu_current_instruction = "UPDATE_POSITIONS"
        else:
            self.cpu_current_instruction = "IDLE"
        
        self.cpu_memory_address = (self.world_time * 7) % 0xFFFF
        self.cpu_instruction_queue_depth = min(len(self.tracks) // 2, 15)
        
        # Queue metrics
        self.radar_queue_depth = len(self.tracks) * 2  # Each track has 2 radar returns
        self.track_queue_depth = sum(1 for t in self.tracks if t.correlation_state != "correlated")
        self.display_queue_depth = min(len(self.tracks) + len(self.interceptors), 30)
        
        # Processing rates (simulated)
        self.radar_processing_rate = 45 + random.randint(-5, 5)
        self.track_processing_rate = 12 + random.randint(-2, 2)
        self.display_processing_rate = 60  # 60 FPS
    
    def process_scenario_events(self):
        """
        Process scenario event timeline - triggers dynamic events during scenarios.
        Called every simulation tick to check for events that should fire.
        """
        if not self._event_timeline:
            return
        
        # Check for events that should trigger
        triggered_events = self._event_timeline.check_and_trigger(self.world_time, self)
        
        # Process each triggered event
        for event in triggered_events:
            print(f"[EVENT] Triggered: {event.event_type.name} at {self.scenario_elapsed_time:.1f}s")
            self.handle_scenario_event(event)
            self.active_events_count += 1
        
        # Update scenario elapsed time for display
        self.scenario_elapsed_time = self._event_timeline.get_elapsed_time(self.world_time)
    
    def handle_scenario_event(self, event: scenario_events.ScenarioEvent):
        """Execute a specific scenario event"""
        import math
        
        if event.event_type == scenario_events.EventType.SPAWN_TRACK:
            # Spawn new track
            data = event.data
            heading_rad = math.radians(data["heading"])
            speed_scale = 0.00005
            vx = math.cos(heading_rad) * data["speed"] * speed_scale
            vy = math.sin(heading_rad) * data["speed"] * speed_scale
            
            new_track = state_model.Track(
                id=data["track_id"],
                x=data["x"],
                y=data["y"],
                vx=vx,
                vy=vy,
                altitude=data["altitude"],
                speed=int(data["speed"]),
                heading=int(data["heading"]),
                track_type=data["track_type"].lower(),
                threat_level=data["threat_level"],
                time_detected=self.world_time / 1000.0
            )
            self.tracks.append(new_track)
            
            # System message if provided
            if data.get("message"):
                self.system_messages_log.append(
                    system_messages.SystemMessage(
                        timestamp=datetime.now().strftime("%H:%M:%S"),
                        category="DETECTION",
                        message=data["message"]
                    )
                )
        
        elif event.event_type == scenario_events.EventType.COURSE_CHANGE:
            # Change existing track course
            data = event.data
            track = next((t for t in self.tracks if t.id == data["track_id"]), None)
            if track:
                if data.get("new_heading") is not None:
                    heading_rad = math.radians(data["new_heading"])
                    speed_scale = 0.00005
                    speed = data.get("new_speed", track.speed)
                    track.vx = math.cos(heading_rad) * speed * speed_scale
                    track.vy = math.sin(heading_rad) * speed * speed_scale
                    track.heading = int(data["new_heading"])
                
                if data.get("new_speed") is not None:
                    track.speed = int(data["new_speed"])
                    # Recalculate velocity with new speed
                    heading_rad = math.radians(track.heading)
                    speed_scale = 0.00005
                    track.vx = math.cos(heading_rad) * track.speed * speed_scale
                    track.vy = math.sin(heading_rad) * track.speed * speed_scale
                
                if data.get("message"):
                    self.system_messages_log.append(
                        system_messages.SystemMessage(
                            timestamp=datetime.now().strftime("%H:%M:%S"),
                            category="TRACK",
                            message=data["message"]
                        )
                    )
        
        elif event.event_type == scenario_events.EventType.THREAT_ESCALATION:
            # Escalate threat level
            data = event.data
            track = next((t for t in self.tracks if t.id == data["track_id"]), None)
            if track:
                track.threat_level = data["new_threat_level"]
                
                if data.get("message"):
                    self.system_messages_log.append(
                        system_messages.SystemMessage(
                            timestamp=datetime.now().strftime("%H:%M:%S"),
                            category="WARNING",
                            message=data["message"]
                        )
                    )
        
        elif event.event_type == scenario_events.EventType.EQUIPMENT_FAILURE:
            # Trigger tube failures
            data = event.data
            tube_ids = data.get("tube_ids")
            count = data.get("count", 1)
            
            if tube_ids:
                # Specific tubes
                for tube_id in tube_ids:
                    if 0 <= tube_id < len(self.maintenance.tubes):
                        tube = self.maintenance.tubes[tube_id]
                        tube.status = "degrading"
                        tube.health = 50
            else:
                # Random tubes
                import random
                healthy_tubes = [t for t in self.maintenance.tubes if t.status == "ok"]
                for _ in range(min(count, len(healthy_tubes))):
                    if healthy_tubes:
                        tube = random.choice(healthy_tubes)
                        tube.status = "degrading"
                        tube.health = 50
                        healthy_tubes.remove(tube)
            
            if data.get("message"):
                self.system_messages_log.append(
                    system_messages.SystemMessage(
                        timestamp=datetime.now().strftime("%H:%M:%S"),
                        category="MAINTENANCE",
                        message=data["message"]
                    )
                )
        
        elif event.event_type == scenario_events.EventType.SYSTEM_MESSAGE:
            # Display system message
            data = event.data
            self.system_messages_log.append(
                system_messages.SystemMessage(
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    category=data.get("category", "SYSTEM"),
                    message=data["message"],
                    details=data.get("details")
                )
            )
        
        elif event.event_type == scenario_events.EventType.WAVE_SPAWN:
            # Spawn multiple tracks as wave
            data = event.data
            for track_data in data["tracks"]:
                heading_rad = math.radians(track_data["heading"])
                speed_scale = 0.00005
                vx = math.cos(heading_rad) * track_data["speed"] * speed_scale
                vy = math.sin(heading_rad) * track_data["speed"] * speed_scale
                
                new_track = state_model.Track(
                    id=track_data["track_id"],
                    x=track_data["x"],
                    y=track_data["y"],
                    vx=vx,
                    vy=vy,
                    altitude=track_data["altitude"],
                    speed=int(track_data["speed"]),
                    heading=int(track_data["heading"]),
                    track_type=track_data["track_type"].lower(),
                    threat_level=track_data["threat_level"],
                    time_detected=self.world_time / 1000.0
                )
                self.tracks.append(new_track)
            
            if data.get("message"):
                self.system_messages_log.append(
                    system_messages.SystemMessage(
                        timestamp=datetime.now().strftime("%H:%M:%S"),
                        category="WARNING",
                        message=data["message"]
                    )
                )
    
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
        
        # Initialize interceptors at nearby airbases
        self.interceptors = [
            state_model.Interceptor(
                id="INT-001",
                aircraft_type="F-106 Delta Dart",
                base_name="Otis AFB",
                base_x=0.85, base_y=0.25,  # Cape Cod area
                status="READY",
                fuel_percent=100,
                max_speed=1525,  # Mach 2+
                weapon_type="AIM-4 Falcon",
                weapons_remaining=4
            ),
            state_model.Interceptor(
                id="INT-002",
                aircraft_type="F-102 Delta Dagger",
                base_name="Hanscom Field",
                base_x=0.82, base_y=0.30,  # Bedford, MA
                status="READY",
                fuel_percent=100,
                max_speed=825,
                weapon_type="AIM-4 Falcon",
                weapons_remaining=6
            ),
            state_model.Interceptor(
                id="INT-003",
                aircraft_type="F-89 Scorpion",
                base_name="Suffolk County AFB",
                base_x=0.75, base_y=0.15,  # Long Island
                status="REFUELING",
                fuel_percent=45,
                max_speed=636,
                weapon_type="MB-1 Genie",
                weapons_remaining=2
            ),
        ]
        
        # Initialize scenario event timeline
        events = scenario_events.get_events_for_scenario(scenario_name)
        self._event_timeline = scenario_events.EventTimeline(events)
        self._event_timeline.reset(self.world_time)
        self.scenario_elapsed_time = 0.0
        self.active_events_count = 0
        
        # Log scenario load
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                category="SCENARIO",
                message=f"Loaded: {scenario.name}",
                details=f"{len(self.tracks)} tracks, {len(self.interceptors)} interceptors"
            )
        )
    
    def change_scenario(self, scenario_name: str):
        """Change to a different scenario"""
        print(f"[SCENARIO] change_scenario called with: {scenario_name}")
        print(f"[SCENARIO] Before load - messages count: {len(self.system_messages_log)}")
        self.load_scenario(scenario_name)
        print(f"[SCENARIO] After load - messages count: {len(self.system_messages_log)}, tracks: {[t.id for t in self.tracks]}")
        # Log scenario change
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                category="SCENARIO",
                message=f"Scenario changed to: {scenario_name}",
                details=f"{len(self.tracks)} tracks loaded"
            )
        )
        print(f"[SCENARIO] After message append - messages count: {len(self.system_messages_log)}")
    
    def pause_simulation(self):
        """Pause the simulation loop"""
        self.is_paused = True
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
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
                timestamp=datetime.now().strftime("%H:%M:%S"),
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
                timestamp=datetime.now().strftime("%H:%M:%S"),
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
        # Note: Sound trigger handled by JavaScript via window.playSound()
    
    def disarm_lightgun(self):
        """Deactivate light gun (press ESC key)"""
        self.lightgun_armed = False
        self.selected_track_id = ""
    
    def handle_track_click(self):
        """Handle track click from canvas - reads track ID from button data attribute"""
        # Get track ID from the hidden button's data attribute
        # This is set by JavaScript when canvas is clicked
        # Note: In Reflex, we can't directly read DOM attributes during event handling
        # Instead, we'll use a different approach - pass track ID via event payload
        pass  # Will be handled by JavaScript directly calling select_track
    
    def select_track(self, track_id: str):
        """User clicked a track with armed light gun"""
        if not self.lightgun_armed:
            return
        
        self.selected_track_id = track_id
        # Note: lightgun_select sound triggered by JavaScript on canvas click
        
        # Mark track as selected in state
        for track in self.tracks:
            track.selected = (track.id == track_id)
        
        # If track is uncorrelated, open classification panel
        target = next((t for t in self.tracks if t.id == track_id), None)
        if target and target.correlation_state in ["uncorrelated", "correlating"]:
            self.show_classification_panel = True
            self.classifying_track_id = track_id
    
    def assign_interceptor(self, interceptor_id: str, track_id: str = ""):
        """Assign an interceptor to engage a hostile track"""
        # Use selected track if no track_id provided
        target_id = track_id if track_id else self.selected_track_id
        if not target_id:
            return
        
        # Find target track
        target = next((t for t in self.tracks if t.id == target_id), None)
        if not target:
            return
        
        # Find interceptor
        interceptor = next((i for i in self.interceptors if i.id == interceptor_id), None)
        if not interceptor or interceptor.status != "READY":
            return
        
        # Assign interceptor to target
        interceptor.assigned_target_id = target_id
        interceptor.status = "SCRAMBLING"
        target.interceptor_assigned = True
        # Note: intercept_launch sound triggered by JavaScript via window.playSound('intercept_launch', 'effect')
        
        # Calculate distance for logging
        import math
        distance = math.sqrt((interceptor.x - target.x)**2 + (interceptor.y - target.y)**2)
        # Convert normalized distance to nautical miles (screen is ~600nm)
        distance_nm = distance * 600
        
        # Log assignment
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                category="INTERCEPT",
                message=f"INTERCEPTOR ASSIGNED: {interceptor_id} → {target_id}",
                details=f"{interceptor.aircraft_type} scrambling from {interceptor.base_name}. Distance: {distance_nm:.0f} nm"
            )
        )
    
    def get_best_interceptor_for_track(self, track_id: str) -> str:
        """
        Auto-suggest best interceptor for a track based on:
        - Distance (closer is better)
        - Fuel (more fuel is better)
        - Status (READY only)
        - Speed (faster gets there sooner)
        """
        target = next((t for t in self.tracks if t.id == track_id), None)
        if not target:
            return ""
        
        import math
        best_interceptor = None
        best_score = -1
        
        for interceptor in self.interceptors:
            if interceptor.status != "READY":
                continue
            
            # Calculate distance
            distance = math.sqrt((interceptor.x - target.x)**2 + (interceptor.y - target.y)**2)
            
            # Scoring: lower distance, higher fuel, higher speed = better score
            # Normalize distance (0-1 screen units), invert so closer is better
            distance_score = 1.0 - min(distance, 1.0)
            fuel_score = interceptor.fuel_percent / 100.0
            speed_score = interceptor.max_speed / 2000.0  # Normalize to typical max speed
            
            # Weighted combination (distance is most important)
            total_score = (distance_score * 0.6) + (fuel_score * 0.2) + (speed_score * 0.2)
            
            if total_score > best_score:
                best_score = total_score
                best_interceptor = interceptor
        
        return best_interceptor.id if best_interceptor else ""
    
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
    # TRACK CLASSIFICATION
    # ========================
    
    def classify_track_hostile(self):
        """Manually classify track as hostile"""
        if not self.classifying_track_id:
            return
        
        track = next((t for t in self.tracks if t.id == self.classifying_track_id), None)
        if track:
            track.track_type = "hostile"
            track.correlation_state = "correlated"
            track.confidence_level = "high"
            track.correlation_reason = "manual"
            track.classification_time = self.world_time / 1000.0
            # Note: hostile_alert sound triggered by JavaScript via window.playSound('hostile_alert', 'alert')
            
            self.system_messages_log.append(
                system_messages.SystemMessage(
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    level="warning",
                    category="classification",
                    message=f"HOSTILE CLASSIFIED: {track.id}",
                    details=f"Manual classification by operator"
                )
            )
        
        self.show_classification_panel = False
        self.classifying_track_id = ""
    
    def classify_track_friendly(self):
        """Manually classify track as friendly"""
        if not self.classifying_track_id:
            return
        
        track = next((t for t in self.tracks if t.id == self.classifying_track_id), None)
        if track:
            track.track_type = "friendly"
            track.correlation_state = "correlated"
            track.confidence_level = "high"
            track.correlation_reason = "manual"
            track.classification_time = self.world_time / 1000.0
            
            self.system_messages_log.append(
                system_messages.SystemMessage(
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    level="info",
                    category="classification",
                    message=f"FRIENDLY CLASSIFIED: {track.id}",
                    details=f"Manual classification by operator"
                )
            )
        
        self.show_classification_panel = False
        self.classifying_track_id = ""
    
    def classify_track_unknown(self):
        """Manually classify track as unknown"""
        if not self.classifying_track_id:
            return
        
        track = next((t for t in self.tracks if t.id == self.classifying_track_id), None)
        if track:
            track.track_type = "unknown"
            track.correlation_state = "correlated"
            track.confidence_level = "medium"
            track.correlation_reason = "manual"
            track.classification_time = self.world_time / 1000.0
            
            self.system_messages_log.append(
                system_messages.SystemMessage(
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    level="info",
                    category="classification",
                    message=f"UNKNOWN CLASSIFIED: {track.id}",
                    details=f"Manual classification by operator"
                )
            )
        
        self.show_classification_panel = False
        self.classifying_track_id = ""
    
    def ignore_track(self):
        """Mark track to be ignored (remove from display)"""
        if not self.classifying_track_id:
            return
        
        # Remove track from list
        self.tracks = [t for t in self.tracks if t.id != self.classifying_track_id]
        
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                level="info",
                category="classification",
                message=f"TRACK IGNORED: {self.classifying_track_id}",
                details=f"Track removed from scope by operator"
            )
        )
        
        self.show_classification_panel = False
        self.classifying_track_id = ""
    
    def close_classification_panel(self):
        """Close classification panel without action"""
        self.show_classification_panel = False
        self.classifying_track_id = ""
    
    def toggle_correlation_help(self):
        """Toggle correlation help panel"""
        self.show_correlation_help = not self.show_correlation_help
    
    
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
                timestamp=datetime.now().strftime("%H:%M:%S"),
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
                timestamp=datetime.now().strftime("%H:%M:%S"),
                category="INFO",
                message=f"Overlay {action.upper()}",
                details=f"Display: {overlay_name.replace('_', ' ').upper()}"
            )
        )
    
    # ========================
    # 7x7 SECTOR GRID CONTROLS
    # ========================
    
    def toggle_sector_grid(self):
        """Toggle 7x7 sector grid overlay"""
        self.show_sector_grid = not self.show_sector_grid
        action = "ENABLED" if self.show_sector_grid else "DISABLED"
        self.add_system_message(f"7×7 Sector Grid {action}")
    
    def select_sector_row(self, row: int):
        """Select sector row (0-6, displayed as 1-7)"""
        self.selected_sector_row = row
        self.add_system_message(f"Selected Row {row + 1}")
    
    def select_sector_col(self, col: int):
        """Select sector column (0-6, displayed as A-G)"""
        self.selected_sector_col = col
        self.add_system_message(f"Selected Column {chr(65 + col)}")
    
    def set_expansion_level(self, level: int):
        """Set expansion magnification level (1x/2x/4x/8x)"""
        self.expansion_level = level
        sector_label = f"{self.selected_sector_row + 1}-{chr(65 + self.selected_sector_col)}"
        self.add_system_message(f"Magnification: {level}X | Sector {sector_label}")
    
    def toggle_system_inspector(self):
        """Toggle System Inspector Overlay (Shift+I) - Priority 3"""
        self.show_system_inspector = not self.show_system_inspector
        
        # Log the toggle
        action = "OPENED" if self.show_system_inspector else "CLOSED"
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now(),
                category="INFO",
                message=f"System Inspector {action}",
                details="Press Shift+I to toggle"
            )
        )
    
    # ========================
    # SCENARIO DEBRIEF HANDLERS (Priority 4)
    # ========================
    
    def close_debrief(self):
        """Close debrief panel and continue to next scenario"""
        self.scenario_complete = False
        self.scenario_metrics = {}
    
    def restart_scenario(self):
        """Restart current scenario"""
        self.scenario_complete = False
        self.scenario_metrics = {}
        self.load_scenario(self.current_scenario_name)
        self.start_simulation()
    
    def next_scenario(self):
        """Load next scenario in sequence"""
        scenarios = list(sim_scenarios.SCENARIOS.keys())
        current_idx = scenarios.index(self.current_scenario_name) if self.current_scenario_name in scenarios else 0
        next_idx = (current_idx + 1) % len(scenarios)
        next_scenario_name = scenarios[next_idx]
        
        self.scenario_complete = False
        self.scenario_metrics = {}
        self.load_scenario(next_scenario_name)
        self.start_simulation()
    
    def complete_scenario(self):
        """Complete current scenario and show debrief"""
        # Create metrics from current state
        from .state_model import ScenarioMetrics
        
        metrics = ScenarioMetrics()
        metrics.scenario_duration = time.time() - self.scenario_start_time
        
        # Track metrics
        metrics.tracks_detected = len([t for t in self.tracks])
        metrics.tracks_total = len(self.tracks)  # TODO: Track this from scenario initial state
        
        # Classification metrics
        metrics.total_classifications = len([t for t in self.tracks if t.correlation_state == "correlated"])
        # Assume correct if correlated (real version would check against ground truth)
        metrics.correct_classifications = metrics.total_classifications
        
        # Intercept metrics
        metrics.attempted_intercepts = len([i for i in self.interceptors if i.status != "READY"])
        metrics.successful_intercepts = len([i for i in self.interceptors if i.status == "ENGAGING"])
        
        # Get objectives from scenario
        scenario = sim_scenarios.SCENARIOS.get(self.current_scenario_name)
        if scenario:
            metrics.objectives = scenario.objectives
            metrics.success_criteria = scenario.success_criteria
            # Mark all objectives as complete for now (would check actual conditions in real version)
            metrics.completed_objectives = [True] * len(scenario.objectives)
        
        # Add learning moments (examples)
        if metrics.correct_classifications < metrics.tracks_total:
            metrics.add_learning_moment(
                "warning",
                "Incomplete Classification",
                f"Only {metrics.correct_classifications}/{metrics.tracks_total} tracks were classified",
                "Use light gun to manually classify uncorrelated tracks"
            )
        
        if metrics.attempted_intercepts == 0 and metrics.tracks_total > 0:
            metrics.add_learning_moment(
                "error",
                "No Interceptors Assigned",
                "No interceptors were scrambled to engage threats",
                "Select hostile tracks and click 'ASSIGN TO TARGET' to scramble interceptors"
            )
        
        # Calculate overall score
        metrics.calculate_overall_score()
        
        # Set state
        self.scenario_metrics = metrics.to_dict()
        self.scenario_complete = True
        self.stop_simulation()
    
    # ========================
    # SOUND EFFECTS HANDLERS (Priority 5)
    # ========================
    
    def play_sound(self, sound_id: str, category: str = "effects"):
        """Trigger a sound effect (handled by JavaScript)"""
        # Sound playing is handled by JavaScript SAGESoundPlayer
        # This method exists to be called from event handlers
        pass
    
    def set_ambient_volume(self, volume: list[float]):
        """Set ambient sounds volume (0.0-1.0) - slider passes list[float]"""
        vol = volume[0] if volume else 0.5
        self.ambient_volume = max(0.0, min(1.0, vol))
        return rx.call_script(f"window.setSoundVolume('ambient', {self.ambient_volume})")
    
    def set_effects_volume(self, volume: list[float]):
        """Set effects sounds volume (0.0-1.0) - slider passes list[float]"""
        vol = volume[0] if volume else 0.5
        self.effects_volume = max(0.0, min(1.0, vol))
        return rx.call_script(f"window.setSoundVolume('effects', {self.effects_volume})")
    
    def set_alerts_volume(self, volume: list[float]):
        """Set alert sounds volume (0.0-1.0) - slider passes list[float]"""
        vol = volume[0] if volume else 0.5
        self.alerts_volume = max(0.0, min(1.0, vol))
        return rx.call_script(f"window.setSoundVolume('alerts', {self.alerts_volume})")
    
    def toggle_sound_mute(self):
        """Toggle all sounds on/off"""
        self.mute_all = not self.mute_all
        return rx.call_script(f"window.muteSounds({str(self.mute_all).lower()})")
    
    def set_sound_preset(self, preset: str):
        """Apply sound volume preset (silent/subtle/normal/immersive)"""
        presets = {
            "silent": (0.0, 0.0, 0.0),
            "subtle": (0.1, 0.3, 0.4),
            "normal": (0.3, 0.7, 0.8),
            "immersive": (0.5, 1.0, 1.0)
        }
        if preset in presets:
            self.ambient_volume, self.effects_volume, self.alerts_volume = presets[preset]
            # Update all three volumes in JavaScript
            return [
                rx.call_script(f"window.setSoundVolume('ambient', {self.ambient_volume})"),
                rx.call_script(f"window.setSoundVolume('effects', {self.effects_volume})"),
                rx.call_script(f"window.setSoundVolume('alerts', {self.alerts_volume})")
            ]
    
    # ========================
    # NETWORK STATION VIEW HANDLERS (Priority 6)
    # ========================
    
    def toggle_network_view(self):
        """Toggle network station overlay"""
        self.show_network_view = not self.show_network_view
    
    def select_station(self, station_id: str):
        """Select a station to view details"""
        self.selected_station_id = station_id
    
    def simulate_station_failure(self, station_id: str):
        """Simulate a radar station going offline"""
        # Future: update station status in network_stations_data
        pass
    
    def restore_station(self, station_id: str):
        """Bring a failed station back online"""
        # Future: restore station status in network_stations_data
        pass
    
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
    
    def add_system_message(self, message: str, category: str = "INFO", details: str = ""):
        """Helper method to add a system message to the log"""
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                category=category,
                message=message,
                details=details
            )
        )
    
    
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
            "trail": getattr(t, 'trail', []),  # Include trail history for rendering
            "correlation_state": getattr(t, 'correlation_state', 'correlated'),
            "confidence_level": getattr(t, 'confidence_level', 'high'),
            "correlation_reason": getattr(t, 'correlation_reason', ''),
        } for t in filtered_tracks])
    
    def get_overlays_json(self) -> str:
        """Serialize active overlays"""
        return json.dumps(list(self.active_overlays))
    
    def get_geo_json(self) -> str:
        """Serialize geographic data"""
        from .components_v2 import geographic_overlays
        
        # Build coastlines data
        coastlines = []
        for coastline in [geographic_overlays.EAST_COAST_OUTLINE, 
                         geographic_overlays.GREAT_LAKES_OUTLINE]:
            coastlines.append({
                "name": coastline.name,
                "style": coastline.style,
                "points": [[p.x, p.y] for p in coastline.points]
            })
        
        # Build cities data
        cities = [{
            "label": city.label,
            "x": city.x,
            "y": city.y
        } for city in geographic_overlays.MAJOR_CITIES]
        
        # Build range rings data (already dicts, just copy)
        range_rings = geographic_overlays.RANGE_RINGS
        
        # Build bearing markers (already dicts, just copy)
        bearing_markers = geographic_overlays.BEARING_MARKERS
        
        return json.dumps({
            "coastlines": coastlines,
            "cities": cities,
            "range_rings": range_rings,
            "bearing_markers": bearing_markers
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
    def classifying_track(self) -> Optional[state_model.Track]:
        """Get track being classified in classification panel (computed var)"""
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track
        # Return default empty track if not found
        return state_model.Track(
            id="",
            x=0.0,
            y=0.0,
            altitude=0,
            speed=0,
            heading=0,
            track_type="unknown",
            correlation_state="uncorrelated",
            confidence_level="unknown"
        )
    
    @rx.var
    def tracks_json_var(self) -> str:
        """Embed filtered tracks as JSON for JavaScript access (computed var)"""
        return self.get_tracks_json()
    
    @rx.var
    def tracks_script_tag(self) -> str:
        """Return complete script tag with tracks data - for rx.html injection"""
        return f"<script>window.__SAGE_TRACKS__ = {self.get_tracks_json()};</script>"
    
    @rx.var
    def world_time_seconds(self) -> float:
        """Convert world_time from milliseconds to seconds for UI display"""
        return self.world_time / 1000.0
    
    @rx.var
    def geo_json_var(self) -> str:
        """Embed geographic data as JSON for JavaScript access (computed var)"""
        return self.get_geo_json()
    
    @rx.var
    def geo_script_tag(self) -> str:
        """Return complete script tag with geo data - for rx.html injection"""
        return f"<script>window.__SAGE_GEO__ = {self.get_geo_json()};</script>"
    
    def get_interceptors_json(self) -> str:
        """Convert interceptors list to JSON for JavaScript"""
        interceptors_data = [
            {
                "id": i.id,
                "x": i.x,
                "y": i.y,
                "heading": i.heading,
                "status": i.status,
                "assigned_target_id": i.assigned_target_id if i.assigned_target_id else None,
            }
            for i in self.interceptors
        ]
        return json.dumps(interceptors_data)
    
    @rx.var
    def interceptors_json_var(self) -> str:
        """Embed interceptors as JSON for JavaScript access (computed var)"""
        return self.get_interceptors_json()
    
    @rx.var
    def interceptors_script_tag(self) -> str:
        """Return complete script tag with interceptors data - for rx.html injection"""
        return f"<script>window.__SAGE_INTERCEPTORS__ = {self.get_interceptors_json()};</script>"
    
    @rx.var
    def sector_grid_script_tag(self) -> str:
        """Return complete script tag with 7x7 sector grid state - for rx.html injection"""
        data = {
            "show_sector_grid": self.show_sector_grid,
            "expansion_level": self.expansion_level,
            "selected_sector_row": self.selected_sector_row,
            "selected_sector_col": self.selected_sector_col,
        }
        return f"<script>window.__SAGE_SECTOR_GRID__ = {json.dumps(data)};</script>"
    
    def get_network_stations_json(self) -> str:
        """Convert network stations to JSON for JavaScript rendering"""
        stations_data = [
            {
                "id": s.id,
                "name": s.name,
                "station_type": s.station_type,
                "x": s.x,
                "y": s.y,
                "coverage_radius": s.coverage_radius,
                "status": s.status,
                "description": s.description
            }
            for s in network_stations.ALL_STATIONS
        ]
        return json.dumps(stations_data)
    
    @rx.var
    def network_stations_script_tag(self) -> str:
        """Inject network stations data for JavaScript rendering"""
        return f"<script>window.__SAGE_NETWORK_STATIONS__ = {self.get_network_stations_json()};</script>"
    
    # Sound config is managed through UI event handlers directly calling JavaScript
    # Initial volumes are set in SOUND_PLAYER_SCRIPT constructor
    
    # Helper vars for classification panel (avoid nested property access issues)
    @rx.var
    def classifying_track_type(self) -> str:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.track_type
        return "unknown"
    
    @rx.var
    def classifying_correlation_state(self) -> str:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.correlation_state
        return "uncorrelated"
    
    @rx.var
    def classifying_confidence_level(self) -> str:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.confidence_level
        return "unknown"
    
    @rx.var
    def classifying_altitude(self) -> int:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.altitude
        return 0
    
    @rx.var
    def classifying_speed(self) -> int:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.speed
        return 0
    
    @rx.var
    def classifying_heading(self) -> int:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.heading
        return 0
    
    @rx.var
    def classifying_x(self) -> float:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.x
        return 0.0
    
    @rx.var
    def classifying_y(self) -> float:
        for track in self.tracks:
            if track.id == self.classifying_track_id:
                return track.y
        return 0.0
    
    @rx.var
    def sector_label(self) -> str:
        """Computed sector label for display (e.g., '4-D | 2X')"""
        row_num = self.selected_sector_row + 1  # 0-6 -> 1-7
        col_letter = chr(65 + self.selected_sector_col)  # 0-6 -> A-G
        return f"SECTOR {row_num}-{col_letter} | {self.expansion_level}X"
    
    @rx.var
    def system_messages_script_tag(self) -> str:
        """Inject system messages log as JSON for JavaScript access"""
        messages_data = [
            {
                "timestamp": msg.timestamp,
                "category": msg.category,
                "message": msg.message,
                "details": msg.details if hasattr(msg, 'details') and msg.details else ""
            }
            for msg in self.system_messages_log
        ]
        return f"<script>window.__SAGE_SYSTEM_MESSAGES__ = {json.dumps(messages_data)};</script>"


# ========================
# MAIN PAGE LAYOUT
# ========================

def index() -> rx.Component:
    """Main SAGE simulator page"""
    return rx.fragment(
        rx.container(
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
                    # Temporary test button for debrief
                    rx.button(
                        "TEST DEBRIEF",
                        on_click=InteractiveSageState.complete_scenario,
                        size="3",
                        color_scheme="yellow",
                        style={
                            "background": "#FF6600",
                            "border": "2px solid #FFAA00",
                            "font-family": "'Courier New', monospace",
                            "cursor": "pointer"
                        }
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
                    sound_effects.sound_settings_panel(
                        ambient_volume=InteractiveSageState.ambient_volume,
                        effects_volume=InteractiveSageState.effects_volume,
                        alerts_volume=InteractiveSageState.alerts_volume,
                        mute_all=InteractiveSageState.mute_all,
                        state_class=InteractiveSageState
                    ),
                    # Network view toggle (Priority 6)
                    rx.button(
                        rx.cond(
                            InteractiveSageState.show_network_view,
                            "📡 RADAR VIEW",
                            "🌐 NETWORK VIEW"
                        ),
                        on_click=InteractiveSageState.toggle_network_view,
                        size="3",
                        style={
                            "width": "100%",
                            "background": rx.cond(
                                InteractiveSageState.show_network_view,
                                "#00AA00",
                                "#0066AA"
                            ),
                            "border": "2px solid #00ff00",
                            "font-family": "'Courier New', monospace",
                            "cursor": "pointer",
                            "font-weight": "bold"
                        }
                    ),
                    # Network legend (show when network view active)
                    rx.cond(
                        InteractiveSageState.show_network_view,
                        network_stations.network_legend_panel()
                    ),
                    width="300px",
                    spacing="4"
                ),
                
                # CENTER COLUMN: Radar Scope + Tutorial
                rx.vstack(
                    # Radar scope (Canvas with inline initialization)
                    rx.box(
                        radar_scope_with_init(),
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
                
                # RIGHT COLUMN: Simulation Controls + CPU Trace + Light Gun + Interceptors
                rx.vstack(
                    simulation_controls.simulation_control_panel(
                        InteractiveSageState.is_paused,
                        InteractiveSageState.speed_multiplier,
                        InteractiveSageState.world_time,
                        InteractiveSageState.pause_simulation,
                        InteractiveSageState.resume_simulation,
                        InteractiveSageState.set_speed_multiplier
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
                    interceptor_panel.interceptor_panel(),
                    system_messages.system_messages_panel(
                        messages=InteractiveSageState.system_messages_log,
                        max_height="250px",
                        on_clear=InteractiveSageState.clear_system_messages
                    ),
                    execution_trace_panel.execution_trace_panel_compact(
                        InteractiveSageState.cpu_trace
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
        
        # Overlay panels (fixed position)
        rx.cond(
            InteractiveSageState.show_classification_panel,
            track_classification_panel.track_classification_panel(
                track_id=InteractiveSageState.classifying_track_id,
                track_type=InteractiveSageState.classifying_track_type,
                correlation_state=InteractiveSageState.classifying_correlation_state,
                confidence_level=InteractiveSageState.classifying_confidence_level,
                altitude=InteractiveSageState.classifying_altitude,
                speed=InteractiveSageState.classifying_speed,
                heading=InteractiveSageState.classifying_heading,
                x=InteractiveSageState.classifying_x,
                y=InteractiveSageState.classifying_y,
                on_classify_hostile=InteractiveSageState.classify_track_hostile,
                on_classify_friendly=InteractiveSageState.classify_track_friendly,
                on_classify_unknown=InteractiveSageState.classify_track_unknown,
                on_ignore=InteractiveSageState.ignore_track,
                on_close=InteractiveSageState.close_classification_panel
            )
        ),
        
        rx.cond(
            InteractiveSageState.show_correlation_help,
            track_classification_panel.correlation_help_panel()
        ),
        
        # System Inspector Overlay (Priority 3) - Toggle with Shift+I
        system_inspector.system_inspector_overlay(
            show=InteractiveSageState.show_system_inspector,
            accumulator=InteractiveSageState.cpu_accumulator,
            index_register=InteractiveSageState.cpu_index_register,
            program_counter=InteractiveSageState.cpu_program_counter,
            current_instruction=InteractiveSageState.cpu_current_instruction,
            memory_address=InteractiveSageState.cpu_memory_address,
            instruction_queue_depth=InteractiveSageState.cpu_instruction_queue_depth,
            radar_queue_depth=InteractiveSageState.radar_queue_depth,
            track_queue_depth=InteractiveSageState.track_queue_depth,
            display_queue_depth=InteractiveSageState.display_queue_depth,
            radar_processing_rate=InteractiveSageState.radar_processing_rate,
            track_processing_rate=InteractiveSageState.track_processing_rate,
            display_processing_rate=InteractiveSageState.display_processing_rate,
            on_close=InteractiveSageState.toggle_system_inspector
        ),
        
        # Scenario Debrief Panel (Priority 4) - Shows after scenario completion
        scenario_debrief.scenario_debrief_panel(InteractiveSageState),
        
        # Native React component handles data via props - no hidden divs needed!
        
        # Inject CSS and scripts
        rx.html(crt_effects.CRT_DISPLAY_CSS),  # Authentic P7 phosphor CRT effects
        rx.html(radar_scope.RADAR_SCOPE_CSS),
        rx.html(tube_maintenance.TUBE_ANIMATIONS_CSS),
        # Inject track data as complete script tags via computed vars
        rx.html(InteractiveSageState.tracks_script_tag),
        rx.html(InteractiveSageState.geo_script_tag),
        rx.html(InteractiveSageState.interceptors_script_tag),
        rx.html(InteractiveSageState.sector_grid_script_tag),  # 7x7 sector grid state
        rx.html(InteractiveSageState.system_messages_script_tag),  # System messages for event display
        
        # Network station rendering system (Priority 6)
        rx.script(network_stations.NETWORK_RENDERING_SCRIPT),
        rx.html(InteractiveSageState.network_stations_script_tag),
        
        # Enhanced CRT Radar scope with P7 phosphor simulation - external script
        crt_effects.load_crt_script(),
        
        # Sound Effects System (Priority 5) - config managed through UI event handlers
        rx.script(sound_effects.SOUND_PLAYER_SCRIPT),
        
        rx.html(light_gun.LIGHT_GUN_KEYBOARD_SCRIPT),
        
        # System Inspector keyboard shortcut (Shift+I)
        rx.script("""
            document.addEventListener('keydown', function(event) {
                // Shift+I to toggle System Inspector
                if (event.shiftKey && event.key === 'I') {
                    event.preventDefault();
                    console.log('[System Inspector] Shift+I pressed, toggling...');
                    // Trigger Reflex event through WebSocket
                    if (window.__reflex__) {
                        window.__reflex__.toggle_system_inspector();
                    }
                }
            });
        """),
        
        # Bridge canvas track clicks to Reflex event handlers via localStorage
        rx.script("""
            window.__reflex_track_selected = function(trackId) {
                console.log('[Reflex Bridge] Track selected:', trackId);
                // Store in localStorage and trigger a state sync
                localStorage.setItem('sage_selected_track', trackId);
                localStorage.setItem('sage_track_click_timestamp', Date.now().toString());
            };
        """),
        
        max_width="100%",
        background="#000000",
        on_mount=InteractiveSageState.on_page_load
        )
    )


# Create the Reflex app
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Courier+New:wght@400;700&display=swap"
    ],
    head_components=[
        # Priority 8: Authentic SAGE tabular display system
        rx.script(src="/dot_matrix_font.js"),          # 5x7 character matrix font
        rx.script(src="/tabular_track_display.js"),    # 5-feature (A/B/C/D/E) track format
        rx.script(src="/crt_radar.js")                  # Main CRT rendering (includes history trails)
    ]
)
app.add_page(index, route="/")
