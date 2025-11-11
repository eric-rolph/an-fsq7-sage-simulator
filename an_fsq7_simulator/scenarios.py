import random
import math
from typing import List
from an_fsq7_simulator.interactive_state import (
    Track, TrackType, TrackStatus, SimulatorState
)

# ============================================================================
# Radar Scenario Generator - Creates believable track patterns
# ============================================================================

def spawn_bomber_stream(state: SimulatorState, count: int = 3):
    """Spawn bomber formation from Arctic heading toward NYC"""
    base_x = 0.5 + random.uniform(-0.1, 0.1)
    
    for i in range(count):
        track_id = f"BMB-{1000 + len(state.tracks) + i}"
        
        # Bombers start at top, head south with slight variation
        x = base_x + (i - count//2) * 0.05
        y = 0.05  # Near top
        
        # Heading roughly 180° (south) with spread
        heading = 180 + random.randint(-15, 15)
        speed = random.randint(350, 420)
        altitude = random.randint(35000, 45000)
        
        # Convert heading to velocity
        rad = math.radians(heading)
        speed_norm = speed / 10000.0  # Normalize speed
        vx = speed_norm * math.sin(rad)
        vy = speed_norm * math.cos(rad)
        
        state.tracks.append(Track(
            id=track_id,
            type=TrackType.HOSTILE,
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            altitude=altitude,
            speed=speed,
            heading=heading
        ))

def spawn_missile_launch(state: SimulatorState):
    """Spawn ICBM with countdown"""
    track_id = f"MSL-{2000 + len(state.tracks)}"
    
    # Missiles come from north
    x = 0.5 + random.uniform(-0.2, 0.2)
    y = 0.1
    
    heading = 180 + random.randint(-10, 10)
    speed = random.randint(800, 1200)
    altitude = random.randint(60000, 80000)
    
    rad = math.radians(heading)
    speed_norm = speed / 10000.0
    vx = speed_norm * math.sin(rad)
    vy = speed_norm * math.cos(rad)
    
    # Calculate time to impact (assume target at y=0.8)
    if vy != 0:
        t_minus = int((0.8 - y) / vy)
    else:
        t_minus = 60
    
    state.tracks.append(Track(
        id=track_id,
        type=TrackType.MISSILE,
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        altitude=altitude,
        speed=speed,
        heading=heading,
        t_minus=t_minus
    ))

def spawn_friendly_cap(state: SimulatorState, count: int = 2):
    """Spawn friendly CAP (Combat Air Patrol) aircraft"""
    for i in range(count):
        track_id = f"CAP-{3000 + len(state.tracks) + i}"
        
        # Patrol in middle of scope
        x = 0.4 + i * 0.2
        y = 0.5
        
        # Random patrol heading
        heading = random.randint(0, 359)
        speed = random.randint(300, 400)
        altitude = random.randint(20000, 30000)
        
        rad = math.radians(heading)
        speed_norm = speed / 10000.0
        vx = speed_norm * math.sin(rad)
        vy = speed_norm * math.cos(rad)
        
        state.tracks.append(Track(
            id=track_id,
            type=TrackType.FRIENDLY,
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            altitude=altitude,
            speed=speed,
            heading=heading
        ))

def spawn_interceptor(state: SimulatorState, target_id: str):
    """Launch interceptor toward selected target"""
    target = next((t for t in state.tracks if t.id == target_id), None)
    if not target:
        return
    
    track_id = f"INT-{4000 + len(state.tracks)}"
    
    # Interceptor starts at bottom (airbase)
    x = 0.5
    y = 0.95
    
    # Calculate heading toward target
    dx = target.x - x
    dy = target.y - y
    heading = int(math.degrees(math.atan2(dx, -dy))) % 360
    
    speed = 600  # Fast interceptor
    altitude = 40000
    
    rad = math.radians(heading)
    speed_norm = speed / 10000.0
    vx = speed_norm * math.sin(rad)
    vy = speed_norm * math.cos(rad)
    
    state.tracks.append(Track(
        id=track_id,
        type=TrackType.INTERCEPTOR,
        x=x,
        y=y,
        vx=vx,
        vy=vy,
        altitude=altitude,
        speed=speed,
        heading=heading,
        target_id=target_id
    ))

def move_tracks(tracks: List[Track], dt_ms: int):
    """Update track positions based on velocity"""
    dt_sec = dt_ms / 1000.0
    
    for track in tracks:
        if track.status != TrackStatus.ACTIVE:
            continue
        
        # Store old position for trail
        track.trail.append((track.x, track.y))
        if len(track.trail) > 20:  # Keep last 20 positions
            track.trail.pop(0)
        
        # Update position
        track.x += track.vx * dt_sec
        track.y += track.vy * dt_sec
        
        # Update countdown for missiles
        if track.t_minus is not None:
            track.t_minus -= int(dt_sec)
            if track.t_minus <= 0:
                track.status = TrackStatus.DEPARTED
        
        # Remove tracks that leave scope
        if track.x < -0.1 or track.x > 1.1 or track.y < -0.1 or track.y > 1.1:
            track.status = TrackStatus.DEPARTED
        
        # Interceptors: simple pursuit AI
        if track.type == TrackType.INTERCEPTOR and track.target_id:
            target = next((t for t in tracks if t.id == track.target_id), None)
            if target and target.status == TrackStatus.ACTIVE:
                # Recalculate heading toward target
                dx = target.x - track.x
                dy = target.y - track.y
                heading = int(math.degrees(math.atan2(dx, -dy))) % 360
                track.heading = heading
                
                rad = math.radians(heading)
                speed_norm = track.speed / 10000.0
                track.vx = speed_norm * math.sin(rad)
                track.vy = speed_norm * math.cos(rad)

def resolve_intercepts(tracks: List[Track]):
    """Check if interceptors reached their targets"""
    for interceptor in [t for t in tracks if t.type == TrackType.INTERCEPTOR]:
        if not interceptor.target_id:
            continue
        
        target = next((t for t in tracks if t.id == interceptor.target_id), None)
        if not target or target.status != TrackStatus.ACTIVE:
            continue
        
        # Check distance
        dx = target.x - interceptor.x
        dy = target.y - interceptor.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 0.03:  # Intercept radius
            target.status = TrackStatus.INTERCEPTED
            interceptor.status = TrackStatus.DEPARTED

def maybe_spawn_new(state: SimulatorState):
    """Randomly spawn new tracks based on mission"""
    if state.paused or not state.powered_on:
        return
    
    # Keep 5-10 active tracks
    active_count = sum(1 for t in state.tracks if t.status == TrackStatus.ACTIVE)
    
    if active_count < 5:
        r = random.random()
        if r < 0.3:
            spawn_bomber_stream(state, 1)
        elif r < 0.5:
            spawn_friendly_cap(state, 1)
        elif r < 0.6:
            spawn_missile_launch(state)

def advance_world(dt_ms: int, state: SimulatorState):
    """Main simulation tick function"""
    if state.paused or not state.powered_on:
        return
    
    # Apply performance penalty from failed tubes
    effective_dt = dt_ms * (1.0 + state.maintenance.performance_penalty)
    
    move_tracks(state.tracks, int(effective_dt))
    resolve_intercepts(state.tracks)
    maybe_spawn_new(state)
    
    # Remove departed tracks after a while
    state.tracks = [t for t in state.tracks if t.status != TrackStatus.DEPARTED or len(t.trail) > 0]

def init_scenario(state: SimulatorState, scenario: str = "default"):
    """Initialize a specific scenario"""
    state.tracks.clear()
    
    if scenario == "bomber_raid":
        spawn_bomber_stream(state, 5)
        spawn_friendly_cap(state, 2)
    elif scenario == "missile_attack":
        spawn_missile_launch(state)
        spawn_friendly_cap(state, 2)
    elif scenario == "default":
        spawn_bomber_stream(state, 2)
        spawn_friendly_cap(state, 1)
        spawn_missile_launch(state)
