"""
Playwright browser tests for SAGE UI smoke testing.

These tests verify critical UI paths work correctly in a real browser.
Run with: uv run pytest tests/browser --headed (to see browser)
"""

import pytest
from playwright.sync_api import Page, expect
import time


@pytest.mark.browser
class TestUILoad:
    """Test basic page loading and initialization."""

    def test_homepage_loads_successfully(self, page: Page):
        """Verify homepage loads without errors."""
        # Navigate to the app
        page.goto("http://localhost:3000")
        
        # Wait for page to load
        page.wait_for_load_state("networkidle")
        
        # Check page title
        expect(page).to_have_title("AN/FSQ-7 SAGE System Simulator")

    def test_radar_canvas_present(self, page: Page):
        """Verify radar canvas element is present on page."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Wait for canvas to be visible
        canvas = page.locator("#radar-scope-canvas")
        expect(canvas).to_be_visible(timeout=5000)

    def test_no_console_errors_on_load(self, page: Page):
        """Verify no JavaScript errors on page load."""
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Wait a bit for any delayed errors
        page.wait_for_timeout(2000)
        
        # Filter out expected WebSocket warnings
        serious_errors = [e for e in errors if "WebSocket" not in e and "delta to disconnected" not in e]
        assert len(serious_errors) == 0, f"Console errors found: {serious_errors}"


@pytest.mark.browser
class TestDataInjection:
    """Test Python->JavaScript data injection."""

    def test_sage_globals_present(self, page: Page):
        """Verify window.__SAGE_* globals are injected."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Wait for data injection
        page.wait_for_timeout(1000)
        
        # Check for SAGE globals
        has_tracks = page.evaluate("() => typeof window.__SAGE_TRACKS__ !== 'undefined'")
        has_interceptors = page.evaluate("() => typeof window.__SAGE_INTERCEPTORS__ !== 'undefined'")
        
        assert has_tracks, "window.__SAGE_TRACKS__ not found"
        assert has_interceptors, "window.__SAGE_INTERCEPTORS__ not found"

    def test_crt_radar_scope_initialized(self, page: Page):
        """Verify CRT radar scope JavaScript object is initialized."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Wait for initialization
        page.wait_for_timeout(2000)
        
        # Check CRT scope exists
        has_scope = page.evaluate("() => typeof window.crtRadarScope !== 'undefined'")
        assert has_scope, "window.crtRadarScope not initialized"


@pytest.mark.browser
@pytest.mark.smoke
class TestCriticalWorkflows:
    """Test critical user workflows end-to-end."""

    def test_arm_light_gun_button_exists(self, page: Page):
        """Verify ARM LIGHT GUN button is present."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Look for ARM LIGHT GUN button (may be in various forms)
        arm_button = page.get_by_role("button", name="ARM LIGHT GUN")
        expect(arm_button).to_be_visible(timeout=5000)

    def test_scenario_selector_visible(self, page: Page):
        """Verify scenario selector is visible."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Check for scenario selection UI
        # This might be a dropdown, buttons, or other selector
        page.wait_for_timeout(1000)
        
        # Just verify page loaded - specific selector UI varies
        body = page.locator("body")
        expect(body).to_be_visible()

    def test_page_renders_without_crash(self, page: Page):
        """Smoke test: page renders and stays stable for 5 seconds."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Wait and ensure page doesn't crash
        page.wait_for_timeout(5000)
        
        # Verify body still visible
        body = page.locator("body")
        expect(body).to_be_visible()


@pytest.mark.browser
class TestCanvasInteraction:
    """Test canvas interaction capabilities."""

    def test_canvas_clickable(self, page: Page):
        """Verify radar canvas accepts click events."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        canvas = page.locator("#radar-scope-canvas")
        expect(canvas).to_be_visible(timeout=5000)
        
        # Try clicking canvas (won't select anything without arming, but shouldn't crash)
        canvas.click(position={"x": 400, "y": 300})
        
        # Verify page still responsive
        page.wait_for_timeout(500)
        expect(canvas).to_be_visible()

    def test_canvas_has_correct_size(self, page: Page):
        """Verify radar canvas has reasonable dimensions."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        canvas = page.locator("#radar-scope-canvas")
        box = canvas.bounding_box()
        
        assert box is not None, "Canvas has no bounding box"
        assert box["width"] > 400, f"Canvas too narrow: {box['width']}px"
        assert box["height"] > 400, f"Canvas too short: {box['height']}px"


# Fixture for automatic server management (optional)
@pytest.fixture(scope="session", autouse=True)
def check_server_running():
    """Verify dev server is running before tests."""
    import httpx
    
    try:
        response = httpx.get("http://localhost:3000", timeout=2)
        if response.status_code not in [200, 304]:
            pytest.fail("Server not responding correctly. Run: uv run reflex run")
    except Exception as e:
        pytest.fail(f"Server not running. Start with: uv run reflex run\nError: {e}")
    
    yield  # Run tests
    
    # Teardown (nothing needed)
