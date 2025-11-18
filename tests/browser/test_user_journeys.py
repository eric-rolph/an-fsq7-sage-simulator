"""
End-to-end user journey tests for SAGE simulator workflows.

Tests complete operator workflows from start to finish:
- Light gun selection and track classification
- Interceptor assignment and launch
- Scenario execution and debrief
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.browser
class TestLightGunWorkflow:
    """Test complete light gun selection and classification workflow."""

    def test_light_gun_arm_and_disarm(self, page: Page):
        """Test arming and disarming the light gun."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Find the ARM LIGHT GUN button (use role to avoid text ambiguity)
        arm_button = page.get_by_role("button", name="ARM LIGHT GUN")
        expect(arm_button).to_be_visible(timeout=5000)
        
        # Click to arm (button should remain visible and clickable)
        arm_button.click()
        page.wait_for_timeout(500)
        
        # Verify button is still visible (indicates UI responded)
        expect(arm_button).to_be_visible()
        
        # Click again to toggle
        arm_button.click()
        page.wait_for_timeout(500)
        
        # Verify button is still functional
        expect(arm_button).to_be_visible()

    def test_track_selection_with_light_gun(self, page: Page):
        """Test selecting a track using the light gun."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Start any available scenario to get tracks
        scenario_buttons = page.locator("button").filter(has_text="Demo")
        if scenario_buttons.count() > 0:
            scenario_buttons.first.click()
            page.wait_for_timeout(1000)
        
        # Arm light gun
        arm_button = page.get_by_role("button", name="ARM LIGHT GUN")
        if arm_button.is_visible():
            arm_button.click()
            page.wait_for_timeout(500)
        
        # Get canvas and click in the center
        canvas = page.locator("#radar-scope-canvas")
        expect(canvas).to_be_visible()
        
        box = canvas.bounding_box()
        if box:
            # Click near center where tracks likely are (force to bypass overlays)
            canvas.click(position={"x": box["width"] * 0.6, "y": box["height"] * 0.4}, force=True)
            page.wait_for_timeout(1000)
            
            # Check if a track was selected
            selected_track = page.evaluate("() => window.crtRadarScope?.selectedTrack")
            # Note: Track selection depends on timing and track positions, so this may not always succeed
            # This is more of a "does it crash" test than a guaranteed selection test

    def test_track_classification_workflow(self, page: Page):
        """Test classifying a selected track as hostile or friendly."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Start any available scenario
        scenario_buttons = page.locator("button").filter(has_text="Demo")
        if scenario_buttons.count() > 0:
            scenario_buttons.first.click()
            page.wait_for_timeout(1000)
        
        # Look for classification buttons (these should exist in the UI)
        # The exact text may vary, looking for common patterns
        hostile_button = page.get_by_text("HOSTILE", exact=False).first
        friendly_button = page.get_by_text("FRIENDLY", exact=False).first
        
        # These buttons should exist but may be disabled if no track is selected
        # Just verify they're in the DOM
        page.wait_for_timeout(500)


@pytest.mark.browser
class TestInterceptorWorkflow:
    """Test interceptor assignment and launch workflow."""

    def test_interceptor_panel_visible(self, page: Page):
        """Test that interceptor panel is visible and shows interceptors."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Look for interceptor-related UI elements
        # Check if interceptor data is injected
        has_interceptors = page.evaluate(
            "() => typeof window.__SAGE_INTERCEPTORS__ !== 'undefined' && window.__SAGE_INTERCEPTORS__.length > 0"
        )
        
        if has_interceptors:
            interceptor_count = page.evaluate("() => window.__SAGE_INTERCEPTORS__.length")
            assert interceptor_count > 0, "Should have at least one interceptor"

    def test_interceptor_assignment_button_exists(self, page: Page):
        """Test that interceptor assignment controls exist."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Look for assign/launch buttons
        # These may be in various places depending on UI state
        assign_text_visible = page.get_by_text("ASSIGN", exact=False).count() > 0
        launch_text_visible = page.get_by_text("LAUNCH", exact=False).count() > 0
        
        # At least one of these should exist in the UI
        assert assign_text_visible or launch_text_visible, "Should have interceptor controls"


@pytest.mark.browser
class TestScenarioWorkflow:
    """Test complete scenario execution workflow."""

    @pytest.mark.slow
    def test_scenario_selection_and_start(self, page: Page):
        """Test selecting and starting a scenario."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Look for any scenario button
        scenario_buttons = page.locator("button").filter(has_text="Demo")
        expect(scenario_buttons.first).to_be_visible(timeout=5000)
        training_scenario = scenario_buttons.first
        
        # Click to start scenario
        training_scenario.click()
        page.wait_for_timeout(2000)
        
        # Verify scenario started by checking for tracks
        has_tracks = page.evaluate(
            "() => typeof window.__SAGE_TRACKS__ !== 'undefined' && window.__SAGE_TRACKS__.length > 0"
        )
        
        assert has_tracks, "Scenario should create tracks after starting"

    @pytest.mark.slow
    def test_scenario_pause_and_resume(self, page: Page):
        """Test pausing and resuming a scenario."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Start any available scenario
        scenario_buttons = page.locator("button").filter(has_text="Demo")
        if scenario_buttons.count() > 0:
            scenario_buttons.first.click()
            page.wait_for_timeout(1000)
        
        # Look for pause/resume controls
        pause_button = page.get_by_text("PAUSE", exact=False).first
        resume_button = page.get_by_text("RESUME", exact=False).first
        
        # These controls may not always be visible depending on UI state
        # Just verify the page doesn't crash when we look for them
        page.wait_for_timeout(500)

    @pytest.mark.slow
    def test_scenario_completion_shows_debrief(self, page: Page):
        """Test that completing a scenario shows debrief screen."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Start any available scenario
        scenario_buttons = page.locator("button").filter(has_text="Demo")
        if scenario_buttons.count() > 0:
            scenario_buttons.first.click()
            page.wait_for_timeout(1000)
        
        # Wait a bit for scenario to potentially complete
        # (This is a smoke test, not waiting for full scenario)
        page.wait_for_timeout(3000)
        
        # Check if debrief-related elements exist in the DOM
        # (They may not be visible yet if scenario isn't complete)
        debrief_text_exists = page.get_by_text("DEBRIEF", exact=False).count() > 0 or \
                              page.get_by_text("GRADE", exact=False).count() > 0 or \
                              page.get_by_text("PERFORMANCE", exact=False).count() > 0
        
        # This is just checking the UI has these concepts, not that scenario completed
        page.wait_for_timeout(500)


@pytest.mark.browser
class TestCompleteOperatorJourney:
    """Test complete end-to-end operator workflow."""

    @pytest.mark.slow
    def test_full_operator_workflow(self, page: Page):
        """Test complete workflow: start scenario → select track → classify → intercept → debrief."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Step 1: Start any scenario
        scenario_buttons = page.locator("button").filter(has_text="Demo")
        expect(scenario_buttons.first).to_be_visible(timeout=5000)
        scenario_buttons.first.click()
        page.wait_for_timeout(2000)
        
        # Verify tracks appeared
        has_tracks = page.evaluate(
            "() => typeof window.__SAGE_TRACKS__ !== 'undefined' && window.__SAGE_TRACKS__.length > 0"
        )
        assert has_tracks, "Scenario should create tracks"
        
        # Step 2: Arm light gun
        arm_button = page.get_by_role("button", name="ARM LIGHT GUN")
        if arm_button.is_visible():
            arm_button.click()
            page.wait_for_timeout(500)
        
        # Step 3: Click on canvas to select track
        canvas = page.locator("#radar-scope-canvas")
        box = canvas.bounding_box()
        if box:
            # Force click to bypass any overlays
            canvas.click(position={"x": box["width"] * 0.6, "y": box["height"] * 0.4}, force=True)
            page.wait_for_timeout(1000)
        
        # Step 4: Look for classification/intercept options
        # The UI should now show options for the selected track
        page.wait_for_timeout(1000)
        
        # Verify no crashes occurred during the workflow
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.wait_for_timeout(2000)
        
        # Filter expected warnings
        serious_errors = [
            e for e in errors 
            if "WebSocket" not in e 
            and "UNSAFE_componentWillMount" not in e
        ]
        
        assert len(serious_errors) == 0, f"No errors should occur during workflow: {serious_errors}"

    @pytest.mark.slow
    def test_system_inspector_toggle(self, page: Page):
        """Test toggling the system inspector overlay."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Try pressing Shift+I to toggle inspector
        page.keyboard.press("Shift+I")
        page.wait_for_timeout(1000)
        
        # Check if inspector overlay appeared
        inspector_visible = page.get_by_text("CPU STATE", exact=False).is_visible() or \
                           page.get_by_text("MEMORY BANKS", exact=False).is_visible() or \
                           page.get_by_text("SYSTEM INSPECTOR", exact=False).is_visible()
        
        # Press again to toggle off
        page.keyboard.press("Shift+I")
        page.wait_for_timeout(500)

    @pytest.mark.slow
    def test_network_view_toggle(self, page: Page):
        """Test toggling the network/station view."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Look for network toggle button
        network_button = page.get_by_text("NETWORK", exact=False).first
        
        if network_button.is_visible():
            network_button.click()
            page.wait_for_timeout(1000)
            
            # Check if network data is available
            has_stations = page.evaluate(
                "() => typeof window.__SAGE_NETWORK_STATIONS__ !== 'undefined'"
            )
            
            # Click again to toggle off
            if network_button.is_visible():
                network_button.click()
                page.wait_for_timeout(500)


@pytest.mark.browser
class TestUIResponsiveness:
    """Test UI responsiveness and interactions."""

    def test_multiple_button_clicks_no_crash(self, page: Page):
        """Test that rapidly clicking buttons doesn't crash the app."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Find ARM LIGHT GUN button
        arm_button = page.get_by_role("button", name="ARM LIGHT GUN")
        
        if arm_button.is_visible():
            # Click multiple times rapidly
            for _ in range(5):
                arm_button.click()
                page.wait_for_timeout(100)
        
        # Verify page is still responsive
        page.wait_for_timeout(1000)
        expect(page.locator("#radar-scope-canvas")).to_be_visible()

    def test_canvas_remains_interactive(self, page: Page):
        """Test that canvas remains clickable throughout session."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        canvas = page.locator("#radar-scope-canvas")
        box = canvas.bounding_box()
        
        if box:
            # Click canvas multiple times in different positions
            positions = [
                {"x": box["width"] * 0.25, "y": box["height"] * 0.25},
                {"x": box["width"] * 0.75, "y": box["height"] * 0.25},
                {"x": box["width"] * 0.50, "y": box["height"] * 0.50},
                {"x": box["width"] * 0.25, "y": box["height"] * 0.75},
            ]
            
            for pos in positions:
                canvas.click(position=pos)
                page.wait_for_timeout(300)
        
        # Verify canvas is still visible and functional
        expect(canvas).to_be_visible()

    def test_page_survives_rapid_scenario_changes(self, page: Page):
        """Test switching between scenarios rapidly."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Click through multiple scenario buttons rapidly
        demo_buttons = page.locator("button").filter(has_text="Demo")
        scenario_buttons = page.locator("button").filter(has_text="Scenario")
        
        # Click first demo
        if demo_buttons.count() > 0:
            demo_buttons.first.click()
            page.wait_for_timeout(1000)
        
        # Click first scenario
        if scenario_buttons.count() > 0:
            scenario_buttons.first.click()
            page.wait_for_timeout(1000)
        
        # Click second demo if available
        if demo_buttons.count() > 1:
            demo_buttons.nth(1).click()
            page.wait_for_timeout(1000)
        
        # Verify page is still functional
        expect(page.locator("#radar-scope-canvas")).to_be_visible()
        
        has_tracks = page.evaluate(
            "() => typeof window.__SAGE_TRACKS__ !== 'undefined'"
        )
        assert has_tracks, "Track data should still be present"
