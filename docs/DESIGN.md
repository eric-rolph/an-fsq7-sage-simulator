# AN/FSQ-7 SAGE Simulator - Design Document

## Historical Context & Authenticity

### The Real AN/FSQ-7

The AN/FSQ-7 was developed by IBM and deployed as part of SAGE (Semi-Automatic Ground Environment) from 1958-1983. Key specifications:

- **Physical Size:** 2 stories tall, 22,000 sq ft floor space, 250 tons
- **Computing Power:** 58,000 vacuum tubes, 256 flip-flop registers
- **Memory:** 
  - Magnetic core: 64K 32-bit words (256 KB in modern terms)
  - Magnetic drum: 150K words secondary storage
- **Power:** 3 megawatts (enough to power a small town)
- **Cooling:** Required massive HVAC systems
- **MTBF:** Mean time between failures measured in minutes due to tube failures
- **Cost:** $30 million per installation (1958 dollars)

### Operator Console Design

Each SAGE direction center had approximately 24 operator consoles featuring:

1. **Display Tube:** 19-inch round CRT with P7 phosphor (green)
2. **Light Gun:** Photo-sensitive stylus for pointing at display
3. **Control Panel:** Switches, buttons, and indicator lights
4. **Alphanumeric Keyboard:** For command entry
5. **Telephone Handset:** For coordination with other sites

## Simulation Design Philosophy

### What We Simulate Accurately

1. **Visual Aesthetics**
   - Green phosphor CRT glow with decay
   - Scan line artifacts
   - Period-appropriate typography (monospace)
   - Control panel layout and styling

2. **Operational Workflow**
   - System startup sequence (tube warm-up)
   - Light gun target selection
   - Display mode switching
   - Manual override capabilities
   - Intercept assignment workflow

3. **System Behavior**
   - Vacuum tube statistics and failures
   - Memory utilization patterns
   - Radar target tracking and movement
   - Real-time status updates

### What We Simplify

1. **Programming Model**
   - Real SAGE: Assembly language with job scheduling
   - Simulator: High-level Python state management

2. **Radar Data Processing**
   - Real SAGE: Complex correlation and filtering algorithms
   - Simulator: Simple random target generation

3. **Network Coordination**
   - Real SAGE: Connected to 100+ radar sites and other centers
   - Simulator: Standalone operation

## Technical Architecture

### Component Hierarchy

```
App (FSQ7State)
├── Title Bar
│   ├── System Name
│   └── Status Badge
├── Main Content (HStack)
│   ├── Left Panel (Control & Status)
│   │   ├── Control Panel
│   │   │   ├── Power Control
│   │   │   ├── Manual Override
│   │   │   ├── Intercept Mode
│   │   │   ├── Display Mode
│   │   │   └── Console Status
│   │   └── System Status
│   │       ├── Tube Status
│   │       ├── Memory Status
│   │       └── Mission Data
│   ├── Center Panel (Display & Radar)
│   │   ├── CRT Display
│   │   │   ├── Canvas (WebGL)
│   │   │   ├── Display Overlay
│   │   │   ├── Scan Lines
│   │   │   └── Vignette
│   │   └── Radar Scope
│   │       ├── Target Table
│   │       └── Statistics
│   └── Right Panel (Memory)
│       └── Memory Banks
│           ├── Core Memory Stats
│           ├── Bank Grid
│           └── Drum Storage
└── Status Bar
    ├── Mission Time
    ├── Tube Count
    ├── Target Count
    └── Intercept Count
```

### State Management Flow

```
User Action (Event)
    ↓
Event Handler (Python)
    ↓
State Update (FSQ7State)
    ↓
Reflex Compilation
    ↓
React Component Update
    ↓
Browser Render
```

### Real-time Simulation Loop

```python
async def update_simulation(self):
    while True:
        await asyncio.sleep(0.05)  # 20 FPS
        
        # Update mission clock
        # Move radar targets
        # Simulate tube failures
        # Update memory cycles
        # Yield state changes to frontend
```

## CRT Display Technology

### Phosphor Effects

The P7 phosphor used in SAGE displays had these characteristics:
- **Color:** Green (525nm wavelength)
- **Persistence:** Medium-short (microseconds)
- **Brightness:** High initial, exponential decay
- **Ghosting:** Minimal with proper refresh rate

Our simulation uses CSS to approximate:
```css
color: #00FF00
text-shadow: 0 0 10px #00FF00
box-shadow: inset 0 0 20px rgba(0, 255, 0, 0.3)
```

### Scan Line Rendering

Period CRTs displayed visible horizontal scan lines:
```css
background: repeating-linear-gradient(
    0deg,
    transparent 0px,
    transparent 2px,
    rgba(0, 0, 0, 0.3) 2px,
    rgba(0, 0, 0, 0.3) 4px
)
```

### Light Gun Technology

Real SAGE light guns worked by:
1. Detecting the CRT electron beam timing
2. Correlating beam position with display coordinates
3. Sending position data back to computer

Our simulation:
1. Uses standard mouse click events
2. Calculates screen coordinates
3. Checks proximity to displayed targets
4. Updates selection state

## Future Enhancements

### Planned Features

1. **Enhanced WebGL Rendering**
   - True phosphor decay simulation
   - Beam sweep animation
   - Screen curvature distortion
   - Color fringing at edges

2. **Sound Design**
   - Vacuum tube hum
   - Cooling fan noise
   - Alarm bells
   - Teleprinter sounds
   - Relay clicking

3. **Historical Scenarios**
   - 1960s Soviet bomber scenarios
   - Cuban Missile Crisis timeline
   - Training exercises
   - Equipment failure scenarios

4. **Advanced Simulation**
   - Real radar physics (signal processing)
   - Weather effects on tracking
   - ECM (Electronic Counter Measures)
   - Multi-site coordination

5. **Educational Features**
   - Guided tours
   - Historical documentation viewer
   - Operator training mode
   - Quiz/challenge scenarios

### Technical Debt & Improvements

1. **Performance Optimization**
   - Current: Full state updates every frame
   - Goal: Delta-based updates for efficiency
   - Target: 60 FPS on modest hardware

2. **WebGL Shaders**
   - Implement true CRT shader effects
   - Add post-processing pipeline
   - Support for different phosphor types

3. **Mobile Support**
   - Touch-friendly light gun
   - Responsive layout for tablets
   - Simplified UI for small screens

4. **Multiplayer Architecture**
   - WebSocket state synchronization
   - Multiple operator roles
   - Collaborative target tracking
   - Voice chat integration

## Research Resources

### Primary Sources

1. **SAGE System Documentation**
   - MIT Lincoln Laboratory Archives
   - IBM SAGE Programming Manual (1960)
   - Air Defense Command Operations Manual

2. **Photographs and Video**
   - Computer History Museum collection
   - National Archives SAGE imagery
   - USAF Historical Research Agency

3. **Interviews and Oral Histories**
   - SAGE operator testimonials
   - IBM engineer interviews
   - Air Force officer accounts

### Secondary Sources

1. **Books**
   - "The SAGE Air Defense System" by Hughes Aircraft
   - "Computing's Cold War" by Nathan Ensmenger
   - "Digital Defense" by Claude Baum

2. **Academic Papers**
   - IEEE Annals of Computing History
   - ACM SIGARCH Computer Architecture News
   - Journal of Strategic Studies

3. **Websites**
   - Computer History Museum SAGE exhibit
   - Wikipedia SAGE & AN/FSQ-7 articles
   - VintageTech forums

## Design Decisions

### Why Reflex?

Chosen for:
- **Python-first:** No need for JavaScript
- **Real-time state:** Built-in WebSocket updates
- **Component system:** Reusable UI elements
- **Type safety:** Static typing support
- **Deployment:** Easy hosting options

Trade-offs:
- Larger bundle size vs pure React
- Python backend required vs static site
- Learning curve for Reflex-specific patterns

### Why Green CRT Aesthetic?

Authentic to period:
- P7 phosphor was standard in 1950s-60s
- Green provided best contrast and eye comfort
- Instantly recognizable as vintage computing
- Strong association with SAGE system

### Why Real-time Updates?

Matches operational reality:
- SAGE processed data in real-time
- Operators needed immediate feedback
- Simulation feels more authentic
- Demonstrates concurrent programming concepts

## Conclusion

This simulator aims to be:
1. **Educational:** Teach computing history
2. **Authentic:** Capture the SAGE experience
3. **Accessible:** Run in any modern browser
4. **Extensible:** Easy to add features
5. **Performant:** Smooth on modest hardware

The AN/FSQ-7 represents a pivotal moment in computing history—when computers transitioned from batch processing to interactive real-time systems. This simulator preserves that legacy for future generations to explore and understand.
