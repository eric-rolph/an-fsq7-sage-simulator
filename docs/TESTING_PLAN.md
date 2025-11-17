# SAGE Simulator - Testing Plan

**Status:** Testing infrastructure planned, not yet implemented  
**Priority:** HIGH - Critical for production readiness  
**Created:** November 17, 2025  

---

## 🎯 Testing Strategy Overview

This document outlines the testing infrastructure needed before the SAGE simulator can be considered production-ready. Currently, the project has **no automated tests** - all validation is manual.

---

## 📋 Test Suite Architecture

```
tests/
├── unit/                    # Core logic tests (isolated)
│   ├── test_cpu_core.py
│   ├── test_drum_io.py
│   ├── test_light_gun.py
│   └── test_track_correlation.py
│
├── sim/                     # Simulation tests (integrated)
│   ├── test_scenarios.py
│   ├── test_track_physics.py
│   ├── test_interceptor_logic.py
│   └── test_scenario_events.py
│
├── design_language/         # UI contract tests (invariants)
│   ├── test_mode_free_ui.py
│   ├── test_layout_invariants.py
│   ├── test_p14_monochrome.py
│   └── test_track_symbology.py
│
├── integration/             # End-to-end workflows
│   ├── test_light_gun_workflow.py
│   ├── test_intercept_workflow.py
│   └── test_scenario_debrief.py
│
└── property_based/          # Numerical correctness (hypothesis)
    ├── test_coordinates.py
    ├── test_heading_calculations.py
    └── test_physics_invariants.py
```

---

## 🧪 Unit Tests (tests/unit/)

### test_cpu_core.py

**Purpose:** Verify AN/FSQ-7 CPU core correctness

**Test Cases:**
```python
def test_indexed_addressing():
    """Verify index register addressing modes work correctly"""
    # Set index register to 10
    # Load from base address + index
    # Assert correct memory location accessed

def test_ones_complement_arithmetic():
    """Verify one''s complement addition/subtraction"""
    # Test positive + positive
    # Test positive + negative
    # Test negative + negative
    # Test -0 vs +0 handling

def test_program_execution_array_sum():
    """Verify array sum program executes correctly"""
    # Load array into drum memory
    # Execute array sum program
    # Assert correct sum computed

def test_program_execution_search():
    """Verify search program finds targets"""
    # Load track data into drum
    # Execute search for hostile tracks
    # Assert correct tracks identified
```

### test_drum_io.py

**Purpose:** Verify drum I/O system persistence and retrieval

**Test Cases:**
```python
def test_write_read_track():
    """Verify track data persists to drum and retrieves correctly"""

def test_drum_addressing():
    """Verify drum addressing calculations (module, sector, word)"""

def test_concurrent_access():
    """Verify drum handles multiple simultaneous reads/writes"""
```

### test_light_gun.py

**Purpose:** Verify light gun selection logic

**Test Cases:**
```python
def test_light_gun_arm():
    """Verify ARM state enables light gun"""

def test_light_gun_select_track():
    """Verify click on track selects it when armed"""

def test_light_gun_reject_when_disarmed():
    """Verify click has no effect when disarmed"""

def test_light_gun_canvas_to_world_coords():
    """Verify canvas coordinates map correctly to world space"""
```

### test_track_correlation.py

**Purpose:** Verify track correlation state machine

**Test Cases:**
```python
def test_uncorrelated_to_correlated():
    """Verify track transitions from UNCORRELATED to CORRELATED"""

def test_correlation_requires_classification():
    """Verify track must be classified (FRIENDLY/HOSTILE/UNKNOWN)"""

def test_uncorrelated_track_properties():
    """Verify uncorrelated tracks have ''?'' indicator, dashed outline"""
```

---

## 🎮 Simulation Tests (tests/sim/)

### test_scenarios.py

**Purpose:** Verify all scenarios load and execute

**Test Cases:**
```python
def test_scenario_training():
    """Verify Training scenario initializes correctly"""

def test_scenario_heavy_load():
    """Verify Heavy Load scenario spawns 50+ tracks"""

def test_scenario_wave_attack():
    """Verify Wave Attack spawns tracks in waves"""

def test_scenario_metrics_tracking():
    """Verify performance metrics calculated correctly"""
```

### test_track_physics.py

**Purpose:** Verify track movement and physics

**Test Cases:**
```python
def test_track_position_updates():
    """Verify tracks move based on heading/speed"""

def test_heading_calculations():
    """Verify heading angles compute correctly (0-360°)"""

def test_boundary_wrapping():
    """Verify tracks wrap at display edges"""

def test_altitude_changes():
    """Verify altitude changes apply correctly"""
```

### test_interceptor_logic.py

**Purpose:** Verify interceptor assignment and engagement

**Test Cases:**
```python
def test_assign_interceptor():
    """Verify interceptor assigned to selected track"""

def test_launch_interceptor():
    """Verify interceptor launches and moves toward target"""

def test_intercept_success():
    """Verify successful intercept (distance < threshold)"""

def test_intercept_failure():
    """Verify intercept fails if target too fast/evasive"""
```

### test_scenario_events.py

**Purpose:** Verify dynamic scenario events

**Test Cases:**
```python
def test_new_track_event():
    """Verify NEW_TRACK event spawns track"""

def test_speed_change_event():
    """Verify SPEED_CHANGE modifies track velocity"""

def test_course_change_event():
    """Verify COURSE_CHANGE updates heading"""

def test_system_message_event():
    """Verify SYSTEM_MESSAGE displays in UI"""
```

---

## 🎨 Design Language Tests (tests/design_language/)

### test_mode_free_ui.py

**Purpose:** Verify mode-free UI invariants

**Test Cases:**
```python
def test_buttons_disabled_not_hidden():
    """Verify unavailable buttons are disabled, not removed from DOM"""

def test_launch_button_disabled_when_no_selection():
    """Verify LAUNCH INTERCEPT disabled when no track selected"""

def test_assign_button_disabled_when_no_interceptor():
    """Verify ASSIGN disabled when no interceptors available"""
```

### test_layout_invariants.py

**Purpose:** Verify fixed layout structure

**Test Cases:**
```python
def test_detail_panel_always_right():
    """Verify track detail panel always on right side"""

def test_radar_scope_central():
    """Verify radar scope is central visual focus"""

def test_action_controls_bottom():
    """Verify global action controls in bottom/action region"""
```

### test_p14_monochrome.py

**Purpose:** Verify P14 phosphor monochrome compliance

**Test Cases:**
```python
def test_no_color_coding_in_symbology():
    """Verify tracks do not use color to indicate type"""

def test_all_symbology_orange_phosphor():
    """Verify all symbology uses P14 orange phosphor color"""

def test_shape_indicates_type():
    """Verify track type indicated by SHAPE, not color"""
```

### test_track_symbology.py

**Purpose:** Verify historically accurate track symbols

**Test Cases:**
```python
def test_friendly_circle():
    """Verify friendly tracks use circle symbol"""

def test_hostile_square():
    """Verify hostile tracks use square symbol"""

def test_unknown_diamond():
    """Verify unknown tracks use diamond symbol"""

def test_missile_triangle():
    """Verify missiles use triangle symbol"""

def test_uncorrelated_dashed():
    """Verify uncorrelated tracks use dashed outline with ''?'' indicator"""
```

---

## 🔗 Integration Tests (tests/integration/)

### test_light_gun_workflow.py

**Purpose:** Verify end-to-end light gun workflow

**Test Workflow:**
1. Click ARM LIGHT GUN button
2. Verify button state changes (blue highlight)
3. Click on track in radar scope
4. Verify track selected (detail panel updates)
5. Click CLEAR SELECTION
6. Verify selection cleared

### test_intercept_workflow.py

**Purpose:** Verify end-to-end intercept workflow

**Test Workflow:**
1. Select hostile track with light gun
2. Click ASSIGN INTERCEPTOR
3. Verify interceptor assigned (detail panel shows interceptor)
4. Click LAUNCH INTERCEPT
5. Verify interceptor launches (moves toward target)
6. Wait for intercept completion
7. Verify debrief metrics updated

### test_scenario_debrief.py

**Purpose:** Verify scenario completion and debrief

**Test Workflow:**
1. Start Training scenario
2. Complete all objectives (detect, classify, intercept)
3. Verify scenario completes
4. Verify debrief panel shows metrics
5. Verify performance grade calculated

---

## 🔢 Property-Based Tests (tests/property_based/)

Uses Hypothesis library for generative testing.

### test_coordinates.py

**Purpose:** Verify coordinate transformations are reversible

**Properties:**
```python
@given(st.floats(min_value=0, max_value=1), 
       st.floats(min_value=0, max_value=1))
def test_canvas_to_world_to_canvas(x, y):
    """Verify canvas → world → canvas is identity transform"""
    world = canvas_to_world(x, y)
    canvas = world_to_canvas(world.x, world.y)
    assert abs(canvas.x - x) < 0.001
    assert abs(canvas.y - y) < 0.001
```

### test_heading_calculations.py

**Purpose:** Verify heading math is consistent

**Properties:**
```python
@given(st.floats(min_value=0, max_value=360))
def test_heading_always_in_range(heading):
    """Verify heading normalization keeps angles in [0, 360)"""
    normalized = normalize_heading(heading + 720)  # Add 2 full rotations
    assert 0 <= normalized < 360
```

---

## 🌐 Cross-Browser Testing (Manual)

**Browsers to Test:**
- Chrome (primary development browser)
- Firefox
- Safari (macOS/iOS)
- Edge

**Test Checklist per Browser:**
- [ ] Server loads at http://localhost:3000
- [ ] Radar scope renders (P14 phosphor glow)
- [ ] Tracks move smoothly
- [ ] Light gun selection works (click tracks)
- [ ] Audio plays correctly
- [ ] No console errors (F12)
- [ ] Canvas rendering performance acceptable (60fps)

---

## ♿ Accessibility Testing (Manual)

**WCAG Compliance:**
- [ ] Keyboard navigation (Tab, Enter, Space, Escape)
- [ ] Screen reader compatibility (ARIA labels)
- [ ] Sufficient color contrast (WCAG AA)
- [ ] Focus indicators visible
- [ ] Alternative text for visual elements

**Specific Tests:**
- [ ] Navigate UI without mouse (keyboard only)
- [ ] Test with NVDA/JAWS screen reader
- [ ] Verify all buttons have accessible names
- [ ] Verify radar scope has descriptive ARIA label

---

## ⚡ Performance Testing

**Stress Tests:**
```python
def test_50_tracks_performance():
    """Verify simulator maintains 60fps with 50 tracks"""

def test_100_tracks_performance():
    """Verify simulator degrades gracefully with 100 tracks"""

def test_memory_leak_detection():
    """Verify no memory leaks during 10-minute session"""
```

**Profiling:**
- Use Chrome DevTools Performance tab
- Measure frame times during heavy load
- Identify rendering bottlenecks

---

## 🔒 Security Testing

**XSS Prevention:**
```python
def test_track_name_xss_injection():
    """Verify track names sanitized (no <script> injection)"""

def test_system_message_xss_injection():
    """Verify system messages sanitized"""
```

**Input Validation:**
```python
def test_invalid_track_id():
    """Verify invalid track ID handled gracefully"""

def test_invalid_scenario_name():
    """Verify invalid scenario name handled gracefully"""
```

---

## 📊 Test Coverage Goals

**Target Coverage:**
- Unit tests: 80%+ coverage
- Simulation tests: 70%+ coverage
- Design language tests: 100% (all invariants)
- Integration tests: 100% (all critical workflows)

**Measurement:**
```powershell
uv run pytest --cov=an_fsq7_simulator --cov-report=html
```

---

## 🚀 Running Tests

**All Tests:**
```powershell
uv run pytest
```

**Specific Suite:**
```powershell
uv run pytest tests/unit
uv run pytest tests/sim
uv run pytest tests/design_language
uv run pytest tests/integration
```

**With Coverage:**
```powershell
uv run pytest --cov=an_fsq7_simulator --cov-report=term-missing
```

**Verbose Output:**
```powershell
uv run pytest -v -s
```

---

## 📅 Implementation Timeline

**Phase 1: Foundation (Week 1)**
- [ ] Set up pytest configuration
- [ ] Create test directory structure
- [ ] Implement 5 unit tests (CPU, drum, light gun)

**Phase 2: Core Logic (Week 2)**
- [ ] Implement simulation tests (scenarios, physics, interceptors)
- [ ] Implement design language tests (mode-free, layout, P14)
- [ ] Achieve 50%+ coverage

**Phase 3: Integration (Week 3)**
- [ ] Implement integration tests (workflows)
- [ ] Implement property-based tests
- [ ] Achieve 70%+ coverage

**Phase 4: Cross-Platform (Week 4)**
- [ ] Manual cross-browser testing
- [ ] Accessibility testing
- [ ] Performance profiling
- [ ] Security audit

---

## 📚 References

- **pytest Documentation:** https://docs.pytest.org/
- **Hypothesis (Property Testing):** https://hypothesis.readthedocs.io/
- **WCAG Guidelines:** https://www.w3.org/WAI/WCAG21/quickref/
- **Chrome DevTools:** https://developer.chrome.com/docs/devtools/

---

## ✅ Success Criteria

Before declaring the project "production-ready":

1. ✅ 80%+ test coverage on core logic
2. ✅ All design language invariants tested
3. ✅ All critical workflows have integration tests
4. ✅ Cross-browser compatibility verified
5. ✅ Accessibility WCAG AA compliance
6. ✅ No known security vulnerabilities
7. ✅ Performance acceptable (60fps with 50 tracks)

---

**Next Steps:** Begin Phase 1 (Foundation) - set up pytest and create first 5 unit tests.
