# Simulation Controls Implementation Plan

## Current Status
- Trail rendering system fully operational (commit f619587)
- Scenario selector UI working (commit 54a9be0)
- Demo 3 successfully loaded (6 tracks at 680-800 knots)
- Simulation loop runs continuously at 1 second intervals

## Implementation Task: Simulation Control Panel

### Components to Create
**File**: `an_fsq7_simulator/components_v2/simulation_controls.py`

### Features
1. **Pause/Resume Button**
   - Single button that toggles between "▶ RESUME" and "⏸ PAUSE"
   - Updates based on `is_paused` state
   - Green when running, amber when paused

2. **Speed Multiplier Buttons**
   - Four buttons: 0.5x, 1x, 2x, 5x
   - Highlight current speed (green background)
   - Others use default terminal styling
   - Updates `speed_multiplier` state

3. **Status Display**
   - Show current simulation status: "RUNNING" or "PAUSED"
   - Show current speed multiplier: "Speed: 2.0x"
   - Show elapsed world time in seconds

### State Changes Required
**File**: `an_fsq7_simulator/interactive_sage.py`

Add to InteractiveSageState class:
```python
# ===== SIMULATION CONTROL STATE =====
is_paused: bool = False
speed_multiplier: float = 1.0
```

### Event Handlers

**pause_simulation()**
```python
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
```

**resume_simulation()**
```python
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
```

**set_speed_multiplier(speed: float)**
```python
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
```

### Update Simulation Loop
**File**: `an_fsq7_simulator/interactive_sage.py`

Modify `simulation_tick_loop()`:
```python
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
            if self.world_time % 10000 == 0:
                self.degrade_tubes()
```

### UI Integration
**File**: `an_fsq7_simulator/interactive_sage.py`

Add import:
```python
from .components_v2 import (
    # ... existing imports ...
    simulation_controls,  # NEW
)
```

Wire into page layout (right column, above CPU Trace):
```python
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
    # ... rest of column ...
```

## Testing Plan

### Test 1: Pause/Resume
1. Load Demo 3 (6 tracks)
2. Verify tracks are moving
3. Click PAUSE button
4. Verify tracks stop moving
5. Verify button changes to RESUME
6. Click RESUME
7. Verify tracks resume moving

### Test 2: Speed Multiplier
1. Set speed to 2x
2. Observe tracks move faster
3. Set speed to 0.5x
4. Observe tracks move slower
5. Verify trails accumulate correctly at all speeds

### Test 3: Paused + Speed Change
1. Pause simulation
2. Change speed to 5x
3. Resume
4. Verify tracks move at 5x speed

### Test 4: System Messages
1. Perform pause/resume/speed changes
2. Check system messages log shows:
   - "Simulation PAUSED"
   - "Simulation RESUMED"
   - "Speed set to 2.0x"

## Expected Issues & Solutions

### Issue 1: Reflex Var Comparisons
**Problem**: Can't use `if is_paused` directly with Var objects
**Solution**: Use `rx.cond()` for conditional rendering
```python
rx.cond(
    is_paused,
    rx.button("▶ RESUME", on_click=on_resume),
    rx.button("⏸ PAUSE", on_click=on_pause)
)
```

### Issue 2: Time Display Formatting
**Problem**: Can't use `.strftime()` on Var objects
**Solution**: Format in Python before passing to UI, or use computed vars
```python
@rx.var
def world_time_seconds(self) -> int:
    return self.world_time // 1000
```

### Issue 3: Button Active State
**Problem**: Need to highlight current speed button
**Solution**: Use `rx.cond()` with background color
```python
rx.button(
    "2x",
    on_click=lambda: set_speed(2.0),
    background=rx.cond(
        speed_multiplier == 2.0,
        "#00ff00",  # Active
        "#003300"   # Inactive
    )
)
```

## Success Criteria
✅ Pause button stops track animation  
✅ Resume button restarts track animation  
✅ Speed multiplier changes animation speed  
✅ UI shows current state (paused/running, speed)  
✅ System messages log all control actions  
✅ Trails still render correctly at all speeds  
✅ No errors in browser or backend console  

## Next Steps After Completion
1. Test Demo 4 (Patrol Route scenario)
2. Optimize background task for disconnected clients
3. Add trail length/fade configurability
4. Add more demo scenarios (intercept scenarios, patrol patterns)
5. Implement light gun selection with trails
