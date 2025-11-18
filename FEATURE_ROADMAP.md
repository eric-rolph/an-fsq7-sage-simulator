# Feature Development Roadmap

**Last Updated:** November 17, 2025
**Current Status:** Testing Phase Complete - 450 tests, 30% coverage
**Ready For:** New Feature Development

---

## 🎯 Immediate High-Value Features (Week 1-2)

### 1. **Keyboard Shortcuts & Accessibility** 🔥
**Priority:** CRITICAL for usability
**Effort:** Medium (2-3 days)
**Value:** High

**Features:**
- Global keyboard shortcuts (D for light gun, SPACE for quick actions)
- Tab navigation through all interactive elements
- ARIA labels for screen readers
- Focus indicators for all buttons
- Escape key to dismiss panels

**Files to Create/Modify:**
- `an_fsq7_simulator/components_v2/keyboard_shortcuts.py` (NEW)
- Update all components with `aria-label` attributes
- Add focus styles to CSS

**Success Criteria:**
- [ ] Can complete full scenario using only keyboard
- [ ] Screen reader announces all actions
- [ ] Focus indicators visible on all interactive elements
- [ ] Keyboard shortcut help panel (press ?)

---

### 2. **Advanced Scenario Features** 🎮
**Priority:** HIGH for educational value
**Effort:** Medium (3-4 days)
**Value:** High

**Features:**
- **Weather Effects:** Rain clutter, storms affecting radar
- **ECM/Jamming:** Electronic countermeasures reducing track quality
- **Multiple Raid Sizes:** Small/Medium/Large bomber formations
- **Time Pressure:** Limited time to classify tracks before engagement
- **Scoring Bonuses:** Early detection, efficient fuel use, minimal alerts

**Files to Create:**
- `an_fsq7_simulator/sim/weather.py` (NEW)
- `an_fsq7_simulator/sim/ecm.py` (NEW)
- Update `sim/scenario_events.py` with new event types

**Success Criteria:**
- [ ] 3 new scenarios with weather effects
- [ ] ECM reduces track confidence levels
- [ ] Detailed scoring breakdown in debrief
- [ ] Visual weather indicators on radar

---

### 3. **Historical Scenario Pack** 📚
**Priority:** HIGH for educational users
**Effort:** Medium (2-3 days)
**Value:** High

**Features:**
- **Cuban Missile Crisis (1962):** Heightened alert, unknown aircraft
- **Berlin Airlift (1948):** Friendly track management, no hostiles
- **DEW Line Alert (1960s):** Polar approach, limited radar coverage
- **Strategic Air Command Exercise:** Multi-wave coordinated strike

**Files to Modify:**
- `an_fsq7_simulator/sim/scenarios.py`
- Add historical context to debrief panel

**Success Criteria:**
- [ ] 4 new historical scenarios
- [ ] Historical briefing text before each scenario
- [ ] Period-accurate threat assessments
- [ ] Historical outcome comparison in debrief

---

### 4. **Performance Monitoring & Optimization** ⚡
**Priority:** MEDIUM for scalability
**Effort:** Small (1-2 days)
**Value:** Medium

**Features:**
- Track count optimization (support 100+ tracks)
- FPS monitoring overlay (toggle with Shift+P)
- Memory usage profiling
- Canvas rendering optimizations
- Lazy loading for large scenarios

**Files to Create:**
- `an_fsq7_simulator/components_v2/performance_overlay.py` (NEW - actually already exists!)
- Update `assets/crt_radar.js` with optimizations

**Success Criteria:**
- [ ] 60 FPS with 100+ tracks
- [ ] < 2 second scenario load time
- [ ] < 200MB memory usage
- [ ] Performance overlay shows real-time metrics

---

## 🚀 Medium-Term Features (Week 3-4)

### 5. **Multi-Console Co-Op Mode** 👥
**Priority:** MEDIUM for engagement
**Effort:** Large (5-7 days)
**Value:** High

**Features:**
- Multiple browser instances as different operator consoles
- Shared track database
- Division of labor (one identifies, one assigns interceptors)
- Team scoring system
- WebSocket-based real-time sync

**Technical Approach:**
- Use Reflex's built-in WebSocket support
- Shared Redis/database for track state
- Console role assignment (ID Officer, Weapons Director, Supervisor)

**Success Criteria:**
- [ ] 2-3 players can control same scenario
- [ ] Track updates sync in real-time
- [ ] Team score calculated correctly
- [ ] Role-based UI variations

---

### 6. **SAGE Command Language Interpreter** 💻
**Priority:** MEDIUM for authenticity
**Effort:** Large (6-8 days)
**Value:** Medium-High

**Features:**
- Text command interface (like original SAGE)
- Commands: `TRACK 1234`, `ASSIGN F-106 TO 1234`, `LAUNCH INT-01`
- Command history (up/down arrows)
- Auto-completion
- Educational mode explains each command

**Files to Create:**
- `an_fsq7_simulator/components_v2/command_console.py` (NEW)
- `an_fsq7_simulator/sim/command_parser.py` (NEW)

**Success Criteria:**
- [ ] 20+ commands implemented
- [ ] Command help system (type `HELP`)
- [ ] Can complete scenarios using only commands
- [ ] Command history persists across sessions

---

### 7. **Advanced Network Visualization** 🗺️
**Priority:** LOW for current phase
**Effort:** Medium (3-4 days)
**Value:** Medium

**Features:**
- Click stations to see detailed info
- Coverage circle animation
- Station status (online/offline/degraded)
- Data link visualization (blinking lines)
- Sector hand-off simulation

**Files to Modify:**
- `assets/network_visualization.js`
- `an_fsq7_simulator/components_v2/network_stations.py`

**Success Criteria:**
- [ ] Interactive station selection
- [ ] Real-time coverage updates
- [ ] Visual indication of track hand-offs
- [ ] Station failure simulation

---

## 🎨 Polish & Quality (Ongoing)

### 8. **Cross-Browser Testing**
**Priority:** HIGH for accessibility
**Effort:** Small (1 day)

**Browsers to Test:**
- Firefox
- Safari
- Edge
- Mobile Chrome (touch support)

### 9. **Documentation Updates**
**Priority:** MEDIUM
**Effort:** Small (1 day)

**Updates Needed:**
- USER_GUIDE.md with keyboard shortcuts
- Video tutorials (screen recordings)
- Contributing guide for new features
- Architecture diagrams

### 10. **CI/CD Pipeline**
**Priority:** MEDIUM for quality
**Effort:** Small (1 day)

**Setup:**
- GitHub Actions workflow
- Automatic test runs on PR
- Coverage reporting
- Automatic deployment to GitHub Pages

---

## 📊 Feature Prioritization Matrix

| Feature | User Impact | Dev Effort | Priority |
|---------|-------------|------------|----------|
| Keyboard Shortcuts | 🔥🔥�� | Medium | **DO FIRST** |
| Advanced Scenarios | 🔥🔥🔥 | Medium | **DO FIRST** |
| Historical Pack | 🔥🔥 | Medium | **DO SECOND** |
| Performance | 🔥🔥 | Small | **DO SECOND** |
| Multi-Console | 🔥🔥 | Large | **DO THIRD** |
| Command Language | 🔥 | Large | **LATER** |
| Network Viz | 🔥 | Medium | **LATER** |

---

## 🎯 Recommended Next Steps

### Option A: Usability Focus (Recommended)
**Timeline:** 1 week
1. Keyboard shortcuts & accessibility (2 days)
2. Advanced scenario features (3 days)
3. Performance optimizations (1 day)
4. Cross-browser testing (1 day)

**Outcome:** Production-ready for educational use

### Option B: Content Focus
**Timeline:** 1 week
1. Historical scenario pack (3 days)
2. Advanced scenarios (3 days)
3. Documentation updates (1 day)

**Outcome:** Rich educational content library

### Option C: Innovation Focus
**Timeline:** 2 weeks
1. Multi-console co-op mode (1 week)
2. SAGE command language (1 week)

**Outcome:** Unique features not found elsewhere

---

## 🏆 Success Metrics

### Quantitative
- [ ] Load time < 2 seconds
- [ ] 60 FPS with 100+ tracks
- [ ] 100% keyboard accessible
- [ ] 10+ scenarios available
- [ ] WCAG 2.1 AA compliance

### Qualitative
- [ ] Positive user feedback from educators
- [ ] Used in at least 1 CS course
- [ ] GitHub stars > 100
- [ ] Featured on Hacker News / Reddit

---

**Recommendation:** Start with **Option A: Usability Focus** to make the existing feature-complete system production-ready, then proceed to content and innovation features based on user feedback.
