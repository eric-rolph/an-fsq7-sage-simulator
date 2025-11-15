# SAGE Console Historical Accuracy Assessment

## Current Implementation vs. Historical SAGE Consoles

Based on Bernd Ulmann's "AN/FSQ-7 – The Computer That Shaped the Cold War" and IBM Display System manuals (via Ed Thelen), this document compares our current implementation with authentic SAGE console design.

---

## 🎯 Two Console Types: Surveillance vs. Situation Display

**CRITICAL DISTINCTION:** SAGE Direction Centers had **two different console types** working together in the air defense workflow:

### 1. **Surveillance Consoles (LRI/GFI - Raw Radar)**
**Purpose:** Initial detection and track assignment

**Display Technology:** 
- PPI-style radar display (Plan Position Indicator)
- Shows **raw radar returns** from ground-based radars
- Displays "last seven scans" so operators see trails
- 16" or 19" CRT with sweep-style display

**Operator Role:** 
- Search operators monitor raw radar blips
- Assign track numbers to new contacts
- Filter noise/clutter from actual aircraft
- Feed track data into SAGE computer for correlation

**Controls:**
- Range scale selector (10mi, 25mi, 50mi, 100mi, etc.)
- Gain/intensity controls
- Sweep speed adjustment
- Trail persistence controls
- Camera capture toggle (for photographic record)

**Symbology:**
- Raw blips (uncorrelated radar returns)
- Range rings
- Geographic overlay (coastlines, bases)
- Assigned track numbers appear once computer accepts

---

### 2. **Situation Display Consoles (SD - Consolidated Picture)**
**Purpose:** Air defense coordination and intercept control

**Display Technology:**
- 19" P14 phosphor vector display
- Shows **computer-generated symbology** (tracks, not raw returns)
- Digital/vector display updated every 2.5 seconds
- Displays correlated, filtered, and identified tracks

**Operator Role:**
- Identification controllers classify tracks (FRIENDLY/HOSTILE/UNKNOWN)
- Weapons controllers assign interceptors to hostile tracks
- Senior controllers monitor overall air defense picture
- Crosstell operators coordinate with other Direction Centers

**Controls:**
- Category selection switches (S1-S13) - filter by track type
- Feature selection switches (S20-S24) - toggle overlays
- Off-centering (7×7 grid) - focus on specific area
- Expansion rotary (1×/2×/4×/8×) - zoom into sector
- Light gun - select tracks for action
- MI switches - manual intervention buttons

**Symbology:**
- Correlated tracks (circles, squares, diamonds, triangles)
- Track IDs and altitude blocks
- Flight paths (history trails)
- Interceptor vectors
- Threat corridors

---

## 🔄 Workflow: Surveillance → Situation Display

**Historical Air Defense Process:**

1. **Detection (Surveillance Console)**
   - Raw radar sweeps show new blip
   - Operator sees blip persist across 3-7 scans
   - Operator uses light gun to "hook" the blip
   - Assigns preliminary track number (e.g., "TRACK 5001")

2. **Computer Correlation (SAGE System)**
   - Computer receives track 5001 from multiple radars
   - Correlates position/altitude/speed across sites
   - Calculates trajectory and threat assessment
   - Adds to consolidated air picture

3. **Identification (SD Console)**
   - Track 5001 appears on SD as UNKNOWN symbol
   - ID controller checks IFF response
   - Uses light gun to select track
   - MI button: "CHANGE ID" → reclassifies as FRIENDLY or HOSTILE

4. **Intercept Control (SD Console)**
   - Weapons controller sees HOSTILE track
   - Selects track with light gun
   - MI button: "WEAPONS ASSIGN" → assigns F-106 interceptor
   - Monitors intercept progress on SD

5. **Crosstell/Handoff (SD Console)**
   - As track crosses sector boundary
   - Controller selects track
   - MI button: "TRANSFER" → sends to adjacent Direction Center

---

## ✅ Historically Accurate (Keep/Refine)

### 1. Category Selection Switches (S1-S13)
**Status:** ✅ **Implemented correctly**

**Historical:** Left-side vertical bank of switches to filter which message categories display (track types, raids, etc.). Too much symbology was a problem, so these gate which message types are drawn.

**Current Implementation:** 
- `category_select_panel()` in `sd_console.py`
- 13 switches: ALL, FRIENDLY, UNKNOWN, HOSTILE, MISSILE, BOMBER, FIGHTER, ALT<10K, ALT 10K-30K, ALT>30K, INBOUND, OUTBOUND, LOITERING
- Visual feedback with active/inactive states
- Correctly filters radar display

**Action:** ✅ Keep as-is, already accurate

---

### 2. Feature Selection Switches (S20-S24)
**Status:** ✅ **Implemented correctly**

**Historical:** Separate bank from category switches; used to toggle feature groups (coastlines, grid, installation markers, etc.) on/off.

**Current Implementation:**
- `feature_select_panel()` in `sd_console.py`
- 4 switches: S20 FLIGHT PATHS, S21 INTERCEPTS, S23 CALLSIGNS, S24 COASTLINES
- Note: S22 (RANGE RINGS) correctly removed as it's a PPI radar feature, not SD

**Action:** ✅ Keep as-is, already accurate

---

### 3. Off-Centering Controls (7×7 Grid)
**Status:** ✅ **Implemented correctly**

**Historical:** The SD screen is conceptually split into 7×7 areas. Buttons along the left and top let you choose which cell to expand. This solves the "symbology overprinting problem" when many tracks cluster together.

**Current Implementation:**
- `off_centering_controls()` in `sd_console.py`
- 7 row buttons (1-7)
- 7 column buttons (A-G)
- Sector selection: operator clicks vertical + horizontal (e.g., "3" + "D" = sector 3-D)
- Grid toggle: SHOW GRID button

**Action:** ✅ Keep as-is, already accurate

---

### 4. Expansion Rotary Switch
**Status:** ✅ **Implemented correctly**

**Historical:** A rotary switch sets the expansion factor (×1, ×2, ×4, ×8). This comes directly from Whirlwind experience with overprinted symbology; ×8 expansion is explicitly justified in manuals.

**Current Implementation:**
- 4 discrete buttons: 1X, 2X, 4X, 8X
- No smooth zoom (correct — free pan/zoom is fiction)
- Visual feedback for selected magnification

**Action:** ✅ Keep as-is, already accurate

---

### 5. Light Gun
**Status:** ⚠️ **Partially implemented** (exists in `light_gun.py`)

**Historical:** The operator uses the light gun to associate messages with a particular track/target on the SD. The trigger essentially "releases" a message similar to an activate push-button. Light gun events carry: (console ID, time, track/target position) into the MDI layer.

**Current Implementation:**
- `light_gun.py` component exists
- ARM LIGHT GUN button
- Crosshair mode
- Click to select track
- ✅ Simulates light gun correctly

**Action:** ✅ Keep as-is, already accurate

---

## ❌ Historically Inaccurate (Fix Required)

### 1. Brightness Control (CRITICAL FIX)
**Status:** ❌ **Historically inaccurate**

**Historical:** Brightness is controlled **per-feature group** via **bright/dim switches**, not as a single analog knob for the whole tube. You pick "bright" vs "dim" for specific groups (coastlines, grids, tracks, etc.).

**Current Implementation:**
- `bright_dim_control()` in `sd_console.py`
- Single continuous slider (0-100%)
- Preset buttons: DIM (30%), MED (50%), BRIGHT (75%)
- ❌ This is wrong — there was no master brightness slider

**Required Changes:**
1. Remove global brightness slider
2. Add BRIGHT/DIM toggle switches **per feature group**:
   - TRACKS: BRIGHT/DIM
   - COASTLINES: BRIGHT/DIM
   - GRID: BRIGHT/DIM
   - FLIGHT PATHS: BRIGHT/DIM
   - INTERCEPTS: BRIGHT/DIM
   - CALLSIGNS: BRIGHT/DIM
3. Each feature gets 2-position switch (not continuous)
4. BRIGHT = 100% intensity, DIM = 30-40% intensity
5. Position switches adjacent to feature selection switches

**File to modify:** `an_fsq7_simulator/components_v2/sd_console.py`

---

### 2. Manual Intervention (MI) Buttons (MISSING)
**Status:** ❌ **Not implemented**

**Historical:** IBM's introduction manual describes "manual-intervention switches" on consoles for requesting data, answering computer queries, transferring messages to other consoles, etc. These are core MI buttons near the SD/DD.

**Historical MI Button Functions:**
- ASSIGN TRACK
- CHANGE ID
- TRANSFER / CROSSTELL
- REQUEST DATA
- WEAPONS ASSIGN / LAUNCH
- CANCEL / CLEAR

**Current Implementation:**
- ❌ None of these exist
- We have scattered action buttons but not proper MI switch cluster

**Required Changes:**
1. Create new `mi_switches_panel()` component
2. Add 6-8 MI buttons in a cluster (right side near DD tube location)
3. Wire to state methods:
   - `assign_track()` - assign track number to light gun selection
   - `change_track_id()` - reclassify track (FRIENDLY→HOSTILE, etc.)
   - `request_track_data()` - pull detailed track info to DD
   - `transfer_message()` - send to another console (simulated)
   - `weapons_assign()` - assign interceptor (already exists, wire to this)
   - `cancel_action()` - clear current selection
4. Require light gun selection + MI button press (authentic workflow)

**New file:** Create `an_fsq7_simulator/components_v2/mi_switches.py`

---

### 3. Digital Display (DD) Tube Controls (MISSING)
**Status:** ❌ **Not implemented**

**Historical:** DD tube sits in console frame upper-right, shows tabular/slow-changing data (track details, status lists). Controlled by MI buttons like REQUEST TRACK DETAIL, REQUEST SYSTEM STATUS.

**Current Implementation:**
- ❌ We show track detail in a panel but not as a separate "DD tube"
- ❌ No explicit "DD mode selector" or "DD request buttons"

**Required Changes:**
1. Create `dd_tube_display()` component (separate from SD)
2. Position in upper-right area of console
3. Add DD control buttons:
   - REQUEST TRACK DETAIL (shows selected track)
   - REQUEST SYSTEM STATUS (shows tube health, interceptor status)
   - REQUEST INTERCEPTOR STATUS
4. DD shows last-requested data until updated
5. Use monospace font, limited to ~20 lines (Typotron constraint)

**New file:** Create `an_fsq7_simulator/components_v2/dd_tube.py`

---

### 4. Console Alarms and Status Lights (MISSING)
**Status:** ❌ **Not implemented**

**Historical:** Typical console has alarms and warning lights. At minimum:
- CONSOLE READY
- DATA LINK / DISPLAY OK
- SYSTEM ALERT / AIR DEFENSE ALERT
- MESSAGE PENDING / ACK REQUIRED

**Current Implementation:**
- ❌ No status lights panel
- We have scenario debrief but no real-time alert indicators

**Required Changes:**
1. Create `alarm_panel()` component
2. Add 4-6 indicator lights (colored boxes/circles)
3. Wire to state:
   - CONSOLE READY: always green (sim always ready)
   - DATA LINK OK: green if tracks updating, red if frozen
   - SYSTEM ALERT: red if HIGH/CRITICAL threats detected
   - MESSAGE PENDING: amber if unacknowledged events in system_messages_log
4. Add optional audio alarm for SYSTEM ALERT (can be toggled off)

**File to modify:** `an_fsq7_simulator/components_v2/sd_console.py` (add new function)

---

## 🔧 Layout Refactor Required

### Current Layout Issues
- Controls are scattered across left side
- No clear separation of function banks
- Brightness control prominent but historically inaccurate
- Missing MI button cluster
- Missing DD tube

### Authentic SAGE Console Layout

```
┌─────────────────────────────────────────────────────────┐
│                   CONSOLE FRAME                         │
│                                                         │
│  ┌──────────┐  ┌──────────────────┐  ┌──────────┐     │
│  │CATEGORY  │  │                  │  │  DD TUBE │     │
│  │SWITCHES  │  │   SD SCOPE       │  │(Typotron)│     │
│  │(S1-S13)  │  │   (19" P14)      │  │          │     │
│  │          │  │                  │  │          │     │
│  │          │  │                  │  └──────────┘     │
│  ├──────────┤  │                  │                   │
│  │FEATURE   │  │                  │  ┌──────────┐     │
│  │SWITCHES  │  │                  │  │ MI       │     │
│  │(S20-S24) │  │                  │  │ BUTTONS  │     │
│  │          │  │                  │  │          │     │
│  │ + BRIGHT │  │                  │  │ ASSIGN   │     │
│  │ + DIM    │  │                  │  │ CHANGE   │     │
│  │per group │  │                  │  │ REQUEST  │     │
│  ├──────────┤  │                  │  │ WEAPONS  │     │
│  │OFF-      │  │                  │  │ CANCEL   │     │
│  │CENTER    │  │                  │  └──────────┘     │
│  │7×7 GRID  │  └──────────────────┘                   │
│  │          │                        ┌──────────┐     │
│  │+ EXPAND  │                        │ ALARM    │     │
│  │(1×2×4×8×)│                        │ LIGHTS   │     │
│  └──────────┘                        └──────────┘     │
└─────────────────────────────────────────────────────────┘
```

**Left Bank (top to bottom):**
1. Category switches (S1-S13)
2. Feature switches (S20-S24) **with BRIGHT/DIM per feature**
3. Off-center controls (7×7)
4. Expansion switch (1×/2×/4×/8×)

**Right Bank (top to bottom):**
1. DD tube (upper right)
2. MI button cluster (middle right)
3. Alarm/status lights (lower right)

**Center:**
- SD scope (19" P14 phosphor display)
- Light gun interaction area

---

## 🎯 Implementation Priority

### Phase 1: Critical Fixes (Breaks Authenticity)
1. ✅ **Remove global brightness slider** - Replace with per-feature BRIGHT/DIM
2. ✅ **Add MI button cluster** - Core console interaction pattern
3. ✅ **Add DD tube component** - Separate display from SD

### Phase 2: Historical Completeness
4. ✅ **Add alarm/status lights** - Visual feedback for system state
5. ✅ **Refactor layout** - Left/right banks matching authentic console
6. ✅ **Add console ID** - Each console has designation (e.g., "ID-01")

### Phase 3: Polish
7. ✅ **Telephone facet** (optional) - Interconsole communication simulation
8. ✅ **Camera capture toggle** (for PPI monitors) - Historical feature
9. ✅ **Mark modern features** - Clearly label non-authentic additions

---

## 📝 Files to Modify/Create

### Modify Existing:
- `an_fsq7_simulator/components_v2/sd_console.py`
  - Remove `bright_dim_control()` function
  - Add BRIGHT/DIM toggles to `feature_select_panel()`
  - Refactor layout to left/right banks

### Create New:
- `an_fsq7_simulator/components_v2/mi_switches.py` - Manual intervention button cluster
- `an_fsq7_simulator/components_v2/dd_tube.py` - Digital Display (Typotron) component
- `an_fsq7_simulator/components_v2/alarm_lights.py` - Status indicators

### Update State:
- `an_fsq7_simulator/interactive_sage.py`
  - Add `feature_brightness: dict[str, str]` (maps feature → "bright"/"dim")
  - Add `dd_mode: str` (current DD display mode)
  - Add `dd_content: str` (current DD text content)
  - Add MI button handlers: `assign_track()`, `change_track_id()`, `request_track_data()`, etc.
  - Add alarm state: `system_alert: bool`, `message_pending: bool`

---

## 🔍 What to Drop/Demote

### Remove from "Authentic" Mode:
1. ❌ **Continuous brightness slider** - Never existed, per-feature only
2. ❌ **Free pan/zoom** - Discrete off-center + expansion only
3. ❌ **Sweep controls on SD** - SD is vector/digital, not raw radar

### Mark as "Modern/Dev Mode":
1. 🔧 **Time scrub** - Freeze and scrub SD states (debugging aid)
2. 🔧 **Free camera** - Pan/zoom for debugging (separate from authentic controls)
3. 🔧 **Debug overlays** - Hitboxes, internal IDs, etc.

---

## 🎮 Implementing Dual Console Modes in Simulator

### Console Mode Selector

Add a **console type selector** to switch between surveillance and situation display modes:

```python
# State field
console_mode: str = "situation_display"  # or "surveillance"

# Selector component
rx.tabs(
    rx.tabs_list(
        rx.tabs_trigger("Situation Display (SD)", value="situation_display"),
        rx.tabs_trigger("Surveillance Console (LRI)", value="surveillance"),
    )
)
```

---

### Mode 1: Surveillance Console (Raw Radar/PPI)

**Display Characteristics:**
- ✅ **Keep sweep controls** - authentic for surveillance consoles
- Show raw radar returns as blips
- Display "last seven scans" with fading trails
- Rotating sweep line (simulated radar antenna)
- Range rings at fixed intervals

**Controls Panel (Left Side):**
```
┌──────────────┐
│ RANGE SCALE  │
│ ○ 10 MI      │
│ ○ 25 MI      │
│ ● 50 MI      │
│ ○ 100 MI     │
│ ○ 200 MI     │
├──────────────┤
│ SWEEP        │
│ Speed: [===] │
│ Gain:  [===] │
│ Trails:[===] │
├──────────────┤
│ OVERLAYS     │
│ □ Range Rings│
│ □ Coastlines │
│ □ Bases      │
├──────────────┤
│ TRACK HOOK   │
│ [ARM LIGHT   │
│  GUN]        │
│              │
│ [ASSIGN      │
│  TRACK #]    │
└──────────────┘
```

**Display Features:**
- Raw blips (uncorrelated returns)
- Fading trails (last 7 scans)
- Rotating sweep line
- Range rings
- Hook cursor for track assignment

**Use Cases:**
- **Tutorial Scenario:** "Surveillance Operator Training"
  - Player identifies new blips
  - Hooks blips to assign track numbers
  - Feeds tracks to SAGE computer
  
- **Realistic Detection:** Show raw radar before computer correlation
  - Noisy/cluttered environment
  - Player must distinguish aircraft from weather/ground clutter

**File:** `an_fsq7_simulator/components_v2/surveillance_console.py`

---

### Mode 2: Situation Display Console (Consolidated Picture)

**Display Characteristics:**
- ❌ **No sweep controls** - SD is vector/digital display
- Show correlated tracks (computer-processed)
- Vector symbology (circles, squares, diamonds)
- Clean, filtered air picture

**Controls Panel (Left Side):**
```
┌──────────────┐
│ CATEGORY     │
│ SELECT       │
│ (S1-S13)     │
├──────────────┤
│ FEATURE      │
│ SELECT       │
│ (S20-S24)    │
│ + BRIGHT/DIM │
├──────────────┤
│ OFF-CENTER   │
│ 7×7 GRID     │
│ + EXPANSION  │
└──────────────┘
```

**Controls Panel (Right Side):**
```
┌──────────────┐
│  DD TUBE     │
│ (Typotron)   │
├──────────────┤
│ MI BUTTONS   │
│ - ASSIGN     │
│ - CHANGE ID  │
│ - REQUEST    │
│ - WEAPONS    │
│ - CANCEL     │
├──────────────┤
│ ALARM LIGHTS │
│ ● READY      │
│ ● DATA LINK  │
│ ○ ALERT      │
└──────────────┘
```

**Display Features:**
- Correlated tracks with symbols
- Track IDs and altitude blocks
- Flight path trails (computed history)
- Interceptor vectors
- Threat assessment overlays

**Use Cases:**
- **Identification Scenario:** "IFF Correlation Training" (Scenario 5)
  - Player reclassifies tracks based on IFF
  - Uses MI buttons to change track classification
  
- **Weapons Control:** "Interceptor Assignment" (Scenario 6, 7)
  - Player assigns interceptors to hostile tracks
  - Monitors engagement progress

**File:** `an_fsq7_simulator/components_v2/sd_console.py` (current implementation)

---

### Combined Workflow: Using Both Consoles

**Scenario Idea: "Full Detection Cycle"**

**Phase 1: Raw Detection (Surveillance Console)**
```
TIME: 0-60s
CONSOLE: Surveillance (LRI)
TASK: 
  1. Monitor raw radar sweeps
  2. Identify 3 new blips appearing at edge of scope
  3. Hook each blip with light gun
  4. Assign preliminary track numbers (5001, 5002, 5003)
  5. Feed to SAGE computer

EVALUATION:
  - Correct track assignment within 30 seconds?
  - Missed any contacts?
  - False alarms (hooked noise/clutter)?
```

**Phase 2: Computer Correlation (Automatic)**
```
TIME: 60-90s
DISPLAY: Transition animation showing:
  - "CORRELATING RADAR DATA..."
  - "TRACK 5001: CORRELATED (3 SITES)"
  - "TRACK 5002: CORRELATED (2 SITES)"
  - "TRACK 5003: UNCORRELATED (1 SITE)"
  
SWITCH TO: Situation Display Console
```

**Phase 3: Identification & Control (SD Console)**
```
TIME: 90-180s
CONSOLE: Situation Display (SD)
TASK:
  1. Review 3 tracks on SD (now as UNKNOWN symbols)
  2. Check IFF responses (simulated)
  3. Light gun + "CHANGE ID" MI button
     - Track 5001: FRIENDLY (positive IFF)
     - Track 5002: HOSTILE (no IFF, heading toward border)
     - Track 5003: UNKNOWN (weak IFF)
  4. Assign F-106 to Track 5002 (HOSTILE)
  5. Monitor intercept

EVALUATION:
  - Correct classification?
  - Interceptor assigned to highest threat?
  - Time to engagement?
```

---

### Technical Implementation

**State Fields:**
```python
# Console mode
console_mode: str = "situation_display"  # "surveillance" or "situation_display"

# Surveillance console state
raw_blips: List[RawBlip] = []  # Uncorrelated radar returns
sweep_angle: float = 0.0  # Rotating sweep position
sweep_speed: float = 6.0  # RPM (10 seconds per rotation)
radar_range_miles: int = 50  # Selected range scale
trail_scans: int = 7  # Number of scans to persist
hooked_blips: Set[str] = set()  # Blips operator has selected

# SD console state (already exists)
tracks: List[Track] = []  # Correlated tracks
selected_track_id: Optional[str] = None
# ... existing SD state ...
```

**JavaScript Rendering:**
```javascript
// assets/surveillance_scope.js - NEW FILE
class SurveillanceScope {
  renderRawBlips() {
    // Draw uncorrelated blips as dots
    // Fade older scans (last 7)
    // Show rotating sweep line
  }
  
  renderSweepLine() {
    // Rotating line from center
    // Clears previous blips as it passes
  }
  
  hookBlip(x, y) {
    // Light gun action: assign track number to blip
    // Send to SAGE for correlation
  }
}

// assets/crt_radar.js - EXISTING FILE (SD console)
class CRTRadarScope {
  // Already handles correlated tracks
  // Vector symbology, no sweep
}
```

**Component Files:**
```
an_fsq7_simulator/components_v2/
├── surveillance_console.py  (NEW - raw radar PPI)
├── sd_console.py           (EXISTING - situation display)
├── console_selector.py     (NEW - mode switcher)
└── ...
```

---

### Benefits of Dual Console Implementation

**Educational Value:**
1. **Show complete workflow** - From raw detection to intercept
2. **Understand radar limitations** - Why computer correlation matters
3. **Appreciate SAGE innovation** - Raw radar vs. computed air picture

**Historical Accuracy:**
1. **Two console types existed** - Not fictional, actually deployed
2. **Different operator roles** - Search vs. weapons control
3. **Workflow fidelity** - Surveillance → Computer → SD

**Gameplay/Training:**
1. **Progressive difficulty** - Start with raw detection, graduate to SD
2. **Scenario variety** - Some focus on detection, others on weapons control
3. **Realistic air defense** - Player experiences full process

---

### Scenario Examples

**Surveillance-Focused:**
- "Radar Operator Training" - Hook 10 blips correctly
- "Clutter Discrimination" - Distinguish aircraft from weather
- "High Traffic Environment" - Multiple simultaneous contacts

**SD-Focused:**
- "IFF Correlation" (Scenario 5) - Classify ambiguous tracks
- "Weapons Assignment" (Scenario 7) - Assign interceptors under pressure
- "Sector Handoff" - Transfer tracks to adjacent centers

**Combined Workflow:**
- "Full Detection Cycle" - Surveillance → SD → Intercept
- "Real-Time Integration" - Switch between consoles mid-scenario
- "Direction Center Operations" - Multi-console coordination

---

## 📚 References

- Ulmann, Bernd. *AN/FSQ-7 – The Computer That Shaped the Cold War*. Chapter 9: The SAGE Console
- IBM Display System Introduction Manual (via Ed Thelen's Nike Missile Website)
- [Ed Thelen's SAGE Console Photos](https://ed-thelen.org/comp-hist/SAGE.html)

---

## ✅ Sign-Off

This document serves as the design specification for Phase 7 refactoring to achieve historical accuracy in SAGE console controls, including both Surveillance (LRI/GFI) and Situation Display (SD) console types.

**Approved by:** AI Agent (GitHub Copilot)  
**Date:** 2025-11-15  
**Status:** Ready for implementation - Dual console mode support included
