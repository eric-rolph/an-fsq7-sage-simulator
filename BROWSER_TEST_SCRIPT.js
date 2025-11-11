// ====================================
// SAGE Simulator - Browser Test Script
// ====================================
// Copy-paste this into browser console at http://localhost:3001/
// to test the JavaScript -> Python bridge

console.log("=== SAGE Simulator Test Script ===");

// Step 1: Check if radar scope initialized
if (!window.radarScope) {
    console.error("❌ Radar scope not initialized!");
    console.log("Wait a few seconds and try again, or manually initialize:");
    console.log("window.radarScope = initRadarScope('radar-scope-canvas');");
} else {
    console.log("✅ Radar scope initialized");
}

// Step 2: Check if hidden input exists
const hiddenInput = document.getElementById('radar-track-selector');
if (!hiddenInput) {
    console.error("❌ Hidden input #radar-track-selector not found!");
} else {
    console.log("✅ Hidden input found:", hiddenInput);
}

// Step 3: Check if onTrackClick is wired
if (window.radarScope && window.radarScope.onTrackClick) {
    console.log("✅ onTrackClick callback is wired");
} else {
    console.warn("⚠️ onTrackClick callback not set yet");
}

// Step 4: Load test tracks
console.log("\n=== Loading Test Tracks ===");
const testTracks = [
    { 
        id: 'B-052', 
        track_id: 'B-052', 
        x: 0.375, 
        y: 0.25, 
        altitude: 35000, 
        speed: 450, 
        heading: 180, 
        track_type: 'hostile', 
        threat_level: 'high', 
        selected: false 
    },
    { 
        id: 'F-311', 
        track_id: 'F-311', 
        x: 0.625, 
        y: 0.5, 
        altitude: 28000, 
        speed: 520, 
        heading: 45, 
        track_type: 'friendly', 
        threat_level: 'none', 
        selected: false 
    },
    { 
        id: 'U-099', 
        track_id: 'U-099', 
        x: 0.75, 
        y: 0.375, 
        altitude: 40000, 
        speed: 380, 
        heading: 270, 
        track_type: 'unknown', 
        threat_level: 'medium', 
        selected: false 
    }
];

if (window.radarScope) {
    window.radarScope.updateTracks(testTracks);
    console.log("✅ Loaded 3 test tracks:");
    console.log("  - B-052 (RED hostile bomber) at top");
    console.log("  - F-311 (GREEN friendly transport) at right");
    console.log("  - U-099 (YELLOW unknown) at upper right");
} else {
    console.error("❌ Cannot load tracks - radar not initialized");
}

// Step 5: Test manual bridge trigger
console.log("\n=== Testing JavaScript -> Python Bridge ===");
console.log("Run these commands to test the bridge manually:");
console.log("\n// Test 1: Trigger selection via hidden input");
console.log("const input = document.getElementById('radar-track-selector');");
console.log("input.value = 'F-311';");
console.log("input.dispatchEvent(new Event('change', { bubbles: true }));");

console.log("\n// Test 2: Click on radar track (should auto-trigger)");
console.log("// Just click on the green dot (F-311) on the radar");

console.log("\n// Test 3: Check current selection");
console.log("window.radarScope.tracks.filter(t => t.selected);");

// Step 6: Add helper functions
window.testSelectTrack = function(trackId) {
    console.log(`\n=== Testing track selection: ${trackId} ===`);
    const input = document.getElementById('radar-track-selector');
    if (input) {
        input.value = trackId;
        input.dispatchEvent(new Event('change', { bubbles: true }));
        console.log(`✅ Sent ${trackId} to backend via hidden input`);
    } else {
        console.error("❌ Hidden input not found");
    }
};

window.testClickRadarTrack = function(trackIndex) {
    console.log(`\n=== Simulating click on track ${trackIndex} ===`);
    if (!window.radarScope || !window.radarScope.tracks[trackIndex]) {
        console.error("❌ Track not found");
        return;
    }
    
    const track = window.radarScope.tracks[trackIndex];
    const canvas = document.getElementById('radar-scope-canvas');
    const rect = canvas.getBoundingClientRect();
    
    const clickX = rect.left + (track.x * rect.width);
    const clickY = rect.top + (track.y * rect.height);
    
    const event = new MouseEvent('click', {
        clientX: clickX,
        clientY: clickY,
        bubbles: true
    });
    canvas.dispatchEvent(event);
    
    console.log(`✅ Simulated click on ${track.id} at (${track.x}, ${track.y})`);
};

console.log("\n=== Helper Functions Added ===");
console.log("window.testSelectTrack('F-311')  // Test bridge directly");
console.log("window.testClickRadarTrack(0)    // Click B-052 (index 0)");
console.log("window.testClickRadarTrack(1)    // Click F-311 (index 1)");
console.log("window.testClickRadarTrack(2)    // Click U-099 (index 2)");

console.log("\n=== Test Complete ===");
console.log("Now try clicking the test buttons in the UI or radar dots!");
console.log("Watch for 'Track click sent to backend: [track-id]' in console");
console.log("Track Detail panel should update on the right side");
