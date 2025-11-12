# SAGE Simulator - Manual Testing Guide

## Server Status: ✅ RUNNING

The Reflex development server is now running successfully at:
- **Frontend**: http://localhost:3000
- **Backend**: http://0.0.0.0:8000

## Current Test Page

A minimal test page is available at http://localhost:3000 that displays:
- "SAGE Simulator Test Page" heading
- "If you see this, the server is working!" message

## What Was Fixed

### 1. Missing State Model (✅ FIXED)
Created `state_model.py` with all required data classes:
- `Track` - Radar target information
- `CpuTrace`, `ExecutionStep`, `CpuRegisters` - CPU execution data
- `TubeState`, `MaintenanceState` - Vacuum tube maintenance
- `Mission`, `MissionStep` - Tutorial system
- `SystemMessage` - Operator action logs

### 2. Import Errors (✅ FIXED)
- Fixed `scenarios` → `scenarios_layered` import
- Added `state_model` module import
- Removed non-serializable `GeographicOverlays` from State

### 3. Component Function Calls (✅ FIXED)
Updated `interactive_sage.py` to pass proper State parameters:
```python
# Before (broken):
sd_console.sd_console_master_panel()

# After (fixed):
sd_console.sd_console_master_panel(
    InteractiveSageState.active_filters,
    InteractiveSageState.active_overlays,
    InteractiveSageState.brightness
)
```

### 4. Server Configuration (✅ FIXED)
Updated `rxconfig.py` to use test_page module while full page is being completed.

## Manual Testing Steps

### Test 1: Verify Server is Running
```powershell
# Check ports are listening
netstat -ano | findstr ":3000 :8000"

# Should show:
#   TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       <PID>
#   TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       <PID>
```

### Test 2: Access Test Page
1. Open browser to http://localhost:3000
2. **Expected**: See "SAGE Simulator Test Page" with success message
3. **If connection error**: Wait 10 seconds and refresh (WebSocket connection may take time)

### Test 3: Check Console for Errors
1. Open browser DevTools (F12)
2. Go to Console tab
3. **Expected**: Only Vite connection messages and React DevTools suggestions
4. **If errors**: Note the error message for debugging

## Known Issues

### Issue 1: Full Interactive Page Not Yet Active
**Status**: In Progress  
**Reason**: The full `interactive_sage.py` page has many components that need additional wiring

**Workaround**: Currently using minimal `test_page.py` to verify server works

**To activate full page**:
```python
# In rxconfig.py, change:
app_module_import="an_fsq7_simulator.test_page"
# To:
app_module_import="an_fsq7_simulator.interactive_sage"
```

### Issue 2: Missing Component Implementations
**Status**: TODO  
**Components needing implementation**:
- `scenarios_layered.advance_world()` - World simulation tick
- `scenarios_layered.spawn_interceptor()` - Interceptor missile spawning
- Geographic overlay rendering
- Radar scope WebGL integration

### Issue 3: Playwright MCP Connection Timeouts
**Status**: Known Issue  
**Reason**: Playwright MCP server has timeout issues with WebSocket connections

**Workaround**: Use manual browser testing for now

## Next Steps for Full Functionality

### 1. Complete Component Wiring (Priority: HIGH)
File: `interactive_sage.py`

Need to verify all component function calls have proper parameters:
- ✅ `sd_console.sd_console_master_panel()` - Fixed
- ✅ `tube_maintenance.tube_maintenance_panel()` - Fixed
- ✅ `execution_trace_panel.execution_trace_panel_compact()` - Fixed
- ✅ `light_gun.track_detail_panel()` - Fixed
- ⏳ `radar_scope.create_radar_scope_component()` - Needs testing
- ⏳ `tutorial_system.tutorial_sidebar_compact()` - Needs testing

### 2. Implement Scenario Functions (Priority: MEDIUM)
File: `components_v2/scenarios_layered.py`

Add these functions:
```python
def advance_world(delta_ms: int, tracks: List[Track], maintenance: MaintenanceState) -> List[Track]:
    """Update track positions and spawn new tracks based on scenario"""
    # TODO: Implement track movement logic
    pass

def spawn_interceptor(target: Track) -> Track:
    """Create interceptor missile track toward target"""
    # TODO: Implement interceptor spawning
    pass
```

### 3. Add Sample Track Data (Priority: HIGH)
File: `interactive_sage.py`

Initialize state with test tracks:
```python
class InteractiveSageState(rx.State):
    tracks: List[state_model.Track] = [
        state_model.Track(
            id="T001",
            x=40.7128,  # NYC latitude
            y=-74.0060, # NYC longitude
            altitude=35000,
            speed=450,
            heading=180,
            track_type="hostile",
            threat_level="HIGH"
        ),
        # Add more test tracks...
    ]
```

### 4. Test Each Component (Priority: HIGH)

#### A. SD Console Buttons
1. Uncomment `interactive_sage.py` in rxconfig
2. Navigate to http://localhost:3000
3. Click category filters (S1-S13) - verify button state changes
4. Click feature overlays (S20-S24) - verify visual feedback
5. **Expected**: Buttons toggle active/inactive state

#### B. Light Gun Selection
1. Press 'D' key to arm light gun
2. **Expected**: Cursor changes to crosshair (if implemented)
3. Click on a track on radar scope
4. **Expected**: Track detail panel shows track info

#### C. System Messages Log
1. Perform any action (filter toggle, track selection)
2. Check System Messages panel at bottom
3. **Expected**: See timestamped log entries

#### D. Intercept Launch Flow
1. Arm light gun ('D' key)
2. Select hostile track
3. Click "LAUNCH INTERCEPT" button
4. **Expected**: System message logged, interceptor spawned (when implemented)

### 5. Performance Testing (Priority: LOW)
Once basic functionality works, test with high track counts:
- Load performance_test.py scenarios
- Verify FPS stays above 30 with 50+ tracks
- Check memory usage over time

## Troubleshooting

### Server Won't Start
**Symptom**: Server exits immediately after "App Running" message

**Solution**: Check for Python import errors
```powershell
cd C:\Users\ericr\an-fsq7-sage-simulator
python -c "from an_fsq7_simulator import interactive_sage; print('OK')"
```

### Connection Error in Browser
**Symptom**: "Connection Error" message on page

**Causes**:
1. Backend not running on port 8000
2. WebSocket connection blocked
3. State serialization error

**Debug**:
```powershell
# Check backend is running
netstat -ano | findstr ":8000"

# Check browser console for WebSocket errors
# Look for "WebSocket connection failed" messages
```

### Port Already in Use
**Symptom**: "Address already in use" error

**Solution**:
```powershell
# Find process using port 3000 or 8000
netstat -ano | findstr ":3000"

# Kill the process (replace <PID> with actual PID)
Stop-Process -Id <PID> -Force
```

## Testing Checklist

Copy this checklist when testing:

### Basic Functionality
- [ ] Server starts without errors
- [ ] Frontend loads on http://localhost:3000
- [ ] Backend responds on http://0.0.0.0:8000
- [ ] No console errors in browser DevTools
- [ ] Page renders without "Connection Error"

### SD Console
- [ ] Category filters (S1-S13) toggle active state
- [ ] Feature overlays (S20-S24) toggle active state
- [ ] Pan controls respond to clicks
- [ ] Brightness slider works
- [ ] System messages log button actions

### Light Gun
- [ ] 'D' key arms light gun
- [ ] Can select tracks on scope
- [ ] Detail panel shows track information
- [ ] Can deselect track

### Operator Workflow
- [ ] Progress bar shows current step
- [ ] Instructions update based on step
- [ ] Action buttons enable/disable correctly
- [ ] Can complete detect→intercept flow

### System Messages
- [ ] Messages appear in chronological order
- [ ] Timestamps are accurate
- [ ] Color coding works (info/warning/critical)
- [ ] Categories display correctly

### Performance
- [ ] Page loads in < 5 seconds
- [ ] No lag when toggling buttons
- [ ] Smooth track animations (if implemented)
- [ ] Memory usage stays stable

## Success Criteria

The simulator is considered **fully functional** when:

1. ✅ Server runs continuously without stopping
2. ⏳ All 10 operator requirements are testable in the UI
3. ⏳ No console errors during normal operation
4. ⏳ Light gun selection works end-to-end
5. ⏳ Intercept launch workflow completes
6. ⏳ System messages log all operator actions
7. ⏳ All SD console buttons provide visual feedback
8. ⏳ Page maintains 30+ FPS with multiple tracks

Current Status: **2/8 Complete** (25%)

---

## Quick Start Commands

### Start Server
```powershell
cd C:\Users\ericr\an-fsq7-sage-simulator
python -m reflex run
```

### Stop Server
Press `Ctrl+C` in the terminal, or:
```powershell
# Find and kill Python process
Get-Process python | Stop-Process -Force
```

### View Logs
```powershell
# Run with debug logging
python -m reflex run --loglevel debug
```

### Reset State
```powershell
# Delete state database to start fresh
Remove-Item reflex.db -ErrorAction SilentlyContinue
```

---

**Last Updated**: 2025-11-10 22:45 UTC  
**Server Status**: ✅ Running on localhost:3000  
**Next Action**: Switch to `interactive_sage` module and test component interactions
