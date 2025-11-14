# Radar Scope Testing Instructions

## Quick Test

1. **Open the application**: http://localhost:3000/

2. **Open Browser Developer Console** (F12 or Right-click → Inspect → Console tab)

3. **Look for these console messages** (in order):
   ```
   [SAGE] Loading radar_scope.js via createElement
   [SAGE] radar_scope.js loaded, setting up initialization
   RadarScope initialized: radar-scope-canvas
   [SAGE] Radar scope initialized manually
   [SAGE] Geographic data loaded
   [SAGE] Initial tracks: X
   ```

4. **Verify radar display**:
   - Canvas should show a **phosphor green background**
   - You should see a **rotating sweep line**
   - **Range rings** should be visible (concentric circles)
   - **Coastlines** should appear (if "Coastlines" overlay enabled)
   - **Cities** should show as markers (if "Cities" overlay enabled)
   - **Tracks** should appear as colored dots with trails

5. **Check in console**:
   ```javascript
   window.radarScope  // Should NOT be undefined
   window.RadarScope  // Should be a class definition
   ```

## What Was Fixed

The radar wasn't displaying because React's security model blocks inline `<script>` execution via `innerHTML`. 

**Solution**: Used `document.createElement('script')` to dynamically load `/radar_scope.js`, which bypasses React's security restrictions. All initialization logic is now in the `script.onload` callback.

## Troubleshooting

### If you see NO console messages:
- The initial `<script>` tag itself isn't executing
- This means React is still blocking it
- Try hard refresh: Ctrl+Shift+R

### If you see "Loading radar_scope.js" but nothing else:
- The external file isn't loading from `/radar_scope.js`
- Check Network tab (F12 → Network) for radar_scope.js - should be 200 OK
- Verify file exists: `assets/radar_scope.js`

### If you see messages but no display:
- Check if canvas element exists: `document.getElementById('radar-scope-canvas')`
- Check for JavaScript errors in console (red text)
- Verify `window.radarScope` is defined

### If tracks don't appear:
- Check: `document.getElementById('sage-track-data')`
- Check: `document.getElementById('sage-track-data').dataset.tracks`
- Verify simulation is running (time counter should be updating)

## Current Status

✅ Server running: http://localhost:3000/
✅ External script: `/radar_scope.js` exists in assets/
✅ Dynamic loading: Uses `document.createElement()` approach
✅ Initialization: Consolidated in script.onload callback
✅ Track updates: 1-second interval timer

The radar should now be fully functional!
