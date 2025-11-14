# AN/FSQ-7 SAGE Computer Simulator

A fully interactive web-based simulator of the AN/FSQ-7 computer, the massive vacuum tube computer used in the SAGE (Semi-Automatic Ground Environment) air defense system during the Cold War era (1958-1983).

**🎮 NOW FULLY INTERACTIVE!** Experience Cold War air defense with working radar display, track visualization, authentic P7 phosphor CRT rendering, and hands-on vacuum tube maintenance.

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

### 💻 CPU Execution Trace
See programs run in real-time:
- **Step-by-step visualization**: Watch each instruction execute
- **Register display**: See A (Accumulator), I (Index), P (Program Counter), FLAGS update live
- **Speed controls**: Real-time, Slow (step-by-step), or Step (manual advance)
- **Final result banner**: Large display of computed result
- **Color-coded output**: Green for normal, yellow for results, cyan for values
- **Scrollable trace**: Review full execution history

### 🎨 Professional WebGL Radar Scope
Authentic phosphor screen experience:
- **Rotating sweep**: 4-second rotation with phosphor fade effect
- **Color-coded tracks**:
  - 🔴 Red: Hostile
  - 🟢 Green: Friendly  
  - 🟡 Yellow: Unknown
  - 🟣 Magenta: Missile
  - 🔵 Blue: Interceptor
- **Fading trails**: 20-point history showing flight paths
- **Glow effects**: Box-shadow halos around tracks, enhanced on selection
- **Geographic rendering**: Coastlines, cities, range rings with toggle control
- **Click detection**: Precise light gun target selection
- **Pan/Zoom**: Smooth controls for detailed inspection
- **60 FPS rendering**: Smooth Canvas 2D API performance

## Classic Features

### 🖥️ Authentic CRT Display
- Vintage phosphor glow effects with decay
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
- pip package manager

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

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Reflex app:**
   ```bash
   reflex init
   ```

3. **Run the simulator:**
   ```bash
   reflex run
   ```

4. **Open your browser:**
   Navigate to http://localhost:3000

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
- **Brightness slider**: Adjust phosphor intensity (20-100%)

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
├── an_fsq7_simulator.py       # Main application (original)
├── interactive_sage.py        # NEW: Interactive simulator main
├── cpu_core.py                # CPU execution engine
├── sage_programs.py           # Example programs
├── components/                # Original UI components
│   ├── crt_display.py
│   ├── control_panel.py
│   ├── cpu_panel.py
│   └── ...
├── components_v2/             # NEW: Interactive components
│   ├── state_model.py         # Core data structures
│   ├── scenarios.py           # Scenario generation & physics
│   ├── execution_trace_panel.py  # CPU trace visualization
│   ├── light_gun.py           # Light gun target selection
│   ├── sd_console.py          # Console controls
│   ├── geographic_overlays.py # Coastlines, cities, range rings
│   ├── tube_maintenance.py    # Tube maintenance mini-game
│   ├── tutorial_system.py     # Training missions
│   ├── radar_scope.py         # WebGL radar renderer
│   └── README.md              # Component documentation
└── docs/                       # Documentation
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    ├── HISTORY.md
    ├── INDEXED_ADDRESSING.md
    ├── INTEGRATION_GUIDE.md
    └── archive/               # Old implementation docs
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

Run the CPU execution tests:

```bash
# Test array sum example
cd an_fsq7_simulator
python -m cpu_core

# Run all examples
python -m sage_programs
```

Expected output:
```
✓ All indexed addressing examples working correctly!
  The AN/FSQ-7 CPU core properly implements:
    • effective_address = base_address + I
    • Index register (I) for loop counters
    • Indexed load: LDA base(I)
    • Indexed store: STO base(I)
    • Loop control: TIX (Transfer on Index)
```

## Technology Stack

- **Framework**: Reflex (Python → React web framework)
- **State Management**: Reflex State with real-time updates
- **UI Components**: Radix UI via Reflex
- **Styling**: CSS-in-Python with vintage CRT effects
- **Backend**: Python with async event handlers
- **Frontend**: React (auto-compiled by Reflex)
- **CPU Emulation**: Custom Python implementation
- **Rendering**: WebGL/Canvas 2D API for radar scope
- **Animation**: CSS @keyframes for tube states

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

Contributions welcome! Areas for enhancement:

**Interactive Features:**
- [ ] Multi-player support (multiple operator consoles)
- [ ] Historical mission scenarios (Cuban Missile Crisis, etc.)
- [ ] Authentic SAGE command language interpreter
- [ ] WebGL shader improvements for CRT effects
- [ ] Sound effects (tape drive, alarm bells, teleprinter)
- [ ] Mobile/touch-friendly light gun
- [ ] More scenario types (recon flights, transport, etc.)
- [ ] Weather effects on radar

**CPU Features:**
- [ ] More SAGE instruction opcodes
- [ ] Subroutine library
- [ ] Drum timing simulation
- [ ] More example programs

**System Features:**
- [ ] Additional display modes
- [ ] Network teletype simulation
- [ ] Alarm system with bells
- [ ] Printer output simulation

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick installation and first run guide
- **[DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)** - Planned features and development priorities
- **[docs/](docs/)** - Detailed technical and design documentation:
  - `DESIGN_NOTES` - Educational framework, personas, learning objectives
  - `VISUAL_REFERENCE.md` - P7 phosphor CRT design language
  - `RADAR_ARCHITECTURE.md` - Technical implementation details
  - `ARCHITECTURE.md` - System architecture overview
  - `HISTORY.md` - SAGE system historical context
  - `archive/` - Historical session notes and implementation details

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
