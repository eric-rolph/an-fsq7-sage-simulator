"""
Dynamic Script Loader Component
Properly loads external JavaScript files in Reflex by creating script elements dynamically
"""

import reflex as rx  # type: ignore
from typing import Optional


def load_external_script(src: str, on_load_callback: Optional[str] = None) -> rx.Component:
    """
    Load an external JavaScript file and optionally call a function when it loads.
    
    Args:
        src: URL of the script to load (e.g., "/radar_scope.js")
        on_load_callback: JavaScript code to execute after script loads
    
    Returns:
        Reflex component that dynamically loads the script
    """
    callback_code = f"""
        script.onload = function() {{
            console.log('[Script Loader] Loaded:', script.src);
            {on_load_callback if on_load_callback else ''}
        }};
    """ if on_load_callback else ""
    
    return rx.html(f'''<script>
(function loadScript() {{
    var script = document.createElement('script');
    script.src = '{src}';
    script.type = 'text/javascript';
    {callback_code}
    script.onerror = function() {{
        console.error('[Script Loader] Failed to load:', script.src);
    }};
    document.head.appendChild(script);
}})();
</script>''')


# Specialized loader for radar scope
def load_radar_scope() -> rx.Component:
    """
    Load radar_scope.js and auto-initialize when ready.
    Includes track data binding and proper event handling.
    """
    return rx.html('''<script>
(function loadAndInitRadar() {
    console.log('[SAGE] Starting radar scope loader...');
    
    // Step 1: Load radar_scope.js dynamically
    var script = document.createElement('script');
    script.src = '/radar_scope.js';
    script.type = 'text/javascript';
    
    script.onload = function() {
        console.log('[SAGE] radar_scope.js loaded successfully');
        
        // Step 2: Poll for canvas existence (React might not have rendered it yet)
        var attempts = 0;
        var maxAttempts = 50; // 5 seconds max
        
        function initWhenCanvasReady() {
            attempts++;
            var canvas = document.getElementById('radar-scope-canvas');
            
            if (canvas && typeof window.initRadarScope !== 'undefined') {
                console.log('[SAGE] Canvas found, initializing radar scope...');
                window.initRadarScope('radar-scope-canvas');
                
                // Step 3: Load tracks from embedded data attribute
                setTimeout(function() {
                    if (window.radarScope) {
                        var trackDataDiv = document.getElementById('sage-track-data');
                        if (trackDataDiv && trackDataDiv.dataset.tracks) {
                            var tracks = JSON.parse(trackDataDiv.dataset.tracks);
                            console.log('[SAGE] Loading', tracks.length, 'tracks from state');
                            window.radarScope.updateTracks(tracks);
                        }
                    }
                }, 100);
                
            } else if (attempts < maxAttempts) {
                setTimeout(initWhenCanvasReady, 100);
            } else {
                console.error('[SAGE] Timeout waiting for canvas or initRadarScope function');
            }
        }
        
        // Start polling after a short delay to let React render
        setTimeout(initWhenCanvasReady, 500);
    };
    
    script.onerror = function() {
        console.error('[SAGE] Failed to load radar_scope.js');
    };
    
    document.head.appendChild(script);
})();
</script>''')
