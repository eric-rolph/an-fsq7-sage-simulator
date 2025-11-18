"""
Additional tests for FSQ7_IO_System integration.

Tests the integrated drum and light gun I/O system.
"""

import pytest
from an_fsq7_simulator.drum_io_system import (
    FSQ7_IO_System,
    DrumField,
    StatusChannel
)


@pytest.mark.unit
class TestFSQ7IOSystem:
    """Test integrated FSQ7 I/O system."""

    def test_fsq7_io_system_initialization(self):
        """Verify FSQ7_IO_System initializes correctly."""
        io_system = FSQ7_IO_System()
        
        assert io_system.drum is not None
        assert io_system.light_gun is not None

    def test_simulate_radar_input(self):
        """Verify simulate_radar_input writes to LRI field."""
        io_system = FSQ7_IO_System()
        
        targets = [
            {"x": 100, "y": 200, "altitude": 30000, "speed": 450},
            {"x": 150, "y": 250, "altitude": 35000, "speed": 500},
        ]
        
        io_system.simulate_radar_input(targets, timestamp=0.0)
        
        # Verify status channel set
        assert io_system.drum.check_status(StatusChannel.OD_LRI) == True

    def test_cpu_poll_loop_radar_data(self):
        """Verify CPU can poll and read radar data."""
        io_system = FSQ7_IO_System()
        
        # Simulate radar input
        targets = [
            {"x": 100, "y": 200, "altitude": 30000, "speed": 450},
        ]
        io_system.simulate_radar_input(targets, timestamp=0.0)
        
        # CPU polls
        cpu_data = io_system.cpu_poll_loop({})
        
        # Verify data received
        assert cpu_data is not None
        assert "radar_targets" in cpu_data
        assert len(cpu_data["radar_targets"]) == 1
        
        # Verify status cleared
        assert io_system.drum.check_status(StatusChannel.OD_LRI) == False

    def test_cpu_poll_loop_light_gun_selection(self):
        """Verify CPU can poll light gun selection."""
        io_system = FSQ7_IO_System()
        
        # Arm light gun
        io_system.light_gun.arm(100, 200)
        
        # Draw target that triggers flash
        flash = io_system.light_gun.draw_event("TGT-1", 100, 200, radius=20)
        assert flash == True
        
        # Set status channel (hardware would do this)
        io_system.drum.status_channels[StatusChannel.LIGHT_GUN] = True
        
        # CPU polls
        cpu_data = io_system.cpu_poll_loop({})
        
        # Verify selection received
        assert cpu_data is not None
        assert "light_gun_selection" in cpu_data
        assert cpu_data["light_gun_selection"] == "TGT-1"
        
        # Verify status cleared
        assert io_system.drum.check_status(StatusChannel.LIGHT_GUN) == False
        assert io_system.light_gun.get_selected_id() is None

    def test_cpu_poll_loop_no_data(self):
        """Verify CPU poll returns None when no data available."""
        io_system = FSQ7_IO_System()
        
        # Poll without any input
        cpu_data = io_system.cpu_poll_loop({})
        
        # Should return None
        assert cpu_data is None

    def test_cpu_poll_loop_multiple_sources(self):
        """Verify CPU can poll multiple I/O sources."""
        io_system = FSQ7_IO_System()
        
        # Simulate radar input
        targets = [{"x": 100, "y": 200, "altitude": 30000, "speed": 450}]
        io_system.simulate_radar_input(targets, timestamp=0.0)
        
        # Arm light gun and trigger selection
        io_system.light_gun.arm(100, 200)
        io_system.light_gun.draw_event("TGT-1", 100, 200, radius=20)
        io_system.drum.status_channels[StatusChannel.LIGHT_GUN] = True
        
        # CPU polls
        cpu_data = io_system.cpu_poll_loop({})
        
        # Verify both sources read
        assert cpu_data is not None
        assert "radar_targets" in cpu_data
        assert "light_gun_selection" in cpu_data

    def test_io_system_tick(self):
        """Verify tick updates drum timing."""
        io_system = FSQ7_IO_System()
        
        initial_rotation = io_system.drum.rotation_angle
        
        # Tick forward with sufficient time to see change
        io_system.tick(0.001)
        
        # Rotation should advance (drum spins at 3600 RPM)
        assert io_system.drum.rotation_angle > initial_rotation

    def test_radar_input_empty_list(self):
        """Verify simulate_radar_input handles empty target list."""
        io_system = FSQ7_IO_System()
        
        # Simulate with no targets - no writes, so no status bit set
        io_system.simulate_radar_input([], timestamp=0.0)
        
        # Status bit should NOT be set (no writes happened)
        assert io_system.drum.check_status(StatusChannel.OD_LRI) == False

    def test_cpu_poll_reads_multiple_radar_targets(self):
        """Verify CPU poll can read multiple radar targets."""
        io_system = FSQ7_IO_System()
        
        # Simulate with multiple targets
        targets = [
            {"x": 100, "y": 200, "altitude": 30000, "speed": 450},
            {"x": 150, "y": 250, "altitude": 35000, "speed": 500},
            {"x": 200, "y": 300, "altitude": 40000, "speed": 550},
        ]
        io_system.simulate_radar_input(targets, timestamp=0.0)
        
        # CPU polls
        cpu_data = io_system.cpu_poll_loop({})
        
        # Verify all targets received
        assert cpu_data is not None
        assert len(cpu_data["radar_targets"]) == 3

    def test_light_gun_poll_without_armed(self):
        """Verify light gun poll when not armed."""
        io_system = FSQ7_IO_System()
        
        # Draw without arming
        flash = io_system.light_gun.draw_event("TGT-1", 100, 200, radius=20)
        assert flash == False
        
        # Set status anyway
        io_system.drum.status_channels[StatusChannel.LIGHT_GUN] = True
        
        # CPU polls
        cpu_data = io_system.cpu_poll_loop({})
        
        # Should clear status but no selection
        assert io_system.drum.check_status(StatusChannel.LIGHT_GUN) == False


@pytest.mark.unit
class TestLightGunSystemAdditional:
    """Additional light gun tests."""

    def test_light_gun_get_selected_id_when_not_armed(self):
        """Verify get_selected_id returns None when not armed."""
        from an_fsq7_simulator.drum_io_system import LightGunSystem
        
        gun = LightGunSystem()
        
        # Not armed, no flash
        selected = gun.get_selected_id()
        
        assert selected is None

    def test_light_gun_clear_status(self):
        """Verify clear_status resets flash state."""
        from an_fsq7_simulator.drum_io_system import LightGunSystem
        
        gun = LightGunSystem()
        
        # Arm and trigger flash
        gun.arm(100, 200)
        gun.draw_event("TGT-1", 100, 200, radius=20)
        
        # Verify flash detected
        assert gun.poll_status() == True
        assert gun.get_selected_id() == "TGT-1"
        
        # Clear status
        gun.clear_status()
        
        # Verify cleared
        assert gun.poll_status() == False
        assert gun.get_selected_id() is None


@pytest.mark.unit
class TestDrumIOSystemMainFunction:
    """Test drum_io_system.py main test function."""

    def test_drum_io_system_test_function_runs(self):
        """Verify test_drum_io_system() executes without errors."""
        from an_fsq7_simulator import drum_io_system
        
        # Should not raise exception
        drum_io_system.test_drum_io_system()
