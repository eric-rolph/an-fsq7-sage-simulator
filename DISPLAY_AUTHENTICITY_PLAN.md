# SAGE Display Authenticity Implementation Plan

**Date:** November 14, 2025  
**Sources:** Ullman dissertation pp. 166-170, Ed Thelen SAGE documentation  

---

## Historical Display Characteristics

### Situation Display (SD) Console - 19" CRT

**Phosphor Type: P14 (NOT P7)**
- **Initial flash:** Purple (when electron beam hits)
- **Afterglow:** Orange, persisting for several seconds
- **Persistence:** Long (multi-second decay)
- **Purpose:** Allow tracks to remain visible between 2.5-second refresh cycles

**P11 Phosphor** (photography consoles only):
- Bright blue flash, negligible afterglow
- For photographic recording, not operator viewing

**Display Technology:**
- **Character generation:** Stencil matrix (64 characters etched in steel plate)
- **Vector drawing:** Deflected electron beam for tracks, coastlines, range rings
- **Refresh rate:** Every 2.5 seconds (computer-driven)
- **Display size:** 19 inches diagonal
- **Brightness:** Very dim, required special lighting

### Blue Room Environment

**Lighting:**
- **Color:** Blue indirect lighting from ceiling honeycomb structure
- **Purpose:** Eliminate glare on dim phosphor screens
- **Intensity:** Low, non-glare
- **Effect:** Blue environment (initially caused vertigo concerns)
- **Benefit:** Allowed operators to work at higher light levels than pure darkness

### Visual Characteristics

**Monochrome Display:**
- **Base color:** Purple flash → orange glow (P14 phosphor)
- **No color coding:** All symbology monochrome
- **Track differentiation:** Via **symbol shapes** and **patterns**, NOT colors
  - Friendly: One symbol shape
  - Hostile: Different symbol shape
  - Unknown: Yet another symbol shape
  - Speed leaders (velocity vectors): Dashed lines
  - Heading indicators: Solid lines

**Symbology:**
- Alphanumeric characters (via stencil matrix)
- Vector tracks (electron beam deflection)
- Coastlines, range rings (vector drawing)
- Track IDs, altitude, speed (text overlays)

---

## Current Simulator Implementation Issues

### ❌ Incorrect P7 Phosphor Simulation
**Current:** Blue-white flash + green slow persistence  
**Actual:** Purple flash + orange afterglow

### ❌ Multi-Color Track Coding
**Current:** Yellow (uncorrelated), orange (correlating), green (correlated)  
**Actual:** Monochrome symbols with different **shapes**, not colors

### ❌ WebGL/Canvas Rendering
**Current:** Canvas 2D API (correct), but wrong phosphor colors  
**Actual:** Should simulate P14 purple→orange decay

### ❌ Sweep Speed
**Current:** 60-second rotation (6°/sec)  
**Actual:** No evidence of rotating sweep in Ullman text - may be PPI radar display, not SD console

### ❌ Refresh Rate
**Current:** 60 FPS continuous rendering  
**Actual:** 2.5-second refresh cycles (computer-driven updates)

---

## Implementation Status

### ✅ Phase 1: P14 Phosphor Simulation (COMPLETE)

**Updated `assets/crt_radar.js` phosphor colors:**

```javascript
// P14 Phosphor (historically accurate)
this.phosphorFast = 'rgba(180, 100, 255, 0.9)';  // Purple flash
this.phosphorSlow = 'rgba(255, 180, 100, 0.8)';   // Orange afterglow
this.phosphorPersistence = 'rgba(255, 180, 100, 0.4)'; // Fading orange trail
```

**Decay characteristics:**
- Fast purple decay (~100ms)
- Slow orange persistence (2-3 seconds visible)
- Matches "several seconds" from Ullman description

**Status:** ✅ Committed (414deea), verified via browser console

### ✅ Phase 2: Monochrome Symbol-Based Track Differentiation (COMPLETE)

**Remove color coding, add symbol shapes:**

```javascript
// Track symbols based on type (monochrome)
function drawTrackSymbol(ctx, x, y, trackType, correlationState) {
    ctx.strokeStyle = phosphorOrange; // Single color
    ctx.lineWidth = 2;
    
    // Symbol shape indicates track type
    switch(trackType) {
        case 'friendly':
            // Circle symbol
            ctx.beginPath();
            ctx.arc(x, y, 6, 0, Math.PI * 2);
            ctx.stroke();
            break;
        case 'hostile':
            // Square symbol
            ctx.strokeRect(x-6, y-6, 12, 12);
            break;
        case 'unknown':
            // Diamond symbol
            ctx.beginPath();
            ctx.moveTo(x, y-8);
            ctx.lineTo(x+8, y);
            ctx.lineTo(x, y+8);
            ctx.lineTo(x-8, y);
            ctx.closePath();
            ctx.stroke();
            break;
        case 'missile':
            // Triangle symbol (pointing up)
            ctx.beginPath();
            ctx.moveTo(x, y-8);
            ctx.lineTo(x+7, y+6);
            ctx.lineTo(x-7, y+6);
            ctx.closePath();
            ctx.stroke();
            break;
    }
    
    // Correlation state via pattern, not color
    if (correlationState === 'uncorrelated') {
        // Dashed outline for uncorrelated
        ctx.setLineDash([3, 3]);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Question mark nearby
        ctx.font = '12px monospace';
        ctx.fillStyle = phosphorOrange;
        ctx.fillText('?', x+10, y-10);
    }
}
```

### Phase 3: Blue Room Environment Simulation

**Add blue ambient lighting effect:**

```css
.radar-display-container {
    /* Blue indirect lighting simulation */
    background: radial-gradient(circle at center, 
        rgba(50, 80, 150, 0.3), 
        rgba(20, 40, 80, 0.8));
    
    /* Dim overall environment */
    filter: brightness(0.7);
}
```

**Add blue light glow to UI panels:**

```css
.control-panel, .sd-console {
    box-shadow: 0 0 20px rgba(100, 150, 255, 0.3);
    border: 1px solid rgba(100, 150, 255, 0.5);
}
```

### ✅ Phase 3: 2.5-Second Computer Refresh Cycle (COMPLETE)

**Updated render loop to simulate computer-driven updates:**

```javascript
// SAGE 2.5-second computer refresh cycle
this.lastComputerRefresh = Date.now();
this.refreshInterval = 2500; // milliseconds (historically accurate)
this.enableRefreshCycle = true; // Toggle for A/B comparison

render() {
    const now = Date.now();
    const timeSinceRefresh = now - this.lastComputerRefresh;
    
    // Phosphor decay continues at 60fps (always)
    this.applyPhosphorDecay();
    
    // Computer refreshes display every 2.5 seconds
    const shouldRefresh = this.enableRefreshCycle 
        ? (timeSinceRefresh >= this.refreshInterval)
        : true; // Continuous mode for comparison
    
    if (shouldRefresh) {
        this.updateTrackData();           // Fetch from window.__SAGE_*
        this.addSweepToPersistence();     // Write sweep to persistence layer
        this.drawTracksOnPersistence();   // Write tracks to persistence layer
        
        if (this.enableRefreshCycle) {
            this.lastComputerRefresh = now;
        }
    } else {
        // Between refreshes: only sweep decays, tracks persist via phosphor
        this.addSweepToPersistence();
    }
    
    // Composite persistence layer to main canvas (phosphor glow)
    this.ctx.drawImage(this.persistenceCanvas, 0, 0);
    
    requestAnimationFrame(() => this.render());
}
```

**Key Features:**
- Computer writes fresh track data every 2.5 seconds (matches SAGE display drum update timing)
- Phosphor persistence decays continuously at 60fps between refreshes
- Tracks remain visible via P14 orange afterglow (2-3 second persistence)
- Toggle `enableRefreshCycle` to compare authentic vs continuous (modern) mode

**Status:** ✅ Implemented, README updated with 2.5-second refresh documentation

### Phase 4: Character Matrix Simulation (Optional)

**Simulate stencil-based character rendering:**

```javascript
// Draw characters using vector outlines (simulating stencil effect)
function drawStencilChar(ctx, char, x, y) {
    ctx.strokeStyle = phosphorOrange;
    ctx.lineWidth = 1;
    ctx.font = '14px "Courier New", monospace';
    ctx.strokeText(char, x, y); // Outline only
    ctx.fillText(char, x, y);    // Then fill
}
```

---

## Design Language Updates

### README.md Section Rewrite

Replace "Vector CRT Radar Scope" section with:

```markdown
### 🎨 Authentic P14 Phosphor Situation Display

Faithful simulation of the SAGE 19" situation display console:

- **P14 Phosphor CRT**: Purple flash → orange afterglow (2-3 second persistence)
- **Monochrome Symbology**: Track types differentiated by **symbol shapes**, not colors
  - ⬤ Circle: Friendly aircraft
  - ⬛ Square: Hostile aircraft
  - ◆ Diamond: Unknown tracks
  - ▲ Triangle: Missiles
  - Dashed outlines: Uncorrelated tracks (with "?" indicator)
- **Blue Room Environment**: Dim blue ambient lighting (historically accurate)
- **2.5-Second Refresh**: Computer updates display every 2.5 seconds (persistence layer decays continuously)
- **Vector Drawing**: Coastlines, range rings, velocity vectors via electron beam simulation
- **Character Matrix**: Stencil-based alphanumeric rendering (64-character set)
- **Dim Display**: Requires simulated low-light environment for visibility
```

### agents.md Design Invariants

Add to "CRT Display" section:

```markdown
- **P14 Phosphor (NOT P7)**: Purple flash → orange afterglow
- **Monochrome symbology**: Symbol **shapes** differentiate track types (circle/square/diamond/triangle)
- **No color coding**: Real SAGE used one phosphor color with different patterns/shapes
- **Blue room lighting**: Ambient blue glow simulates authentic indirect lighting
- **2.5-second refresh**: Computer-driven updates, NOT continuous 60fps data changes
```

---

## Implementation Priority

**Phase 1 (High Priority):**
- ✅ Fix phosphor colors (purple→orange P14)
- ✅ Remove multi-color track coding
- ✅ Implement symbol shapes (circle/square/diamond/triangle)

**Phase 2 (Medium Priority):**
- ✅ Add blue room ambient lighting
- ✅ Implement 2.5-second refresh cycle
- ✅ Update README + agents.md

**Phase 3 (Low Priority):**
- ⚠️ Character matrix stencil simulation (optional polish)
- ⚠️ Rotating sweep removal (if not historically accurate)

---

## Testing Checklist

After implementation:

- [ ] Phosphor appears purple on flash, fades to orange
- [ ] Tracks use symbol shapes, not colors
- [ ] Blue ambient lighting visible in UI
- [ ] Display updates every 2.5 seconds (not continuous)
- [ ] Persistence layer decays smoothly between refreshes
- [ ] Light gun selection still works with new symbol rendering
- [ ] README accurately describes P14 phosphor + monochrome symbology
- [ ] agents.md updated with correct design invariants

---

## References

1. **Ullman, J. A. N. (2003).** *The AN/FSQ-7 Computer.* Dissertation, pp. 166-170.
   - P14 phosphor characteristics (purple flash, orange afterglow)
   - Blue room lighting environment
   - 2.5-second refresh cycles
   - Character stencil matrix (64 characters)

2. **Ed Thelen SAGE Documentation.** https://ed-thelen.org/SageIntro.html
   - Situation display layout (Figure 9.2)
   - 19" CRT display tubes
   - Light gun operation (photomultiplier tube)

3. **IBM DSP 1 Manual.** (Referenced in Ullman)
   - Display tube technical specifications
   - Character matrix stencil design (Figure 9.4)
