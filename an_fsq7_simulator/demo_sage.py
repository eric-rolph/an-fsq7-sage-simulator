"""
Minimal SAGE Demo Page - For Testing Core Functionality

This is a simplified version of the full SAGE simulator that demonstrates
the core interactive features without all the complex integrations.
"""

import reflex as rx
from typing import List, Set
from datetime import datetime
from . import state_model
from .components_v2 import system_messages, sd_console, light_gun


class DemoSageState(rx.State):
    """Simplified state for testing"""
    
    # Light gun state
    lightgun_armed: bool = False
    selected_track_id: str = ""
    
    # SD Console state
    active_filters: Set[str] = set()
    active_overlays: Set[str] = {"range_rings", "coastlines"}
    brightness: float = 0.75
    
    # System messages
    system_messages_log: List[state_model.SystemMessage] = []
    
    # Sample tracks for testing
    test_tracks: List[state_model.Track] = [
        state_model.Track(
            id="TGT-001",
            x=40.7128,
            y=-74.0060,
            altitude=35000,
            speed=520,
            heading=180,
            track_type="hostile",
            threat_level="HIGH"
        ),
        state_model.Track(
            id="TGT-002",
            x=42.3601,
            y=-71.0589,
            altitude=28000,
            speed=450,
            heading=225,
            track_type="friendly",
            threat_level="NONE"
        ),
    ]
    
    def arm_lightgun(self):
        """Arm the light gun for target selection"""
        self.lightgun_armed = True
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                level="info",
                category="operator",
                message="LIGHT GUN ARMED",
                details="Press D key or click ARM button"
            )
        )
    
    def disarm_lightgun(self):
        """Disarm the light gun"""
        self.lightgun_armed = False
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                level="info",
                category="operator",
                message="LIGHT GUN DISARMED",
                details=""
            )
        )
    
    def select_track(self, track_id: str):
        """Select a track with the light gun"""
        self.selected_track_id = track_id
        self.lightgun_armed = False
        track = next((t for t in self.test_tracks if t.id == track_id), None)
        if track:
            self.system_messages_log.append(
                system_messages.SystemMessage(
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    level="info",
                    category="operator",
                    message=f"TRACK SELECTED: {track_id}",
                    details=f"{track.track_type.upper()} @ {track.altitude} ft, {track.speed} kts"
                )
            )
    
    def toggle_filter(self, filter_name: str):
        """Toggle a category filter"""
        if filter_name in self.active_filters:
            self.active_filters.remove(filter_name)
            action = "DISABLED"
        else:
            self.active_filters.add(filter_name)
            action="ENABLED"
        
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                level="info",
                category="system",
                message=f"FILTER {action}: {filter_name.upper()}",
                details=f"Active filters: {len(self.active_filters)}"
            )
        )
    
    def toggle_overlay(self, overlay_name: str):
        """Toggle a display overlay"""
        if overlay_name in self.active_overlays:
            self.active_overlays.remove(overlay_name)
            action = "DISABLED"
        else:
            self.active_overlays.add(overlay_name)
            action = "ENABLED"
        
        self.system_messages_log.append(
            system_messages.SystemMessage(
                timestamp=datetime.now().strftime("%H:%M:%S"),
                level="info",
                category="system",
                message=f"OVERLAY {action}: {overlay_name.upper()}",
                details=""
            )
        )
    
    def get_selected_track(self) -> state_model.Track:
        """Get the currently selected track"""
        return next((t for t in self.test_tracks if t.id == self.selected_track_id), None)


def demo_page() -> rx.Component:
    """Minimal demo page for testing"""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading("AN/FSQ-7 SAGE Simulator - Demo", size="9", color="#00ff00"),
            rx.text("Testing Core Interactive Features", color="#88ff88", margin_bottom="2rem"),
            
            # Main content area
            rx.hstack(
                # LEFT: SD Console controls
                rx.vstack(
                    sd_console.sd_console_master_panel(
                        DemoSageState.active_filters,
                        DemoSageState.active_overlays,
                        DemoSageState.brightness
                    ),
                    width="300px"
                ),
                
                # CENTER: Simulated radar display
                rx.vstack(
                    rx.box(
                        rx.heading("RADAR SCOPE", color="#00ff00", size="5", text_align="center"),
                        rx.text(
                            "Simulated radar display area",
                            color="#888888",
                            text_align="center",
                            margin_top="100px"
                        ),
                        rx.vstack(
                            rx.foreach(
                                DemoSageState.test_tracks,
                                lambda track: rx.button(
                                    f"◎ {track.id} - {track.track_type.upper()}",
                                    on_click=DemoSageState.select_track(track.id),
                                    background="#003300" if track.id != DemoSageState.selected_track_id else "#00ff00",
                                    color="#00ff00" if track.id != DemoSageState.selected_track_id else "#000000",
                                    size="3",
                                    margin="10px"
                                )
                            ),
                            margin_top="50px"
                        ),
                        width="600px",
                        height="600px",
                        border="2px solid #00ff00",
                        border_radius="8px",
                        padding="20px"
                    ),
                    width="640px"
                ),
                
                # RIGHT: Track detail and light gun
                rx.vstack(
                    light_gun.track_detail_panel(
                        DemoSageState.get_selected_track(),
                        DemoSageState.lightgun_armed
                    ),
                    light_gun.light_gun_controls(),
                    width="350px"
                ),
                
                spacing="5",
                align="start"
            ),
            
            # Bottom: System messages
            rx.box(
                system_messages.system_messages_panel(
                    DemoSageState.system_messages_log,
                    max_height="200px"
                ),
                width="100%",
                margin_top="2rem"
            ),
            
            spacing="4",
            padding="20px"
        ),
        max_width="100%",
        background="#000000"
    )


# Create the Reflex app
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Courier+New:wght@400;700&display=swap"
    ]
)
app.add_page(demo_page, route="/")
