"""
Professional WebGL Radar Scope Renderer

The visual heart of the SAGE simulator:
- Authentic phosphor green on black aesthetic
- Rotating radar sweep with fade
- Color-coded tracks (green=friendly, red=hostile, yellow=unknown)
- Fading trails showing flight paths
- Geographic overlays (coastlines, range rings)
- Smooth animations and glow effects

This creates the immersive Cold War radar experience.
"""

# WebGL/Canvas JavaScript code for radar rendering
# This will be injected into the Reflex page

RADAR_SCOPE_JAVASCRIPT = """
<script>
class RadarScope {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        // State
        this.tracks = [];
        this.overlays = {};
        this.geoData = null;
        this.sweepAngle = 0;
        this.brightness = 0.75;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
        this.zoom = 1.0;
        this.panX = 0;
        this.panY = 0;
        
        // Trail history (for fading paths)
        this.trailHistory = new Map();  // trackId -> array of {x, y, timestamp}
        this.maxTrailLength = 20;
        this.trailFadeMs = 5000;
        
        // Click handler for light gun
        this.onTrackClick = null;
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        
        // Start animation loop
        this.lastFrameTime = Date.now();
        requestAnimationFrame(() => this.render());
    }
    
    updateTracks(tracks) {
        this.tracks = tracks;
        
        // Update trail history
        const now = Date.now();
        tracks.forEach(track => {
            if (!this.trailHistory.has(track.id)) {
                this.trailHistory.set(track.id, []);
            }
            
            const trail = this.trailHistory.get(track.id);
            trail.push({
                x: track.x,
                y: track.y,
                timestamp: now
            });
            
            // Remove old trail points
            while (trail.length > this.maxTrailLength || 
                   (trail.length > 0 && now - trail[0].timestamp > this.trailFadeMs)) {
                trail.shift();
            }
        });
    }
    
    updateOverlays(overlays) {
        this.overlays = new Set(overlays);
    }
    
    updateGeoData(geoData) {
        this.geoData = geoData;
    }
    
    setBrightness(brightness) {
        this.brightness = Math.max(0.2, Math.min(1.0, brightness));
    }
    
    setPan(x, y) {
        this.panX = x;
        this.panY = y;
    }
    
    setZoom(zoom) {
        this.zoom = Math.max(0.5, Math.min(3.0, zoom));
    }
    
    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const clickX = (e.clientX - rect.left) / this.width;
        const clickY = (e.clientY - rect.top) / this.height;
        
        // Find nearest track within threshold
        let nearestTrack = null;
        let nearestDist = 0.05;  // 5% of screen
        
        this.tracks.forEach(track => {
            const dx = track.x - clickX;
            const dy = track.y - clickY;
            const dist = Math.sqrt(dx*dx + dy*dy);
            
            if (dist < nearestDist) {
                nearestDist = dist;
                nearestTrack = track;
            }
        });
        
        if (nearestTrack && this.onTrackClick) {
            this.onTrackClick(nearestTrack);
        }
    }
    
    render() {
        const now = Date.now();
        const dt = now - this.lastFrameTime;
        this.lastFrameTime = now;
        
        // Clear screen (black background)
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Update sweep angle (complete rotation every 4 seconds)
        this.sweepAngle = (this.sweepAngle + (dt / 4000) * Math.PI * 2) % (Math.PI * 2);
        
        // Apply transforms
        this.ctx.save();
        this.ctx.translate(this.centerX + this.panX, this.centerY + this.panY);
        this.ctx.scale(this.zoom, this.zoom);
        this.ctx.translate(-this.centerX, -this.centerY);
        
        // 1. Draw geographic overlays
        if (this.geoData) {
            this.drawGeographicOverlays();
        }
        
        // 2. Draw sweep
        this.drawSweep();
        
        // 3. Draw flight trails
        if (this.overlays.has('flight_paths')) {
            this.drawTrails();
        }
        
        // 4. Draw tracks
        this.drawTracks();
        
        // 5. Draw intercept vectors
        if (this.overlays.has('intercept_vectors')) {
            this.drawInterceptVectors();
        }
        
        this.ctx.restore();
        
        // Request next frame
        requestAnimationFrame(() => this.render());
    }
    
    drawSweep() {
        // Rotating sweep line with fade
        const gradient = this.ctx.createRadialGradient(
            this.centerX, this.centerY, 0,
            this.centerX, this.centerY, Math.min(this.width, this.height) / 2
        );
        gradient.addColorStop(0, `rgba(0, 255, 0, ${0.3 * this.brightness})`);
        gradient.addColorStop(0.5, `rgba(0, 255, 0, ${0.1 * this.brightness})`);
        gradient.addColorStop(1, 'rgba(0, 255, 0, 0)');
        
        this.ctx.save();
        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY);
        const sweepX = this.centerX + Math.cos(this.sweepAngle) * (this.width / 2);
        const sweepY = this.centerY + Math.sin(this.sweepAngle) * (this.height / 2);
        this.ctx.lineTo(sweepX, sweepY);
        this.ctx.stroke();
        this.ctx.restore();
    }
    
    drawTrails() {
        const now = Date.now();
        
        this.trailHistory.forEach((trail, trackId) => {
            if (trail.length < 2) return;
            
            const track = this.tracks.find(t => t.id === trackId);
            if (!track) return;
            
            // Determine trail color based on track type
            let baseColor = this.getTrackColor(track);
            
            this.ctx.save();
            this.ctx.strokeStyle = baseColor;
            this.ctx.lineWidth = 1;
            
            for (let i = 0; i < trail.length - 1; i++) {
                const age = now - trail[i].timestamp;
                const alpha = Math.max(0, 1 - (age / this.trailFadeMs)) * this.brightness * 0.5;
                
                this.ctx.globalAlpha = alpha;
                this.ctx.beginPath();
                this.ctx.moveTo(trail[i].x * this.width, trail[i].y * this.height);
                this.ctx.lineTo(trail[i+1].x * this.width, trail[i+1].y * this.height);
                this.ctx.stroke();
            }
            
            this.ctx.restore();
        });
    }
    
    drawTracks() {
        this.tracks.forEach(track => {
            const x = track.x * this.width;
            const y = track.y * this.height;
            const color = this.getTrackColor(track);
            const isSelected = track.selected || false;
            
            // Draw glow
            this.ctx.save();
            this.ctx.shadowColor = color;
            this.ctx.shadowBlur = isSelected ? 20 : 10;
            this.ctx.fillStyle = color;
            
            // Draw track dot
            this.ctx.globalAlpha = this.brightness;
            this.ctx.beginPath();
            this.ctx.arc(x, y, isSelected ? 8 : 5, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Draw selection ring
            if (isSelected) {
                this.ctx.strokeStyle = color;
                this.ctx.lineWidth = 2;
                this.ctx.globalAlpha = this.brightness * 0.8;
                this.ctx.beginPath();
                this.ctx.arc(x, y, 15, 0, Math.PI * 2);
                this.ctx.stroke();
            }
            
            // Draw callsign/label
            if (this.overlays.has('callsigns')) {
                this.ctx.font = '10px Courier New';
                this.ctx.fillStyle = color;
                this.ctx.globalAlpha = this.brightness * 0.8;
                this.ctx.fillText(track.id, x + 10, y - 5);
            }
            
            this.ctx.restore();
        });
    }
    
    drawInterceptVectors() {
        // Draw lines from interceptors to their targets
        this.tracks.forEach(track => {
            if (track.track_type === 'interceptor' && track.target_id) {
                const target = this.tracks.find(t => t.id === track.target_id);
                if (!target) return;
                
                const x1 = track.x * this.width;
                const y1 = track.y * this.height;
                const x2 = target.x * this.width;
                const y2 = target.y * this.height;
                
                this.ctx.save();
                this.ctx.strokeStyle = '#0088ff';
                this.ctx.lineWidth = 1;
                this.ctx.setLineDash([5, 5]);
                this.ctx.globalAlpha = this.brightness * 0.6;
                this.ctx.beginPath();
                this.ctx.moveTo(x1, y1);
                this.ctx.lineTo(x2, y2);
                this.ctx.stroke();
                this.ctx.restore();
            }
        });
    }
    
    drawGeographicOverlays() {
        if (!this.geoData) return;
        
        const baseAlpha = this.brightness * 0.3;
        
        // Draw coastlines
        if (this.overlays.has('coastlines') && this.geoData.coastlines) {
            this.ctx.save();
            this.ctx.strokeStyle = `rgba(0, 255, 0, ${baseAlpha})`;
            this.ctx.lineWidth = 1.5;
            
            this.geoData.coastlines.forEach(coastline => {
                if (coastline.style === 'dashed') {
                    this.ctx.setLineDash([5, 5]);
                } else if (coastline.style === 'dotted') {
                    this.ctx.setLineDash([2, 3]);
                } else {
                    this.ctx.setLineDash([]);
                }
                
                this.ctx.beginPath();
                coastline.points.forEach((point, i) => {
                    const x = point[0] * this.width;
                    const y = point[1] * this.height;
                    if (i === 0) {
                        this.ctx.moveTo(x, y);
                    } else {
                        this.ctx.lineTo(x, y);
                    }
                });
                this.ctx.stroke();
            });
            
            this.ctx.setLineDash([]);
            this.ctx.restore();
        }
        
        // Draw range rings
        if (this.overlays.has('range_rings') && this.geoData.range_rings) {
            this.ctx.save();
            this.ctx.strokeStyle = `rgba(0, 255, 0, ${baseAlpha * 0.6})`;
            this.ctx.lineWidth = 1;
            this.ctx.font = '12px Courier New';
            this.ctx.fillStyle = `rgba(0, 255, 0, ${baseAlpha})`;
            
            this.geoData.range_rings.forEach(ring => {
                this.ctx.beginPath();
                this.ctx.arc(
                    this.centerX,
                    this.centerY,
                    ring.radius * Math.min(this.width, this.height),
                    0,
                    Math.PI * 2
                );
                this.ctx.stroke();
                
                // Label
                this.ctx.fillText(
                    ring.label,
                    this.centerX + ring.radius * this.width + 5,
                    this.centerY
                );
            });
            
            this.ctx.restore();
        }
        
        // Draw bearing markers (N/E/S/W)
        if (this.geoData.bearing_markers) {
            this.ctx.save();
            this.ctx.fillStyle = `rgba(0, 255, 0, ${baseAlpha})`;
            this.ctx.font = 'bold 14px Courier New';
            
            this.geoData.bearing_markers.forEach(marker => {
                this.ctx.fillText(
                    marker.label,
                    marker.x * this.width - 7,
                    marker.y * this.height + 5
                );
            });
            
            this.ctx.restore();
        }
        
        // Draw city labels
        if (this.overlays.has('callsigns') && this.geoData.cities) {
            this.ctx.save();
            this.ctx.fillStyle = `rgba(0, 255, 0, ${baseAlpha})`;
            this.ctx.font = '10px Courier New';
            
            this.geoData.cities.forEach(city => {
                const x = city.x * this.width;
                const y = city.y * this.height;
                
                // City dot
                this.ctx.beginPath();
                this.ctx.arc(x, y, 2, 0, Math.PI * 2);
                this.ctx.fill();
                
                // Label
                this.ctx.fillText(city.label, x + 5, y - 5);
            });
            
            this.ctx.restore();
        }
    }
    
    getTrackColor(track) {
        switch(track.track_type) {
            case 'hostile': return '#ff0000';  // Red
            case 'missile': return '#ff00ff';  // Magenta
            case 'friendly': return '#00ff00'; // Green
            case 'interceptor': return '#0088ff'; // Blue
            case 'unknown': return '#ffff00';  // Yellow
            default: return '#888888';         // Gray
        }
    }
}

// Initialize radar scope
let radarScope = null;

function initRadarScope(canvasId) {
    radarScope = new RadarScope(canvasId);
    console.log('Radar scope initialized');
    return radarScope;
}

// Export for use from Python/Reflex
window.radarScope = null;
window.initRadarScope = initRadarScope;

</script>
"""


# Reflex component wrapper for the radar scope
RADAR_SCOPE_HTML = """
<div style="position: relative; width: 100%; height: 100%;">
    <canvas 
        id="radar-scope-canvas" 
        width="800" 
        height="800"
        style="width: 100%; height: 100%; background: #000000; border-radius: 8px;"
    ></canvas>
</div>
"""


# Python helper functions to bridge Reflex state to JavaScript

def create_radar_scope_component() -> str:
    """
    Creates the complete HTML/JS for the radar scope
    To be used in Reflex: rx.html(create_radar_scope_component())
    """
    return f"""
    {RADAR_SCOPE_JAVASCRIPT}
    {RADAR_SCOPE_HTML}
    <script>
        // Initialize on load
        window.addEventListener('load', function() {{
            setTimeout(() => {{
                window.radarScope = initRadarScope('radar-scope-canvas');
            }}, 100);
        }});
    </script>
    """


def radar_update_script(tracks_json: str, overlays_json: str, geo_json: str) -> str:
    """
    Generates JavaScript to update the radar scope with new data
    Call this from Reflex backend when state changes
    """
    return f"""
    <script>
        if (window.radarScope) {{
            window.radarScope.updateTracks({tracks_json});
            window.radarScope.updateOverlays({overlays_json});
            window.radarScope.updateGeoData({geo_json});
        }}
    </script>
    """


# CSS for radar scope container
RADAR_SCOPE_CSS = """
<style>
#radar-scope-canvas {
    image-rendering: crisp-edges;
    image-rendering: -moz-crisp-edges;
    image-rendering: -webkit-crisp-edges;
    cursor: crosshair;
}

#radar-scope-canvas:hover {
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

/* Crosshair cursor when light gun armed */
.lightgun-armed #radar-scope-canvas {
    cursor: crosshair;
}

/* Animation for track selection pulse */
@keyframes pulse-ring {
    0% { r: 8; opacity: 1; }
    100% { r: 20; opacity: 0; }
}
</style>
"""
