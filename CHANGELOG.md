# Changelog

All notable changes to the AN/FSQ-7 SAGE Simulator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Testing Infrastructure - Week 1 In Progress** (2025-11-17)
  - Pytest configuration with coverage reporting
  - 116 automated tests (49 unit, 36 simulation, 31 design_language)
  - Test fixtures for tracks, interceptors, scenarios
  - Unit tests:
    * CPU core (one's complement arithmetic, indexed addressing)
    * Light gun (selection logic, coordinate mapping)
    * Track correlation (state machine transitions)
    * Drum I/O (asynchronous field-based storage, status channels) - NEW
  - Simulation tests for interceptor logic, scenarios, track physics
  - Design language tests enforcing UI/display contracts:
    * Mode-free UI pattern (buttons disabled not hidden)
    * P14 monochrome display (shape-based symbology, no color coding)
    * Layout invariants (fixed panel positions, consistent structure)
  - 100% pass rate achieved (116/116 tests)
  - 11% code coverage (up from 8%, target 80%+)

---

## [1.0.0] - 2025-11-17

### Added

**Core Simulation (Priority 1-3)**
- Track correlation system with state machine (UNCORRELATED → CORRELATED)
- Interceptor assignment and launch capabilities
- System inspector overlay for debugging
- Light gun selection system with arm/select/clear workflow
- CPU core with authentic AN/FSQ-7 instruction set
- Drum I/O system for track persistence
- Real-time scenario simulation loop

**Scenarios & Events (Priority 4, 7)**
- 8 complete scenarios: Training, Heavy Load, Stealth, Waves, Intercept Demo, etc.
- Dynamic scenario events system (NEW_TRACK, SPEED_CHANGE, ALTITUDE_CHANGE, etc.)
- Performance metrics tracking (response time, classification accuracy, engagement success)
- Scenario debrief system with detailed analytics

**Display System (Priority 6)**
- P14 phosphor CRT simulation with authentic orange phosphor glow
- 2.5-second refresh cycle (historically accurate SAGE display drum timing)
- Phosphor persistence layer with continuous 60fps decay
- Vector-based track symbology (circles, squares, diamonds, triangles)
- Monochrome display (no color coding - historically accurate)
- Blue room ambient lighting simulation
- Geographic overlays (coastlines, range rings, SAGE stations)
- Network and station view with BOMARC/Nike site visualization

**Audio System (Priority 5)**
- Authentic 1950s radar sweep loop
- Track detection blips and correlation beeps
- Light gun click and selection sounds
- Intercept launch and hostile alerts
- System message beeps
- Volume controls (ambient, effects, alerts)

**User Interface (Priority 2, 3, 8)**
- Mode-free UI design (buttons disabled, not hidden)
- Track detail panel (right side, fixed layout)
- Interceptor assignment panel
- Track classification panel
- System messages panel with reactive updates
- Tube maintenance indicators
- Global action controls (ARM LIGHT GUN, LAUNCH INTERCEPT, CLEAR SELECTION)

**Developer Tools**
- Tutorial system with 8 interactive lessons
- Operator workflow guide
- System inspector with CPU trace
- Performance testing tools

### Technical Implementation

- **Frontend:** Reflex framework (Python → React)
- **Rendering:** Canvas 2D with JavaScript rendering loop
- **State Management:** Centralized Reflex state with event handlers
- **Data Injection:** Python → JSON → window globals → JavaScript
- **Package Manager:** UV (not conda/pip)

### Design Invariants

- **Mode-Free UI:** No hidden modes, buttons disabled when unavailable
- **Fixed Layout:** Detail panel always on right, action controls in bottom region
- **P14 Monochrome:** All symbology in orange phosphor, no color coding
- **Track Symbols:** Shape indicates type (circle=friendly, square=hostile, diamond=unknown, triangle=missile)
- **2.5-Second Refresh:** Computer updates display drum every 2.5 seconds (historically accurate)

### Documentation

- Complete user guide with operator workflows
- Architecture documentation
- Design philosophy and patterns
- Historical context and SAGE background
- Developer contribution guide
- Indexed addressing implementation notes
- High-fidelity emulation details

---

## [Unreleased]

### Planned Features

- Authentic tabular track display (Priority 8 completion)
- Multi-player support (multiple operator consoles)
- Historical scenarios (Cuban Missile Crisis, Berlin Airlift)
- SAGE command language interpreter
- Weather effects (rain clutter, storm cells)
- Accessibility improvements (keyboard navigation, screen reader support)

### Known Issues

- WebSocket warnings during hot reload (harmless, ignore)
- No automated test suite (manual testing only)
- Mobile/touch support limited (light gun requires mouse)

---

## Release Notes

### Version 1.0.0 - "Initial Release"

This release marks the completion of all 8 development priorities and represents a historically accurate simulation of the AN/FSQ-7 SAGE computer''s Situation Display console. The simulator faithfully reproduces the P14 phosphor CRT display, 2.5-second refresh cycle, vector symbology, and operator workflows used by Cold War air defense crews.

**Key Achievements:**
- ✅ All 8 development priorities complete
- ✅ 8 interactive scenarios with dynamic events
- ✅ Historically accurate P14 phosphor display
- ✅ Authentic 1950s audio design
- ✅ Complete operator workflows (detection → correlation → intercept)
- ✅ Comprehensive documentation (user guide, architecture, design)

**Target Audience:**
- Computer history enthusiasts
- Cold War researchers
- Aviation historians
- Software developers interested in historical computing
- Educators teaching computing history

**System Requirements:**
- Python 3.11+
- UV package manager
- Modern web browser (Chrome, Firefox, Edge, Safari)
- 4GB RAM minimum
- Audio output recommended

---

## Historical Context

The AN/FSQ-7 was the largest computer ever built (3 acres, 55,000 vacuum tubes) and served as the backbone of North American air defense from 1958-1983. This simulator preserves and educates about this remarkable Cold War technology.

**References:**
- SAGE Air Defense System (Wikipedia)
- Computer History Museum SAGE Collection
- MITRE Corporation SAGE Technical Reports
- MIT Lincoln Laboratory Archives

---

For more information, see:
- [README.md](README.md) - Feature overview
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Comprehensive user manual
- [docs/HISTORY.md](docs/HISTORY.md) - SAGE historical background
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current development status
