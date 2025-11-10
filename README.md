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
- **Manual Override** - Take direct control of operations
- **Intercept Mode** - Enable weapons-free status
- **Display Mode Selection** - Switch between different views
- **Console Status** - Monitor active operator stations

### 📊 System Status Monitoring
- Tube health and temperature
- Memory utilization
- Mission statistics
- Alert and intercept counts
- Real-time mission clock

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

### Architecture

```
an_fsq7_simulator/
├── an_fsq7_simulator.py       # Main application and state management
├── components/
│   ├── crt_display.py         # CRT display with effects
│   ├── control_panel.py       # Control surfaces and switches
│   ├── system_status.py       # System health monitoring
│   ├── memory_banks.py        # Memory visualization
│   └── radar_scope.py         # Radar tracking display
└── .web/                       # Compiled frontend (auto-generated)
```

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - 5-minute getting started guide
- **[Project Summary](PROJECT_SUMMARY.md)** - Executive overview and features
- **[Design Document](docs/DESIGN.md)** - Technical architecture and decisions
- **[Historical Context](docs/HISTORY.md)** - AN/FSQ-7 and SAGE history
- **[Implementation Thoughts](docs/THOUGHTS.md)** - Development considerations

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

## Contributing

Contributions are welcome! Areas for enhancement:

- [ ] More realistic radar simulation algorithms
- [ ] Additional display modes and visualizations
- [ ] Sound effects (tape drive, alarm bells, teleprinter)
- [ ] Historical mission scenarios
- [ ] Multiplayer support (multiple operator consoles)
- [ ] Mobile/touch-friendly interface
- [ ] WebGL shader improvements for CRT effects
- [ ] Authentic SAGE command language interpreter

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by the thousands of engineers, operators, and maintainers who worked on SAGE
- Thanks to the Computer History Museum for preserving SAGE documentation
- Built with [Reflex](https://reflex.dev) - Python web framework
- CRT effects inspired by vintage computing enthusiasts

---

**Note:** This is a simulation for educational and entertainment purposes. It does not represent classified military systems or current air defense technology.

---

**"The SAGE system was the most ambitious computing project of its era, and in many ways, it defined what we now take for granted in modern computing."**

*Press POWER ON to begin your journey back to the dawn of interactive computing.*
