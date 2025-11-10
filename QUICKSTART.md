# Quick Start Guide

## Installation (5 minutes)

### Prerequisites
- Python 3.8 or higher installed
- Internet connection for downloading packages

### Steps

1. **Open a terminal in the project directory**

2. **Install Reflex and dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Reflex app**
   ```bash
   reflex init
   ```
   When prompted, press Enter to accept defaults.

4. **Run the simulator**
   ```bash
   reflex run
   ```

5. **Open your browser**
   Navigate to: http://localhost:3000

## First Time Usage

### Starting the System

1. Look for the **Control Panel** on the left side
2. Click the green **POWER ON** button
3. Watch the vacuum tubes warm up (progress bar)
4. Wait for "OPERATIONAL" badge to appear

### Exploring the Display

1. **Display Modes** - Click buttons below the CRT:
   - RADAR - Primary radar scope
   - TACTICAL - Tactical overview
   - STATUS - System diagnostics
   - MEMORY - Memory visualization

2. **Light Gun** - Click on radar targets to select them
   - Selected targets highlight in yellow
   - Target info shows in radar table

3. **Intercept Mode**:
   - Toggle "INTERCEPT MODE" switch
   - Select a target with light gun
   - Click "ASSIGN INTERCEPT" button

### Exploring Controls

- **Manual Override** - Toggle for direct control
- **Display Mode** - Cycle through views
- **Brightness** - Adjust CRT phosphor intensity
- **Console Status** - View operator station count

## Troubleshooting

### "Import reflex could not be resolved"
This is just a linting error. The app will still run. To fix:
```bash
pip install reflex
```

### Port 3000 already in use
```bash
reflex run --port 8000
```

### App won't start
1. Check Python version: `python --version` (need 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Clear cache: `reflex clean`

## Next Steps

- Read `README.md` for full feature documentation
- Check `docs/HISTORY.md` for historical background
- Review `docs/DESIGN.md` for technical details
- See `docs/THOUGHTS.md` for implementation discussion

## Quick Tips

1. **Performance**: Close other tabs if display is slow
2. **Full Screen**: Press F11 for immersive experience
3. **Screenshots**: Use the status display mode for best photos
4. **Learning**: Try different display modes to see all features

Enjoy your journey back to the dawn of interactive computing!
