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
        
        // P14 Phosphor (historically accurate SAGE situation display)
        // Purple flash when electron beam hits, orange afterglow for 2-3 seconds
        this.phosphorFast = 'rgba(180, 100, 255, 0.9)';      // Purple flash (fast decay ~100ms)
        this.phosphorSlow = 'rgba(255, 180, 100, 0.8)';      // Orange afterglow (slow persistence)
        this.phosphorPersistence = 'rgba(255, 180, 100, 0.4)'; // Fading orange trail
        
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
        
        // Track history for bright/dim trail rendering (Priority 8 - Task 4)
        // Map<trackId, Array<{x, y, timestamp}>>
        // Stores last 7 positions per track for P14 phosphor history effect
        this.trackHistory = new Map();
        this.historyMaxLength = 7;
        this.historyUpdateInterval = 500; // milliseconds between history snapshots
        this.lastHistoryUpdate = Date.now();
        
        // 7x7 Sector Grid State (IBM DSP authentic feature)
        this.show_sector_grid = false;
        this.expansion_level = 1;  // 1x, 2x, 4x, 8x
        this.selected_sector_row = 3;  // 0-6 (center = 3)
        this.selected_sector_col = 3;  // 0-6 (center = 3)
        
        // Phosphor persistence decay alpha (how much to fade each frame)
        // P14 phosphor has ~2-3 second visible persistence (orange afterglow)
        // At 60fps, need ~0.008-0.010 for proper P14 decay rate
        this.persistenceDecay = 0.009;  // Gives ~2.5 second trails (matches 2.5s refresh)
        
        // SAGE 2.5-second computer refresh cycle (Priority 7 - Phase 3)
        this.lastComputerRefresh = Date.now();
        this.refreshInterval = 2500; // milliseconds (historically accurate)
        this.enableRefreshCycle = true; // Toggle for A/B comparison
        
        // Animation
        this.lastFrameTime = Date.now();
        this.sweepSpeed = 6.0; // degrees per second
        
        console.log('[CRT] Initialized with P14 phosphor simulation (purple flash + orange afterglow)');
        console.log('[CRT] Persistence decay:', this.persistenceDecay);
        console.log('[CRT] Computer refresh cycle:', this.enableRefreshCycle ? '2.5 seconds (authentic)' : 'continuous (modern)');
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
        
        // Apply phosphor persistence decay to fade old content (always at 60fps)
        this.persistenceCtx.globalCompositeOperation = 'source-over';
        this.persistenceCtx.fillStyle = `rgba(0, 0, 0, ${this.persistenceDecay})`;
        this.persistenceCtx.fillRect(0, 0, this.width, this.height);
        
        // SAGE 2.5-second computer refresh cycle (Phase 3)
        // Computer updates display drum every 2.5 seconds, phosphor decays continuously
        const timeSinceRefresh = now - this.lastComputerRefresh;
        const shouldRefresh = this.enableRefreshCycle 
            ? (timeSinceRefresh >= this.refreshInterval)
            : true; // Always refresh if cycle disabled (modern continuous mode)
        
        if (shouldRefresh) {
            // Fetch updated track data from window globals
            this.updateTrackData();
            
            // Write fresh data to persistence layer (computer refresh)
            this.addSweepToPersistence();
            this.drawTracksOnPersistence();
            
            // Reset refresh timer
            if (this.enableRefreshCycle) {
                this.lastComputerRefresh = now;
            }
        } else {
            // Between refreshes: only add sweep trail, don't redraw tracks
            // This simulates phosphor persistence while waiting for next computer update
            this.addSweepToPersistence();
        }
        
        // Now composite everything to main display canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Save context state before zoom transformation
        this.ctx.save();
        
        // Apply sector zoom if expansion > 1x
        if (this.expansion_level > 1) {
            this.applySectorZoom();
        }
        
        // Draw persistence layer (faded trails)
        this.ctx.drawImage(this.persistenceCanvas, 0, 0);
        
        // NOTE: Range rings removed for historical authenticity
        // SD (Situation Display) consoles showed computer-processed tracks from 28 radar stations.
        // Range rings belong on PPI (Plan Position Indicator) displays at actual radar stations,
        // not on Direction Center SD consoles where "range from where?" is ambiguous.
        
        // Draw 7x7 sector grid (IBM DSP authentic feature)
        if (this.show_sector_grid) {
            this.drawSectorGrid();
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
        
        // Restore context state (undo zoom transformation)
        this.ctx.restore();
        
        this.animationId = requestAnimationFrame(() => this.render());
    }
    
    /**
     * Apply sector zoom transformation to canvas context
     * 
     * IMPLEMENTATION:
     * When expansion_level > 1, we zoom into the selected sector by:
     * 1. Calculating sector boundaries (7x7 grid)
     * 2. Translating canvas to move selected sector to origin
     * 3. Scaling by expansion_level (2x, 4x, 8x)
     * 4. Translating back so zoomed sector fills display
     * 
     * This makes tracks in selected sector appear larger while keeping
     * normalized coordinates (0-1) unchanged in code.
     */
    applySectorZoom() {
        const sectorWidth = this.width / 7;
        const sectorHeight = this.height / 7;
        
        // Calculate sector boundaries in canvas coordinates
        const sectorX = this.selected_sector_col * sectorWidth;
        const sectorY = this.selected_sector_row * sectorHeight;
        
        // Calculate zoom origin (center of selected sector)
        const centerX = sectorX + sectorWidth / 2;
        const centerY = sectorY + sectorHeight / 2;
        
        // Apply transformation:
        // 1. Translate so sector center is at canvas center
        // 2. Scale by expansion level
        // 3. Result: selected sector fills entire display
        
        // Move origin to center of canvas
        this.ctx.translate(this.width / 2, this.height / 2);
        
        // Scale by expansion level
        this.ctx.scale(this.expansion_level, this.expansion_level);
        
        // Move back so selected sector center is at origin
        this.ctx.translate(-centerX, -centerY);
    }
    
    /**
     * Apply sector zoom transformation to persistence canvas
     * Same logic as applySectorZoom() but for persistenceCtx
     */
    applySectorZoomToPersistence() {
        const sectorWidth = this.width / 7;
        const sectorHeight = this.height / 7;
        
        const sectorX = this.selected_sector_col * sectorWidth;
        const sectorY = this.selected_sector_row * sectorHeight;
        
        const centerX = sectorX + sectorWidth / 2;
        const centerY = sectorY + sectorHeight / 2;
        
        this.persistenceCtx.translate(this.width / 2, this.height / 2);
        this.persistenceCtx.scale(this.expansion_level, this.expansion_level);
        this.persistenceCtx.translate(-centerX, -centerY);
    }
    
    /**
     * Draw 7x7 sector grid overlay (IBM DSP authentic feature)
     * 
     * HISTORICAL CONTEXT:
     * IBM DSP 1 documentation shows Direction Centers used 7x7 sector grid
     * with off-centering push-buttons for 8x expansion. This solved the
     * "symbology overprinting problem" when many tracks clustered together.
     * 
     * "16 incidents were related to [symbology overprinting] problem and all
     * recommendations called for the provision of X8 as a solution."
     * 
     * Grid divides display into 49 sectors (7 rows × 7 columns). Operators
     * select sector via push-buttons, then magnify to 8x for detailed view.
     */
    drawSectorGrid() {
        const sectorWidth = this.width / 7;
        const sectorHeight = this.height / 7;
        
        // Use dim P14 orange for grid lines (low visibility, non-intrusive)
        this.ctx.strokeStyle = 'rgba(255, 180, 100, 0.15)';
        this.ctx.lineWidth = 1;
        this.ctx.setLineDash([]);  // Solid lines
        
        // Draw 6 vertical lines (creates 7 columns)
        for (let i = 1; i < 7; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(i * sectorWidth, 0);
            this.ctx.lineTo(i * sectorWidth, this.height);
            this.ctx.stroke();
        }
        
        // Draw 6 horizontal lines (creates 7 rows)
        for (let i = 1; i < 7; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * sectorHeight);
            this.ctx.lineTo(this.width, i * sectorHeight);
            this.ctx.stroke();
        }
        
        // Highlight selected sector if expansion enabled
        if (this.expansion_level > 1 && this.selected_sector_row >= 0 && this.selected_sector_col >= 0) {
            const row = this.selected_sector_row;
            const col = this.selected_sector_col;
            
            // Draw bright outline around selected sector
            this.ctx.strokeStyle = 'rgba(255, 180, 100, 0.6)';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(
                col * sectorWidth,
                row * sectorHeight,
                sectorWidth,
                sectorHeight
            );
            
            // Draw sector label (e.g., "3-D | 8X")
            const sectorLabel = `SECTOR ${row + 1}-${String.fromCharCode(65 + col)} | ${this.expansion_level}X`;
            this.ctx.font = '12px monospace';
            this.ctx.fillStyle = 'rgba(255, 180, 100, 0.9)';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(
                sectorLabel,
                col * sectorWidth + sectorWidth / 2,
                row * sectorHeight + 20
            );
        }
    }
    
    // HISTORICAL NOTE: Range rings removed for authenticity
    // IBM DSP 1 Figure 9.2 shows NO range rings on SAGE SD consoles.
    // Range rings appear on PPI radar displays (rotating sweep) at radar stations.
    // SD consoles showed processed tracks from 28 radars - "range from where?" is meaningless.
    // Geographic reference provided by coastlines instead.
    /*
    drawRangeRings() {
        const rings = [50, 100, 150, 200, 250, 300, 350];
        
        // Draw DIRECTLY to main canvas (static overlay, always visible)
        this.ctx.strokeStyle = 'rgba(255, 180, 100, 0.3)';  // P14 phosphor orange (dim intensity)
        this.ctx.lineWidth = 1;  // Thin lines like real CRT
        
        rings.forEach(radius => {
            this.ctx.beginPath();
            this.ctx.arc(this.centerX, this.centerY, radius, 0, Math.PI * 2);
            this.ctx.stroke();
        });
    }
    */
    
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
        gradient.addColorStop(1, 'rgba(255, 180, 100, 0)');  // P14 orange transparent
        
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
        // SAGE authentic: Monochrome P14 phosphor, symbol SHAPES indicate track type
        if (!this.tracks || !Array.isArray(this.tracks)) {
            return;
        }
        
        // Save persistence context state
        this.persistenceCtx.save();
        
        // Apply sector zoom if expansion > 1x
        if (this.expansion_level > 1) {
            this.applySectorZoomToPersistence();
        }
        
        this.tracks.forEach(track => {
            // Tracks use normalized coordinates (0-1), convert to canvas pixels
            const x = track.x * this.width;
            const y = track.y * this.height;
            
            // Monochrome P14 orange phosphor (all tracks same color)
            this.persistenceCtx.strokeStyle = this.phosphorSlow;
            this.persistenceCtx.fillStyle = this.phosphorSlow;
            this.persistenceCtx.lineWidth = 2;
            
            // Correlation state: dashed outline for uncorrelated
            if (track.correlation_state === 'uncorrelated') {
                this.persistenceCtx.setLineDash([3, 3]);
            } else {
                this.persistenceCtx.setLineDash([]);
            }
            
            // Track type determines SYMBOL SHAPE (not color)
            // Based on historical SAGE symbology
            const trackType = track.track_type || 'unknown';
            
            if (trackType === 'friendly') {
                // Circle for friendly
                this.persistenceCtx.beginPath();
                this.persistenceCtx.arc(x, y, 6, 0, Math.PI * 2);
                this.persistenceCtx.stroke();
            } else if (trackType === 'hostile' || trackType === 'bomber' || trackType === 'fighter') {
                // Square for hostile
                this.persistenceCtx.strokeRect(x - 6, y - 6, 12, 12);
            } else if (trackType === 'missile') {
                // Triangle pointing up for missile
                this.persistenceCtx.beginPath();
                this.persistenceCtx.moveTo(x, y - 8);
                this.persistenceCtx.lineTo(x + 7, y + 6);
                this.persistenceCtx.lineTo(x - 7, y + 6);
                this.persistenceCtx.closePath();
                this.persistenceCtx.stroke();
            } else {
                // Diamond for unknown
                this.persistenceCtx.beginPath();
                this.persistenceCtx.moveTo(x, y - 8);
                this.persistenceCtx.lineTo(x + 8, y);
                this.persistenceCtx.lineTo(x, y + 8);
                this.persistenceCtx.lineTo(x - 8, y);
                this.persistenceCtx.closePath();
                this.persistenceCtx.stroke();
            }
            
            // Reset line dash
            this.persistenceCtx.setLineDash([]);
            
            // Question mark for uncorrelated tracks
            if (track.correlation_state === 'uncorrelated') {
                this.persistenceCtx.font = '14px "Courier New", monospace';
                this.persistenceCtx.textAlign = 'center';
                this.persistenceCtx.textBaseline = 'middle';
                this.persistenceCtx.fillText('?', x + 12, y - 10);
            }
        });
        
        // Restore persistence context state
        this.persistenceCtx.restore();
    }
    
    drawTracksBright() {
        // Draw bright track markers on top with history trails (doesn't persist)
        // P14 phosphor: purple flash on impact, orange afterglow history
        // Priority 8 Task 4: Bright/dim history system with 7-position trails
        if (!this.tracks || !Array.isArray(this.tracks)) {
            return;
        }
        
        // Alpha values for history trail (7 positions, progressively dimmer)
        const historyAlpha = [0.85, 0.7, 0.55, 0.4, 0.3, 0.2, 0.15];
        
        this.tracks.forEach(track => {
            // Draw history trail first (dim positions)
            const history = this.trackHistory.get(track.id);
            if (history && history.length > 0) {
                // Draw from oldest to newest (so newest overlaps oldest)
                for (let i = 0; i < history.length; i++) {
                    const pos = history[i];
                    const x = pos.x * this.width;
                    const y = pos.y * this.height;
                    const alpha = historyAlpha[i] || 0.1;
                    
                    // Use orange phosphor for history (P14 afterglow)
                    const historyColor = `rgba(255, 180, 100, ${alpha})`;
                    
                    this.ctx.fillStyle = historyColor;
                    this.ctx.shadowColor = historyColor;
                    this.ctx.shadowBlur = 8;
                    this.ctx.beginPath();
                    this.ctx.arc(x, y, 2, 0, Math.PI * 2);
                    this.ctx.fill();
                }
                this.ctx.shadowBlur = 0;
            }
            
            // Draw present position (brightest)
            const x = track.x * this.width;
            const y = track.y * this.height;
            
            // Monochrome P14 phosphor: purple flash for present position
            const brightColor = this.phosphorFast;   // Purple flash
            const shadowColor = this.phosphorSlow;   // Orange glow
            
            // Draw bright center spot with P14 phosphor glow
            this.ctx.fillStyle = brightColor;
            this.ctx.shadowColor = shadowColor;
            this.ctx.shadowBlur = 15;
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
            
            // Interceptors use normalized coordinates (0-1), convert to canvas pixels
            const x = interceptor.x * this.width;
            const y = interceptor.y * this.height;
            
            // Draw intercept vector (dashed line to target) if engaging
            if (interceptor.assigned_target_id && (interceptor.status === 'AIRBORNE' || interceptor.status === 'ENGAGING')) {
                const target = this.tracks.find(t => t.id === interceptor.assigned_target_id);
                if (target) {
                    const targetX = target.x * this.width;
                    const targetY = target.y * this.height;
                    
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
            
            // P14 Monochrome: Use brightness/pattern/glow to differentiate status (NOT color)
            let alpha = 0.9;  // Default brightness (AIRBORNE)
            let lineDash = [];  // Default solid line
            let shadowBlur = 0;  // Default no glow
            
            if (interceptor.status === 'ENGAGING') {
                alpha = 1.0;  // BRIGHTEST for engaging
                shadowBlur = 15;  // Pulsing glow effect
            } else if (interceptor.status === 'RETURNING') {
                alpha = 0.5;  // DIM for returning to base
                lineDash = [3, 3];  // Dashed outline
            }
            
            const color = `rgba(255, 180, 100, ${alpha})`;  // P14 orange monochrome
            
            // Draw triangle
            this.ctx.fillStyle = color;
            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 2;
            this.ctx.setLineDash(lineDash);
            if (shadowBlur > 0) {
                this.ctx.shadowBlur = shadowBlur;
                this.ctx.shadowColor = 'rgba(255, 180, 100, 1.0)';
            }
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
                this.ctx.fillStyle = 'rgba(255, 180, 100, 0.9)';  // P14 orange monochrome
                this.ctx.font = '10px "Courier New", monospace';
                this.ctx.textAlign = 'left';
                this.ctx.textBaseline = 'middle';
                this.ctx.fillText(interceptor.id, x + 12, y);
            }
        });
    }
    
    updateTrackData() {
        // Fetch fresh data from window globals (simulates computer reading display drum)
        if (window.__SAGE_TRACKS__) {
            this.tracks = window.__SAGE_TRACKS__;
            
            // Update track history for bright/dim trail rendering
            const now = Date.now();
            if (now - this.lastHistoryUpdate >= this.historyUpdateInterval) {
                this.updateTrackHistory(now);
                this.lastHistoryUpdate = now;
            }
        }
        if (window.__SAGE_INTERCEPTORS__) {
            this.interceptors = window.__SAGE_INTERCEPTORS__;
        }
        if (window.__SAGE_OVERLAYS__) {
            this.overlays = new Set(window.__SAGE_OVERLAYS__);
        }
        if (window.__SAGE_GEO_DATA__) {
            this.geoData = window.__SAGE_GEO_DATA__;
        }
        if (window.__SAGE_NETWORK_STATIONS__) {
            this.networkStations = window.__SAGE_NETWORK_STATIONS__;
        }
        if (window.__SAGE_SECTOR_GRID__) {
            const grid = window.__SAGE_SECTOR_GRID__;
            this.show_sector_grid = grid.show_sector_grid;
            this.expansion_level = grid.expansion_level;
            this.selected_sector_row = grid.selected_sector_row;
            this.selected_sector_col = grid.selected_sector_col;
        }
    }
    
    updateTrackHistory(timestamp) {
        /**
         * Update track history for bright/dim trail rendering
         * Called every ~500ms to capture track positions
         * Maintains last 7 positions per track for P14 phosphor history effect
         */
        if (!this.tracks || !Array.isArray(this.tracks)) {
            return;
        }
        
        // Create set of current track IDs
        const currentTrackIds = new Set(this.tracks.map(t => t.id));
        
        // Remove history for tracks that no longer exist
        for (const trackId of this.trackHistory.keys()) {
            if (!currentTrackIds.has(trackId)) {
                this.trackHistory.delete(trackId);
            }
        }
        
        // Update history for each current track
        this.tracks.forEach(track => {
            let history = this.trackHistory.get(track.id);
            if (!history) {
                history = [];
                this.trackHistory.set(track.id, history);
            }
            
            // Add current position to history
            history.push({
                x: track.x,
                y: track.y,
                timestamp: timestamp
            });
            
            // Keep only last N positions (shift oldest if exceeded)
            if (history.length > this.historyMaxLength) {
                history.shift();
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
