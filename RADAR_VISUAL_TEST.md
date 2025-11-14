# SAGE Radar 60-Second Visual Test
# Manual testing procedure

## Setup
1. Open browser to http://localhost:3000/
2. Open browser DevTools (F12)
3. Go to Console tab

## Test Procedure

### T+0s (Initial Load)
1. Paste this into console:
```javascript
console.log('=== T+0s Initial State ===');
console.log('Canvas:', document.getElementById('radar-scope-canvas') ? 'EXISTS' : 'MISSING');
console.log('CRT Object:', window.crtRadar ? 'EXISTS' : 'MISSING');
if (window.crtRadar) {
    console.log('Sweep Angle:', window.crtRadar.sweepAngle);
    console.log('Persistence Decay:', window.crtRadar.persistenceDecay);
    console.log('Tracks:', window.crtRadar.tracks);
}
```

2. Take screenshot (Windows: Win+Shift+S)
3. Observe:
   - Is the canvas black or showing anything?
   - Are range rings visible?
   - Is the green sweep line visible?
   - Is it animating?

### T+15s (After 15 seconds)
1. Wait 15 seconds
2. Paste this into console:
```javascript
console.log('=== T+15s After 15 Seconds ===');
const canvas = document.getElementById('radar-scope-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    const centerPixel = ctx.getImageData(400, 400, 1, 1).data;
    const topLeftPixel = ctx.getImageData(100, 100, 1, 1).data;
    console.log('Center Pixel RGBA:', Array.from(centerPixel));
    console.log('TopLeft Pixel RGBA:', Array.from(topLeftPixel));
}
if (window.crtRadar) {
    console.log('Sweep Angle:', window.crtRadar.sweepAngle);
    console.log('Animation running:', window.crtRadar.sweepAngle > 0);
}
```

3. Take screenshot
4. Observe:
   - Has the display changed?
   - Is the sweep still rotating?
   - Are phosphor trails visible?

### T+30s (After 30 seconds)
1. Wait another 15 seconds (30s total)
2. Repeat console check:
```javascript
console.log('=== T+30s After 30 Seconds ===');
const sweepAngle1 = window.crtRadar ? window.crtRadar.sweepAngle : 0;
setTimeout(() => {
    const sweepAngle2 = window.crtRadar ? window.crtRadar.sweepAngle : 0;
    console.log('Sweep moved:', (sweepAngle2 - sweepAngle1).toFixed(2), 'degrees');
    console.log('Animation:', sweepAngle2 !== sweepAngle1 ? 'RUNNING' : 'STOPPED');
}, 1000);
```

3. Take screenshot

### T+45s (After 45 seconds)
1. Wait another 15 seconds (45s total)
2. Take screenshot
3. Compare visually with previous screenshots

### T+60s (After 60 seconds)
1. Wait another 15 seconds (60s total)
2. Final console check:
```javascript
console.log('=== T+60s After 60 Seconds ===');
const canvas = document.getElementById('radar-scope-canvas');
const ctx = canvas.getContext('2d');
// Sample multiple points
for (let angle = 0; angle < 360; angle += 90) {
    const rad = angle * Math.PI / 180;
    const x = 400 + Math.cos(rad) * 200;
    const y = 400 + Math.sin(rad) * 200;
    const pixel = ctx.getImageData(x, y, 1, 1).data;
    console.log(`Pixel at ${angle}°:`, Array.from(pixel));
}
```

3. Take final screenshot

## What to Look For

### Expected Behavior (GOOD):
- ✓ Green sweep line continuously rotating
- ✓ Faint green phosphor trail behind sweep (P7 persistence)
- ✓ Range rings visible as faint green circles
- ✓ Sweep angle increasing over time
- ✓ Display remains visible throughout entire 60 seconds
- ✓ No flickering or disappearing elements

### Problem Indicators (BAD):
- ✗ Display goes black after initial flash
- ✗ Sweep line disappears
- ✗ Range rings fade away
- ✗ Canvas becomes completely black
- ✗ Sweep angle stops changing
- ✗ Flickering or strobing effect

## Quick Visual Test
Just watch the display for 60 seconds:
1. Does the green sweep line keep rotating?
2. Can you see a faint green trail behind it?
3. Do the range rings stay visible?
4. Does anything disappear or go black?

## Common Issues

### Issue: "Display goes black immediately"
- Check: `window.crtRadar.persistenceDecay` should be ~0.03
- Check: Console for errors
- Check: Canvas pixel data (should show green values)

### Issue: "Sweep visible but no trails"
- Check: Persistence decay value
- Check: Persistence canvas exists
- Check: drawSweepToPersistence being called

### Issue: "Flickering or strobing"
- Check: Render order (persistence before composite)
- Check: Not clearing canvas after drawing
- Check: Frame rate (should be ~60fps)
