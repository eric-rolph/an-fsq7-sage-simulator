"""
Track Lifecycle Visualization

Requirement #6: Track Lifecycle Visualization

Visualize track states with distinct visuals:
- NEW: Just detected, pulsing white halo
- CORRELATED: Confirmed target, solid green/red
- DESIGNATED: Operator selected, yellow highlight
- ASSIGNED: Intercept dispatched, blue connection line
- INTERCEPTED: Neutralized, fading out
- LOST: Contact lost, dashed outline

Each state has:
- Distinct color coding
- Halo/glow effects
- Status icon
- Log entry on state change
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


class TrackState(Enum):
    """Track lifecycle states"""
    NEW = "new"                    # Just detected
    CORRELATED = "correlated"      # Confirmed and tracked
    DESIGNATED = "designated"      # Operator selected
    ASSIGNED = "assigned"          # Intercept assigned
    INTERCEPTED = "intercepted"    # Neutralized
    LOST = "lost"                  # Contact lost


@dataclass
class TrackLifecycle:
    """
    Complete track lifecycle data
    Extends base Track with state management
    """
    state: TrackState = TrackState.NEW
    state_changed_at: float = 0.0  # Timestamp of last state change
    designated_by: str = ""        # Operator who designated
    assigned_interceptor: str = "" # ID of assigned interceptor
    time_in_state: float = 0.0     # Seconds in current state
    history: list = field(default_factory=list)  # State change history
    

# Visual styling for each state
TRACK_STATE_STYLES = {
    TrackState.NEW: {
        "color": "#ffffff",           # White
        "glow": "0 0 20px #ffffff, 0 0 40px #ffffff",
        "size": 6,
        "icon": "⊕",                  # New contact
        "blink": True,
        "pulse_speed": "1s",
        "description": "NEW CONTACT - Unconfirmed detection"
    },
    
    TrackState.CORRELATED: {
        "color": "#00ff00",           # Green (friendly) or #ff0000 (hostile)
        "glow": "0 0 10px currentColor",
        "size": 5,
        "icon": "●",                  # Solid dot
        "blink": False,
        "pulse_speed": None,
        "description": "CORRELATED - Confirmed target"
    },
    
    TrackState.DESIGNATED: {
        "color": "#ffff00",           # Yellow
        "glow": "0 0 20px #ffff00, 0 0 40px #ffaa00",
        "size": 8,
        "icon": "◉",                  # Target reticle
        "blink": False,
        "pulse_speed": "0.5s",        # Fast pulse
        "description": "DESIGNATED - Operator selected"
    },
    
    TrackState.ASSIGNED: {
        "color": "#00ffff",           # Cyan
        "glow": "0 0 15px #00ffff, 0 0 30px #0088ff",
        "size": 7,
        "icon": "⚡",                  # Intercept assigned
        "blink": False,
        "pulse_speed": "2s",          # Slow pulse
        "description": "ASSIGNED - Intercept in progress"
    },
    
    TrackState.INTERCEPTED: {
        "color": "#ff00ff",           # Magenta
        "glow": "0 0 30px #ff00ff",
        "size": 10,
        "icon": "✗",                  # Neutralized
        "blink": True,
        "pulse_speed": "0.3s",        # Very fast blink
        "description": "INTERCEPTED - Target neutralized"
    },
    
    TrackState.LOST: {
        "color": "#888888",           # Gray
        "glow": "0 0 5px #888888",
        "size": 4,
        "icon": "○",                  # Empty circle
        "blink": True,
        "pulse_speed": "1.5s",
        "description": "LOST - Contact lost"
    }
}


# State transition rules
VALID_TRANSITIONS = {
    TrackState.NEW: [TrackState.CORRELATED, TrackState.LOST],
    TrackState.CORRELATED: [TrackState.DESIGNATED, TrackState.LOST],
    TrackState.DESIGNATED: [TrackState.ASSIGNED, TrackState.CORRELATED, TrackState.LOST],
    TrackState.ASSIGNED: [TrackState.INTERCEPTED, TrackState.LOST],
    TrackState.INTERCEPTED: [],  # Terminal state
    TrackState.LOST: []          # Terminal state
}


def can_transition(from_state: TrackState, to_state: TrackState) -> bool:
    """Check if state transition is valid"""
    return to_state in VALID_TRANSITIONS.get(from_state, [])


def transition_track_state(
    track_lifecycle: TrackLifecycle,
    new_state: TrackState,
    operator: str = "AUTO",
    timestamp: float = None
) -> tuple[bool, str]:
    """
    Transition track to new state
    Returns (success, message)
    """
    if timestamp is None:
        timestamp = datetime.now().timestamp()
    
    # Check if transition is valid
    if not can_transition(track_lifecycle.state, new_state):
        return False, f"Invalid transition: {track_lifecycle.state.value} → {new_state.value}"
    
    # Record in history
    track_lifecycle.history.append({
        "from_state": track_lifecycle.state.value,
        "to_state": new_state.value,
        "timestamp": timestamp,
        "operator": operator
    })
    
    # Update state
    old_state = track_lifecycle.state
    track_lifecycle.state = new_state
    track_lifecycle.state_changed_at = timestamp
    track_lifecycle.time_in_state = 0.0
    
    message = f"Track transitioned: {old_state.value} → {new_state.value}"
    return True, message


def get_track_color(track_lifecycle: TrackLifecycle, track_type: str) -> str:
    """
    Get appropriate color for track based on state and type
    State takes precedence over type for designated/assigned tracks
    """
    # State-specific colors override type
    if track_lifecycle.state in [TrackState.NEW, TrackState.DESIGNATED, 
                                   TrackState.ASSIGNED, TrackState.INTERCEPTED, 
                                   TrackState.LOST]:
        return TRACK_STATE_STYLES[track_lifecycle.state]["color"]
    
    # Correlated tracks use type-based colors
    if track_lifecycle.state == TrackState.CORRELATED:
        type_colors = {
            "hostile": "#ff0000",
            "friendly": "#00ff00",
            "unknown": "#ffff00",
            "missile": "#ff00ff",
            "interceptor": "#00ffff"
        }
        return type_colors.get(track_type, "#ffffff")
    
    return "#ffffff"


def get_track_style(track_lifecycle: TrackLifecycle) -> dict:
    """Get complete visual style for track based on current state"""
    return TRACK_STATE_STYLES.get(track_lifecycle.state, TRACK_STATE_STYLES[TrackState.NEW])


# CSS animations for track state visualization
TRACK_LIFECYCLE_CSS = """
<style>
/* NEW state - pulsing white */
@keyframes pulse-new {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.3); }
}

.track-new {
    animation: pulse-new 1s ease-in-out infinite;
}

/* DESIGNATED state - fast pulse yellow */
@keyframes pulse-designated {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.2); }
}

.track-designated {
    animation: pulse-designated 0.5s ease-in-out infinite;
}

/* ASSIGNED state - slow pulse cyan */
@keyframes pulse-assigned {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.track-assigned {
    animation: pulse-assigned 2s ease-in-out infinite;
}

/* INTERCEPTED state - fast blink magenta */
@keyframes blink-intercepted {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0; }
}

.track-intercepted {
    animation: blink-intercepted 0.3s step-end infinite;
}

/* LOST state - slow blink gray */
@keyframes blink-lost {
    0%, 49% { opacity: 0.5; }
    50%, 100% { opacity: 0.1; }
}

.track-lost {
    animation: blink-lost 1.5s step-end infinite;
}

/* State indicator badge */
.track-state-badge {
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'Courier New', monospace;
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 3px;
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid currentColor;
    white-space: nowrap;
}

/* Connection line for assigned intercepts */
.intercept-connection {
    stroke-dasharray: 5, 5;
    stroke-width: 2;
    opacity: 0.6;
    animation: dash-flow 1s linear infinite;
}

@keyframes dash-flow {
    to { stroke-dashoffset: -10; }
}
</style>
"""


# JavaScript for track state rendering on canvas
TRACK_STATE_RENDER_SCRIPT = """
function renderTrackWithState(ctx, track, trackLifecycle) {
    const x = track.x * canvas.width;
    const y = track.y * canvas.height;
    const style = getTrackStateStyle(trackLifecycle.state);
    
    // Save context
    ctx.save();
    
    // Draw glow
    ctx.shadowColor = style.color;
    ctx.shadowBlur = style.size * 3;
    
    // Draw main track dot
    ctx.fillStyle = style.color;
    ctx.globalAlpha = calculateAlpha(trackLifecycle);
    ctx.beginPath();
    ctx.arc(x, y, style.size, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw state ring if designated/assigned
    if (trackLifecycle.state === 'designated' || trackLifecycle.state === 'assigned') {
        ctx.strokeStyle = style.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = 0.8;
        ctx.beginPath();
        ctx.arc(x, y, style.size * 2.5, 0, Math.PI * 2);
        ctx.stroke();
    }
    
    // Draw state icon above track
    ctx.font = '12px Courier New';
    ctx.fillStyle = style.color;
    ctx.globalAlpha = 1.0;
    ctx.textAlign = 'center';
    ctx.fillText(style.icon, x, y - 15);
    
    // Draw connection line if assigned
    if (trackLifecycle.state === 'assigned' && trackLifecycle.assigned_interceptor) {
        const interceptor = findTrack(trackLifecycle.assigned_interceptor);
        if (interceptor) {
            drawInterceptLine(ctx, track, interceptor, style.color);
        }
    }
    
    ctx.restore();
}

function calculateAlpha(trackLifecycle) {
    // Pulse effect based on state
    const time = Date.now() / 1000;
    
    switch(trackLifecycle.state) {
        case 'new':
            return 0.6 + 0.4 * Math.sin(time * 6);  // Fast pulse
        case 'designated':
            return 0.8 + 0.2 * Math.sin(time * 12); // Very fast pulse
        case 'assigned':
            return 0.7 + 0.3 * Math.sin(time * 3);  // Slow pulse
        case 'intercepted':
            return Math.floor(time * 3) % 2 ? 1 : 0; // Blink
        case 'lost':
            return Math.floor(time * 0.7) % 2 ? 0.5 : 0.1; // Slow blink
        default:
            return 1.0;
    }
}

function drawInterceptLine(ctx, target, interceptor, color) {
    const x1 = target.x * canvas.width;
    const y1 = target.y * canvas.height;
    const x2 = interceptor.x * canvas.width;
    const y2 = interceptor.y * canvas.height;
    
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.globalAlpha = 0.6;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.restore();
}
"""


def get_state_description(state: TrackState) -> str:
    """Get human-readable description of track state"""
    return TRACK_STATE_STYLES[state]["description"]


def get_state_duration_warning(track_lifecycle: TrackLifecycle) -> Optional[str]:
    """
    Check if track has been in state too long
    Returns warning message if applicable
    """
    warnings = {
        TrackState.NEW: (10.0, "Track not correlated - check radar"),
        TrackState.DESIGNATED: (30.0, "Designated track not assigned - action required"),
        TrackState.ASSIGNED: (120.0, "Long intercept time - check status"),
    }
    
    if track_lifecycle.state in warnings:
        threshold, message = warnings[track_lifecycle.state]
        if track_lifecycle.time_in_state > threshold:
            return message
    
    return None
