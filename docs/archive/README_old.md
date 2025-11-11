# AN/FSQ-7 SAGE Computer Simulator

A full-featured web-based simulator of the AN/FSQ-7 computer, the massive vacuum tube computer used in the SAGE (Semi-Automatic Ground Environment) air defense system during the Cold War era (1958-1983).


## About the AN/FSQ-7

The AN/FSQ-7 was:
- **The largest computer ever built** - Each installation weighed 250 tons and occupied 22,000 square feet
- **58,000 vacuum tubes** - Required constant maintenance and generated enormous heat
- **Magnetic core memory** - 64K words (incredibly advanced for its time)
- **Real-time processing** - Tracked hundreds of aircraft simultaneously
- **Light gun interface** - One of the first interactive graphical user interfaces
- **24 operator consoles** - Multiple operators could work simultaneously
- **$8 billion program** - Equivalent to over $100 billion in today's dollars

## Features

This simulator recreates the experience of operating an AN/FSQ-7 console with:

### 🖥️ Authentic CRT Display
- Vintage phosphor glow effects with decay
- Scan line overlay for period authenticity
- Multiple display modes (Radar, Tactical, Status, Memory)
- Adjustable brightness control
- Vignette and curvature effects
- Light gun interaction for target selection

### 🎯 **NEW: Functional CPU Core**
- **Indexed Addressing ** - `effective_addr = base + I`
- **Index Register (I)** - Critical for list processing and loops
- **Accumulator (A)** - Main computation register
- **Program Counter (P)** - Instruction pointer
- **Instruction Execution** - Step-by-step or full-speed execution
- **64K Word Memory** - Actual program storage and execution
- **10 Core Opcodes** - LDA, STO, ADD, SUB, MPY, DVH, TRA, TNZ, TIX, TSX

### 📜 Executable SAGE Programs
Run authentic SAGE programs that demonstrate indexed addressing:
- **Array Sum** - Sum array elements using indexed load
- **Array Search** - Find value in array using index register
- **Array Copy** - Copy data with indexed load and store
- **Matrix Initialization** - Fill 2D structures with indexed addressing

Each program can be:
- **Loaded** into memory with one click
- **Stepped** through instruction-by-instruction
- **Run** at full speed (100 Hz execution)
- **Reset** to initial state

### ⚡ Vacuum Tube System Simulation
- Real-time tube count and status monitoring
- Temperature simulation during warm-up
- Random tube failure simulation
- 58,000 tube management

### 💾 Magnetic Core Memory Visualization
- 64K word memory capacity
- Real-time memory usage tracking (reflects actual CPU memory)
- Memory cycle counter
- Visual memory bank status (16 banks)
- Drum storage indicators

### 📡 Radar Tracking
- Real-time target generation and movement
- Multiple target types (Aircraft, Missile, Friendly, Unknown)
- Threat level assessment (Low, Medium, High)
- Target selection via light gun
- Altitude, speed, and heading tracking
- Intercept course assignment

### 🎮 Control Panels
- **Power Control** - System startup with vacuum tube warm-up sequence
- **CPU Control Panel** (NEW) - Register display and program execution
  - View A (Accumulator), I (Index), P (Program Counter) in real-time
  - Load example programs
  - Step through instructions one at a time
  - Run programs at full speed
  - Reset CPU to initial state
- **Manual Override** - Take direct control of operations
- **Intercept Mode** - Enable weapons-free status
- **Display Mode Selection** - Switch between different views
- **Console Status** - Monitor active operator stations

### 📊 System Status Monitoring
- Tube health and temperature
- Memory utilization (actual CPU memory usage)
- Mission statistics
- Alert and intercept counts
- Real-time mission clock
- **CPU registers in status bar** - See A, I, P values at a glance

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
   Navigate to `http://localhost:3000`

## Usage

### Starting the System

1. **Power On:** Click the "POWER ON" button in the control panel
2. **Wait for Warm-up:** The vacuum tubes need time to reach operating temperature (simulated)
3. **System Ready:** When progress reaches 100%, the system is operational

### **NEW: Running SAGE Programs**

1. **Select a Program:** Choose from the dropdown in the CPU panel:
   - "Array Sum (Ch 12.5)" - Sum array elements
   - "Array Search (Ch 12.5)" - Find value in array
   - "Array Copy (Ch 12.5)" - Copy array data
   - "Matrix Init (Ch 12.5)" - Initialize 3x3 matrix

2. **Load Program:** Click "LOAD PROGRAM" to load into memory

3. **Execute:**
   - **STEP** - Execute one instruction at a time (watch registers change!)
   - **RUN** - Execute at full speed until halt
   - **RESET CPU** - Clear memory and reset to initial state

4. **Watch the Index Register (I):**
   - Highlighted in **cyan** in the CPU panel
   - Decrements as loops execute
   - Shows current position in array operations
   - **This is the key to understanding indexed addressing!**

### Operating the Radar Display

1. **Select Display Mode:** Use the buttons to switch between views:
   - **RADAR** - Primary radar scope with range rings
   - **TACTICAL** - Tactical situation display
   - **STATUS** - System health and diagnostics
   - **MEMORY** - Magnetic core memory visualization

2. **Light Gun Operation:**
   - Click on any target on the radar display to select it
   - Selected targets are highlighted in yellow
   - Target details appear in the radar tracking table

3. **Intercept Assignment:**
   - Enable "INTERCEPT MODE" in the control panel
   - Select a target using the light gun
   - Click "ASSIGN INTERCEPT" to dispatch an interceptor

### Display Controls

- **Brightness Slider:** Adjust CRT phosphor brightness (0-100%)
- **Display Mode Buttons:** Switch between operational views
- **Light Gun:** Click directly on the display to interact

## Technical Details

### Technology Stack

- **Framework:** Reflex (Python web framework)
- **State Management:** Reflex State with real-time updates
- **UI Components:** Radix UI via Reflex
- **Styling:** CSS-in-Python with vintage CRT effects
- **Backend:** Python with async event handlers
- **Frontend:** React (via Reflex compilation)
- **CPU Emulation:** Custom Python implementation with indexed addressing

### Architecture

```
an_fsq7_simulator/
├── an_fsq7_simulator.py       # Main application and state management
├── cpu_core.py                # CPU execution engine (NEW!)
├── sage_programs.py           # Example programs (NEW!)
├── components/
│   ├── crt_display.py         # CRT display with effects
│   ├── control_panel.py       # Control surfaces and switches
│   ├── cpu_panel.py           # CPU register display (NEW!)
│   ├── system_status.py       # System health monitoring
│   ├── memory_banks.py        # Memory visualization
│   └── radar_scope.py         # Radar tracking display
└── .web/                       # Compiled frontend (auto-generated)
```

### Instruction Set Summary

The simulator implements these core AN/FSQ-7 instructions:

| Opcode | Mnemonic | Description | Indexed? |
|--------|----------|-------------|----------|
| 0x01 | LDA | Load Accumulator | Yes |
| 0x02 | STO | Store Accumulator | Yes |
| 0x03 | ADD | Add to Accumulator | Yes |
| 0x04 | SUB | Subtract from Accumulator | Yes |
| 0x05 | MPY | Multiply | Yes |
| 0x06 | DVH | Divide (high quotient) | Yes |
| 0x10 | TRA | Transfer (unconditional jump) | No |
| 0x11 | TNZ | Transfer if Non-Zero | No |
| 0x12 | TMI | Transfer if Minus | No |
| 0x13 | TSX | Transfer and Set Index | No |
| 0x14 | TIX | Transfer on Index (loop control) | No |
| 0xFF | HLT | Halt execution | No |

**All memory access instructions support indexed addressing via the Index Register (I).**

### Indexed Addressing Example

```assembly
; Sum array[0..9]
    LDA  ZERO       ; A ← 0
    LDA  TEN        ; I ← 10
LOOP:
    ADD  ARRAY(I)   ; A ← A + memory[ARRAY + I]  <-- indexed!
    TIX  LOOP       ; I ← I-1; if I>0 goto LOOP
    HLT
```

See **[docs/INDEXED_ADDRESSING.md](docs/INDEXED_ADDRESSING.md)** for complete details on implementation.

## Testing CPU Execution

Run the included test programs:

```bash
# Test single array sum example
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

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - 5-minute getting started guide
- **[Project Summary](PROJECT_SUMMARY.md)** - Executive overview and features
- **[Design Document](docs/DESIGN.md)** - Technical architecture and decisions
- **[Historical Context](docs/HISTORY.md)** - AN/FSQ-7 and SAGE history
- **[Implementation Thoughts](docs/THOUGHTS.md)** - Development considerations
- **[Indexed Addressing](docs/INDEXED_ADDRESSING.md)** - ⚡ NEW: implementation details

## Historical Context

The Semi-Automatic Ground Environment (SAGE) was:
- **Purpose:** Continental air defense against Soviet bomber threat
- **Deployment:** 1958-1983 (25 years of operation)
- **Scope:** 24 direction centers across North America
- **Cost:** $8 billion ($100+ billion in 2025 dollars)
- **Legacy:** Pioneered many computer concepts still used today

### Innovations Introduced by SAGE

1. **Real-time computing** - Processing data as it arrived
2. **Interactive graphics** - Light gun pointing at display
3. **Networking** - Computers connected via phone lines
4. **Distributed computing** - Multiple sites working together
5. **Modular software** - Programs could be updated independently
6. **Human-computer interaction** - Operators directly controlling systems
7. **Indexed addressing** - Loop processing and data structures

## Contributing

Contributions are welcome! Areas for enhancement:

- [ ] More SAGE instruction opcodes 
- [ ] Drum timing simulation - realistic memory latency
- [ ] More realistic radar simulation algorithms
- [ ] Additional display modes and visualizations
- [ ] Sound effects (tape drive, alarm bells, teleprinter)
- [ ] Historical mission scenarios
- [ ] Multiplayer support (multiple operator consoles)
- [ ] Mobile/touch-friendly interface
- [ ] WebGL shader improvements for CRT effects
- [ ] Authentic SAGE command language interpreter
- [ ] Subroutine library

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by the thousands of engineers, operators, and maintainers who worked on SAGE
- Thanks to the Computer History Museum for preserving SAGE documentation
- Built with [Reflex](https://reflex.dev) - Python web framework
- CRT effects inspired by vintage computing enthusiasts
- CPU implementation follows SAGE Programming Manual

---

**Note:** This is a simulation for educational and entertainment purposes. It does not represent classified military systems or current air defense technology.

---

**"The SAGE system was the most ambitious computing project of its era, and in many ways, it defined what we now take for granted in modern computing."**

*Press POWER ON to begin your journey back to the dawn of interactive computing.*

*Then load a program and watch the Index Register (I) work its magic! ⚡*

