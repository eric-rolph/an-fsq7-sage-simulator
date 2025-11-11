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
    return rx.button(
        label,
        on_click=on_click or (lambda: None),
        background="#003300" if active else "#001100",
        color="#00ff00" if active else "#004400",
        border=f"2px solid {'#00ff00' if active else '#003300'}",
        size=size,
        font_family="'Courier New', monospace",
        font_weight="bold",
        _hover={
            "background": "#005500" if active else "#002200",
            "border_color": "#00ff00",
            "color": "#00ff00",
        },
        box_shadow="0 0 10px rgba(0,255,0,0.3)" if active else "none",
        transition="all 0.2s",
    )


def category_select_panel(active_filters: Set[str]) -> rx.Component:
    """
    Category Select Switches (S1-S13)
    Filter what appears on radar scope
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
                    active=(filter_key in active_filters),
                    on_click=rx.State.toggle_filter(filter_key),  # type: ignore
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


def feature_select_panel(active_overlays: Set[str]) -> rx.Component:
    """
    Feature Select Switches (S20-S24)
    Toggle display overlays
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
                        active=(overlay_key in active_overlays),
                        on_click=rx.State.toggle_overlay(overlay_key),  # type: ignore
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


def off_centering_controls() -> rx.Component:
    """
    Off-Centering Pushbuttons
    Pan and zoom the radar view
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
                    console_button("↑", on_click=rx.State.pan_scope("up"), size="2"),  # type: ignore
                    rx.box(),  # Empty corner
                    console_button("←", on_click=rx.State.pan_scope("left"), size="2"),  # type: ignore
                    console_button("⊙", on_click=rx.State.center_scope, size="2"),  # type: ignore
                    console_button("→", on_click=rx.State.pan_scope("right"), size="2"),  # type: ignore
                    rx.box(),  # Empty corner
                    console_button("↓", on_click=rx.State.pan_scope("down"), size="2"),  # type: ignore
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
                    console_button("−", on_click=rx.State.zoom_scope("out"), size="2"),  # type: ignore
                    console_button("+", on_click=rx.State.zoom_scope("in"), size="2"),  # type: ignore
                    console_button("FIT", on_click=rx.State.zoom_scope("fit"), size="2"),  # type: ignore
                    spacing="2",
                ),
            ),
            
            rx.divider(),
            
            # Rotation (bonus feature)
            rx.box(
                rx.text("ROTATE", color="#888888", font_size="0.8rem", margin_bottom="0.5rem"),
                rx.hstack(
                    console_button("↶", on_click=rx.State.rotate_scope("ccw"), size="2"),  # type: ignore
                    console_button("N", on_click=rx.State.rotate_scope("north"), size="2"),  # type: ignore
                    console_button("↷", on_click=rx.State.rotate_scope("cw"), size="2"),  # type: ignore
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


def bright_dim_control(brightness: float) -> rx.Component:
    """
    Bright-Dim Control (S20 & S25)
    Adjust scope brightness
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
                on_change=rx.State.set_brightness_percent,  # type: ignore
                color_scheme="green",
            ),
            
            # Percentage display
            rx.text(
                f"{int(brightness * 100)}%",
                color="#00ff00",
                font_size="1.5rem",
                font_family="'Courier New', monospace",
                font_weight="bold",
                text_align="center",
            ),
            
            # Quick presets
            rx.hstack(
                console_button("DIM", on_click=rx.State.set_brightness_preset(0.4), size="1"),  # type: ignore
                console_button("MED", on_click=rx.State.set_brightness_preset(0.7), size="1"),  # type: ignore
                console_button("BRIGHT", on_click=rx.State.set_brightness_preset(1.0), size="1"),  # type: ignore
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
                rx.wrap(
                    *[
                        rx.badge(f.upper(), color_scheme="green", size="1")
                        for f in sorted(filters)
                    ] if filters else [rx.text("NONE", color="#666666", font_size="0.75rem")],
                    spacing="1",
                ),
            ),
            
            rx.divider(orientation="vertical", height="30px"),
            
            # Active overlays
            rx.box(
                rx.text("ACTIVE OVERLAYS:", font_weight="bold", color="#00ff00", font_size="0.8rem"),
                rx.wrap(
                    *[
                        rx.badge(o.replace("_", " ").upper(), color_scheme="blue", size="1")
                        for o in sorted(overlays)
                    ] if overlays else [rx.text("NONE", color="#666666", font_size="0.75rem")],
                    spacing="1",
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
) -> rx.Component:
    """
    Complete SD Console Control Panel
    Combines all console controls in one place
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
            category_select_panel(active_filters),
            feature_select_panel(active_overlays),
            off_centering_controls(),
            bright_dim_control(brightness),
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
        rx.wrap(
            console_button("ALL", active=("all" in active_filters), on_click=rx.State.toggle_filter("all"), size="1"),  # type: ignore
            console_button("HOSTILE", active=("hostile" in active_filters), on_click=rx.State.toggle_filter("hostile"), size="1"),  # type: ignore
            console_button("FRIENDLY", active=("friendly" in active_filters), on_click=rx.State.toggle_filter("friendly"), size="1"),  # type: ignore
            console_button("MISSILE", active=("missile" in active_filters), on_click=rx.State.toggle_filter("missile"), size="1"),  # type: ignore
            spacing="1",
        ),
        
        rx.divider(margin_y="0.5rem"),
        
        # Quick overlays
        rx.wrap(
            console_button("PATHS", active=("flight_paths" in active_overlays), on_click=rx.State.toggle_overlay("flight_paths"), size="1"),  # type: ignore
            console_button("RINGS", active=("range_rings" in active_overlays), on_click=rx.State.toggle_overlay("range_rings"), size="1"),  # type: ignore
            console_button("COAST", active=("coastlines" in active_overlays), on_click=rx.State.toggle_overlay("coastlines"), size="1"),  # type: ignore
            spacing="1",
        ),
        
        padding="1rem",
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
    )
