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

### CRT Display
Scope is a **vector CRT**:
- Use **strokes** (blips, lines, arcs, polylines, vector glyphs) – not filled HUD widgets over the radar picture.
- Visual hierarchy:
  - **Map/coastlines/static geometry**: thin, low-intensity strokes.
  - **Range rings/grids**: slightly brighter, but still secondary.
  - **Tracks/selected targets**: brightest strokes; selection adds halo/outline, not a random UI chip floating over the scope.

### Threat Encoding
Threat state differences must be visible via **shape/pattern**, not color alone:
- E.g. symbol shape (diamond vs circle vs square), solid vs dashed vs dotted strokes.
- Color changes (friendly/hostile/unknown) are allowed as an accessibility/clarity layer, but must not be the only signal.

### Agent Behavior
- When editing components in `an_fsq7_simulator/components_v2/`, keep these invariants intact.
- If a change needs to bend a rule, document it and adjust tests so it's intentional, not accidental.
- Prefer adding/adjusting tests in `tests/design_language` when you change layout or interaction patterns.

## JavaScript Integration

**Data Flow**: Python → JSON → window global → JS polls every 100ms

```python
def get_data_json(self) -> str:
    return json.dumps(
        [{"id": t.id, "x": t.x, "y": t.y, "type": t.track_type} for t in self.tracks]
    )

@rx.var
def data_script_tag(self) -> str:
    return f"<script>window.__SAGE_DATA__ = {self.get_data_json()};</script>"
```

```javascript
// JavaScript polls window globals
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

## Testing Checklist (manual + smoke tests)

Before you consider a change "done":

- [ ] `uv run python -c "import an_fsq7_simulator.interactive_sage"` succeeds (no import errors).
- [ ] Server starts: `uv run reflex run` without crashing.
- [ ] Browser loads at http://localhost:3000.
- [ ] UI renders with no red errors in F12 console.
- [ ] `window.__SAGE_*` globals are present and populated in DevTools.
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
- Always check `TODO_COMPLETION_REPORT.md` for current status.
- Read `DEVELOPMENT_ROADMAP.md` for priority order.
- Check `AGENTS.md` (this file) for common patterns and constraints.
- Use `git log --oneline -10` to see recent work.
- Don't assume commands work without the `uv run` prefix.
- Don't introduce new tools or package managers without updating this file and the roadmap.

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
