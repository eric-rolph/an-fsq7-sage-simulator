# Integration Guide: Refactoring FSQ7State to use Simulator

## Overview

This guide explains how to integrate the new `Simulator` class into the existing `FSQ7State` to centralize simulation logic.

---

## Current State

**File**: `an_fsq7_simulator/an_fsq7_simulator.py`

`FSQ7State` currently:
- Owns all simulation state variables (tubes, radar, CPU, mission clock)
- Implements simulation logic scattered across multiple methods
- Mixes UI state (display brightness, selected program) with simulation state

---

## Target State

`FSQ7State` should:
- Own a `Simulator` instance (`self.simulator`)
- Call `simulator.tick(dt)` from `update_simulation()`
- Read simulation state for UI display (computed properties)
- Only maintain UI-specific state (brightness, selected program dropdown)

---

## Integration Steps

### Step 1: Add Simulator Instance to FSQ7State

```python
# At top of file
from .sim import Simulator, DisplayMode, list_scenarios, load_scenario

class FSQ7State(rx.State):
    # UI-specific state (keep these)
    display_brightness: int = 75
    phosphor_decay: float = 0.85
    selected_program: str = "Array Sum (Authentic)"
    selected_scenario: str = "Demo 1 - Three Inbound"
    animation_frame: int = 0
    
    # Remove these (now in Simulator):
    # power_on, system_ready, startup_progress
    # total_tubes, active_tubes, failed_tubes, tube_temperature
    # memory_cycles
    # radar_targets, tracked_objects, high_threat_count
    # mission_time
    # light_gun_x, light_gun_y, light_gun_active, selected_target
    
    # CPU state (keep for UI binding)
    cpu_accumulator: int = 0
    cpu_ix0: int = 0
    cpu_ix1: int = 0
    cpu_ix2: int = 0
    cpu_ix3: int = 0
    cpu_program_counter: int = 0
    cpu_pc_bank: int = 1
    cpu_rtc: int = 0
    cpu_instruction_count: int = 0
    cpu_halted: bool = True
    cpu_running: bool = False
    
    # Display mode (convert to enum)
    display_mode: DisplayMode = DisplayMode.RADAR
    
    # Private
    _simulator: Optional[Simulator] = None
    _cpu_core: Optional[FSQ7CPU] = None
    
    def _get_simulator(self) -> Simulator:
        if self._simulator is None:
            self._simulator = Simulator(cpu_core=self._get_cpu())
        return self._simulator
```

### Step 2: Add Computed Properties for UI

```python
@rx.var
def power_on(self) -> bool:
    sim = self._get_simulator()
    return sim.powered_on

@rx.var
def system_ready(self) -> bool:
    sim = self._get_simulator()
    return sim.system_ready

@rx.var
def total_tubes(self) -> int:
    sim = self._get_simulator()
    return sim.tubes.total_tubes

@rx.var
def active_tubes(self) -> int:
    sim = self._get_simulator()
    return sim.tubes.active_tubes

@rx.var
def failed_tubes(self) -> int:
    sim = self._get_simulator()
    return sim.tubes.failed_tubes

@rx.var
def tube_temperature(self) -> float:
    sim = self._get_simulator()
    return sim.tubes.temperature

@rx.var
def mission_time(self) -> str:
    sim = self._get_simulator()
    return sim.mission_clock.to_string()

@rx.var
def radar_targets(self) -> List[dict]:
    sim = self._get_simulator()
    return sim.get_radar_targets_as_dicts()

@rx.var
def tracked_objects(self) -> int:
    sim = self._get_simulator()
    return sim.tracked_objects_count

@rx.var
def high_threat_count(self) -> int:
    sim = self._get_simulator()
    return sim.high_threat_count

@rx.var
def memory_cycles(self) -> int:
    sim = self._get_simulator()
    return sim.memory_cycles

@rx.var
def selected_target(self) -> str:
    sim = self._get_simulator()
    return sim.selected_target_id or ""
```

### Step 3: Refactor Event Handlers

```python
def power_on_system(self):
    sim = self._get_simulator()
    sim.power_on()

def power_off_system(self):
    sim = self._get_simulator()
    sim.power_off()
    self.cpu_running = False

def toggle_display_mode(self):
    from .sim import cycle_mode
    self.display_mode = cycle_mode(self.display_mode)

def light_gun_click(self, x: int, y: int):
    sim = self._get_simulator()
    from .sim import get_mode_info
    
    mode_info = get_mode_info(self.display_mode)
    if mode_info.allows_light_gun:
        target = sim.select_target(x, y)
        # target is now a RadarTarget object or None

def clear_light_gun(self):
    sim = self._get_simulator()
    sim.selected_target_id = None

def assign_intercept(self):
    sim = self._get_simulator()
    if sim.selected_target_id and self.intercept_mode:
        sim.assign_intercept()

def load_scenario(self, scenario_name: str):
    from .sim import load_scenario as load_sim_scenario
    sim = self._get_simulator()
    load_sim_scenario(sim, scenario_name)
    self.selected_scenario = scenario_name
```

### Step 4: Refactor update_simulation

```python
async def update_simulation(self):
    import asyncio
    
    last_time = time.time()
    
    while True:
        await asyncio.sleep(0.05)  # 20 FPS
        
        async with self:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # SINGLE CALL to advance all simulation
            sim = self._get_simulator()
            sim.tick(dt)
            
            # Sync CPU state to UI variables (if not running)
            if not self.cpu_running:
                self.sync_cpu_state()
            
            self.animation_frame += 1
```

### Step 5: Remove Old Methods

Delete these methods (logic now in Simulator):
- `startup_sequence()` → handled by `Simulator.tick()` during warmup
- `generate_sample_targets()` → replaced by `load_scenario()`
- `tick_rtc()` → handled by `Simulator.tick()`

---

## UI Component Updates

### Add Status Bar Component

Create `components/status_bar.py`:

```python
import reflex as rx
from ..sim import get_mode_info

def status_bar() -> rx.Component:
    ""`Top status bar showing current mode, mission time, CPU, tubes.`""
    return rx.box(
        rx.hstack(
            # Left: Mode indicator
            rx.hstack(
                rx.text("MODE:", font_weight="bold", color="#00FFFF"),
                rx.text(
                    rx.cond(
                        FSQ7State.display_mode == "RADAR",
                        "RADAR SURVEILLANCE",
                        rx.cond(
                            FSQ7State.display_mode == "TACTICAL",
                            "TACTICAL SITUATION",
                            rx.cond(
                                FSQ7State.display_mode == "STATUS",
                                "SYSTEM STATUS",
                                "MEMORY VISUALIZATION"
                            )
                        )
                    ),
                    color="#FFFF00"
                ),
                spacing="2",
            ),
            
            # Center: Mission time
            rx.hstack(
                rx.text("MISSION:", font_weight="bold", color="#00FFFF"),
                rx.text(FSQ7State.mission_time, color="#00FF00", font_family="monospace"),
                spacing="2",
            ),
            
            # Right: Quick stats
            rx.hstack(
                rx.text(f"PC: {FSQ7State.cpu_program_counter_hex}", font_family="monospace", color="#FFFF00"),
                rx.text(f"A: {FSQ7State.cpu_accumulator_hex}", font_family="monospace", color="#FFFF00"),
                rx.text(f"TUBES: {FSQ7State.active_tubes}", color=rx.cond(FSQ7State.active_tubes > 57000, "#00FF00", "#FF8800")),
                rx.text(f"{FSQ7State.tube_temperature:.0f}°C", color=rx.cond(FSQ7State.tube_temperature > 250, "#00FF00", "#FFFF00")),
                spacing="3",
            ),
            
            justify_content="space-between",
            width="100%",
            padding="0.5em 1em",
        ),
        background="linear-gradient(to bottom, #1a1a2e, #0f0f1e)",
        border_bottom="2px solid #00FFFF",
        width="100%",
    )
```

### Add Scenario Selector to Control Panel

In `components/control_panel.py`, add:

```python
# Scenario selection
rx.vstack(
    rx.text("SCENARIO", size="2", weight="bold", color="#00FFFF"),
    rx.select(
        ["Demo 1 - Three Inbound", "Demo 2 - Mixed Friendly/Unknown", 
         "Demo 3 - High Threat Saturation", "Demo 4 - Patrol Route"],
        value=FSQ7State.selected_scenario,
        on_change=FSQ7State.load_scenario,
    ),
    spacing="1",
    width="100%",
),
```

---

## Testing

1. **Basic power on**: Tubes should warm up, system should become ready
2. **Radar display**: Targets should move across screen
3. **Light gun**: Click on radar target should select it (only in RADAR mode)
4. **Scenario loading**: Dropdown should spawn predefined targets
5. **Mode switching**: Display mode button should cycle through 4 modes
6. **Mission clock**: Should increment every second
7. **CPU execution**: Step/Run should work as before
8. **Status bar**: Should show current mode, time, CPU, tubes

---

## Benefits

- **Single simulation loop**: All state advances together
- **Testable**: Can test Simulator without UI
- **Extensible**: Easy to add drum storage, multi-console
- **Clear separation**: Simulation in `sim/`, presentation in `components/`
- **Scenario-driven**: Quick testing with predefined scenarios

---

*Integration guide created: 2025-11-10 15:23*
