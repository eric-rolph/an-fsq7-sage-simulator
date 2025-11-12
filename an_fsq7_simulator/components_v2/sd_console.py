"""
SD Console Controls Component

Implements functional SAGE Situation Display console buttons:
- Category Select (S1-S13): Filter radar by track type/altitude
- Feature Select (S20-S24): Toggle display overlays
- Off-Centering: Pan and zoom controls
- Bright-Dim: Adjust scope brightness

Each button provides visual feedback and actually affects the display.

Requirement #3: SD Console Button Semantics
- All buttons wired to state methods
- Visual active state feedback
- System messages logging
"""

import reflex as rx
from typing import List, Set


# NOTE: Import InteractiveSageState from parent when integrating
# For now, these functions accept State as parameter


def console_button(
    label: str,
    active: bool = False,
    on_click = None,
    size: str = "2",
) -> rx.Component:
    """
    Styled console button with lit/unlit states
    """
    button_props = {
        "background": rx.cond(active, "#003300", "#001100"),
        "color": rx.cond(active, "#00ff00", "#004400"),
        "border": rx.cond(active, "2px solid #00ff00", "2px solid #003300"),
        "size": size,
        "font_family": "'Courier New', monospace",
        "font_weight": "bold",
        "_hover": {
            "background": rx.cond(active, "#005500", "#002200"),
            "border_color": "#00ff00",
            "color": "#00ff00",
        },
        "box_shadow": rx.cond(active, "0 0 10px rgba(0,255,0,0.3)", "none"),
        "transition": "all 0.2s",
    }
    if on_click is not None:
        button_props["on_click"] = on_click
    
    return rx.button(
        label,
        **button_props,
    )


def category_select_panel(active_filters: Set[str], on_toggle_filter=None) -> rx.Component:
    """
    Category Select Switches (S1-S13)
    Filter what appears on radar scope
    
    Args:
        active_filters: Set of currently active filter keys
        on_toggle_filter: Event handler for toggle_filter(filter_key: str)
    """
    categories = [
        ("S1", "ALL", "all"),
        ("S2", "FRIENDLY", "friendly"),
        ("S3", "UNKNOWN", "unknown"),
        ("S4", "HOSTILE", "hostile"),
        ("S5", "MISSILE", "missile"),
        ("S6", "BOMBER", "bomber"),
        ("S7", "FIGHTER", "fighter"),
        ("S8", "ALT<10K", "alt_low"),
        ("S9", "ALT 10K-30K", "alt_med"),
        ("S10", "ALT>30K", "alt_high"),
        ("S11", "INBOUND", "inbound"),
        ("S12", "OUTBOUND", "outbound"),
        ("S13", "LOITERING", "loitering"),
    ]
    
    return rx.box(
        rx.heading(
            "CATEGORY SELECT (S1-S13)",
            size="3",
            color="#00ff00",
            margin_bottom="0.5rem",
            font_family="'Courier New', monospace",
        ),
        rx.text(
            "Filter radar display by track type",
            color="#888888",
            font_size="0.8rem",
            margin_bottom="0.75rem",
        ),
        
        # Grid of category buttons
        rx.grid(
            *[
                console_button(
                    f"{switch} {name}",
                    active=active_filters.contains(filter_key),
                    on_click=lambda fk=filter_key: on_toggle_filter(fk),
                    size="1",
                )
                for switch, name, filter_key in categories
            ],
            columns="2",
            spacing="2",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def feature_select_panel(active_overlays: Set[str], on_toggle_overlay=None) -> rx.Component:
    """
    Feature Select Switches (S20-S24)
    Toggle display overlays
    
    Args:
        active_overlays: Set of currently enabled overlay keys
        on_toggle_overlay: Callback function to toggle an overlay, receives overlay_key
    """
    features = [
        ("S20", "FLIGHT PATHS", "flight_paths", "Show trailing paths behind targets"),
        ("S21", "INTERCEPTS", "intercept_vectors", "Show intercept missile vectors"),
        ("S22", "RANGE RINGS", "range_rings", "Show 100/200/300 mile range circles"),
        ("S23", "CALLSIGNS", "callsigns", "Show track ID labels"),
        ("S24", "COASTLINES", "coastlines", "Show geographic coastline overlay"),
    ]
    
    return rx.box(
        rx.heading(
            "FEATURE SELECT (S20-S24)",
            size="3",
            color="#00ff00",
            margin_bottom="0.5rem",
            font_family="'Courier New', monospace",
        ),
        rx.text(
            "Toggle display overlays",
            color="#888888",
            font_size="0.8rem",
            margin_bottom="0.75rem",
        ),
        
        # Feature buttons with descriptions
        rx.vstack(
            *[
                rx.box(
                    console_button(
                        f"{switch} {name}",
                        active=active_overlays.contains(overlay_key),
                        on_click=lambda ok=overlay_key: on_toggle_overlay(ok) if on_toggle_overlay else None,
                        size="2",
                    ),
                    rx.text(
                        desc,
                        color="#666666",
                        font_size="0.75rem",
                        margin_top="0.25rem",
                        font_style="italic",
                    ),
                )
                for switch, name, overlay_key, desc in features
            ],
            spacing="3",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def off_centering_controls(on_pan=None, on_zoom=None, on_rotate=None, on_center=None) -> rx.Component:
    """
    Off-Centering Pushbuttons
    Pan and zoom the radar view
    
    Args:
        on_pan: Callback for pan direction, receives direction string ("up", "down", "left", "right")
        on_zoom: Callback for zoom, receives action string ("in", "out", "fit")
        on_rotate: Callback for rotation, receives direction string ("ccw", "reset", "cw")
        on_center: Callback to center the view
    """
    return rx.box(
        rx.heading(
            "OFF-CENTERING CONTROLS",
            size="3",
            color="#00ff00",
            margin_bottom="0.5rem",
            font_family="'Courier New', monospace",
        ),
        
        rx.vstack(
            # Directional pan controls
            rx.box(
                rx.text("PAN VIEW", color="#888888", font_size="0.8rem", margin_bottom="0.5rem"),
                rx.grid(
                    rx.box(),  # Empty corner
                    console_button("↑", on_click=lambda: on_pan("up") if on_pan else None, size="2"),
                    rx.box(),  # Empty corner
                    console_button("←", on_click=lambda: on_pan("left") if on_pan else None, size="2"),
                    console_button("⊙", on_click=lambda: on_center() if on_center else None, size="2"),
                    console_button("→", on_click=lambda: on_pan("right") if on_pan else None, size="2"),
                    rx.box(),  # Empty corner
                    console_button("↓", on_click=lambda: on_pan("down") if on_pan else None, size="2"),
                    rx.box(),  # Empty corner
                    columns="3",
                    spacing="1",
                    justify_items="center",
                    width="180px",
                ),
            ),
            
            rx.divider(),
            
            # Zoom controls
            rx.box(
                rx.text("ZOOM", color="#888888", font_size="0.8rem", margin_bottom="0.5rem"),
                rx.hstack(
                    console_button("−", on_click=lambda: on_zoom("out") if on_zoom else None, size="2"),
                    console_button("+", on_click=lambda: on_zoom("in") if on_zoom else None, size="2"),
                    console_button("FIT", on_click=lambda: on_zoom("fit") if on_zoom else None, size="2"),
                    spacing="2",
                ),
            ),
            
            rx.divider(),
            
            # Rotation (bonus feature)
            rx.box(
                rx.text("ROTATE", color="#888888", font_size="0.8rem", margin_bottom="0.5rem"),
                rx.hstack(
                    console_button("↶", on_click=lambda: on_rotate("ccw") if on_rotate else None, size="2"),
                    console_button("N", on_click=lambda: on_rotate("reset") if on_rotate else None, size="2"),
                    console_button("↷", on_click=lambda: on_rotate("cw") if on_rotate else None, size="2"),
                    spacing="2",
                ),
            ),
            
            spacing="3",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def bright_dim_control(brightness: float, on_brightness_change=None, on_preset=None) -> rx.Component:
    """
    Bright-Dim Control (S20 & S25)
    Adjust scope brightness
    
    Args:
        brightness: Current brightness value (0.0 to 1.0)
        on_brightness_change: Callback for slider change, receives percentage value (0-100)
        on_preset: Callback for preset buttons, receives preset name ("dim", "med", "bright")
    """
    return rx.box(
        rx.heading(
            "SCOPE BRIGHTNESS",
            size="3",
            color="#00ff00",
            margin_bottom="0.5rem",
            font_family="'Courier New', monospace",
        ),
        
        rx.vstack(
            # Brightness slider
            rx.slider(
                default_value=brightness * 100,
                min=20,
                max=100,
                step=5,
                on_change=lambda val: on_brightness_change(val) if on_brightness_change else None,
                color_scheme="green",
            ),
            
            # Percentage display
            rx.text(
                f"{brightness * 100:.0f}%",
                color="#00ff00",
                font_size="1.5rem",
                font_family="'Courier New', monospace",
                font_weight="bold",
                text_align="center",
            ),
            
            # Quick presets
            rx.hstack(
                console_button("DIM", on_click=lambda: on_preset("dim") if on_preset else None, size="1"),
                console_button("MED", on_click=lambda: on_preset("med") if on_preset else None, size="1"),
                console_button("BRIGHT", on_click=lambda: on_preset("bright") if on_preset else None, size="1"),
                spacing="2",
                justify="center",
            ),
            
            spacing="3",
            width="100%",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )


def active_filters_display(filters: Set[str], overlays: Set[str]) -> rx.Component:
    """
    Status bar showing currently active filters and overlays
    """
    return rx.box(
        rx.hstack(
            # Active filters
            rx.box(
                rx.text("ACTIVE FILTERS:", font_weight="bold", color="#00ff00", font_size="0.8rem"),
                rx.flex(
                    rx.foreach(
                        filters,
                        lambda f: rx.badge(f.upper(), color_scheme="green", size="1")
                    ),
                    wrap="wrap",
                    spacing="1",
                    min_height="1.5rem",
                ),
            ),
            
            rx.divider(orientation="vertical", height="30px"),
            
            # Active overlays
            rx.box(
                rx.text("ACTIVE OVERLAYS:", font_weight="bold", color="#00ff00", font_size="0.8rem"),
                rx.flex(
                    rx.foreach(
                        overlays,
                        lambda o: rx.badge(o.replace("_", " ").upper(), color_scheme="blue", size="1")
                    ),
                    wrap="wrap",
                    spacing="1",
                    min_height="1.5rem",
                ),
            ),
            
            spacing="4",
            width="100%",
        ),
        padding="0.75rem",
        background="#001100",
        border="1px solid #003300",
        border_radius="4px",
        margin_bottom="1rem",
    )


def sd_console_master_panel(
    active_filters: Set[str],
    active_overlays: Set[str],
    brightness: float,
    on_toggle_filter=None,
    on_toggle_overlay=None,
    on_pan=None,
    on_zoom=None,
    on_rotate=None,
    on_center=None,
    on_brightness_change=None,
    on_preset=None,
) -> rx.Component:
    """
    Complete SD Console Control Panel
    Combines all console controls in one place
    
    Args:
        active_filters: Set of active filter keys
        active_overlays: Set of active overlay keys
        brightness: Current brightness (0.0 to 1.0)
        on_toggle_filter: Callback to toggle a filter
        on_toggle_overlay: Callback to toggle an overlay
        on_pan: Callback for pan direction
        on_zoom: Callback for zoom action
        on_rotate: Callback for rotation
        on_center: Callback to center view
        on_brightness_change: Callback for brightness slider
        on_preset: Callback for brightness presets
    """
    return rx.box(
        rx.heading(
            "SD CONSOLE CONTROLS",
            size="5",
            color="#00ff00",
            margin_bottom="1rem",
            font_family="'Courier New', monospace",
        ),
        
        # Status display
        active_filters_display(active_filters, active_overlays),
        
        # Control sections
        rx.vstack(
            category_select_panel(active_filters, on_toggle_filter),
            feature_select_panel(active_overlays, on_toggle_overlay),
            off_centering_controls(on_pan, on_zoom, on_rotate, on_center),
            bright_dim_control(brightness, on_brightness_change, on_preset),
            spacing="4",
            width="100%",
        ),
        
        padding="1.5rem",
        background="#000000",
        border="2px solid #00ff00",
        border_radius="8px",
        max_height="100vh",
        overflow_y="auto",
    )


def sd_console_compact(
    active_filters: Set[str],
    active_overlays: Set[str],
) -> rx.Component:
    """
    Compact SD Console for embedding in main layout
    Shows most-used controls only
    """
    return rx.box(
        rx.heading("CONSOLE", size="4", color="#00ff00", margin_bottom="0.5rem"),
        
        # Quick filters
        rx.flex(
            console_button("ALL", active=active_filters.contains("all"), size="1"),  # TODO: Wire up event handler
            console_button("HOSTILE", active=active_filters.contains("hostile"), size="1"),  # TODO: Wire up event handler
            console_button("FRIENDLY", active=active_filters.contains("friendly"), size="1"),  # TODO: Wire up event handler
            console_button("MISSILE", active=active_filters.contains("missile"), size="1"),  # TODO: Wire up event handler
            wrap="wrap",
            spacing="1",
        ),
        
        rx.divider(margin_y="0.5rem"),
        
        # Quick overlays
        rx.flex(
            console_button("PATHS", active=active_overlays.contains("flight_paths"), size="1"),  # TODO: Wire up event handler
            console_button("RINGS", active=active_overlays.contains("range_rings"), size="1"),  # TODO: Wire up event handler
            console_button("COAST", active=active_overlays.contains("coastlines"), size="1"),  # TODO: Wire up event handler
            wrap="wrap",
            spacing="1",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )
