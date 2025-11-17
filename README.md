# AN/FSQ-7 SAGE Computer Simulator

A fully interactive web-based simulator of the AN/FSQ-7 computer, the massive vacuum tube computer used in the SAGE (Semi-Automatic Ground Environment) air defense system during the Cold War era (1958-1983).

**🎮 NOW FULLY INTERACTIVE!** Experience Cold War air defense as a **SAGE Direction Center operator**, with authentic P14 phosphor CRT display, working light gun, and hands-on vacuum tube maintenance.

## Your Role: Direction Center Operator

You are operating a **SAGE Direction Center (DC) situation display console**. The DC aggregates radar data from 28 stations across North America (DEW Line, Mid-Canada Line, Pinetree Line, Gap-Fillers, Ground Control Intercept sites) and coordinates continental air defense responses. Think of it as the "command center" receiving real-time feeds from multiple radar installations.

## About the AN/FSQ-7

The AN/FSQ-7 was:
- **The largest computer ever built** - Each installation weighed 250 tons and occupied 22,000 square feet
- **58,000 vacuum tubes** - Required constant maintenance and generated enormous heat
- **Magnetic core memory** - 64K words (incredibly advanced for its time)
- **Real-time processing** - Tracked hundreds of aircraft simultaneously
- **Light gun interface** - One of the first interactive graphical user interfaces
- **24 operator consoles** - Multiple operators could work simultaneously
- **$8 billion program** - Equivalent to over $100 billion in today's dollars

## 🆕 Interactive Features (NEW!)

> **⚠️ NOTICE - Historical Accuracy Update Coming:** Based on official AN/FSQ-7 technical manuals, we've discovered the track display format needs major corrections. SAGE used **character-based tabular displays** with alphanumeric text (not geometric shapes). This will be implemented in a future update. See `docs/SAGE_DISPLAY_CORRECTIONS_REQUIRED.md` for details.

### 🎯 Working Light Gun System
- **Press 'D' key** to arm the light gun → crosshair appears
- **Click any target** on radar scope → highlight yellow and populate Track Detail panel
- **View complete target info**: ID, type, altitude, speed, heading, threat level, position, velocity
- **Launch interceptors**: Click "LAUNCH INTERCEPT" button for hostile targets
- **Press ESC** to clear selection

### 🎛️ Functional SD Console
18 working control buttons with visual feedback:
- **Category Filters (S1-S13)**: ALL, FRIENDLY, UNKNOWN, HOSTILE, MISSILE, BOMBER, FIGHTER, altitude filters (LOW/MED/HIGH), INBOUND, OUTBOUND, LOITERING
- **Feature Overlays (S20-S24)**: FLIGHT PATHS, INTERCEPTS, RANGE RINGS, CALLSIGNS, COASTLINES
- **Scope Controls**: Pan (↑↓←→), Center (⊙), Zoom (−/+/FIT), Rotate (↶/↷/N)
- **Brightness Control**: Slider with presets (DIM 40% / MED 70% / BRIGHT 100%)
- **Active Status Display**: Badges showing current filters and overlays

### 📡 Realistic Radar Scenarios
Physics-based target generation:
- **Bomber Streams**: Formations of 3-5 bombers from Arctic, 35-45K ft, 450-600 kts, heading toward NYC
- **Missile Launches**: ICBM trajectories, 60K+ ft, 800+ kts, with countdown timers (T-minus)
- **CAP Patrols**: Friendly racetrack patterns, 20-30K ft, 300-400 kts
- **Interceptors**: Launch from base with seek/pursue AI toward hostile targets
- **Smooth Physics**: Velocity-based movement, intercept radius detection, realistic flight patterns

### 🗺️ Geographic Context
Navigate with real geography:
- **East Coast**: Detailed coastline from Maine → Virginia (18 waypoints)
- **Great Lakes**: Superior, Michigan, Huron, Erie, Ontario
- **Canadian Border**: Dashed boundary line
- **Major Cities**: BOS, NYC, PHL, DC, CHI, CLE, BUF, DET with coordinates
- **Range Rings**: 100mi, 200mi, 300mi radii from center
- **Bearing Markers**: N/E/S/W directional indicators
- **Sector Boundaries**: Dotted lines dividing airspace

### 🔧 Vacuum Tube Maintenance Mini-Game
Hands-on system maintenance:
- **8×8 Grid**: 64 vacuum tubes with real-time status monitoring
- **Tube States**: ▓ OK (green), ▒ Degrading (yellow), ✗ Failed (red), ◌ Warming Up (cyan)
- **Interactive Replacement**: Click failed tube → 4-step procedure (power down → pull → insert → warm up)
- **Performance Impact**: Failed tubes reduce system tick rate and cause scope flicker
- **Visual Animations**: CSS effects for blinking (failed), pulsing (degrading), glowing (warming)
- **Statistics Dashboard**: Count operational/degrading/failed tubes with performance gauge

### 🎓 Tutorial System
Learn through 6 guided training missions:
1. **Power-On & Scope Basics** (4 steps) - Toggle overlays and familiarize with display
2. **Target Selection** (3 steps) - Learn light gun operation
3. **Launch Intercept** (4 steps) - Engage hostile targets
4. **Console Filters** (4 steps) - Master SD Console controls
5. **Tube Maintenance** (4 steps) - Replace failed vacuum tubes
6. **CPU Program Execution** (4 steps) - Load and run SAGE programs

Each mission includes:
- Step-by-step instructions with hints
- Automatic progress checking
- Visual progress indicators (✓ complete, → current, # pending)
- Reward messages on completion
- Welcome modal on first visit (Start Training / Skip)

### 🎯 Track Correlation & Classification System
Realistic detect → correlate → classify workflow:
- **Track States**: UNCORRELATED → CORRELATING → CORRELATED
- **Confidence Levels**: LOW/MED/HIGH based on radar returns and IFF signals
- **Manual Override**: Use light gun to correlate ambiguous tracks
- **Classification Panel**: Mark tracks as Hostile / Friendly / Unknown / Ignore
- **Track History**: View lifecycle progression and correlation decisions
- **Visual Feedback**: Different shapes/colors per state on radar scope

### ✈️ Interceptor Assignment System
Tactical aircraft management with real consequences:
- **3 Aircraft Types**: F-106 Delta Dart, F-102 Delta Dagger, F-89 Scorpion
- **Detailed Status**: View fuel levels, weapon loads (AIM-4 Falcon, MB-1 Genie), base location
- **Smart Suggestions**: System recommends best interceptor for selected target
- **State Tracking**: READY → REFUELING → SCRAMBLING → AIRBORNE → ENGAGING → RETURNING
- **Intercept Vectors**: Blue dashed lines show flight path on radar
- **Engagement Outcomes**: SPLASH ONE (success) vs MISS (failure) with feedback

### 🔍 System Inspector (Advanced)
Deep-dive system transparency for students and enthusiasts (press **Shift+I**):
- **Drum Fields**: View magnetic drum storage with status bits (LRI, GFI, XTL, SDC)
- **CPU State**: Real-time accumulator, index register, program counter, flags
- **Queue Inspector**: See processing bottlenecks and data flow
- **Status Channels**: Monitor asynchronous I/O polling (OD_LRI, CD_LRI, LIGHT_GUN)
- **Educational Value**: Understand SAGE's drum-buffered I/O and polling architecture

### 📊 Scenario Debrief System
Performance assessment and learning feedback:
- **7 Training Scenarios**: Beginner → Expert difficulty progression
- **Performance Metrics**: Detection %, classification accuracy, intercept success rate
- **Letter Grades**: A-F scoring with detailed breakdown
- **Learning Moments**: Mistakes highlighted with severity icons and improvement tips
- **Mission Objectives**: Checklist showing completion status
- **Action Options**: Continue, Replay Scenario, Next Scenario

### 🔊 Sound Effects & Audio Feedback
Authentic Cold War era audio ambiance:
- **25+ Sound Library**: Radar sweep, light gun clicks, tube replacements, alarm bells, intercepts
- **3 Volume Channels**: Ambiance, UI interactions, alerts (independent control)
- **4 Audio Presets**: Silent, Minimal, Balanced, Full Immersion
- **Real-time Feedback**: Audio cues for target selection, intercept launches, system events
- **Historical Accuracy**: Vintage equipment sounds sourced from period recordings

### 🗺️ Network & Station View
Strategic air defense network visualization:
- **28 SAGE Stations**: Direction Centers, Combat Centers, NORAD HQ
- **5 Station Types**: Different icons for DC, CC, NORAD, Early Warning, Gap Filler
- **Coverage Circles**: Visual representation of radar range
- **Network Connectivity**: Cross-tell communication links between stations
- **Legend Panel**: Station type reference with toggle controls
- **Geographic Accuracy**: Stations placed at historical locations across North America

### 💻 CPU Execution Trace
See programs run in real-time:
- **Step-by-step visualization**: Watch each instruction execute
- **Register display**: See A (Accumulator), I (Index), P (Program Counter), FLAGS update live
- **Speed controls**: Real-time, Slow (step-by-step), or Step (manual advance)
- **Final result banner**: Large display of computed result
- **Color-coded output**: Green for normal, yellow for results, cyan for values
- **Scrollable trace**: Review full execution history

### 🔍 System Inspector (Advanced)
For deep-dive system transparency (press **Shift+I** to toggle):
- **Drum Fields**: View magnetic drum storage with status bits (LRI, GFI, XTL, SDC)
- **CPU State**: Real-time accumulator, index register, program counter, and flags
- **Queue Inspector**: See processing bottlenecks and data flow
- **Status Channels**: Monitor asynchronous I/O polling (OD_LRI, CD_LRI, LIGHT_GUN)
- **Educational Value**: Understand SAGE's drum-buffered I/O and polling architecture
- Designed for CS students (Ada persona) exploring system architecture

### 🎨 Authentic P14 Phosphor Situation Display
Faithful simulation of the SAGE 19" situation display console:
- **P14 Phosphor CRT** (historically accurate): Purple flash → orange afterglow (2-3 second persistence)
- **Monochrome Symbology**: Track types differentiated by **symbol shapes**, not colors
  - ⬤ Circle: Friendly aircraft
  - ⬛ Square: Hostile aircraft (bombers, fighters)
  - ◆ Diamond: Unknown tracks
  - ▲ Triangle: Missiles
  - Dashed outlines: Uncorrelated tracks (with "?" indicator)
- **Blue Room Environment**: Dim blue ambient lighting (simulates indirect lighting to prevent phosphor glare)
- **2.5-Second Refresh Cycle**: Computer updates display drum every 2.5 seconds (historically accurate)
  - Phosphor persistence decays continuously at 60fps between refreshes
  - Simulates SAGE's computer-driven display update timing
  - Tracks remain visible via P14 orange afterglow between updates
- **Computer-Driven Display**: Tracks rendered with authentic monochrome vector symbology
- **Phosphor Persistence**: ~2.5 second orange afterglow matches SAGE 2.5s display refresh cycles
- **Geographic Overlays**: Coastlines, range rings, cities (vector rendering)
- **Light Gun Target Selection**: Precise click detection on symbol shapes
- **Pan/Zoom Controls**: Smooth view manipulation for detailed inspection
- **60 FPS Persistence Decay**: Canvas 2D API with dual-layer phosphor simulation

## Under the Hood: SAGE's Unusual Architecture

The AN/FSQ-7 was fundamentally different from modern computers. This simulator models several of SAGE's unusual architectural features:

### One's Complement Arithmetic
- **Not two's complement**: Uses one's complement binary representation (two zeros: +0 and -0)
- **Fractional values**: Numbers represented as fractions between -1.0 and +1.0
- **Parallel processing**: Each 32-bit word contains TWO 16-bit values processed simultaneously
- **Implicit shift quirk**: Addition automatically shifts right by one bit (programmers had to pre-compensate!)

### Drum-Buffered I/O
- **No direct I/O**: CPU never talks directly to radar, consoles, or other sites
- **Magnetic drum intermediary**: All external data written to dedicated drum fields (LRI for radar, GFI for ground radar, XTL for cross-tell)
- **Status channel polling**: CPU continuously polls status bits to detect when new data arrives
- **Asynchronous operation**: Input systems write to drum independently while CPU runs

### Light Gun Polling
- **Not mouse coordinates**: Light gun used a photomultiplier tube that detected the CRT electron beam
- **Sequential detection**: CPU draws each target, then polls a flip-flop bit to see if the gun "flashed"
- **Timing-based**: Selected target identified by which draw operation triggered the photomultiplier
- **Polling required**: CPU must check status after EVERY draw operation

These architectural quirks made SAGE programming challenging but enabled real-time operation with 1950s technology. For technical details, see [`docs/HIGH_FIDELITY_EMULATION.md`](docs/HIGH_FIDELITY_EMULATION.md).

## Classic Features

### 🖥️ Long-Persistence CRT Display (P7-Style)
- Vintage phosphor glow effects with decay (rendered in green for readability)
- Scan line overlay for period authenticity
- Multiple display modes (Radar, Tactical, Status, Memory)
- Adjustable brightness control (0-100%)
- Vignette and curvature effects

### 🎯 Functional CPU Core
- **Indexed Addressing**: ffective_addr = base + I
- **Index Register (I)**: Critical for list processing and loops
- **Accumulator (A)**: Main computation register
- **Program Counter (P)**: Instruction pointer
- **64K Word Memory**: Actual program storage and execution
- **10 Core Opcodes**: LDA, STO, ADD, SUB, MPY, DVH, TRA, TNZ, TIX, TSX

### 📜 Executable SAGE Programs
Run authentic programs demonstrating indexed addressing:
- **Array Sum** - Sum array elements using indexed load
- **Array Search** - Find value in array using index register
- **Array Copy** - Copy data with indexed load and store
- **Matrix Initialization** - Fill 2D structures with indexed addressing

### ⚡ Vacuum Tube System Simulation
- Real-time tube count and status monitoring
- Temperature simulation during warm-up
- Random tube failure simulation
- 58,000 tube management

### 💾 Magnetic Core Memory Visualization
- 64K word memory capacity
- Real-time memory usage tracking
- Memory cycle counter
- Visual memory bank status (16 banks)

## Installation

### Prerequisites
- Python 3.8 or higher
- **UV package manager** (automatically handles dependencies)

### Quick Start

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Run the simulator:**
   ```powershell
   # Windows PowerShell
   uv run reflex run
   
   # Linux/Mac
   uv run reflex run
   ```

3. **Open your browser:**
   Navigate to http://localhost:3000

**Note:** This project uses `uv` for package management. All commands must be prefixed with `uv run` (e.g., `uv run python script.py`, `uv run reflex run`).

## Usage Guide

### 🚀 First Time? Start Here!

1. **Power On**: Click "POWER ON" button → watch vacuum tubes warm up
2. **Welcome Modal**: Choose "Start Training" for guided tutorial or "Skip" to explore
3. **Follow Mission 1**: Learn scope basics and overlay controls

### 🎯 Using the Light Gun (Most Fun!)

1. **Arm**: Press **D** key → crosshair appears over scope
2. **Select**: Click any radar target → highlights yellow
3. **View Details**: Track Detail panel populates on right side:
   - Track ID and type
   - Altitude, speed, heading
   - Position (x, y) and velocity (vx, vy)
   - Threat level assessment
   - Missile countdown timer (if applicable)
4. **Intercept**: Click "LAUNCH INTERCEPT" for hostile/missile targets
5. **Clear**: Press **ESC** to deselect

### 🎛️ Operating the SD Console

**Filter Tracks (S1-S13 buttons):**
- S1: ALL - Show all tracks
- S2: FRIENDLY - Friendly aircraft only
- S3: UNKNOWN - Unidentified targets
- S4: HOSTILE - Enemy aircraft
- S5: MISSILE - ICBM launches
- S6: BOMBER - Bomber aircraft
- S7: FIGHTER - Fighter aircraft
- S8: ALT<10K - Low altitude (<10,000 ft)
- S9: ALT 10K-30K - Medium altitude
- S10: ALT>30K - High altitude (>30,000 ft)
- S11: INBOUND - Approaching targets
- S12: OUTBOUND - Departing targets
- S13: LOITERING - Stationary/circling

**Toggle Overlays (S20-S24 buttons):**
- S20: FLIGHT PATHS - Show fading trails
- S21: INTERCEPTS - Show intercept vectors (blue dashed lines)
- S22: RANGE RINGS - 100mi/200mi/300mi circles
- S23: CALLSIGNS - Display track IDs and city names
- S24: COASTLINES - Show East Coast, Great Lakes, borders

**Scope Controls:**
- **Arrow buttons** (↑↓←→): Pan view
- **Center** (⊙): Reset to center
- **Zoom** (−/+): Zoom out/in
- **FIT**: Reset zoom to 1.0
- **Rotate** (↶/↷): Rotate view (clockwise/counter-clockwise)
- **N**: Reset rotation to North-up
- **Brightness slider**: Adjust display intensity (20-100%)

### 🔧 Maintaining Vacuum Tubes

Tubes degrade over time and affect system performance:

1. **Monitor Status**: Watch 8×8 grid for color changes:
   - ▓ Green (OK): Tube healthy
   - ▒ Yellow (Degrading): Tube weakening (pulsing animation)
   - ✗ Red (Failed): Tube dead (blinking animation)
   - ◌ Cyan (Warming): New tube heating up (glowing animation)

2. **Performance Gauge**: Shows system health (OPTIMAL → CRITICAL)
   - Failed tubes reduce tick rate and cause scope flicker

3. **Replace Failed Tubes**:
   - Click on failed tube (red ✗)
   - Follow 4-step procedure in modal:
     1. Power down affected section
     2. Pull failed tube from socket
     3. Insert new tube
     4. Wait 5 seconds for warmup
   - Tube turns green (▓) → performance restored!

4. **Statistics**: View counts of operational/degrading/failed tubes

### 💻 Running CPU Programs

1. **Select Program**: Choose from dropdown in CPU panel
2. **Load**: Click "LOAD PROGRAM" → loads into memory
3. **Execute**:
   - **STEP**: Execute one instruction (watch registers!)
   - **RUN**: Full-speed execution until halt
   - **RESET CPU**: Clear and start over
4. **Watch Execution Trace**:
   - See each instruction execute
   - Register values update in real-time
   - Final result displayed in banner
5. **Index Register (I)**: Highlighted in cyan, shows loop progress

### 📡 Understanding Radar Scenarios

The system spawns realistic scenarios automatically:

- **Bomber Streams**: Formation flying from Arctic → NYC
  - Watch multiple targets maintain formation
  - High altitude (35-45K ft)
  - Moderate speed (450-600 kts)
  
- **Missile Launches**: ICBM trajectories with countdown
  - Extremely high altitude (60K+ ft)
  - Very high speed (800+ kts)
  - T-minus countdown timer visible in Track Detail
  
- **CAP Patrols**: Friendly racetrack patterns
  - Medium altitude (20-30K ft)
  - Loitering behavior
  
- **Interceptors**: Auto-launched toward hostiles
  - Blue tracks with dashed intercept vectors
  - Homing behavior toward targets

## Architecture

```
an_fsq7_simulator/
├── interactive_sage.py        # Main interactive simulator state and handlers
├── state_model.py             # Reflex-compatible data structures
├── cpu_core.py                # CPU execution engine (one's complement arithmetic)
├── drum_io_system.py          # Drum-buffered I/O simulation
├── sage_programs.py           # Example SAGE programs
├── scenarios.py               # Legacy scenario definitions
├── components/                # Original UI components (v1)
│   ├── crt_display.py
│   ├── control_panel.py
│   ├── cpu_panel.py
│   └── ...
├── components_v2/             # Current interactive components
│   ├── execution_trace_panel.py   # CPU trace visualization
│   ├── geographic_overlays.py     # Coastlines, cities, range rings
│   ├── light_gun.py               # Light gun target selection
│   ├── operator_workflow.py       # Track correlation & classification
│   ├── radar_scope.py             # Vector CRT radar renderer
│   ├── safe_actions.py            # Interceptor assignment panel
│   ├── scenarios_layered.py       # Scenario debrief system
│   ├── sd_console.py              # Console controls (filters, overlays)
│   ├── sound_effects.py           # Audio system with volume controls
│   ├── system_messages.py         # Network & station view
│   ├── track_lifecycle.py         # Track state visualization
│   ├── tube_maintenance.py        # Vacuum tube mini-game
│   ├── tutorial_system.py         # Training missions
│   └── README.md                  # Component documentation
├── sim/                       # Simulation engine
│   ├── models.py              # Core domain models (Track, Interceptor, Tube, etc.)
│   ├── scenarios.py           # Scenario definitions with learning objectives
│   ├── sim_loop.py            # Physics and state updates
│   └── modes.py               # Display modes and filters
└── docs/                       # Comprehensive documentation
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    ├── FIDELITY_SUMMARY.md
    ├── HIGH_FIDELITY_EMULATION.md
    ├── HISTORY.md
    ├── INDEXED_ADDRESSING.md
    ├── INTEGRATION_GUIDE.md
    ├── SOUND_EFFECTS_GUIDE.md
    ├── UI_DESIGN_PATTERNS.md
    └── archive/               # Historical implementation docs
```

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - 5-minute getting started
- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[Design Document](docs/DESIGN.md)** - Technical decisions
- **[Historical Context](docs/HISTORY.md)** - AN/FSQ-7 and SAGE history
- **[Indexed Addressing](docs/INDEXED_ADDRESSING.md)** - CPU implementation details
- **[Integration Guide](docs/INTEGRATION_GUIDE.md)** - Component wiring
- **[Interactive Components](an_fsq7_simulator/components_v2/README.md)** - NEW component docs
- **[Fidelity Summary](docs/FIDELITY_SUMMARY.md)** - Historical accuracy notes

## Testing

Run tests using UV package manager:

```powershell
# Core unit tests (CPU, drum, light gun)
uv run pytest tests/unit

# Simulation tests (scenarios, physics)
uv run pytest tests/sim

# Design language / UI contract tests
uv run pytest tests/design_language

# Property-based tests (optional)
uv run pytest tests/property_based

# Test imports
uv run python -c "import an_fsq7_simulator.interactive_sage; print('✓ Imports OK')"
```

**Manual Testing:**
1. Start server: `uv run reflex run`
2. Open http://localhost:3000
3. Verify features work:
   - Track rendering and movement
   - Light gun selection (press D, click target)
   - Interceptor assignment panel
   - System Inspector (Shift+I)
   - Scenario debrief after mission
   - Sound effects (check volume controls)
   - Network view toggle

## Technology Stack

- **Framework**: Reflex 0.8.19 (Python → React web framework)
- **Package Manager**: UV (fast Python package and project manager)
- **State Management**: Reflex State with real-time WebSocket updates
- **UI Components**: Radix UI via Reflex
- **Styling**: CSS-in-Python with vintage CRT effects (P14 phosphor simulation)
- **Backend**: Python 3.8+ with async event handlers
- **Frontend**: React (auto-compiled by Reflex)
- **CPU Emulation**: Custom one's complement arithmetic with indexed addressing
- **I/O Architecture**: Drum-buffered asynchronous I/O with status channel polling
- **Rendering**: Canvas 2D API for vector CRT radar scope
- **Animation**: CSS @keyframes for tube states, phosphor decay, scan lines
- **Audio**: HTML5 Audio API with multi-channel mixing
- **Testing**: pytest for unit, simulation, and design language tests

## Historical Context

The Semi-Automatic Ground Environment (SAGE) was:
- **Purpose**: Continental air defense against Soviet bomber threat
- **Deployment**: 1958-1983 (25 years of operation)
- **Scope**: 24 direction centers across North America
- **Cost**: $8 billion ($100+ billion in 2025 dollars)
- **Legacy**: Pioneered many computer concepts still used today

### Innovations Introduced by SAGE

1. **Real-time computing** - Processing data as it arrived
2. **Interactive graphics** - Light gun pointing at display
3. **Networking** - Computers connected via phone lines
4. **Distributed computing** - Multiple sites working together
5. **Modular software** - Programs could be updated independently
6. **Human-computer interaction** - Operators directly controlling systems
7. **Indexed addressing** - Loop processing and data structures

## Contributing

Contributions welcome! Current system is production-ready with all 6 development priorities complete. Areas for future enhancement:

**Interactive Features:**
- [ ] Multi-player support (multiple operator consoles)
- [ ] Historical mission scenarios (Cuban Missile Crisis, Berlin Airlift, etc.)
- [ ] Authentic SAGE command language interpreter
- [ ] WebGL shader improvements for CRT phosphor effects
- [ ] Mobile/touch-friendly light gun (touch events)
- [ ] More scenario types (recon flights, transport, tankers, etc.)
- [ ] Weather effects on radar (rain clutter, storm cells)
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)

**CPU Features:**
- [ ] Complete SAGE instruction set (all 50+ opcodes)
- [ ] Subroutine library (authentic SAGE system programs)
- [ ] Drum timing simulation (rotational latency)
- [ ] More example programs (weapon control, data link)
- [ ] Assembly language syntax support

**System Features:**
- [ ] Network teletype simulation (cross-tell messages)
- [ ] Alarm system with authentic bell sounds
- [ ] Printer output simulation (status reports)
- [ ] Accessibility improvements (keyboard navigation, screen readers)
- [ ] Create actual pytest tests for design language invariants
- [ ] Property-based testing for numerical correctness

**Documentation:**
- [ ] Video tutorials for each training mission
- [ ] Interactive architecture diagrams
- [ ] Historical photo gallery with comparisons

## Documentation

**Getting Started:**
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributor guide with testing & PR guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current development status

**For Developers:**
- **[agents.md](agents.md)** - Development patterns, design invariants, common gotchas
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and data flow
- **[docs/DESIGN.md](docs/DESIGN.md)** - Design philosophy and technical decisions
- **[docs/HIGH_FIDELITY_EMULATION.md](docs/HIGH_FIDELITY_EMULATION.md)** - SAGE technical implementation details
- **[docs/INDEXED_ADDRESSING.md](docs/INDEXED_ADDRESSING.md)** - CPU architecture and instruction set
- **[an_fsq7_simulator/components_v2/README.md](an_fsq7_simulator/components_v2/README.md)** - Component API reference

**For Users:**
- **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** - Comprehensive user manual
- **[docs/SOUND_EFFECTS_GUIDE.md](docs/SOUND_EFFECTS_GUIDE.md)** - Audio system reference
- **[docs/UI_DESIGN_PATTERNS.md](docs/UI_DESIGN_PATTERNS.md)** - Design language and patterns

**Historical Context:**
- **[docs/HISTORY.md](docs/HISTORY.md)** - AN/FSQ-7 and SAGE system history
- **[docs/FIDELITY_SUMMARY.md](docs/FIDELITY_SUMMARY.md)** - Historical accuracy notes
- **[docs/archive/](docs/archive/)** - Completed session reports and historical notes

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by thousands who worked on SAGE (engineers, operators, maintainers)
- Thanks to Computer History Museum for preserving SAGE documentation
- Built with [Reflex](https://reflex.dev) - Python web framework
- CRT effects inspired by vintage computing enthusiasts
- CPU implementation follows SAGE Programming Manual Chapter 12

---

**Note:** This is a simulation for educational and entertainment purposes. It does not represent classified military systems or current air defense technology.

---

**"The SAGE system was the most ambitious computing project of its era, and in many ways, it defined what we now take for granted in modern computing."**

*Press POWER ON to begin your journey back to the dawn of interactive computing.*

*Then press 'D', click a target, and watch the magic happen! 🎯✨*
