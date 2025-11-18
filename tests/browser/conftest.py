"""
Playwright browser test configuration.

Provides fixtures and utilities for browser-based testing.
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure browser context for SAGE simulator.
    
    Sets viewport size, permissions, and other browser settings.
    """
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }


@pytest.fixture(scope="function")
def context(browser: Browser, browser_context_args):
    """
    Create a new browser context for each test.
    
    Ensures test isolation - each test gets a fresh browser state.
    """
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    Create a new page for each test.
    
    Automatically closes after test completes.
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def sage_app(page: Page):
    """
    Navigate to SAGE app and wait for initialization.
    
    Usage:
        def test_something(sage_app):
            # sage_app is already on homepage and loaded
            sage_app.click("#some-button")
    """
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")
    
    # Wait for CRT radar scope to initialize
    page.wait_for_timeout(1000)
    
    return page


@pytest.fixture
def sage_with_scenario(sage_app: Page):
    """
    Start SAGE app with a scenario loaded.
    
    Useful for tests that need active simulation state.
    """
    # Click scenario button if available
    # This is a placeholder - adjust based on actual UI
    try:
        scenario_btn = sage_app.get_by_role("button", name="Training Scenario")
        if scenario_btn.is_visible(timeout=1000):
            scenario_btn.click()
            sage_app.wait_for_timeout(500)
    except Exception:
        pass  # No scenario button, continue anyway
    
    return sage_app


@pytest.fixture
def light_gun_armed(sage_app: Page):
    """
    Arm the light gun for selection tests.
    
    Returns page with light gun armed and ready for track selection.
    """
    arm_button = sage_app.get_by_role("button", name="ARM LIGHT GUN")
    if arm_button.is_visible(timeout=2000):
        arm_button.click()
        sage_app.wait_for_timeout(500)
    
    return sage_app
