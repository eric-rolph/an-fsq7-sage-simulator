"""
AN/FSQ-7 Magnetic Drum I/O System

This implements the authentic drum-buffered asynchronous I/O architecture
that was fundamental to SAGE operation. The drum acted as a "decoupler"
between the central computer and all external devices.

Key architectural features:
- Magnetic drum as intermediary storage
- Asynchronous data transfer (external hardware writes to drum)
- Status channel polling (CPU checks flags to detect new data)
- Dedicated drum fields for different input types (LRI, GFI, XTL)
- No direct I/O between CPU and external devices
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import IntEnum


# ============================================================================
# Drum Field Definitions
# ============================================================================

class DrumField(IntEnum):
    """Magnetic drum field assignments"""
    LRI = 0      # Long Range Input (radar data)
    GFI = 1      # Ground Forward Input (ground radar)
    XTL = 2      # Cross-Tell (data from other SAGE sites)
    SDC = 3      # Scope Display Control (light gun, console inputs)
    LOG = 4      # Log drum (general storage)
    TMP = 5      # Temporary working storage


class StatusChannel(IntEnum):
    """Status channel bit assignments for polling"""
    CD_LRI = 0   # Core-to-Drum LRI transfer complete
    CD_GFI = 1   # Core-to-Drum GFI transfer complete
    CD_XTL = 2   # Core-to-Drum XTL transfer complete
    OD_LRI = 3   # Output-Drum LRI data available
    OD_GFI = 4   # Output-Drum GFI data available
    OD_XTL = 5   # Output-Drum XTL data available
    LIGHT_GUN = 6  # Light gun flash detected


@dataclass
class DrumRecord:
    """Single record on the magnetic drum"""
    field: DrumField
    address: int          # Word address within field
    data: int             # 32-bit word
    timestamp: float      # When data was written


# ============================================================================
# Magnetic Drum Storage
# ============================================================================

class MagneticDrum:
    """
    AN/FSQ-7 Magnetic Drum System
    
    The drum is THE critical component that made SAGE work. It:
    - Buffered all input/output operations
    - Decoupled real-time devices from batch processing
    - Provided asynchronous data exchange
    - Enabled polled I/O instead of interrupts
    
    External hardware (radar, cross-tell) writes to drum fields.
    CPU polls status channels to detect new data.
    CPU reads from drum fields when status indicates data ready.
    """
    
    def __init__(self):
        # Drum storage organized by fields
        self.fields: Dict[DrumField, Dict[int, int]] = {
            field: {} for field in DrumField
        }
        
        # Status channel flip-flops (polled by CPU)
        self.status_channels: Dict[StatusChannel, bool] = {
            channel: False for channel in StatusChannel
        }
        
        # Transfer log for debugging
        self.transfer_log: List[DrumRecord] = []
        
        # Drum rotation simulation (for authentic timing)
        self.rotation_angle = 0.0  # 0-360 degrees
        self.rpm = 3600  # 3600 RPM = 60 Hz
    
    def write_field(self, field: DrumField, address: int, data: int, timestamp: float = 0.0):
        """
        Write data to drum field (external hardware operation).
        
        This simulates external devices (radar, cross-tell) writing
        to the drum asynchronously.
        """
        self.fields[field][address] = data
        self.transfer_log.append(DrumRecord(field, address, data, timestamp))
        
        # Set appropriate status channel based on field
        if field == DrumField.LRI:
            self.status_channels[StatusChannel.OD_LRI] = True
        elif field == DrumField.GFI:
            self.status_channels[StatusChannel.OD_GFI] = True
        elif field == DrumField.XTL:
            self.status_channels[StatusChannel.OD_XTL] = True
    
    def read_field(self, field: DrumField, address: int) -> Optional[int]:
        """
        Read data from drum field (CPU operation).
        
        CPU uses this after polling status channels.
        """
        return self.fields[field].get(address, None)
    
    def check_status(self, channel: StatusChannel) -> bool:
        """
        Poll status channel (CPU operation).
        
        This is how the CPU detects new data availability.
        Original SAGE software had polling loops checking these bits.
        """
        return self.status_channels.get(channel, False)
    
    def clear_status(self, channel: StatusChannel):
        """
        Clear status channel bit (CPU operation after reading data).
        
        CPU must explicitly clear the bit after processing data.
        """
        self.status_channels[channel] = False
    
    def tick(self, dt: float):
        """Update drum rotation (for timing simulation)"""
        degrees_per_second = self.rpm * 6.0
        self.rotation_angle = (self.rotation_angle + degrees_per_second * dt) % 360.0


# ============================================================================
# Light Gun System
# ============================================================================

class LightGunSystem:
    """
    Authentic light gun implementation with polling.
    
    The real hardware:
    1. Light gun has photomultiplier tube
    2. Trigger pull arms the gun
    3. CRT electron beam draws targets
    4. When beam hits armed gun position, photomultiplier fires
    5. Signal sets flip-flop bit in status channel
    6. CPU must poll this bit after EVERY draw operation
    7. CPU identifies selected target by which draw caused the flash
    
    This is fundamentally different from modern mouse clicks!
    """
    
    def __init__(self):
        self.armed = False           # Trigger pulled?
        self.flash_detected = False  # Photomultiplier fired?
        self.gun_x = 0               # Gun position (for simulation)
        self.gun_y = 0
        self.last_drawn_id = None    # ID of last object drawn
    
    def arm(self, x: int, y: int):
        """
        Arm light gun (trigger pulled).
        
        Stores position and waits for flash.
        """
        self.armed = True
        self.gun_x = x
        self.gun_y = y
        self.flash_detected = False
        self.last_drawn_id = None
    
    def disarm(self):
        """Disarm light gun (trigger released or flash detected)"""
        self.armed = False
    
    def draw_event(self, obj_id: str, x: int, y: int, radius: int = 20) -> bool:
        """
        Simulate CRT drawing an object.
        
        If gun is armed and beam passes through gun position,
        photomultiplier fires and sets flash_detected flag.
        
        Returns: True if flash detected, False otherwise
        """
        if not self.armed:
            return False
        
        # Check if beam passes near gun position
        dx = abs(x - self.gun_x)
        dy = abs(y - self.gun_y)
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance <= radius:
            # FLASH! Photomultiplier detected beam
            self.flash_detected = True
            self.last_drawn_id = obj_id
            self.disarm()
            return True
        
        return False
    
    def poll_status(self) -> bool:
        """
        Poll light gun status (CPU operation).
        
        CPU calls this after every draw operation to check
        if the light gun detected that specific object.
        """
        return self.flash_detected
    
    def get_selected_id(self) -> Optional[str]:
        """Get ID of selected object"""
        return self.last_drawn_id if self.flash_detected else None
    
    def clear_status(self):
        """Clear flash detected flag (CPU operation)"""
        self.flash_detected = False
        self.last_drawn_id = None


# ============================================================================
# Integrated I/O System
# ============================================================================

class FSQ7_IO_System:
    """
    Complete AN/FSQ-7 I/O architecture integrating drum and light gun.
    
    Architecture:
    1. External devices write to drum fields asynchronously
    2. Drum sets status channel bits
    3. CPU polls status channels in main loop
    4. CPU reads from drum when status indicates data ready
    5. CPU clears status bits after processing
    
    For light gun:
    1. Operator pulls trigger (arms gun)
    2. CPU draws targets one by one on CRT
    3. CPU polls light gun status after EACH draw
    4. When poll returns True, that target is selected
    """
    
    def __init__(self):
        self.drum = MagneticDrum()
        self.light_gun = LightGunSystem()
    
    def simulate_radar_input(self, targets: List[dict], timestamp: float):
        """
        Simulate external radar writing to LRI drum field.
        
        In real SAGE, radar hardware would do this automatically.
        """
        for i, target in enumerate(targets):
            # Pack target data into 32-bit words
            # (Simplified: real format was more complex)
            x_y_word = (int(target['x']) << 16) | int(target['y'])
            alt_spd_word = (int(target['altitude']) << 16) | int(target['speed'])
            
            # Write to LRI field
            self.drum.write_field(DrumField.LRI, i * 2, x_y_word, timestamp)
            self.drum.write_field(DrumField.LRI, i * 2 + 1, alt_spd_word, timestamp)
        
        # Status channel OD_LRI is automatically set by write_field
    
    def cpu_poll_loop(self, cpu_state: dict) -> Optional[dict]:
        """
        Authentic SAGE CPU polling loop (simplified).
        
        This is what the CPU software would do continuously:
        1. Check all status channels
        2. Read data from drum fields that have data ready
        3. Clear status bits
        4. Process data
        
        Returns: New data if available, None otherwise
        """
        new_data = {}
        
        # Poll LRI (radar data)
        if self.drum.check_status(StatusChannel.OD_LRI):
            # Data available in LRI field
            radar_targets = []
            for addr in range(0, 100, 2):  # Read up to 50 targets
                word1 = self.drum.read_field(DrumField.LRI, addr)
                word2 = self.drum.read_field(DrumField.LRI, addr + 1)
                if word1 is not None and word2 is not None:
                    x = (word1 >> 16) & 0xFFFF
                    y = word1 & 0xFFFF
                    altitude = (word2 >> 16) & 0xFFFF
                    speed = word2 & 0xFFFF
                    radar_targets.append({'x': x, 'y': y, 'altitude': altitude, 'speed': speed})
            
            new_data['radar_targets'] = radar_targets
            
            # Clear status bit (CPU acknowledges receipt)
            self.drum.clear_status(StatusChannel.OD_LRI)
        
        # Poll light gun
        if self.drum.check_status(StatusChannel.LIGHT_GUN):
            selected = self.light_gun.get_selected_id()
            if selected:
                new_data['light_gun_selection'] = selected
            
            # Clear status bits
            self.drum.clear_status(StatusChannel.LIGHT_GUN)
            self.light_gun.clear_status()
        
        return new_data if new_data else None
    
    def tick(self, dt: float):
        """Update drum rotation timing"""
        self.drum.tick(dt)


# ============================================================================
# Testing and Demo
# ============================================================================

def test_drum_io_system():
    """Test the drum-buffered I/O system"""
    print("=== AN/FSQ-7 Drum I/O System Test ===\n")
    
    io_system = FSQ7_IO_System()
    
    # Test 1: Simulate radar input
    print("Test 1: Radar Data Transfer")
    radar_targets = [
        {'x': 100, 'y': 200, 'altitude': 30000, 'speed': 450},
        {'x': 150, 'y': 250, 'altitude': 35000, 'speed': 500},
    ]
    io_system.simulate_radar_input(radar_targets, timestamp=0.0)
    print(f"  Radar wrote {len(radar_targets)} targets to LRI drum field")
    
    # Check status channel
    status = io_system.drum.check_status(StatusChannel.OD_LRI)
    print(f"  Status channel OD_LRI: {status}")
    
    # CPU polls and reads data
    cpu_data = io_system.cpu_poll_loop({})
    if cpu_data and 'radar_targets' in cpu_data:
        print(f"  CPU read {len(cpu_data['radar_targets'])} targets from drum")
        for i, target in enumerate(cpu_data['radar_targets']):
            print(f"    Target {i}: x={target['x']}, y={target['y']}, alt={target['altitude']}, spd={target['speed']}")
    
    # Verify status cleared
    status_after = io_system.drum.check_status(StatusChannel.OD_LRI)
    print(f"  Status channel after CPU clear: {status_after}")
    print()
    
    # Test 2: Light gun polling
    print("Test 2: Light Gun Polling Mechanism")
    io_system.light_gun.arm(100, 200)
    print(f"  Light gun armed at position (100, 200)")
    
    # CPU draws targets and polls after each one
    targets_to_draw = [
        ('TGT-1', 50, 50),
        ('TGT-2', 100, 200),  # This one should trigger flash
        ('TGT-3', 150, 250),
    ]
    
    for target_id, x, y in targets_to_draw:
        flash = io_system.light_gun.draw_event(target_id, x, y, radius=20)
        print(f"  Drew {target_id} at ({x}, {y}) - Flash: {flash}")
        
        if flash:
            # Set status channel (hardware would do this)
            io_system.drum.status_channels[StatusChannel.LIGHT_GUN] = True
            
            # CPU polls
            selected = io_system.light_gun.get_selected_id()
            print(f"  >>> SELECTED: {selected}")
            break
    print()


if __name__ == "__main__":
    test_drum_io_system()
