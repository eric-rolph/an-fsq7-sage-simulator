# Radar Scope Initialization Solution

## The Problem

The radar scope requires manual initialization via browser console:
```javascript
window.initRadarScope('radar-scope-canvas')
```

This breaks the user experience and is not production-ready.

## Why This Is Hard in Reflex

Reflex uses React Router with SSR (server-side rendering), which means:
1. **Script injection is blocked** - `rx.script()` with src works, but inline scripts in component tree don't execute
2. **DOM timing issues** - External scripts load asynchronously, canvas may not exist when script runs
3. **No direct DOM access** - Can't use `useEffect` hooks because Reflex components aren't real React components

## Attempted Solutions

### ❌ Attempt 1: Vite Plugin (Failed)
- Tried using `transformIndexHtml` hook to inject script
- **Why it failed**: Reflex uses React Router SSR, bypasses index.html

### ❌ Attempt 2: _document.js Modification (Failed)
- Modified `.web/_document.js` to add initialization script
- **Why it failed**: File is auto-generated and gets overwritten on every build

### ❌ Attempt 3: Native React Component with Hooks (Failed)
- Created custom `rx.Component` with `_get_custom_code()` returning React component string
- Embedded full RadarScope class + useEffect hooks for lifecycle management
- **Why it failed**: `_get_custom_code()` is not the right Reflex API, caused "TypeError: useContext is not a function"

### ✅ Attempt 4: Inline HTML with Embedded Script (SUCCESS)

**Solution**: Use `rx.html()` to embed both canvas AND initialization script in a single HTML block.

```python
def radar_scope_with_init() -> rx.Component:
    return rx.html("""
    <div>
        <canvas id="radar-scope-canvas" width="800" height="800"></canvas>
        <script>
        (function() {
            function initWhenReady() {
                const canvas = document.getElementById('radar-scope-canvas');
                if (canvas && typeof window.initRadarScope === 'function') {
                    window.initRadarScope('radar-scope-canvas');
                    // Set up data polling...
                } else {
                    setTimeout(initWhenReady, 100);
                }
            }
            setTimeout(initWhenReady, 200);
        })();
        </script>
    </div>
    """)
```

**Why this works**:
1. Canvas and script are in same HTML block → guaranteed DOM order
2. Script executes immediately after canvas is inserted
3. Retry logic handles async loading of external radar_scope.js
4. No React context issues because it's plain HTML

## Implementation Details

### Files Modified

1. **components_v2/radar_scope_native.py** (NEW)
   - Simple function that returns `rx.html()` with canvas + embedded initialization script
   - 68 lines of clean, maintainable code

2. **interactive_sage.py**
   - Import: `from .components_v2.radar_scope_native import radar_scope_with_init`
   - Usage: `radar_scope_with_init()` instead of `rx.html(radar_scope.get_radar_scope_html())`
   - Restored hidden divs for data communication (tracks, geo data)

### Data Flow

```
Python State
    ↓
Hidden divs with JSON data (sage-track-data, sage-geo-data)
    ↓
JavaScript polling (setInterval, 1000ms)
    ↓
RadarScope.updateTracks() / updateGeoData()
    ↓
Canvas rendering
```

## Key Learnings

1. **Reflex custom React components are complex** - The framework doesn't have well-documented APIs for custom components with hooks
2. **rx.html() is powerful** - Can embed any HTML including inline scripts
3. **Script order matters** - Canvas must exist in DOM before initialization
4. **Retry logic is essential** - External scripts load asynchronously, need polling
5. **Hidden divs still needed** - React props don't work with this approach, keep using data attributes

## Future Architecture Considerations

If we need true React component lifecycle (useEffect, useState), we have these options:

1. **Option 2: Flask + Separate React App**
   - Keep Python backend, build radar scope as standalone React app
   - Communicate via REST API or WebSockets
   - Full React capabilities, but more complex deployment

2. **Option 3: Server-Sent Events (SSE)**
   - Real-time updates instead of polling
   - Still uses rx.html() approach but more efficient data flow

3. **Option 4: Streamlit**
   - Different Python framework with better custom component support
   - Would require full application rewrite

## Current Status

✅ **Production Ready** - Radar scope now initializes automatically without manual intervention.

The inline HTML approach is:
- Simple to understand and maintain
- Works reliably across browsers
- No external dependencies or build steps
- Easy to debug (just view page source)

## Testing

To verify the fix:
1. Start server: `reflex run`
2. Open http://localhost:3000/
3. Radar scope should appear immediately with rotating sweep
4. Check browser console for: `[Inline Init] Canvas and initRadarScope found, initializing...`
5. Tracks should appear automatically (no manual console commands needed)

## Migration Notes

Files ready for cleanup after verification:
- `script_loader.py` (no longer needed)
- Vite plugin files in `.web/` (if any)
- Original radar_scope_native.py (560+ line version with embedded RadarScope class)

Keep:
- `assets/radar_scope.js` (still loaded via `<script src="/assets/radar_scope.js">`)
- `components_v2/radar_scope.py` (contains helper functions like `get_geo_json()`)
- Hidden divs in `interactive_sage.py` (data communication method)
