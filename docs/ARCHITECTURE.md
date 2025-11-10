# AN/FSQ-7 SAGE Simulator Architecture

## Overview

This document maps the current architecture of the AN/FSQ-7 SAGE simulator, showing the separation between simulation logic and UI presentation.

---

## 1. Entry Point

**File**: n_fsq7_simulator/an_fsq7_simulator.py

**App Configuration**:
- Reflex app with dark theme
- Single page application with `index()` as main layout
- On-load trigger: `FSQ7State.update_simulation` (background async task)

**Key Function**:
```python
def index() -> rx.Component:
    # Returns main layout with CRT display, controls, and SD console
```

---

## 2. Simulation Objects (Domain Model)

### Core Classes

| Class | File | Purpose |
|-------|------|---------|
| `RadarTarget` | `an_fsq7_simulator.py` | Represents tracked aircraft (x, y, heading, speed, altitude, threat_level) |
| `FSQ7CPU` | `cpu_core_authentic.py` | Authentic Q-7 CPU with 4 index regs, 2 memory banks, RTC (per Ulmann Ch.12) |
| `FSQ7Word` | `cpu_core_authentic.py` | 32-bit word with two 15-bit signed halves |
| `MemoryBanks` | `cpu_core_authentic.py` | Bank 1 (65K) + Bank 2 (4K) memory management |
| `IOHandler` | `cpu_core_authentic.py` | I/O mapped display routines |
| `SAGEProgramsAuthentic` | `sage_programs_authentic.py` | Real Q-7 programs with authentic encoding |

### State Management

**Class**: `FSQ7State(rx.State)`  
**File**: `an_fsq7_simulator.py`

Centralizes ALL simulation state:
- **System**: `power_on`, `system_ready`, `startup_progress`
- **Tubes**: `total_tubes`, `active_tubes`, `failed_tubes`, `tube_temperature`
- **Memory**: `memory_capacity_bank1/2`, `memory_used_bank1/2`, `memory_cycles`
- **CPU**: `cpu_accumulator`, `cpu_ix0..3`, `cpu_program_counter`, `cpu_rtc`, `cpu_halted`
- **Display**: `display_mode` (RADAR/TACTICAL/STATUS/MEMORY), `brightness`
- **Radar**: `radar_targets` (list), `tracked_objects`, `high_threat_count`
- **Controls**: `manual_override`, `intercept_mode`, `master_alarm`
- **Light Gun**: `light_gun_x`, `light_gun_y`, `selected_target`
- **Mission**: `mission_time`, `alerts_count`, `successful_intercepts`

**Private Instance**: `_cpu_core: Optional[FSQ7CPU]` - authentic CPU core

---

## 3. UI Components (Presentation Layer)

All components are **pure functions** that return `rx.Component` - they subscribe to `FSQ7State` but DO NOT contain simulation logic.

| Component | File | Displays | Interactive Elements |
|-----------|------|----------|---------------------|
| `crt_display()` | `components/crt_display.py` | Large circular CRT with mode-based overlays (radar, tactical, status, memory) | Light gun clicks |
| `control_panel()` | `components/control_panel.py` | Power, display mode, brightness, program selection, CPU controls | All buttons/sliders |
| `system_status()` | `components/system_status.py` | Tubes, temperature, memory, ready status | None (read-only) |
| `cpu_panel()` | `components/cpu_panel.py` | A, ix[0..3], PC, RTC, instruction count | Step/Run/Reset buttons |
| `memory_banks()` | `components/memory_banks.py` | Bank 1 (65K) and Bank 2 (4K) usage bars | None (read-only) |
| `radar_scope()` | `components/radar_scope.py` | Target list table with threat levels | None (read-only) |
| `sd_console()` | `components/sd_console.py` | SD console switches, feature/category selectors, telephone keys | All switches/buttons |

### Component Hierarchy

```
index()
├─ rx.box (main container)
│  ├─ rx.hstack (3-column layout)
│  │  ├─ LEFT: crt_display()
│  │  ├─ MIDDLE: memory_banks(), radar_scope()
│  │  └─ RIGHT: control_panel(), system_status(), cpu_panel()
│  └─ BOTTOM: sd_console() (full width)
```

---

## 4. Data Flow

### Current Pattern: **Centralized State, Scattered Updates**

```
UI Component           FSQ7State Method              Simulation Effect
────────────────────   ─────────────────────────────  ──────────────────────────
Button: "POWER ON"  →  power_on_system()          →  Starts startup_sequence()
                       startup_sequence()          →  Increments tubes, temp over 5s
                       
Button: "LOAD"      →  load_selected_program()    →  Calls cpu._get_cpu().load_program()
Button: "STEP"      →  cpu_step()                 →  Calls cpu.step(), syncs state
Button: "RUN"       →  cpu_run()                  →  Starts cpu_run_background() task

Toggle: Display     →  toggle_display_mode()      →  Cycles RADAR→TACTICAL→STATUS→MEMORY
Light Gun Click     →  light_gun_click(x, y)      →  Finds nearest radar target, sets selected_target

Background Loop     →  update_simulation()         →  Every 100ms: updates mission_time, 
                                                        moves radar targets, ticks RTC,
                                                        updates tube failures
```

### State Sync Pattern

1. **UI → State**: User clicks button → Reflex calls `FSQ7State.method()`
2. **State → CPU**: Method calls `self._get_cpu()` → operates on `FSQ7CPU` instance
3. **CPU → State**: Method calls `self.sync_cpu_state()` → copies CPU regs to `FSQ7State` vars
4. **State → UI**: Reflex auto-updates bound components when state vars change

---

## 5. Simulation Updates

### Where Updates Happen Today

| Update Type | Location | Method | Frequency |
|-------------|----------|--------|-----------|
| Tube warmup | `FSQ7State` | `startup_sequence()` | During startup (5s) |
| Tube failures | `FSQ7State` | `update_simulation()` | Every 100ms (random) |
| Radar movement | `FSQ7State` | `update_simulation()` | Every 100ms |
| Mission clock | `FSQ7State` | `update_simulation()` | Every 100ms |
| RTC ticking | `FSQ7State` | `tick_rtc()` called from `update_simulation()` | Every 31.25ms (32 Hz) |
| CPU execution | `FSQ7State` | `cpu_run_background()` (separate async task) | As fast as possible when running |
| CPU single step | `FSQ7State` | `cpu_step()` | On button click |

### Problems with Current Design

1. **Scattered timing logic**: Tubes, radar, RTC, CPU all updated in different places
2. **No unified tick**: `update_simulation()` runs at 100ms, RTC ticks at 31.25ms, CPU runs async
3. **No dt parameter**: Everything assumes fixed intervals
4. **Hard to test**: Can't easily inject scenarios or control time
5. **Hard to extend**: Adding drum storage or multi-console views requires editing multiple places

---

## 6. Console Modes

### Current Implementation

**State Variable**: `display_mode: str` with values: `"RADAR"`, `"TACTICAL"`, `"STATUS"`, `"MEMORY"`

**Mode Switching**: 
- User clicks "DISPLAY MODE" button
- Calls `FSQ7State.toggle_display_mode()`
- Cycles through 4 modes
- `crt_display()` component uses `rx.cond()` to show different overlays

### Issues

- No explicit "current mode" object with metadata
- Each overlay implemented separately in `crt_display.py`
- No unified control surface per mode
- Light gun selection works only in RADAR mode
- Status bar shows CPU regs but not current mode name

---

## 7. Interaction: Light Gun

**Current Implementation**:

1. User clicks on CRT display
2. `rx.box(on_click=FSQ7State.light_gun_click)` passes `(x, y)` coordinates
3. `light_gun_click()` iterates through `radar_targets`
4. Finds nearest target within 30px radius
5. Sets `self.selected_target = target["id"]`
6. Sets `self.light_gun_active = True`
7. UI shows yellow highlight around selected target

**Issues**:
- Selection logic mixed with UI event handler
- No "select" command to simulation model
- No validation that selection is within current mode
- `selected_target` is just an ID string, not a reference to `RadarTarget` object

---

## 8. Scenarios

**Current State**: No scenario system

Radar targets are generated manually via:
- `FSQ7State.generate_sample_targets()` creates 9 hardcoded targets
- Called from `startup_sequence()` after tubes warm up

**Issues**:
- No way to load different scenarios
- No way to spawn targets dynamically during mission
- Targets are static dicts, not `RadarTarget` objects
- No friendly/unknown/hostile classification system

---

## 9. Next Steps (Architecture Improvements)

Based on user requirements in task list:

1. **Create `sim/` package** with:
   - `sim/sim_loop.py` with `Simulator` class and `tick(dt)` method
   - `sim/models.py` with `RadarTarget`, `VacuumTubeBank`, `MissionClock`
   - `sim/scenarios.py` with scenario definitions

2. **Refactor `FSQ7State`** to:
   - Own a `Simulator` instance
   - Call `simulator.tick(dt)` from `update_simulation()`
   - Read simulation state instead of maintaining it
   - Only handle UI-specific state (selected target, display brightness)

3. **Add `ConsoleMode` enum** with:
   - Mode name, description, allowed actions
   - Per-mode control panels
   - Unified status bar

4. **Extract selection logic** to:
   - `Simulator.select_target(x, y, mode)` method
   - Return `Optional[RadarTarget]` object

5. **Add scenario loader** to:
   - `scenarios.py` with named scenarios
   - UI dropdown to select/load scenario
   - `Simulator.load_scenario(name)` method

---

## 10. File Structure Recommendation

Current:
```
an_fsq7_simulator/
├── an_fsq7_simulator.py     # State + entry point (535 lines - TOO BIG)
├── cpu_core_authentic.py    # CPU model ✓
├── sage_programs_authentic.py  # Programs ✓
└── components/              # UI components ✓
```

Proposed:
```
an_fsq7_simulator/
├── app.py                   # Entry point + Reflex config (50 lines)
├── state.py                 # FSQ7State (UI state only, 150 lines)
├── sim/
│   ├── __init__.py
│   ├── sim_loop.py         # Simulator class with tick()
│   ├── models.py           # RadarTarget, TubeBank, etc.
│   ├── scenarios.py        # Scenario definitions
│   └── modes.py            # ConsoleMode enum
├── cpu/
│   ├── __init__.py
│   ├── cpu_core.py         # FSQ7CPU
│   └── programs.py         # SAGEPrograms
└── components/              # UI components (unchanged)
```

This separates **simulation** (`sim/`), **computation** (`cpu/`), **presentation** (`components/`), and **coordination** (`state.py`).

---

*Document created: 2025-11-10 15:14*
*Status: Maps current architecture before refactoring*
