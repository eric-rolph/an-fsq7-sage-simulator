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
    
    // Draw vector if present
    if (track.heading !== undefined && track.speed) {
        drawVector(ctx, centerX, centerY, track.heading, track.speed, color, alpha, positions);
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
 * Draw direction/speed vector from E feature
 * Vector cannot cross character features (constrained by SAGE hardware)
 * @param {number} heading - Heading in degrees (0=North, 90=East, 180=South, 270=West)
 * @param {number} speed - Speed in knots
 */
function drawVector(ctx, centerX, centerY, heading, speed, color, alpha, featurePositions) {
    // Calculate vector length based on speed
    let length = speed * VECTOR_LENGTH_SCALE;
    length = Math.max(VECTOR_MIN_LENGTH, Math.min(VECTOR_MAX_LENGTH, length));
    
    // Convert heading to radians (0° = North = -90° in canvas coords)
    const angleRad = ((heading - 90) * Math.PI) / 180;
    
    // Calculate end point
    let endX = centerX + length * Math.cos(angleRad);
    let endY = centerY + length * Math.sin(angleRad);
    
    // TODO: Implement constraint to prevent crossing character features
    // For now, just draw the vector
    
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
