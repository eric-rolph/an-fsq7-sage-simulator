// Enhanced CRT rendering with P7 phosphor simulation
class CRTRadarScope {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error('[CRT] Canvas not found:', canvasId);
            return;
        }
        
        this.ctx = this.canvas.getContext('2d', { alpha: false });
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        // P7 Phosphor colors (inspired by real CRT phosphor)
        // P7 has two components: fast blue decay + slow green persistence
        this.phosphorFast = 'rgba(100, 150, 255, 0.9)';  // Blue, fast decay
        this.phosphorSlow = 'rgba(0, 255, 100, 0.8)';    // Green, slow persistence
        this.phosphorPersistence = 'rgba(0, 255, 100, 0.3)'; // Fading trail
        
        // Persistence layer for phosphor trails
        this.persistenceCanvas = document.createElement('canvas');
        this.persistenceCanvas.width = this.width;
        this.persistenceCanvas.height = this.height;
        this.persistenceCtx = this.persistenceCanvas.getContext('2d', { alpha: true });
        
        // Radar state
        this.tracks = [];
        this.overlays = new Set(['range_rings', 'coastlines']);
        this.geoData = null;
        this.sweepAngle = 0;
        this.brightness = 0.75;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
        
        // Phosphor persistence decay alpha (how much to fade each frame)
        // P7 phosphor has ~1-2 second visible persistence
        // At 60fps, need ~0.01-0.015 for proper decay rate
        this.persistenceDecay = 0.012;  // Gives ~1.5 second trails
        
        // Animation
        this.lastFrameTime = Date.now();
        this.sweepSpeed = 6.0; // degrees per second
        
        console.log('[CRT] Initialized with P7 phosphor simulation');
        console.log('[CRT] Persistence decay:', this.persistenceDecay);
        console.log('[CRT] Overlays:', Array.from(this.overlays));
        
        this.animationId = null;
        this.stopped = false;
        this.animationId = requestAnimationFrame(() => this.render());
    }
    
    stop() {
        console.log('[CRT] Stopping radar scope animation');
        this.stopped = true;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }
    
    render() {
        // Check if stopped or canvas invalid
        if (this.stopped || !this.canvas || !this.canvas.isConnected || !this.ctx) {
            if (!this.stopped) {
                console.warn('[CRT] Canvas disconnected from DOM, stopping render loop');
            }
            return;
        }
        
        const now = Date.now();
        const dt = (now - this.lastFrameTime) / 1000;
        this.lastFrameTime = now;
        
        // Update sweep angle
        this.sweepAngle = (this.sweepAngle + this.sweepSpeed * dt) % 360;
        
        // Apply phosphor persistence decay to fade old content
        this.persistenceCtx.globalCompositeOperation = 'source-over';
        this.persistenceCtx.fillStyle = `rgba(0, 0, 0, ${this.persistenceDecay})`;
        this.persistenceCtx.fillRect(0, 0, this.width, this.height);
        
        // Add sweep trail to persistence layer
        this.addSweepToPersistence();
        
        // Draw tracks to persistence layer
        this.drawTracksOnPersistence();
        
        // Now composite everything to main display canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw persistence layer (faded trails)
        this.ctx.drawImage(this.persistenceCanvas, 0, 0);
        
        // Draw range rings DIRECTLY on main canvas (static overlay, no persistence)
        if (this.overlays.has('range_rings')) {
            this.drawRangeRings();
        }
        
        // Draw bright sweep leading edge on top
        this.drawSweepBright();
        
        // Draw bright track markers on top
        this.drawTracksBright();
        
        this.animationId = requestAnimationFrame(() => this.render());
    }
    
    drawRangeRings() {
        const rings = [50, 100, 150, 200, 250, 300, 350];
        
        // Draw DIRECTLY to main canvas (static overlay, always visible)
        this.ctx.strokeStyle = 'rgba(0, 255, 100, 0.8)';  // BRIGHT green for visibility
        this.ctx.lineWidth = 2;  // Thicker for debugging
        
        rings.forEach(radius => {
            this.ctx.beginPath();
            this.ctx.arc(this.centerX, this.centerY, radius, 0, Math.PI * 2);
            this.ctx.stroke();
        });
        
        // Debug: Draw a bright test marker at center
        this.ctx.fillStyle = 'rgba(255, 0, 0, 1.0)';  // RED dot at center
        this.ctx.fillRect(this.centerX - 5, this.centerY - 5, 10, 10);
    }
    
    addSweepToPersistence() {
        // Add sweep trail to persistence layer (will fade over time)
        const sweepLength = 350;
        const angleRad = (this.sweepAngle * Math.PI) / 180;
        
        this.persistenceCtx.save();
        this.persistenceCtx.translate(this.centerX, this.centerY);
        this.persistenceCtx.rotate(angleRad);
        this.persistenceCtx.strokeStyle = this.phosphorPersistence;
        this.persistenceCtx.lineWidth = 2;
        this.persistenceCtx.beginPath();
        this.persistenceCtx.moveTo(0, 0);
        this.persistenceCtx.lineTo(sweepLength, 0);
        this.persistenceCtx.stroke();
        this.persistenceCtx.restore();
    }
    
    drawSweepBright() {
        // Draw bright leading edge of sweep (doesn't persist)
        const sweepLength = 350;
        const angleRad = (this.sweepAngle * Math.PI) / 180;
        
        // Create radial gradient for sweep
        const gradient = this.ctx.createRadialGradient(
            this.centerX, this.centerY, 0,
            this.centerX, this.centerY, sweepLength
        );
        gradient.addColorStop(0, this.phosphorFast);
        gradient.addColorStop(0.7, this.phosphorSlow);
        gradient.addColorStop(1, 'rgba(0, 255, 100, 0)');
        
        this.ctx.save();
        this.ctx.translate(this.centerX, this.centerY);
        this.ctx.rotate(angleRad);
        
        // Draw bright sweep line with glow
        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = 3;
        this.ctx.shadowBlur = 20;
        this.ctx.shadowColor = this.phosphorSlow;
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(sweepLength, 0);
        this.ctx.stroke();
        
        this.ctx.restore();
    }
    
    drawTracksOnPersistence() {
        // Draw tracks to persistence layer (will fade over time)
        if (!this.tracks || !Array.isArray(this.tracks)) {
            return;
        }
        this.tracks.forEach(track => {
            const x = this.centerX + track.x;
            const y = this.centerY + track.y;
            
            // Add to persistence layer
            this.persistenceCtx.fillStyle = this.phosphorSlow;
            this.persistenceCtx.beginPath();
            this.persistenceCtx.arc(x, y, 4, 0, Math.PI * 2);
            this.persistenceCtx.fill();
        });
    }
    
    drawTracksBright() {
        // Draw bright track markers on top (doesn't persist)
        if (!this.tracks || !Array.isArray(this.tracks)) {
            return;
        }
        this.tracks.forEach(track => {
            const x = this.centerX + track.x;
            const y = this.centerY + track.y;
            
            // Draw bright spot with glow
            this.ctx.fillStyle = this.phosphorFast;
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = this.phosphorSlow;
            this.ctx.beginPath();
            this.ctx.arc(x, y, 3, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        });
    }
    
    updateTracks(tracks) {
        this.tracks = tracks || [];
    }
    
    updateOverlays(overlays) {
        this.overlays = new Set(overlays || []);
    }
    
    updateGeoData(geoData) {
        this.geoData = geoData;
    }
}

// Expose to window
window.CRTRadarScope = CRTRadarScope;

// Auto-initialization with canvas replacement detection
function initCRTWhenReady() {
    const canvas = document.getElementById('radar-scope-canvas');
    
    // Check if canvas exists and if it's a NEW canvas element (different from stored one)
    if (canvas) {
        const isNewCanvas = !window.crtRadarScope || window.crtRadarScope.canvas !== canvas;
        
        if (isNewCanvas) {
            console.log('[CRT] Canvas ' + (window.crtRadarScope ? 'REPLACED' : 'found') + ', (re)initializing P7 phosphor radar scope...');
            
            // Stop old instance if it exists
            if (window.crtRadarScope && window.crtRadarScope.stop) {
                window.crtRadarScope.stop();
            }
            
            window.crtRadarScope = new CRTRadarScope('radar-scope-canvas');
            console.log('[CRT] ✓ Radar scope initialized with P7 phosphor');
        }
        
        return true;
    }
    
    return false;
}

// Data update loop (separate from initialization)
setInterval(function() {
    if (window.crtRadarScope) {
        var trackDiv = document.getElementById('sage-track-data');
        var geoDiv = document.getElementById('sage-geo-data');
        
        if (trackDiv && trackDiv.dataset.tracks) {
            try {
                var tracks = JSON.parse(trackDiv.dataset.tracks);
                window.crtRadarScope.updateTracks(tracks);
            } catch(e) {
                console.error('[CRT] Error parsing tracks:', e);
            }
        }
        
        if (geoDiv && geoDiv.dataset.geo) {
            try {
                var geo = JSON.parse(geoDiv.dataset.geo);
                window.crtRadarScope.updateGeoData(geo);
            } catch(e) {
                console.error('[CRT] Error parsing geo data:', e);
            }
        }
    }
}, 1000);

// Continuous polling to detect canvas replacement by React
var pollInterval = setInterval(function() {
    initCRTWhenReady();
}, 100);

console.log('[CRT] Auto-initialization started with continuous canvas monitoring');
