// Radar monitoring script for Node.js with Puppeteer
// Run with: node monitor_radar.js

const puppeteer = require('puppeteer');
const fs = require('fs');

async function monitorRadar() {
    console.log('=== SAGE Radar 60-Second Monitoring Test ===\n');
    
    const browser = await puppeteer.launch({
        headless: false, // Show browser so you can see it
        defaultViewport: { width: 1200, height: 900 }
    });
    
    const page = await browser.newPage();
    
    // Enable console logging from the page
    page.on('console', msg => {
        const text = msg.text();
        if (text.includes('[CRT]')) {
            console.log(`  Browser Console: ${text}`);
        }
    });
    
    console.log('Navigating to http://localhost:3000/...');
    await page.goto('http://localhost:3000/', { waitUntil: 'networkidle2' });
    
    const intervals = [0, 15, 30, 45, 60]; // seconds
    
    for (const interval of intervals) {
        if (interval > 0) {
            console.log(`\nWaiting ${interval - (intervals[intervals.indexOf(interval) - 1] || 0)} seconds...`);
            await new Promise(resolve => setTimeout(resolve, (interval - (intervals[intervals.indexOf(interval) - 1] || 0)) * 1000));
        }
        
        console.log(`\n[T+${interval}s] Capturing radar state...`);
        
        // Check page elements and state
        const state = await page.evaluate(() => {
            const canvas = document.getElementById('radar-scope-canvas');
            const crt = window.crtRadar;
            
            let canvasPixels = null;
            if (canvas) {
                const ctx = canvas.getContext('2d');
                const imageData = ctx.getImageData(400, 400, 1, 1); // Center pixel
                canvasPixels = Array.from(imageData.data);
            }
            
            return {
                canvasExists: !!canvas,
                canvasWidth: canvas ? canvas.width : null,
                canvasHeight: canvas ? canvas.height : null,
                crtExists: !!crt,
                sweepAngle: crt ? crt.sweepAngle : null,
                persistenceDecay: crt ? crt.persistenceDecay : null,
                trackCount: crt && crt.tracks ? crt.tracks.length : 0,
                centerPixel: canvasPixels
            };
        });
        
        console.log(`  Canvas: ${state.canvasExists ? '✓' : '✗'} (${state.canvasWidth}x${state.canvasHeight})`);
        console.log(`  CRT Object: ${state.crtExists ? '✓' : '✗'}`);
        console.log(`  Sweep Angle: ${state.sweepAngle !== null ? state.sweepAngle.toFixed(2) + '°' : 'N/A'}`);
        console.log(`  Persistence Decay: ${state.persistenceDecay !== null ? state.persistenceDecay : 'N/A'}`);
        console.log(`  Track Count: ${state.trackCount}`);
        console.log(`  Center Pixel RGBA: [${state.centerPixel ? state.centerPixel.join(', ') : 'N/A'}]`);
        
        // Take screenshot
        const filename = `radar_screenshot_${interval}s.png`;
        await page.screenshot({
            path: filename,
            clip: {
                x: 0,
                y: 0,
                width: 1200,
                height: 900
            }
        });
        console.log(`  Screenshot saved: ${filename}`);
    }
    
    console.log('\n✓ Monitoring complete!');
    console.log('Check the generated PNG files for visual comparison.');
    
    await browser.close();
}

monitorRadar().catch(console.error);
