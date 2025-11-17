// SAGE Tabular Track Message Display System
// Based on C702-416L-ST Manual Figures 4-5, 4-6, 4-10
// Renders 5-feature tabular format (A, B, C, D, E) with vector

/**
 * Track Feature Layout Constants
 * Based on authentic SAGE display format
 */
const FEATURE_SPACING = 8;  // Pixels between feature rows
const CHAR_SPACING = 4;      // Pixels between characters within a feature
const VECTOR_LENGTH_SCALE = 2.0;  // Pixels per knot of speed
const VECTOR_MIN_LENGTH = 10;
const VECTOR_MAX_LENGTH = 60;

/**
 * Positioning modes for tabular format
 * Determines where features A/B/C/D appear relative to E (central point)
 * 
 * Mode 0: Format to right of central point
 * Mode 1: Format to left of central point  
 * Mode 2: Format above central point
 * Mode 3: Format below central point
 */
const POSITION_MODES = {
    RIGHT: 0,   // E feature | (format)
    LEFT: 1,    // (format) | E feature
    ABOVE: 2,   // (format above) \n E feature
    BELOW: 3    // E feature \n (format below)
};

/**
 * Render a single track in tabular format
 * @param {CanvasRenderingContext2D} ctx - Canvas context
 * @param {object} track - Track data with feature strings
 * @param {number} centerX - Screen X coordinate of E feature (central point)
 * @param {number} centerY - Screen Y coordinate of E feature (central point)
 * @param {string} color - Phosphor color
 * @param {number} alpha - Brightness (0.0-1.0)
 */
function renderTabularTrack(ctx, track, centerX, centerY, color, alpha = 1.0) {
    if (!track || !track.features) {
        console.warn('[Tabular Track] Invalid track data:', track);
        return;
    }
    
    const features = track.features;
    const positionMode = track.positionMode || POSITION_MODES.RIGHT;
    const charDims = window.DotMatrixFont.getCharDimensions();
    
    // Draw E feature (central point) - always brightest
    drawEFeature(ctx, centerX, centerY, color, alpha);
    
    // Calculate feature positions based on position mode
    let positions = calculateFeaturePositions(
        centerX, centerY, features, positionMode, charDims
    );
    
    // Draw features A, B, C, D
    if (features.A) {
        window.DotMatrixFont.renderString(
            ctx, features.A, positions.A.x, positions.A.y, color, alpha, CHAR_SPACING
        );
    }
    if (features.B) {
        window.DotMatrixFont.renderString(
            ctx, features.B, positions.B.x, positions.B.y, color, alpha, CHAR_SPACING
        );
    }
    if (features.C) {
        window.DotMatrixFont.renderString(
            ctx, features.C, positions.C.x, positions.C.y, color, alpha, CHAR_SPACING
        );
    }
    if (features.D) {
        window.DotMatrixFont.renderString(
            ctx, features.D, positions.D.x, positions.D.y, color, alpha, CHAR_SPACING
        );
    }
    
    // Draw vector if present (with constraint checking to avoid crossing features)
    if (track.heading !== undefined && track.speed) {
        drawVector(ctx, centerX, centerY, track.heading, track.speed, color, alpha, positions, features);
    }
}

/**
 * Draw E feature (central point marker)
 * Small cross or dot marking aircraft position
 */
function drawEFeature(ctx, x, y, color, alpha) {
    ctx.save();
    ctx.strokeStyle = color.replace(/[\d.]+\)$/, ` ${alpha})`);
    ctx.lineWidth = 2;
    
    // Draw small cross
    const size = 4;
    ctx.beginPath();
    ctx.moveTo(x - size, y);
    ctx.lineTo(x + size, y);
    ctx.moveTo(x, y - size);
    ctx.lineTo(x, y + size);
    ctx.stroke();
    
    // Add glow for bright display
    if (alpha > 0.8) {
        ctx.strokeStyle = color.replace(/[\d.]+\)$/, ` ${alpha * 0.4})`);
        ctx.lineWidth = 4;
        ctx.stroke();
    }
    
    ctx.restore();
}

/**
 * Calculate positions for all features based on position mode
 * Returns {A: {x,y}, B: {x,y}, C: {x,y}, D: {x,y}}
 */
function calculateFeaturePositions(centerX, centerY, features, positionMode, charDims) {
    const positions = {};
    const featureHeight = charDims.height + FEATURE_SPACING;
    const margin = 12;  // Distance from E feature to start of format
    
    switch (positionMode) {
        case POSITION_MODES.RIGHT:
            // Format to right: E | A
            //                    | B
            //                    | D
            //                    | C
            positions.A = { x: centerX + margin, y: centerY - featureHeight * 1.5 };
            positions.B = { x: centerX + margin, y: centerY - featureHeight * 0.5 };
            positions.D = { x: centerX + margin, y: centerY + featureHeight * 0.5 };
            positions.C = { x: centerX + margin, y: centerY + featureHeight * 1.5 };
            break;
            
        case POSITION_MODES.LEFT:
            // Format to left: A | E
            //                 B |
            //                 D |
            //                 C |
            const maxWidth = Math.max(
                features.A ? window.DotMatrixFont.getStringWidth(features.A, CHAR_SPACING) : 0,
                features.B ? window.DotMatrixFont.getStringWidth(features.B, CHAR_SPACING) : 0,
                features.C ? window.DotMatrixFont.getStringWidth(features.C, CHAR_SPACING) : 0,
                features.D ? window.DotMatrixFont.getStringWidth(features.D, CHAR_SPACING) : 0
            );
            positions.A = { x: centerX - margin - maxWidth, y: centerY - featureHeight * 1.5 };
            positions.B = { x: centerX - margin - maxWidth, y: centerY - featureHeight * 0.5 };
            positions.D = { x: centerX - margin - maxWidth, y: centerY + featureHeight * 0.5 };
            positions.C = { x: centerX - margin - maxWidth, y: centerY + featureHeight * 1.5 };
            break;
            
        case POSITION_MODES.ABOVE:
            // Format above: A B D
            //               C
            //               E
            const aWidth = features.A ? window.DotMatrixFont.getStringWidth(features.A, CHAR_SPACING) : 0;
            positions.A = { x: centerX - aWidth / 2, y: centerY - margin - featureHeight * 2 };
            positions.B = { x: centerX - aWidth / 2, y: centerY - margin - featureHeight };
            positions.D = { x: centerX - aWidth / 2, y: centerY - margin - featureHeight };
            positions.C = { x: centerX - aWidth / 2, y: centerY - margin };
            break;
            
        case POSITION_MODES.BELOW:
            // Format below: E
            //               A
            //               B D
            //               C
            const bWidth = features.B ? window.DotMatrixFont.getStringWidth(features.B, CHAR_SPACING) : 0;
            positions.A = { x: centerX - bWidth / 2, y: centerY + margin };
            positions.B = { x: centerX - bWidth / 2, y: centerY + margin + featureHeight };
            positions.D = { x: centerX - bWidth / 2, y: centerY + margin + featureHeight };
            positions.C = { x: centerX - bWidth / 2, y: centerY + margin + featureHeight * 2 };
            break;
    }
    
    return positions;
}

/**
 * Calculate bounding box for a feature string
 * Returns {x1, y1, x2, y2} representing top-left and bottom-right corners
 */
function getFeatureBoundingBox(featureText, x, y) {
    if (!featureText || featureText.trim() === '') {
        return null;
    }
    
    const charDims = window.DotMatrixFont.getCharDimensions();
    const width = window.DotMatrixFont.getStringWidth(featureText, CHAR_SPACING);
    const height = charDims.height;
    
    // Add small margin for safety
    const margin = 2;
    
    return {
        x1: x - margin,
        y1: y - margin,
        x2: x + width + margin,
        y2: y + height + margin
    };
}

/**
 * Check if a line segment intersects with a bounding box
 * Line defined by (x1, y1) to (x2, y2)
 * Box defined by {x1, y1, x2, y2}
 */
function lineIntersectsBox(lineX1, lineY1, lineX2, lineY2, box) {
    if (!box) return false;
    
    // Check if either endpoint is inside the box
    if ((lineX1 >= box.x1 && lineX1 <= box.x2 && lineY1 >= box.y1 && lineY1 <= box.y2) ||
        (lineX2 >= box.x1 && lineX2 <= box.x2 && lineY2 >= box.y1 && lineY2 <= box.y2)) {
        return true;
    }
    
    // Check intersection with each edge of the box using parametric line equations
    // This is a simplified check - more robust algorithms exist but this is sufficient
    
    // Check if line crosses any of the four box edges
    const edges = [
        {x1: box.x1, y1: box.y1, x2: box.x2, y2: box.y1}, // Top
        {x1: box.x2, y1: box.y1, x2: box.x2, y2: box.y2}, // Right
        {x1: box.x1, y1: box.y2, x2: box.x2, y2: box.y2}, // Bottom
        {x1: box.x1, y1: box.y1, x2: box.x1, y2: box.y2}  // Left
    ];
    
    for (const edge of edges) {
        if (lineSegmentsIntersect(lineX1, lineY1, lineX2, lineY2, 
                                  edge.x1, edge.y1, edge.x2, edge.y2)) {
            return true;
        }
    }
    
    return false;
}

/**
 * Check if two line segments intersect
 * Based on parametric line equation
 */
function lineSegmentsIntersect(x1, y1, x2, y2, x3, y3, x4, y4) {
    const denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1);
    
    if (denom === 0) {
        return false; // Lines are parallel
    }
    
    const ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom;
    const ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom;
    
    return ua >= 0 && ua <= 1 && ub >= 0 && ub <= 1;
}

/**
 * Find the maximum safe vector length that doesn't intersect features
 * Returns adjusted length (may be shorter than requested)
 */
function constrainVectorLength(centerX, centerY, angleRad, maxLength, featurePositions, features) {
    // Build list of feature bounding boxes
    const boxes = [];
    
    if (features.A && featurePositions.A) {
        boxes.push(getFeatureBoundingBox(features.A, featurePositions.A.x, featurePositions.A.y));
    }
    if (features.B && featurePositions.B) {
        boxes.push(getFeatureBoundingBox(features.B, featurePositions.B.x, featurePositions.B.y));
    }
    if (features.C && featurePositions.C) {
        boxes.push(getFeatureBoundingBox(features.C, featurePositions.C.x, featurePositions.C.y));
    }
    if (features.D && featurePositions.D) {
        boxes.push(getFeatureBoundingBox(features.D, featurePositions.D.x, featurePositions.D.y));
    }
    
    // Remove null boxes
    const validBoxes = boxes.filter(box => box !== null);
    
    if (validBoxes.length === 0) {
        return maxLength; // No features to avoid
    }
    
    // Binary search for maximum safe length
    let safeLength = maxLength;
    const step = 5; // Check every 5 pixels
    
    for (let len = step; len <= maxLength; len += step) {
        const endX = centerX + len * Math.cos(angleRad);
        const endY = centerY + len * Math.sin(angleRad);
        
        // Check if this length intersects any feature
        let intersects = false;
        for (const box of validBoxes) {
            if (lineIntersectsBox(centerX, centerY, endX, endY, box)) {
                intersects = true;
                break;
            }
        }
        
        if (intersects) {
            // Found intersection, return previous safe length
            safeLength = len - step;
            break;
        }
        
        safeLength = len;
    }
    
    // Ensure minimum length for visibility
    return Math.max(VECTOR_MIN_LENGTH, safeLength);
}

/**
 * Draw direction/speed vector from E feature
 * Vector constrained to not cross character features (authentic SAGE hardware limitation)
 * Priority 8 Task 5: Vector rendering with intersection constraints
 * 
 * @param {number} heading - Heading in degrees (0=North, 90=East, 180=South, 270=West)
 * @param {number} speed - Speed in knots
 * @param {object} features - Feature strings {A, B, C, D}
 */
function drawVector(ctx, centerX, centerY, heading, speed, color, alpha, featurePositions, features) {
    // Calculate desired vector length based on speed
    let requestedLength = speed * VECTOR_LENGTH_SCALE;
    requestedLength = Math.max(VECTOR_MIN_LENGTH, Math.min(VECTOR_MAX_LENGTH, requestedLength));
    
    // Convert heading to radians (0° = North = -90° in canvas coords)
    const angleRad = ((heading - 90) * Math.PI) / 180;
    
    // Constrain vector to not cross feature bounding boxes
    const safeLength = constrainVectorLength(
        centerX, centerY, angleRad, requestedLength, featurePositions, features
    );
    
    // Calculate constrained end point
    const endX = centerX + safeLength * Math.cos(angleRad);
    const endY = centerY + safeLength * Math.sin(angleRad);
    
    ctx.save();
    ctx.strokeStyle = color.replace(/[\d.]+\)$/, ` ${alpha})`);
    ctx.lineWidth = 1.5;
    
    // Draw vector line
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(endX, endY);
    ctx.stroke();
    
    // Draw arrowhead
    const arrowSize = 5;
    const arrowAngle = Math.PI / 6;  // 30 degrees
    
    ctx.beginPath();
    ctx.moveTo(endX, endY);
    ctx.lineTo(
        endX - arrowSize * Math.cos(angleRad - arrowAngle),
        endY - arrowSize * Math.sin(angleRad - arrowAngle)
    );
    ctx.moveTo(endX, endY);
    ctx.lineTo(
        endX - arrowSize * Math.cos(angleRad + arrowAngle),
        endY - arrowSize * Math.sin(angleRad + arrowAngle)
    );
    ctx.stroke();
    
    ctx.restore();
}

/**
 * Determine best position mode to avoid clutter
 * @param {number} x - Track X position (normalized 0-1)
 * @param {number} y - Track Y position (normalized 0-1)
 * @param {array} nearbyTracks - Other tracks to avoid
 * @returns {number} Position mode (0-3)
 */
function calculateBestPositionMode(x, y, nearbyTracks = []) {
    // Simple heuristic: use screen quadrant
    // Top-left quadrant: format to right/below
    // Top-right quadrant: format to left/below
    // Bottom-left quadrant: format to right/above
    // Bottom-right quadrant: format to left/above
    
    if (x < 0.5 && y < 0.5) {
        // Top-left
        return POSITION_MODES.RIGHT;
    } else if (x >= 0.5 && y < 0.5) {
        // Top-right
        return POSITION_MODES.LEFT;
    } else if (x < 0.5 && y >= 0.5) {
        // Bottom-left
        return POSITION_MODES.RIGHT;
    } else {
        // Bottom-right
        return POSITION_MODES.LEFT;
    }
}

/**
 * Create track data structure with features
 * @param {object} trackData - Raw track data
 * @returns {object} Track with formatted features
 */
function formatTrackForDisplay(trackData) {
    return {
        id: trackData.id,
        x: trackData.x,
        y: trackData.y,
        heading: trackData.heading,
        speed: trackData.speed,
        positionMode: calculateBestPositionMode(trackData.x, trackData.y),
        features: {
            A: generateFeatureA(trackData),  // Track ID
            B: generateFeatureB(trackData),  // Altitude/Speed
            C: generateFeatureC(trackData),  // Classification
            D: generateFeatureD(trackData)   // Additional data
        }
    };
}

/**
 * Generate Feature A: Track identification
 * Format: 4 characters (letters/numbers)
 */
function generateFeatureA(track) {
    // Use track ID, pad or truncate to 4 chars
    const id = track.id || 'UNK';
    return id.substring(0, 4).padEnd(4, ' ');
}

/**
 * Generate Feature B: Altitude and speed data
 * Format: 4 characters
 */
function generateFeatureB(track) {
    // Altitude in thousands of feet (2 chars) + speed category (2 chars)
    const altThousands = Math.floor((track.altitude || 0) / 1000);
    const altStr = String(altThousands).padStart(2, ' ').substring(0, 2);
    
    // Speed category: SL (slow), MD (medium), FS (fast), SS (supersonic)
    const speed = track.speed || 0;
    let speedCat = '  ';
    if (speed < 300) speedCat = 'SL';
    else if (speed < 600) speedCat = 'MD';
    else if (speed < 800) speedCat = 'FS';
    else speedCat = 'SS';
    
    return altStr + speedCat;
}

/**
 * Generate Feature C: Classification and threat data
 * Format: 4 characters
 */
function generateFeatureC(track) {
    // Track type (2 chars) + threat level (2 chars)
    let typeStr = '  ';
    const type = track.track_type || 'unknown';
    
    if (type === 'friendly') typeStr = 'FR';
    else if (type === 'hostile') typeStr = 'HS';
    else if (type === 'unknown') typeStr = 'UN';
    else if (type === 'missile') typeStr = 'MS';
    else if (type === 'bomber') typeStr = 'BM';
    else if (type === 'fighter') typeStr = 'FT';
    
    // Threat level: L (low), M (medium), H (high), C (critical)
    let threatStr = '  ';
    if (type === 'hostile' || type === 'bomber') threatStr = ' H';
    else if (type === 'missile') threatStr = ' C';
    else if (type === 'unknown') threatStr = ' M';
    else threatStr = ' L';
    
    return typeStr + threatStr;
}

/**
 * Generate Feature D: Additional metadata
 * Format: 2 characters (+2 from A feature per spec)
 */
function generateFeatureD(track) {
    // Heading quadrant: N, NE, E, SE, S, SW, W, NW
    const heading = track.heading || 0;
    let headingStr = ' ';
    
    if (heading >= 337.5 || heading < 22.5) headingStr = 'N';
    else if (heading >= 22.5 && heading < 67.5) headingStr = 'NE';
    else if (heading >= 67.5 && heading < 112.5) headingStr = 'E';
    else if (heading >= 112.5 && heading < 157.5) headingStr = 'SE';
    else if (heading >= 157.5 && heading < 202.5) headingStr = 'S';
    else if (heading >= 202.5 && heading < 247.5) headingStr = 'SW';
    else if (heading >= 247.5 && heading < 292.5) headingStr = 'W';
    else if (heading >= 292.5 && heading < 337.5) headingStr = 'NW';
    
    return headingStr + ' ';
}

// Expose to window
window.TabularTrackDisplay = {
    renderTrack: renderTabularTrack,
    formatTrackForDisplay: formatTrackForDisplay,
    calculateBestPositionMode: calculateBestPositionMode,
    POSITION_MODES,
    FEATURE_SPACING,
    CHAR_SPACING
};

console.log('[Tabular Track] Tabular track display system loaded (5-feature format)');
