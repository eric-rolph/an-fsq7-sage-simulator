"""
Radar scope component - simple wrapper.
JavaScript is injected at the app level in interactive_sage.py.
Now using CRT P7 phosphor system (crt_radar.js) exclusively.
"""

import reflex as rx


def radar_scope_with_init() -> rx.Component:
    """
    Return the radar scope canvas.
    CRT radar initialization happens via /crt_radar.js script.
    This just provides the canvas element without competing JavaScript.
    """
    # Plain canvas for CRT radar - no competing JavaScript
    return rx.html("""
<div style="position: relative; width: 100%; height: 100%;">
    <canvas 
        id="radar-scope-canvas" 
        width="800" 
        height="800"
        style="width: 100%; height: 100%; background: #000000; border-radius: 8px;"
    ></canvas>
</div>
""")
