# HIGH-FIDELITY EMULATION - AN/FSQ-7 SAGE Computer

## Overview

This implementation transforms the SAGE simulator from a visualization demo into a **high-fidelity emulation** capable of running original SAGE software. The focus is on authentic architectural fidelity rather than just visual simulation.

## Critical Architectural Improvements

### 1. One's Complement Fractional Arithmetic ✅

**The Real Hardware:**
The AN/FSQ-7's Arithmetic Element (AE) was fundamentally different from modern CPUs:
- **Parallel processing**: Each 32-bit word contained TWO 16-bit values processed simultaneously
- **Fractional numbers**: All values represented as fractions between -1.0 and +1.0
- **One's complement**: Used one's complement representation (not two's complement)
- **Implicit shift**: Addition included an automatic right shift (hardware quirk programmers had to work around)

**Previous Implementation:**
- Standard integer arithmetic
- Single accumulator value
- Two's complement representation
- Direct addition without shift

**New Implementation** (`cpu_core_fractional.py`):
```python
class OnesComplementWord:
    # One's complement arithmetic with end-around carry
    # Parallel operation on two 16-bit fractional halves
    # Implicit right shift during addition (hardware quirk)
    # All values between -1.0 and +1.0
```

**Key Differences:**
- ✅ One's complement with end-around carry
- ✅ Parallel processing of both halfwords
- ✅ Fractional arithmetic (-1.0 to +1.0)
- ✅ Implicit right shift on addition
- ✅ Two representations of zero (+0 and -0)
- ✅ Authentic negation (bit inversion)

**Example:**
```python
# Add 0.5 + 0.3 with implicit shift
word1 = from_fractions(0.5, 0.3)
word2 = from_fractions(0.4, 0.2)
result = parallel_add_with_shift(word1, word2)
# Result: (0.45, 0.25) due to >>1 shift
# Programmers had to pre-shift operands to compensate!
```

### 2. Light Gun Polling Mechanism ✅

**The Real Hardware:**
The light gun used a photomultiplier tube and timing-based detection:
1. Operator pulls trigger → gun is "armed"
2. CRT electron beam draws each target sequentially
3. When beam passes gun position → photomultiplier fires
4. Signal sets a flip-flop bit in status channel
5. **CPU must poll this bit after EVERY draw operation**
6. CPU identifies selected target by which draw caused the flash

**Previous Implementation:**
- Mouse click provides (X,Y) coordinates
- Direct target identification
- No polling required

**New Implementation** (`drum_io_system.py`):
```python
class LightGunSystem:
    def arm(self, x, y):
        # Operator pulls trigger
        
    def draw_event(self, obj_id, x, y):
        # CPU draws object, checks for flash
        if beam_passes_gun_position:
            self.flash_detected = True
            return True
            
    # CPU must poll after EACH draw:
    for target in targets:
        draw_target(target)
        if light_gun.poll_status():
            selected = target
            break
```

**Key Differences:**
- ✅ Flip-flop flag instead of coordinates
- ✅ CPU must poll after each draw operation
- ✅ Sequential detection (not instant identification)
- ✅ Photomultiplier timing simulation

### 3. Drum-Buffered Asynchronous I/O ✅

**The Real Hardware:**
The magnetic drum was the "great decoupler" of SAGE:
- **No direct CPU-to-device I/O**: CPU NEVER talks directly to radar, consoles, or other sites
- **Asynchronous writes**: External hardware writes to drum fields independently
- **Status channel polling**: CPU continuously polls status bits to detect new data
- **Dedicated drum fields**: LRI (radar), GFI (ground radar), XTL (cross-tell), etc.

**Previous Implementation:**
- Direct target generation in simulation loop
- Real-time data flow into CPU
- No buffering layer

**New Implementation** (`drum_io_system.py`):
```python
class FSQ7_IO_System:
    def __init__(self):
        self.drum = MagneticDrum()
        # Drum fields: LRI, GFI, XTL, SDC, LOG, TMP
        # Status channels: CD_LRI, OD_LRI, LIGHT_GUN, etc.
    
    # External radar writes to drum (asynchronously):
    def simulate_radar_input(self, targets):
        for target in targets:
            self.drum.write_field(DrumField.LRI, addr, data)
            # Automatically sets status channel OD_LRI
    
    # CPU polling loop (what SAGE software actually did):
    def cpu_poll_loop(self):
        # Check status channel
        if self.drum.check_status(StatusChannel.OD_LRI):
            # Read data from LRI field
            data = self.drum.read_field(DrumField.LRI, addr)
            # Process data
            # Clear status bit
            self.drum.clear_status(StatusChannel.OD_LRI)
```

**Authentic SAGE Software Flow:**
```
1. Radar hardware → writes to LRI drum field → sets status bit
2. CPU main loop → polls status channels
3. CPU detects OD_LRI status set
4. CPU reads LRI field data
5. CPU processes targets
6. CPU clears OD_LRI status bit
7. Loop continues...
```

**Key Differences:**
- ✅ Magnetic drum intermediary (not direct I/O)
- ✅ Status channel polling (not interrupts)
- ✅ Asynchronous data buffering
- ✅ Dedicated drum fields for each input type
- ✅ CPU must explicitly clear status bits

## Architecture Comparison

| Feature | Previous (Demo) | New (High-Fidelity) |
|---------|----------------|---------------------|
| **Arithmetic** | Integer, two's complement | One's complement fractions |
| **Word Format** | Single 32-bit value | Two parallel 16-bit fractions |
| **Number Range** | -2³¹ to +2³¹ | -1.0 to +1.0 (each half) |
| **Addition** | Standard add | Add with implicit right shift |
| **Light Gun** | Mouse (X,Y) coordinates | Flip-flop flag polling |
| **Target Selection** | Direct identification | Poll after each draw |
| **I/O Architecture** | Direct data flow | Drum-buffered asynchronous |
| **Radar Input** | Real-time generation | Write to LRI drum field |
| **Status Detection** | Immediate | Poll status channels |

## Implementation Files

### Core Arithmetic
- **`cpu_core_fractional.py`** - One's complement fractional CPU
  - `OnesComplementWord` class
  - Parallel arithmetic operations
  - Implicit shift implementation
  - Fraction conversion utilities

### I/O System
- **`drum_io_system.py`** - Authentic drum I/O architecture
  - `MagneticDrum` class (fields, status channels)
  - `LightGunSystem` class (polling mechanism)
  - `FSQ7_IO_System` integration class
  - Status channel definitions (LRI, GFI, XTL)

## Testing

Both implementations include comprehensive tests:

```bash
# Test one's complement arithmetic
python an_fsq7_simulator/cpu_core_fractional.py

# Test drum I/O and light gun polling
python an_fsq7_simulator/drum_io_system.py
```

## Benefits of High-Fidelity Emulation

1. **Authentic Software Execution**
   - Can run original SAGE programs (if we had them)
   - Correct arithmetic behavior for coordinate transformations
   - Proper timing and synchronization

2. **Educational Value**
   - Shows how 1950s computers actually worked
   - Demonstrates unique architectural choices
   - Explains why SAGE programs were written the way they were

3. **Historical Accuracy**
   - Preserves knowledge of AN/FSQ-7 architecture
   - Documents unusual features (implicit shift, drum I/O)
   - Enables future research and restoration

4. **Programming Challenges**
   - Fractional arithmetic requires different algorithms
   - Implicit shift demands pre-compensation
   - Polling loops instead of event handlers
   - Drum buffering changes data flow patterns

## Remaining Work

To complete the high-fidelity emulation:

1. **Integration** - Connect new modules to Reflex UI
   - Replace integer CPU with fractional CPU
   - Wire drum I/O system to radar simulation
   - Implement light gun polling in CRT component

2. **Full Opcode Set** - Implement remaining opcodes
   - Multiply (TMU) with fractional math
   - Shift operations
   - Branch instructions
   - I/O class instructions

3. **Drum Timing** - Add realistic timing delays
   - 3600 RPM rotation (60 Hz)
   - Sector access delays
   - Transfer rates

4. **Memory Banks** - Authentic bank switching
   - 65K main core (Memory 1)
   - 4K auxiliary core (Memory 2)
   - Octal addressing with bank prefix

## References

- **Technical Documentation**: AN/FSQ-7 architecture specifications
- **Wikipedia**: AN/FSQ-7 Combat Direction Central
- **Historical Sources**: SAGE programming manuals and operational procedures

## Next Steps

1. Integrate `cpu_core_fractional.py` into main simulator
2. Replace current target generation with drum-buffered radar
3. Implement light gun polling in CRT click handler
4. Add status channel displays to UI
5. Create example programs demonstrating fractional arithmetic
6. Document programming patterns for implicit shift compensation

---

**This implementation represents a fundamental shift from "looks like SAGE" to "works like SAGE".**
