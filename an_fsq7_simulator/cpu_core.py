"""
AN/FSQ-7 CPU Core - Instruction Execution Engine

This module implements the actual CPU core of the AN/FSQ-7 SAGE computer,
including the index register for indexed addressing as specified in technical specification

The AN/FSQ-7 instruction format:
    OPCODE ADDRESS [INDEX_BIT]
    
Where INDEX_BIT determines if the index register (I) is added to the address:
    effective_address = ADDRESS + I    (if indexed)
    effective_address = ADDRESS        (if not indexed)

This is essential for list processing and loop operations demonstrated in technical specification
"""

from typing import Optional, List, Tuple, Callable
import struct


class CPUCore:
    """
    AN/FSQ-7 CPU Core with indexed addressing support.
    
    Registers:
        A (Accumulator): Main computation register
        I (Index): Used for indexed addressing and loop counters
        P (Program Counter): Current instruction address
        
    Memory:
        64K words (cycle-free access for now, drum timing can be added later)
        Each word is 32 bits
    """
    
    # Instruction opcodes (simplified set for technical specification examples)
    OP_LDA = 0x01  # Load Accumulator:        A ← mem[addr]
    OP_STO = 0x02  # Store Accumulator:       mem[addr] ← A
    OP_ADD = 0x03  # Add to Accumulator:      A ← A + mem[addr]
    OP_SUB = 0x04  # Subtract from Acc:       A ← A - mem[addr]
    OP_MPY = 0x05  # Multiply:                A ← A × mem[addr]
    OP_DVH = 0x06  # Divide (high quotient):  A ← A ÷ mem[addr]
    OP_TRA = 0x10  # Transfer (unconditional jump): P ← addr
    OP_TNZ = 0x11  # Transfer if Non-Zero:    if A ≠ 0 then P ← addr
    OP_TMI = 0x12  # Transfer if Minus:       if A < 0 then P ← addr
    OP_TSX = 0x13  # Transfer and Set Index:  I ← P+1; P ← addr
    OP_TIX = 0x14  # Transfer on Index:       I ← I-1; if I > 0 then P ← addr
    OP_TXI = 0x15  # Transfer with Index Inc: I ← I + decrement; if I ≤ count then P ← addr
    OP_HLT = 0xFF  # Halt execution
    
    # Index bit flag (bit 17 in a 32-bit word)
    INDEX_BIT_MASK = 0x00020000
    
    def __init__(self, memory_size: int = 65536):
        """
        Initialize the CPU core.
        
        Args:
            memory_size: Size of memory in words (default 64K)
        """
        # Registers
        self.accumulator = 0        # A register (32-bit signed)
        self.index_reg = 0          # I register (index for addressing)
        self.program_counter = 0    # P register (instruction pointer)
        
        # Memory (cycle-free instant access for now)
        self.memory_size = memory_size
        self.memory = [0] * memory_size
        
        # Execution state
        self.halted = False
        self.instruction_count = 0
        self.cycle_count = 0
        
        # Instruction history for debugging
        self.trace_enabled = False
        self.trace_buffer = []
        
        # Real-time clock (for compatibility with sim_loop tick_rtc call)
        self.rtc_ticks = 0
        
    def tick_rtc(self, delta_seconds: float):
        """
        Update real-time clock (stub for compatibility with sim_loop).
        
        Args:
            delta_seconds: Time elapsed since last RTC tick
        """
        self.rtc_ticks += 1
        
    def reset(self):
        """Reset CPU to initial state."""
        self.accumulator = 0
        self.index_reg = 0
        self.program_counter = 0
        self.halted = False
        self.instruction_count = 0
        self.cycle_count = 0
        self.trace_buffer = []
        
    def load_program(self, program: List[int], start_address: int = 0):
        """
        Load a program into memory.
        
        Args:
            program: List of 32-bit words (instructions and data)
            start_address: Memory address to start loading at
        """
        for i, word in enumerate(program):
            addr = start_address + i
            if addr < self.memory_size:
                self.memory[addr] = word & 0xFFFFFFFF  # Ensure 32-bit
                
    def compute_effective_address(self, instruction: int) -> int:
        """
        Compute the effective address from an instruction word.
        
        This is the critical indexed addressing implementation from technical specification:
            effective_addr = base_addr + (I if indexed else 0)
        
        Args:
            instruction: 32-bit instruction word
            
        Returns:
            Effective memory address (16-bit)
        """
        # Extract base address (bits 0-15, lower 16 bits)
        base_addr = instruction & 0xFFFF
        
        # Check index bit (bit 17)
        use_index = (instruction & self.INDEX_BIT_MASK) != 0
        
        if use_index:
            # Indexed addressing: addr = base + I
            effective = (base_addr + self.index_reg) & 0xFFFF
        else:
            # Direct addressing: addr = base
            effective = base_addr
            
        return effective
    
    def fetch(self) -> int:
        """
        Fetch the next instruction from memory.
        
        Returns:
            32-bit instruction word
        """
        if self.program_counter >= self.memory_size:
            self.halted = True
            return self.encode_instruction(self.OP_HLT, 0)
            
        instruction = self.memory[self.program_counter]
        self.program_counter += 1
        return instruction
    
    def decode_instruction(self, instruction: int) -> Tuple[int, int, bool]:
        """
        Decode an instruction word into components.
        
        Args:
            instruction: 32-bit instruction word
            
        Returns:
            Tuple of (opcode, address, indexed_flag)
        """
        opcode = (instruction >> 24) & 0xFF
        address = instruction & 0xFFFF
        indexed = (instruction & self.INDEX_BIT_MASK) != 0
        return opcode, address, indexed
    
    def execute_instruction(self, instruction: int):
        """
        Execute a single instruction.
        
        Args:
            instruction: 32-bit instruction word
        """
        opcode, raw_addr, indexed = self.decode_instruction(instruction)
        effective_addr = self.compute_effective_address(instruction)
        
        # Trace if enabled
        if self.trace_enabled:
            self.trace_buffer.append({
                "pc": self.program_counter - 1,
                "instruction": instruction,
                "opcode": opcode,
                "raw_addr": raw_addr,
                "indexed": indexed,
                "effective_addr": effective_addr,
                "accumulator_before": self.accumulator,
                "index_before": self.index_reg,
            })
        
        # Execute based on opcode
        if opcode == self.OP_LDA:
            # Load Accumulator
            self.accumulator = self.read_memory(effective_addr)
            
        elif opcode == self.OP_STO:
            # Store Accumulator
            self.write_memory(effective_addr, self.accumulator)
            
        elif opcode == self.OP_ADD:
            # Add to Accumulator
            operand = self.read_memory(effective_addr)
            self.accumulator = self.to_signed32(self.accumulator + operand)
            
        elif opcode == self.OP_SUB:
            # Subtract from Accumulator
            operand = self.read_memory(effective_addr)
            self.accumulator = self.to_signed32(self.accumulator - operand)
            
        elif opcode == self.OP_MPY:
            # Multiply
            operand = self.read_memory(effective_addr)
            self.accumulator = self.to_signed32(self.accumulator * operand)
            
        elif opcode == self.OP_DVH:
            # Divide (high quotient)
            operand = self.read_memory(effective_addr)
            if operand != 0:
                self.accumulator = self.to_signed32(self.accumulator // operand)
            else:
                # Division by zero - set to max value
                self.accumulator = 0x7FFFFFFF
                
        elif opcode == self.OP_TRA:
            # Unconditional Transfer (jump)
            self.program_counter = effective_addr
            
        elif opcode == self.OP_TNZ:
            # Transfer if Non-Zero
            if self.accumulator != 0:
                self.program_counter = effective_addr
                
        elif opcode == self.OP_TMI:
            # Transfer if Minus
            if self.to_signed32(self.accumulator) < 0:
                self.program_counter = effective_addr
                
        elif opcode == self.OP_TSX:
            # Transfer and Set Index (subroutine call)
            self.index_reg = self.program_counter  # Save return address in I
            self.program_counter = effective_addr
            
        elif opcode == self.OP_TIX:
            # Transfer on Index (loop control)
            # Decrement index and jump if still positive
            self.index_reg = self.to_signed32(self.index_reg - 1)
            if self.index_reg > 0:
                self.program_counter = effective_addr
                
        elif opcode == self.OP_TXI:
            # Transfer with Index Increment (advanced loop control)
            # Format: TXI addr,increment,limit
            # Extract increment and limit from address field
            increment = (raw_addr >> 8) & 0xFF
            limit = raw_addr & 0xFF
            self.index_reg += increment
            if self.index_reg <= limit:
                self.program_counter = effective_addr
                
        elif opcode == self.OP_HLT:
            # Halt
            self.halted = True
            
        else:
            # Unknown opcode - halt with error
            self.halted = True
            print(f"ERROR: Unknown opcode 0x{opcode:02X} at address {self.program_counter-1}")
        
        self.instruction_count += 1
        self.cycle_count += 1  # For now, 1 cycle per instruction (drum timing would add more)
    
    def step(self) -> bool:
        """
        Execute one instruction (fetch-decode-execute cycle).
        
        Returns:
            True if execution should continue, False if halted
        """
        if self.halted:
            return False
            
        instruction = self.fetch()
        self.execute_instruction(instruction)
        
        return not self.halted
    
    def run(self, max_instructions: int = 10000):
        """
        Run the program until halt or max instructions reached.
        
        Args:
            max_instructions: Maximum number of instructions to execute
        """
        while not self.halted and self.instruction_count < max_instructions:
            self.step()
            
    def read_memory(self, address: int) -> int:
        """Read a word from memory."""
        if 0 <= address < self.memory_size:
            return self.memory[address]
        return 0
    
    def write_memory(self, address: int, value: int):
        """Write a word to memory."""
        if 0 <= address < self.memory_size:
            self.memory[address] = value & 0xFFFFFFFF
            
    @staticmethod
    def to_signed32(value: int) -> int:
        """Convert to signed 32-bit integer."""
        value = value & 0xFFFFFFFF
        if value & 0x80000000:
            return value - 0x100000000
        return value
    
    @staticmethod
    def encode_instruction(opcode: int, address: int, indexed: bool = False) -> int:
        """
        Encode an instruction word.
        
        Args:
            opcode: 8-bit operation code
            address: 16-bit address
            indexed: Whether to use indexed addressing
            
        Returns:
            32-bit instruction word
        """
        instruction = (opcode << 24) | (address & 0xFFFF)
        if indexed:
            instruction |= CPUCore.INDEX_BIT_MASK
        return instruction
    
    def get_state(self) -> dict:
        """
        Get current CPU state for display/debugging.
        
        Returns:
            Dictionary with register values and status
        """
        return {
            "accumulator": self.accumulator,
            "index_reg": self.index_reg,
            "program_counter": self.program_counter,
            "halted": self.halted,
            "instruction_count": self.instruction_count,
            "cycle_count": self.cycle_count,
        }
    
    def get_trace(self) -> List[dict]:
        """Get instruction trace buffer."""
        return self.trace_buffer.copy()
    
    def clear_trace(self):
        """Clear trace buffer."""
        self.trace_buffer = []


# Example programs demonstrating indexed addressing (technical specification style)

def example_array_sum():
    """
    Example: Sum an array using indexed addressing.
    
    Pseudocode:
        sum = 0
        I = 0
        for i in range(10):
            sum += array[I]
            I += 1
    """
    cpu = CPUCore()
    
    # Data: array of 10 numbers at address 100
    array_data = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    cpu.load_program(array_data, start_address=100)
    
    # Program starting at address 0
    program = [
        # Initialize
        CPUCore.encode_instruction(CPUCore.OP_LDA, 200),      # 0: Load 0 into A (sum)
        CPUCore.encode_instruction(CPUCore.OP_STO, 201),      # 1: Store sum at 201
        CPUCore.encode_instruction(CPUCore.OP_LDA, 202),      # 2: Load 10 into A (counter)
        
        # Loop start (address 3)
        CPUCore.encode_instruction(CPUCore.OP_ADD, 100, indexed=True),  # 3: A += array[I]
        CPUCore.encode_instruction(CPUCore.OP_STO, 201),      # 4: Store sum
        CPUCore.encode_instruction(CPUCore.OP_TIX, 3),        # 5: I--; if I>0 goto 3
        
        CPUCore.encode_instruction(CPUCore.OP_HLT, 0),        # 6: Halt
    ]
    
    # Data constants
    cpu.write_memory(200, 0)   # Initial sum = 0
    cpu.write_memory(201, 0)   # Sum storage
    cpu.write_memory(202, 10)  # Counter = 10
    cpu.index_reg = 0          # Start index at 0
    
    cpu.load_program(program, start_address=0)
    cpu.trace_enabled = True
    cpu.run()
    
    return cpu


if __name__ == "__main__":
    # Test the indexed addressing example
    print("Testing AN/FSQ-7 CPU Core with Indexed Addressing")
    print("=" * 60)
    
    cpu = example_array_sum()
    print(f"\nFinal state:")
    print(f"  Accumulator: {cpu.accumulator}")
    print(f"  Index Register: {cpu.index_reg}")
    print(f"  Sum at address 201: {cpu.read_memory(201)}")
    print(f"  Instructions executed: {cpu.instruction_count}")
    print(f"\nExpected sum: {sum([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])} (should be 275)")
