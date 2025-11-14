# Agent Development Guide

Critical patterns and gotchas for AI agents working on this SAGE simulator project.

## UV Package Manager (CRITICAL)

This project uses `uv` for Python - NOT conda/pip/poetry.

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
# Server won't start - kill zombie processes
Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force

# Changes not reflected - clear cache
Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue

# Test imports
uv run python -c "import an_fsq7_simulator.interactive_sage; print('OK')"
```

## Reflex Framework Rules

**NEVER use Python operators with Reflex Var types** (causes VarTypeError):

```python
# ❌ WRONG
color = "green" if fuel > 60 else "red"
disabled = (status != "READY") and (fuel < 50)

# ✅ CORRECT
color = rx.cond(fuel > 60, "green", "red")  # Use rx.cond
disabled = (status != "READY") | (fuel < 50)  # Use | & ~ operators
items = rx.foreach(list, lambda x: ...)  # Not list comprehension
```

**JavaScript Data Injection**:
```python
@rx.var
def data_script_tag(self) -> str:
    return f"<script>window.__DATA__ = {self.get_json()};</script>"

# In page: rx.html(InteractiveSageState.data_script_tag)
```

## JavaScript Integration

**Data Flow**: Python → JSON → window global → JS polls every 100ms

```python
def get_data_json(self) -> str:
    return json.dumps([{"id": i.id, "x": i.x} for i in self.items])

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

- `an_fsq7_simulator/interactive_sage.py` - State, handlers, JSON serialization (~1290), injection (~1526)
- `an_fsq7_simulator/sim/models.py` - Core simulation models
- `an_fsq7_simulator/state_model.py` - Reflex dataclasses
- `an_fsq7_simulator/components_v2/*.py` - UI components (register in `__init__.py`)
- `assets/crt_radar.js` - Radar rendering

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

## Debugging

**Server Issues**:
1. Syntax: `uv run python -c "import an_fsq7_simulator.interactive_sage"`
2. Zombies: `Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force`
3. Cache: `Remove-Item .\.reflex -Recurse -Force; uv run reflex run`

**WebSocket Warnings** (`Attempting to send delta to disconnected client`): **HARMLESS** - normal during refresh/hot reload. Ignore unless persistent >30s.

**JS Not Getting Data**: F12 console → check `window.__SAGE_*` exists → verify polling in crt_radar.js

**VarTypeError**: Use `rx.cond()` not `if/else`, use `| & ~` not `and or not`



## Testing Checklist

- [ ] `uv run python -c "import an_fsq7_simulator.interactive_sage"` succeeds
- [ ] Server starts: `uv run reflex run`
- [ ] Browser loads at http://localhost:3000
- [ ] UI renders, no console errors (F12)
- [ ] Data flows to JavaScript (check window globals)
- [ ] Interactive elements respond

## Browser Testing with Playwright MCP

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
  function: `() => window.crtRadarScope ? { interceptors: window.crtRadarScope.interceptors } : 'not found'`
})
```

### Canvas Interaction

```javascript
// Click on radar at normalized coords (0.875, 0.125)
mcp_playwright-ex_browser_evaluate({
  function: `() => {
    const canvas = document.getElementById('radar-scope-canvas');
    const rect = canvas.getBoundingClientRect();
    const x = rect.left + rect.width * 0.875;
    const y = rect.top + rect.height * 0.125;
    canvas.dispatchEvent(new MouseEvent('click', { bubbles: true, clientX: x, clientY: y }));
    return { clickedAt: { x, y } };
  }`
})
```

### Common Issues

1. **Page not loading**: Wait for initial compilation
2. **Canvas not found**: Wait for `[CRT] ✓ Radar scope initialized`
3. **Elements disabled**: Check prereqs (light gun armed, track selected)
4. **Data missing**: Check console for `[SAGE] Executed N data injection scripts`



## Common Gotchas

1. **UV is required** - Don't try to run `reflex` or `python` directly
2. **Reflex Var types** - Cannot use Python boolean operators
3. **Script tag injection** - Must use `@rx.var` computed property
4. **JavaScript polling** - Data doesn't push, it polls window globals
5. **Hot reload** - Sometimes requires manual cache clear
6. **Type hints** - Lint errors are often non-blocking in Reflex
7. **Canvas coordinates** - Normalized 0.0-1.0, multiply by width/height
8. **Heading angles** - In degrees, convert to radians for JavaScript: `* Math.PI / 180`
9. **WebSocket warnings** - "Attempting to send delta to disconnected client" warnings are normal during refreshes/hot reloads and can be safely ignored

## Priority System

Current roadmap priorities:

- ✅ Priority 1: Track Correlation System (COMPLETE)
- ✅ Priority 2: Interceptor Assignment System (COMPLETE - visualization added)
- ⏳ Priority 3: System Inspector Overlay (NEXT)

When implementing new features:
1. Update `sim/models.py` for core domain models
2. Update `state_model.py` for Reflex-compatible models
3. Add state fields to `InteractiveSageState`
4. Create UI component in `components_v2/`
5. Register component in `components_v2/__init__.py`
6. Add event handlers to `interactive_sage.py`
7. Add JavaScript rendering if needed in `assets/*.js`
8. Test with `uv run reflex run`
9. Commit and push to Git

## Agent Collaboration Notes

When multiple agents work on this project:
- Always check `TODO_COMPLETION_REPORT.md` for current status
- Read `DEVELOPMENT_ROADMAP.md` for priority order
- Check `agents.md` (this file!) for common patterns
- Use `git log --oneline -10` to see recent work
- Don't assume commands work without `uv run` prefix

## Emergency Recovery

If the project is completely broken:

```powershell
# 1. Stop all Python processes
Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force

# 2. Clear Reflex cache
Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue

# 3. Verify Python imports work
uv run python -c "import an_fsq7_simulator.interactive_sage; print('OK')"

# 4. If imports fail, check syntax in the error'd file
# Fix Python syntax errors first

# 5. Try starting server
uv run reflex run --loglevel info

# 6. If still broken, check git history
git log --oneline -10
git show HEAD   # See last commit

# 7. Consider reverting to last working commit
git reset --hard HEAD~1  # DESTRUCTIVE - use with caution
```
