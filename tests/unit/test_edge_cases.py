"""
Edge case tests for SAGE simulator modules.

Tests boundary conditions, error handling, and unusual inputs.
"""

import pytest
import math
from an_fsq7_simulator.cpu_core import CPUCore
from an_fsq7_simulator.sim.models import (
    RadarTarget,
    VacuumTubeBank,
    Interceptor
)
from an_fsq7_simulator.state_model import Track, Interceptor as StateInterceptor


@pytest.mark.unit
class TestCPUEdgeCases:
    """Edge case tests for CPU core."""

    def test_cpu_maximum_memory_address(self):
        """Verify CPU handles maximum memory address."""
        cpu = CPUCore()
        max_addr = 32767
        
        cpu.write_memory(max_addr, 42)
        result = cpu.read_memory(max_addr)
        
        assert result == 42

    def test_cpu_zero_address(self):
        """Verify CPU handles address zero."""
        cpu = CPUCore()
        
        cpu.write_memory(0, 123)
        result = cpu.read_memory(0)
        
        assert result == 123

    def test_cpu_accumulator_overflow(self):
        """Verify CPU handles accumulator overflow."""
        cpu = CPUCore()
        
        # Set accumulator to large value
        cpu.accumulator = 0x7FFFFFFF
        cpu.write_memory(100, 1)
        
        program = [
            CPUCore.encode_instruction(CPUCore.OP_LDA, 100),
            CPUCore.encode_instruction(CPUCore.OP_ADD, 100),
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0)
        ]
        
        cpu.load_program(program, start_address=0)
        cpu.run(max_instructions=100)
        
        # Should handle overflow (32-bit arithmetic)
        assert cpu.halted

    def test_cpu_index_register_zero(self):
        """Verify CPU handles index register at zero."""
        cpu = CPUCore()
        cpu.index_reg = 0
        
        cpu.write_memory(100, 42)
        
        # Indexed load with I=0
        program = [
            CPUCore.encode_instruction(CPUCore.OP_LDA, 100, indexed=True),
            CPUCore.encode_instruction(CPUCore.OP_HLT, 0)
        ]
        
        cpu.load_program(program, start_address=0)
        cpu.run(max_instructions=100)
        
        # Should load from address 100+0 = 100
        assert cpu.accumulator == 42

    def test_cpu_empty_program(self):
        """Verify CPU handles empty program."""
        cpu = CPUCore()
        
        cpu.load_program([], start_address=0)
        cpu.run(max_instructions=10)
        
        # Should not crash
        assert cpu.instruction_count >= 0

    def test_cpu_run_with_max_instructions_zero(self):
        """Verify CPU handles max_instructions=0."""
        cpu = CPUCore()
        
        program = [CPUCore.encode_instruction(CPUCore.OP_HLT, 0)]
        cpu.load_program(program, start_address=0)
        
        cpu.run(max_instructions=0)
        
        # Should execute no instructions
        assert cpu.instruction_count == 0


@pytest.mark.unit
class TestRadarTargetEdgeCases:
    """Edge case tests for RadarTarget."""

    def test_radar_target_zero_speed(self):
        """Verify RadarTarget handles zero speed."""
        target = RadarTarget(
            target_id="T-001",
            x=400, y=300,
            heading=90, speed=0,
            altitude=30000
        )
        
        initial_x, initial_y = target.x, target.y
        target.move(1.0)
        
        # Should barely move (speed_factor near zero)
        assert abs(target.x - initial_x) < 0.1
        assert abs(target.y - initial_y) < 0.1

    def test_radar_target_negative_coordinates(self):
        """Verify RadarTarget wraps negative coordinates."""
        target = RadarTarget(
            target_id="T-001",
            x=-10, y=-10,
            heading=0, speed=500,
            altitude=30000
        )
        
        target.wrap_bounds(800, 600)
        
        # Should wrap to positive
        assert target.x >= 0
        assert target.y >= 0

    def test_radar_target_distance_to_self(self):
        """Verify RadarTarget distance to itself is zero."""
        target = RadarTarget(
            target_id="T-001",
            x=400, y=300,
            heading=0, speed=500,
            altitude=30000
        )
        
        dist = target.distance_to(400, 300)
        
        assert dist == 0

    def test_radar_target_large_altitude(self):
        """Verify RadarTarget handles large altitude."""
        target = RadarTarget(
            target_id="T-001",
            x=400, y=300,
            heading=0, speed=500,
            altitude=100000  # Very high
        )
        
        assert target.altitude == 100000


@pytest.mark.unit
class TestVacuumTubeBankEdgeCases:
    """Edge case tests for VacuumTubeBank."""

    def test_tube_bank_zero_tubes(self):
        """Verify VacuumTubeBank handles zero tubes."""
        bank = VacuumTubeBank(total_tubes=0)
        
        bank.warm_up(1.0)
        
        # Should not crash
        assert bank.active_tubes == 0

    def test_tube_bank_negative_warmup_time(self):
        """Verify VacuumTubeBank handles negative dt."""
        bank = VacuumTubeBank()
        
        initial_temp = bank.temperature
        bank.warm_up(-1.0)
        
        # With negative dt, temperature can go negative (edge case)
        # This documents the behavior
        assert isinstance(bank.temperature, float)

    def test_tube_bank_already_warmed(self):
        """Verify VacuumTubeBank handles already-warmed state."""
        bank = VacuumTubeBank()
        bank.temperature = bank.target_temperature
        
        bank.warm_up(1.0)
        
        # Temperature should not exceed target
        assert bank.temperature <= bank.target_temperature * 1.01

    def test_tube_bank_is_ready_at_95_percent(self):
        """Verify VacuumTubeBank is ready at 95% temperature."""
        bank = VacuumTubeBank()
        bank.temperature = bank.target_temperature * 0.95
        
        assert bank.is_ready()

    def test_tube_bank_tick_failures(self):
        """Verify VacuumTubeBank tick can handle tube failures."""
        bank = VacuumTubeBank()
        bank.active_tubes = 58000
        
        initial_failed = bank.failed_tubes
        
        # Run many ticks to potentially trigger failures
        for _ in range(100):
            bank.tick(1.0)
        
        # Failed tubes should not exceed total
        assert bank.failed_tubes <= bank.total_tubes


@pytest.mark.unit
class TestInterceptorEdgeCases:
    """Edge case tests for sim Interceptor."""

    def test_sim_interceptor_distance_calculation(self):
        """Verify sim Interceptor distance calculation."""
        interceptor = Interceptor(
            interceptor_id="INT-001",
            aircraft_type="F-106",
            base_name="Otis AFB",
            base_x=0.1,
            base_y=0.1,
            x=0.5,
            y=0.5
        )
        
        distance = interceptor.distance_to_target(0.6, 0.6)
        
        # Distance should be roughly sqrt(0.1^2 + 0.1^2) = ~0.141
        assert 0.14 < distance < 0.15

    def test_sim_interceptor_zero_distance(self):
        """Verify sim Interceptor at target location."""
        interceptor = Interceptor(
            interceptor_id="INT-002",
            aircraft_type="F-102",
            base_name="Hanscom",
            base_x=0.2,
            base_y=0.2,
            x=0.8,
            y=0.8
        )
        
        # Distance to self should be zero
        distance = interceptor.distance_to_target(0.8, 0.8)
        assert distance == 0.0


@pytest.mark.unit
class TestTrackEdgeCases:
    """Edge case tests for Track state model."""

    def test_track_minimum_fields(self):
        """Verify Track with minimum required fields."""
        track = Track(
            id="T-001",
            x=0.5,
            y=0.5,
            altitude=30000,
            speed=500,
            heading=180
        )
        
        assert track.id == "T-001"
        assert track.track_type == "unknown"  # Default (lowercase)

    def test_track_normalized_coordinates(self):
        """Verify Track handles normalized coordinates."""
        track = Track(
            id="T-001",
            x=1.0,
            y=1.0,
            altitude=30000,
            speed=500,
            heading=180
        )
        
        # Coordinates should be at boundary
        assert track.x == 1.0
        assert track.y == 1.0

    def test_track_zero_altitude(self):
        """Verify Track with zero altitude."""
        track = Track(
            id="T-001",
            x=0.5,
            y=0.5,
            altitude=0,
            speed=500,
            heading=180
        )
        
        assert track.altitude == 0

    def test_track_360_degree_heading(self):
        """Verify Track with 360-degree heading."""
        track = Track(
            id="T-001",
            x=0.5,
            y=0.5,
            altitude=30000,
            speed=500,
            heading=360
        )
        
        assert track.heading == 360


@pytest.mark.unit
class TestStateInterceptorEdgeCases:
    """Edge case tests for state model interceptor."""

    def test_state_interceptor_has_fields(self):
        """Verify StateInterceptor has required fields."""
        interceptor = StateInterceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Otis AFB",
            base_x=0.1,
            base_y=0.1,
            x=0.5,
            y=0.9,
            status="AIRBORNE",
            altitude=40000,
            current_speed=600,
            heading=270,
            fuel_percent=85,
            assigned_target_id="TGT-001"
        )
        
        assert interceptor.id == "INT-001"
        assert interceptor.aircraft_type == "F-106 Delta Dart"
        assert interceptor.base_name == "Otis AFB"
        assert interceptor.assigned_target_id == "TGT-001"
