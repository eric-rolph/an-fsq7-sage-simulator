"""
Unit tests for console display modes.

Tests mode definitions, metadata, and mode cycling.
"""

import pytest
from an_fsq7_simulator.sim import modes


@pytest.mark.unit
class TestDisplayMode:
    """Test DisplayMode enum."""

    def test_display_mode_enum_exists(self):
        """Verify DisplayMode enum is defined."""
        assert modes.DisplayMode.RADAR is not None
        assert modes.DisplayMode.TACTICAL is not None
        assert modes.DisplayMode.STATUS is not None
        assert modes.DisplayMode.MEMORY is not None

    def test_display_mode_values(self):
        """Verify DisplayMode enum values."""
        assert modes.DisplayMode.RADAR.value == "RADAR"
        assert modes.DisplayMode.TACTICAL.value == "TACTICAL"
        assert modes.DisplayMode.STATUS.value == "STATUS"
        assert modes.DisplayMode.MEMORY.value == "MEMORY"


@pytest.mark.unit
class TestConsoleModeInfo:
    """Test ConsoleModeInfo dataclass."""

    def test_console_mode_info_creation(self):
        """Verify ConsoleModeInfo can be created."""
        info = modes.ConsoleModeInfo(
            mode=modes.DisplayMode.RADAR,
            title="Test Mode",
            description="Test description",
            allowed_actions=["Action 1", "Action 2"],
            shows_radar=True,
            allows_light_gun=True
        )
        
        assert info.mode == modes.DisplayMode.RADAR
        assert info.title == "Test Mode"
        assert info.description == "Test description"
        assert len(info.allowed_actions) == 2
        assert info.shows_radar == True
        assert info.allows_light_gun == True

    def test_console_mode_info_defaults(self):
        """Verify ConsoleModeInfo has correct defaults."""
        info = modes.ConsoleModeInfo(
            mode=modes.DisplayMode.RADAR,
            title="Test",
            description="Test",
            allowed_actions=[]
        )
        
        # Defaults should be False
        assert info.shows_radar == False
        assert info.shows_cpu == False
        assert info.shows_memory == False
        assert info.allows_light_gun == False


@pytest.mark.unit
class TestModeDefinitions:
    """Test mode definitions in MODE_INFO."""

    def test_radar_mode_info(self):
        """Verify RADAR mode info is correct."""
        info = modes.MODE_INFO[modes.DisplayMode.RADAR]
        
        assert info.mode == modes.DisplayMode.RADAR
        assert "RADAR" in info.title
        assert info.shows_radar == True
        assert info.allows_light_gun == True
        assert len(info.allowed_actions) > 0
        assert "Light gun" in info.allowed_actions[0]

    def test_tactical_mode_info(self):
        """Verify TACTICAL mode info is correct."""
        info = modes.MODE_INFO[modes.DisplayMode.TACTICAL]
        
        assert info.mode == modes.DisplayMode.TACTICAL
        assert "TACTICAL" in info.title
        assert info.shows_radar == True
        assert info.allows_light_gun == False
        assert len(info.allowed_actions) > 0

    def test_status_mode_info(self):
        """Verify STATUS mode info is correct."""
        info = modes.MODE_INFO[modes.DisplayMode.STATUS]
        
        assert info.mode == modes.DisplayMode.STATUS
        assert "STATUS" in info.title
        assert info.shows_radar == False
        assert info.shows_cpu == True
        assert info.shows_memory == True
        assert info.allows_light_gun == False

    def test_memory_mode_info(self):
        """Verify MEMORY mode info is correct."""
        info = modes.MODE_INFO[modes.DisplayMode.MEMORY]
        
        assert info.mode == modes.DisplayMode.MEMORY
        assert "MEMORY" in info.title
        assert info.shows_radar == False
        assert info.shows_cpu == True
        assert info.shows_memory == True
        assert info.allows_light_gun == False

    def test_all_modes_have_info(self):
        """Verify all display modes have info defined."""
        for mode in modes.DisplayMode:
            assert mode in modes.MODE_INFO


@pytest.mark.unit
class TestGetModeInfo:
    """Test get_mode_info function."""

    def test_get_mode_info_returns_info(self):
        """Verify get_mode_info returns correct info."""
        info = modes.get_mode_info(modes.DisplayMode.RADAR)
        
        assert info.mode == modes.DisplayMode.RADAR
        assert isinstance(info, modes.ConsoleModeInfo)

    def test_get_mode_info_for_all_modes(self):
        """Verify get_mode_info works for all modes."""
        for mode in modes.DisplayMode:
            info = modes.get_mode_info(mode)
            assert info.mode == mode


@pytest.mark.unit
class TestCycleMode:
    """Test mode cycling function."""

    def test_cycle_mode_from_radar(self):
        """Verify cycle_mode from RADAR goes to TACTICAL."""
        next_mode = modes.cycle_mode(modes.DisplayMode.RADAR)
        assert next_mode == modes.DisplayMode.TACTICAL

    def test_cycle_mode_from_tactical(self):
        """Verify cycle_mode from TACTICAL goes to STATUS."""
        next_mode = modes.cycle_mode(modes.DisplayMode.TACTICAL)
        assert next_mode == modes.DisplayMode.STATUS

    def test_cycle_mode_from_status(self):
        """Verify cycle_mode from STATUS goes to MEMORY."""
        next_mode = modes.cycle_mode(modes.DisplayMode.STATUS)
        assert next_mode == modes.DisplayMode.MEMORY

    def test_cycle_mode_from_memory(self):
        """Verify cycle_mode from MEMORY wraps back to RADAR."""
        next_mode = modes.cycle_mode(modes.DisplayMode.MEMORY)
        assert next_mode == modes.DisplayMode.RADAR

    def test_cycle_mode_full_cycle(self):
        """Verify cycling through all modes returns to start."""
        current = modes.DisplayMode.RADAR
        
        # Cycle through all modes
        for _ in range(len(modes.DisplayMode)):
            current = modes.cycle_mode(current)
        
        # Should be back at RADAR
        assert current == modes.DisplayMode.RADAR


@pytest.mark.unit
class TestModeMetadata:
    """Test mode metadata consistency."""

    def test_radar_modes_allow_light_gun_correctly(self):
        """Verify only RADAR mode allows light gun."""
        for mode, info in modes.MODE_INFO.items():
            if mode == modes.DisplayMode.RADAR:
                assert info.allows_light_gun == True
            else:
                assert info.allows_light_gun == False

    def test_radar_showing_modes(self):
        """Verify RADAR and TACTICAL show radar."""
        radar_showing = [
            modes.DisplayMode.RADAR,
            modes.DisplayMode.TACTICAL
        ]
        
        for mode in modes.DisplayMode:
            info = modes.MODE_INFO[mode]
            if mode in radar_showing:
                assert info.shows_radar == True
            else:
                assert info.shows_radar == False

    def test_cpu_showing_modes(self):
        """Verify STATUS and MEMORY show CPU."""
        cpu_showing = [
            modes.DisplayMode.STATUS,
            modes.DisplayMode.MEMORY
        ]
        
        for mode in modes.DisplayMode:
            info = modes.MODE_INFO[mode]
            if mode in cpu_showing:
                assert info.shows_cpu == True
            else:
                assert info.shows_cpu == False

    def test_all_modes_have_actions(self):
        """Verify all modes have at least one allowed action."""
        for mode, info in modes.MODE_INFO.items():
            assert len(info.allowed_actions) > 0

    def test_all_modes_have_titles(self):
        """Verify all modes have non-empty titles."""
        for mode, info in modes.MODE_INFO.items():
            assert info.title != ""
            assert len(info.title) > 0

    def test_all_modes_have_descriptions(self):
        """Verify all modes have non-empty descriptions."""
        for mode, info in modes.MODE_INFO.items():
            assert info.description != ""
            assert len(info.description) > 10  # Meaningful description
