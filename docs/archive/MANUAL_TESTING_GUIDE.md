# Manual Testing Guide for SD Console

## Issue: Windows Hot-Reload Problem
The Reflex development server has a known issue on Windows where it automatically stops after 10-15 seconds due to the React Router dev server receiving shutdown signals from the Windows file watcher.

**Root Cause**: Exit code `3221225786` (0xC000013A - STATUS_CONTROL_C_EXIT) indicates the frontend process is receiving Control-C signals.

**Workarounds**:
1. **Use WSL** (Recommended): Run `wsl` then `python -m reflex run` for stable server
2. **Manual Quick Testing**: Start server, test features within the 10-15 second window
3. **Use keep_alive.py**: Run `python keep_alive.py` to auto-restart server when it crashes

## Manual Testing Procedure

### Starting the Server
```powershell
python -m reflex run
```
- Server will start at http://localhost:3000
- **Act quickly** - you have ~10 seconds before auto-shutdown
- Or use WSL for stable server

### Test Checklist

#### 1. Category Filters (13 buttons)
Located in left panel under "CATEGORY SELECT":
- [ ] S1 ALL
- [ ] S2 FRIENDLY  
- [ ] S3 UNKNOWN
- [ ] S4 HOSTILE
- [ ] S5 INTERCEPTOR
- [ ] S6 BOMBER
- [ ] S7 ECM
- [ ] S8 MISSILE
- [ ] S9 HIGH ALT
- [ ] S10 MED ALT
- [ ] S11 LOW ALT
- [ ] S12 FAST
- [ ] S13 SLOW

**Expected Behavior**:
- Clicking toggles button highlight (green when active)
- State updates: `active_filters` set
- No console errors

#### 2. Feature Overlays (5 buttons)
Located under "FEATURE SELECT":
- [ ] S20 GRID
- [ ] S21 RANGE RINGS
- [ ] S22 LABELS
- [ ] S23 VECTORS
- [ ] S24 IFF ZONES

**Expected Behavior**:
- Clicking toggles button highlight
- State updates: `active_overlays` set
- No console errors

#### 3. Off-Centering Controls (11 buttons)
Located under "OFF CENTERING":

**Pan Controls (5)**:
- [ ] UP
- [ ] DOWN
- [ ] LEFT
- [ ] RIGHT
- [ ] CENTER

**Zoom Controls (3)**:
- [ ] IN
- [ ] OUT
- [ ] FIT

**Rotate Controls (3)**:
- [ ] CCW (Counter-clockwise)
- [ ] RESET
- [ ] CW (Clockwise)

**Expected Behavior**:
- Clicking calls appropriate State method
- Visual feedback on radar scope (if visible)
- No console errors

#### 4. Brightness Control
Located under "BRIGHT/DIM":
- [ ] Slider (0-100%)
- [ ] DIM preset button
- [ ] MED preset button
- [ ] BRIGHT preset button

**Expected Behavior**:
- Slider changes brightness value (0.0-1.0)
- Preset buttons set specific values (0.3, 0.6, 1.0)
- State updates: `brightness` value
- No console errors

#### 5. Light Gun System
Located in right panel:
- [ ] ARM button (enable light gun)
- [ ] Crosshair appears when armed
- [ ] Click on target track
- [ ] Track detail panel populates with:
  - Track ID
  - Position (x, y, altitude)
  - Speed
  - Heading
  - Threat level badge
  - IFF status

**Expected Behavior**:
- ARM button toggles `lightgun_armed` state
- Clicking track updates `selected_track_id`
- Detail panel shows track information
- No console errors

### Checking for Errors

#### Browser Console
1. Open DevTools (F12)
2. Go to Console tab
3. Look for:
   - ❌ Red errors (TypeErrors, ReferenceErrors)
   - ⚠️ Yellow warnings (acceptable)
   - ✅ Green success messages

#### Python Backend
Watch terminal output for:
```
TypeError: unhashable type: 'dict'
AttributeError: ...
ValueError: ...
```

### Known Issues (Fixed)
- ✅ **Event Handler Runtime Errors** (Fixed in commit 0979401)
  - Was: TypeError when clicking buttons
  - Fix: Changed to State class direct reference pattern
  - All callbacks now work correctly

### Test Results Template
```markdown
## Test Session: [Date]

### Environment
- OS: Windows 10/11
- Python: 3.13
- Reflex: 0.8.19
- Browser: Chrome/Edge/Firefox

### Category Filters
- S1-S13: [✓/✗] [Notes]

### Feature Overlays
- S20-S24: [✓/✗] [Notes]

### Off-Centering Controls
- Pan: [✓/✗] [Notes]
- Zoom: [✓/✗] [Notes]
- Rotate: [✓/✗] [Notes]

### Brightness
- Slider: [✓/✗] [Notes]
- Presets: [✓/✗] [Notes]

### Light Gun
- ARM: [✓/✗] [Notes]
- Target Select: [✓/✗] [Notes]
- Detail Panel: [✓/✗] [Notes]

### Errors Encountered
[List any errors with screenshots/stack traces]

### Overall Status
[PASS/FAIL with summary]
```

## Alternative: WSL Testing
For stable server:
```bash
# In WSL terminal
cd /mnt/c/Users/ericr/an-fsq7-sage-simulator
python -m reflex run
```

Server will remain stable for Playwright automated testing.

## Playwright Testing (When Server Stable)
Once server is running stably (via WSL or fix):
```powershell
# Navigate to app
mcp_playwright_browser_navigate http://localhost:3000

# Take snapshot
mcp_playwright_browser_snapshot

# Click buttons using ref from snapshot
mcp_playwright_browser_click --element "S1 ALL" --ref "..."

# Verify state changes
# Check for errors
```
