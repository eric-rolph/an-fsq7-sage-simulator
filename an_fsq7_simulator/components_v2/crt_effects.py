"""
Authentic CRT Display Effects for SAGE Radar

Inspired by the masswerk.at PDP-1 Type 30 CRT emulation:
- P7 phosphor glow (blue short activation + green long persistence)
- Screen curvature
- Scanline effects
- Vignette/screen border darkening
- Phosphor persistence trails
"""

CRT_DISPLAY_CSS = """
<style>
/* CRT Display Container - simulates physical radar scope */
.crt-display-container {
    position: relative;
    display: inline-block;
    background: #000;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 
        inset 0 0 50px rgba(0,255,100,0.1),
        0 0 100px rgba(0,0,0,0.9);
}

/* CRT Bezel - simulates the physical screen frame */
.crt-bezel {
    position: relative;
    background: radial-gradient(ellipse at center, #000 0%, #111 70%, #000 100%);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 
        inset 0 0 30px rgba(0,255,100,0.15),
        inset 0 0 60px rgba(0,255,100,0.05);
}

/* Canvas wrapper with CRT effects */
.crt-screen {
    position: relative;
    overflow: hidden;
    border-radius: 5px;
}

/* The actual radar canvas */
.crt-screen canvas {
    display: block;
    background: #000;
    /* Phosphor glow effect */
    filter: 
        blur(0.3px)
        brightness(1.1)
        contrast(1.2);
}

/* Scanline overlay - creates horizontal lines like a real CRT */
.crt-screen::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        rgba(0, 0, 0, 0.15),
        rgba(0, 0, 0, 0.15) 1px,
        transparent 1px,
        transparent 2px
    );
    z-index: 10;
}

/* Screen curvature and vignette effect */
.crt-screen::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    background: radial-gradient(
        ellipse at center,
        transparent 0%,
        transparent 60%,
        rgba(0, 0, 0, 0.3) 85%,
        rgba(0, 0, 0, 0.7) 100%
    );
    border-radius: 5px;
    z-index: 11;
}

/* Phosphor glow animation for active elements */
@keyframes phosphorGlow {
    0%, 100% { 
        filter: 
            drop-shadow(0 0 2px rgba(0, 255, 100, 0.8))
            drop-shadow(0 0 5px rgba(0, 255, 100, 0.5))
            drop-shadow(0 0 10px rgba(0, 255, 100, 0.3));
    }
    50% { 
        filter: 
            drop-shadow(0 0 3px rgba(0, 255, 100, 0.9))
            drop-shadow(0 0 7px rgba(0, 255, 100, 0.6))
            drop-shadow(0 0 15px rgba(0, 255, 100, 0.4));
    }
}

/* Flicker effect for ultra-realism (optional, subtle) */
@keyframes crtFlicker {
    0% { opacity: 1.0; }
    2% { opacity: 0.98; }
    4% { opacity: 1.0; }
    19% { opacity: 0.99; }
    21% { opacity: 1.0; }
    80% { opacity: 0.98; }
    83% { opacity: 1.0; }
}

.crt-screen.flickering canvas {
    animation: crtFlicker 4s infinite;
}
</style>
"""

def load_crt_script():
    """Load external CRT radar script using Reflex script component"""
    import reflex as rx
    return rx.script(src="/crt_radar.js")

def get_crt_radar_html():
    """
    Returns HTML for CRT-wrapped radar display
    Inspired by masswerk.at's PDP-1 Type 30 CRT emulation
    """
    return """
    <div class="crt-display-container">
        <div class="crt-bezel">
            <div class="crt-screen">
                <canvas id="radar-scope-canvas" width="800" height="800"></canvas>
            </div>
        </div>
    </div>
    """

# Legacy inline code removed - now using external JS file
# All CRT logic is in assets/crt_radar.js, loaded via script_loader pattern
