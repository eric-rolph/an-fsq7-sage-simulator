# AN/FSQ-7 SAGE Simulator - Visual Layout

This document provides ASCII art representations of the simulator's user interface layout.

## Main Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  AN/FSQ-7 SAGE COMPUTER SIMULATOR                           [OPERATIONAL]       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────┬─────────────────────────────────────────────┬──────────────────────┐
│              │                                         │                      │
│  CONTROL     │           CRT DISPLAY                   │   MEMORY BANKS       │
│  PANEL       │    ╔═══════════════════════╗            │                      │
│              │    ║                       ║            │  MAGNETIC CORE       │
│ ┌──────────┐ │    ║     ◉   ◉    ◉       ║            │  MEMORY              │
│ │ POWER ON │ │    ║   ◉      ◉           ║            │                      │
│ │  (GREEN) │ │    ║       ◉              ║            │  Capacity: 65,536    │
│ └──────────┘ │    ║  ◉        ◉     ◉    ║            │  In Use: 29,450      │
│              │    ║     ◉   ◉            ║            │  Cycles: 1,234,567   │
│ [■] MANUAL   │    ║                       ║            │                      │
│     OVERRIDE │    ║   Range Rings         ║            │  ████████░░  45%     │
│              │    ║   └─────────┘         ║            │                      │
│ [■] INTERCEPT│    ║                       ║            │  BANK STATUS         │
│     MODE     │    ╚═══════════════════════╝            │  ┌──┬──┬──┬──┐      │
│              │    [RADAR][TACTICAL][STATUS][MEMORY]    │  │B0│B1│B2│B3│      │
│ ┌──────────┐ │    Brightness: ─────◉────── 75%        │  ├──┼──┼──┼──┤      │
│ │ DISPLAY  │ │                                         │  │B4│B5│B6│B7│      │
│ │  MODE:   │ │─────────────────────────────────────────│  ├──┼──┼──┼──┤      │
│ │  RADAR   │ │                                         │  │B8│B9│BA│BB│      │
│ └──────────┘ │    RADAR TRACKING                       │  ├──┼──┼──┼──┤      │
│              │    ┌──────────────────────────────────┐ │  │BC│BD│BE│BF│      │
│  CONSOLES    │    │ ID     TYPE   ALT    SPD   THR   │ │  └──┴──┴──┴──┘      │
│  Active: 8/24│    ├──────────────────────────────────┤ │                      │
│  ████░░░░░░  │    │TGT-1001 ACFT  35000  450  HIGH   │ │  DRUM STORAGE        │
│              │    │TGT-1002 MISS  45000  800  HIGH   │ │  ● ROTATING          │
│ ┌──────────┐ │    │TGT-1003 FRND  20000  300  LOW    │ │  12,000 RPM          │
│ │ SYSTEM   │ │    │TGT-1004 UNKN  15000  220  MED    │ │                      │
│ │ STATUS   │ │    └──────────────────────────────────┘ │                      │
│ └──────────┘ │                                         │                      │
│              │    Tracked: 12  Intercepts: 3  OK: 2   │                      │
│ Tubes:       │                                         │                      │
│ 58000/58000  │                                         │                      │
│              │                                         │                      │
│ Failed: 3    │                                         │                      │
│              │                                         │                      │
│ Temp: 245°C  │                                         │                      │
│              │                                         │                      │
└──────────────┴─────────────────────────────────────────────┴──────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────────┐
│ MISSION: 02:34:12  │ TUBES: 57997/58000  │ TARGETS: 12  │ INTERCEPTS: 3      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Color Scheme

**Primary Colors:**
- **Green (#00FF00)**: Primary UI, text, borders (authentic P7 phosphor)
- **Yellow (#FFFF00)**: Warnings, selected items, data highlights
- **Red (#FF0000)**: Critical alerts, high threats, errors
- **Cyan (#00FFFF)**: Memory indicators, secondary info
- **Orange (#FF8800)**: Medium threats, caution states

**Backgrounds:**
- **Black (#000000)**: Primary background
- **Dark Green (rgba(0, 20, 0, 0.5))**: Panel backgrounds
- **Very Dark (rgba(0, 0, 0, 0.8))**: Overlays

## Typography

- **Font Family**: Courier New, monospace
- **Headings**: Bold, larger sizes
- **Body Text**: Regular weight, 11-12px
- **Display Text**: 14-16px for readability
- **Data Labels**: 10-11px, uppercase

## Effects & Styling

**Glow Effects:**
```css
text-shadow: 0 0 10px #00FF00
box-shadow: 0 0 20px rgba(0, 255, 0, 0.3)
```

**Scan Lines:**
```css
background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 2px,
    rgba(0, 0, 0, 0.3) 2px,
    rgba(0, 0, 0, 0.3) 4px
)
```

**Vignette:**
```css
box-shadow: inset 0 0 100px rgba(0, 0, 0, 0.8)
```
## Vector CRT Display Language (Situation Display)

The radar/situation scope is modeled as a **vector CRT** with long-persistence P14-like phosphor, not as a modern raster game HUD.

### 2.1 Visual primitives

All content drawn on the scope uses a small set of **stroke-based primitives**:

- **Points / blips** – single-pixel or tiny cross strokes with bloom.
- **Lines / vectors** – straight segments for:
  - Intercept vectors
  - Track velocity arrows
  - Cross-range / bearing lines
- **Arcs / circles** – range rings and altitude circles.
- **Polyline outlines** – coastlines, corridors, sector boundaries.
- **Vector text glyphs** – minimal monoline characters (ID labels, numeric readouts) built from short strokes.

No filled shapes on the CRT itself; fill is reserved for UI chrome around the scope.

### 2.2 Phosphor behavior & afterglow

We approximate the P14 long-persistence tube described in Ulmann: a short bright flash followed by a dim orange afterglow that fades over several seconds.

Rules:

- **Frame refresh flash**
  - Every simulated “frame” (≈ 2–3 s of sim time), the scope briefly shows a brighter “draw pass” as all vectors are re-written.
  - This can be a **single animation frame** where strokes jump to ~150–200% brightness, then drop back.
- **Afterglow**
  - Strokes decay smoothly over ~5–8 s.
  - Fresh data (latest track position, new hits) is brighter; older trail segments are dimmer.
  - Trail length is configurable in settings (short/medium/long persistence) for usability.

Implementation hint (for WebGL/Reflex):
- Keep a **phosphor buffer** for the scope where each frame:
  - Multiply existing color by a decay factor (e.g., 0.90–0.95).
  - Add newly rendered strokes with additive blending.
- The result gives you natural-looking “ghost tails” and burn-in without manual per-track trail logic.

### 2.3 Line weight & hierarchy

Because the display is stroke-only, **line weight and brightness** are the main hierarchy tools:

- **Map & static geometry**
  - Very thin, low-intensity strokes.
  - Coastlines, DEW/Pinetree/GCI station markers, sector boundaries.
- **Range rings & grid**
  - Slightly brighter than map, but still secondary.
- **Tracks & hits**
  - Brightest strokes; blip + short tail.
  - Selected track adds a brighter halo or double-stroke.
- **Threat state**
  - Hostile / unknown / friendly are distinguished by:
    - Stroke pattern (solid vs dashed vs dotted),
    - Shape (diamond vs circle vs square),
    - Only secondarily by color.
- **Vectors**
  - Intercept / route vectors are medium-weight, solid lines with a subtle head arrow.

### 2.4 Vector text & glyphs on the scope

Text on the CRT should feel like **stroke characters**, not UI fonts:

- Characters composed from 1px strokes aligned to a simple grid (e.g., 8×12 or 10×14 units).
- Limited character set:
  - Uppercase A–Z, digits, a few punctuation marks.
- Use vector text for:
  - Track IDs (“T27”, “B3”), short labels, range / bearing readouts at the scope edge.
- For longer text (e.g., full track table, explanations), use **digital/Typotron-style panels outside** the circular scope.

This mirrors the real SAGE split between **vector situation displays** and **Typotron digital displays**. :contentReference[oaicite:7]{index=7}

### 2.5 Motion & sweep

Even though the real SAGE vector refresh didn’t literally draw a radar sweep hand, players expect it, and it helps convey “this is radar”:

- Optionally show a **sweep arm**:
  - Dim, slow-moving radial line, rotating at a configurable period.
  - Blips can “pop” brighter as the sweep passes over them.
- Trails update on refresh, not every render tick, to suggest frame-based computer updates rather than arcade-game scans.

If the sweep is distracting, it can be toggled off in settings.

### 2.6 Sector & radar-network integration

Tie in the SAGE radar station network: DEW, Mid-Canada, Pinetree, gap-filler, GCI, etc. 

- Each contributing radar line or station can be:
  - A small icon on the periphery of the scope or in a surrounding ring.
  - A short radial “spoke” showing its coverage direction.
- When a particular radar feed drops or degrades:
  - Its icon fades or flashes.
  - Hit density from that azimuth visibly changes on the scope.

This keeps the **vector aesthetic** but makes the broader SAGE radar-station network a visible part of the display language.

## Responsive Behavior

**Desktop (>1200px):**
- 3-column layout (Control | Display | Memory)
- Full-width CRT display (800x600px)
- All panels visible

**Tablet (768px - 1200px):**
- 2-column layout (Control+Display | Memory)
- Scaled CRT display (600x450px)
- Stacked panels

**Mobile (<768px):**
- Single column layout
- Collapsible panels
- Touch-optimized controls
- Portrait/landscape adaptive

## Interaction States

**Buttons:**
- Default: Green border, dark background
- Hover: Brighter glow
- Active: Filled green background
- Disabled: Dimmed, no glow

**Switches:**
- OFF: Empty checkbox, gray
- ON: Filled checkbox, green glow
- Transition: Smooth 0.2s

**Targets:**
- Unselected: Small blip, normal color
- Hovered: Slightly larger, brighter
- Selected: Yellow highlight, label visible
- Assigned: Blinking indicator

## Accessibility Considerations

**Color Blindness:**
- High contrast ratios
- Not relying solely on color (use shapes/text too)
- Alternative color schemes possible

**Screen Readers:**
- Proper ARIA labels
- Semantic HTML structure
- Keyboard navigation support

**Low Vision:**
- Adjustable brightness slider
- Scalable UI elements
- High contrast mode option

---

These visual guidelines ensure the simulator maintains authentic period aesthetics while remaining usable on modern hardware.
