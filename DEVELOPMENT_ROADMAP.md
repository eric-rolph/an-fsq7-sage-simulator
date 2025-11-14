# SAGE Simulator - Development Roadmap

**Status:** Radar Display Fixed ✅  
**Last Updated:** 2025-11-13  
**Current Phase:** Core Interactions & Track Management

---

## ✅ COMPLETED: Radar Display Foundation

### Achievements
- **P7 Phosphor CRT Simulation**: Authentic dual-layer canvas (blue fast decay + green slow persistence, 0.012 decay rate)
- **React Lifecycle Solution**: Canvas replacement detection (100ms polling) survives React re-renders
- **Geographic Overlays**: East Coast, Great Lakes, range rings, cities, bearing markers
- **Rotating Sweep**: 6° per second with additive phosphor trails
- **Track Rendering**: Color-coded dots with 1.5-second phosphor persistence trails

### Technical Foundation
- Canvas 2D rendering @ 60 FPS with dual-layer persistence
- Continuous canvas monitoring (100ms polling) detects React replacements
- Clean separation: Python state → JSON (data divs) → JavaScript (crt_radar.js) → Canvas
- Automatic initialization on page load (no manual console commands)

---

## ✅ COMPLETED PRIORITIES (Core Features)

### Priority 1: **Track Lifecycle & Correlation** ✅ COMPLETE
**Persona:** Ada (CS/engineering student)  
**Learning Objective:** Understand detect → correlate → classify workflow
**Status:** Implemented and committed (commits fd5ec4d, 4c58f60, f5d565e)

#### Features to Implement:
1. **Track State Visualization**
   - New track appears as "UNCORRELATED" (yellow + question mark)
   - Correlation process shows "CORRELATING..." status (2-3 seconds)
   - Successful correlation → classified type (hostile/friendly/unknown)
   - Show confidence level (LOW/MED/HIGH) based on radar returns

2. **Manual Correlation Override**
   - Light gun click on uncorrelated track → opens classification panel
   - Operator can manually classify: Hostile / Friendly / Unknown / Ignore
   - Shows why auto-correlation failed (weak signal, no IFF, etc.)
   - **Meaningful play:** Manual classification changes track color immediately

3. **Track History Panel**
   - Side panel showing track lifecycle: First Detection → Correlation → Classification → Current
   - Shows raw radar data: altitude, speed, heading, IFF response
   - **Cognitive fidelity:** Mirrors real SAGE correlation process

**Implementation:**
- Add `track.correlation_state: str` (uncorrelated/correlating/correlated)
- Add `track.confidence_level: str` (low/med/high)
- Add `track.correlation_reason: str` (auto/manual/iff/visual)
- Create `components_v2/track_classification_panel.py`
- Update CRT radar to show correlation state visually (different shapes/colors)

### Priority 2: **Interceptor Assignment** ✅ COMPLETE
**Persona:** Sam (sim/games player)  
**Learning Objective:** Make tactical decisions with visible consequences
**Status:** Implemented and committed (commits c8a8be9, d6dc8bf)

#### Features to Implement:
1. **Interceptor Launch Panel**
   - List of available interceptors with:
     - Type (F-89, F-102, etc.)
     - Location (base name, distance to track)
     - Fuel status, weapon load
     - Status (ready/scrambling/airborne/engaging/returning)
   
2. **Assignment Workflow**
   - Light gun select hostile track → shows threat assessment
   - Click "ASSIGN INTERCEPTOR" button
   - System suggests best interceptor (closest, adequate fuel, armed)
   - Operator can override selection
   - **Meaningful play:** Assignment creates intercept vector on radar (blue dashed line)

3. **Engagement Visualization**
   - Interceptor track appears on radar (blue icon + trail)
   - Intercept vector updates in real-time as aircraft closes
   - Distance countdown: "120 mi → 100 mi → 80 mi..."
   - Weapon range indicator: "IN RANGE" when <10 miles
   - Engagement result: "SPLASH ONE" (success) or "MISS" (failure)

**Implementation:**
- Add `sim/models.py`: `Interceptor` dataclass
- Add `state_model.py`: `InterceptorState` with location, fuel, status
- Update `simulation_tick_loop()`: Move interceptors toward targets
- Create `components_v2/interceptor_panel.py`
- Add intercept vector rendering to `crt_radar.js`
- Add engagement outcome logic (probability based on distance, weapon type)

### Priority 3: **System Inspector Overlay** ✅ COMPLETE
**Persona:** Ada (CS/engineering student)  
**Learning Objective:** See "inside" the computer system
**Status:** Implemented and committed (commit 4db3781)
**Features:** CPU state panel, 16 memory banks visualization, queue inspector with bottleneck warnings, Shift+I toggle

---

## 🎯 NEXT PRIORITIES (Additional Features)

#### Features to Implement:
1. **CPU State Panel**
   - Show current instruction being executed
   - Program counter, accumulator, index registers
   - Memory address being accessed
   - Instruction queue depth
   - **Toggle on/off** via keyboard shortcut (Shift+I)

2. **Memory Visualization**
   - Show which memory banks are active (visual highlight)
   - Track which programs are loaded in which banks
   - Show memory access patterns (hot/cold addresses)
   - Display vacuum tube health per memory bank

3. **Queue Inspector**
   - Radar input queue: raw returns waiting for correlation
   - Track processing queue: tracks awaiting classification
   - Display update queue: pending screen updates
   - **Show bottlenecks:** Queue depth warnings (red if >80% full)

**Implementation:**
- Add `state_model.py`: `CPUState` with registers, program counter
- Create `components_v2/system_inspector_overlay.py`
- Add keyboard shortcut handling for toggle
- Integrate with existing `cpu_core.py` authentic execution
- Visual design: Semi-transparent overlay, doesn't block radar view

---

## 📋 Additional Features (Lower Priority)

### Scenario System Enhancement
**Persona:** All personas  
**Pillars:** Scenario-driven learning, Meaningful play

- **Pre-built scenarios** with learning objectives:
  - "Scenario 1: Single Inbound" - Learn basic track detection
  - "Scenario 2: Multiple Bogeys" - Practice prioritization
  - "Scenario 3: Equipment Failure" - Handle tube failures mid-engagement
  - "Scenario 4: Saturated Defense" - Overwhelming enemy attack
  
- **Debrief System:**
  - Show performance metrics after scenario
  - Tracks detected: 12/15 (80%)
  - Correct classifications: 10/12 (83%)
  - Successful intercepts: 7/10 (70%)
  - Time to assignment: avg 45 seconds
  - **Learning moment:** Show what went wrong on missed intercepts

### Sound Effects & Audio Feedback
**Persona:** Grace (history nerd)  
**Pillar:** Historical feel

- Authentic sounds from SAGE documentation:
  - Radar sweep "ping"
  - Teletype clatter for track data
  - Warning klaxon for high-priority threats
  - "Engagement tone" when interceptor in weapon range
  - Voice alerts (synthesized): "UNCORRELATED TRACK", "HOSTILE CONFIRMED"

### Network & Station View
**Persona:** Ada (system understanding)  
**Pillar:** System transparency

- Show SAGE radar network:
  - DEW Line stations (Arctic)
  - Mid-Canada Line
  - Pinetree Line
  - Gap-filler radars
  - GCI (Ground Control Intercept) stations
  
- Visual map showing which stations contribute to current radar picture
- Station failure simulation (track drops disappear from coverage area)

---

## 🛠️ Technical Debt & Improvements

### Performance Optimization
- Benchmark track rendering at 100+ tracks
- Implement spatial partitioning if needed (quadtree for track queries)
- Optimize trail rendering (currently 20 points × N tracks)

### Cross-Browser Testing
- Test on Chrome, Firefox, Safari, Edge
- Handle Canvas 2D differences
- Fallback for older browsers

### Accessibility
- Keyboard navigation for all controls
- Screen reader support for track data
- High contrast mode option
- Colorblind-friendly palette options

### Documentation
- User guide with keyboard shortcuts
- Developer docs for adding scenarios
- API documentation for components
- Architecture diagrams

---

## 📊 Metrics & Success Criteria

### For Ada (CS/Engineering Student):
- Can identify all major subsystems (radar, correlator, tracker, display) ✓
- Understands correlation workflow (detect → correlate → classify) ⏳
- Can explain why SAGE used vacuum tube memory ⏳
- Sees direct connection between CPU instructions and radar updates ⏳

### For Grace (History Nerd):
- Feels period-authentic visual design ✓
- Experiences realistic operator workflow ⏳
- Understands Cold War context and SAGE's role ⏳
- Appreciates technical achievement (1950s computing) ⏳

### For Sam (Sim/Games Player):
- Makes meaningful tactical decisions (target prioritization) ⏳
- Experiences consequences of choices (successful/failed intercepts) ⏳
- Wants to replay scenarios to improve scores ⏳
- Finds gameplay engaging (not just educational) ⏳

---

## 🎯 Immediate Next Steps (This Week)

1. **Track Correlation Panel** (2-3 hours)
   - Add correlation state to Track model
   - Create classification UI panel
   - Wire light gun click → panel open
   - Add manual classification buttons
   - Show immediate visual feedback on radar

2. **Interceptor Data Model** (1-2 hours)
   - Define Interceptor dataclass
   - Add to InteractiveSageState
   - Create sample interceptors at bases
   - Position on radar scope

3. **Intercept Vector Rendering** (1 hour)
   - Add blue dashed line drawing to crt_radar.js
   - Show distance to target
   - Update vector in render loop

4. **Test & Iterate** (1 hour)
   - Create test scenario with 3 hostiles + 5 interceptors
   - Verify assignment workflow
   - Check for visual clarity
   - Adjust colors/labels for legibility

---

## 📚 Reference Materials

### Design Documents:
- `docs/DESIGN_NOTES` - Personas, pillars, principles
- `docs/VISUAL_REFERENCE.md` - P7 phosphor, vector CRT language
- `docs/RADAR_ARCHITECTURE.md` - Current technical implementation

### Key Implementation Files:
- `assets/crt_radar.js` - Canvas rendering, P7 phosphor
- `interactive_sage.py` - State management, simulation loop
- `sim/models.py` - Core data models
- `components_v2/` - UI components

### Historical References:
- SAGE System documentation (Ulmann's work)
- AN/FSQ-7 specifications
- 1950s radar operator procedures

---

**Next Review:** After implementing track correlation panel  
**Status Updates:** Document in git commits with learning objective tags
