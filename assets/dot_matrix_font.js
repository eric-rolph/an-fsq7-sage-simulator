// SAGE Character Matrix Font System
// Authentic 5x7 dot-matrix characters for CRT display
// Based on C702-416L-ST Situation Display Generator Element Manual

/**
 * 5x7 Dot Matrix Character Patterns
 * Each character is a 5-column by 7-row grid
 * 1 = dot illuminated, 0 = dark
 * Characters formed by electron beam passing through aperture mask
 */

const CHAR_WIDTH = 5;
const CHAR_HEIGHT = 7;
const DOT_SIZE = 2;  // Pixel radius for each dot
const DOT_SPACING = 1;  // Space between dots

// Character patterns stored as arrays of 7 rows (top to bottom)
// Each row is a 5-bit value (rightmost bit = leftmost column)
const CHAR_PATTERNS = {
    // Letters A-Z
    'A': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10001,  // #...#
        0b11111,  // #####
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001   // #...#
    ],
    'B': [
        0b11110,  // ####.
        0b10001,  // #...#
        0b10001,  // #...#
        0b11110,  // ####.
        0b10001,  // #...#
        0b10001,  // #...#
        0b11110   // ####.
    ],
    'C': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10000,  // #....
        0b10000,  // #....
        0b10000,  // #....
        0b10001,  // #...#
        0b01110   // .###.
    ],
    'D': [
        0b11110,  // ####.
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b11110   // ####.
    ],
    'E': [
        0b11111,  // #####
        0b10000,  // #....
        0b10000,  // #....
        0b11110,  // ####.
        0b10000,  // #....
        0b10000,  // #....
        0b11111   // #####
    ],
    'F': [
        0b11111,  // #####
        0b10000,  // #....
        0b10000,  // #....
        0b11110,  // ####.
        0b10000,  // #....
        0b10000,  // #....
        0b10000   // #....
    ],
    'G': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10000,  // #....
        0b10111,  // #.###
        0b10001,  // #...#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    'H': [
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b11111,  // #####
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001   // #...#
    ],
    'I': [
        0b01110,  // .###.
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b01110   // .###.
    ],
    'J': [
        0b00111,  // ..###
        0b00010,  // ...#.
        0b00010,  // ...#.
        0b00010,  // ...#.
        0b00010,  // ...#.
        0b10010,  // #..#.
        0b01100   // .##..
    ],
    'K': [
        0b10001,  // #...#
        0b10010,  // #..#.
        0b10100,  // #.#..
        0b11000,  // ##...
        0b10100,  // #.#..
        0b10010,  // #..#.
        0b10001   // #...#
    ],
    'L': [
        0b10000,  // #....
        0b10000,  // #....
        0b10000,  // #....
        0b10000,  // #....
        0b10000,  // #....
        0b10000,  // #....
        0b11111   // #####
    ],
    'M': [
        0b10001,  // #...#
        0b11011,  // ##.##
        0b10101,  // #.#.#
        0b10101,  // #.#.#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001   // #...#
    ],
    'N': [
        0b10001,  // #...#
        0b11001,  // ##..#
        0b10101,  // #.#.#
        0b10011,  // #..##
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001   // #...#
    ],
    'O': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    'P': [
        0b11110,  // ####.
        0b10001,  // #...#
        0b10001,  // #...#
        0b11110,  // ####.
        0b10000,  // #....
        0b10000,  // #....
        0b10000   // #....
    ],
    'Q': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10101,  // #.#.#
        0b10010,  // #..#.
        0b01101   // .##.#
    ],
    'R': [
        0b11110,  // ####.
        0b10001,  // #...#
        0b10001,  // #...#
        0b11110,  // ####.
        0b10100,  // #.#..
        0b10010,  // #..#.
        0b10001   // #...#
    ],
    'S': [
        0b01111,  // .####
        0b10000,  // #....
        0b10000,  // #....
        0b01110,  // .###.
        0b00001,  // ....#
        0b00001,  // ....#
        0b11110   // ####.
    ],
    'T': [
        0b11111,  // #####
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100   // ..#..
    ],
    'U': [
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    'V': [
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b01010,  // .#.#.
        0b00100   // ..#..
    ],
    'W': [
        0b10001,  // #...#
        0b10001,  // #...#
        0b10001,  // #...#
        0b10101,  // #.#.#
        0b10101,  // #.#.#
        0b11011,  // ##.##
        0b10001   // #...#
    ],
    'X': [
        0b10001,  // #...#
        0b10001,  // #...#
        0b01010,  // .#.#.
        0b00100,  // ..#..
        0b01010,  // .#.#.
        0b10001,  // #...#
        0b10001   // #...#
    ],
    'Y': [
        0b10001,  // #...#
        0b10001,  // #...#
        0b01010,  // .#.#.
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100   // ..#..
    ],
    'Z': [
        0b11111,  // #####
        0b00001,  // ....#
        0b00010,  // ...#.
        0b00100,  // ..#..
        0b01000,  // .#...
        0b10000,  // #....
        0b11111   // #####
    ],
    
    // Numbers 0-9
    '0': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10011,  // #..##
        0b10101,  // #.#.#
        0b11001,  // ##..#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    '1': [
        0b00100,  // ..#..
        0b01100,  // .##..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b00100,  // ..#..
        0b01110   // .###.
    ],
    '2': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b00001,  // ....#
        0b00010,  // ...#.
        0b00100,  // ..#..
        0b01000,  // .#...
        0b11111   // #####
    ],
    '3': [
        0b11111,  // #####
        0b00010,  // ...#.
        0b00100,  // ..#..
        0b00010,  // ...#.
        0b00001,  // ....#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    '4': [
        0b00010,  // ...#.
        0b00110,  // ..##.
        0b01010,  // .#.#.
        0b10010,  // #..#.
        0b11111,  // #####
        0b00010,  // ...#.
        0b00010   // ...#.
    ],
    '5': [
        0b11111,  // #####
        0b10000,  // #....
        0b11110,  // ####.
        0b00001,  // ....#
        0b00001,  // ....#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    '6': [
        0b00110,  // ..##.
        0b01000,  // .#...
        0b10000,  // #....
        0b11110,  // ####.
        0b10001,  // #...#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    '7': [
        0b11111,  // #####
        0b00001,  // ....#
        0b00010,  // ...#.
        0b00100,  // ..#..
        0b01000,  // .#...
        0b01000,  // .#...
        0b01000   // .#...
    ],
    '8': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10001,  // #...#
        0b01110,  // .###.
        0b10001,  // #...#
        0b10001,  // #...#
        0b01110   // .###.
    ],
    '9': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b10001,  // #...#
        0b01111,  // .####
        0b00001,  // ....#
        0b00010,  // ...#.
        0b01100   // .##..
    ],
    
    // Special characters
    ' ': [
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b00000   // .....
    ],
    '.': [
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b01100,  // .##..
        0b01100   // .##..
    ],
    '?': [
        0b01110,  // .###.
        0b10001,  // #...#
        0b00001,  // ....#
        0b00010,  // ...#.
        0b00100,  // ..#..
        0b00000,  // .....
        0b00100   // ..#..
    ],
    '-': [
        0b00000,  // .....
        0b00000,  // .....
        0b00000,  // .....
        0b11111,  // #####
        0b00000,  // .....
        0b00000,  // .....
        0b00000   // .....
    ],
    '/': [
        0b00001,  // ....#
        0b00001,  // ....#
        0b00010,  // ...#.
        0b00100,  // ..#..
        0b01000,  // .#...
        0b10000,  // #....
        0b10000   // #....
    ]
};

/**
 * Render a single character as dot-matrix on canvas
 * @param {CanvasRenderingContext2D} ctx - Canvas context
 * @param {string} char - Character to render (single char)
 * @param {number} x - X position (top-left of character box)
 * @param {number} y - Y position (top-left of character box)
 * @param {string} color - Dot color (e.g., 'rgba(0, 255, 100, 1.0)')
 * @param {number} alpha - Overall alpha multiplier (0.0-1.0)
 */
function renderDotMatrixChar(ctx, char, x, y, color = 'rgba(0, 255, 100, 1.0)', alpha = 1.0) {
    const pattern = CHAR_PATTERNS[char.toUpperCase()];
    if (!pattern) {
        console.warn(`[Character Matrix] Unknown character: '${char}'`);
        return;
    }
    
    const dotSpacing = DOT_SIZE * 2 + DOT_SPACING;
    
    // Draw each row
    for (let row = 0; row < CHAR_HEIGHT; row++) {
        const rowBits = pattern[row];
        
        // Draw each column (right to left in bit order)
        for (let col = 0; col < CHAR_WIDTH; col++) {
            const bitMask = 1 << col;
            if (rowBits & bitMask) {
                // Dot is illuminated
                const dotX = x + (CHAR_WIDTH - 1 - col) * dotSpacing;
                const dotY = y + row * dotSpacing;
                
                ctx.fillStyle = color.replace(/[\d.]+\)$/,` ${alpha})`);  // Adjust alpha
                ctx.beginPath();
                ctx.arc(dotX, dotY, DOT_SIZE, 0, Math.PI * 2);
                ctx.fill();
                
                // Optional: Add slight glow for CRT effect
                if (alpha > 0.8) {
                    ctx.fillStyle = color.replace(/[\d.]+\)$/, ` ${alpha * 0.3})`);
                    ctx.beginPath();
                    ctx.arc(dotX, dotY, DOT_SIZE * 1.5, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        }
    }
}

/**
 * Render a string of characters as dot-matrix
 * @param {CanvasRenderingContext2D} ctx - Canvas context
 * @param {string} text - Text to render
 * @param {number} x - X position (left edge)
 * @param {number} y - Y position (top edge)
 * @param {string} color - Dot color
 * @param {number} alpha - Overall alpha multiplier (0.0-1.0)
 * @param {number} spacing - Extra spacing between characters (pixels)
 */
function renderDotMatrixString(ctx, text, x, y, color = 'rgba(0, 255, 100, 1.0)', alpha = 1.0, spacing = 4) {
    const charWidth = CHAR_WIDTH * (DOT_SIZE * 2 + DOT_SPACING);
    let currentX = x;
    
    for (let i = 0; i < text.length; i++) {
        renderDotMatrixChar(ctx, text[i], currentX, y, color, alpha);
        currentX += charWidth + spacing;
    }
}

/**
 * Get the width of a string in pixels
 * @param {string} text - Text to measure
 * @param {number} spacing - Extra spacing between characters
 * @returns {number} Width in pixels
 */
function getDotMatrixStringWidth(text, spacing = 4) {
    const charWidth = CHAR_WIDTH * (DOT_SIZE * 2 + DOT_SPACING);
    return text.length * (charWidth + spacing) - spacing;
}

/**
 * Get character dimensions
 * @returns {object} {width, height} in pixels
 */
function getCharDimensions() {
    return {
        width: CHAR_WIDTH * (DOT_SIZE * 2 + DOT_SPACING),
        height: CHAR_HEIGHT * (DOT_SIZE * 2 + DOT_SPACING)
    };
}

// Expose to window
window.DotMatrixFont = {
    renderChar: renderDotMatrixChar,
    renderString: renderDotMatrixString,
    getStringWidth: getDotMatrixStringWidth,
    getCharDimensions: getCharDimensions,
    CHAR_WIDTH,
    CHAR_HEIGHT,
    DOT_SIZE,
    DOT_SPACING
};

console.log('[Character Matrix] Dot-matrix font system loaded (5x7, A-Z 0-9)');
