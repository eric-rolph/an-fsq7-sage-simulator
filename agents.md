# Agent Development Guide

This document contains critical patterns, commands, and gotchas for AI agents working on this SAGE simulator project.

## Environment & Tools

### Python Environment - UV Package Manager

**CRITICAL**: This project uses `uv` for Python package management, NOT conda/pip/poetry.

```powershell
# ✅ CORRECT - Run commands with uv
uv run reflex run
uv run python script.py
uv run pytest

# ❌ WRONG - Do not use these
reflex run                    # Will fail: command not found
python script.py              # Uses wrong Python/packages
pip install package           # Installs to wrong environment
```

### Starting the Development Server

```powershell
# Method 1: Direct uv command (PREFERRED)
uv run reflex run

# Method 2: Using setup script
.\setup.ps1 run

# Method 3: Manual with logging
uv run reflex run --loglevel info
```

**Common Server Issues**:
- If server won't start, check for zombie Python processes:
  ```powershell
  Get-Process -Name python* -ErrorAction SilentlyContinue | Stop-Process -Force
  ```
- If changes aren't reflected, clear Reflex cache:
  ```powershell
  Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue
  ```

### Testing Python Imports

```powershell
# Test if module imports successfully
uv run python -c "import an_fsq7_simulator.interactive_sage; print('Import successful')"

# Test specific functionality
uv run python -c "from an_fsq7_simulator import interactive_sage; state = interactive_sage.InteractiveSageState(); print(f'Interceptors: {len(state.interceptors)}')"
```

## Reflex Framework Patterns

### Critical Reflex Rules

**NEVER use Python conditionals/operators with Reflex Var types**:

```python
# ❌ WRONG - Will cause VarTypeError
color = "green" if fuel_percent > 60 else "red"
disabled = (status != "READY") and (fuel < 50)
items = [x for x in my_list if x.status == "READY"]

# ✅ CORRECT - Use Reflex operators and components
color = rx.cond(fuel_percent > 60, "green", "red")
disabled = (status != "READY") | (fuel < 50)  # Use bitwise operators
items = rx.foreach(my_list, lambda x: rx.cond(x.status == "READY", render_item(x), rx.fragment()))
```

### Nested Conditionals

```python
# ✅ CORRECT - Nested rx.cond for multiple conditions
rx.cond(
    fuel_percent > 60,
    rx.progress(color_scheme="green", ...),
    rx.cond(
        fuel_percent > 30,
        rx.progress(color_scheme="yellow", ...),
        rx.progress(color_scheme="red", ...)
    )
)
```

### Reflex Boolean Operators

```python
# Use bitwise operators with Reflex Var types
disabled = (condition1) | (condition2)      # OR
disabled = (condition1) & (condition2)      # AND
disabled = ~(condition1)                    # NOT
```

### Computed Vars for JavaScript Injection

```python
@rx.var
def data_script_tag(self) -> str:
    """Return complete script tag for JavaScript injection"""
    return f"<script>window.__SAGE_DATA__ = {self.get_data_json()};</script>"

# Then inject in the page:
rx.html(InteractiveSageState.data_script_tag)
```

## JavaScript Integration Patterns

### Data Injection from Python to JavaScript

**Pattern**: Python state → JSON → window global → JavaScript reads periodically

```python
# Step 1: Create JSON serialization method
def get_interceptors_json(self) -> str:
    data = [{"id": i.id, "x": i.x, "y": i.y} for i in self.interceptors]
    return json.dumps(data)

# Step 2: Create computed var for script tag
@rx.var
def interceptors_script_tag(self) -> str:
    return f"<script>window.__SAGE_INTERCEPTORS__ = {self.get_interceptors_json()};</script>"

# Step 3: Inject in page (interactive_sage.py ~line 1520)
rx.html(InteractiveSageState.interceptors_script_tag)
```

```javascript
// Step 4: JavaScript reads data periodically (assets/crt_radar.js ~line 480)
setInterval(function() {
    if (window.crtRadarScope && window.__SAGE_INTERCEPTORS__) {
        window.crtRadarScope.updateInterceptors(window.__SAGE_INTERCEPTORS__);
    }
}, 100);  // Poll every 100ms
```

### Hot Reload Fallback

```javascript
// Execute inline scripts on hot reload (crt_radar.js ~line 457)
if (!sageScriptsExecuted && !window.__SAGE_TRACKS__) {
    var scripts = Array.from(document.querySelectorAll('script'));
    scripts.forEach(function(s) {
        var text = s.innerHTML || '';
        if (text.includes('__SAGE_')) {
            eval(text);
        }
    });
    sageScriptsExecuted = true;
}
```

## Common File Locations

### Key Files for Data Flow

1. **State Management**: `an_fsq7_simulator/interactive_sage.py`
   - Main Reflex state class (InteractiveSageState)
   - Event handlers and simulation logic
   - JSON serialization methods (~line 1290+)
   - Script tag injection (~line 1526)

2. **Data Models**: 
   - `an_fsq7_simulator/sim/models.py` - Core simulation models
   - `an_fsq7_simulator/state_model.py` - Reflex-compatible dataclasses

3. **UI Components**: `an_fsq7_simulator/components_v2/*.py`
   - Each component is a separate module
   - Import with: `from an_fsq7_simulator.components_v2 import component_name`

4. **JavaScript Assets**: `assets/*.js`
   - `crt_radar.js` - Main radar scope rendering
   - Must be loaded via `rx.script()` or external file

### Component Registration

```python
# In components_v2/__init__.py
from .new_component import new_component_panel

__all__ = ["new_component_panel", ...]

# Then import in interactive_sage.py
from an_fsq7_simulator.components_v2 import new_component_panel
```

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

## Debugging Patterns

### Server Won't Start

1. Check for Python syntax errors:
   ```powershell
   uv run python -c "import an_fsq7_simulator.interactive_sage"
   ```

2. Check for zombie processes:
   ```powershell
   Get-Process -Name python* -ErrorAction SilentlyContinue
   ```

3. Clear Reflex cache and restart:
   ```powershell
   Remove-Item -Path .\.reflex -Recurse -Force -ErrorAction SilentlyContinue
   uv run reflex run
   ```

### JavaScript Not Receiving Data

1. Check browser console for errors (F12)
2. Verify window global exists: `console.log(window.__SAGE_TRACKS__)`
3. Verify script tag is in DOM: Check "Elements" tab for `<script>` with `window.__SAGE_`
4. Check polling interval is running in crt_radar.js

### Reflex VarTypeError

**Symptom**: `TypeError: cannot use Python operator with Var type`

**Solution**: Replace Python boolean operators with Reflex equivalents:
- `if/else` → `rx.cond()`
- `and` → `&`
- `or` → `|`
- `not` → `~`
- List comprehension → `rx.foreach()` with lambda

## Project Architecture Patterns

### State Machine Pattern

Used for interceptor status transitions:

```python
def update_interceptor_positions(self, dt: float = 1.0):
    for i in range(len(self.interceptors)):
        interceptor = self.interceptors[i]
        
        if interceptor.status == "SCRAMBLING":
            # Accelerate and climb
            interceptor.current_speed += 50 * dt
            interceptor.altitude += 500 * dt
            if interceptor.current_speed >= interceptor.max_speed * 0.9:
                interceptor.status = "AIRBORNE"
        
        elif interceptor.status == "AIRBORNE":
            # Move toward target
            if interceptor.assigned_target_id:
                target = self.get_track_by_id(interceptor.assigned_target_id)
                if target and interceptor.is_in_weapon_range(target.x, target.y):
                    interceptor.status = "ENGAGING"
        
        # ... more states
```

### Distance-Based Selection Algorithm

```python
def get_best_interceptor_for_track(self, track_id: str) -> Optional[str]:
    track = self.get_track_by_id(track_id)
    ready_interceptors = [i for i in self.interceptors if i.status == "READY"]
    
    best_score = -1
    best_interceptor = None
    
    for interceptor in ready_interceptors:
        distance = interceptor.distance_to_target(track.x, track.y)
        
        # Weighted scoring: distance 60%, fuel 20%, speed 20%
        distance_score = max(0, 1.0 - distance / 1.0)
        fuel_score = interceptor.fuel_percent / 100.0
        speed_score = interceptor.max_speed / 1600.0
        
        total_score = (distance_score * 0.6 + 
                      fuel_score * 0.2 + 
                      speed_score * 0.2)
        
        if total_score > best_score:
            best_score = total_score
            best_interceptor = interceptor
    
    return best_interceptor.id if best_interceptor else None
```

## Testing Checklist

Before committing major features:

- [ ] `uv run python -c "import an_fsq7_simulator.interactive_sage"` succeeds
- [ ] Server starts without errors: `uv run reflex run`
- [ ] Browser loads at http://localhost:3000
- [ ] UI components render correctly
- [ ] JavaScript console shows no errors (F12)
- [ ] Data flows from Python to JavaScript (check window globals)
- [ ] Interactive elements respond to clicks
- [ ] Simulation loop runs without crashes

## Performance Considerations

### Reflex State Updates

- Minimize computed var calculations - they run on every render
- Use `@rx.var(cache=True)` for expensive computations
- Batch state updates when possible

### JavaScript Rendering

- Use `requestAnimationFrame` for smooth animations
- Throttle data polling to 100ms (not faster)
- Clear old canvas paths before drawing new ones
- Use separate canvases for persistence and bright overlays

## Common Gotchas

1. **UV is required** - Don't try to run `reflex` or `python` directly
2. **Reflex Var types** - Cannot use Python boolean operators
3. **Script tag injection** - Must use `@rx.var` computed property
4. **JavaScript polling** - Data doesn't push, it polls window globals
5. **Hot reload** - Sometimes requires manual cache clear
6. **Type hints** - Lint errors are often non-blocking in Reflex
7. **Canvas coordinates** - Normalized 0.0-1.0, multiply by width/height
8. **Heading angles** - In degrees, convert to radians for JavaScript: `* Math.PI / 180`

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
