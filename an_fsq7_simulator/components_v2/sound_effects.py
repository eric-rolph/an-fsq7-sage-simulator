"""
Sound Effects System for SAGE Simulator

Authentic Cold War era radar and computer sound effects to enhance immersion.

Sound Categories:
- Radar sweep/ping sounds (continuous background)
- Track detection alerts (new contact)
- Button press/console clicks (mechanical switches)
- Light gun selection (CRT beam lock)
- Intercept launch (weapons release)
- Computer processing (data correlation)
- Alert tones (hostile designation)
- Tube failure/maintenance sounds

All sounds should be period-appropriate (1950s-1960s vintage electronics).

Recommended Sources (Creative Commons / Public Domain):
- Freesound.org radar/sonar packs
- Archive.org vintage military electronics
- NASA archives (early space program computer sounds)
"""

import reflex as rx
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class SoundEffect:
    """Single sound effect definition"""
    id: str
    name: str
    file_path: str  # Path to audio file (mp3/wav/ogg)
    volume: float = 1.0  # 0.0 to 1.0
    loop: bool = False
    category: str = "effect"  # "ambient", "effect", "alert", "interface"
    description: str = ""


# ================================
# SOUND EFFECT LIBRARY
# ================================

SOUND_LIBRARY: Dict[str, SoundEffect] = {
    # AMBIENT BACKGROUND (LOOPS)
    "radar_sweep": SoundEffect(
        id="radar_sweep",
        name="Radar Sweep",
        file_path="/sounds/radar_sweep_loop.wav",
        volume=0.3,
        loop=True,
        category="ambient",
        description="Continuous rotating radar beam sweep (Freesound #371178 - Sonar sweep beep)"
    ),
    
    "computer_hum": SoundEffect(
        id="computer_hum",
        name="Computer Room Ambience",
        file_path="/sounds/computer_room_ambient.wav",
        volume=0.2,
        loop=True,
        category="ambient",
        description="Vacuum tube computer hum and cooling fans (Freesound #79100 - 1950s Computer)"
    ),
    
    "crt_hum": SoundEffect(
        id="crt_hum",
        name="CRT Display Hum",
        file_path="/sounds/crt_hum.wav",
        volume=0.15,
        loop=True,
        category="ambient",
        description="High voltage CRT transformer whine"
    ),
    
    # RADAR EVENTS
    "track_detected": SoundEffect(
        id="track_detected",
        name="New Track Detected",
        file_path="/sounds/radar_blip.wav",
        volume=0.6,
        category="effect",
        description="Short radar ping for new contact (Freesound #131708 - Radar Blip)"
    ),
    
    "track_correlated": SoundEffect(
        id="track_correlated",
        name="Track Correlated",
        file_path="/sounds/correlation_beep.wav",
        volume=0.5,
        category="effect",
        description="Computer confirms track correlation"
    ),
    
    "track_lost": SoundEffect(
        id="track_lost",
        name="Track Lost",
        file_path="/sounds/track_lost.wav",
        volume=0.4,
        category="effect",
        description="Descending tone for lost radar contact"
    ),
    
    # OPERATOR ACTIONS
    "lightgun_select": SoundEffect(
        id="lightgun_select",
        name="Light Gun Selection",
        file_path="/sounds/lightgun_click.wav",
        volume=0.7,
        category="interface",
        description="CRT beam detection click (like Star Trek tactical)"
    ),
    
    "button_press": SoundEffect(
        id="button_press",
        name="Console Button",
        file_path="/sounds/button_press.wav",
        volume=0.5,
        category="interface",
        description="Mechanical switch click (vintage toggle)"
    ),
    
    "button_release": SoundEffect(
        id="button_release",
        name="Button Release",
        file_path="/sounds/button_release.wav",
        volume=0.4,
        category="interface",
        description="Mechanical switch release"
    ),
    
    "keyboard_type": SoundEffect(
        id="keyboard_type",
        name="Keyboard Entry",
        file_path="/sounds/keyboard_click.wav",
        volume=0.45,
        category="interface",
        description="Teletype/electric typewriter key"
    ),
    
    # DESIGNATION & WEAPONS
    "hostile_alert": SoundEffect(
        id="hostile_alert",
        name="Hostile Designation Alert",
        file_path="/sounds/hostile_alert.wav",
        volume=0.8,
        category="alert",
        description="Warning tone for hostile track (Freesound #807657 - Scanning For Hostiles)"
    ),
    
    "intercept_launch": SoundEffect(
        id="intercept_launch",
        name="Intercept Launched",
        file_path="/sounds/intercept_launch.wav",
        volume=0.85,
        category="effect",
        description="Weapons release confirmation tone"
    ),
    
    "intercept_assign": SoundEffect(
        id="intercept_assign",
        name="Interceptor Assigned",
        file_path="/sounds/intercept_assign.wav",
        volume=0.6,
        category="effect",
        description="Computer calculating intercept solution"
    ),
    
    "engagement_success": SoundEffect(
        id="engagement_success",
        name="Engagement Successful",
        file_path="/sounds/engagement_success.wav",
        volume=0.7,
        category="alert",
        description="Target destroyed confirmation"
    ),
    
    # SYSTEM STATUS
    "program_load": SoundEffect(
        id="program_load",
        name="Program Loading",
        file_path="/sounds/program_load.wav",
        volume=0.5,
        category="effect",
        description="Magnetic drum/core memory access (Freesound #43762 - TI99 cassette)"
    ),
    
    "program_execute": SoundEffect(
        id="program_execute",
        name="Program Execute",
        file_path="/sounds/program_execute.wav",
        volume=0.55,
        category="effect",
        description="CPU cycle burst for program execution"
    ),
    
    "error_tone": SoundEffect(
        id="error_tone",
        name="System Error",
        file_path="/sounds/error_tone.wav",
        volume=0.75,
        category="alert",
        description="Error/fault warning (Freesound #811740 - Vintage Error)"
    ),
    
    "warning_tone": SoundEffect(
        id="warning_tone",
        name="Warning",
        file_path="/sounds/warning_tone.wav",
        volume=0.65,
        category="alert",
        description="Attention required tone"
    ),
    
    # MAINTENANCE
    "tube_failure": SoundEffect(
        id="tube_failure",
        name="Tube Failure",
        file_path="/sounds/tube_failure.wav",
        volume=0.6,
        category="alert",
        description="Vacuum tube failure pop/crackle"
    ),
    
    "tube_warmup": SoundEffect(
        id="tube_warmup",
        name="Tube Warming Up",
        file_path="/sounds/tube_warmup.wav",
        volume=0.4,
        category="effect",
        description="Filament heating noise"
    ),
    
    "tube_eject": SoundEffect(
        id="tube_eject",
        name="Tube Ejection",
        file_path="/sounds/tube_eject.wav",
        volume=0.5,
        category="effect",
        description="Mechanical tube removal"
    ),
    
    "tube_insert": SoundEffect(
        id="tube_insert",
        name="Tube Insertion",
        file_path="/sounds/tube_insert.wav",
        volume=0.5,
        category="effect",
        description="New tube socketed"
    ),
    
    # SCENARIO EVENTS
    "scenario_start": SoundEffect(
        id="scenario_start",
        name="Scenario Start",
        file_path="/sounds/scenario_start.wav",
        volume=0.7,
        category="effect",
        description="Mission begin chime"
    ),
    
    "scenario_complete": SoundEffect(
        id="scenario_complete",
        name="Scenario Complete",
        file_path="/sounds/scenario_complete.wav",
        volume=0.8,
        category="effect",
        description="Mission success fanfare"
    ),
    
    "scenario_failed": SoundEffect(
        id="scenario_failed",
        name="Scenario Failed",
        file_path="/sounds/scenario_failed.wav",
        volume=0.75,
        category="alert",
        description="Mission failure alarm"
    ),
}


# ================================
# SOUND PRESETS BY CONTEXT
# ================================

SOUND_PRESETS = {
    "track_lifecycle": {
        "new": "track_detected",
        "correlated": "track_correlated",
        "designated": "hostile_alert",
        "assigned": "intercept_assign",
        "intercepted": "engagement_success",
        "lost": "track_lost",
    },
    
    "console_actions": {
        "button": "button_press",
        "filter": "button_press",
        "overlay": "button_press",
        "lightgun": "lightgun_select",
    },
    
    "system_messages": {
        "INFO": None,  # Silent
        "ACTION": "button_press",
        "WARNING": "warning_tone",
        "ERROR": "error_tone",
        "SUCCESS": "engagement_success",
        "TRACK": "track_detected",
        "INTERCEPT": "intercept_launch",
        "FILTER": "button_press",
        "CPU": "program_execute",
    },
}


# ================================
# SOUND MANAGER COMPONENT
# ================================

def sound_settings_panel(
    ambient_volume: float,
    effects_volume: float,
    alerts_volume: float,
    mute_all: bool,
) -> rx.Component:
    """
    Sound settings control panel
    """
    return rx.box(
        rx.vstack(
            rx.heading(
                "🔊 SOUND SETTINGS",
                size="4",
                color="#00ff88",
                font_family="Courier New"
            ),
            
            rx.divider(border_color="#00ff8844"),
            
            # Master mute
            rx.hstack(
                rx.switch(
                    checked=not mute_all,
                    on_change=rx.State.toggle_sound_mute,  # type: ignore
                    color_scheme="green"
                ),
                rx.text(
                    "SOUND ENABLED" if not mute_all else "SOUND MUTED",
                    font_weight="bold",
                    color="#00ff00" if not mute_all else "#ff0000",
                    font_family="Courier New"
                ),
                spacing="3",
                align="center"
            ),
            
            rx.divider(border_color="#444444"),
            
            # Volume controls
            volume_slider(
                label="AMBIENT (radar sweep, computer hum)",
                value=ambient_volume,
                on_change=rx.State.set_ambient_volume,  # type: ignore
                color="blue"
            ),
            
            volume_slider(
                label="EFFECTS (button clicks, selections)",
                value=effects_volume,
                on_change=rx.State.set_effects_volume,  # type: ignore
                color="green"
            ),
            
            volume_slider(
                label="ALERTS (warnings, hostiles, intercepts)",
                value=alerts_volume,
                on_change=rx.State.set_alerts_volume,  # type: ignore
                color="orange"
            ),
            
            rx.divider(border_color="#444444"),
            
            # Sound test buttons
            rx.text(
                "TEST SOUNDS",
                font_weight="bold",
                color="#888888",
                font_size="11px"
            ),
            rx.wrap(
                test_sound_button("Radar Ping", "track_detected"),
                test_sound_button("Button Click", "button_press"),
                test_sound_button("Light Gun", "lightgun_select"),
                test_sound_button("Hostile Alert", "hostile_alert"),
                test_sound_button("Intercept", "intercept_launch"),
                test_sound_button("Error Tone", "error_tone"),
                spacing="2"
            ),
            
            rx.divider(border_color="#444444"),
            
            # Quick presets
            rx.text(
                "PRESETS",
                font_weight="bold",
                color="#888888",
                font_size="11px"
            ),
            rx.hstack(
                rx.button(
                    "SILENT",
                    size="1",
                    variant="soft",
                    on_click=rx.State.set_sound_preset("silent"),  # type: ignore
                    style={"font_family": "Courier New"}
                ),
                rx.button(
                    "SUBTLE",
                    size="1",
                    variant="soft",
                    on_click=rx.State.set_sound_preset("subtle"),  # type: ignore
                    style={"font_family": "Courier New"}
                ),
                rx.button(
                    "NORMAL",
                    size="1",
                    variant="soft",
                    on_click=rx.State.set_sound_preset("normal"),  # type: ignore
                    style={"font_family": "Courier New"}
                ),
                rx.button(
                    "IMMERSIVE",
                    size="1",
                    variant="soft",
                    on_click=rx.State.set_sound_preset("immersive"),  # type: ignore
                    style={"font_family": "Courier New"}
                ),
                spacing="2"
            ),
            
            spacing="3",
            width="100%"
        ),
        padding="20px",
        background="#000000",
        border="2px solid #00ff88",
        border_radius="8px",
        max_width="500px"
    )


def volume_slider(
    label: str,
    value: float,
    on_change,
    color: str = "green"
) -> rx.Component:
    """Single volume control slider"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(label, font_size="11px", color="#888888"),
                rx.spacer(),
                rx.text(
                    f"{int(value * 100)}%",
                    font_family="Courier New",
                    font_weight="bold",
                    color="#00ff00"
                ),
                width="100%"
            ),
            rx.slider(
                value=value * 100,
                min=0,
                max=100,
                step=5,
                on_change=lambda v: on_change(v / 100.0),
                color_scheme=color,
                width="100%"
            ),
            spacing="2",
            width="100%"
        ),
        width="100%"
    )


def test_sound_button(label: str, sound_id: str) -> rx.Component:
    """Button to test a specific sound"""
    return rx.button(
        label,
        size="1",
        variant="outline",
        color_scheme="gray",
        on_click=rx.State.play_sound(sound_id),  # type: ignore
        style={
            "font_family": "Courier New",
            "font_size": "10px"
        }
    )


def sound_status_indicator(is_playing: bool, current_sound: Optional[str]) -> rx.Component:
    """
    Small indicator showing current sound status
    """
    return rx.cond(
        is_playing and current_sound is not None,
        rx.badge(
            rx.hstack(
                rx.text("🔊", font_size="10px"),
                rx.text(current_sound.replace("_", " ").upper(), font_size="9px"),
                spacing="1"
            ),
            color_scheme="green",
            variant="soft",
            size="1"
        ),
        rx.box()  # Empty when no sound playing
    )


# ================================
# SOUND DOCUMENTATION
# ================================

def sound_sources_documentation() -> rx.Component:
    """
    Documentation for where to obtain authentic SAGE-era sounds
    """
    return rx.box(
        rx.vstack(
            rx.heading(
                "Authentic SAGE Sound Sources",
                size="5",
                color="#00ff00"
            ),
            
            rx.text(
                "For historical accuracy, use sounds from these Creative Commons / Public Domain sources:",
                color="#888888",
                margin_bottom="20px"
            ),
            
            # Freesound.org
            sound_source_card(
                title="Freesound.org",
                url="https://freesound.org",
                icon="🎵",
                sounds=[
                    "#371178 - Sonar sweep beep (radar sweep loop)",
                    "#131708 - Radar Blip (track detection)",
                    "#807657 - Scanning For Hostiles (hostile alert)",
                    "#96694 - Battlezone Radar Noise (retro radar)",
                    "#79100 - 1950s Computer sounds (ambient hum)",
                    "#811740 - Vintage Error Report (error tone)",
                    "#43762 - TI99 cassette (program loading)",
                ]
            ),
            
            # Archive.org
            sound_source_card(
                title="Archive.org",
                url="https://archive.org",
                icon="📚",
                sounds=[
                    "Military Electronics Collection (authentic 1950s-60s)",
                    "Cold War Documentary Audio (radar rooms, command centers)",
                    "NASA Mission Audio (early computer sounds)",
                ]
            ),
            
            # Sound characteristics
            rx.box(
                rx.vstack(
                    rx.heading("Period-Appropriate Sound Characteristics", size="4", color="#00ff88"),
                    rx.unordered_list(
                        rx.list_item("Vacuum tube electronics (warm, analog tone)"),
                        rx.list_item("Mechanical switches and relays (distinct clicks)"),
                        rx.list_item("CRT display interference (high-pitched whine)"),
                        rx.list_item("Rotating radar sweep (doppler-like whoosh)"),
                        rx.list_item("Magnetic drum/core memory (mechanical access sounds)"),
                        rx.list_item("Teletype keyboards (heavy mechanical keys)"),
                        rx.list_item("Alert tones (simple sine/square waves, not modern synths)"),
                    ),
                    spacing="2"
                ),
                padding="15px",
                background="#001100",
                border="1px solid #00ff88",
                border_radius="4px"
            ),
            
            spacing="4",
            width="100%"
        ),
        padding="30px",
        max_width="800px"
    )


def sound_source_card(title: str, url: str, icon: str, sounds: list) -> rx.Component:
    """Card showing a sound source"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(icon, font_size="24px"),
                rx.heading(title, size="4", color="#00ff00"),
                spacing="3"
            ),
            rx.link(
                url,
                href=url,
                is_external=True,
                color="#00ffff",
                text_decoration="underline"
            ),
            rx.unordered_list(
                *[rx.list_item(sound, color="#888888", font_size="12px") for sound in sounds],
                spacing="1",
                margin_left="20px"
            ),
            spacing="2",
            width="100%"
        ),
        padding="15px",
        background="#000000",
        border="1px solid #00ff0044",
        border_radius="4px",
        width="100%"
    )


# ================================
# JAVASCRIPT SOUND PLAYER
# ================================

SOUND_PLAYER_SCRIPT = """
// Web Audio API sound player for SAGE simulator
class SAGESoundPlayer {
    constructor() {
        this.context = new (window.AudioContext || window.webkitAudioContext)();
        this.sounds = new Map();
        this.volumes = {
            ambient: 0.3,
            effects: 0.7,
            alerts: 0.8,
            master: 1.0
        };
        this.muted = false;
        this.currentAmbient = null;
    }
    
    async loadSound(id, url) {
        try {
            const response = await fetch(url);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.context.decodeAudioData(arrayBuffer);
            this.sounds.set(id, audioBuffer);
            console.log(`Loaded sound: ${id}`);
        } catch (error) {
            console.error(`Failed to load sound ${id}:`, error);
        }
    }
    
    play(soundId, category = 'effects', loop = false) {
        if (this.muted) return;
        
        const buffer = this.sounds.get(soundId);
        if (!buffer) {
            console.warn(`Sound not loaded: ${soundId}`);
            return;
        }
        
        const source = this.context.createBufferSource();
        const gainNode = this.context.createGain();
        
        source.buffer = buffer;
        source.loop = loop;
        
        const categoryVolume = this.volumes[category] || 0.5;
        gainNode.gain.value = categoryVolume * this.volumes.master;
        
        source.connect(gainNode);
        gainNode.connect(this.context.destination);
        
        source.start(0);
        
        if (loop && category === 'ambient') {
            if (this.currentAmbient) {
                this.currentAmbient.stop();
            }
            this.currentAmbient = source;
        }
        
        return source;
    }
    
    setVolume(category, value) {
        this.volumes[category] = Math.max(0, Math.min(1, value));
    }
    
    setMute(muted) {
        this.muted = muted;
        if (muted && this.currentAmbient) {
            this.currentAmbient.stop();
            this.currentAmbient = null;
        }
    }
}

// Global instance
window.sageSoundPlayer = new SAGESoundPlayer();

// Helper functions
window.playSound = (soundId, category = 'effects', loop = false) => {
    window.sageSoundPlayer.play(soundId, category, loop);
};

window.setSoundVolume = (category, value) => {
    window.sageSoundPlayer.setVolume(category, value);
};

window.muteSounds = (muted) => {
    window.sageSoundPlayer.setMute(muted);
};
"""
