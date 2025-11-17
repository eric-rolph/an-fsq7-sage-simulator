# SAGE Display System Authenticity Review

Based on: C702-416L-ST Situation Display Generator Element Manual (Page 0440+)

## Document Overview

The manual describes the **Situation Display Generator Element** used in SAGE Direction Centers. This is the subsystem responsible for generating visual information on the radar scopes that operators interact with.

---

## Current Implementation Review

### ✅ What We Got RIGHT

#### 1. **P14 Phosphor CRT Display**
- ✅ Using P14 phosphor simulation (purple flash → orange afterglow)
- ✅ Vector-based drawing (not filled HUD widgets)
- ✅ Persistence/afterglow effects
- ✅ Monochrome display (not using color coding)
- ✅ 60fps phosphor decay with 2.5-second refresh cycle

#### 2. **Track Symbology Shape-Based**
- ✅ Using different symbols for track types (circle, square, diamond, triangle)
- ✅ Shape differentiation rather than color
- ✅ Selection halos/outlines

#### 3. **Range Rings & Overlays**
- ✅ Circular range rings
- ✅ Geographic overlays (coastlines)
- ✅ Toggleable overlay system

#### 4. **Light Gun Interaction**
- ✅ Target selection via light gun
- ✅ Arm → Click → Select workflow

---

## ⚠️ What Needs CORRECTION

### Critical Issues from Manual (Page 0440+)

Based on the Situation Display Generator Element documentation, here are the key areas that need review:

#### 1. **Display Refresh & Update Cycle**

**Current Implementation:**
- We have a 2.5-second refresh cycle where the computer updates the display drum
- Phosphor decays continuously at 60fps between refreshes

**From Manual - Need to Verify:**
- Actual refresh timing from SAGE system
- How track data is buffered and displayed
- Synchronization between computer cycles and display updates

**Action Items:**
- [ ] Review page 0440+ for exact refresh cycle specifications
- [ ] Verify our 2.5-second cycle against documented timing
- [ ] Check if display drum buffer model matches authentic system

#### 2. **Track Symbol Generation**

**Current Implementation:**
- Simple geometric shapes (circle, square, diamond, triangle)
- Single-stroke outlines
- Uniform sizing

**From Manual - Need to Verify:**
- Exact symbol specifications from display generator
- Track identification code display format
- Altitude/speed data presentation
- Data block formatting and positioning

**Action Items:**
- [ ] Extract authentic track symbol specifications
- [ ] Review data block format (track ID, altitude, speed, heading)
- [ ] Verify symbol sizing and stroke width
- [ ] Check how correlated vs uncorrelated tracks differ

#### 3. **Coordinate System & Scaling**

**Current Implementation:**
- Normalized 0.0-1.0 coordinate system
- Simple center-relative positioning
- Basic off-centering/panning controls

**From Manual - Need to Verify:**
- Authentic coordinate projection system
- How geographic coordinates map to display coordinates
- Range scaling and distance measurements
- Off-centering capabilities and limits

**Action Items:**
- [ ] Review coordinate transformation specifications
- [ ] Verify range/distance calculations
- [ ] Check authentic off-centering behavior
- [ ] Validate pan/zoom constraints

#### 4. **Network Station Display**

**Current Implementation (Priority 6):**
- 25 radar stations with coverage circles
- Station symbols (△, ◇, ▽, ○, ⬟)
- Connection lines to GCI stations

**From Manual - Need to Verify:**
- Whether network stations were displayed on operator scopes
- If displayed, what format/symbology was used
- How station coverage was represented
- Data flow visualization (if any)

**Action Items:**
- [ ] Confirm if network view was part of operator display or a separate system
- [ ] Review authentic station representation
- [ ] Verify coverage circle display
- [ ] Check if this feature should exist at all on operator scopes

#### 5. **Intercept Vector Display**

**Current Implementation:**
- Blue triangles for interceptors
- Dashed lines to assigned targets
- Status-based visibility (READY/AIRBORNE/ENGAGING)

**From Manual - Need to Verify:**
- Authentic interceptor symbology
- Intercept vector line format
- Commit/launch point indicators
- Engagement zone display

**Action Items:**
- [ ] Extract authentic interceptor symbol specifications
- [ ] Review intercept vector display format
- [ ] Verify engagement visualization
- [ ] Check weapon system range indicators

#### 6. **Geographic Overlays**

**Current Implementation:**
- Simple coastline overlay
- Toggle on/off capability
- Low-intensity strokes

**From Manual - Need to Verify:**
- What geographic features were available
- How overlays were generated and stored
- Overlay detail levels and selection
- Map projection used

**Action Items:**
- [ ] Review available geographic overlay types
- [ ] Verify coastline data format
- [ ] Check if state/country boundaries were displayed
- [ ] Validate projection system

#### 7. **Display Brightness & Intensity**

**Current Implementation:**
- Simple brightness slider (0-100%)
- Preset levels (DIM/MED/BRIGHT)
- Uniform intensity adjustment

**From Manual - Need to Verify:**
- Authentic brightness control mechanism
- Intensity levels for different display elements
- Automatic gain control (if any)
- Persistence time variation with brightness

**Action Items:**
- [ ] Review brightness control specifications
- [ ] Check if different elements had different intensities
- [ ] Verify preset levels against authentic system
- [ ] Validate intensity range and granularity

---

## Immediate Actions

### Phase 1: Documentation Review (URGENT)
1. **Read pages 0440+ thoroughly** - Extract all display specifications
2. **Create detailed notes** - Document authentic display behavior
3. **Compare with current implementation** - Identify specific discrepancies
4. **Prioritize corrections** - Determine what's critical vs nice-to-have

### Phase 2: Critical Corrections
Based on what we find in the manual:
1. Fix any major inaccuracies in display behavior
2. Correct track symbology if needed
3. Adjust refresh/update cycle if timing is wrong
4. Revise coordinate system if projection is incorrect

### Phase 3: Enhanced Authenticity
1. Add missing display features
2. Refine symbol details
3. Improve data block formatting
4. Enhanced overlay accuracy

---

## Questions for Manual Review

When reading page 0440+, focus on these questions:

### Track Display
- What is the exact format of track symbols?
- How are data blocks positioned relative to track symbols?
- What information is displayed in data blocks?
- How do correlated and uncorrelated tracks differ visually?
- What happens during track correlation (visual feedback)?

### Display Timing
- What is the actual display refresh rate?
- How is data synchronized with computer cycles?
- How long do tracks persist between updates?
- Is there a sweep or just point-plotting?

### Symbology Standards
- What symbols represent different aircraft types?
- How are missiles displayed?
- What symbology indicates track status (friendly/hostile/unknown)?
- How are engagement zones shown?

### Operator Interaction
- How does light gun selection work exactly?
- What visual feedback occurs on selection?
- How are multiple tracks distinguished in dense areas?
- What cursor/crosshair system is used?

### Geographic Information
- What map overlays were standard?
- How detailed were coastlines?
- Were cities/landmarks displayed?
- How were sector boundaries shown?

---

## Implementation Impact

### Low Impact (Minor Fixes)
- Symbol size adjustments
- Brightness level tweaking
- Overlay intensity changes
- Text formatting

### Medium Impact (Feature Refinements)
- Data block format changes
- Track correlation visual feedback
- Intercept vector improvements
- Coordinate system adjustments

### High Impact (Major Rework)
- Display refresh cycle changes
- Symbol generation system overhaul
- Coordinate projection rewrite
- New display features from manual

---

## Next Steps

1. **READ THE MANUAL** - Pages 0440+ thoroughly
2. **Document findings** - Create detailed notes on authentic display system
3. **Update this document** - Fill in specific corrections needed
4. **Plan implementation** - Prioritize changes based on impact and accuracy importance
5. **Test against historical photos/videos** - Validate our corrections

---

## References

- C702-416L-ST Situation Display Generator Element Manual (Page 0440+)
- Current implementation: `assets/crt_radar.js`
- Current symbology: `an_fsq7_simulator/components_v2/` various files
- Historical reference: `docs/VISUAL_REFERENCE.md`

---

**Status:** 🔍 UNDER REVIEW - Awaiting detailed manual analysis

This document will be updated as we extract specific information from the manual and identify exact corrections needed.
