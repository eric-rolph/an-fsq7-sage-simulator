# AN/FSQ-7 SAGE Simulator - User Guide

**Version:** 1.0  
**Last Updated:** November 14, 2025  
**For:** Students, History Enthusiasts, Simulation Gamers

---

## 🚀 Quick Start (5 Minutes)

### Installation

1. **Prerequisites:** Python 3.11+, Git
   
2. **Clone the repository:**
   ```powershell
   git clone https://github.com/eric-rolph/an-fsq7-sage-simulator.git
   cd an-fsq7-sage-simulator
   ```

3. **Install UV package manager** (Windows):
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

4. **Start the simulator:**
   ```powershell
   uv run reflex run
   ```

5. **Open browser:** Navigate to http://localhost:3000

**That's it!** The simulator will compile and launch automatically. First startup takes ~30 seconds.

---

## 🎮 Basic Controls

### Essential Keyboard Shortcuts

| Key | Action | Context |
|-----|--------|---------|
| **D** | Arm Light Gun | Select tracks on radar scope |
| **ESC** | Clear Selection | Deselect current target |
| **Shift+I** | System Inspector | Toggle CPU/memory/queue viewer |
| **Space** | Pause/Resume | Simulation control |

### Mouse Controls

- **Left Click (Light Gun Armed):** Select track on radar scope
- **Left Click (Buttons):** Activate controls
- **Scroll Wheel:** Zoom radar scope (if enabled)

---

## 📡 The Radar Scope

### Understanding the Display

The **19" P14 Phosphor CRT** is your primary view of airspace:

- **Purple Flash:** Initial track detection (electron beam hit)
- **Orange Afterglow:** Track persistence (2-3 seconds, historically accurate)
- **Orange Sweep Line:** Rotating radar sweep (60-second rotation)
- **Green Range Rings:** 100/200/300 mile distance markers
- **Green Coastlines:** Geographic reference overlay

### Track Symbology (Shape, Not Color)

Real SAGE used **monochrome symbols** - shape indicates type:

| Symbol | Type | Meaning |
|--------|------|---------|
| ⬤ Circle | Friendly | Allied aircraft, low threat |
| ⬛ Square | Hostile | Enemy bombers/fighters, HIGH threat |
| ◆ Diamond | Unknown | Unidentified aircraft, needs classification |
| ▲ Triangle | Missile | Ballistic or cruise missiles, CRITICAL threat |

**Dashed Outline + "?"** = Uncorrelated track (not yet identified)

---

## 🎯 Using the Light Gun

The **light gun** is SAGE's primary selection tool (historically: photomultiplier tube that detected CRT phosphor).

### Selection Workflow

1. **Press 'D' key** or click **🎯 ARM LIGHT GUN** button
   - Status changes to: "LIGHT GUN ARMED - SELECT TARGET"
   - Crosshair appears over radar scope

2. **Click on a track** (circle, square, diamond, or triangle)
   - Track highlights
   - **TARGET DETAIL** panel populates with:
     - Track ID (e.g., "TRK-042")
     - Position (lat/lon)
     - Altitude (feet)
     - Speed (knots)
     - Heading (degrees)
     - Classification (FRIENDLY/HOSTILE/UNKNOWN)

3. **View track information** in right panel

4. **Press ESC** or click another track to change selection

### Common Issues

❌ **"Light gun not working"**
- Ensure you've pressed 'D' key first (status must show "ARMED")
- Click directly on track symbol, not near it
- If scope is empty, wait for tracks to spawn (scenario dependent)

---

## ✈️ Interceptor Assignment

### The Threat

When **hostile tracks** (squares) or **missiles** (triangles) are detected, you must assign interceptors to neutralize them.

### Assignment Process

1. **Select a hostile track** with light gun
   - Track detail shows threat level (LOW/MEDIUM/HIGH/CRITICAL)

2. **Choose an interceptor** from available aircraft:
   - **F-106 Delta Dart:** Fast (1525 kts), 4x AIM-4 Falcon missiles
   - **F-102 Delta Dagger:** Moderate (825 kts), 6x AIM-4 Falcon missiles
   - **F-89 Scorpion:** Slow (636 kts), 2x MB-1 Genie nuclear rockets

3. **Check interceptor status:**
   - ✅ **READY:** Available for immediate assignment
   - 🔄 **REFUELING:** Not available (wait 2-5 minutes game time)
   - 🎯 **ENGAGED:** Already assigned to target
   - 🔧 **MAINTENANCE:** Under repair

4. **Click "ASSIGN TO TARGET"** button under chosen interceptor

5. **Monitor engagement:**
   - Intercept vector appears on scope (dashed line from base to target)
   - Fuel decreases as aircraft flies
   - Weapons decrease when fired
   - Status updates: FLYING → FIRING → RETURNING

### Tactical Tips

💡 **Prioritize threats:**
- **CRITICAL** (missiles) → Assign fastest interceptor (F-106)
- **HIGH** (bombers near cities) → Assign any available aircraft
- **MEDIUM/LOW** → Can wait if interceptors are scarce

💡 **Fuel management:**
- Interceptors auto-return at 20% fuel
- Keep one interceptor in reserve for emergencies
- Refueling takes 2-5 minutes (real-time at 1x speed)

💡 **Weapon loadouts:**
- AIM-4 Falcon: Air-to-air missiles (conventional)
- MB-1 Genie: Nuclear-tipped rocket (1.5kt yield, 1000ft blast radius)

---

## 📊 Scenarios & Objectives

### Available Scenarios

1. **Demo 1 - Three Inbound** (Beginner)
   - 3 unknown tracks approach coastline
   - Learn: Detection, correlation, classification
   - Time: 5 minutes

2. **Demo 2 - Bomber Stream** (Intermediate)
   - 5 hostile bombers in formation
   - Learn: Multi-target management, prioritization
   - Time: 8 minutes

3. **Demo 3 - Mixed Threat** (Intermediate)
   - 2 bombers + 3 fighters + 1 unknown
   - Learn: Threat assessment, interceptor allocation
   - Time: 10 minutes

4. **Demo 4 - Missile Attack** (Advanced)
   - 3 ballistic missiles + 2 decoys
   - Learn: Rapid response, critical decision-making
   - Time: 3 minutes

5. **Demo 5 - Coordinated Strike** (Advanced)
   - 4 bombers + 6 fighters + 2 missiles
   - Learn: Large-scale air battle coordination
   - Time: 15 minutes

6. **Demo 6 - Night Defense** (Expert)
   - 10+ mixed threats, limited interceptors
   - Learn: Resource management, triage
   - Time: 20 minutes

7. **Demo 7 - Equipment Failure** (Expert)
   - Normal scenario + vacuum tube degradation
   - Learn: System maintenance under pressure
   - Time: 12 minutes

### Mission Grading

Your performance is graded **A-F** based on:

| Metric | Weight | Calculation |
|--------|--------|-------------|
| **Track Detection** | 25% | Detected tracks / Total tracks |
| **Classification Accuracy** | 25% | Correct classifications / Total tracks |
| **Intercept Success** | 30% | Successful intercepts / High threats |
| **Mission Duration** | 20% | Time to complete objectives |

**Grade Scale:**
- **A (90-100):** Excellent - All objectives met efficiently
- **B (80-89):** Good - Minor mistakes, objectives mostly complete
- **C (70-79):** Satisfactory - Some objectives missed
- **D (60-69):** Poor - Major mistakes, slow response
- **F (0-59):** Fail - Critical failures, incomplete objectives

### Learning Moments

After each mission, review **Learning Moments** (⚠️ icons):
- Explains what went wrong
- Provides tactical tips
- Suggests better approaches

💡 **Example:** "Incomplete Intercept Assignment - Only 1 of 2 available interceptors were assigned. Tip: Always assign interceptors to all HIGH and CRITICAL threats."

---

## 🎛️ SD Console Controls

### Category Select (S1-S13)

Filter radar display by track characteristics:

| Button | Filter | Shows |
|--------|--------|-------|
| S1 ALL | All tracks | Everything |
| S2 FRIENDLY | Classification | Green circles only |
| S3 UNKNOWN | Classification | Yellow diamonds only |
| S4 HOSTILE | Classification | Red squares only |
| S5 MISSILE | Type | Orange triangles only |
| S6 BOMBER | Subtype | Heavy aircraft |
| S7 FIGHTER | Subtype | Fast aircraft |
| S8 ALT<10K | Altitude | Low-altitude tracks |
| S9 ALT 10K-30K | Altitude | Medium-altitude tracks |
| S10 ALT>30K | Altitude | High-altitude tracks |
| S11 INBOUND | Direction | Approaching coast |
| S12 OUTBOUND | Direction | Leaving coast |
| S13 LOITERING | Behavior | Circling/hovering |

**Tip:** Use **S4 HOSTILE** + **S11 INBOUND** to focus on threats.

### Feature Select (S20-S24)

Toggle display overlays:

| Button | Overlay | Purpose |
|--------|---------|---------|
| S20 FLIGHT PATHS | Track history | See where tracks have been (30s trail) |
| S21 INTERCEPTS | Intercept vectors | Show interceptor routes to targets |
| S22 RANGE RINGS | Distance markers | 100/200/300 mile circles |
| S23 CALLSIGNS | Track IDs | Text labels for each track |
| S24 COASTLINES | Geography | North American coastline overlay |

**Recommended Settings:**
- **Beginner:** S22 (Range Rings) + S24 (Coastlines) + S23 (Callsigns)
- **Expert:** S20 (Flight Paths) + S21 (Intercepts) only (less clutter)

### Off-Centering Controls

Pan/zoom/rotate the radar view:

**Pan View:**
- ↑ ← ⊙ → ↓ buttons
- ⊙ = Reset to centered

**Zoom:**
- **−** Zoom out (show more area)
- **+** Zoom in (show detail)
- **FIT** Auto-scale to show all tracks

**Rotate:**
- **↶** Rotate counter-clockwise
- **N** Reset to north-up orientation
- **↷** Rotate clockwise

**Tip:** Use **FIT** button when tracks disappear off-screen.

### Scope Brightness

Adjust display intensity (simulates CRT brightness control):

- **Slider:** 0-100% brightness
- **DIM:** 30% (historically accurate, hard to see)
- **MED:** 60% (balanced)
- **BRIGHT:** 90% (modern, easier to read)

**Recommended:** Start with **BRIGHT** (90%) until comfortable, then try **MED** (60%) for authenticity.

---

## 🔊 Sound Settings

### Audio Channels

The simulator has **3 independent volume channels**:

1. **AMBIENT** (Default: 30%)
   - Radar sweep whoosh
   - Computer hum
   - Background machinery

2. **EFFECTS** (Default: 70%)
   - Button clicks
   - Light gun selection
   - Menu interactions

3. **ALERTS** (Default: 80%)
   - Hostile detection warning
   - Intercept launch
   - System errors
   - Threat proximity alarms

### Volume Presets

Quick volume configurations:

| Preset | Ambient | Effects | Alerts | Use Case |
|--------|---------|---------|--------|----------|
| **SILENT** | 0% | 0% | 0% | Library, quiet work |
| **SUBTLE** | 10% | 30% | 50% | Background learning |
| **NORMAL** | 30% | 70% | 80% | Default (balanced) |
| **IMMERSIVE** | 50% | 90% | 100% | Full experience |

### Test Sounds

Verify audio setup with test buttons:
- **Radar Ping:** Sweep sound (ambient channel)
- **Button Click:** UI feedback (effects channel)
- **Light Gun:** Selection confirmation (effects channel)
- **Hostile Alert:** Threat warning (alerts channel)
- **Intercept:** Launch notification (alerts channel)
- **Error Tone:** System error (alerts channel)

**Note:** Audio files are not included in repository. Simulator plays silence until you add `.mp3` files to `assets/sounds/` directory.

---

## 🛠️ System Inspector (Shift+I)

Press **Shift+I** to toggle the **System Inspector Overlay** - a deep dive into SAGE's internal state.

### What You'll See

**CPU State:**
- Current instruction pointer
- Accumulator register value
- Index register value
- Queue counters

**Memory Banks:**
- 16 magnetic core banks (4K words each)
- Read/write activity indicators
- Bank selection state

**Drum I/O:**
- Drum rotation position
- Read/write heads active
- Transfer buffers
- Queue lengths

**Queue Inspector:**
- Track processing queue
- Correlation jobs pending
- Intercept calculations queued

### Educational Use

**For Computer Science Students:**
- Observe how drum-buffered I/O works (2.5-second refresh = drum rotation)
- See magnetic core memory access patterns
- Understand queue-based processing
- Watch instruction execution in real-time

**Example Exercise:**
1. Open inspector (Shift+I)
2. Start a complex scenario (Demo 5)
3. Watch queue lengths grow as tracks are detected
4. Observe drum I/O spikes during correlation
5. See memory bank activation patterns

---

## 🌐 Network View

Click **🌐 NETWORK VIEW** button to see the SAGE network:

### 28 Historical Stations

**Station Types:**
- **DEW Line** (Distant Early Warning): Arctic Circle radar sites
- **Mid-Canada Line**: Central Canada radar chain
- **Pinetree Line**: US-Canada border radar network
- **Gap-Filler:** Low-altitude radar stations
- **GCI** (Ground Control Intercept): Air defense coordination centers

### Network Features

- **Coverage Circles:** Radar range visualization (300 mile radius)
- **Station Status:** Operational, degraded, or offline
- **Data Links:** Connections between stations and SAGE centers
- **Track Handoff:** Watch tracks transfer between stations

**Tip:** Notice how tracks become **uncorrelated** when they enter a coverage gap (no radar).

---

## 🧪 Vacuum Tube Maintenance

### System Performance

Monitor overall system health:
- **100%:** OPTIMAL - All systems functioning
- **90-99%:** GOOD - Minor degradation
- **75-89%:** DEGRADED - Noticeable performance loss
- **<75%:** CRITICAL - Major system issues

### Tube Status

The simulator tracks **25,000 vacuum tubes** (historically accurate):

- **OPERATIONAL** (▓): Working normally
- **DEGRADING** (▒): Reduced reliability (replace soon)
- **FAILED** (✗): Non-functional (replace immediately)
- **WARMING UP** (◌): Recently replaced (2-minute warmup)

### Replacing Tubes

1. **Identify failed/degrading tubes** in tube rack (red ✗ or yellow ▒)
2. **Click on tube** to select it
3. **Tube automatically replaced** (simulated technician)
4. **Wait 2 minutes** for warmup period (◌ symbol)
5. **Tube becomes operational** (green ▓)

**Important:** System performance drops as tubes fail. In Expert scenarios, you must maintain tubes while managing threats.

---

## 🎓 Educational Features

### For Computer Science Students (Ada)

**Learn About:**
- **Drum-Buffered I/O:** Why 2.5-second refresh cycle?
- **Magnetic Core Memory:** 64K words, non-volatile storage
- **Vacuum Tube Logic:** 25,000 tubes, MTBF calculations
- **Queue-Based Processing:** Track correlation workflow
- **Real-Time Computing:** Constraints and trade-offs

**Recommended Path:**
1. Start with Demo 1 (Three Inbound)
2. Open System Inspector (Shift+I)
3. Watch CPU/memory/queue activity
4. Read ARCHITECTURE.md for technical details
5. Try Demo 7 (Equipment Failure) to see degradation

### For History Students (Grace)

**Experience:**
- **Cold War Context:** Continental air defense during nuclear threat
- **P14 Phosphor Display:** Purple→orange authentic CRT simulation
- **Blue Room Environment:** Indirect lighting (prevents CRT glare)
- **SAGE Network:** 28 real radar stations across North America
- **Light Gun Technology:** Photomultiplier tube selection system

**Recommended Path:**
1. Start with Demo 2 (Bomber Stream) - authentic threat scenario
2. Enable **IMMERSIVE** sound preset
3. Adjust brightness to **DIM** (30%) for authenticity
4. Open Network View to see station coverage
5. Read HISTORY.md for Cold War background

### For Simulation Gamers (Sam)

**Challenge Yourself:**
- **Grade Goals:** Aim for A (90+) on all scenarios
- **Time Trials:** Complete missions faster than par times
- **Perfect Runs:** 100% on all metrics
- **Expert Scenarios:** Demo 6 (Night Defense) and Demo 7 (Equipment Failure)

**Recommended Path:**
1. Complete Demo 1-3 for basics (aim for B+ grades)
2. Unlock advanced scenarios (Demo 4-5)
3. Try expert scenarios (Demo 6-7)
4. Compare debrief scores with friends
5. Study learning moments to improve

---

## 🐛 Troubleshooting

### Server Won't Start

**Symptoms:** `uv run reflex run` fails or hangs

**Solutions:**
1. Kill zombie Python processes:
   ```powershell
   Get-Process -Name python* | Stop-Process -Force
   ```

2. Clear Reflex cache:
   ```powershell
   Remove-Item -Path .\.reflex -Recurse -Force
   ```

3. Verify imports:
   ```powershell
   uv run python -c "import an_fsq7_simulator.interactive_sage"
   ```

4. Restart server:
   ```powershell
   uv run reflex run
   ```

### Browser Not Connecting

**Symptoms:** "Connection Error" or blank page

**Solutions:**
- Wait 30 seconds for initial compilation
- Hard refresh: **Ctrl+Shift+R** (Windows) or **Cmd+Shift+R** (Mac)
- Check server is running: Look for "App running at: http://localhost:3000/"
- Try different browser (Chrome, Firefox, Edge)

### Radar Scope Empty

**Symptoms:** No tracks visible, scope is blank

**Solutions:**
- Check scenario is running (status should show "RUNNING", not "PAUSED")
- Wait 10-20 seconds for tracks to spawn
- Press **FIT** button to auto-scale view
- Try different scenario (some have delayed spawns)
- Check console (F12) for JavaScript errors

### Light Gun Not Working

**Symptoms:** Clicking on tracks does nothing

**Solutions:**
- Press **D** key to arm light gun (status must show "ARMED")
- Click directly on track symbol (circle/square/diamond/triangle)
- Ensure tracks are visible (not off-screen)
- Try clicking closer to track center
- Check browser console (F12) for errors

### Performance Issues

**Symptoms:** Lag, stuttering, low FPS

**Solutions:**
- Close other browser tabs
- Reduce scenario complexity (try Demo 1 instead of Demo 6)
- Lower brightness slider (less GPU load)
- Disable flight paths overlay (S20 button)
- Check CPU usage in Task Manager

### Sound Not Playing

**Symptoms:** Test sounds are silent

**Expected:** Audio files are NOT included in repository. You must add `.mp3` files to `assets/sounds/` directory for audio to play. The simulator plays silence by default.

**To Add Audio:**
1. Create `assets/sounds/` directory
2. Add `.mp3` files with correct names:
   - `radar_ping.mp3`
   - `button_click.mp3`
   - `light_gun_select.mp3`
   - `hostile_alert.mp3`
   - `intercept_launch.mp3`
   - `error_tone.mp3`
3. Restart server

---

## ⌨️ Complete Keyboard Reference

| Key | Action | Category |
|-----|--------|----------|
| **D** | Arm Light Gun | Selection |
| **ESC** | Clear Selection | Selection |
| **Shift+I** | System Inspector Toggle | Debug |
| **Space** | Pause/Resume Simulation | Simulation |
| **Arrow Keys** | Pan Radar View | Navigation |
| **+/-** | Zoom In/Out | Navigation |
| **N** | Reset North-Up | Navigation |
| **S** + **(1-13)** | Category Select | Filtering |
| **S** + **(20-24)** | Feature Toggle | Overlays |
| **F** | Fit All Tracks | Navigation |
| **R** | Reset View | Navigation |
| **?** | Toggle Help (if implemented) | Help |

---

## 📖 Additional Resources

### Documentation

- **README.md:** Project overview, features, installation
- **ARCHITECTURE.md:** Technical details, system design
- **HISTORY.md:** Cold War context, SAGE background
- **DISPLAY_AUTHENTICITY_PLAN.md:** P14 phosphor implementation details
- **DEVELOPMENT_ROADMAP.md:** Development history, completed priorities
- **MANUAL_TESTING_REPORT.md:** Comprehensive testing results

### Online Resources

- **Ed Thelen SAGE Documentation:** https://ed-thelen.org/SageIntro.html
- **Ullman Dissertation (AN/FSQ-7 Computer):** Primary technical reference
- **Wikipedia - SAGE System:** https://en.wikipedia.org/wiki/Semi-Automatic_Ground_Environment
- **Computer History Museum:** SAGE exhibits and archives

### Community

- **GitHub Issues:** Report bugs, request features
- **GitHub Discussions:** Ask questions, share tips
- **Pull Requests:** Contribute improvements

---

## 🎯 Quick Reference Card

**Print this section for desk reference:**

### Essential Controls
- **D** = Arm Light Gun
- **ESC** = Clear Selection
- **Shift+I** = System Inspector
- **Space** = Pause

### Track Symbols
- ⬤ = Friendly
- ⬛ = Hostile
- ◆ = Unknown
- ▲ = Missile

### Quick Filtering
- **S1** = All Tracks
- **S4** = Hostile Only
- **S11** = Inbound Only

### Recommended Settings (Beginners)
- Brightness: **BRIGHT** (90%)
- Sound: **NORMAL** preset
- Overlays: S22 (Range) + S24 (Coast) + S23 (Labels)
- Scenario: **Demo 1 - Three Inbound**

---

## 💡 Pro Tips

1. **Always arm light gun FIRST** (D key) before clicking tracks
2. **Prioritize CRITICAL threats** (missiles) over HIGH threats (bombers)
3. **Keep one interceptor in reserve** for emergencies
4. **Use FIT button** when tracks disappear off-screen
5. **Read learning moments** after each mission to improve
6. **Start with Demo 1-3** before attempting expert scenarios
7. **Open System Inspector** (Shift+I) to understand internal state
8. **Adjust brightness to BRIGHT** (90%) for easier visibility
9. **Enable S23 (Callsigns)** overlay to track target IDs
10. **Review debrief metrics** to identify weak areas

---

## 🎉 Getting Started Checklist

First-time users should complete this checklist:

- [ ] Install UV package manager
- [ ] Clone repository and start server (`uv run reflex run`)
- [ ] Open browser to http://localhost:3000
- [ ] Complete **Demo 1 - Three Inbound** (aim for B+ grade)
- [ ] Practice light gun selection (D key)
- [ ] Assign your first interceptor
- [ ] Read mission debrief and learning moments
- [ ] Toggle System Inspector (Shift+I) to see internals
- [ ] Open Network View (🌐 button) to see SAGE stations
- [ ] Adjust sound settings to your preference
- [ ] Try **Demo 2 - Bomber Stream** (intermediate scenario)
- [ ] Experiment with S1-S13 category filters
- [ ] Enable/disable overlays (S20-S24)
- [ ] Read HISTORY.md for Cold War context
- [ ] Aim for A grade on Demo 1-3

**Congratulations!** You're now ready to defend North America from Cold War threats. 🚀

---

**Questions?** Check GitHub Issues or create a new discussion. Happy defending! 🛡️
