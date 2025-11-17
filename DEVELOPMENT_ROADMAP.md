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

### Priority 4: **Scenario System Enhancement** ✅ COMPLETE
**Persona:** All personas (Ada: learning assessment, Grace: mission realism, Sam: score improvement)
**Status:** Implemented and committed (commits 3fbc807, 0f95d24)

#### Implemented Features:
1. **Debrief System** ✅
   - Performance metrics: detection %, classification accuracy, intercept success
   - Learning moments panel: mistakes with improvement tips
   - Mission objectives tracker with completion status
   - Grade panel (A-F) based on weighted scoring (30% detection, 40% classification, 30% intercepts)
   - Action buttons: Continue, Replay Scenario, Next Scenario
   - Full-screen modal overlay with SAGE-authentic styling

2. **Enhanced Scenario Model** ✅
   - `learning_objectives`: Educational goals for each scenario
   - `success_criteria`: Clear mission completion requirements
   - `difficulty`: beginner/intermediate/advanced/expert ratings
   - `objectives`: Specific tasks to complete

3. **Educational Scenarios** ✅
   - **Demo 1 - Three Inbound** (beginner): Basic detection and threat prioritization
   - **Scenario 5 - Correlation Training** (intermediate): Manual classification practice
   - **Scenario 6 - Equipment Degradation** (advanced): Tube failures under pressure
   - **Scenario 7 - Saturated Defense** (expert): Resource allocation with 8 targets, 3 interceptors

4. **Performance Tracking** ✅
   - `ScenarioMetrics` dataclass: tracks detection, classification, intercepts, timing
   - Event handlers: `close_debrief()`, `restart_scenario()`, `next_scenario()`, `complete_scenario()`
   - State fields: `scenario_complete`, `scenario_start_time`, `scenario_metrics`

**Files:**
- `components_v2/scenario_debrief.py` (362 lines)
- `state_model.py`: ScenarioMetrics dataclass
- `sim/scenarios.py`: Enhanced Scenario class + 3 new educational scenarios
- `interactive_sage.py`: State integration and event handlers

---

### Priority 5: **Sound Effects & Audio Feedback** ✅ COMPLETE
**Persona:** Sam (immersion), Grace (authenticity)  
**Pillars:** Cognitive fidelity, Meaningful play, Historical feel  
**Status:** Implemented and committed (commit c35e6b6)

#### Features Implemented:
1. **Comprehensive Sound System**
   - 25+ sound effects across 4 categories (ambient, UI, alerts, effects)
   - Web Audio API integration with JavaScript sound player
   - Real-time volume control (3 independent channels: ambient, effects, alerts)
   - Master mute toggle
   - 4 volume presets: SILENT, SUBTLE, NORMAL, IMMERSIVE

2. **Sound Settings Panel**
   - Dedicated UI panel in left sidebar
   - 3 volume sliders with real-time percentage display
   - 6 test sound buttons for immediate feedback
   - Preset buttons for quick configuration

3. **Event Integration**
   - Sound triggers on: track detection, light gun selection, button presses, interceptor assignment
   - Direct JavaScript calls via rx.call_script for real-time playback
   - State synchronization between Python and JavaScript

4. **Ready for Audio Files**
   - Sound library defined with file paths, volumes, categories
   - Player ready to load .wav/.mp3 files when available
   - Console logging for debugging sound loading

**Files:**
- `components_v2/sound_effects.py` (741 lines) - complete sound system
- `interactive_sage.py`: Sound state fields and event handlers
- Integration with existing UI events

**Note:** Actual audio files not included - system ready for authentic SAGE sound research phase

---

### Priority 6: **Network & Station View** ✅ COMPLETE
**Persona:** Ada (system understanding)  
**Pillar:** System transparency  
**Status:** Implemented and committed (commits 46f57db, e121c12)

#### Features Implemented:
1. **Comprehensive Station Network**
   - 25 historical SAGE radar stations across North America
   - 5 station types with unique symbols and colors:
     - △ DEW Line (8 stations) - cyan, Arctic early warning
     - ◇ Mid-Canada Line (6 stations) - orange, central Canada
     - ▽ Pinetree Line (8 stations) - green, southern border
     - ○ Gap-Filler (3 stations) - yellow, US interior
     - ⬟ GCI/SAGE DC (3 stations) - magenta, command centers
   
2. **Canvas Rendering System**
   - Coverage circles showing radar range (semi-transparent, status-based alpha)
   - Station markers with type symbols and abbreviated names
   - Connection lines from stations to nearest GCI center (dashed, low opacity)
   - Status-based rendering: operational (1.0), degraded (0.6), offline (0.3)

3. **UI Integration**
   - Toggle button: 🌐 NETWORK VIEW / 📡 RADAR VIEW
   - Network legend panel showing all station types (auto-shows with network view)
   - Total station count display (28 stations including scenario bases)
   - Seamless toggle between network overlay and standard radar view

4. **State Management**
   - `show_network_view`: Toggle state
   - `selected_station_id`: For future station selection feature
   - `network_stations_data`: JSON serialization of all stations
   - Methods: `toggle_network_view()`, `select_station()`, etc.

5. **JavaScript Integration**
   - CRTRadarScope prototype methods: `renderNetworkStations()`, `getStationStyle()`, `findNearestGCI()`
   - Data polling integrated with existing CRT update loop (1000ms)
   - Automatic station data injection via window.__SAGE_NETWORK_STATIONS__

**Files:**
- `components_v2/network_stations.py` (389 lines) - station data, legend panel, rendering script
- `interactive_sage.py`: Network state fields, handlers, data serialization
- `assets/crt_radar.js`: Integration hooks for network rendering

**Verified:**
- ✅ 28 stations rendering correctly with coverage circles
- ✅ Station markers with proper symbols and colors
- ✅ GCI connection lines displayed
- ✅ Toggle functionality working perfectly
- ✅ Legend panel shows/hides appropriately

---

## 🎯 NEXT PRIORITIES (Additional Features)

### Future Network Enhancements
**When:** After core features complete

- Interactive station selection (click to show details panel)
- Station failure simulation affecting track coverage
- Real-time data flow animation from stations to GCI
- Station status degradation over time

---

### Priority 8: **🔴 CRITICAL - Authentic SAGE Display Format** ⚠️ IN PLANNING
**Status:** Major corrections required based on C702-416L-ST manual analysis  
**Persona:** All (historical accuracy fundamental to experience)  
**Pillar:** Historical feel, Cognitive fidelity  
**Impact:** HIGH - Complete rewrite of track rendering system

#### Discovery from Official Manual

Analysis of the **C702-416L-ST Situation Display Generator Element** manual (pages 0440-0540) reveals our track display format is **fundamentally incorrect**.

**Current Implementation (WRONG):**
- Geometric shapes: circles (friendly), squares (hostile), diamonds (unknown), triangles (missiles)
- Color-coded symbology
- Simple dot rendering

**Authentic SAGE Display (CORRECT):**
- **CHARACTER-BASED TABULAR FORMAT** with 5 features:
  ```
      A1 A2 A3 A4    ← Track ID (e.g., "FPTKG")
      B1 B2 B3 B4    ← Track data
      D1 D2 A5 A6    ← Additional data
  ──►  E  ◄──        ← Central point (aircraft position)
      C1 C2 C3 C4    ← More data
  
  With VECTOR line showing direction/speed
  ```
- **Alphanumeric text** displayed as dot-matrix characters
- **4 positioning modes** (above/below/left/right of central point) to avoid clutter
- **RD (Radar) symbols**: Bright PRESENT + dim HISTORY trail (7 positions)
- **Up to 4 vectors** per track showing heading, speed, predicted path

#### Required Changes

1. **Character Rendering System** (NEW)
   - Implement 5×7 or 7×9 dot-matrix font
   - Generate A-Z, 0-9 characters for CRT display
   - Position text relative to canvas coordinates

2. **Tabular Track Format** (MAJOR REWRITE)
   - Replace geometric shapes with character matrix
   - Define A/B/C/D/E feature layout
   - Encode track data into alphanumeric characters
   - Support 4 orientation modes based on position bits
   - Implement vector constraints (cannot cross character groups)

3. **Bright/Dim History System** (MODERATE)
   - Present radar returns: BRIGHT intensity
   - History positions (last 7): DIM and fading
   - Update every ~0.5 seconds (not synchronized)
   - Comet-tail effect showing track movement

4. **Track Data Encoding** (NEW)
   - Generate proper character codes for:
     - Feature A: Track identification
     - Feature B: Altitude/speed data
     - Feature C: Heading/classification
     - Feature D: Additional metadata
   - Match authentic SAGE encoding (requires more manual research)

5. **Multiple Vector Display** (MODERATE)
   - Support up to 4 vectors per track
   - Vector length = magnitude (speed)
   - Vector direction = heading
   - Quadrant-based positioning (LS/RS bits)

#### Implementation Plan

**Phase 1: Prototype Character System** (2-3 days)
- Create dot-matrix font renderer
- Test character display on canvas
- Verify readability at CRT resolution

**Phase 2: Tabular Format Core** (3-5 days)
- Implement 5-feature layout engine
- Position features around central point
- Add 4 orientation modes
- Test with static data

**Phase 3: Track Data Integration** (2-3 days)
- Update Track model with character data
- Generate feature characters from track properties
- Integrate with existing simulation loop

**Phase 4: History & Vectors** (2-3 days)
- Implement bright/dim history trail
- Add vector rendering with constraints
- Polish timing and persistence

**Phase 5: Testing & Refinement** (1-2 days)
- Validate against historical photographs
- Adjust character spacing and sizing
- Optimize rendering performance
- Update documentation

#### What We Keep (Already Correct)

✅ Console layout and switches (matches Figure 9.2)  
✅ CRT phosphor characteristics (P14 simulation)  
✅ Geographic overlays (coastlines, range rings)  
✅ Off-centering controls  
✅ Feature selection system  
✅ Light gun interaction workflow  
✅ Drum buffer architecture  

#### Documentation References

- **Primary Source**: `docs/SAGE_DISPLAY_CORRECTIONS_REQUIRED.md` (complete analysis)
- **Manual Pages**: C702-416L-ST pages 0440-0540
- **Figures Referenced**: 4-5 (tabular format), 4-8 (character examples), 4-9 (vectors), 4-11 (history), 4-12 (RD symbols), 9.2 (console layout)

**Estimated Effort:** 10-15 days (major rewrite)  
**Priority:** HIGH (fundamental to historical accuracy)  
**Breaking Changes:** Track rendering only (scenarios/logic unchanged)

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
