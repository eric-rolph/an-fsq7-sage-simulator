// Execute SAGE data scripts on page load (Reflex rx.html() doesn't auto-execute script innerHTML)
(function() {
    // Wait for DOM to be ready
    function executeSAGEScripts() {
        var scripts = Array.from(document.querySelectorAll('script'));
        var executed = 0;
        scripts.forEach(function(s) {
            var text = s.innerHTML || '';
            if (text.includes('__SAGE_')) {
                try {
                    eval(text);
                    executed++;
                } catch(e) {
                    console.error('[SAGE] Error executing data script:', e);
                }
            }
        });
        if (executed > 0) {
            console.log('[SAGE] Executed ' + executed + ' data injection scripts');
        }
    }
    
    // Execute immediately if DOM ready, otherwise wait
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', executeSAGEScripts);
    } else {
        executeSAGEScripts();
    }
})();

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
        this.interceptors = [];
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
        
        // Light gun click handler
        this.onTrackClick = null;
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        
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
    
    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const clickX = (e.clientX - rect.left) / rect.width;
        const clickY = (e.clientY - rect.top) / rect.height;
        
        console.log('[CRT] Canvas clicked at:', clickX.toFixed(3), clickY.toFixed(3));
        
        // Find nearest track within threshold
        let nearestTrack = null;
        let nearestDist = 0.05;  // 5% of screen
        
        if (this.tracks && this.tracks.length > 0) {
            this.tracks.forEach(track => {
                const dx = track.x - clickX;
                const dy = track.y - clickY;
                const dist = Math.sqrt(dx*dx + dy*dy);
                
                if (dist < nearestDist) {
                    nearestDist = dist;
                    nearestTrack = track;
                }
            });
        }
        
        if (nearestTrack) {
            // Deselect all tracks first
            this.tracks.forEach(t => t.selected = false);
            // Select the clicked track
            nearestTrack.selected = true;
            
            // Call callback if set
            if (this.onTrackClick) {
                this.onTrackClick(nearestTrack);
            }
            
            console.log('[CRT] Track selected:', nearestTrack.id, 'at distance:', nearestDist.toFixed(3));
        } else {
            console.log('[CRT] No track found near click (tracks:', this.tracks ? this.tracks.length : 0, ')');
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
        
        // Draw network stations overlay (Priority 6) if available
        if (this.networkStations && Array.isArray(this.networkStations) && this.networkStations.length > 0) {
            this.drawNetworkStations();
        }
        
        // Draw bright sweep leading edge on top
        this.drawSweepBright();
        
        // Draw bright track markers on top
        this.drawTracksBright();
        
        // Draw interceptors on top (blue triangles with vectors)
        this.drawInterceptors();
        
        this.animationId = requestAnimationFrame(() => this.render());
    }
    
    drawRangeRings() {
        const rings = [50, 100, 150, 200, 250, 300, 350];
        
        // Draw DIRECTLY to main canvas (static overlay, always visible)
        this.ctx.strokeStyle = 'rgba(0, 255, 100, 0.4)';  // Authentic P7 green phosphor
        this.ctx.lineWidth = 1;  // Thin lines like real CRT
        
        rings.forEach(radius => {
            this.ctx.beginPath();
            this.ctx.arc(this.centerX, this.centerY, radius, 0, Math.PI * 2);
            this.ctx.stroke();
        });
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
            
            // Color based on correlation state
            let trackColor = this.phosphorSlow;  // Default green
            if (track.correlation_state === 'uncorrelated') {
                trackColor = 'rgba(255, 255, 0, 0.8)';  // Yellow for uncorrelated
            } else if (track.correlation_state === 'correlating') {
                trackColor = 'rgba(255, 165, 0, 0.8)';  // Orange for correlating
            }
            
            // Add to persistence layer
            this.persistenceCtx.fillStyle = trackColor;
            this.persistenceCtx.beginPath();
            this.persistenceCtx.arc(x, y, 4, 0, Math.PI * 2);
            this.persistenceCtx.fill();
            
            // Add question mark symbol for uncorrelated tracks
            if (track.correlation_state === 'uncorrelated') {
                this.persistenceCtx.fillStyle = 'rgba(255, 255, 0, 1.0)';
                this.persistenceCtx.font = '14px "Courier New", monospace';
                this.persistenceCtx.textAlign = 'center';
                this.persistenceCtx.textBaseline = 'middle';
                this.persistenceCtx.fillText('?', x + 12, y - 10);
            }
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
            
            // Color based on correlation state
            let brightColor = this.phosphorFast;  // Default blue-white
            let shadowColor = this.phosphorSlow;  // Default green glow
            
            if (track.correlation_state === 'uncorrelated') {
                brightColor = 'rgba(255, 255, 0, 1.0)';  // Yellow bright
                shadowColor = 'rgba(255, 255, 0, 0.8)';  // Yellow glow
            } else if (track.correlation_state === 'correlating') {
                brightColor = 'rgba(255, 200, 0, 1.0)';  // Orange bright
                shadowColor = 'rgba(255, 165, 0, 0.8)';  // Orange glow
            }
            
            // Draw bright spot with glow
            this.ctx.fillStyle = brightColor;
            this.ctx.shadowColor = shadowColor;
            this.ctx.shadowBlur = 15;
            this.ctx.shadowColor = this.phosphorSlow;
            this.ctx.beginPath();
            this.ctx.arc(x, y, 3, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        });
    }
    
    drawInterceptors() {
        // Draw interceptor aircraft as blue triangles with heading indicators
        if (!this.interceptors || !Array.isArray(this.interceptors)) {
            return;
        }
        
        this.interceptors.forEach(interceptor => {
            // Only draw if not at base and not READY status
            if (interceptor.status === 'READY' || interceptor.status === 'REFUELING') {
                return;
            }
            
            const x = this.centerX + (interceptor.x * this.width);
            const y = this.centerY + (interceptor.y * this.height);
            
            // Draw intercept vector (dashed line to target) if engaging
            if (interceptor.assigned_target_id && (interceptor.status === 'AIRBORNE' || interceptor.status === 'ENGAGING')) {
                const target = this.tracks.find(t => t.id === interceptor.assigned_target_id);
                if (target) {
                    const targetX = this.centerX + (target.x * this.width);
                    const targetY = this.centerY + (target.y * this.height);
                    
                    this.ctx.strokeStyle = 'rgba(0, 150, 255, 0.6)';
                    this.ctx.lineWidth = 1;
                    this.ctx.setLineDash([5, 5]);
                    this.ctx.beginPath();
                    this.ctx.moveTo(x, y);
                    this.ctx.lineTo(targetX, targetY);
                    this.ctx.stroke();
                    this.ctx.setLineDash([]);
                }
            }
            
            // Draw interceptor as triangle pointing in heading direction
            const heading = (interceptor.heading || 0) * Math.PI / 180;
            const size = 8;
            
            this.ctx.save();
            this.ctx.translate(x, y);
            this.ctx.rotate(heading);
            
            // Status-based colors
            let color = 'rgba(0, 150, 255, 0.9)';  // Default blue
            if (interceptor.status === 'ENGAGING') {
                color = 'rgba(255, 50, 50, 0.9)';  // Red when engaging
            } else if (interceptor.status === 'RETURNING') {
                color = 'rgba(100, 100, 255, 0.7)';  // Lighter blue returning
            }
            
            // Draw triangle
            this.ctx.fillStyle = color;
            this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
            this.ctx.lineWidth = 1;
            this.ctx.beginPath();
            this.ctx.moveTo(size, 0);  // Nose pointing right (0 degrees)
            this.ctx.lineTo(-size, size);  // Bottom left
            this.ctx.lineTo(-size, -size);  // Top left
            this.ctx.closePath();
            this.ctx.fill();
            this.ctx.stroke();
            
            this.ctx.restore();
            
            // Add ID label if active
            if (interceptor.status === 'AIRBORNE' || interceptor.status === 'ENGAGING') {
                this.ctx.fillStyle = 'rgba(0, 200, 255, 0.9)';
                this.ctx.font = '10px "Courier New", monospace';
                this.ctx.textAlign = 'left';
                this.ctx.textBaseline = 'middle';
                this.ctx.fillText(interceptor.id, x + 12, y);
            }
        });
    }
    
    updateTracks(tracks) {
        this.tracks = tracks || [];
    }
    
    updateInterceptors(interceptors) {
        this.interceptors = interceptors || [];
    }
    
    updateOverlays(overlays) {
        this.overlays = new Set(overlays || []);
    }
    
    updateGeoData(geoData) {
        this.geoData = geoData;
    }
    
    updateNetworkStations(stations) {
        this.networkStations = stations;
    }
    
    drawNetworkStations() {
        // Call renderNetworkStations method if it was added by network_stations.py
        if (typeof this.renderNetworkStations === 'function' && this.networkStations) {
            this.renderNetworkStations(this.networkStations);
        }
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
            
            // Set up light gun callback to communicate with Reflex
            window.crtRadarScope.onTrackClick = function(track) {
                console.log('[CRT] Track clicked, sending to Reflex:', track.id);
                
                // Trigger Reflex state update by calling the global event handler
                // This function is injected by Reflex's rx.script() on the page
                if (typeof window.__reflex_track_selected !== 'undefined' && window.__reflex_track_selected) {
                    window.__reflex_track_selected(track.id);
                } else {
                    console.warn('[CRT] Reflex track selection handler not found');
                }
            };
            
            console.log('[CRT] ✓ Radar scope initialized with P7 phosphor');
        }
        
        return true;
    }
    
    return false;
}

// Data update loop (separate from initialization)
// Updated to use global variables instead of data attributes to avoid JSON corruption
var sageScriptsExecuted = false;
setInterval(function() {
    // Execute SAGE data scripts if not already done (fallback for hot reload)
    if (!sageScriptsExecuted && !window.__SAGE_TRACKS__) {
        var scripts = Array.from(document.querySelectorAll('script'));
        var executed = 0;
        scripts.forEach(function(s) {
            var text = s.innerHTML || '';
            if (text.includes('__SAGE_')) {
                try {
                    eval(text);
                    executed++;
                } catch(e) {
                    console.error('[SAGE] Error executing data script:', e);
                }
            }
        });
        if (executed > 0) {
            console.log('[SAGE] Executed ' + executed + ' data injection scripts (hot reload fallback)');
            sageScriptsExecuted = true;
        }
    }
    
    if (window.crtRadarScope) {
        // Read track data from global variable injected by Python state
        if (window.__SAGE_TRACKS__ && Array.isArray(window.__SAGE_TRACKS__)) {
            try {
                window.crtRadarScope.updateTracks(window.__SAGE_TRACKS__);
            } catch(e) {
                console.error('[CRT] Error updating tracks:', e);
            }
        }
        
        // Read interceptor data from global variable injected by Python state
        if (window.__SAGE_INTERCEPTORS__ && Array.isArray(window.__SAGE_INTERCEPTORS__)) {
            try {
                window.crtRadarScope.updateInterceptors(window.__SAGE_INTERCEPTORS__);
            } catch(e) {
                console.error('[CRT] Error updating interceptors:', e);
            }
        }
        
        // Read geo data from global variable injected by Python state
        if (window.__SAGE_GEO__) {
            try {
                window.crtRadarScope.updateGeoData(window.__SAGE_GEO__);
            } catch(e) {
                console.error('[CRT] Error updating geo data:', e);
            }
        }
        
        // Read network station data from global variable (Priority 6)
        if (window.__SAGE_NETWORK_STATIONS__ && Array.isArray(window.__SAGE_NETWORK_STATIONS__)) {
            try {
                window.crtRadarScope.updateNetworkStations(window.__SAGE_NETWORK_STATIONS__);
            } catch(e) {
                console.error('[CRT] Error updating network stations:', e);
            }
        }
    }
}, 1000);

// Continuous polling to detect canvas replacement by React
var pollInterval = setInterval(function() {
    initCRTWhenReady();
}, 100);

console.log('[CRT] Auto-initialization started with continuous canvas monitoring');
