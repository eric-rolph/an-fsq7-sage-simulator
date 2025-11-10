# SD Console Implementation

## Overview

The **SD (Situation Display) Console** is an authentic reproduction of the operator console used in the AN/FSQ-7 SAGE system for air defense operations. This implementation is based on:

1. **IBM DSP 1** (Display System Programming Manual) - Figure 9.2: Situation Display Layout
2. **Computer History Museum** photographs of actual SAGE consoles
3. Historical documentation of SAGE operator procedures

## Console Layout

### Main Components

```
┌─────────────────────────────────────────────────────────────┐
│  OFF-CENTERING PUSHBUTTONS (7 buttons across top)           │
├──────┬────────────────────────────────────────┬─────────────┤
│      │                                        │             │
│ S20  │                                        │  DD CRT     │
│ S25  │        LARGE CIRCULAR SD CRT          │  (120x120)  │
│      │           (400x400)                    │             │
│ S20  │                                        │ TELEPHONE   │
│ S21  │        • Radar Grid                    │ KEY UNITS   │
│ S22  │        • Target Tracks                 │             │
│ S23  │        • Intercept Vectors             │  ○ ○ ○      │
│ S24  │        • Light Gun Selection           │  ○ ○ ○      │
│      │                                        │  ...        │
│ S1   │                                        │ (3×6 matrix)│
│ S2   │                                        │             │
│ ...  │                                        │             │
│ S13  │                                        │             │
│      │                                        │             │
├──────┴────────────────────────────────────────┴─────────────┤
│    OPTIONS        RESET         ALARM                        │
│      ○              ○             ○                          │
│   (knob)         (knob)        (knob)                        │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

#### 1. **Large SD CRT (Main Display)**
- **Size**: 400×400 pixels (circular)
- **Function**: Primary tactical/radar display
- **Features**:
  - Radar grid with range circles (50, 100, 150 units)
  - Crosshair reference lines
  - Target tracks with IDs (TGT-1, TGT-2, etc.)
  - Intercept vectors (dashed yellow lines)
  - Green phosphor glow effect
- **Historical Context**: The actual SAGE SD CRT was ~19 inches in diameter

#### 2. **Left Side Switches**

##### Bright-Dim Switches (S20 & S25)
- **Position**: Top left
- **Function**: Control display brightness
- **Style**: Vertical toggle switches

##### Feature Selection Switches (S20-S24)
- **Count**: 5 switches
- **Function**: Select display features to show/hide
- **Style**: Horizontal toggle switches
- **Examples**: 
  - Aircraft tracks
  - Weather overlays
  - Sector boundaries
  - Altitude readouts
  - Friendly identifiers

##### Category Selection Switches (S1-S13)
- **Count**: 13 switches
- **Function**: Filter targets by category
- **Style**: Horizontal toggle switches
- **Categories** (from IBM DSP 1):
  - Unknown aircraft
  - Identified hostile
  - Identified friendly
  - Emergency tracks
  - Height-finding tracks
  - etc.

#### 3. **Off-Centering Pushbuttons**
- **Position**: Top center (above SD CRT)
- **Count**: 7 circular buttons
- **Function**: Adjust display centering/positioning
- **Style**: Circular buttons with green borders
- **Operation**: Push to shift display in various directions

#### 4. **DD CRT (Data Display)**
- **Position**: Upper right
- **Size**: 120×120 pixels
- **Function**: Alphanumeric data for selected targets
- **Display Content**:
  ```
  TGT-1001
  ALT: 25000
  SPD: 450 KTS
  HDG: 270
  ```
- **Historical Context**: Provided detailed track information

#### 5. **Telephone Key Units**
- **Position**: Right side (below DD CRT)
- **Layout**: 3 rows × 6 columns = 18 buttons
- **Function**: Direct communication lines
- **Indicators**: Dual LED lights per button (green/red)
  - **Green**: Line available
  - **Red**: Line in use
- **Usage**: Connect to other SAGE sectors, direction centers, interceptor bases

#### 6. **Control Knobs**
- **Position**: Bottom center
- **Count**: 3 rotary knobs

##### Options Knob
- **Function**: General display options/settings
- **Style**: Gray circular knob

##### Reset Knob
- **Function**: Reset display to default state
- **Style**: Gray circular knob

##### Alarm Knob
- **Function**: Acknowledge/silence alarms
- **Style**: Red/orange knob with glow effect

## Implementation Files

### `components/sd_console.py`
Main component file containing the complete SD console layout.

**Key Features**:
- Responsive layout using Reflex boxes
- SVG-based radar display
- Authentic SAGE green phosphor styling
- Hover effects on interactive elements
- Component composition for reusability

**Code Structure**:
```python
def sd_console() -> rx.Component:
    """
    Render the authentic SD console.
    
    Returns complete console with:
    - Large circular SD CRT
    - Feature/category switches
    - Telephone key matrix
    - Control knobs
    """
```

### Integration in `an_fsq7_simulator.py`

```python
# Import the SD console component
from .components.sd_console import sd_console

# Add to layout (full width, below main simulator)
rx.box(
    rx.divider(...),
    sd_console(),
    width="100%",
    padding="10px 20px",
)
```

## Historical Accuracy

### References Used

1. **IBM DSP 1 Manual** - Figure 9.2
   - Exact switch numbering (S1-S25)
   - Console dimensions and layout
   - Control descriptions

2. **Computer History Museum Photos**
   - Physical console appearance
   - CRT characteristics
   - Control knob styling
   - Overall color scheme (gray/green)

3. **Wikipedia**: AN/FSQ-7
   - System architecture context
   - Operator procedures
   - Console variations

### Authentic Details

✅ **Correct**:
- Switch numbering matches IBM documentation
- Layout proportions from museum photos
- Green phosphor CRT aesthetic
- Telephone key matrix (3×6 = 18 keys)
- Three control knobs at bottom
- Circular SD CRT design
- Small rectangular DD CRT

⚠️ **Approximated**:
- Exact CRT curvature (museum photos show slight curve)
- Physical knob textures
- Switch toggle mechanisms
- Telephone key LED brightness

## Visual Styling

### Color Palette

- **Primary Green**: `#00FF00` (phosphor glow)
- **Dark Background**: `#001100` to `#003300` (console surface)
- **Alarm Red**: `#FF6600` (warning states)
- **Data Cyan**: `#00FFFF` (secondary information)
- **Gray**: `#666` to `#888` (labels and inactive elements)

### Effects

1. **Phosphor Glow**:
   ```css
   box-shadow: inset 0 0 40px rgba(0, 255, 0, 0.3),
               0 0 20px rgba(0, 255, 0, 0.5)
   ```

2. **CRT Gradient**:
   ```css
   background: radial-gradient(
     circle at 45% 45%,
     rgba(0, 80, 0, 0.4),
     rgba(0, 20, 0, 0.9)
   )
   ```

3. **Switch Hover**:
   ```css
   _hover: {
     background: "linear-gradient(90deg, #004400 0%, #002200 100%)"
   }
   ```

## Future Enhancements

### Interactive Features (Phase 2)

1. **Clickable Switches**
   - Toggle feature visibility on SD CRT
   - Category filtering of targets
   - Brightness adjustment

2. **Light Gun Simulation**
   - Click-to-select targets on SD CRT
   - Update DD CRT with selected target data
   - Trigger intercept assignment

3. **Telephone Key Animation**
   - Click to "call" different sectors
   - Simulate communication delays
   - Visual/audio feedback

4. **Radar Sweep Animation**
   - Rotating sweep line
   - Fade-out trails for persistence
   - Real-time target movement

5. **DD CRT Updates**
   - Auto-update when target selected
   - Show multiple data pages
   - Alert messages

### Advanced Features (Phase 3)

1. **Multi-Console Simulation**
   - Multiple SD consoles in parallel
   - Coordinate between operators
   - Show sector handoffs

2. **Historical Scenarios**
   - Cuban Missile Crisis timeline
   - Training exercises
   - Intercept missions

3. **Performance Metrics**
   - Track operator response time
   - Intercept success rates
   - Communication efficiency

## Usage

### Running the Simulator

```bash
cd an-fsq7-sage-simulator
pip install -r requirements.txt
reflex init
reflex run
```

Navigate to `http://localhost:3000` and the SD console will appear below the main simulator panels.

### Testing the Console

1. **Power On System**: Click "POWER ON" button
2. **Wait for Warmup**: Tubes warm up (~2 seconds)
3. **View SD Console**: Scroll to bottom of page
4. **Observe**:
   - Large circular CRT with target tracks
   - DD CRT showing target data
   - All switches and controls laid out authentically

## Credits

- **Implementation**: Based on historical SAGE documentation
- **Design Reference**: IBM DSP 1 (Display System Programming Manual)
- **Visual Reference**: Computer History Museum SAGE console photographs
- **Historical Context**: "Computer: A History of the Information Machine" by Martin Campbell-Kelly
- **Technical Specs**: Ulmann's "Analog and Hybrid Computer Programming"

## License

This implementation is part of the AN/FSQ-7 SAGE simulator project, created for educational and historical preservation purposes.

---

**Last Updated**: November 10, 2025
**Commit**: 9f00491a5e566c411749657aad41cf36b878223e
**Component File**: `an_fsq7_simulator/components/sd_console.py` (21,555 bytes)
