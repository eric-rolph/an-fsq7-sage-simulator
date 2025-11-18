"""
Extended tests for CPU core - instruction execution and indexed addressing.

Tests the AN/FSQ-7 CPU instruction set implementation in cpu_core.py.
"""

import pytest
from an_fsq7_simulator.cpu_core import CPUCore


@pytest.mark.unit
class TestCPUCoreArithmetic:
    """Test arithmetic instructions (LDA, STO, ADD, SUB, MPY, DVH)."""

    def test_lda_loads_value_into_accumulator(self):
        """Verify LDA instruction loads memory value into accumulator."""
        cpu = CPUCore()
        
        # Store value in memory
        cpu.memory[100] = 42
        
        # Create LDA instruction: opcode=0x01, address=100
        instruction = (CPUCore.OP_LDA << 24) | 100
        
        cpu.execute_instruction(instruction)
        
        assert cpu.accumulator == 42

    def test_sto_stores_accumulator_to_memory(self):
        """Verify STO instruction stores accumulator to memory."""
        cpu = CPUCore()
        
        cpu.accumulator = 123
        
        # Create STO instruction: opcode=0x02, address=200
        instruction = (CPUCore.OP_STO << 24) | 200
        
        cpu.execute_instruction(instruction)
        
        assert cpu.memory[200] == 123

    def test_add_adds_memory_to_accumulator(self):
        """Verify ADD instruction adds memory value to accumulator."""
        cpu = CPUCore()
        
        cpu.accumulator = 10
        cpu.memory[100] = 5
        
        # Create ADD instruction
        instruction = (CPUCore.OP_ADD << 24) | 100
        
        cpu.execute_instruction(instruction)
        
        assert cpu.accumulator == 15

    def test_sub_subtracts_memory_from_accumulator(self):
        """Verify SUB instruction subtracts memory value from accumulator."""
        cpu = CPUCore()
        
        cpu.accumulator = 20
        cpu.memory[100] = 7
        
        # Create SUB instruction
        instruction = (CPUCore.OP_SUB << 24) | 100
        
        cpu.execute_instruction(instruction)
        
        assert cpu.accumulator == 13

    def test_mpy_multiplies_accumulator_by_memory(self):
        """Verify MPY instruction multiplies accumulator by memory value."""
        cpu = CPUCore()
        
        cpu.accumulator = 6
        cpu.memory[100] = 7
        
        # Create MPY instruction
        instruction = (CPUCore.OP_MPY << 24) | 100
        
        cpu.execute_instruction(instruction)
        
        assert cpu.accumulator == 42

    def test_dvh_divides_accumulator_by_memory(self):
        """Verify DVH instruction divides accumulator by memory value."""
        cpu = CPUCore()
        
        cpu.accumulator = 50
        cpu.memory[100] = 5
        
        # Create DVH instruction
        instruction = (CPUCore.OP_DVH << 24) | 100
        
        cpu.execute_instruction(instruction)
        
        assert cpu.accumulator == 10


@pytest.mark.unit
class TestCPUCoreBranching:
    """Test branching instructions (TRA, TNZ, TMI, TSX, TIX, TXI)."""

    def test_tra_unconditional_jump(self):
        """Verify TRA instruction jumps unconditionally."""
        cpu = CPUCore()
        
        cpu.program_counter = 100
        
        # Create TRA instruction to address 500
        instruction = (CPUCore.OP_TRA << 24) | 500
        
        cpu.execute_instruction(instruction)
        
        assert cpu.program_counter == 500

    def test_tnz_jumps_when_accumulator_nonzero(self):
        """Verify TNZ instruction jumps when accumulator is non-zero."""
        cpu = CPUCore()
        
        cpu.accumulator = 42
        cpu.program_counter = 100
        
        # Create TNZ instruction
        instruction = (CPUCore.OP_TNZ << 24) | 500
        
        cpu.execute_instruction(instruction)
        
        assert cpu.program_counter == 500

    def test_tnz_no_jump_when_accumulator_zero(self):
        """Verify TNZ instruction does not jump when accumulator is zero."""
        cpu = CPUCore()
        
        cpu.accumulator = 0
        cpu.program_counter = 100
        
        # Create TNZ instruction
        instruction = (CPUCore.OP_TNZ << 24) | 500
        
        cpu.execute_instruction(instruction)
        
        assert cpu.program_counter == 100  # No jump

    def test_tmi_jumps_when_accumulator_negative(self):
        """Verify TMI instruction jumps when accumulator is negative."""
        cpu = CPUCore()
        
        # Set negative value (two's complement)
        cpu.accumulator = -10
        cpu.program_counter = 100
        
        # Create TMI instruction
        instruction = (CPUCore.OP_TMI << 24) | 500
        
        cpu.execute_instruction(instruction)
        
        assert cpu.program_counter == 500

    def test_tmi_no_jump_when_accumulator_positive(self):
        """Verify TMI instruction does not jump when accumulator is positive."""
        cpu = CPUCore()
        
        cpu.accumulator = 10
        cpu.program_counter = 100
        
        # Create TMI instruction
        instruction = (CPUCore.OP_TMI << 24) | 500
        
        cpu.execute_instruction(instruction)
        
        assert cpu.program_counter == 100  # No jump


@pytest.mark.unit
class TestCPUCoreIndexedAddressing:
    """Test indexed addressing mode."""

    def test_compute_effective_address_direct(self):
        """Verify effective address calculation for direct addressing."""
        cpu = CPUCore()
        
        cpu.index_reg = 100
        
        # Instruction with address 500, no index bit
        instruction = (CPUCore.OP_LDA << 24) | 500
        
        effective = cpu.compute_effective_address(instruction)
        
        # Direct addressing: should be 500 (ignore index)
        assert effective == 500

    def test_compute_effective_address_indexed(self):
        """Verify effective address calculation for indexed addressing."""
        cpu = CPUCore()
        
        cpu.index_reg = 100
        
        # Instruction with address 500, WITH index bit set
        instruction = (CPUCore.OP_LDA << 24) | 500 | CPUCore.INDEX_BIT_MASK
        
        effective = cpu.compute_effective_address(instruction)
        
        # Indexed addressing: should be 500 + 100 = 600
        assert effective == 600

    def test_lda_with_indexed_addressing(self):
        """Verify LDA works with indexed addressing."""
        cpu = CPUCore()
        
        cpu.index_reg = 50
        cpu.memory[150] = 999  # Base address 100 + index 50 = 150
        
        # LDA with base address 100, indexed
        instruction = (CPUCore.OP_LDA << 24) | 100 | CPUCore.INDEX_BIT_MASK
        
        cpu.execute_instruction(instruction)
        
        assert cpu.accumulator == 999

    def test_sto_with_indexed_addressing(self):
        """Verify STO works with indexed addressing."""
        cpu = CPUCore()
        
        cpu.accumulator = 777
        cpu.index_reg = 25
        
        # STO with base address 200, indexed (effective = 225)
        instruction = (CPUCore.OP_STO << 24) | 200 | CPUCore.INDEX_BIT_MASK
        
        cpu.execute_instruction(instruction)
        
        assert cpu.memory[225] == 777


@pytest.mark.unit
class TestCPUCoreExecution:
    """Test CPU execution control flow."""

    def test_fetch_increments_program_counter(self):
        """Verify fetch() increments program counter."""
        cpu = CPUCore()
        
        cpu.program_counter = 100
        cpu.memory[100] = 0x12345678
        
        instruction = cpu.fetch()
        
        assert instruction == 0x12345678
        assert cpu.program_counter == 101

    def test_fetch_halts_at_memory_boundary(self):
        """Verify fetch() halts when PC exceeds memory size."""
        cpu = CPUCore(memory_size=100)
        
        cpu.program_counter = 100  # At boundary
        
        instruction = cpu.fetch()
        
        assert cpu.halted == True
        # Should return HLT instruction
        assert (instruction >> 24) & 0xFF == CPUCore.OP_HLT

    def test_decode_instruction(self):
        """Verify decode_instruction extracts components correctly."""
        cpu = CPUCore()
        
        # Instruction: opcode=0x05 (MPY), address=0x1234, indexed
        instruction = (0x05 << 24) | 0x1234 | CPUCore.INDEX_BIT_MASK
        
        opcode, address, indexed = cpu.decode_instruction(instruction)
        
        assert opcode == 0x05
        assert address == 0x1234
        assert indexed == True

    def test_reset_clears_all_state(self):
        """Verify reset() clears all CPU state."""
        cpu = CPUCore()
        
        # Modify state
        cpu.accumulator = 123
        cpu.index_reg = 456
        cpu.program_counter = 789
        cpu.halted = True
        cpu.instruction_count = 100
        
        cpu.reset()
        
        assert cpu.accumulator == 0
        assert cpu.index_reg == 0
        assert cpu.program_counter == 0
        assert cpu.halted == False
        assert cpu.instruction_count == 0

    def test_load_program(self):
        """Verify load_program() loads instructions into memory."""
        cpu = CPUCore()
        
        program = [0x01000064, 0x02000065, 0xFF000000]  # LDA, STO, HLT
        
        cpu.load_program(program, start_address=100)
        
        assert cpu.memory[100] == 0x01000064
        assert cpu.memory[101] == 0x02000065
        assert cpu.memory[102] == 0xFF000000


@pytest.mark.unit
class TestCPUCoreTracing:
    """Test execution tracing features."""

    def test_trace_disabled_by_default(self):
        """Verify tracing is disabled by default."""
        cpu = CPUCore()
        
        assert cpu.trace_enabled == False
        assert len(cpu.trace_buffer) == 0

    def test_trace_records_execution(self):
        """Verify trace records instruction execution when enabled."""
        cpu = CPUCore()
        
        cpu.trace_enabled = True
        cpu.accumulator = 10
        cpu.memory[100] = 5
        cpu.program_counter = 50
        
        # Execute ADD instruction
        instruction = (CPUCore.OP_ADD << 24) | 100
        cpu.execute_instruction(instruction)
        
        # Should have trace entry
        assert len(cpu.trace_buffer) == 1
        trace = cpu.trace_buffer[0]
        assert trace["opcode"] == CPUCore.OP_ADD
        assert trace["accumulator_before"] == 10
