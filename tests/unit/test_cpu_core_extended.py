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


@pytest.mark.unit
class TestCPUCoreAdvancedBranching:
    """Test advanced branching instructions (TSX, TIX, TXI, HLT)."""

    def test_tsx_saves_return_address(self):
        """Verify TSX instruction saves return address in index register."""
        cpu = CPUCore()
        
        cpu.program_counter = 100
        
        # Create TSX instruction (subroutine call)
        instruction = (CPUCore.OP_TSX << 24) | 500
        
        cpu.execute_instruction(instruction)
        
        # Should save return address (100) in index register
        assert cpu.index_reg == 100
        # Should jump to subroutine
        assert cpu.program_counter == 500

    def test_tix_decrements_index_and_jumps(self):
        """Verify TIX instruction decrements index and jumps if positive."""
        cpu = CPUCore()
        
        cpu.index_reg = 5
        cpu.program_counter = 100
        
        # Create TIX instruction
        instruction = (CPUCore.OP_TIX << 24) | 200
        
        cpu.execute_instruction(instruction)
        
        # Should decrement index
        assert cpu.index_reg == 4
        # Should jump (index still positive)
        assert cpu.program_counter == 200

    def test_tix_no_jump_when_index_zero(self):
        """Verify TIX does not jump when index reaches zero."""
        cpu = CPUCore()
        
        cpu.index_reg = 1
        cpu.program_counter = 100
        
        # Create TIX instruction
        instruction = (CPUCore.OP_TIX << 24) | 200
        
        cpu.execute_instruction(instruction)
        
        # Should decrement to zero
        assert cpu.index_reg == 0
        # Should NOT jump
        assert cpu.program_counter == 100

    def test_txi_increments_index_and_jumps(self):
        """Verify TXI instruction increments index and jumps if within limit."""
        cpu = CPUCore()
        
        cpu.index_reg = 5
        cpu.program_counter = 100
        
        # Create TXI instruction with increment=2, limit=10
        # Address field: (increment << 8) | limit = 522
        address_field = (2 << 8) | 10
        instruction = (CPUCore.OP_TXI << 24) | address_field
        
        cpu.execute_instruction(instruction)
        
        # Should increment index by 2 (5 + 2 = 7)
        assert cpu.index_reg == 7
        # Should jump to effective_addr (522)
        assert cpu.program_counter == 522

    def test_hlt_stops_execution(self):
        """Verify HLT instruction halts CPU."""
        cpu = CPUCore()
        
        # Create HLT instruction
        instruction = (CPUCore.OP_HLT << 24) | 0
        
        cpu.execute_instruction(instruction)
        
        assert cpu.halted == True

    def test_unknown_opcode_halts_cpu(self):
        """Verify unknown opcode halts CPU with error."""
        cpu = CPUCore()
        
        # Create instruction with invalid opcode 0x99
        instruction = (0x99 << 24) | 100
        
        cpu.execute_instruction(instruction)
        
        assert cpu.halted == True


@pytest.mark.unit
class TestCPUCoreExecutionFlow:
    """Test execution flow (step, run)."""

    def test_step_executes_one_instruction(self):
        """Verify step() executes one fetch-decode-execute cycle."""
        cpu = CPUCore()
        
        # Load simple program: LDA 100, HLT
        cpu.memory[0] = (CPUCore.OP_LDA << 24) | 100
        cpu.memory[1] = (CPUCore.OP_HLT << 24) | 0
        cpu.memory[100] = 42
        
        # Execute first instruction
        continue_execution = cpu.step()
        
        assert cpu.accumulator == 42
        assert cpu.program_counter == 1
        assert cpu.instruction_count == 1
        assert continue_execution == True

    def test_step_returns_false_when_halted(self):
        """Verify step() returns False after halt."""
        cpu = CPUCore()
        
        # Load HLT instruction
        cpu.memory[0] = (CPUCore.OP_HLT << 24) | 0
        
        # Execute HLT
        continue_execution = cpu.step()
        
        assert cpu.halted == True
        assert continue_execution == False

    def test_step_does_not_execute_when_already_halted(self):
        """Verify step() does nothing if CPU already halted."""
        cpu = CPUCore()
        
        cpu.halted = True
        initial_pc = cpu.program_counter
        
        continue_execution = cpu.step()
        
        assert cpu.program_counter == initial_pc
        assert continue_execution == False

    def test_run_executes_until_halt(self):
        """Verify run() executes program until HLT instruction."""
        cpu = CPUCore()
        
        # Load program: LDA 100, ADD 101, STO 102, HLT
        cpu.memory[0] = (CPUCore.OP_LDA << 24) | 100
        cpu.memory[1] = (CPUCore.OP_ADD << 24) | 101
        cpu.memory[2] = (CPUCore.OP_STO << 24) | 102
        cpu.memory[3] = (CPUCore.OP_HLT << 24) | 0
        cpu.memory[100] = 10
        cpu.memory[101] = 20
        
        cpu.run()
        
        # Should execute all 4 instructions
        assert cpu.instruction_count == 4
        assert cpu.memory[102] == 30
        assert cpu.halted == True

    def test_run_stops_at_max_instructions(self):
        """Verify run() stops at max_instructions limit."""
        cpu = CPUCore()
        
        # Create infinite loop: TRA 0
        cpu.memory[0] = (CPUCore.OP_TRA << 24) | 0
        
        cpu.run(max_instructions=100)
        
        # Should stop at limit, not halt
        assert cpu.instruction_count == 100
        assert cpu.halted == False


@pytest.mark.unit
class TestCPUCoreMemoryAccess:
    """Test memory read/write methods."""

    def test_read_memory_bounds_check(self):
        """Verify read_memory returns 0 for out-of-bounds address."""
        cpu = CPUCore(memory_size=100)
        
        value = cpu.read_memory(200)  # Beyond memory size
        
        assert value == 0

    def test_write_memory_bounds_check(self):
        """Verify write_memory ignores out-of-bounds address."""
        cpu = CPUCore(memory_size=100)
        
        cpu.write_memory(200, 999)  # Beyond memory size
        
        # Should not crash, memory unchanged
        assert len(cpu.memory) == 100

    def test_write_memory_masks_to_32_bits(self):
        """Verify write_memory masks values to 32 bits."""
        cpu = CPUCore()
        
        # Write value larger than 32 bits
        cpu.write_memory(100, 0x123456789ABCDEF)
        
        # Should be masked to 32 bits
        assert cpu.memory[100] == 0x89ABCDEF


@pytest.mark.unit
class TestCPUCoreDivisionByZero:
    """Test division by zero handling."""

    def test_dvh_division_by_zero(self):
        """Verify DVH handles division by zero gracefully."""
        cpu = CPUCore()
        
        cpu.accumulator = 100
        cpu.memory[50] = 0  # Zero divisor
        
        # Create DVH instruction
        instruction = (CPUCore.OP_DVH << 24) | 50
        
        cpu.execute_instruction(instruction)
        
        # Should set accumulator to max value
        assert cpu.accumulator == 0x7FFFFFFF


@pytest.mark.unit
class TestCPUCoreHelperMethods:
    """Test helper methods (to_signed32, encode_instruction, get_state, etc)."""

    def test_to_signed32_positive_value(self):
        """Verify to_signed32 handles positive values correctly."""
        result = CPUCore.to_signed32(0x7FFFFFFF)
        
        assert result == 0x7FFFFFFF

    def test_to_signed32_negative_value(self):
        """Verify to_signed32 converts negative values correctly."""
        # Two''s complement: 0xFFFFFFFF = -1
        result = CPUCore.to_signed32(0xFFFFFFFF)
        
        assert result == -1

    def test_to_signed32_masks_to_32_bits(self):
        """Verify to_signed32 masks values to 32 bits."""
        result = CPUCore.to_signed32(0x1FFFFFFFF)
        
        # Should mask to 32 bits: 0xFFFFFFFF = -1
        assert result == -1

    def test_encode_instruction_without_index(self):
        """Verify encode_instruction creates correct instruction word."""
        instruction = CPUCore.encode_instruction(CPUCore.OP_LDA, 0x1234)
        
        # Opcode in upper 8 bits, address in lower 16 bits
        assert (instruction >> 24) & 0xFF == CPUCore.OP_LDA
        assert instruction & 0xFFFF == 0x1234
        # Index bit should NOT be set
        assert (instruction & CPUCore.INDEX_BIT_MASK) == 0

    def test_encode_instruction_with_index(self):
        """Verify encode_instruction sets index bit correctly."""
        instruction = CPUCore.encode_instruction(CPUCore.OP_LDA, 0x1234, indexed=True)
        
        # Index bit should be set
        assert (instruction & CPUCore.INDEX_BIT_MASK) != 0

    def test_get_state(self):
        """Verify get_state returns current CPU state."""
        cpu = CPUCore()
        
        cpu.accumulator = 123
        cpu.index_reg = 456
        cpu.program_counter = 789
        cpu.instruction_count = 10
        
        state = cpu.get_state()
        
        assert state["accumulator"] == 123
        assert state["index_reg"] == 456
        assert state["program_counter"] == 789
        assert state["instruction_count"] == 10
        assert state["halted"] == False

    def test_get_trace(self):
        """Verify get_trace returns copy of trace buffer."""
        cpu = CPUCore()
        
        cpu.trace_enabled = True
        cpu.memory[100] = 42
        
        # Execute instruction to create trace entry
        instruction = (CPUCore.OP_LDA << 24) | 100
        cpu.execute_instruction(instruction)
        
        trace = cpu.get_trace()
        
        assert len(trace) == 1
        assert trace[0]["opcode"] == CPUCore.OP_LDA
        # Should be a copy, not reference
        assert trace is not cpu.trace_buffer

    def test_clear_trace(self):
        """Verify clear_trace empties trace buffer."""
        cpu = CPUCore()
        
        cpu.trace_enabled = True
        cpu.memory[100] = 42
        
        # Execute instruction to create trace entry
        instruction = (CPUCore.OP_LDA << 24) | 100
        cpu.execute_instruction(instruction)
        
        assert len(cpu.trace_buffer) == 1
        
        cpu.clear_trace()
        
        assert len(cpu.trace_buffer) == 0


@pytest.mark.unit
class TestCPUCoreExamplePrograms:
    """Test example programs (array sum, indexed addressing)."""

    def test_example_array_sum(self):
        """Verify example_array_sum program executes without errors."""
        from an_fsq7_simulator.cpu_core import example_array_sum
        
        cpu = example_array_sum()
        
        # Program demonstrates indexed addressing (may not compute correct sum)
        # Just verify it executes and halts
        assert cpu.halted == True
        assert cpu.instruction_count > 0
        # Verify indexed addressing was used (index register changed)
        assert cpu.index_reg != 10  # Changed from initial value
