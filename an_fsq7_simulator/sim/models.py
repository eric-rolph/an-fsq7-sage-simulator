"""
Simulation domain models for the AN/FSQ-7 SAGE system.

These are pure Python classes representing the physical/logical elements
of the SAGE system, independent of UI presentation.
"""

from dataclasses import dataclass, field
from typing import Optional
import math
import random


@dataclass
class RadarTarget:
    """Represents an aircraft or object being tracked by radar."""
    
    target_id: str
    x: float
    y: float
    heading: float  # degrees, 0 = East, 90 = North
    speed: float    # knots
    altitude: int   # feet
    target_type: str = "UNKNOWN"  # AIRCRAFT, MISSILE, FRIENDLY, UNKNOWN
    threat_level: str = "UNKNOWN"  # LOW, MEDIUM, HIGH, UNKNOWN
    
    def move(self, dt: float):
        """Move target based on heading and speed."""
        heading_rad = math.radians(self.heading)
        # Speed in knots, dt in seconds, convert to screen pixels
        speed_factor = (self.speed / 1000.0) * dt * 20  # Adjusted for frame rate
        self.x += math.cos(heading_rad) * speed_factor
        self.y += math.sin(heading_rad) * speed_factor
    
    def wrap_bounds(self, width: float = 800, height: float = 600):
        """Wrap target position around screen boundaries."""
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0
        if self.y < 0:
            self.y = height
        elif self.y > height:
            self.y = 0
    
    def distance_to(self, x: float, y: float) -> float:
        """Calculate distance to a point."""
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


@dataclass
class VacuumTubeBank:
    """Manages the 58,000 vacuum tubes in the Q-7."""
    
    total_tubes: int = 58000
    active_tubes: int = 0
    failed_tubes: int = 0
    temperature: float = 20.0  # Celsius
    
    # Operational parameters
    target_temperature: float = 270.0
    warmup_time: float = 5.0  # seconds
    failure_rate: float = 0.0001  # probability per tick
    
    def warm_up(self, dt: float):
        """Simulate tube warmup during system startup."""
        if self.temperature < self.target_temperature:
            self.temperature += (self.target_temperature - 20.0) / self.warmup_time * dt
            self.temperature = min(self.temperature, self.target_temperature)
            
            # Activate tubes proportional to temperature
            progress = (self.temperature - 20.0) / (self.target_temperature - 20.0)
            self.active_tubes = int(self.total_tubes * progress)
    
    def is_ready(self) -> bool:
        """Check if tubes are warmed up and system is ready."""
        return self.temperature >= self.target_temperature * 0.95
    
    def tick(self, dt: float):
        """Simulate random tube failures over time."""
        if random.random() < self.failure_rate * dt * 20:  # Adjusted for tick rate
            if self.active_tubes > 0:
                self.active_tubes -= 1
                self.failed_tubes += 1
    
    def shutdown(self):
        """Cool down tubes during system shutdown."""
        self.temperature = 20.0
        self.active_tubes = 0


@dataclass
class MissionClock:
    """Tracks mission elapsed time."""
    
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    
    def tick(self, dt: float):
        """Advance clock by dt seconds."""
        self.seconds += dt
        if self.seconds >= 1.0:
            whole_seconds = int(self.seconds)
            self.seconds -= whole_seconds
            
            self.seconds += whole_seconds
            while self.seconds >= 60:
                self.seconds -= 60
                self.minutes += 1
            while self.minutes >= 60:
                self.minutes -= 60
                self.hours += 1
    
    def to_string(self) -> str:
        """Format as HH:MM:SS."""
        return f"{self.hours:02d}:{self.minutes:02d}:{int(self.seconds):02d}"
    
    def reset(self):
        """Reset clock to 00:00:00."""
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
