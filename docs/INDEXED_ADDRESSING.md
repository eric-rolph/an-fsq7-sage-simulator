# Indexed Addressing Implementation (Chapter 12.3)

## Overview

The AN/FSQ-7 SAGE computer uses **indexed addressing** as a fundamental addressing mode. This is **not optional** — it's essential for almost all real SAGE programs, especially the list processing and loop examples in Chapter 12.5.

## The Critical Formula

```
effective_address = base_address + I
```

Where:
- `base_address`: The address field from the instruction (16 bits)
- `I`: The Index Register (a CPU register)
- `effective_address`: The actual memory address accessed

## Why It Matters

Without indexed addressing, you cannot:
- **Loop through arrays** (Chapter 12.5 examples)
- **Process lists** (core SAGE data structures)
- **Implement subroutines with local variables**
- **Access data structures** (tables, matrices)

**Half of SAGE's instruction flow depends on this feature.**

## Instruction Format

```
┌─────────┬──────────┬─────────────────┐
│ OPCODE  │ INDEX_BIT│    ADDRESS      │
│ 8 bits  │  1 bit   │    16 bits      │
└─────────┴──────────┴─────────────────┘
   31-24      17           15-0

INDEX_BIT = 0: Direct addressing (use ADDRESS as-is)
INDEX_BIT = 1: Indexed addressing (use ADDRESS + I)
```

### Example Instructions

```assembly
; Direct addressing - loads from fixed address 100
LDA  100        ; A ← memory[100]

; Indexed addressing - loads from 100 + I
LDA  100(I)     ; A ← memory[100 + I]
                ; If I=5, loads from memory[105]
```

## The Index Register (I)

The **Index Register** is a general-purpose register used for:

1. **Array indexing**: Access element `array[I]`
2. **Loop counters**: Decrement I and loop while I > 0
3. **Return addresses**: Store return point in subroutine calls

### Common Usage Patterns

```assembly
; Pattern 1: Loop through array (backward)
        LDA  TEN        ; I ← 10 (loop 10 times)
LOOP:   LDA  ARRAY(I)   ; Access array[I]
        ; ... process element ...
        TIX  LOOP       ; I ← I-1; if I>0 goto LOOP

; Pattern 2: Copy array
        LDA  COUNT
LOOP:   LDA  SRC(I)     ; Load source[I]
        STO  DST(I)     ; Store to dest[I]
        TIX  LOOP

; Pattern 3: Search array
        LDA  SIZE
LOOP:   LDA  ARRAY(I)
        SUB  TARGET
        TNZ  NEXT       ; If not match, continue
        ; Found it! I contains the index
        HLT
NEXT:   TIX  LOOP
```

## Chapter 12.5 Example Programs

### 1. Array Sum (Indexed Load)

```python
# Sum array[0..9] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
# Expected result: 275

program = [
    LDA  ZERO           # A ← 0
    STO  SUM            # sum ← 0
    LDA  TEN            # I ← 10
LOOP:
    LDA  SUM            # A ← sum
    ADD  ARRAY(I)       # A ← A + array[I]  <-- INDEXED!
    STO  SUM            # sum ← A
    TIX  LOOP           # I--; loop if I>0
    HLT
]
```

**Key Point**: The `ADD ARRAY(I)` instruction computes `effective_addr = ARRAY + I`, allowing the loop to access different array elements each iteration.

### 2. Array Search (Indexed Compare)

```python
# Search for value 25 in array
# Expected result: Index 4 (0-based)

program = [
    LDA  SEARCH         # A ← search_value
    STO  TEMP
LOOP:
    LDA  ARRAY(I)       # A ← array[I]  <-- INDEXED!
    SUB  TEMP           # A ← array[I] - search_value
    TNZ  NEXT           # If not zero, not found yet
    ; Found it!
    LDA  I_REG          # A ← I (current index)
    STO  RESULT
    HLT
NEXT:
    TIX  LOOP
    HLT                 # Not found
]
```

### 3. Array Copy (Indexed Load and Store)

```python
# Copy src[0..4] to dst[0..4]

program = [
    LDA  FIVE           # I ← 5
LOOP:
    LDA  SRC(I)         # A ← src[I]     <-- INDEXED LOAD
    STO  DST(I)         # dst[I] ← A     <-- INDEXED STORE
    TIX  LOOP
    HLT
]
```

**Key Point**: Both load and store can use indexed addressing, enabling efficient array operations.

### 4. Matrix Initialization (Nested Loops)

```python
# Initialize 3x3 matrix to [1, 2, 3, 4, 5, 6, 7, 8, 9]

program = [
    LDA  ONE            # value ← 1
    STO  VALUE
    LDA  NINE           # I ← 9
LOOP:
    LDA  VALUE          # A ← value
    STO  MATRIX(I)      # matrix[I] ← value  <-- INDEXED!
    ADD  ONE            # value++
    STO  VALUE
    TIX  LOOP
    HLT
]
```

## Implementation Details

### CPU Core (cpu_core.py)

```python
class CPUCore:
    def __init__(self):
        self.accumulator = 0       # A register
        self.index_reg = 0         # I register - CRITICAL!
        self.program_counter = 0   # P register
        self.memory = [0] * 65536  # 64K words
    
    def compute_effective_address(self, instruction: int) -> int:
        """
        Core indexed addressing implementation.
        """
        base_addr = instruction & 0xFFFF           # Extract address
        use_index = (instruction & 0x00020000) != 0  # Check index bit
        
        if use_index:
            return (base_addr + self.index_reg) & 0xFFFF
        else:
            return base_addr
```

### Instruction Encoding

```python
# Create indexed instruction
instruction = CPUCore.encode_instruction(
    opcode=CPUCore.OP_LDA,  # Load accumulator
    address=100,             # Base address
    indexed=True             # Enable indexed addressing
)

# Result: 0x01020064
#   01 = LDA opcode
#   02 = INDEX_BIT set
#   0064 = address 100 (hex)
```

## TIX Instruction (Transfer on Index)

The **TIX** (Transfer on Index) instruction is the primary loop control:

```
TIX  addr

Behavior:
    I ← I - 1
    if I > 0:
        P ← addr    (jump back to loop start)
    else:
        continue    (fall through, loop ends)
```

### Usage Example

```assembly
    LDA  TEN        ; I ← 10 (loop counter)
LOOP:
    ; ... loop body using I for indexing ...
    TIX  LOOP       ; Decrement and loop
    ; Loop executed 10 times with I = 10, 9, 8, ..., 1
```

## Testing Indexed Addressing

Run the test suite:

```bash
cd an_fsq7_simulator
python -m cpu_core
```

Expected output:
```
Testing AN/FSQ-7 CPU Core with Indexed Addressing
============================================================

Final state:
  Accumulator: 275
  Index Register: 0
  Sum at address 201: 275
  Instructions executed: 37

Expected sum: 275 (should be 275)
```

Or run all Chapter 12.5 examples:

```bash
python -m sage_programs
```

Expected output:
```
AN/FSQ-7 SAGE Programs - Indexed Addressing Demonstrations
Chapter 12.5 Example Programs

============================================================
Program: Array Sum
Description: Sum array elements using indexed addressing
============================================================
...
✓ All indexed addressing examples working correctly!
  The AN/FSQ-7 CPU core properly implements:
    • effective_address = base_address + I
    • Index register (I) for loop counters
    • Indexed load: LDA base(I)
    • Indexed store: STO base(I)
    • Loop control: TIX (Transfer on Index)
```

## Web UI Integration

The simulator now includes a **CPU Panel** that displays:

- **A (Accumulator)**: Main computation register
- **I (Index Register)**: Highlighted in cyan - critical for debugging loops
- **P (Program Counter)**: Current instruction address
- **Program Selector**: Load Chapter 12.5 examples
- **Execution Controls**: Step, Run, Reset

### Using the Web Interface

1. **Start the simulator**: `reflex run`
2. **Power on** the system (wait for tube warm-up)
3. **Select a program** from the dropdown (e.g., "Array Sum (Ch 12.5)")
4. **Click "LOAD PROGRAM"** to load into memory
5. **Click "STEP"** to execute one instruction at a time
6. **Watch the Index Register (I)** decrement as the loop executes
7. **Click "RUN"** to execute at full speed (100 Hz)

### Observing Indexed Addressing

When stepping through array operations:
- **Before loop**: I = 10
- **First iteration**: I = 10, accesses array[10]
- **Second iteration**: I = 9, accesses array[9]
- ...
- **Final iteration**: I = 1, accesses array[1]
- **After loop**: I = 0, loop exits

The status bar shows real-time register values:
```
CPU: A=115 I=7 P=5
```

## Future Enhancements

### Drum Timing (Chapters 7.2-7.3)

Currently using **cycle-free instant memory access**. Future version can add:

- **Drum rotation**: 12,000 RPM (200 rotations/second)
- **Sector timing**: Wait for correct sector to rotate under read head
- **Latency**: Average 2.5ms per access (half rotation)
- **Scheduling**: Optimize instruction placement to minimize wait time

### Multiple Index Registers

The real AN/FSQ-7 had more complex indexing. Could add:
- **Base registers**: Multiple base address registers
- **Index arithmetic**: Add/subtract from index without loading accumulator
- **Indirect addressing**: Use memory word as address pointer

## Summary

✅ **Indexed addressing is now fully implemented**:
- ✅ Index Register (I) in CPU core
- ✅ `effective_addr = base + I` computation
- ✅ INDEX_BIT in instruction format
- ✅ Chapter 12.5 example programs working
- ✅ TIX loop control instruction
- ✅ UI showing I register in real-time
- ✅ Step-by-step execution for debugging

**The simulator can now run authentic SAGE programs that use indexed addressing for list processing and loops.**

## References

- **Chapter 12.3**: Indexed Addressing (defines the I register and effective address formula)
- **Chapter 12.5**: Example Programs (assumes indexed addressing exists)
- **Chapter 7.2-7.3**: Drum timing (future enhancement for realistic latency)
