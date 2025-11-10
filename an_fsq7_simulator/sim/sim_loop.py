"""
Centralized simulation loop for the AN/FSQ-7 SAGE system.

The Simulator class coordinates all simulation subsystems (radar, tubes,
CPU, mission clock) with a single tick() method that advances time uniformly.
"""

from typing import List, Optional
import time
import random

from .models import RadarTarget, VacuumTubeBank, MissionClock


class Simulator:
    ""`
    Central simulation coordinator for SAGE system.
    
    This class owns all simulation state and provides a single tick(dt) method
    that advances all subsystems consistently. The Reflex UI subscribes to this
    state but does not implement simulation logic.
    `""
    
    def __init__(self, cpu_core=None):
        # Simulation subsystems
        self.tubes = VacuumTubeBank()
        self.mission_clock = MissionClock()
        self.radar_targets: List[RadarTarget] = []
        
        # CPU core reference (injected from FSQ7State to avoid circular import)
        self.cpu_core = cpu_core
        
        # State flags
        self.powered_on = False
        self.system_ready = False
        self.warming_up = False
        
        # Statistics
        self.tracked_objects_count = 0
        self.high_threat_count = 0
        self.intercept_courses_count = 0
        self.alerts_count = 0
        self.successful_intercepts_count = 0
        self.memory_cycles = 0
        
        # Selection state
        self.selected_target_id: Optional[str] = None
        
        # RTC timing
        self._last_rtc_tick = 0.0
        self._rtc_interval = 1.0 / 32.0  # 32 Hz = 31.25ms
    
    def tick(self, dt: float):
        ""`
        Advance simulation by dt seconds.
        
        This is the SINGLE place where simulation state is updated.
        Call this at a consistent frame rate (e.g. 20 Hz = 50ms intervals).
        `""
        
        if not self.powered_on:
            return
        
        # 1. Advance mission clock
        self.mission_clock.tick(dt)
        
        # 2. Update tube system
        if self.warming_up:
            self.tubes.warm_up(dt)
            if self.tubes.is_ready():
                self.system_ready = True
                self.warming_up = False
        else:
            self.tubes.tick(dt)
        
        if not self.system_ready:
            return
        
        # 3. Update radar targets
        for target in self.radar_targets:
            target.move(dt)
            target.wrap_bounds()
        
        # Update statistics
        self.tracked_objects_count = len(self.radar_targets)
        self.high_threat_count = sum(1 for t in self.radar_targets 
                                      if t.threat_level == "HIGH")
        
        # 4. Tick CPU real-time clock at 32 Hz
        if self.cpu_core is not None:
            current_time = time.time()
            if current_time - self._last_rtc_tick >= self._rtc_interval:
                elapsed = current_time - self._last_rtc_tick
                self.cpu_core.tick_rtc(elapsed)
                self._last_rtc_tick = current_time
        
        # 5. Increment memory cycle counter (for display purposes)
        self.memory_cycles += 1
    
    def power_on(self):
        ""`Start system power-on sequence.`""
        if not self.powered_on:
            self.powered_on = True
            self.warming_up = True
            self.system_ready = False
            self._last_rtc_tick = time.time()
    
    def power_off(self):
        ""`Shut down system.`""
        self.powered_on = False
        self.system_ready = False
        self.warming_up = False
        self.tubes.shutdown()
        self.mission_clock.reset()
    
    def spawn_radar_targets(self, count: int = 9):
        ""`Generate random radar targets for demonstration.`""
        self.radar_targets.clear()
        
        target_types = ["AIRCRAFT", "MISSILE", "FRIENDLY", "UNKNOWN"]
        threat_levels = ["LOW", "MEDIUM", "HIGH"]
        
        for i in range(count):
            threat = random.choice(threat_levels)
            target = RadarTarget(
                target_id=f"TGT-{1000 + i}",
                x=random.uniform(50, 750),
                y=random.uniform(50, 550),
                heading=random.uniform(0, 359),
                speed=random.uniform(200, 800),
                altitude=random.randint(5000, 45000),
                target_type=random.choice(target_types),
                threat_level=threat,
            )
            self.radar_targets.append(target)
        
        self.tracked_objects_count = len(self.radar_targets)
        self.high_threat_count = sum(1 for t in self.radar_targets if t.threat_level == "HIGH")
    
    def select_target(self, x: float, y: float, max_distance: float = 30.0) -> Optional[RadarTarget]:
        ""`
        Select nearest radar target to given coordinates.
        Returns the target object if found within max_distance, else None.
        `""
        nearest_target = None
        nearest_distance = max_distance
        
        for target in self.radar_targets:
            distance = target.distance_to(x, y)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_target = target
        
        if nearest_target:
            self.selected_target_id = nearest_target.target_id
        else:
            self.selected_target_id = None
        
        return nearest_target
    
    def get_selected_target(self) -> Optional[RadarTarget]:
        ""`Get currently selected target object.`""
        if not self.selected_target_id:
            return None
        for target in self.radar_targets:
            if target.target_id == self.selected_target_id:
                return target
        return None
    
    def assign_intercept(self):
        ""`Assign an interceptor to the currently selected target.`""
        if self.selected_target_id:
            self.intercept_courses_count += 1
            self.alerts_count += 1
            # Future: Actually spawn interceptor aircraft
    
    def get_radar_targets_as_dicts(self) -> List[dict]:
        ""`
        Convert radar targets to dict format for UI compatibility.
        TODO: Refactor UI to use RadarTarget objects directly.
        `""
        return [
            {
                "target_id": t.target_id,
                "x": t.x,
                "y": t.y,
                "heading": t.heading,
                "speed": t.speed,
                "altitude": t.altitude,
                "target_type": t.target_type,
                "threat_level": t.threat_level,
            }
            for t in self.radar_targets
        ]
