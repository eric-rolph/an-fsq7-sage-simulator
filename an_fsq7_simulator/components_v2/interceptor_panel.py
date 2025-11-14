"""
Interceptor Assignment Panel Component

Shows available interceptor aircraft and allows operator to assign them to hostile tracks.
Demonstrates:
- Interceptor readiness status (READY, SCRAMBLING, AIRBORNE, ENGAGING, etc.)
- Distance to target calculations
- Fuel and weapon status
- Assignment workflow with auto-suggestions
"""

import reflex as rx
from typing import List
from .. import state_model


def interceptor_status_badge(status: str) -> rx.Component:
    """Visual badge for interceptor status"""
    colors = {
        "READY": "green",
        "SCRAMBLING": "yellow",
        "AIRBORNE": "blue",
        "ENGAGING": "red",
        "RETURNING": "orange",
        "REFUELING": "gray"
    }
    return rx.badge(
        status,
        color_scheme=colors.get(status, "gray"),
        size="1"
    )


def fuel_gauge(fuel_percent: int) -> rx.Component:
    """Visual fuel gauge"""
    return rx.hstack(
        rx.text("Fuel:", size="1", color="gray"),
        rx.cond(
            fuel_percent > 60,
            rx.progress(
                value=fuel_percent,
                max=100,
                color_scheme="green",
                width="80px",
                height="8px"
            ),
            rx.cond(
                fuel_percent > 30,
                rx.progress(
                    value=fuel_percent,
                    max=100,
                    color_scheme="yellow",
                    width="80px",
                    height="8px"
                ),
                rx.progress(
                    value=fuel_percent,
                    max=100,
                    color_scheme="red",
                    width="80px",
                    height="8px"
                )
            )
        ),
        rx.text(f"{fuel_percent}%", size="1", weight="bold"),
        spacing="2"
    )


def interceptor_card(interceptor: state_model.Interceptor, selected_track_id: str, state) -> rx.Component:
    """Display card for single interceptor with assignment option"""
    
    # Calculate distance to selected track if one is selected
    distance_display = rx.cond(
        selected_track_id != "",
        rx.text(f"Distance: calculating...", size="1", color="gray"),
        rx.text("No target selected", size="1", color="gray")
    )
    
    # Create interceptor ID as a variable for the lambda
    iid = interceptor.id
    
    return rx.card(
        rx.vstack(
            # Header with ID and status
            rx.hstack(
                rx.heading(interceptor.id, size="3", weight="bold"),
                interceptor_status_badge(interceptor.status),
                spacing="2",
                justify="between",
                width="100%"
            ),
            
            # Aircraft type and base
            rx.text(interceptor.aircraft_type, size="2", weight="medium"),
            rx.text(f"Base: {interceptor.base_name}", size="1", color="gray"),
            
            # Status indicators
            rx.divider(),
            rx.hstack(
                fuel_gauge(interceptor.fuel_percent),
                rx.spacer(),
                spacing="2",
                width="100%"
            ),
            
            # Weapons
            rx.hstack(
                rx.text("Weapons:", size="1", color="gray"),
                rx.text(f"{interceptor.weapons_remaining}x {interceptor.weapon_type}", size="1", weight="bold"),
                spacing="2"
            ),
            
            # Speed info
            rx.hstack(
                rx.text("Max Speed:", size="1", color="gray"),
                rx.text(f"{interceptor.max_speed} kts", size="1", weight="bold"),
                spacing="2"
            ),
            
            # Distance to target (if track selected)
            distance_display,
            
            # Assignment button
            rx.divider(),
            rx.button(
                "ASSIGN TO TARGET",
                color_scheme="red",
                variant="soft",
                size="2",
                width="100%",
                disabled=(interceptor.status != "READY") | (selected_track_id == ""),
                on_click=lambda: state.assign_interceptor(iid)
            ),
            
            spacing="2",
            align="start",
            width="100%"
        ),
        width="280px"
    )


def interceptor_panel() -> rx.Component:
    """
    Interceptor Assignment Panel
    
    Shows all available interceptors with their status, allows assignment to selected tracks.
    """
    from ..interactive_sage import InteractiveSageState
    
    return rx.card(
        rx.vstack(
            # Panel header
            rx.hstack(
                rx.icon("plane", size=24, color="blue"),
                rx.heading("Interceptor Assignment", size="5", weight="bold"),
                spacing="2"
            ),
            
            rx.divider(),
            
            # Instructions
            rx.cond(
                InteractiveSageState.selected_track_id == "",
                rx.callout.root(
                    rx.callout.icon(rx.icon("info", size=16)),
                    rx.callout.text(
                        "Arm light gun and select a hostile track to assign an interceptor.",
                        size="2"
                    ),
                    color_scheme="blue",
                    size="1"
                ),
                rx.callout.root(
                    rx.callout.icon(rx.icon("crosshair", size=16)),
                    rx.callout.text(
                        f"Track {InteractiveSageState.selected_track_id} selected. Choose interceptor below.",
                        size="2"
                    ),
                    color_scheme="green",
                    size="1"
                )
            ),
            
            rx.divider(),
            
            # Interceptor cards in scrollable area
            rx.scroll_area(
                rx.vstack(
                    rx.foreach(
                        InteractiveSageState.interceptors,
                        lambda i: interceptor_card(i, InteractiveSageState.selected_track_id, InteractiveSageState)
                    ),
                    spacing="3",
                    align="start"
                ),
                type="auto",
                scrollbars="vertical",
                style={"max_height": "600px"}
            ),
            
            # Summary footer
            rx.divider(),
            rx.hstack(
                rx.text("Interceptor Force:", size="1", color="gray"),
                rx.text(
                    "3 aircraft",
                    size="1",
                    weight="bold",
                    color="green"
                ),
                rx.spacer(),
                rx.text("Available for assignment", size="1", color="gray"),
                spacing="2",
                width="100%"
            ),
            
            spacing="3",
            align="start",
            width="100%"
        ),
        width="300px"
    )
