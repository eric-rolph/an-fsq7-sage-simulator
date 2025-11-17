# SAGE Display System - Manual Review Findings

**Document Source**: C702-416L-ST Situation Display Generator Element Manual (Page 0440+)

**Review Date**: January 11, 2025

**Purpose**: Extract authentic display specifications to correct our simulator implementation

---

## Key Areas for Manual Review

Based on the SAGE Situation Display Generator Element manual, we need to focus on these critical sections starting from page 0440:

### 1. Display Generation Architecture

**What to look for:**
- How the display generator creates visual information
- Timing/refresh specifications
- Coordinate transformation system
- Display resolution and scanning

**Questions:**
- What is the actual display refresh rate?
- How are tracks plotted (point-by-point, vector drawing)?
- What coordinate system is used (polar, rectangular, Lambert projection)?

### 2. Track Symbology Standards

**What to look for:**
- Official symbol specifications for each track type
- Symbol dimensions and proportions
- Data block format and positioning
- Track identification encoding

**Critical Details:**
- Friendly vs Hostile vs Unknown symbols
- Aircraft type indicators
- Missile/weapon symbols
- Correlation status indicators
- Height/altitude display

### 3. Data Block Format

**What to look for:**
- Information displayed alongside tracks
- Text formatting and font specifications
- Data update rates
- Priority of information display

**Expected Content:**
- Track ID/call sign
- Altitude
- Speed
- Heading
- Track classification
- Time stamps

### 4. Geographic Overlays

**What to look for:**
- Available map layers
- Coastline detail level
- Sector boundary display
- Range/bearing grids
- Map projection system

### 5. Operator Interaction

**What to look for:**
- Light gun operation specifications
- Target selection feedback
- Cursor/crosshair display
- Action confirmation indicators

### 6. Display Intensity & Brightness

**What to look for:**
- Brightness control mechanism
- Intensity levels for different elements
- Phosphor persistence specifications
- Automatic gain control

---

## Current Implementation Questions

Based on our current simulator, we need answers to:

### Track Display

1. **Are we using the correct symbols?**
   - Current: Circle (friendly), Square (hostile), Diamond (unknown), Triangle (missile)
   - Need: Official SAGE symbology from manual

2. **Data block positioning correct?**
   - Current: Positioned near track symbol
   - Need: Exact offset and formatting rules

3. **Track correlation display**
   - Current: Solid vs dashed outlines
   - Need: Official indication method

### Refresh Cycle

1. **Is 2.5 seconds accurate?**
   - Current implementation: 2.5-second computer refresh, 60fps phosphor decay
   - Need: Verify against manual specifications

2. **How does the display drum work?**
   - Current: Simulated drum buffer with persistence
   - Need: Authentic operation description

### Coordinate System

1. **What projection is used?**
   - Current: Simple normalized 0.0-1.0 coordinates
   - Need: Authentic SAGE coordinate transformation

2. **Range calculations**
   - Current: Pixel-based estimation
   - Need: Actual range/distance measurement system

### Geographic Features

1. **Network station display**
   - Current: Priority 6 implementation with station symbols
   - **Question**: Were network stations displayed on operator scopes at all?
   - Need: Verify this feature existed in authentic system

2. **Coastline detail**
   - Current: Simple coastline overlay
   - Need: Actual coastline data format and detail level

---

## Manual Sections to Prioritize

When reviewing the manual starting at page 0440, focus on:

### CRITICAL (Fix Immediately)
1. Track symbol specifications
2. Data block format
3. Display refresh timing
4. Coordinate transformation

### HIGH (Important for Accuracy)
1. Light gun interaction
2. Geographic overlay format
3. Brightness/intensity control
4. Track correlation indicators

### MEDIUM (Nice to Have)
1. Sector boundaries
2. Range/bearing grids
3. Off-centering limits
4. Zoom specifications

---

## Implementation Impact Analysis

### If Manual Shows We're Wrong About...

**Track Symbols**:
- Impact: Medium - Need to update symbol drawing code
- Files: `assets/crt_radar.js`, `an_fsq7_simulator/sim/models.py`
- Effort: 1-2 days

**Data Blocks**:
- Impact: High - Major UI change
- Files: UI components, CRT rendering
- Effort: 3-5 days

**Refresh Cycle**:
- Impact: High - Core rendering loop
- Files: `assets/crt_radar.js`
- Effort: 2-3 days

**Coordinate System**:
- Impact: Critical - Fundamental rewrite
- Files: All position calculations
- Effort: 1-2 weeks

**Network Station Display**:
- Impact: Variable - May need to remove entire feature
- Files: `components_v2/network_stations.py`, related handlers
- Effort: If removal needed, 1-2 days

---

## Next Steps

### Phase 1: Manual Reading (IMMEDIATE)
1. Read pages 0440+ thoroughly
2. Take detailed notes on each display specification
3. Capture any diagrams or schematics
4. Note differences from current implementation

### Phase 2: Documentation (1-2 days)
1. Document authentic display system behavior
2. Create comparison table: Current vs Authentic
3. List all required changes with priorities
4. Estimate effort for each change

### Phase 3: Implementation Planning (2-3 days)
1. Prioritize changes by impact and accuracy importance
2. Group related changes
3. Create implementation roadmap
4. Set up test cases for validation

### Phase 4: Corrections (Variable)
1. Start with critical inaccuracies
2. Test each change thoroughly
3. Validate against manual specifications
4. Compare with historical photos/videos if available

---

## Validation Methods

After making corrections, validate against:

1. **Manual Specifications**: Direct comparison with documented behavior
2. **Historical Photos**: SAGE control room photographs
3. **Historical Videos**: SAGE demonstration footage
4. **Veteran Accounts**: First-hand descriptions from operators
5. **Other Simulators**: Compare with other SAGE recreation projects

---

## Documentation Requirements

For each finding from the manual, document:

1. **Page Number**: Where specification was found
2. **Section Title**: What section describes it
3. **Specification**: Exact requirement or description
4. **Current Implementation**: How we do it now
5. **Required Change**: What needs to change
6. **Impact**: Effect on existing code
7. **Priority**: Critical/High/Medium/Low

---

## Outstanding Questions

These questions should be answered by manual review:

### Display Technology
- [ ] What is the exact CRT type? (Confirm P14 phosphor)
- [ ] What is the actual screen size? (Confirm 19")
- [ ] What is the display resolution?
- [ ] What is the refresh rate?

### Track Representation
- [ ] Are symbols drawn as vectors or bitmaps?
- [ ] What line widths are used?
- [ ] How are multiple tracks distinguished when overlapping?
- [ ] What happens during track handoff between sectors?

### Data Display
- [ ] What information is always visible vs. on-demand?
- [ ] How are alerts/warnings displayed?
- [ ] What audio cues accompany visual displays?
- [ ] How are height/speed/heading encoded?

### Operator Workflow
- [ ] What is the exact light gun selection sequence?
- [ ] How are multiple targets selected?
- [ ] What visual feedback confirms actions?
- [ ] How are errors indicated?

---

## Risk Assessment

**Risk**: We've implemented significant features (Priority 1-6) without manual verification

**Mitigation**:
1. Review manual ASAP
2. Prioritize corrections by impact
3. Don't remove working features unless clearly wrong
4. Document all changes and rationale

**Opportunities**:
- Improve authenticity significantly
- Catch inaccuracies early
- Build more defensible simulator
- Learn actual SAGE system operation

---

## Status: AWAITING MANUAL REVIEW

**Next Action**: Read C702-416L-ST manual pages 0440+ and document findings

**Assigned To**: Development team

**Due Date**: ASAP - Should be completed before implementing Priority 7

**Deliverable**: Updated version of this document with specific findings and required changes
