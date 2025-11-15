"""
SAGE Radar Network Station Visualization

Shows the distributed radar network that feeds into SAGE:
- DEW Line (Distant Early Warning) - Arctic stations
- Mid-Canada Line - across central Canada
- Pinetree Line - southern Canada/northern US
- Gap-filler radars - fill coverage gaps
- GCI stations - Ground Control Intercept centers

Provides system transparency showing how SAGE synthesizes
data from multiple radar sources into a unified air picture.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import reflex as rx


@dataclass
class RadarStation:
    """A radar station in the SAGE network"""
    id: str
    name: str
    station_type: str  # DEW, MID_CANADA, PINETREE, GAP_FILLER, GCI
    x: float  # Normalized 0.0-1.0 (west to east)
    y: float  # Normalized 0.0-1.0 (north to south)
    coverage_radius: float  # Miles
    status: str = "operational"  # operational, degraded, offline
    description: str = ""


# DEW Line Stations (Arctic - northern edge of map)
DEW_LINE_STATIONS = [
    RadarStation("DEW-1", "Cape Lisburne AFS", "DEW", 0.15, 0.02, 150, 
                 description="Alaska DEW Line station"),
    RadarStation("DEW-2", "Point Barrow", "DEW", 0.20, 0.01, 150,
                 description="Northernmost US radar"),
    RadarStation("DEW-3", "Barter Island", "DEW", 0.25, 0.02, 150,
                 description="Alaska-Canada border"),
    RadarStation("DEW-4", "Komakuk Beach", "DEW", 0.30, 0.02, 150,
                 description="Yukon DEW station"),
    RadarStation("DEW-5", "Tuktoyaktuk", "DEW", 0.35, 0.03, 150,
                 description="Northwest Territories"),
    RadarStation("DEW-6", "Cambridge Bay", "DEW", 0.45, 0.04, 150,
                 description="Central Arctic"),
    RadarStation("DEW-7", "Hall Beach", "DEW", 0.55, 0.05, 150,
                 description="Baffin Island"),
    RadarStation("DEW-8", "Resolution Island", "DEW", 0.65, 0.08, 150,
                 description="Eastern Arctic gateway"),
]

# Mid-Canada Line (across central Canada)
MID_CANADA_STATIONS = [
    RadarStation("MCL-1", "Dawson Creek", "MID_CANADA", 0.25, 0.18, 120,
                 description="British Columbia station"),
    RadarStation("MCL-2", "Fort McMurray", "MID_CANADA", 0.32, 0.20, 120,
                 description="Alberta oil sands region"),
    RadarStation("MCL-3", "The Pas", "MID_CANADA", 0.42, 0.22, 120,
                 description="Manitoba coverage"),
    RadarStation("MCL-4", "Winisk", "MID_CANADA", 0.50, 0.20, 120,
                 description="Hudson Bay approach"),
    RadarStation("MCL-5", "Moosonee", "MID_CANADA", 0.58, 0.24, 120,
                 description="James Bay coverage"),
    RadarStation("MCL-6", "Hopedale", "MID_CANADA", 0.70, 0.20, 120,
                 description="Labrador station"),
]

# Pinetree Line (southern Canada / northern US border)
PINETREE_STATIONS = [
    RadarStation("PT-1", "Comox", "PINETREE", 0.22, 0.32, 100,
                 description="Vancouver Island"),
    RadarStation("PT-2", "Baldy Hughes", "PINETREE", 0.28, 0.30, 100,
                 description="BC interior"),
    RadarStation("PT-3", "Cold Lake", "PINETREE", 0.35, 0.34, 100,
                 description="Alberta air base"),
    RadarStation("PT-4", "Minot AFB", "PINETREE", 0.42, 0.38, 100,
                 description="North Dakota"),
    RadarStation("PT-5", "Duluth", "PINETREE", 0.52, 0.38, 100,
                 description="Lake Superior coverage"),
    RadarStation("PT-6", "Sault Ste Marie", "PINETREE", 0.60, 0.36, 100,
                 description="Great Lakes gateway"),
    RadarStation("PT-7", "North Bay", "PINETREE", 0.68, 0.34, 100,
                 description="Ontario SAGE center"),
    RadarStation("PT-8", "Goose Bay", "PINETREE", 0.78, 0.28, 100,
                 description="Labrador air base"),
]

# Gap-filler radars (US interior - fill coverage gaps)
GAP_FILLER_STATIONS = [
    RadarStation("GF-1", "Grand Forks", "GAP_FILLER", 0.44, 0.42, 75,
                 description="Red River Valley"),
    RadarStation("GF-2", "Cavalier AFS", "GAP_FILLER", 0.46, 0.40, 75,
                 description="North Dakota gap"),
    RadarStation("GF-3", "Finley AFS", "GAP_FILLER", 0.48, 0.44, 75,
                 description="Eastern ND coverage"),
]

# GCI Stations (Ground Control Intercept - our simulation centers)
GCI_STATIONS = [
    RadarStation("GCI-1", "Otis AFB", "GCI", 0.85, 0.50, 200,
                 description="Cape Cod - Boston SAGE DC-03"),
    RadarStation("GCI-2", "Syracuse", "GCI", 0.75, 0.48, 180,
                 description="New York State coverage"),
    RadarStation("GCI-3", "Hancock Field", "GCI", 0.76, 0.46, 180,
                 description="Syracuse SAGE center"),
]

# All stations combined
ALL_STATIONS = (
    DEW_LINE_STATIONS + 
    MID_CANADA_STATIONS + 
    PINETREE_STATIONS + 
    GAP_FILLER_STATIONS + 
    GCI_STATIONS
)


# Station type styling
STATION_STYLES = {
    "DEW": {
        "color": "#00ffff",  # Cyan - arctic/distant
        "symbol": "△",
        "size": 10,
        "label": "DEW Line"
    },
    "MID_CANADA": {
        "color": "#ffaa00",  # Orange - mid-range
        "symbol": "◇",
        "size": 10,
        "label": "Mid-Canada Line"
    },
    "PINETREE": {
        "color": "#00ff00",  # Green - southern line
        "symbol": "▽",
        "size": 10,
        "label": "Pinetree Line"
    },
    "GAP_FILLER": {
        "color": "#ffff00",  # Yellow - fill gaps
        "symbol": "○",
        "size": 8,
        "label": "Gap-Filler"
    },
    "GCI": {
        "color": "#ff00ff",  # Magenta - command centers
        "symbol": "⬟",
        "size": 14,
        "label": "GCI / SAGE DC"
    }
}


def get_stations_by_type(station_type: str) -> List[RadarStation]:
    """Get all stations of a specific type"""
    return [s for s in ALL_STATIONS if s.station_type == station_type]


def get_station_by_id(station_id: str) -> Optional[RadarStation]:
    """Find a station by ID"""
    for station in ALL_STATIONS:
        if station.id == station_id:
            return station
    return None


def network_legend_panel() -> rx.Component:
    """Legend showing station types"""
    return rx.box(
        rx.vstack(
            rx.heading("SAGE RADAR NETWORK", size="3", color="#00ff00"),
            rx.text("Station Types:", font_size="12px", color="#888888", margin_top="10px"),
            
            # DEW Line
            rx.hstack(
                rx.text(
                    STATION_STYLES["DEW"]["symbol"],
                    color=STATION_STYLES["DEW"]["color"],
                    font_size="16px",
                    font_weight="bold"
                ),
                rx.text(
                    STATION_STYLES["DEW"]["label"],
                    font_size="11px",
                    color="#cccccc"
                ),
                spacing="2"
            ),
            
            # Mid-Canada Line
            rx.hstack(
                rx.text(
                    STATION_STYLES["MID_CANADA"]["symbol"],
                    color=STATION_STYLES["MID_CANADA"]["color"],
                    font_size="16px",
                    font_weight="bold"
                ),
                rx.text(
                    STATION_STYLES["MID_CANADA"]["label"],
                    font_size="11px",
                    color="#cccccc"
                ),
                spacing="2"
            ),
            
            # Pinetree Line
            rx.hstack(
                rx.text(
                    STATION_STYLES["PINETREE"]["symbol"],
                    color=STATION_STYLES["PINETREE"]["color"],
                    font_size="16px",
                    font_weight="bold"
                ),
                rx.text(
                    STATION_STYLES["PINETREE"]["label"],
                    font_size="11px",
                    color="#cccccc"
                ),
                spacing="2"
            ),
            
            # Gap-Filler
            rx.hstack(
                rx.text(
                    STATION_STYLES["GAP_FILLER"]["symbol"],
                    color=STATION_STYLES["GAP_FILLER"]["color"],
                    font_size="16px",
                    font_weight="bold"
                ),
                rx.text(
                    STATION_STYLES["GAP_FILLER"]["label"],
                    font_size="11px",
                    color="#cccccc"
                ),
                spacing="2"
            ),
            
            # GCI
            rx.hstack(
                rx.text(
                    STATION_STYLES["GCI"]["symbol"],
                    color=STATION_STYLES["GCI"]["color"],
                    font_size="16px",
                    font_weight="bold"
                ),
                rx.text(
                    STATION_STYLES["GCI"]["label"],
                    font_size="11px",
                    color="#cccccc"
                ),
                spacing="2"
            ),
            
            rx.divider(margin_top="10px", margin_bottom="10px"),
            
            rx.text(
                f"Total Stations: {len(ALL_STATIONS)}",
                font_size="11px",
                color="#888888"
            ),
            
            spacing="2",
            align_items="flex-start"
        ),
        padding="15px",
        background="rgba(0, 20, 0, 0.9)",
        border="1px solid #00ff00",
        border_radius="5px"
    )


# JavaScript for network rendering (to be injected in crt_radar.js)
NETWORK_RENDERING_SCRIPT = """
// Network station rendering for SAGE radar scope
// Extends crt_radar.js with station overlay capability

(function() {
    // Wait for CRTRadarScope to be defined, then install network rendering methods
    function installNetworkRendering() {
        if (typeof window.CRTRadarScope === 'undefined') {
            setTimeout(installNetworkRendering, 50);
            return;
        }
        
        // Helper: Get visual style for station type
        // P14 Phosphor: Monochrome orange, differentiation via SYMBOL SHAPE only
        window.CRTRadarScope.prototype.getStationStyle = function(stationType) {
            const phosphorOrange = 'rgba(255, 180, 100, 0.8)';  // P14 phosphor color
            const styles = {
                'DEW': { color: phosphorOrange, symbol: '△', size: 10 },        // Triangle up (Arctic)
                'MID_CANADA': { color: phosphorOrange, symbol: '◇', size: 10 }, // Diamond (Mid)
                'PINETREE': { color: phosphorOrange, symbol: '▽', size: 10 },   // Triangle down (South)
                'GAP_FILLER': { color: phosphorOrange, symbol: '○', size: 8 },  // Small circle (Local)
                'GCI': { color: phosphorOrange, symbol: '⬟', size: 14 }         // Pentagon (Command)
            };
            return styles[stationType] || styles['GAP_FILLER'];
        };
        
        // Helper: Calculate distance between two stations
        window.CRTRadarScope.prototype.stationDistance = function(s1, s2) {
            const dx = s2.x - s1.x;
            const dy = s2.y - s1.y;
            return Math.sqrt(dx * dx + dy * dy);
        };
        
        // Helper: Find nearest GCI station for data routing lines
        window.CRTRadarScope.prototype.findNearestGCI = function(station, allStations) {
            const gciStations = allStations.filter(s => s.station_type === 'GCI' && s.status === 'operational');
            if (gciStations.length === 0) return null;
            
            let nearest = gciStations[0];
            let minDist = this.stationDistance(station, nearest);
            
            for (let i = 1; i < gciStations.length; i++) {
                const dist = this.stationDistance(station, gciStations[i]);
                if (dist < minDist) {
                    minDist = dist;
                    nearest = gciStations[i];
                }
            }
            
            return nearest;
        };
        
        // Main rendering method
        window.CRTRadarScope.prototype.renderNetworkStations = function(stations) {
            if (!this.canvas || !this.ctx || !stations) return;
            
            const ctx = this.ctx;
            const width = this.canvas.width;
            const height = this.canvas.height;
            
            stations.forEach(station => {
                const x = station.x * width;
                const y = station.y * height;
                const style = this.getStationStyle(station.station_type);
                
                // Draw coverage radius (semi-transparent circle)
                if (station.status === 'operational' || station.status === 'degraded') {
                    ctx.save();
                    ctx.strokeStyle = style.color;
                    ctx.globalAlpha = station.status === 'operational' ? 0.2 : 0.1;
                    ctx.lineWidth = 1;
                    
                    // Convert coverage radius (miles) to pixels
                    // Assuming scope shows ~600 mile range
                    const radiusPixels = (station.coverage_radius / 600) * (Math.min(width, height) / 2);
                    
                    ctx.beginPath();
                    ctx.arc(x, y, radiusPixels, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.restore();
                }
                
                // Draw station marker
                ctx.save();
                ctx.fillStyle = style.color;
                ctx.font = `${style.size}px monospace`;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                
                // Status indication
                if (station.status === 'offline') {
                    ctx.globalAlpha = 0.3;
                } else if (station.status === 'degraded') {
                    ctx.globalAlpha = 0.6;
                }
                
                ctx.fillText(style.symbol, x, y);
                
                // Small label below station
                ctx.font = '8px monospace';
                ctx.fillText(station.name.substring(0, 8), x, y + 12);
                
                ctx.restore();
                
                // Connection line to GCI (if station is operational)
                if (station.status === 'operational' && station.station_type !== 'GCI') {
                    // Draw line to nearest GCI station
                    const gciStation = this.findNearestGCI(station, stations);
                    if (gciStation) {
                        ctx.save();
                        ctx.strokeStyle = style.color;
                        ctx.globalAlpha = 0.15;
                        ctx.lineWidth = 1;
                        ctx.setLineDash([2, 4]);
                        
                        ctx.beginPath();
                        ctx.moveTo(x, y);
                        ctx.lineTo(gciStation.x * width, gciStation.y * height);
                        ctx.stroke();
                        
                        ctx.restore();
                    }
                }
            });
        };
        
        console.log('[SAGE Network] Station rendering methods installed on CRTRadarScope.prototype');
    }
    
    // Install immediately or wait for CRTRadarScope to be defined
    installNetworkRendering();
})();
"""
