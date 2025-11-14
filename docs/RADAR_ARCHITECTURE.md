# Radar Scope Architecture

## Current Implementation (Canvas 2D)

Despite references to "WebGL" in documentation and comments, the radar scope currently uses **HTML5 Canvas 2D API** for rendering.

### Technology Stack

- **Rendering Engine**: Canvas 2D API (via `canvas.getContext('2d')`)
- **Animation**: RequestAnimationFrame loop targeting 60 FPS
- **Data Flow**: Python (Reflex State) → JSON → JavaScript → Canvas rendering
- **File**: `assets/radar_scope.js` (429 lines standalone JavaScript)

### Why Canvas 2D Instead of WebGL?

The project documentation notes: *"CSS provides 80% of visual effect with 20% effort"*

**Advantages:**
- ✅ Simpler to implement and debug
- ✅ Sufficient performance for current track counts (~50 tracks)
- ✅ Good browser compatibility
- ✅ Easier team onboarding (no shader programming required)

**Limitations:**
- ❌ No true phosphor persistence (decay effect)
- ❌ Limited post-processing capabilities (no bloom, CRT effects)
- ❌ May struggle with 200+ tracks simultaneously
- ❌ No hardware acceleration for complex effects

**Future Enhancement:** WebGL upgrade noted as "future enhancement" for advanced CRT effects.

---

## Architecture Overview

### Data Flow Pipeline

```
Python State (InteractiveSageState)
    ↓
    ├─ tracks: List[Track]           → get_tracks_json() → tracks_json_var
    ├─ active_overlays: Set[str]     → (direct access)
    └─ geo data from geographic_overlays → get_geo_json() → geo_json_var
    
    ↓ (Embedded in hidden divs with data attributes)
    
HTML Page
    ├─ <div id="sage-track-data" data-tracks="{...}">
    └─ <div id="sage-geo-data" data-geo="{...}">
    
    ↓ (Read by JavaScript via dataset attributes)
    
JavaScript (RadarScope class)
    ├─ updateTracks(tracks)          → Render loop processes
    ├─ updateGeoData(geoData)        → Cached for overlay rendering
    └─ render() @ 60 FPS              → Canvas 2D draw calls
```

### Component Files

| File | Purpose | Lines | Technology |
|------|---------|-------|------------|
| `assets/radar_scope.js` | Standalone Canvas 2D renderer | 429 | JavaScript (ES6 class) |
| `components_v2/radar_scope.py` | Reflex wrapper, HTML/CSS strings | 600 | Python + HTML templates |
| `components_v2/geographic_overlays.py` | Geographic data (coastlines, cities, rings) | 367 | Python dataclasses |
| `interactive_sage.py` | State management, JSON serialization | 943 | Reflex State class |

---

## Rendering Pipeline

### Frame Rendering Order (60 FPS)

1. **Clear Canvas** - Fill with black background (`#000000`)
2. **Apply Transforms** - Pan/zoom via Canvas 2D translate/scale
3. **Draw Geographic Overlays** (if enabled):
   - Coastlines (East Coast, Great Lakes)
   - Range rings (100mi, 200mi, 300mi from center)
   - Bearing markers (N/E/S/W)
   - City labels (BOS, NYC, PHL, DC, CHI, etc.)
4. **Draw Rotating Sweep** - 4-second rotation with radial gradient fade
5. **Draw Flight Trails** - Last 20 positions per track, alpha-faded over 5 seconds
6. **Draw Track Dots** - Color-coded by type, 5px (8px when selected)
7. **Draw Track Glow** - Shadow blur (10px normal, 20px selected)
8. **Draw Selection Rings** - 15px radius white ring around selected track
9. **Draw Track Labels** - Callsigns in 10px Courier New font (if enabled)
10. **Draw Intercept Vectors** - Blue dashed lines from interceptors to targets (if enabled)

### Color Coding

```javascript
hostile:      #ff0000  (red)
missile:      #ff00ff  (magenta)
friendly:     #00ff00  (green)
interceptor:  #0088ff  (blue)
unknown:      #ffff00  (yellow)
default:      #888888  (gray)
```

---

## Initialization Flow

### ⚠️ Known Limitation: Manual Initialization Required

**Root Cause:** Reflex's React-based architecture prevents automatic script execution:

1. **React innerHTML Security**: `rx.html()` strips `<script>` tags (XSS protection)
2. **rx.script() Doesn't Render**: No HTML output, scripts don't reach browser
3. **Vite Plugin Bypass**: React Router SSR bypasses `transformIndexHtml` hook
4. **Auto-Regeneration**: `.web/app/_document.js` regenerated on every server start

### Official Solution: Manual Browser Initialization

**Current Working Method:**
- Run server with `reflex run`
- Open browser console (F12)
- Execute: `initRadarScope('radar-scope-canvas')`
- Radar scope renders immediately and works perfectly

**Why This Works:**
- ✅ `radar_scope.js` properly served from `/assets/radar_scope.js`
- ✅ Canvas element `#radar-scope-canvas` exists in DOM
- ✅ Data divs (`#sage-track-data`, `#sage-geo-data`) populated with JSON
- ✅ Manual call bypasses React's security restrictions
- ✅ Animation loop starts and updates continuously

### Initialization Sequence (Manual)

1. **Page Load** - Reflex renders HTML with canvas element and hidden data divs
2. **External JS Load** - Browser fetches `/assets/radar_scope.js` automatically
3. **User Intervention** - Manual `initRadarScope()` call in browser console
4. **Scope Creation** - `new RadarScope('radar-scope-canvas')` instantiates renderer
5. **Data Loading** - Reads JSON from data attributes, calls `updateGeoData()` and `updateTracks()`
6. **Animation Start** - `requestAnimationFrame()` loop begins at 60 FPS
7. **Periodic Updates** - JavaScript polls data divs every 1 second for track updates

### Attempted Solutions (All Failed)

| Approach | Why It Failed |
|----------|---------------|
| `rx.script(src="/radar_scope.js")` | Doesn't render any HTML tags |
| `rx.html('<script src="...">...</script>')` | React innerHTML strips scripts |
| Vite plugin with `transformIndexHtml` | React Router SSR bypasses hook (never called) |
| Direct `.web/app/_document.js` modification | File auto-regenerated on every `reflex run` |

**Conclusion:** Reflex's architecture intentionally prevents script injection for security. Manual initialization is the reliable workaround until Reflex adds official script injection API.

---

## Geographic Data System

### Data Source: `geographic_overlays.py`

Contains historically accurate geographic features for northeastern US:

- **East Coast**: 17 points from Maine to Virginia
- **Great Lakes**: Simplified outlines of Superior, Michigan, Huron, Erie, Ontario
- **Cities**: 8 major cities (BOS, NYC, PHL, DC, CHI, CLE, BUF, DET)
- **Range Rings**: 100mi, 200mi, 300mi radius from center
- **Bearing Markers**: Cardinal directions (N/E/S/W)
- **Sector Boundaries**: SAGE airspace divisions

### Coordinate System

All geometry uses **normalized coordinates** (0.0 to 1.0):
- X: 0.0 = west edge, 1.0 = east edge
- Y: 0.0 = north edge, 1.0 = south edge

**Advantages:**
- Resolution-independent (scales to any canvas size)
- Simple pixel conversion: `pixelX = normalizedX * canvasWidth`
- Easy to reason about geometric relationships

### Data Structures

```python
@dataclass
class GeoPoint:
    x: float      # Normalized 0.0-1.0
    y: float
    label: str = ""

@dataclass
class GeoPolyline:
    points: List[GeoPoint]
    name: str
    style: str = "solid"  # solid, dashed, dotted
```

### JSON Serialization

Python state serializes geographic data to JSON for JavaScript consumption:

```python
def get_geo_json(self) -> str:
    return json.dumps({
        "coastlines": [
            {
                "name": "East Coast",
                "style": "solid",
                "points": [[0.85, 0.05], [0.87, 0.08], ...]
            }
        ],
        "cities": [
            {"label": "BOS", "x": 0.86, "y": 0.18}
        ],
        "range_rings": [
            {"label": "100 mi", "radius": 0.15}
        ],
        "bearing_markers": [
            {"label": "N", "x": 0.50, "y": 0.02}
        ]
    })
```

---

## Track Data System

### Track Object Schema

```javascript
{
  "id": "TGT-1001",
  "x": 0.125,              // Normalized 0.0-1.0
  "y": 0.875,
  "altitude": 25000,       // Feet
  "speed": 450,            // Knots
  "heading": 45,           // Degrees (0=East, 90=North)
  "track_type": "hostile", // hostile|friendly|unknown|missile|interceptor
  "threat_level": "HIGH",  // HIGH|MEDIUM|LOW
  "selected": false,
  "designation": "",
  "trail": [               // Last 20 positions
    [0.12, 0.87],
    [0.121, 0.871],
    ...
  ]
}
```

### Trail History System

**Dual Implementation:**
- Backend provides `trail` array (last 20 positions) in track JSON
- Frontend maintains `trailHistory` Map for fading calculations

**Trail Rendering:**
```javascript
// Fade from 0.1 (oldest) to 0.5 (newest) alpha
const alpha = (0.1 + age * 0.4) * this.brightness;

// Draw segments between consecutive points
for (let i = 0; i < trailLength - 1; i++) {
    ctx.globalAlpha = alpha;
    ctx.moveTo(trail[i][0] * width, trail[i][1] * height);
    ctx.lineTo(trail[i+1][0] * width, trail[i+1][1] * height);
}
```

**Cleanup:**
- Prune points older than 5 seconds (`trailFadeMs`)
- Limit to 20 points maximum (`maxTrailLength`)
- Remove trails when tracks disappear

---

## Interactive Features

### Light Gun (Click Detection)

**Algorithm:**
1. Convert click position to normalized coordinates (0.0-1.0)
2. Calculate Euclidean distance to each track
3. Select nearest track within 5% threshold
4. Deselect all other tracks
5. Call `onTrackClick(track)` callback (if set)

**Visual Feedback:**
- Selected tracks show 15px white selection ring
- Glow blur increases from 10px to 20px
- Track dot size increases from 5px to 8px

### Pan and Zoom

**Controls:**
- `setPan(x, y)` - Offset in pixels
- `setZoom(zoom)` - Scale factor (0.5x to 3.0x range)

**Implementation:**
```javascript
ctx.save();
ctx.translate(centerX + panX, centerY + panY);
ctx.scale(zoom, zoom);
ctx.translate(-centerX, -centerY);
// ... draw all elements ...
ctx.restore();
```

### Brightness Control

**Range:** 0.2 (dim) to 1.0 (full brightness)

**Application:**
- All colors multiplied by brightness alpha
- Glow effects scale with brightness
- Geographic overlays rendered at 30% brightness baseline

---

## Performance Characteristics

### Current Performance

- **Target:** 60 FPS
- **Tested:** Up to ~50 tracks simultaneously
- **Animation Loop:** `requestAnimationFrame()` with delta time calculation
- **Update Frequency:**
  - Tracks: 1-second intervals (Python simulation tick)
  - Rendering: 60 FPS (JavaScript render loop)
  - Sweep rotation: 4-second full rotation

### Performance Optimization Techniques

1. **Minimal Canvas Operations**
   - Single `fillRect()` clear per frame
   - Minimized `save()`/`restore()` calls
   - Pre-calculated transform matrices

2. **Trail System**
   - Cap at 20 points per track
   - Time-based pruning (5-second fade)
   - Map structure for O(1) track lookup

3. **Conditional Rendering**
   - Overlays only drawn if enabled
   - Callsigns optional (performance toggle)
   - Intercept vectors on-demand

### Known Bottlenecks (Hypothetical)

**Not Yet Measured:**
- Performance with 100+ tracks untested
- Geographic overlay complexity not benchmarked
- Trail rendering cost at scale unknown

**Potential Issues:**
- Canvas 2D arc() calls for many tracks (no batching)
- Text rendering for labels (CPU-bound)
- Trail line drawing (20 points × N tracks)

---

## CSS and Styling

### Canvas Element

```html
<canvas 
    id="radar-scope-canvas" 
    width="800" 
    height="800"
    style="
        width: 100%; 
        height: 100%; 
        background: #000000; 
        border-radius: 8px;
        image-rendering: crisp-edges;
    "
>
```

**Rendering Mode:** `crisp-edges` - Pixel-perfect rendering without anti-aliasing (authentic CRT appearance)

### Container Styling

```css
/* radar_scope.py RADAR_SCOPE_CSS */
#radar-scope-canvas {
    image-rendering: crisp-edges;
    cursor: crosshair;
}

#radar-scope-canvas:hover {
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

#radar-scope-canvas.lightgun-armed {
    cursor: crosshair;
    box-shadow: 0 0 30px rgba(0, 255, 0, 0.5);
}
```

### Animation Effects

```css
@keyframes pulse-selection {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 1.0; }
}

.track-selected {
    animation: pulse-selection 1s infinite;
}
```

---

## Future WebGL Migration Path

### Planned Enhancements (Not Yet Implemented)

See [WEBGL_MIGRATION_PLAN.md](./WEBGL_MIGRATION_PLAN.md) for detailed specifications.

**Key Improvements:**
1. **True Phosphor Persistence** - Framebuffer feedback with exponential decay
2. **CRT Screen Effects** - Barrel distortion, vignette, scanlines
3. **Bloom/Glow Post-Processing** - Separable Gaussian blur for authentic phosphor glow
4. **Instanced Rendering** - Hardware-accelerated track drawing (200+ tracks)
5. **Texture Atlases** - Efficient text/symbol rendering

**Learning Resources:**
- **WebGL2 Fundamentals** (webgl2fundamentals.org) - Modern tutorial series
- **Matsuda & Lea** - WebGL Programming Guide (OpenGL ES 2.0 in JavaScript)
- **Ghayour & Cantor** - Real-Time 3D Graphics with WebGL 2 (framebuffers, blending)
- **WebGL Insights** - Performance optimization essays (free PDF)

**Migration Strategy:**
- Keep Canvas 2D as fallback for older browsers
- Incremental feature parity (don't rewrite everything at once)
- Performance benchmarking at each stage
- Visual regression tests comparing Canvas vs WebGL output

---

## Known Issues & Limitations

### Current Issues

1. ✅ **FIXED:** Script auto-initialization broken (React innerHTML security)
   - **Solution:** Inline `rx.script()` with polling initialization
   
2. ⚠️ **PARTIAL:** Light gun backend integration
   - **Status:** Visual selection works, but Reflex state updates incomplete
   - **TODO:** Proper event bridge from JavaScript to Python state

3. ✅ **FIXED:** Geographic data not wired
   - **Solution:** `get_geo_json()` now serializes full geographic dataset

### Design Limitations

1. **No True Phosphor Decay** - Canvas 2D can't do feedback buffers (requires WebGL)
2. **No Hardware Acceleration** - CPU-bound rendering limits scalability
3. **Limited Post-Processing** - No bloom, no screen curvature (requires shader pipeline)
4. **Text Rendering Cost** - Canvas text is expensive (texture atlas would be faster)

---

## Testing & Verification

### Manual Testing Checklist

- [x] Radar scope appears on page load
- [x] Geographic overlays render (coastlines, cities, range rings)
- [x] Rotating sweep animates smoothly (4-second rotation)
- [x] Tracks appear color-coded by type
- [x] Flight trails fade over 5 seconds
- [x] Click detection selects nearest track
- [x] Selection ring appears on selected track
- [x] Console logs show initialization sequence
- [ ] Performance at 100+ tracks (not yet tested)
- [ ] Cross-browser compatibility (Chrome/Firefox/Safari/Edge)

### Console Output Verification

**Expected console messages on successful initialization:**

```
[SAGE] Inline script executing...
[SAGE] Waiting for radar_scope.js...
RadarScope initialized: radar-scope-canvas
[SAGE] initRadarScope available, initializing...
[SAGE] Radar scope initialized
[SAGE] Geographic data loaded
[SAGE] Initial tracks loaded: 12
Updated tracks: 12 tracks
Updated geo data
```

---

## Summary

**Current State:**
- ✅ Canvas 2D rendering delivering smooth 60 FPS
- ✅ Authentic phosphor green aesthetic achieved via CSS and shadows
- ✅ Geographic overlays fully wired from Python data
- ✅ Reliable initialization via inline React-safe scripting
- ✅ Interactive features (click, pan, zoom, brightness) functional

**Next Steps:**
1. Complete light gun → Reflex state event bridge
2. Performance test with 100+ tracks
3. Plan WebGL migration (optional, for advanced effects)
4. Add visual regression tests
5. Cross-browser compatibility testing

---

**Last Updated:** November 12, 2025  
**Technology:** Canvas 2D (not WebGL, despite documentation claims)  
**Performance Target:** 60 FPS @ ~50 tracks  
**Lines of Code:** ~1,567 (JS: 429, Python: 600, Geo: 367, Script: 150)
