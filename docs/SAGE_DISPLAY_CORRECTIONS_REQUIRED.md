# SAGE Display System - Corrections Required

Based on authentic C702-416L-ST Situation Display Generator Element Manual analysis.

---

## 🔴 CRITICAL: Track Display Format is COMPLETELY WRONG

### Current Implementation (INCORRECT)
```
Current: Simple geometric shapes
- Circle for friendly
- Square for hostile  
- Diamond for unknown
- Triangle for missiles
```

### Authentic SAGE Display Format (CORRECT)

From **Figure 4-5: TD Tabular Track Message Format**:

```
Track displayed as CHARACTER-BASED TABULAR FORMAT:

        A1 A2 A3 A4
        B1 B2 B3 B4
        D1 D2 A5 A6
   ──>  E  ◄── Central Point (aircraft position)
        C1 C2 C3 C4

With optional VECTOR line emanating from E (central point)
```

**5 Features (A, B, C, D, E):**
- **E Feature (Point Feature)**: Central point marking aircraft PRESENT position
- **A Feature**: Track identification/classification characters (4 characters)
- **B Feature**: Track data (4 characters)
- **C Feature**: Track data (4 characters)
- **D Feature**: Track data (2 characters + 2 from A)
- **Vector**: Line showing direction and speed (length = speed, direction = heading)

**Character Display:**
- All characters are **DOT-MATRIX ALPHANUMERIC** (not geometric shapes!)
- Examples from Figure 4-8: "FPTKG", "GRB", "GR 8", "C 6"
- Each character position can show letters (A-Z) or numbers (0-9)

**Positioning (Figure 4-6, 4-10):**
- Format positioned **relative to E feature (central point)**
- Can be **above/below/left/right** of central point based on position bits
- **4 possible orientations** to avoid clutter

---

## 🔴 CRITICAL: RD (Radar) Symbol Brightness States

### From Page 0450

**Radar Messages Display TWO Brightness Levels:**

1. **PRESENT (BRIGHT)**: Current radar return - displayed brighter
2. **HISTORY (DIM)**: Previous radar returns (showing track persistence)

**Timing:**
- Symbols appear every **1/2 second on average**
- Total display pattern lasts **~2-7/8 seconds** (Figure 4-11)
- **Not a rotating sweep** - point-plotting with persistence

**Symbol Evolution (Figure 4-11):**
```
Frame 1: •                    (single bright dot)
Frame 2: ••                   (adds history, first dims)
Frame 3: •••                  (trail builds)
Frame 4: ••••                 (full trail)
Frame 5: •••••                (present + 4 history)
Frame 6: ••••••               (trail continues)
Frame 7: •••••••              (longest trail)
Frame 8: ◄──HISTORY(DIM)  PRESENT(BRIGHT)──►
```

**4 RD Symbol Types (Figure 4-12):**

Based on L14 and L15 bits:

| L14 | L15 | Meaning |
|-----|-----|---------|
| 0   | 0   | **Uncorrelated; Search or Identity 0** |
| 0   | 1   | **Correlated; Search or Identity 0** |
| 1   | 0   | **Uncorrelated; MKX or Identity 1** |
| 1   | 1   | **Correlated; MKX or Identity 1** |

The **visual symbols differ** for these 4 states (shown in Figure 4-12).

---

## 🔴 MAJOR: Vector Display System

### From Figures 4-9, 4-10, Pages 0480-0520

**Vectors Show Direction and Speed:**

- **Up to 4 vectors** can be displayed (V1, V2, V3, V4)
- **Origin**: Always at E feature (central point/aircraft position)
- **Direction**: Determined by X/Y sign bits (LS and RS of words)
- **Length**: Proportional to speed/magnitude
- **Positioning**: Vector swept in quadrant based on sign bits

**Quadrant System (Page 0520):**
```
        RS = 0
          ↑
          |
LS = 1 ←──┼──→ LS = 0
          |
          ↓
        RS = 1

Quadrant I:   LS=0, RS=0  (NE)
Quadrant II:  LS=1, RS=0  (NW)
Quadrant III: LS=1, RS=1  (SW)
Quadrant IV:  LS=0, RS=1  (SE)
```

**Vector Components (Figure 4-9):**
- Each vector has **(X,Y) coordinates** relative to central point
- **G character group** positioned at end of 4th vector
- Multiple vectors show **track history, projected path, or intercept vectors**

**Important Constraint:**
- Vectors **cannot cross through the character format**
- Circuitry prevents 4th vector from crossing G characters

---

## 🟡 MODERATE: Display Timing and Refresh

### Current Implementation
- 2.5-second refresh cycle with continuous 60fps phosphor decay
- Computer updates display drum every 2.5 seconds

### Authentic SAGE (Page 0450)

**Two Display Cycle Types:**

1. **RD (Radar Display) Portion:**
   - Duration: **60 microseconds per message**
   - Shows **present radar returns + 7 history positions**
   - 9 RD drum fields (8 displayed, 1 being written)

2. **TD (Track Display) Portion:**
   - Duration: **1040 microseconds per message**
   - Shows **correlated track with tabular format + vector**
   - 6 TD drum fields

**Update Pattern:**
- RD symbols: Every **~1/2 second** (staggered, not synchronized)
- TD tracks: Updated as computer processes
- Display uses **rotating drum buffers** (fields rotated as one is written)

**Our 2.5-second cycle is APPROXIMATELY CORRECT** but details differ:
- ✅ We have persistence/history trails
- ✅ We have drum-based buffering concept
- ❌ Need to differentiate RD vs TD message types
- ❌ Need bright/dim distinction for present/history

---

## 🟡 MODERATE: Feature Selection Switches

### From Page 0470, Figure 9.2

**Console Has Feature Selection Switches (S16-S19, S20-S24):**

**Current Implementation:**
- S20-S24 for overlays (flight paths, range rings, coastlines, callsigns, intercepts)
- These match the manual! ✅

**From Manual (Page 0470):**
- **Operator can suppress individual features** (A, B, C, D, E)
- With selection switches, operator controls which character groups appear
- **Exception**: A and F features cannot both display simultaneously

**Our Current System:**
- ✅ Has category/feature selection switches
- ✅ Matches console layout (Figure 9.2)
- ⚠️ Need to add per-feature (A/B/C/D/E) suppression capability

---

## 🟡 MODERATE: Track Message Character Content

### From Figure 4-8: TD Tabular Information Message Displays

**Example Track Display:**
```
F P T K G     (5 characters shown)
G R B         (3 characters)
G R  8        (3 characters with space)
C  6          (2 characters with space)
```

**What These Mean:**
- **Letters**: Track identification codes
- **Numbers**: Likely altitude (in thousands), speed, heading sectors
- **Spaces**: Empty character positions

**Character Groups (from Page 0470):**
- Each "feature" (A, B, C, D) contains specific information
- **E feature** = point (central position)
- **A, B, C, D features** = alphanumeric data about the track
- Track number, velocity, altitude data encoded in these characters

**Our Implementation Needs:**
- Generate proper **alphanumeric character codes** for each track
- Display characters as **dot-matrix text** (not filled shapes)
- Position character groups **around central point**

---

## 🟢 MINOR: What We Got Right

### 1. Console Layout ✅
- Our switch arrangement matches Figure 9.2
- Category selection (S1-S13) correct
- Feature selection (S20-S24) correct
- Brightness controls present

### 2. CRT Display Characteristics ✅
- Phosphor persistence/afterglow
- Vector-based drawing
- Monochrome display
- Refresh cycling concept

### 3. Geographic Overlays ✅
- Coastlines, range rings correctly implemented
- Toggle capability matches manual

### 4. Off-Centering Controls ✅
- Pan/zoom/rotate controls match console design

---

## 📋 Implementation Plan

### Phase 1: CRITICAL - Track Display Overhaul (HIGH PRIORITY)

**Goal**: Replace geometric shapes with authentic tabular character format

1. **Create character rendering system**
   - Implement dot-matrix font (5x7 or 7x9 character grid)
   - Generate A-Z, 0-9 characters
   - Support for positioning text on canvas

2. **Implement tabular track format**
   - Define 5 features (A, B, C, D, E)
   - Position characters around central point (E)
   - Support 4 positioning orientations (above/below/left/right)
   - Calculate character positions based on X/Y position bits

3. **Generate track character data**
   - Create track identification codes (A feature)
   - Encode altitude, speed, heading into B, C, D features
   - Follow authentic SAGE character encoding (need more manual pages for exact format)

4. **Vector display**
   - Draw direction vector from E feature
   - Length = speed, direction = heading
   - Constrain vector to not cross character groups

### Phase 2: CRITICAL - RD Symbol Bright/Dim System

1. **Implement history trail system**
   - Track last 7 positions for each radar return
   - Display present position **bright**
   - Display history positions **dim** (progressive fade)

2. **RD symbol types**
   - Implement 4 symbol types based on correlation state
   - Different visual appearance for correlated vs uncorrelated

3. **Update timing**
   - RD symbols appear every ~0.5 seconds (staggered)
   - Full history trail ~2-3 seconds

### Phase 3: MODERATE - Display Cycle Refinement

1. **Separate RD and TD messages**
   - RD: Raw radar returns (point symbols with history)
   - TD: Correlated tracks (tabular format with vector)

2. **Update rates**
   - Fast updates for RD portion
   - Slower updates for TD portion
   - Maintain persistence between updates

### Phase 4: MODERATE - Feature Selection System

1. **Per-feature toggle switches**
   - Add controls to suppress A, B, C, D features individually
   - Keep E feature always visible
   - Implement A/F mutual exclusion

2. **Integration with existing SD console**
   - Add to feature selection switches (S16-S19 range)

---

## 📊 Impact Assessment

### Breaking Changes
- **Track rendering system**: Complete rewrite required
- **Existing track models**: Need character data fields
- **Symbol generation**: New character-based system

### Compatibility
- **Scenarios**: Should still work (track data just displayed differently)
- **Light gun selection**: Still targets central point (E feature)
- **Interceptor assignment**: Still works with track IDs

### Authenticity Gain
- **Massive improvement** in historical accuracy
- Display will match authentic SAGE photographs/videos
- Operator experience much closer to real system

---

## 🎯 Priority Order

### Must Fix (Critical for Authenticity):
1. ✅ **Tabular track format** - This is the defining visual characteristic of SAGE
2. ✅ **Character-based display** - No more geometric shapes
3. ✅ **RD bright/dim history trails** - Essential for authentic radar display
4. ✅ **Vector display from central point** - Shows aircraft heading/speed

### Should Fix (Important):
5. ⚠️ **4 RD symbol types** - Correlation status indication
6. ⚠️ **Proper character encoding** - Track ID, altitude, speed in correct format
7. ⚠️ **Feature positioning** - 4 orientation modes to avoid clutter

### Nice to Have (Enhanced Authenticity):
8. 💡 **Feature selection switches** - Per-character-group toggle
9. 💡 **RD/TD cycle separation** - Distinct update rates
10. 💡 **Exact timing specifications** - Match 60μs/1040μs rates

---

## 📖 Additional Manual Findings (Pages 0550-0620)

### Character Generation System Architecture

**From Pages 0570-0580 - Character Matrix Display:**
- **Two sets of deflection plates** in CRT:
  1. **Selection plates**: Shape electron beam through character matrix aperture to form desired character (A-Z, 0-9)
  2. **Positioning plates**: Place character-shaped beam at correct location on screen
- **Push-pull potentiometer arrangement**: Analog voltages control beam deflection
- **Digital to analog conversion**: Position bits from computer → decoded in SDGE → analog voltages → deflection plates
- **Character matrix aperture**: Physical mask that shapes beam into character forms (not pixel-by-pixel drawing)

### Off-Centering and Expansion (Pages 0580-0620)

**Expansion Scales (Figure 4-15):**
- **X1 (NORM)**: Full display area - frame of reference
- **X2**: Displays 1/4 of X1 area (letters become 2x larger)
- **X4**: Displays 1/16 of X1 area (4x zoom)
- **X8**: Displays 1/64 of X1 area (8x zoom)

**Off-Centering Controls (Figure 4-14, 4-15):**
- **14 pushbuttons total**: 7 along top edge, 7 along left side of CRT
- **49 possible viewing areas** when in EXPD mode
- **Grid sections labeled**: ABEF, CDGH, IJMN, KLOP, etc. (16 sections in X2 expansion)
- **Independent operator control**: Each console can select different expansion/area
- **Maintenance-set CONTRACT AREA**: Determines which X1 segment visible in CNTD display

**Expansion Relays (Page 0620):**
- **26 positioning bits** from computer:
  - 13 bits for X-axis positioning
  - 13 bits for Y-axis positioning
- **Expansion switch controls** (S28, S71, S72, S73, S74):
  - S28: 3-position EXPANSION switch (CNTD/NORM/EXPD)
  - S71: CONTRACT AREA switch (X1 or X2 selection)
  - S72: SCALE switch (X1, X4, or X8 in EXPD position)
  - S73, S74: NORMAL AREA switches
- **Intensification gating**: Only messages within expanded area get intensified (bright)
- **Messages outside expanded area**: Not intensified (remain dim or invisible)

### Display System Block Diagram (Figure 4-13, Page 0560)

**Signal Flow:**
1. **Message Positioning Data** (X+Y) → Expansion/Off-Centering Relays
2. **Feature Selection** + **Category Selection** → Gate which messages display
3. **Character Selection** (from SDGE) → Deflection plates via decoders
4. **Position + Compensation** (from SDGE) → Character positioning plates
5. **Intensification Units** (#1 and #2) → Control bright vs dim display
6. **Deflection Amplifier** → **Driver** → **Deflection Yoke** → Beam positioning
7. **High Voltage Unit (HVU)** → Powers CRT cathode ray tube
8. **Convergence Coil** → Focuses electron beam

**Key Components:**
- **ΔHVU (High Voltage Unit)**: Supplies high voltage for CRT operation
- **Intensification Units**: Separate control for present (bright) vs history (dim) symbols
- **10-bit Binary Decoder**: Converts digital position to analog voltages
- **Expansion Relays**: Route only relevant messages to intensification units based on zoom level

### Console Signal Distribution (Page 0550)

**Signals to SD Consoles:**
- **7 lines - Features**: Distributed to all consoles (A, B, C, D, E features)
- **31 lines - Track Categories**: Including one test category
- **90 lines - DAB's** (Display Address Buses): Control message routing
- **Up to 45 lines - Mixed TD Category**: Supplementary drivers
- **2 lines - Mix Controls**: "Mix all categories" and "mix all DAB's"

**Console Limitations:**
- **Maximum 27 DAB's** can be routed to any single console
- Each console can **independently select** which messages to display via category/feature switches
- **CAT and DAB gates** determine if message can display at particular console

### Implementation Implications

**Our Off-Centering System:**
- ✅ We have pan controls (↑↓←→) - CORRECT
- ✅ We have zoom controls (−/+) - CORRECT concept
- ⚠️ Need **discrete zoom levels** (X1/X2/X4/X8), not continuous
- ⚠️ Need **grid-based off-centering** with labeled sections
- ⚠️ Need **intensification gating** (only show tracks in zoomed area when expanded)

**Our Character System:**
- ❌ Currently draw pixels - WRONG
- ✅ Should use **pre-formed character shapes** passed through beam deflection
- ✅ Position via **analog voltage simulation** (digital → analog conversion)
- ⚠️ Character size **does not change** with expansion (spacing changes)

**Our Display Architecture:**
- ⚠️ Need **separate intensification control** for bright/dim
- ⚠️ Need **message gating** based on expansion area
- ⚠️ Need **category/feature selection** integration with display filtering

---

## 🚀 Next Steps

1. **Read more manual pages** - Get character encoding specifications
2. **Create prototype** - Simple tabular format with test data
3. **Test rendering** - Ensure characters visible and positioned correctly
4. **Update track model** - Add character data generation
5. **Integrate with sim** - Replace current track rendering
6. **Verify with historical photos** - Compare with real SAGE displays

---

**Status**: 🔴 MAJOR CORRECTIONS REQUIRED

Our current implementation has the **console layout and controls** correct, but the **actual display format** is fundamentally wrong. SAGE used **character-based tabular displays**, not geometric shapes. This is a significant rewrite but will dramatically improve authenticity.
