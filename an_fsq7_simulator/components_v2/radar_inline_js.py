"""
Embedded radar scope JavaScript as a Python string constant.
This will be injected inline into the page.
"""

RADAR_SCOPE_INLINE_JS = """
class RadarScope {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error('Canvas with id ' + canvasId + ' not found');
            return;
        }
        
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        this.tracks = [];
        this.overlays = new Set(['range_rings', 'coastlines']);
        this.geoData = null;
        this.sweepAngle = 0;
        this.brightness = 0.75;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
        this.zoom = 1.0;
        this.panX = 0;
        this.panY = 0;
        
        this.trailHistory = new Map();
        this.maxTrailLength = 20;
        this.trailFadeMs = 5000;
        
        this.onTrackClick = null;
        this.canvas.addEventListener('click', function(e) { this.handleClick(e); }.bind(this));
        
        this.lastFrameTime = Date.now();
        requestAnimationFrame(function() { this.render(); }.bind(this));
        
        console.log('RadarScope initialized:', canvasId);
    }
    
    updateTracks(tracks) {
        this.tracks = tracks || [];
        var now = Date.now();
        var self = this;
        this.tracks.forEach(function(track) {
            if (!self.trailHistory.has(track.id)) {
                self.trailHistory.set(track.id, []);
            }
            var trail = self.trailHistory.get(track.id);
            trail.push({ x: track.x, y: track.y, timestamp: now });
            while (trail.length > self.maxTrailLength || (trail.length > 0 && now - trail[0].timestamp > self.trailFadeMs)) {
                trail.shift();
            }
        });
    }
    
    updateOverlays(overlays) {
        this.overlays = new Set(overlays || ['range_rings', 'coastlines']);
    }
    
    updateGeoData(geoData) {
        this.geoData = geoData;
    }
    
    setBrightness(brightness) {
        this.brightness = Math.max(0.2, Math.min(1.0, brightness));
    }
    
    handleClick(e) {
        var rect = this.canvas.getBoundingClientRect();
        var clickX = (e.clientX - rect.left) / rect.width;
        var clickY = (e.clientY - rect.top) / rect.height;
        
        var nearestTrack = null;
        var nearestDist = 0.05;
        var self = this;
        
        this.tracks.forEach(function(track) {
            var dx = track.x - clickX;
            var dy = track.y - clickY;
            var dist = Math.sqrt(dx*dx + dy*dy);
            
            if (dist < nearestDist) {
                nearestDist = dist;
                nearestTrack = track;
            }
        });
        
        if (nearestTrack) {
            this.tracks.forEach(function(t) { t.selected = false; });
            nearestTrack.selected = true;
            if (this.onTrackClick) {
                this.onTrackClick(nearestTrack);
            }
        }
    }
    
    render() {
        var now = Date.now();
        var dt = now - this.lastFrameTime;
        this.lastFrameTime = now;
        
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.sweepAngle = (this.sweepAngle + (dt / 4000) * Math.PI * 2) % (Math.PI * 2);
        
        this.ctx.save();
        this.ctx.translate(this.centerX + this.panX, this.centerY + this.panY);
        this.ctx.scale(this.zoom, this.zoom);
        this.ctx.translate(-this.centerX, -this.centerY);
        
        if (this.geoData) {
            this.drawGeographicOverlays();
        }
        
        this.drawSweep();
        this.drawTracks();
        
        this.ctx.restore();
        
        requestAnimationFrame(function() { this.render(); }.bind(this));
    }
    
    drawSweep() {
        var gradient = this.ctx.createRadialGradient(
            this.centerX, this.centerY, 0,
            this.centerX, this.centerY, Math.min(this.width, this.height) / 2
        );
        gradient.addColorStop(0, 'rgba(0, 255, 0, ' + (0.3 * this.brightness) + ')');
        gradient.addColorStop(0.5, 'rgba(0, 255, 0, ' + (0.1 * this.brightness) + ')');
        gradient.addColorStop(1, 'rgba(0, 255, 0, 0)');
        
        this.ctx.save();
        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY);
        var sweepX = this.centerX + Math.cos(this.sweepAngle) * (this.width / 2);
        var sweepY = this.centerY + Math.sin(this.sweepAngle) * (this.height / 2);
        this.ctx.lineTo(sweepX, sweepY);
        this.ctx.stroke();
        this.ctx.restore();
    }
    
    drawTracks() {
        var self = this;
        this.tracks.forEach(function(track) {
            var x = track.x * self.width;
            var y = track.y * self.height;
            var color = self.getTrackColor(track);
            var isSelected = track.selected || false;
            
            self.ctx.save();
            self.ctx.shadowColor = color;
            self.ctx.shadowBlur = isSelected ? 20 : 10;
            self.ctx.fillStyle = color;
            self.ctx.globalAlpha = self.brightness;
            
            self.ctx.beginPath();
            self.ctx.arc(x, y, isSelected ? 8 : 5, 0, Math.PI * 2);
            self.ctx.fill();
            
            if (isSelected) {
                self.ctx.strokeStyle = color;
                self.ctx.lineWidth = 2;
                self.ctx.globalAlpha = self.brightness * 0.8;
                self.ctx.beginPath();
                self.ctx.arc(x, y, 15, 0, Math.PI * 2);
                self.ctx.stroke();
            }
            
            self.ctx.restore();
        });
    }
    
    drawGeographicOverlays() {
        if (!this.geoData) return;
        var baseAlpha = this.brightness * 0.3;
        
        if (this.overlays.has('range_rings') && this.geoData.range_rings) {
            this.ctx.save();
            this.ctx.strokeStyle = 'rgba(0, 255, 0, ' + (baseAlpha * 0.6) + ')';
            this.ctx.lineWidth = 1;
            var self = this;
            this.geoData.range_rings.forEach(function(ring) {
                self.ctx.beginPath();
                self.ctx.arc(self.centerX, self.centerY, ring.radius * Math.min(self.width, self.height), 0, Math.PI * 2);
                self.ctx.stroke();
            });
            this.ctx.restore();
        }
    }
    
    getTrackColor(track) {
        switch(track.track_type) {
            case 'hostile': return '#ff0000';
            case 'missile': return '#ff00ff';
            case 'friendly': return '#00ff00';
            case 'interceptor': return '#0088ff';
            case 'unknown': return '#ffff00';
            default: return '#888888';
        }
    }
}

function initRadarScope(canvasId) {
    var scope = new RadarScope(canvasId);
    window.radarScope = scope;
    return scope;
}

window.initRadarScope = initRadarScope;
"""
