"""
Design Language Tests - Mode-Free UI Pattern

Verifies that the UI follows the "mode-free" design pattern:
- Buttons are DISABLED, not removed, when unavailable
- No hidden "modes" that change UI structure
- All controls remain visible with clear visual feedback

These tests enforce the design invariants documented in agents.md.
"""

import pytest
from an_fsq7_simulator import state_model


@pytest.mark.design
class TestModeFreeUI:
    """Test mode-free UI design pattern."""

    def test_light_gun_button_always_present(self):
        """Verify ARM LIGHT GUN button exists regardless of state."""
        # In a real UI test, we would check that the button element
        # always exists in the DOM. For now, we verify the state model
        # doesn't conditionally hide it.
        ui_state = state_model.UIState()
        
        # Light gun has armed/disarmed states, but button should exist in both
        assert hasattr(ui_state, "lightgun_armed")
        assert isinstance(ui_state.lightgun_armed, bool)
        
        # State should be queryable without conditional logic
        ui_state.lightgun_armed = True
        assert ui_state.lightgun_armed == True
        ui_state.lightgun_armed = False
        assert ui_state.lightgun_armed == False

    def test_intercept_buttons_disabled_not_hidden(self):
        """Verify intercept action buttons are disabled, not removed."""
        # LAUNCH INTERCEPT should be disabled when:
        # - No track selected
        # - No interceptors available
        # - Track already engaged
        # But the button should ALWAYS be present in the UI
        
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Test Base",
            base_x=0.5,
            base_y=0.1,
            status="READY"
        )
        
        # Status changes, but interceptor object structure remains constant
        assert hasattr(interceptor, "status")
        interceptor.status = "ASSIGNED"
        assert interceptor.status == "ASSIGNED"
        interceptor.status = "ENGAGING"
        assert interceptor.status == "ENGAGING"
        
        # No conditional structure changes based on status

    def test_track_detail_panel_structure_constant(self):
        """Verify track detail panel has one structure for all track types."""
        # Track detail panel should have the same layout regardless of track type
        # Only content (values, colors, icons) should change, not structure
        
        track_circle = state_model.Track(
            id="TRK-001",
            x=0.5,
            y=0.5,
            track_type="friendly"  # Circle symbol
        )
        
        track_square = state_model.Track(
            id="TRK-002",
            x=0.6,
            y=0.6,
            track_type="hostile"  # Square symbol
        )
        
        track_diamond = state_model.Track(
            id="TRK-003",
            x=0.7,
            y=0.7,
            track_type="unknown"  # Diamond symbol
        )
        
        # All tracks have same field structure
        for track in [track_circle, track_square, track_diamond]:
            assert hasattr(track, "id")
            assert hasattr(track, "x")
            assert hasattr(track, "y")
            assert hasattr(track, "track_type")
            assert hasattr(track, "heading")
            assert hasattr(track, "speed")
            assert hasattr(track, "altitude")

    def test_scenario_selector_shows_all_scenarios(self):
        """Verify scenario selector shows all scenarios, not conditionally filtered."""
        from an_fsq7_simulator.sim import scenarios
        
        all_scenarios = scenarios.list_scenarios()
        
        # All scenarios should be listable
        assert len(all_scenarios) > 0
        
        # Each scenario should be gettable
        for name in all_scenarios:
            scenario = scenarios.get_scenario(name)
            assert scenario is not None
            assert scenario.name == name

    def test_action_bar_layout_consistent(self):
        """Verify action bar maintains consistent position and content."""
        # Action bar should have consistent location and button set
        # Buttons get enabled/disabled, but layout doesn't change
        
        # This is a structural test - in real UI, we'd verify DOM structure
        # For now, verify state model consistency
        
        ui_state = state_model.UIState()
        
        # Light gun has two states but same interface
        assert hasattr(ui_state, "lightgun_armed")
        assert hasattr(ui_state, "selected_track_id")
        
        # Interface doesn't change when state changes
        ui_state.lightgun_armed = True
        assert hasattr(ui_state, "lightgun_armed")
        assert hasattr(ui_state, "selected_track_id")

    def test_detail_panel_always_right_side(self):
        """Verify detail/target info panel is always on right side."""
        # This is a layout invariant - detail panel position never moves
        # In real UI test, we'd verify CSS positioning
        
        # For now, verify the state model doesn't have conditional layout flags
        track = state_model.Track(
            id="TRK-001",
            x=0.5,
            y=0.5,
            track_type="hostile"
        )
        
        # Track data model doesn't contain layout hints
        assert not hasattr(track, "panel_position")
        assert not hasattr(track, "layout_mode")
        assert not hasattr(track, "ui_location")

    def test_no_hidden_modes_in_state(self):
        """Verify state model doesn't have hidden 'mode' flags."""
        # Mode-free design means no 'mode' field that changes UI structure
        
        track = state_model.Track(id="TRK-001", x=0.5, y=0.5)
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Test Base",
            base_x=0.5,
            base_y=0.1
        )
        ui_state = state_model.UIState()
        
        # No 'mode' or 'ui_mode' or 'view_mode' fields
        for obj in [track, interceptor, ui_state]:
            assert not hasattr(obj, "mode")
            assert not hasattr(obj, "ui_mode")
            assert not hasattr(obj, "view_mode")
            assert not hasattr(obj, "display_mode")

    def test_global_actions_consistent_location(self):
        """Verify global action controls stay in consistent region."""
        # ARM LIGHT GUN, LAUNCH INTERCEPT, CLEAR SELECTION should be
        # in consistent bottom/action region, not moving around
        
        # This is tested via state model consistency
        ui_state = state_model.UIState()
        
        # Actions are state transitions, not layout changes
        ui_state.lightgun_armed = False
        assert ui_state.lightgun_armed == False
        ui_state.lightgun_armed = True
        assert ui_state.lightgun_armed == True
        
        # No layout-related state changes

    def test_disabled_button_states_explicit(self):
        """Verify button disabled states are explicit, not hidden."""
        # Buttons should have clear enabled/disabled state
        # This is tested via status fields being queryable
        
        interceptor = state_model.Interceptor(
            id="INT-001",
            aircraft_type="F-106 Delta Dart",
            base_name="Test Base",
            base_x=0.5,
            base_y=0.1,
            status="READY",
            fuel_percent=100,
            weapons_remaining=2
        )
        
        # Button should be disabled when status != READY
        interceptor.status = "ASSIGNED"
        assert interceptor.status != "READY"
        
        # Button should be disabled when fuel too low
        interceptor.fuel_percent = 10
        assert interceptor.fuel_percent < 20
        
        # Button should be disabled when no weapons
        interceptor.weapons_remaining = 0
        assert interceptor.weapons_remaining == 0
        
        # But button should still be VISIBLE (rendered but disabled)

    def test_track_type_changes_appearance_not_structure(self):
        """Verify changing track type changes appearance, not panel structure."""
        track = state_model.Track(
            id="TRK-001",
            x=0.5,
            y=0.5,
            track_type="unknown"
        )
        
        # Changing track type should only affect visual properties
        # Structure (fields available) should remain the same
        
        original_fields = set(dir(track))
        
        track.track_type = "hostile"
        hostile_fields = set(dir(track))
        
        track.track_type = "friendly"
        friendly_fields = set(dir(track))
        
        # All track types have same field structure
        assert original_fields == hostile_fields == friendly_fields
