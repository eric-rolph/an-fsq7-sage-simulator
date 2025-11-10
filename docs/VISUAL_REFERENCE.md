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
