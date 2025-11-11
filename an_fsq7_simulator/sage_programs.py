"""
SAGE Program Examples - technical specification Style

These programs demonstrate the indexed addressing capability that is
essential to the AN/FSQ-7 instruction set. All examples follow the
pattern from technical specification of the SAGE programming manual.

Each program shows:
    op  base_addr(I)    ; effective_addr = base_addr + I
"""

from .cpu_core import CPUCore


class SAGEPrograms:
    """Collection of example SAGE programs demonstrating indexed addressing."""
    
    @staticmethod
    def array_sum_program():
        """
        Sum elements of an array using indexed addressing.
        
        Pseudocode:
            array[0..9] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
            sum = 0
            I = 0
            while I < 10:
                sum = sum + array[I]
                I = I + 1
                
        Assembly (SAGE style):
            LDA  ZERO       ; A = 0
            STO  SUM        ; sum = 0
            LDA  TEN        ; A = 10 (counter)
            
        LOOP:
            LDA  SUM        ; A = sum
            ADD  ARRAY(I)   ; A = sum + array[I]  <-- INDEXED!
            STO  SUM        ; sum = A
            TIX  LOOP       ; I--; if I>0 goto LOOP
            HLT
        """
        cpu = CPUCore()
        
        # Data: array at address 100
        array_data = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        for i, val in enumerate(array_data):
            cpu.write_memory(100 + i, val)
        
        # Constants
        cpu.write_memory(200, 0)    # ZERO
        cpu.write_memory(201, 0)    # SUM storage
        cpu.write_memory(202, 10)   # TEN
        
        # Program
        program = [
            # Initialize sum = 0
            CPUCore.encode_instruction(CPUCore.OP_LDA, 200),           # 0: A = 0
            CPUCore.encode_instruction(CPUCore.OP_STO, 201),           # 1: sum = 0
            CPUCore.encode_instruction(CPUCore.OP_LDA, 202),           # 2: A = 10
            
            # Loop (address 3)
            CPUCore.encode_instruction(CPUCore.OP_LDA, 201),           # 3: A = sum
            CPUCore.encode_instruction(CPUCore.OP_ADD, 100, indexed=True),  # 4: A += array[I]
            CPUCore.encode_instruction(CPUCore.OP_STO, 201),           # 5: sum = A
            CPUCore.encode_instruction(CPUCore.OP_TIX, 3),             # 6: I--; loop if I>0
            
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0),             # 7: HALT
        ]
        
        cpu.load_program(program, start_address=0)
        cpu.index_reg = len(array_data)  # Start with I = 10
        
        return cpu, {
            "name": "Array Sum",
            "description": "Sum array elements using indexed addressing",
            "expected_result": sum(array_data),
            "result_address": 201,
        }
    
    @staticmethod
    def array_search_program(search_value: int = 25):
        """
        Search for a value in an array using indexed addressing.
        
        Pseudocode:
            array[0..9] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
            search_for = 25
            I = 0
            found = -1
            while I < 10:
                if array[I] == search_for:
                    found = I
                    break
                I = I + 1
                
        Assembly:
            LDA  SEARCH     ; A = search value
            STO  TEMP
            
        LOOP:
            LDA  ARRAY(I)   ; A = array[I]  <-- INDEXED!
            SUB  TEMP       ; A = array[I] - search
            TNZ  NEXT       ; if A != 0 goto NEXT
            ; Found it!
            LDA  INDEX      ; A = I
            STO  RESULT     ; result = I
            HLT
            
        NEXT:
            TIX  LOOP       ; I--; if I>0 goto LOOP
            HLT
        """
        cpu = CPUCore()
        
        # Data: array at address 100
        array_data = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        for i, val in enumerate(array_data):
            cpu.write_memory(100 + i, val)
        
        # Constants and variables
        cpu.write_memory(200, search_value)  # SEARCH value
        cpu.write_memory(201, 0)             # TEMP
        cpu.write_memory(202, -1)            # RESULT (default -1 = not found)
        cpu.write_memory(203, 10)            # Array length
        
        # Program
        program = [
            # Initialize
            CPUCore.encode_instruction(CPUCore.OP_LDA, 200),           # 0: A = search_value
            CPUCore.encode_instruction(CPUCore.OP_STO, 201),           # 1: temp = search_value
            
            # Loop (address 2)
            CPUCore.encode_instruction(CPUCore.OP_LDA, 100, indexed=True),  # 2: A = array[I]
            CPUCore.encode_instruction(CPUCore.OP_SUB, 201),           # 3: A = A - temp
            CPUCore.encode_instruction(CPUCore.OP_TNZ, 7),             # 4: if A!=0 goto NEXT
            
            # Found it! Save index
            CPUCore.encode_instruction(CPUCore.OP_LDA, 204),           # 5: A = I (from memory)
            CPUCore.encode_instruction(CPUCore.OP_STO, 202),           # 6: result = I
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0),             # 7: HALT (found)
            
            # NEXT: continue loop
            CPUCore.encode_instruction(CPUCore.OP_TIX, 2),             # 8: I--; loop if I>0
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0),             # 9: HALT (not found)
        ]
        
        cpu.load_program(program, start_address=0)
        cpu.index_reg = len(array_data)  # Start with I = 10
        cpu.write_memory(204, cpu.index_reg)  # Store I value for saving
        
        expected_index = array_data.index(search_value) if search_value in array_data else -1
        
        return cpu, {
            "name": "Array Search",
            "description": f"Search for value {search_value} using indexed addressing",
            "expected_result": expected_index,
            "result_address": 202,
        }
    
    @staticmethod
    def array_copy_program():
        """
        Copy one array to another using indexed addressing.
        
        Pseudocode:
            src[0..4] = [10, 20, 30, 40, 50]
            dst[0..4] = [0, 0, 0, 0, 0]
            I = 0
            while I < 5:
                dst[I] = src[I]
                I = I + 1
                
        Assembly:
            LDA  FIVE       ; A = 5 (counter)
            
        LOOP:
            LDA  SRC(I)     ; A = src[I]  <-- INDEXED!
            STO  DST(I)     ; dst[I] = A  <-- INDEXED!
            TIX  LOOP       ; I--; if I>0 goto LOOP
            HLT
        """
        cpu = CPUCore()
        
        # Source array at address 100
        src_data = [10, 20, 30, 40, 50]
        for i, val in enumerate(src_data):
            cpu.write_memory(100 + i, val)
        
        # Destination array at address 150 (initially zero)
        for i in range(len(src_data)):
            cpu.write_memory(150 + i, 0)
        
        # Constants
        cpu.write_memory(200, len(src_data))  # Array length
        
        # Program
        program = [
            # Initialize counter
            CPUCore.encode_instruction(CPUCore.OP_LDA, 200),           # 0: A = 5
            
            # Loop (address 1)
            CPUCore.encode_instruction(CPUCore.OP_LDA, 100, indexed=True),  # 1: A = src[I]
            CPUCore.encode_instruction(CPUCore.OP_STO, 150, indexed=True),  # 2: dst[I] = A
            CPUCore.encode_instruction(CPUCore.OP_TIX, 1),             # 3: I--; loop if I>0
            
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0),             # 4: HALT
        ]
        
        cpu.load_program(program, start_address=0)
        cpu.index_reg = len(src_data)  # Start with I = 5
        
        return cpu, {
            "name": "Array Copy",
            "description": "Copy array using indexed addressing on both load and store",
            "expected_result": src_data,
            "result_address": 150,
            "result_length": len(src_data),
        }
    
    @staticmethod
    def nested_loop_program():
        """
        Nested loop example: Initialize a 3x3 matrix.
        
        This demonstrates more complex indexed addressing patterns.
        
        Pseudocode:
            matrix = [[0]*3 for _ in range(3)]
            value = 1
            for row in range(3):
                for col in range(3):
                    matrix[row][col] = value
                    value = value + 1
                    
        In SAGE, this uses index register manipulation for 2D addressing.
        """
        cpu = CPUCore()
        
        # Matrix at address 100 (3x3 = 9 words)
        matrix_base = 100
        matrix_size = 9
        
        # Initialize matrix to zeros
        for i in range(matrix_size):
            cpu.write_memory(matrix_base + i, 0)
        
        # Constants
        cpu.write_memory(200, 1)   # Initial value
        cpu.write_memory(201, 0)   # Current value storage
        cpu.write_memory(202, 9)   # Counter (9 elements)
        
        # Program - simplified version treating matrix as linear array
        program = [
            # Initialize
            CPUCore.encode_instruction(CPUCore.OP_LDA, 200),           # 0: A = 1
            CPUCore.encode_instruction(CPUCore.OP_STO, 201),           # 1: value = 1
            CPUCore.encode_instruction(CPUCore.OP_LDA, 202),           # 2: A = 9
            
            # Loop (address 3)
            CPUCore.encode_instruction(CPUCore.OP_LDA, 201),           # 3: A = value
            CPUCore.encode_instruction(CPUCore.OP_STO, 100, indexed=True),  # 4: matrix[I] = value
            CPUCore.encode_instruction(CPUCore.OP_ADD, 200),           # 5: A = value + 1
            CPUCore.encode_instruction(CPUCore.OP_STO, 201),           # 6: value = A
            CPUCore.encode_instruction(CPUCore.OP_TIX, 3),             # 7: I--; loop if I>0
            
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0),             # 8: HALT
        ]
        
        cpu.load_program(program, start_address=0)
        cpu.index_reg = matrix_size  # Start with I = 9
        
        return cpu, {
            "name": "Matrix Initialization",
            "description": "Fill 3x3 matrix using indexed addressing",
            "expected_result": list(range(1, 10)),
            "result_address": 100,
            "result_length": 9,
        }
    
    @staticmethod
    def get_all_programs():
        """Get all available example programs."""
        return {
            "array_sum": SAGEPrograms.array_sum_program,
            "array_search": SAGEPrograms.array_search_program,
            "array_copy": SAGEPrograms.array_copy_program,
            "nested_loop": SAGEPrograms.nested_loop_program,
        }


def run_program_example(program_func, verbose=True):
    """
    Run a SAGE program example and display results.
    
    Args:
        program_func: Function that returns (cpu, metadata)
        verbose: Print detailed trace
    """
    cpu, metadata = program_func()
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"Program: {metadata['name']}")
        print(f"Description: {metadata['description']}")
        print(f"{'='*60}")
    
    # Enable tracing
    cpu.trace_enabled = True
    
    # Run the program
    cpu.run(max_instructions=1000)
    
    # Get results
    if "result_length" in metadata:
        # Multiple result words
        results = [cpu.read_memory(metadata["result_address"] + i) 
                  for i in range(metadata["result_length"])]
        actual_result = results
    else:
        # Single result word
        actual_result = cpu.read_memory(metadata["result_address"])
    
    # Display results
    if verbose:
        print(f"\nFinal CPU State:")
        print(f"  Accumulator (A): {cpu.accumulator}")
        print(f"  Index Register (I): {cpu.index_reg}")
        print(f"  Program Counter (P): {cpu.program_counter}")
        print(f"  Instructions executed: {cpu.instruction_count}")
        print(f"\nResults:")
        print(f"  Expected: {metadata['expected_result']}")
        print(f"  Actual:   {actual_result}")
        print(f"  Match: {'✓ PASS' if actual_result == metadata['expected_result'] else '✗ FAIL'}")
        
        # Show trace of indexed instructions
        print(f"\nIndexed Address Trace (showing effective_addr = base + I):")
        for entry in cpu.get_trace():
            if entry["indexed"]:
                print(f"  PC={entry['pc']:3d}  OP=0x{entry['opcode']:02X}  "
                      f"base={entry['raw_addr']:4d} + I={entry['index_before']:2d} "
                      f"= effective={entry['effective_addr']:4d}")
    
    return cpu, actual_result == metadata["expected_result"]


if __name__ == "__main__":
    """Run all example programs to demonstrate indexed addressing."""
    
    print("AN/FSQ-7 SAGE Programs - Indexed Addressing Demonstrations")
    print("technical specification Example Programs")
    print("")
    
    all_programs = SAGEPrograms.get_all_programs()
    results = {}
    
    for name, program_func in all_programs.items():
        cpu, passed = run_program_example(program_func, verbose=True)
        results[name] = passed
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    total = len(results)
    passed = sum(results.values())
    print(f"Tests passed: {passed}/{total}")
    for name, status in results.items():
        print(f"  {name:20s} {'✓ PASS' if status else '✗ FAIL'}")
    
    if passed == total:
        print("\n✓ All indexed addressing examples working correctly!")
        print("  The AN/FSQ-7 CPU core properly implements:")
        print("    • effective_address = base_address + I")
        print("    • Index register (I) for loop counters")
        print("    • Indexed load: LDA base(I)")
        print("    • Indexed store: STO base(I)")
        print("    • Loop control: TIX (Transfer on Index)")
