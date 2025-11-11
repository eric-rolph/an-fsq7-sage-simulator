"""
Geographic Overlays for Radar Scope

Provides realistic geographic context:
- East Coast and Great Lakes coastlines
- Range rings (100, 200, 300 miles)
- Bearing indicators (N/E/S/W)
- Major city markers
- Sector boundaries

All geometry stored as normalized coordinates (0.0-1.0)
for easy rendering on any canvas size.
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class GeoPoint:
    """A point in normalized coordinates"""
    x: float  # 0.0 (west) to 1.0 (east)
    y: float  # 0.0 (north) to 1.0 (south)
    label: str = ""


@dataclass
class GeoPolyline:
    """A series of connected points"""
    points: List[GeoPoint]
    name: str
    style: str = "solid"  # solid, dashed, dotted


# East Coast outline (simplified)
# Spans roughly from Boston (42°N, 71°W) to DC (38°N, 77°W)
# Normalized to 0.0-1.0 coordinate space
EAST_COAST_OUTLINE = GeoPolyline(
    name="East Coast",
    points=[
        # Maine coast
        GeoPoint(0.85, 0.05, "Maine"),
        GeoPoint(0.87, 0.08),
        GeoPoint(0.88, 0.12),
        
        # Massachusetts / Boston area
        GeoPoint(0.86, 0.18, "Boston"),
        GeoPoint(0.84, 0.22),
        GeoPoint(0.82, 0.26),
        
        # Long Island / NYC area
        GeoPoint(0.78, 0.32),
        GeoPoint(0.75, 0.36, "New York"),
        GeoPoint(0.72, 0.40),
        
        # New Jersey coast
        GeoPoint(0.70, 0.45),
        GeoPoint(0.68, 0.50),
        
        # Delaware / Philadelphia area
        GeoPoint(0.65, 0.55, "Philadelphia"),
        GeoPoint(0.62, 0.60),
        
        # Maryland / DC area
        GeoPoint(0.58, 0.66, "Washington DC"),
        GeoPoint(0.55, 0.70),
        
        # Virginia coast
        GeoPoint(0.52, 0.75),
        GeoPoint(0.50, 0.80),
    ],
    style="solid",
)


# Great Lakes outlines (simplified)
GREAT_LAKES_OUTLINE = GeoPolyline(
    name="Great Lakes",
    points=[
        # Lake Superior (north, west)
        GeoPoint(0.25, 0.15),
        GeoPoint(0.30, 0.12),
        GeoPoint(0.38, 0.15),
        GeoPoint(0.40, 0.20),
        GeoPoint(0.35, 0.22),
        GeoPoint(0.28, 0.20),
        GeoPoint(0.25, 0.15),
        
        # Gap for Lake Michigan
        GeoPoint(0.42, 0.30),
        
        # Lake Michigan
        GeoPoint(0.42, 0.30),
        GeoPoint(0.40, 0.35),
        GeoPoint(0.40, 0.45),
        GeoPoint(0.42, 0.50),
        GeoPoint(0.44, 0.48),
        GeoPoint(0.44, 0.32),
        GeoPoint(0.42, 0.30),
        
        # Gap for Lake Huron
        GeoPoint(0.48, 0.28),
        
        # Lake Huron
        GeoPoint(0.48, 0.28),
        GeoPoint(0.52, 0.25),
        GeoPoint(0.55, 0.28),
        GeoPoint(0.54, 0.35),
        GeoPoint(0.50, 0.36),
        GeoPoint(0.48, 0.32),
        GeoPoint(0.48, 0.28),
        
        # Lake Erie
        GeoPoint(0.52, 0.42),
        GeoPoint(0.58, 0.40),
        GeoPoint(0.65, 0.42),
        GeoPoint(0.66, 0.45),
        GeoPoint(0.60, 0.46),
        GeoPoint(0.54, 0.44),
        GeoPoint(0.52, 0.42),
        
        # Lake Ontario
        GeoPoint(0.66, 0.35),
        GeoPoint(0.72, 0.33),
        GeoPoint(0.75, 0.36),
        GeoPoint(0.72, 0.38),
        GeoPoint(0.68, 0.37),
        GeoPoint(0.66, 0.35),
    ],
    style="solid",
)


# Canadian border (approximate)
CANADIAN_BORDER = GeoPolyline(
    name="Canadian Border",
    points=[
        GeoPoint(0.20, 0.20),
        GeoPoint(0.45, 0.18),
        GeoPoint(0.70, 0.22),
        GeoPoint(0.90, 0.08),
    ],
    style="dashed",
)


# Major cities (as points for labeling)
MAJOR_CITIES: List[GeoPoint] = [
    GeoPoint(0.86, 0.18, "BOS"),  # Boston
    GeoPoint(0.75, 0.36, "NYC"),  # New York
    GeoPoint(0.65, 0.55, "PHL"),  # Philadelphia
    GeoPoint(0.58, 0.66, "DC"),   # Washington DC
    GeoPoint(0.44, 0.48, "CHI"),  # Chicago
    GeoPoint(0.54, 0.44, "CLE"),  # Cleveland
    GeoPoint(0.60, 0.46, "BUF"),  # Buffalo
    GeoPoint(0.52, 0.25, "DET"),  # Detroit
]


# Range rings (in miles, as radii from center)
RANGE_RINGS = [
    {"radius": 0.15, "distance_mi": 100, "label": "100 mi"},
    {"radius": 0.30, "distance_mi": 200, "label": "200 mi"},
    {"radius": 0.45, "distance_mi": 300, "label": "300 mi"},
]


# Bearing markers (compass directions)
BEARING_MARKERS = [
    {"angle": 0, "label": "N", "x": 0.50, "y": 0.02},    # North
    {"angle": 90, "label": "E", "x": 0.98, "y": 0.50},   # East
    {"angle": 180, "label": "S", "x": 0.50, "y": 0.98},  # South
    {"angle": 270, "label": "W", "x": 0.02, "y": 0.50},  # West
]


# Sector boundaries (SAGE divided airspace into sectors)
SECTOR_BOUNDARIES = [
    GeoPolyline(
        name="Sector A/B",
        points=[GeoPoint(0.50, 0.0), GeoPoint(0.50, 1.0)],
        style="dotted",
    ),
    GeoPolyline(
        name="Sector C/D",
        points=[GeoPoint(0.0, 0.50), GeoPoint(1.0, 0.50)],
        style="dotted",
    ),
]


class GeographicOverlays:
    """
    Container for all geographic overlay data
    Provides methods to retrieve geometry for rendering
    """
    
    @staticmethod
    def get_coastlines() -> List[GeoPolyline]:
        """Get all coastline polylines"""
        return [EAST_COAST_OUTLINE, GREAT_LAKES_OUTLINE, CANADIAN_BORDER]
    
    @staticmethod
    def get_cities() -> List[GeoPoint]:
        """Get major city markers"""
        return MAJOR_CITIES
    
    @staticmethod
    def get_range_rings() -> List[Dict]:
        """Get range ring specifications"""
        return RANGE_RINGS
    
    @staticmethod
    def get_bearing_markers() -> List[Dict]:
        """Get compass bearing markers"""
        return BEARING_MARKERS
    
    @staticmethod
    def get_sector_boundaries() -> List[GeoPolyline]:
        """Get sector boundary lines"""
        return SECTOR_BOUNDARIES
    
    @staticmethod
    def to_json() -> Dict:
        """
        Export all overlay data as JSON
        For passing to WebGL/Canvas renderer
        """
        return {
            "coastlines": [
                {
                    "name": line.name,
                    "points": [(p.x, p.y) for p in line.points],
                    "style": line.style,
                }
                for line in GeographicOverlays.get_coastlines()
            ],
            "cities": [
                {
                    "x": city.x,
                    "y": city.y,
                    "label": city.label,
                }
                for city in GeographicOverlays.get_cities()
            ],
            "range_rings": GeographicOverlays.get_range_rings(),
            "bearing_markers": GeographicOverlays.get_bearing_markers(),
            "sector_boundaries": [
                {
                    "name": line.name,
                    "points": [(p.x, p.y) for p in line.points],
                    "style": line.style,
                }
                for line in GeographicOverlays.get_sector_boundaries()
            ],
        }


# Canvas drawing instructions (for JavaScript/WebGL)
CANVAS_DRAW_SCRIPT = """
function drawGeographicOverlays(ctx, overlays, canvasWidth, canvasHeight, activeOverlays) {
    ctx.save();
    
    // Set drawing style for overlays
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.3)';
    ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
    ctx.lineWidth = 1.5;
    ctx.font = '12px Courier New';
    
    // Draw coastlines
    if (activeOverlays.has('coastlines')) {
        overlays.coastlines.forEach(coastline => {
            ctx.beginPath();
            if (coastline.style === 'dashed') {
                ctx.setLineDash([5, 5]);
            } else if (coastline.style === 'dotted') {
                ctx.setLineDash([2, 3]);
            } else {
                ctx.setLineDash([]);
            }
            
            coastline.points.forEach((point, i) => {
                const x = point[0] * canvasWidth;
                const y = point[1] * canvasHeight;
                if (i === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            ctx.stroke();
        });
        ctx.setLineDash([]);
    }
    
    // Draw range rings
    if (activeOverlays.has('range_rings')) {
        const centerX = canvasWidth / 2;
        const centerY = canvasHeight / 2;
        
        overlays.range_rings.forEach(ring => {
            ctx.beginPath();
            ctx.arc(
                centerX,
                centerY,
                ring.radius * Math.min(canvasWidth, canvasHeight),
                0,
                2 * Math.PI
            );
            ctx.stroke();
            
            // Draw label
            ctx.fillText(
                ring.label,
                centerX + ring.radius * canvasWidth + 5,
                centerY
            );
        });
    }
    
    // Draw bearing markers
    overlays.bearing_markers.forEach(marker => {
        const x = marker.x * canvasWidth;
        const y = marker.y * canvasHeight;
        ctx.fillText(marker.label, x - 5, y + 5);
    });
    
    // Draw city labels
    if (activeOverlays.has('callsigns')) {
        overlays.cities.forEach(city => {
            const x = city.x * canvasWidth;
            const y = city.y * canvasHeight;
            
            // Draw city dot
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
            
            // Draw label
            ctx.fillText(city.label, x + 5, y - 5);
        });
    }
    
    // Draw sector boundaries
    if (activeOverlays.has('sector_boundaries')) {
        ctx.strokeStyle = 'rgba(0, 255, 0, 0.15)';
        ctx.setLineDash([10, 10]);
        overlays.sector_boundaries.forEach(boundary => {
            ctx.beginPath();
            boundary.points.forEach((point, i) => {
                const x = point[0] * canvasWidth;
                const y = point[1] * canvasHeight;
                if (i === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            ctx.stroke();
        });
        ctx.setLineDash([]);
    }
    
    ctx.restore();
}
"""
