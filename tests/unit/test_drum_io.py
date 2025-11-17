"""
Unit tests for AN/FSQ-7 Drum I/O System.

Tests authentic drum-buffered asynchronous I/O architecture with field-based storage
and status channel polling.
"""

import pytest
from an_fsq7_simulator import drum_io_system


@pytest.mark.unit
class TestDrumIO:
    """Test drum I/O system for asynchronous data transfer."""

    def test_drum_initialization(self):
        """Verify drum initializes with all fields empty."""
        drum = drum_io_system.MagneticDrum()
        
        # All drum fields should exist
        for field in drum_io_system.DrumField:
            assert field in drum.fields
            assert len(drum.fields[field]) == 0

    def test_write_read_field(self):
        """Verify writing and reading from drum field."""
        drum = drum_io_system.MagneticDrum()
        
        # Write to LRI field (Long Range Input - radar data)
        address = 100
        data = 0x1234ABCD
        
        drum.write_field(drum_io_system.DrumField.LRI, address, data)
        read_data = drum.read_field(drum_io_system.DrumField.LRI, address)
        
        assert read_data == data

    def test_status_channel_set_on_write(self):
        """Verify status channel is set when external device writes."""
        drum = drum_io_system.MagneticDrum()
        
        # Initially status channel should be clear
        assert drum.check_status(drum_io_system.StatusChannel.OD_LRI) == False
        
        # External device writes to LRI field
        drum.write_field(drum_io_system.DrumField.LRI, 0, 0x1111)
        
        # Status channel should now be set
        assert drum.check_status(drum_io_system.StatusChannel.OD_LRI) == True

    def test_status_channel_clearing(self):
        """Verify CPU can clear status channel after reading data."""
        drum = drum_io_system.MagneticDrum()
        
        # External device writes data
        drum.write_field(drum_io_system.DrumField.GFI, 0, 0x2222)
        assert drum.check_status(drum_io_system.StatusChannel.OD_GFI) == True
        
        # CPU reads data and clears status
        data = drum.read_field(drum_io_system.DrumField.GFI, 0)
        drum.clear_status(drum_io_system.StatusChannel.OD_GFI)
        
        # Status channel should now be clear
        assert drum.check_status(drum_io_system.StatusChannel.OD_GFI) == False

    def test_multiple_fields_independent(self):
        """Verify different drum fields are independent."""
        drum = drum_io_system.MagneticDrum()
        
        # Write to different fields at same address
        address = 50
        drum.write_field(drum_io_system.DrumField.LRI, address, 0xAAAA)
        drum.write_field(drum_io_system.DrumField.GFI, address, 0xBBBB)
        drum.write_field(drum_io_system.DrumField.XTL, address, 0xCCCC)
        
        # Read back - each field should have its own data
        assert drum.read_field(drum_io_system.DrumField.LRI, address) == 0xAAAA
        assert drum.read_field(drum_io_system.DrumField.GFI, address) == 0xBBBB
        assert drum.read_field(drum_io_system.DrumField.XTL, address) == 0xCCCC

    def test_read_unwritten_address_returns_none(self):
        """Verify reading from unwritten address returns None."""
        drum = drum_io_system.MagneticDrum()
        
        # Read from address that was never written
        data = drum.read_field(drum_io_system.DrumField.LRI, 9999)
        
        assert data is None

    def test_overwrite_field_data(self):
        """Verify data in field can be overwritten."""
        drum = drum_io_system.MagneticDrum()
        
        address = 100
        
        drum.write_field(drum_io_system.DrumField.LOG, address, 0x1111)
        assert drum.read_field(drum_io_system.DrumField.LOG, address) == 0x1111
        
        drum.write_field(drum_io_system.DrumField.LOG, address, 0x2222)
        assert drum.read_field(drum_io_system.DrumField.LOG, address) == 0x2222

    def test_transfer_log_records_writes(self):
        """Verify transfer log records all write operations."""
        drum = drum_io_system.MagneticDrum()
        
        initial_count = len(drum.transfer_log)
        
        # Write 3 times
        drum.write_field(drum_io_system.DrumField.LRI, 0, 0x1111, 1.0)
        drum.write_field(drum_io_system.DrumField.LRI, 1, 0x2222, 2.0)
        drum.write_field(drum_io_system.DrumField.GFI, 0, 0x3333, 3.0)
        
        # Log should have 3 new entries
        assert len(drum.transfer_log) == initial_count + 3

    def test_drum_rotation_simulation(self):
        """Verify drum rotation updates correctly."""
        drum = drum_io_system.MagneticDrum()
        
        initial_angle = drum.rotation_angle
        
        # Tick forward 1 second
        drum.tick(1.0)
        
        # At 3600 RPM, drum rotates 60 times per second = 21,600 degrees/sec
        # After 1 second, angle should advance by 21,600 degrees (60 full rotations)
        # Which is 21,600 % 360 = 0 degrees
        assert drum.rotation_angle == 0.0

    def test_cross_tell_field_status(self):
        """Verify Cross-Tell (XTL) field status channel works."""
        drum = drum_io_system.MagneticDrum()
        
        # Write to XTL field (data from other SAGE sites)
        drum.write_field(drum_io_system.DrumField.XTL, 42, 0xCAFE)
        
        # XTL status channel should be set
        assert drum.check_status(drum_io_system.StatusChannel.OD_XTL) == True


@pytest.mark.unit  
class TestLightGunSystem:
    """Test authentic light gun photomultiplier system."""

    def test_light_gun_starts_disarmed(self):
        """Verify light gun starts in disarmed state."""
        gun = drum_io_system.LightGunSystem()
        
        assert gun.armed == False
        assert gun.flash_detected == False

    def test_light_gun_arm(self):
        """Verify arming light gun sets position."""
        gun = drum_io_system.LightGunSystem()
        
        gun.arm(100, 200)
        
        assert gun.armed == True
        assert gun.gun_x == 100
        assert gun.gun_y == 200

    def test_light_gun_disarm(self):
        """Verify disarming light gun."""
        gun = drum_io_system.LightGunSystem()
        
        gun.arm(100, 200)
        gun.disarm()
        
        assert gun.armed == False

    def test_draw_event_no_flash_when_disarmed(self):
        """Verify no flash detection when gun is disarmed."""
        gun = drum_io_system.LightGunSystem()
        
        # Gun is disarmed, draw at any position
        flash = gun.draw_event("TRK-001", 100, 200)
        
        assert flash == False

    def test_draw_event_flash_when_beam_hits_gun(self):
        """Verify flash detection when beam passes through gun position."""
        gun = drum_io_system.LightGunSystem()
        
        # Arm gun at position 100, 200
        gun.arm(100, 200)
        
        # Draw object very close to gun position
        flash = gun.draw_event("TRK-001", 102, 198, radius=20)
        
        assert flash == True

    def test_draw_event_no_flash_when_beam_misses(self):
        """Verify no flash when beam is far from gun position."""
        gun = drum_io_system.LightGunSystem()
        
        # Arm gun at 100, 200
        gun.arm(100, 200)
        
        # Draw object far away
        flash = gun.draw_event("TRK-001", 500, 500, radius=20)
        
        assert flash == False
