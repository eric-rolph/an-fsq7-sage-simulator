# Agent Development Guide

Critical patterns and gotchas for AI agents working on this SAGE simulator project.

---

## UV Package Manager (CRITICAL)

This project uses `uv` for Python – **NOT** conda/pip/poetry.

```powershell
# ✅ CORRECT
uv run reflex run
uv run python script.py

# ❌ WRONG  
reflex run        # Command not found
python script.py  # Wrong environment
```

**Common Issues**:
```powershell
# Server won't start – kill zombie processes
Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force

# Changes not reflected – clear cache
Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue

# Test imports
uv run python -c "import an_fsq7_simulator.interactive_sage; print('OK')"
```

## Reflex Framework Rules

**NEVER use Python boolean operators with Reflex Var types** (causes VarTypeError):

```python
# ❌ WRONG
color = "green" if fuel > 60 else "red"
disabled = (status != "READY") and (fuel < 50)

# ✅ CORRECT
color = rx.cond(fuel > 60, "green", "red")          # Use rx.cond
disabled = (status != "READY") | (fuel < 50)        # Use | & ~ operators
items = rx.foreach(items, lambda x: ...)            # Not list comprehension
```

**JavaScript Data Injection**:
```python
@rx.var
def data_script_tag(self) -> str:
    return f"<script>window.__DATA__ = {self.get_json()};</script>"

# In page:
rx.html(InteractiveSageState.data_script_tag)
```

## Design Language & Invariants (DO NOT BREAK)

These are hard rules for UI/UX. Tests in `tests/design_language` should enforce them.

### Mode-Free UI
- **No hidden "modes"**.
- Buttons should be **disabled**, not removed, when unavailable.
- Track detail uses a single layout:
  - `track_detail_panel` has one structure for all track types.
  - Track type changes color/icon, not panel structure.

### Layout
Main layout has a consistent structure:
- **Radar/scope** is the central visual focus.
- **Detail/target info panel** is always on the right side of the main layout.
- **Global action controls** (e.g. ARM LIGHT GUN, LAUNCH INTERCEPT, CLEAR SELECTION) live in a consistent bottom/action region or clearly defined action bar.
- **Do not move** the detail panel or action region to different sides/views based on state.

### CRT Display (P14 Phosphor - HISTORICALLY ACCURATE)
Scope is a **19" P14 phosphor vector CRT** (SAGE situation display):
- **P14 Phosphor**: Purple flash → orange afterglow (2-3 second persistence)
- **2.5-Second Refresh Cycle**: Computer updates display drum every 2.5 seconds (historically accurate)
  - Phosphor persistence decays continuously at 60fps between computer refreshes
  - Tracks remain visible via P14 orange afterglow during 2.5s intervals
  - Simulates SAGE's drum-buffered display update timing
  - **Toggle available**: `enableRefreshCycle` flag in crt_radar.js for A/B comparison
- **Monochrome Display**: NO color coding - all symbology uses P14 orange phosphor color
- Use **vector strokes** (blips, lines, arcs, polylines, symbol shapes) – not filled HUD widgets
- Visual hierarchy:
  - **Map/coastlines/static geometry**: thin, low-intensity strokes
  - **Range rings/grids**: slightly brighter, but still secondary
  - **Tracks/selected targets**: brightest strokes; selection adds halo/outline
- **Blue Room Lighting**: Dim blue ambient glow simulates SAGE indirect lighting environment

### Track Symbology (HISTORICALLY ACCURATE)
Track types differentiated by **SYMBOL SHAPE**, not color:
- **Circle**: Friendly aircraft
- **Square**: Hostile aircraft (bombers, fighters)
- **Diamond**: Unknown tracks
- **Triangle**: Missiles
- **Dashed outline**: Uncorrelated tracks (with "?" indicator)
- **Solid outline**: Correlated/classified tracks

**CRITICAL**: All symbols render in monochrome P14 orange phosphor. Shape indicates type, NOT color.

### Agent Behavior
- When editing components in `an_fsq7_simulator/components_v2/`, keep these invariants intact.
- If a change needs to bend a rule, document it and adjust tests so it's intentional, not accidental.
- Prefer adding/adjusting tests in `tests/design_language` when you change layout or interaction patterns.

## JavaScript Integration

**Data Flow**: Python → JSON → window global → JS reads on refresh cycle

```python
def get_data_json(self) -> str:
    return json.dumps(
        [{"id": t.id, "x": t.x, "y": t.y, "type": t.track_type} for t in self.tracks]
    )

@rx.var
def data_script_tag(self) -> str:
    return f"<script>window.__SAGE_DATA__ = {self.get_data_json()};</script>"
```

### CRT Render Loop (CRITICAL - DO NOT BREAK)

**2.5-Second Refresh Cycle Implementation** (`assets/crt_radar.js`):

```javascript
// SAGE 2.5-second computer refresh cycle (Phase 3 - Priority 7)
this.lastComputerRefresh = Date.now();
this.refreshInterval = 2500; // milliseconds (historically accurate)
this.enableRefreshCycle = true; // Toggle for A/B comparison

render() {
    const now = Date.now();
    const timeSinceRefresh = now - this.lastComputerRefresh;
    
    // Phosphor decay continues at 60fps (ALWAYS)
    this.applyPhosphorDecay();
    
    // Computer refreshes display every 2.5 seconds
    const shouldRefresh = this.enableRefreshCycle 
        ? (timeSinceRefresh >= this.refreshInterval)
        : true; // Continuous mode for comparison
    
    if (shouldRefresh) {
        this.updateTrackData();           // Fetch from window.__SAGE_*
        this.addSweepToPersistence();     // Write sweep to persistence layer
        this.drawTracksOnPersistence();   // Write tracks to persistence layer
        
        if (this.enableRefreshCycle) {
            this.lastComputerRefresh = now;
        }
    } else {
        // Between refreshes: only sweep, tracks persist via phosphor
        this.addSweepToPersistence();
    }
    
    // Composite persistence to main canvas (phosphor glow)
    this.ctx.drawImage(this.persistenceCanvas, 0, 0);
    
    requestAnimationFrame(() => this.render());
}

updateTrackData() {
    // Fetch fresh data from window globals (simulates computer reading drum)
    if (window.__SAGE_TRACKS__) this.tracks = window.__SAGE_TRACKS__;
    if (window.__SAGE_INTERCEPTORS__) this.interceptors = window.__SAGE_INTERCEPTORS__;
    if (window.__SAGE_OVERLAYS__) this.overlays = new Set(window.__SAGE_OVERLAYS__);
    if (window.__SAGE_GEO_DATA__) this.geoData = window.__SAGE_GEO_DATA__;
    if (window.__SAGE_NETWORK_STATIONS__) this.networkStations = window.__SAGE_NETWORK_STATIONS__;
}
```

**Key Points**:
- **Phosphor decay runs at 60fps** - smooth fading between computer updates
- **Track data updates every 2.5s** - matches SAGE display drum refresh timing
- **Tracks remain visible** via P14 orange afterglow persistence (2-3 seconds)
- **DO NOT** change `drawTracksOnPersistence()` to run every frame - breaks historical accuracy
- **DO NOT** remove `updateTrackData()` method - required for refresh cycle
- **DO NOT** change `refreshInterval` without documenting historical justification

```javascript
// Legacy polling pattern (for reference, not used with refresh cycle)
setInterval(() => {
  if (window.__SAGE_DATA__) {
    scope.updateData(window.__SAGE_DATA__);
  }
}, 100);
```

## File Locations

- `an_fsq7_simulator/interactive_sage.py` - Main Reflex state, handlers, JSON serialization, script tag injection.
- `an_fsq7_simulator/sim/models.py` - Core simulation models (tracks, interceptors, tubes, drum, etc.).
- `an_fsq7_simulator/state_model.py` - Reflex-friendly dataclasses / state structures.
- `an_fsq7_simulator/components_v2/*.py` - UI components (register in `components_v2/__init__.py`).
- `assets/crt_radar.js` - Radar / CRT rendering code.

## Git Workflow

```powershell
# Standard commit workflow
git add .
git commit -m "feat: description of feature"
git push origin main

# Check current status
git status
git log --oneline -5

# View changes
git diff
git diff --staged
```

Agents should not rewrite git history (no rebase, reset --hard, etc.) unless explicitly asked.

## Debugging

**Server Issues**:

1. Check imports:
   ```powershell
   uv run python -c "import an_fsq7_simulator.interactive_sage; print('OK')"
   ```

2. Kill zombie Python processes:
   ```powershell
   Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force
   ```

3. Clear Reflex cache and restart:
   ```powershell
   Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue
   uv run reflex run
   ```

**WebSocket Warnings** (`Attempting to send delta to disconnected client`):
- **HARMLESS** during refresh/hot reload.
- Ignore unless persistent for more than ~30s.

**JS Not Getting Data**:
- Open DevTools (F12) and check that `window.__SAGE_*` globals exist.
- Verify polling in `assets/crt_radar.js` is running.

**VarTypeError**:
- Usually caused by using Python `if/else` or `and/or/not` on Reflex Vars.
- Fix by using `rx.cond`, `|`, `&`, `~`.

## Test Pipeline (agents MUST run before committing)

Whenever you change Python logic or UI components, run these from the repo root using `uv`:

```powershell
# 1) Core unit + sim tests (CPU, drum, light gun, scenarios)
uv run pytest tests/unit
uv run pytest tests/sim

# 2) Design-language / UI contract tests (layout + anti-patterns)
uv run pytest tests/design_language

# 3) (Optional) Property-based tests for numerical correctness
uv run pytest tests/property_based
```

**Rules for agents**:
- Do not skip failing tests; fix them or explicitly call out why they are failing.
- Prefer adding tests when you introduce a new subsystem or UI component.
- If a test directory doesn't exist yet (e.g., `tests/design_language`), create it and add at least one basic test.
- If you can't run a test suite (missing tool, unsupported OS, etc.), state that clearly in comments/PR description.

## Browser Testing with Playwright (Automated UI Tests)

**Overview**: Playwright provides automated browser testing for the SAGE simulator UI. This complements unit tests (core logic) with end-to-end UI validation (Reflex components, canvas interactions, workflows).

**What to test with Playwright**:
- ✅ UI component rendering and visibility
- ✅ Button clicks and form interactions
- ✅ Canvas-based interactions (radar, light gun)
- ✅ JavaScript data injection (window.__SAGE_*)
- ✅ End-to-end workflows (light gun → track selection → classification → intercept)
- ✅ Scenario execution and debrief display
- ✅ Keyboard shortcuts (once implemented)

**What NOT to test with Playwright**:
- ❌ Pure Python logic (use unit tests in tests/unit/)
- ❌ Simulation math (use property tests in tests/property_based/)
- ❌ CPU core operations (use tests/unit/test_cpu.py)

### Installation (Already Complete)

Playwright is already installed and configured:

```powershell
# Verify Playwright is installed
uv run python -c "import playwright; print(f'Playwright {playwright.__version__}')"

# Verify Chromium browser is installed
uv run playwright install --list
```

**Expected output**:
```
Playwright 1.56.0
Chromium 141.0.7390.37 (playwright build v1194) - downloaded
```

### Running Browser Tests

**Prerequisites**: Reflex dev server MUST be running first:

```powershell
# Terminal 1: Start dev server (REQUIRED)
uv run reflex run

# Terminal 2: Run browser tests once server is ready
uv run pytest tests/browser -c pytest-playwright.ini

# Run with visible browser (headed mode)
uv run pytest tests/browser --headed

# Run specific test
uv run pytest tests/browser/test_ui_smoke.py::TestUILoad::test_homepage_loads_successfully --headed

# Run only smoke tests
uv run pytest tests/browser -m smoke
```

### Configuration

**pytest-playwright.ini**:
```ini
[pytest]
markers =
    browser: Browser-based tests using Playwright
    slow: Tests that take longer than 5 seconds
    smoke: Quick smoke tests for critical paths

base_url = http://localhost:3000
headed = false
browser = chromium
slowmo = 0

testpaths = tests/browser
timeout = 30
```

**Markers**:
- `@pytest.mark.browser` - All Playwright tests must have this
- `@pytest.mark.smoke` - Critical path smoke tests (run first)
- `@pytest.mark.slow` - Tests that take >5 seconds

### Writing Browser Tests

**Basic Structure**:

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser
def test_my_feature(page: Page):
    """Test description."""
    # Navigate to app
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")
    
    # Interact with UI
    button = page.get_by_role("button", name="ARM LIGHT GUN")
    button.click()
    
    # Assert state
    expect(button).to_have_class("armed")
```

**Available Fixtures** (see tests/browser/conftest.py):

```python
@pytest.mark.browser
def test_with_app_loaded(sage_app):
    """sage_app fixture: page already loaded at localhost:3000."""
    assert sage_app.title() == "AN/FSQ-7 SAGE System Simulator"

@pytest.mark.browser
def test_with_scenario_active(sage_with_scenario):
    """sage_with_scenario: app loaded with scenario running."""
    # Scenario already started, can test active state
    pass

@pytest.mark.browser
def test_with_light_gun_armed(light_gun_armed):
    """light_gun_armed: light gun already armed for selection."""
    # Can immediately test track selection
    pass
```

**Common Patterns**:

```python
# 1. Find elements by role (RECOMMENDED)
button = page.get_by_role("button", name="ARM LIGHT GUN")
heading = page.get_by_role("heading", name="Track Details")

# 2. Find by CSS selector
canvas = page.locator("#radar-scope-canvas")
panel = page.locator(".track-detail-panel")

# 3. Wait for elements
expect(canvas).to_be_visible(timeout=5000)
page.wait_for_selector("#radar-scope-canvas", state="visible")

# 4. Click elements
button.click()
canvas.click(position={"x": 400, "y": 300})

# 5. Check JavaScript state
has_tracks = page.evaluate("() => typeof window.__SAGE_TRACKS__ !== 'undefined'")
tracks = page.evaluate("() => window.__SAGE_TRACKS__")

# 6. Assert conditions
expect(button).to_be_visible()
expect(button).to_be_enabled()
expect(button).to_have_text("ARMED")
expect(canvas).to_have_attribute("width", "800")

# 7. Wait for network idle
page.wait_for_load_state("networkidle")

# 8. Handle timeouts
page.wait_for_timeout(1000)  # Wait 1 second
```

### Testing Canvas Interactions

**Radar canvas clicks** (light gun selection):

```python
@pytest.mark.browser
def test_light_gun_selection(light_gun_armed):
    """Test light gun track selection on radar canvas."""
    canvas = light_gun_armed.locator("#radar-scope-canvas")
    
    # Get canvas dimensions
    box = canvas.bounding_box()
    
    # Click at specific position (center of canvas)
    center_x = box["width"] / 2
    center_y = box["height"] / 2
    canvas.click(position={"x": center_x, "y": center_y})
    
    # Verify selection occurred
    light_gun_armed.wait_for_timeout(500)
    selected_track = light_gun_armed.evaluate("() => window.crtRadarScope?.selectedTrack")
    assert selected_track is not None, "No track selected"
```

### Debugging Browser Tests

**Run with headed browser to see what's happening**:

```powershell
uv run pytest tests/browser/test_ui_smoke.py::test_homepage_loads_successfully --headed --slowmo 1000
```

**Options**:
- `--headed` - Show browser window (default is headless)
- `--slowmo 1000` - Slow down actions by 1000ms for debugging
- `--browser firefox` - Use Firefox instead of Chromium
- `--tracing on` - Record test execution traces

**Inspect failures**:

```powershell
# Take screenshot on failure (add to conftest.py)
@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"test-screenshots/{request.node.name}.png")
```

**Check console logs**:

```python
@pytest.mark.browser
def test_no_js_errors(page: Page):
    """Verify no JavaScript errors."""
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Filter out expected WebSocket warnings
    serious_errors = [e for e in errors if "WebSocket" not in e]
    assert len(serious_errors) == 0, f"Console errors: {serious_errors}"
```

### Common Issues

**1. "Server not running" error**:

```
pytest.fail("Server not responding correctly. Run: uv run reflex run")
```

**Fix**: Start dev server in a separate terminal before running tests:

```powershell
# Terminal 1
uv run reflex run

# Terminal 2 (once server shows "App running at: http://localhost:3000")
uv run pytest tests/browser
```

**2. "Element not found" timeout**:

```
TimeoutError: locator.click: Timeout 30000ms exceeded.
```

**Fix**: Increase timeout or wait for element to appear:

```python
# Option 1: Increase timeout
button = page.get_by_role("button", name="ARM LIGHT GUN")
button.click(timeout=10000)  # 10 seconds

# Option 2: Wait for visibility first
expect(button).to_be_visible(timeout=10000)
button.click()

# Option 3: Wait for network idle
page.wait_for_load_state("networkidle")
```

**3. "Canvas not initialized" error**:

**Fix**: Wait for CRT radar scope to initialize:

```python
# Wait for canvas element
canvas = page.locator("#radar-scope-canvas")
expect(canvas).to_be_visible(timeout=5000)

# Wait for JavaScript initialization
page.wait_for_timeout(1000)

# Verify scope exists
has_scope = page.evaluate("() => typeof window.crtRadarScope !== 'undefined'")
assert has_scope, "CRT radar scope not initialized"
```

**4. "Chromium executable doesn't exist" error**:

```powershell
# Reinstall Chromium browser
uv run playwright install chromium
```

**5. "window.__SAGE_* is undefined"**:

**Fix**: Wait for data injection scripts to execute:

```python
page.goto("http://localhost:3000")
page.wait_for_load_state("networkidle")
page.wait_for_timeout(1000)  # Wait for data injection

# Verify globals exist
has_tracks = page.evaluate("() => typeof window.__SAGE_TRACKS__ !== 'undefined'")
assert has_tracks, "window.__SAGE_TRACKS__ not injected"
```

### CI/CD Integration (Future)

**GitHub Actions workflow** (future enhancement):

```yaml
name: Browser Tests

on: [push, pull_request]

jobs:
  playwright:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv pip install -r requirements.txt
      - name: Install Playwright
        run: uv run playwright install chromium
      - name: Start dev server
        run: uv run reflex run &
      - name: Wait for server
        run: Start-Sleep -Seconds 10
      - name: Run browser tests
        run: uv run pytest tests/browser -c pytest-playwright.ini
```

### Testing Checklist (manual + smoke tests)

Before you consider a change "done":

- [ ] `uv run python -c "import an_fsq7_simulator.interactive_sage"` succeeds (no import errors).
- [ ] Server starts: `uv run reflex run` without crashing.
- [ ] Browser loads at http://localhost:3000.
- [ ] UI renders with no red errors in F12 console.
- [ ] `window.__SAGE_*` globals are present and populated in DevTools.
- [ ] **Playwright smoke tests pass**: `uv run pytest tests/browser -m smoke`
- [ ] Basic interactions work end-to-end:
  - [ ] Tracks render and move over time.
  - [ ] Light gun / selection flow responds (arm → click → selection).
  - [ ] Intercept actions change state visibly (selected track, engagement state, debrief metrics).

Agents should prioritize fixing import failures, crashes, and console errors before working on new features.

## Browser Testing with Playwright MCP

These are helper patterns for agents that have access to Playwright MCP tools.

### Activating Browser Testing Tools

```typescript
activate_browser_interaction_tools()      // Click, type, navigate
activate_page_capture_tools_2()          // Screenshots, snapshots
```

### Common Testing Patterns

**Navigate to the app**:
```javascript
mcp_playwright-ex_browser_navigate({ url: "http://localhost:3000" })
```

**Take a screenshot**:
```javascript
mcp_playwright-ex_browser_take_screenshot({
  fullPage: true,
  filename: "test-screenshots/feature-name.png"
})
```

**Check page structure**:
```javascript
mcp_playwright-ex_browser_snapshot()  // Returns refs for clicking
```

**Click an element**:
```javascript
mcp_playwright-ex_browser_click({
  ref: "e202",  // From snapshot
  element: "ARM LIGHT GUN button"
})
```

**Execute JavaScript in browser**:
```javascript
mcp_playwright-ex_browser_evaluate({
  function: "() => { return window.__SAGE_INTERCEPTORS__; }"
})
```

### Verifying Data Injection

```javascript
// Check window globals
mcp_playwright-ex_browser_evaluate({
  function: `() => ({ tracks: window.__SAGE_TRACKS__, interceptors: window.__SAGE_INTERCEPTORS__ })`
})

// Check CRT radar scope
mcp_playwright-ex_browser_evaluate({
  function: `() => window.crtRadarScope
    ? { interceptors: window.crtRadarScope.interceptors }
    : 'not found'`
})
```

### Canvas Interaction

```javascript
// Click on radar at normalized coords (0.875, 0.125)
mcp_playwright-ex_browser_evaluate({
  function: `() => {
    const canvas = document.getElementById('radar-scope-canvas');
    if (!canvas) return 'canvas not found';
    const rect = canvas.getBoundingClientRect();
    const x = rect.left + rect.width * 0.875;
    const y = rect.top + rect.height * 0.125;
    canvas.dispatchEvent(new MouseEvent('click', {
      bubbles: true,
      clientX: x,
      clientY: y
    }));
    return { clickedAt: { x, y } };
  }`
})
```

### Common Issues

1. **Page not loading**: Wait for initial Reflex compilation / hot reload to finish.
2. **Canvas not found**: Wait for `[CRT] ✓ Radar scope initialized` in DevTools console.
3. **Elements disabled**: Check prerequisites (light gun armed, track selected, scenario state).
4. **Data missing**: Check console for `[SAGE] Executed N data injection scripts` and verify `window.__SAGE_*` exists.



## Common Gotchas

1. **UV is required** – don't try to run `reflex` or `python` directly.
2. **Reflex Var types** – cannot use `and` / `or` / `not` or inline `if/else` on Vars.
3. **Script tag injection** – must use `@rx.var` computed properties for data injection.
4. **JavaScript polling** – data flows via `window.__SAGE_*` and periodic polling.
5. **Hot reload** – sometimes requires manual `.reflex` cache clear.
6. **Type hints** – Lint errors may be non-blocking, but fix obvious type mismatches.
7. **Canvas coordinates** – normalized 0.0–1.0; multiply by width/height in JS.
8. **Heading angles** – stored in degrees; convert to radians in JS (`deg * Math.PI / 180`).
9. **WebSocket warnings** – "Attempting to send delta to disconnected client" is normal during refreshes.

## Priority System

Current roadmap priorities:

- ✅ Priority 1: Track Correlation System (COMPLETE)
- ✅ Priority 2: Interceptor Assignment System (COMPLETE)
- ✅ Priority 3: System Inspector Overlay (COMPLETE)
- ✅ Priority 4: Scenario Debrief System (COMPLETE – 7 scenarios with performance tracking)
- ✅ Priority 5: Sound Effects & Audio Feedback (COMPLETE)
- ✅ Priority 6: Network & Station View (COMPLETE)
- ✅ Priority 7: Dynamic Scenario Events (COMPLETE – 8 event types, system messages panel with reactive UI)

When implementing new features:
1. Update `sim/models.py` for core domain models.
2. Update `state_model.py` for Reflex-compatible models.
3. Add state fields to `InteractiveSageState`.
4. Create UI component in `components_v2/`.
5. Register component in `components_v2/__init__.py`.
6. Add event handlers to `interactive_sage.py`.
7. Add JavaScript rendering if needed in `assets/*.js`.
8. Run the **Test Pipeline** (`uv run pytest ...`) and the **Testing Checklist**.
9. Commit and push to Git.

## Agent Collaboration Notes

When multiple agents work on this project:
- Always check `PROJECT_STATUS.md` for current status and roadmap.
- Read `CHANGELOG.md` for recent feature additions.
- Check `agents.md` (this file) for common patterns and constraints.
- Review `CONTRIBUTING.md` for testing guidelines and PR process.
- Use `git log --oneline -10` to see recent work.
- Don't assume commands work without the `uv run` prefix.
- Don't introduce new tools or package managers without updating this file.

## Emergency Recovery

If the project is completely broken:

```powershell
# 1. Stop all Python processes
Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Clear Reflex cache
Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue

# 3. Verify Python imports work
uv run python -c "import an_fsq7_simulator.interactive_sage; print('OK')"

# 4. If imports fail, check syntax in the error'd file and fix those first.

# 5. Try starting server with more logs
uv run reflex run --loglevel info

# 6. If still broken, inspect recent history
git log --oneline -10
git show HEAD   # See last commit

# 7. As a last resort, consider reverting to last working commit
git reset --hard HEAD~1  # DESTRUCTIVE – use with caution
```
