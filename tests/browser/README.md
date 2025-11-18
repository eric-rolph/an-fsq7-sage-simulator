# Playwright Browser Tests

Automated browser testing for SAGE UI workflows using Playwright.

## Quick Start

**1. Start the dev server** (Terminal 1):
```powershell
uv run reflex run
```

Wait for "App running at: http://localhost:3000" message.

**2. Run tests** (Terminal 2):
```powershell
# Run all browser tests (headless)
uv run pytest tests/browser -c pytest-playwright.ini

# Run with visible browser (for debugging)
uv run pytest tests/browser --headed

# Run only smoke tests
uv run pytest tests/browser -m smoke

# Run specific test with visible browser
uv run pytest tests/browser/test_ui_smoke.py::TestUILoad::test_homepage_loads_successfully --headed
```

## Test Organization

- `test_ui_smoke.py` - Smoke tests for critical UI paths
  - TestUILoad: Page loading and initialization
  - TestDataInjection: Python → JavaScript data flow
  - TestCriticalWorkflows: End-to-end workflows
  - TestCanvasInteraction: Radar canvas interactions

- `conftest.py` - Shared fixtures
  - `sage_app`: App loaded at localhost:3000
  - `sage_with_scenario`: App with scenario running
  - `light_gun_armed`: Light gun armed for selection

## Writing New Tests

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser
def test_my_feature(sage_app: Page):
    """Test description."""
    # sage_app already loaded at localhost:3000
    button = sage_app.get_by_role("button", name="MY BUTTON")
    button.click()
    
    expect(button).to_have_class("active")
```

## Common Patterns

**Find elements**:
```python
# By role (RECOMMENDED)
button = page.get_by_role("button", name="ARM LIGHT GUN")

# By CSS selector
canvas = page.locator("#radar-scope-canvas")
```

**Wait for elements**:
```python
expect(canvas).to_be_visible(timeout=5000)
page.wait_for_load_state("networkidle")
```

**Check JavaScript state**:
```python
has_tracks = page.evaluate("() => typeof window.__SAGE_TRACKS__ !== 'undefined'")
tracks = page.evaluate("() => window.__SAGE_TRACKS__")
```

**Click canvas at position**:
```python
canvas = page.locator("#radar-scope-canvas")
box = canvas.bounding_box()
canvas.click(position={"x": box["width"] / 2, "y": box["height"] / 2})
```

## Debugging

**Run with visible browser**:
```powershell
uv run pytest tests/browser --headed --slowmo 1000
```

**Check console logs**:
```python
errors = []
page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
page.goto("http://localhost:3000")
```

**Take screenshots**:
```python
page.screenshot(path="test-screenshots/debug.png")
```

## Troubleshooting

**Server not running**:
```
pytest.fail("Server not responding correctly. Run: uv run reflex run")
```
→ Start dev server in Terminal 1 before running tests.

**Element not found timeout**:
```
TimeoutError: locator.click: Timeout 30000ms exceeded.
```
→ Increase timeout or wait for visibility:
```python
expect(button).to_be_visible(timeout=10000)
button.click()
```

**Canvas not initialized**:
```python
# Wait for canvas element
canvas = page.locator("#radar-scope-canvas")
expect(canvas).to_be_visible(timeout=5000)

# Wait for JS initialization
page.wait_for_timeout(1000)

# Verify scope exists
has_scope = page.evaluate("() => typeof window.crtRadarScope !== 'undefined'")
```

**Chromium not installed**:
```powershell
uv run playwright install chromium
```

## Test Markers

- `@pytest.mark.browser` - All Playwright tests (REQUIRED)
- `@pytest.mark.smoke` - Critical path smoke tests
- `@pytest.mark.slow` - Tests taking >5 seconds

## Configuration

See `pytest-playwright.ini` for test configuration:
- base_url: http://localhost:3000
- browser: chromium (headless)
- timeout: 30 seconds

## CI/CD (Future)

Browser tests will run in GitHub Actions on push/PR:
1. Install dependencies
2. Install Chromium
3. Start dev server
4. Run browser tests
5. Capture screenshots on failure
