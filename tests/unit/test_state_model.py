"""
Unit tests for state model transitions and dataclass integrity.

Tests the Reflex-compatible state dataclasses in state_model.py.
"""

import pytest
from an_fsq7_simulator import state_model


@pytest.mark.unit
class TestTrackState:
    """Test Track dataclass state management."""

    def test_track_default_initialization(self):
        """Verify Track initializes with correct defaults."""
        track = state_model.Track(id="TRK-001", x=0.5, y=0.5)
        
        assert track.id == "TRK-001"
        assert track.x == 0.5
        assert track.y == 0.5
        assert track.vx == 0.0
        assert track.vy == 0.0
        assert track.heading == 0
        assert track.speed == 0
        assert track.altitude == 0
        assert track.track_type == "unknown"
        assert track.correlation_state == "uncorrelated"

    def test_track_correlation_state_transitions(self):
        """Verify correlation state can transition correctly."""
        track = state_model.Track(id="TRK-001", x=0.5, y=0.5)
        
        # uncorrelated -> correlating
        track.correlation_state = "correlating"
        assert track.correlation_state == "correlating"
        
        # correlating -> correlated
        track.correlation_state = "correlated"
        assert track.correlation_state == "correlated"

    def test_track_type_transitions(self):
        """Verify track type can change."""
        track = state_model.Track(id="TRK-001", x=0.5, y=0.5)
        
        # unknown -> hostile
        track.track_type = "hostile"
        assert track.track_type == "hostile"
        
        # hostile -> friendly (reclassification)
        track.track_type = "friendly"
        assert track.track_type == "friendly"

    def test_track_position_updates(self):
        """Verify track position can be updated."""
        track = state_model.Track(id="TRK-001", x=0.3, y=0.4)
        
        track.x = 0.35
        track.y = 0.45
        
        assert track.x == 0.35
        assert track.y == 0.45

    def test_track_velocity_updates(self):
        """Verify track velocity can be updated."""
        track = state_model.Track(id="TRK-001", x=0.5, y=0.5, vx=0.01, vy=0.02)
        
        assert track.vx == 0.01
        assert track.vy == 0.02
        
        track.vx = 0.015
        track.vy = 0.025
        
        assert track.vx == 0.015
        assert track.vy == 0.025

    def test_track_classification_time_optional(self):
        """Verify classification_time is optional."""
        track = state_model.Track(id="TRK-001", x=0.5, y=0.5)
        
        # Should be None initially
        assert track.classification_time is None
        
        # Can be set
        track.classification_time = 123.45
        assert track.classification_time == 123.45


@pytest.mark.unit
class TestInterceptorState:
    """Test Interceptor dataclass state management."""

    def test_interceptor_initialization(self):
        """Verify Interceptor initializes correctly."""
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Duluth",
            base_x=0.2,
            base_y=0.1
        )
        
        assert interceptor.id == "INT-001"
        assert interceptor.aircraft_type == "F-106 Delta Dart"
        assert interceptor.base_name == "Duluth"
        assert interceptor.status == "READY"
        assert interceptor.fuel_percent == 100
        assert interceptor.weapons_remaining == 4  # Default is 4 AIM-4 Falcons

    def test_interceptor_status_transitions(self):
        """Verify interceptor status transitions through lifecycle."""
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Base",
            base_x=0.5,
            base_y=0.1
        )
        
        # READY -> ASSIGNED
        interceptor.status = "ASSIGNED"
        assert interceptor.status == "ASSIGNED"
        
        # ASSIGNED -> ENGAGING
        interceptor.status = "ENGAGING"
        assert interceptor.status == "ENGAGING"
        
        # ENGAGING -> RETURNING
        interceptor.status = "RETURNING"
        assert interceptor.status == "RETURNING"
        
        # RETURNING -> READY
        interceptor.status = "READY"
        assert interceptor.status == "READY"

    def test_interceptor_fuel_depletion(self):
        """Verify interceptor fuel can be depleted."""
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Base",
            base_x=0.5,
            base_y=0.1,
            fuel_percent=100
        )
        
        # Deplete fuel
        interceptor.fuel_percent = 75
        assert interceptor.fuel_percent == 75
        
        interceptor.fuel_percent = 25
        assert interceptor.fuel_percent == 25
        
        interceptor.fuel_percent = 0
        assert interceptor.fuel_percent == 0

    def test_interceptor_weapon_expenditure(self):
        """Verify interceptor weapons can be expended."""
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Base",
            base_x=0.5,
            base_y=0.1,
            weapons_remaining=2
        )
        
        # Fire weapon
        interceptor.weapons_remaining = 1
        assert interceptor.weapons_remaining == 1
        
        # Fire last weapon
        interceptor.weapons_remaining = 0
        assert interceptor.weapons_remaining == 0

    def test_interceptor_target_assignment(self):
        """Verify interceptor can be assigned to target."""
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Base",
            base_x=0.5,
            base_y=0.1
        )
        
        # Initially no target
        assert interceptor.assigned_target_id is None
        
        # Assign target
        interceptor.assigned_target_id = "TRK-042"
        assert interceptor.assigned_target_id == "TRK-042"
        
        # Clear assignment
        interceptor.assigned_target_id = None
        assert interceptor.assigned_target_id is None


@pytest.mark.unit
class TestUIState:
    """Test UIState dataclass."""

    def test_ui_state_initialization(self):
        """Verify UIState initializes with correct defaults."""
        ui_state = state_model.UIState()
        
        assert ui_state.lightgun_armed == False
        assert ui_state.selected_track_id == ""
        assert ui_state.active_filters == []
        assert ui_state.active_overlays == []

    def test_light_gun_arm_disarm(self):
        """Verify light gun can be armed and disarmed."""
        ui_state = state_model.UIState()
        
        # Arm
        ui_state.lightgun_armed = True
        assert ui_state.lightgun_armed == True
        
        # Disarm
        ui_state.lightgun_armed = False
        assert ui_state.lightgun_armed == False

    def test_track_selection(self):
        """Verify track can be selected and cleared."""
        ui_state = state_model.UIState()
        
        # Select track
        ui_state.selected_track_id = "TRK-123"
        assert ui_state.selected_track_id == "TRK-123"
        
        # Clear selection
        ui_state.selected_track_id = ""
        assert ui_state.selected_track_id == ""

    def test_active_filters_management(self):
        """Verify active filters can be managed."""
        ui_state = state_model.UIState()
        
        # Add filters
        ui_state.active_filters = ["hostile", "missile"]
        assert "hostile" in ui_state.active_filters
        assert "missile" in ui_state.active_filters
        assert len(ui_state.active_filters) == 2

    def test_active_overlays_management(self):
        """Verify active overlays can be managed."""
        ui_state = state_model.UIState()
        
        # Add overlays
        ui_state.active_overlays = ["coastlines", "range_rings", "stations"]
        assert "coastlines" in ui_state.active_overlays
        assert "range_rings" in ui_state.active_overlays
        assert "stations" in ui_state.active_overlays


@pytest.mark.unit
class TestSystemMessage:
    """Test SystemMessage dataclass."""

    def test_system_message_creation(self):
        """Verify SystemMessage can be created."""
        msg = state_model.SystemMessage(
            timestamp="123.45",
            level="critical",
            category="operator",
            message="New hostile track detected",
            details="Track TRK-001 at sector 4"
        )
        
        assert msg.timestamp == "123.45"
        assert msg.level == "critical"
        assert msg.category == "operator"
        assert msg.message == "New hostile track detected"
        assert msg.details == "Track TRK-001 at sector 4"

    def test_system_message_levels(self):
        """Verify system messages can have different levels."""
        info_msg = state_model.SystemMessage(
            timestamp="1.0",
            level="info",
            category="system",
            message="System ready"
        )
        
        warning_msg = state_model.SystemMessage(
            timestamp="2.0",
            level="warning",
            category="intercept",
            message="Fuel low"
        )
        
        critical_msg = state_model.SystemMessage(
            timestamp="3.0",
            level="critical",
            category="operator",
            message="Incoming threat"
        )
        
        assert info_msg.level == "info"
        assert warning_msg.level == "warning"
        assert critical_msg.level == "critical"


@pytest.mark.unit
class TestScenarioMetrics:
    """Test ScenarioMetrics dataclass."""

    def test_scenario_metrics_initialization(self):
        """Verify ScenarioMetrics initializes with zeros."""
        metrics = state_model.ScenarioMetrics()
        
        assert metrics.tracks_detected == 0
        assert metrics.tracks_total == 0
        assert metrics.correct_classifications == 0
        assert metrics.total_classifications == 0
        assert metrics.successful_intercepts == 0
        assert metrics.attempted_intercepts == 0
        assert metrics.scenario_start_time == 0.0
        assert metrics.scenario_duration == 0.0
        assert metrics.overall_score == 0.0

    def test_scenario_metrics_updates(self):
        """Verify scenario metrics can be updated."""
        metrics = state_model.ScenarioMetrics()
        
        metrics.tracks_detected = 10
        metrics.tracks_total = 12
        metrics.correct_classifications = 8
        metrics.total_classifications = 10
        metrics.successful_intercepts = 5
        metrics.attempted_intercepts = 6
        
        assert metrics.tracks_detected == 10
        assert metrics.tracks_total == 12
        assert metrics.correct_classifications == 8
        assert metrics.total_classifications == 10

    def test_scenario_metrics_score_calculation(self):
        """Verify overall score calculation."""
        metrics = state_model.ScenarioMetrics()
        
        metrics.tracks_detected = 10
        metrics.tracks_total = 10
        metrics.correct_classifications = 8
        metrics.total_classifications = 10
        metrics.successful_intercepts = 5
        metrics.attempted_intercepts = 5
        
        score = metrics.calculate_overall_score()
        
        # 30% detection (100%) + 40% classification (80%) + 30% intercepts (100%)
        # = 30 + 32 + 30 = 92
        assert abs(score - 92.0) < 0.1
        assert abs(metrics.overall_score - 92.0) < 0.1


@pytest.mark.unit
class TestCpuRegisters:
    """Test CpuRegisters dataclass."""

    def test_cpu_registers_initialization(self):
        """Verify CpuRegisters initializes to zero."""
        regs = state_model.CpuRegisters()
        
        assert regs.A == 0  # Accumulator
        assert regs.B == 0  # B register
        assert regs.PC == 0  # Program counter
        assert regs.FLAGS == 0  # Status flags

    def test_cpu_registers_updates(self):
        """Verify CPU registers can be updated."""
        regs = state_model.CpuRegisters()
        
        regs.A = 0x1234
        regs.B = 0x5678
        regs.PC = 100
        regs.FLAGS = 0b1010
        
        assert regs.A == 0x1234
        assert regs.B == 0x5678
        assert regs.PC == 100
        assert regs.FLAGS == 0b1010


@pytest.mark.unit
class TestTubeState:
    """Test TubeState dataclass for vacuum tube maintenance."""

    def test_tube_state_initialization(self):
        """Verify TubeState initializes correctly."""
        tube = state_model.TubeState(
            id=1,
            health=100,
            status="ok",
            temperature=25,
            hours_used=0
        )
        
        assert tube.id == 1
        assert tube.health == 100
        assert tube.status == "ok"
        assert tube.temperature == 25
        assert tube.hours_used == 0

    def test_tube_hours_accumulation(self):
        """Verify tube hours can accumulate."""
        tube = state_model.TubeState(
            id=1,
            health=100,
            status="ok"
        )
        
        tube.hours_used = 100
        assert tube.hours_used == 100
        
        tube.hours_used = 500
        assert tube.hours_used == 500

    def test_tube_status_transitions(self):
        """Verify tube status can transition."""
        tube = state_model.TubeState(
            id=1,
            health=100,
            status="ok"
        )
        
        # ok -> degrading
        tube.status = "degrading"
        assert tube.status == "degrading"
        
        # degrading -> failed
        tube.status = "failed"
        assert tube.status == "failed"

    def test_tube_health_degradation(self):
        """Verify tube health can degrade over time."""
        tube = state_model.TubeState(
            id=1,
            health=100,
            status="ok"
        )
        
        # Health degrades
        tube.health = 75
        assert tube.health == 75
        
        tube.health = 50
        assert tube.health == 50
        
        tube.health = 0
        assert tube.health == 0
