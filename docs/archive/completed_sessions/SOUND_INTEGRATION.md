# Sound Effects Integration Quick Reference

## 🔌 How to Add Sounds to Existing Components

This guide shows how to wire sound effects into the SAGE simulator components.

---

## 1. Import Sound Effects Module

In `interactive_sage.py`:

```python
from .components_v2 import (
    # ... existing imports ...
    sound_effects,  # ADD THIS
)
```

---

## 2. Add Sound State to InteractiveSageState

```python
class InteractiveSageState(rx.State):
    # ... existing state fields ...
    
    # ===== SOUND STATE =====
    sound_enabled: bool = True
    ambient_volume: float = 0.3
    effects_volume: float = 0.7
    alerts_volume: float = 0.8
    current_sound: Optional[str] = None
```

---

## 3. Play Sounds from State Methods

### Track Detection (in `tick()` method)
```python
def tick(self):
    # ... existing track logic ...
    
    # When new track appears
    if new_track_detected:
        self.play_sound("track_detected", "effect")
```

### Button Presses (in `toggle_filter()` etc)
```python
def toggle_filter(self, filter_name: str):
    # Play click sound
    self.play_sound("button_press", "interface")
    
    # ... existing filter logic ...
```

### Light Gun Selection
```python
def select_track_with_lightgun(self, track_id: str):
    # Play selection sound
    self.play_sound("lightgun_select", "interface")
    
    # ... existing selection logic ...
```

### Intercept Launch
```python
def launch_interceptor(self):
    # Play launch sound
    self.play_sound("intercept_launch", "alert")
    
    # ... existing interceptor logic ...
```

### Hostile Designation
```python
def designate_hostile(self, track_id: str):
    # Play alert
    self.play_sound("hostile_alert", "alert")
    
    # ... existing designation logic ...
```

---

## 4. Add Sound Helper Methods to State

```python
class InteractiveSageState(rx.State):
    # ... existing methods ...
    
    def play_sound(self, sound_id: str, category: str = "effects"):
        """Play a sound effect"""
        if not self.sound_enabled:
            return
        
        self.current_sound = sound_id
        # JavaScript call happens via event system
    
    def set_ambient_volume(self, value: float):
        """Set ambient volume (0.0 to 1.0)"""
        self.ambient_volume = value
    
    def set_effects_volume(self, value: float):
        """Set effects volume (0.0 to 1.0)"""
        self.effects_volume = value
    
    def set_alerts_volume(self, value: float):
        """Set alerts volume (0.0 to 1.0)"""
        self.alerts_volume = value
    
    def toggle_sound_mute(self):
        """Toggle all sound on/off"""
        self.sound_enabled = not self.sound_enabled
    
    def set_sound_preset(self, preset: str):
        """Apply sound volume preset"""
        presets = {
            "silent": (0.0, 0.0, 0.0),
            "subtle": (0.1, 0.3, 0.5),
            "normal": (0.3, 0.7, 0.8),
            "immersive": (0.5, 1.0, 1.0),
        }
        if preset in presets:
            self.ambient_volume, self.effects_volume, self.alerts_volume = presets[preset]
```

---

## 5. Add Sound Settings to UI

In the main layout (e.g., sidebar or settings panel):

```python
def main_layout():
    return rx.box(
        # ... existing layout ...
        
        # Add sound settings panel
        rx.cond(
            InteractiveSageState.show_sound_settings,
            sound_effects.sound_settings_panel(
                ambient_volume=InteractiveSageState.ambient_volume,
                effects_volume=InteractiveSageState.effects_volume,
                alerts_volume=InteractiveSageState.alerts_volume,
                mute_all=not InteractiveSageState.sound_enabled,
            )
        ),
    )
```

---

## 6. Add JavaScript Sound Player to Page

In your main page component, include the sound player script:

```python
def index():
    return rx.box(
        # ... existing UI ...
        
        # Include sound player JavaScript
        rx.script(sound_effects.SOUND_PLAYER_SCRIPT),
        
        # Preload sounds on page load
        rx.script("""
            window.addEventListener('load', async () => {
                const sounds = [
                    'radar_sweep', 'track_detected', 'button_press',
                    'lightgun_select', 'hostile_alert', 'intercept_launch'
                ];
                
                for (const soundId of sounds) {
                    await window.sageSoundPlayer.loadSound(
                        soundId, 
                        `/sounds/${soundId}.wav`
                    );
                }
                
                // Start ambient radar sweep
                window.playSound('radar_sweep', 'ambient', true);
            });
        """),
    )
```

---

## 7. Wire Sounds to Track Lifecycle

In `track_lifecycle.py` integration:

```python
def transition_track_state(track: TrackLifecycle, new_state: TrackState):
    """Transition track with sound effect"""
    old_state = track.state
    track.state = new_state
    track.state_changed_at = datetime.now()
    
    # Play appropriate sound based on state
    sound_map = {
        TrackState.NEW: "track_detected",
        TrackState.CORRELATED: "track_correlated",
        TrackState.DESIGNATED: "hostile_alert",
        TrackState.ASSIGNED: "intercept_assign",
        TrackState.INTERCEPTED: "engagement_success",
        TrackState.LOST: "track_lost",
    }
    
    if new_state in sound_map:
        # Trigger sound (will be picked up by state)
        return sound_map[new_state]
    
    return None
```

---

## 8. Wire Sounds to System Messages

In `system_messages.py` log functions, add sound hints:

```python
def log_track_selected(track_id: str) -> SystemMessage:
    """Log track selection with sound"""
    return SystemMessage(
        timestamp=datetime.now(),
        category="ACTION",
        message="Track Selected",
        details=f"ID: {track_id}",
        sound_effect="lightgun_select",  # NEW FIELD
    )
```

Then in the logging call:

```python
def select_track(self, track_id: str):
    msg = system_messages.log_track_selected(track_id)
    self.system_messages_log.append(msg)
    
    # Play sound if specified
    if msg.sound_effect:
        self.play_sound(msg.sound_effect, "interface")
```

---

## 9. Add Sound Status Indicator

Show when sounds are playing:

```python
def status_bar():
    return rx.hstack(
        # ... existing status items ...
        
        # Sound indicator
        sound_effects.sound_status_indicator(
            is_playing=InteractiveSageState.current_sound is not None,
            current_sound=InteractiveSageState.current_sound,
        ),
    )
```

---

## 10. Keyboard Shortcuts for Sound

Add hotkeys:

```python
# In main page event handlers
rx.script("""
    document.addEventListener('keydown', (e) => {
        // M = Mute/Unmute
        if (e.key === 'm' || e.key === 'M') {
            window.muteSounds(!window.sageSoundPlayer.muted);
        }
        
        // [ = Volume Down
        if (e.key === '[') {
            const vol = window.sageSoundPlayer.volumes.master;
            window.setSoundVolume('master', Math.max(0, vol - 0.1));
        }
        
        // ] = Volume Up
        if (e.key === ']') {
            const vol = window.sageSoundPlayer.volumes.master;
            window.setSoundVolume('master', Math.min(1, vol + 0.1));
        }
    });
""")
```

---

## 📋 Complete Integration Checklist

- [ ] Import `sound_effects` module
- [ ] Add sound state fields to `InteractiveSageState`
- [ ] Add sound helper methods (`play_sound`, etc.)
- [ ] Include `SOUND_PLAYER_SCRIPT` in main page
- [ ] Preload essential sounds on page load
- [ ] Wire sounds to button clicks (`toggle_filter`, `toggle_overlay`)
- [ ] Wire sounds to light gun selection
- [ ] Wire sounds to intercept launch
- [ ] Wire sounds to track state transitions
- [ ] Wire sounds to hostile designations
- [ ] Wire sounds to tube maintenance events
- [ ] Add sound settings panel to UI
- [ ] Add sound status indicator
- [ ] Test all sounds in browser
- [ ] Add volume controls
- [ ] Add mute toggle
- [ ] Add keyboard shortcuts
- [ ] Test on mobile devices

---

## 🎮 Testing Your Integration

1. **Open browser console** (F12)

2. **Check sound player loaded**:
   ```javascript
   console.log(window.sageSoundPlayer);
   ```

3. **Test individual sounds**:
   ```javascript
   window.playSound('button_press', 'interface');
   ```

4. **Test state integration**:
   - Click a console button → should hear click
   - Select track with light gun → should hear selection
   - Launch interceptor → should hear launch alert

5. **Test volume controls**:
   - Adjust sliders in settings panel
   - Press `M` to mute
   - Press `[` and `]` for volume

---

## 🐛 Common Issues

**Sounds don't play**:
- Check browser console for loading errors
- Verify files exist in `/public/sounds/`
- Check file paths match `sound_effects.py`
- Ensure AudioContext resumed (Chrome requires user interaction)

**Sounds too loud/quiet**:
- Adjust volume in `SOUND_LIBRARY` definitions
- Normalize audio files in Audacity to -3dB
- Check category volumes (ambient/effects/alerts)

**Sounds lag/stutter**:
- Preload essential sounds on page load
- Compress audio files (OGG format recommended)
- Check file sizes (should be < 500KB each)

**Sounds don't loop smoothly**:
- Edit loop points in Audacity
- Add crossfade at loop boundary
- Use dedicated loop editor

---

**Quick Start**: Copy the code snippets above into your components in the order listed. Start with step 1-6 for basic sound support, then add 7-10 for advanced features.
