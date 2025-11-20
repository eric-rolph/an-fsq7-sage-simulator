"""
Browser tests for Keyboard Shortcuts & Accessibility.
"""

import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser
class TestKeyboardShortcuts:
    """Test global keyboard shortcuts."""

    def test_help_panel_toggle(self, page: Page):
        """Test toggling the keyboard help panel with '?'."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Press '?' (shift + / usually, but '?' key works in Playwright)
        page.keyboard.press("?")
        
        # Check if help panel is visible
        help_panel = page.get_by_role("dialog", name="Keyboard shortcuts help")
        expect(help_panel).to_be_visible(timeout=2000)
        
        # Press '?' again to close (or Esc)
        page.keyboard.press("Escape")
        expect(help_panel).not_to_be_visible(timeout=2000)

    def test_light_gun_shortcut(self, page: Page):
        """Test toggling light gun with 'D'."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Initial state: Light gun disarmed (ARM LIGHT GUN button visible)
        arm_button = page.get_by_role("button", name="ARM LIGHT GUN")
        expect(arm_button).to_be_visible()
        
        # Press 'd'
        page.keyboard.press("d")
        
        # Should now be armed (DISARM button visible or ARM button hidden/changed)
        # Assuming the button text changes or a status indicator appears
        # Based on light_gun.py, it might toggle the button text or show a status
        
        # Let's check for the status indicator "LIGHT GUN ARMED"
        status = page.get_by_text("LIGHT GUN ARMED")
        expect(status).to_be_visible(timeout=2000)
        
        # Press 'd' again to disarm
        page.keyboard.press("d")
        expect(status).not_to_be_visible(timeout=2000)

    def test_system_inspector_shortcut(self, page: Page):
        """Test toggling system inspector with 'Shift+I'."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Press Shift+I
        page.keyboard.press("Shift+I")
        
        # Check for system inspector
        inspector = page.get_by_text("SYSTEM INSPECTOR")
        expect(inspector).to_be_visible(timeout=2000)
        
        # Press Shift+I again to close
        page.keyboard.press("Shift+I")
        expect(inspector).not_to_be_visible(timeout=2000)

    def test_dismiss_panels_shortcut(self, page: Page):
        """Test dismissing panels with 'Esc'."""
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Open help panel
        page.keyboard.press("?")
        help_panel = page.get_by_role("dialog", name="Keyboard shortcuts help")
        expect(help_panel).to_be_visible()
        
        # Press Esc
        page.keyboard.press("Escape")
        expect(help_panel).not_to_be_visible()
        
        # Open inspector
        page.keyboard.press("Shift+I")
        inspector = page.get_by_text("SYSTEM INSPECTOR")
        expect(inspector).to_be_visible()
        
        # Press Esc
        page.keyboard.press("Escape")
        expect(inspector).not_to_be_visible()
