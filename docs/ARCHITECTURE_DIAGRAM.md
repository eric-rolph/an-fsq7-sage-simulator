# AN/FSQ-7 Architecture: Visual Comparison

## Previous Architecture (Visual Demo)

```
┌─────────────────────────────────────────────────────────────┐
│                     SAGE Simulator (Demo)                    │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │  Reflex UI   │
                    │   (Web UI)   │
                    └──────┬───────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  FSQ7State (Python)  │
                │  - Integer CPU       │
                │  - Direct I/O        │
                │  - Mouse clicks      │
                └──────────┬───────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌────────┐       ┌─────────┐      ┌──────────┐
    │ Radar  │       │  CPU    │      │ Light    │
    │ Targets│       │ (Basic) │      │ Gun      │
    │ (List) │       │ Integer │      │ (X,Y)    │
    └────────┘       └─────────┘      └──────────┘

Key Issues:
❌ Integer arithmetic (not fractional)
❌ Direct data flow (no drum buffering)
❌ Mouse coordinates (not polling)
❌ Standard CPU (not one's complement)
```

## New Architecture (High-Fidelity Emulation)

```
┌─────────────────────────────────────────────────────────────┐
│             SAGE Simulator (High-Fidelity)                   │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │  Reflex UI   │
                    │   (Web UI)   │
                    └──────┬───────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  FSQ7State (Python)  │
                │  - Fractional CPU    │
                │  - Drum I/O          │
                │  - Polling loops     │
                └──────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  FSQ7_IO_System        │
              │  (Drum + Light Gun)    │
              └────────┬───────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌───────────────┐  ┌───────────────┐  ┌──────────────┐
│ MagneticDrum  │  │   CPU Core    │  │ LightGunSys  │
│               │  │  (Fractional) │  │              │
│ ┌───────────┐ │  │               │  │ ┌──────────┐ │
│ │ LRI Field │ │  │ • One's comp  │  │ │  Armed?  │ │
│ │ GFI Field │ │  │ • Parallel    │  │ │  Flash?  │ │
│ │ XTL Field │ │  │ • Shift       │  │ │  Poll()  │ │
│ │ SDC Field │ │  │ • Fractions   │  │ └──────────┘ │
│ └───────────┘ │  └───────────────┘  └──────────────┘
│               │          │                   │
│ ┌───────────┐ │          │                   │
│ │  Status   │ │          │                   │
│ │ Channels  │◄┼──────────┤                   │
│ │           │ │          │                   │
│ │ • OD_LRI  │ │          │  ┌────────────────┘
│ │ • OD_GFI  │ │          │  │
│ │ • OD_XTL  │ │          │  │
│ │ • LIGHT_GUN│◄┼──────────┼──┘
│ └───────────┘ │          │
└───────────────┘          │
        ▲                  │
        │                  ▼
        │         ┌──────────────────┐
        │         │  CPU Poll Loop   │
        │         │                  │
        │         │  while True:     │
        │         │    check status  │
        └─────────┤    read drum     │
                  │    clear status  │
                  └──────────────────┘

External Devices (Asynchronous):
    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │  Radar   │────▶│   Drum   │◀────│Cross-Tell│
    │ Hardware │     │ LRI Field│     │  (XTL)   │
    └──────────┘     └──────────┘     └──────────┘

Key Improvements:
✅ One's complement fractional arithmetic
✅ Drum-buffered asynchronous I/O
✅ Status channel polling (no interrupts)
✅ Light gun flip-flop detection
✅ Parallel processing of halfwords
✅ Implicit shift compensation
```

## Data Flow Comparison

### Previous: Direct I/O
```
Radar → FSQ7State → CPU
             ↓
           CRT Display
             ↓
        Mouse Click → Target ID
```

### New: Drum-Buffered I/O
```
Radar Hardware
    │ (asynchronous write)
    ▼
┌─────────────┐
│ Drum LRI    │ ──sets─▶ Status Channel OD_LRI
│ Field       │
└─────────────┘
    ▲
    │ (CPU polls)
    │
CPU Main Loop:
    while True:
        if check_status(OD_LRI):
            data = read_field(LRI, addr)
            process(data)
            clear_status(OD_LRI)
```

## CPU Arithmetic Comparison

### Previous: Integer Addition
```
A = 0x00001234  (decimal 4660)
B = 0x00005678  (decimal 22136)
───────────────
C = 0x000068AC  (decimal 26796)

Single accumulator
Two's complement
Standard integer math
```

### New: Fractional Parallel Addition with Shift
```
Word1 = [0x4000, 0x2666]  (fractions: 0.5, 0.3)
Word2 = [0x3333, 0x1999]  (fractions: 0.4, 0.2)

Step 1: One's complement add each half
  Left:  0x4000 + 0x3333 = 0x7333
  Right: 0x2666 + 0x1999 = 0x3FFF

Step 2: Implicit right shift (HARDWARE QUIRK!)
  Left:  0x7333 >> 1 = 0x3999  (0.45)
  Right: 0x3FFF >> 1 = 0x1FFF  (0.25)

Result = [0x3999, 0x1FFF]

Parallel processing
One's complement with end-around carry
Implicit shift (programmers must compensate!)
Fractional values only (-1.0 to +1.0)
```

## Light Gun Comparison

### Previous: Mouse Click
```
┌──────────────┐
│  CRT Display │
│   ╔═══╗      │
│   ║TGT║      │
│   ╚═══╝      │
└──────┬───────┘
       │ click!
       ▼
  get_mouse_coords()
  → (X: 100, Y: 200)
  → identify_target(100, 200)
  → "TGT-1" selected

INSTANT identification
```

### New: Polling Detection
```
Operator pulls trigger → light_gun.arm(x, y)

CPU draws each target sequentially:

for target in targets:
    draw_target(target.id, target.x, target.y)
    │
    │ ◄── CRT beam draws target
    │
    if light_gun.poll_status():  ◄── Check for flash!
        selected = target.id
        break

When beam passes gun position:
  photomultiplier fires → flip-flop set → poll returns True

SEQUENTIAL polling after each draw
CPU software must handle detection
```

## Status Channel Polling

```
┌─────────────────────────────────────┐
│      Magnetic Drum Status Word      │
├─────────────────────────────────────┤
│ Bit 0: CD_LRI   (Core→Drum LRI)    │
│ Bit 1: CD_GFI   (Core→Drum GFI)    │
│ Bit 2: CD_XTL   (Core→Drum XTL)    │
│ Bit 3: OD_LRI   (Drum→Out LRI)  ✓  │ ◄── Set when radar writes
│ Bit 4: OD_GFI   (Drum→Out GFI)     │
│ Bit 5: OD_XTL   (Drum→Out XTL)     │
│ Bit 6: LIGHT_GUN (Flash detected)  │
└─────────────────────────────────────┘

CPU polling code:
    status = drum.check_status(StatusChannel.OD_LRI)
    if status:
        # New radar data available!
        for addr in range(0, 100):
            word = drum.read_field(DrumField.LRI, addr)
            process(word)
        drum.clear_status(StatusChannel.OD_LRI)
```

## Memory Word Format

### Previous: Single 32-bit Integer
```
┌────────────────────────────────────┐
│        32-bit Integer              │
│  0x12345678 = 305,419,896          │
└────────────────────────────────────┘
```

### New: Two Parallel 16-bit Fractions
```
┌─────────────────┬─────────────────┐
│   Left Half     │   Right Half    │
│  16-bit (S.15)  │  16-bit (S.15)  │
├─────────────────┼─────────────────┤
│  0x4000 = 0.5   │  0x2666 = 0.3   │
└─────────────────┴─────────────────┘

Coordinate transformation example:
  Left:  X coordinate (fraction)
  Right: Y coordinate (fraction)

Both halves processed SIMULTANEOUSLY in hardware!
```

## Summary

| Feature | Previous | New |
|---------|----------|-----|
| **Arithmetic** | Integer | One's complement fractional |
| **Processing** | Single value | Parallel dual halfwords |
| **I/O** | Direct | Drum-buffered asynchronous |
| **Selection** | Mouse coords | Flip-flop polling |
| **CPU Loop** | Event-driven | Status channel polling |
| **Data Flow** | Synchronous | Asynchronous via drum |

**Bottom Line:**
The simulator now replicates the actual hardware architecture of the AN/FSQ-7,
not just its visual appearance. This enables authentic SAGE software execution.
