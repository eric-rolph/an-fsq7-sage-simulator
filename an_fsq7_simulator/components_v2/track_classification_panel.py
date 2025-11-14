"""
Track Classification Panel

Manual track classification UI for uncorrelated tracks.
Supports Ada's learning objective: Understanding detect → correlate → classify workflow.

Design Principles:
- Shows why auto-correlation failed (system transparency)
- Provides clear classification options (hostile/friendly/unknown/ignore)
- Gives immediate visual feedback on radar scope (meaningful play)
- Mirrors real SAGE operator workflow (cognitive fidelity)
"""

import reflex as rx
from typing import Optional


def track_classification_panel(
    track_id: str,
    track_type: str,
    correlation_state: str,
    confidence_level: str,
    altitude: int,
    speed: int,
    heading: int,
    x: float,
    y: float,
    on_classify_hostile = None,
    on_classify_friendly = None,
    on_classify_unknown = None,
    on_ignore = None,
    on_close = None
) -> rx.Component:
    """
    Track classification panel for manual correlation override.
    
    Appears when operator clicks uncorrelated track with light gun.
    Provides context and classification options.
    
    Args:
        track_id: Track identifier
        track_type: Current classification
        correlation_state: uncorrelated/correlating/correlated
        confidence_level: low/medium/high/unknown
        altitude: Track altitude in feet
        speed: Track speed in knots
        heading: Track heading in degrees
        x, y: Track position (normalized 0-1)
        on_classify_*: Event handlers for classification
        on_close: Handler for closing panel
    """
    
    # Determine why correlation failed
    correlation_issue = "Unknown correlation issue"
    if correlation_state == "uncorrelated":
        if confidence_level == "low":
            correlation_issue = "Weak radar return signal"
        elif speed > 600:
            correlation_issue = "Velocity exceeds known aircraft profiles"
        elif altitude > 60000:
            correlation_issue = "Altitude exceeds normal flight envelope"
        else:
            correlation_issue = "No IFF response received"
    
    return rx.box(
        # Header
        rx.hstack(
            rx.heading(
                f"CLASSIFY TRACK {track_id}",
                size="5",
                color="rgb(0, 255, 100)",
                font_family="'Courier New', monospace",
            ),
            rx.button(
                "✕",
                on_click=on_close,
                size="2",
                variant="ghost",
                color="rgb(0, 255, 100)",
                cursor="pointer",
            ),
            justify="between",
            width="100%",
            padding_bottom="1em",
            border_bottom="1px solid rgba(0, 255, 100, 0.3)",
        ),
        
        # Correlation Status
        rx.vstack(
            rx.text(
                "CORRELATION STATUS",
                font_weight="bold",
                color="rgb(0, 255, 100)",
                font_family="'Courier New', monospace",
                font_size="0.9em",
            ),
            rx.hstack(
                rx.box(
                    width="12px",
                    height="12px",
                    border_radius="50%",
                    background=rx.cond(
                        correlation_state == "uncorrelated",
                        "rgb(255, 255, 0)",
                        rx.cond(
                            correlation_state == "correlating",
                            "rgb(255, 165, 0)",
                            "rgb(0, 255, 0)"
                        )
                    ),
                    box_shadow="0 0 10px rgba(255, 255, 0, 0.5)",
                ),
                rx.text(
                    correlation_state.upper(),
                    color="rgb(255, 255, 0)",
                    font_family="'Courier New', monospace",
                ),
                align_items="center",
            ),
            rx.text(
                f"Confidence: {confidence_level.upper()}",
                color="rgba(0, 255, 100, 0.7)",
                font_family="'Courier New', monospace",
                font_size="0.85em",
            ),
            align_items="start",
            spacing="2",
            padding_y="1em",
        ),
        
        # Correlation Issue
        rx.box(
            rx.text(
                "WHY AUTO-CORRELATION FAILED:",
                font_weight="bold",
                color="rgb(255, 100, 0)",
                font_family="'Courier New', monospace",
                font_size="0.9em",
                margin_bottom="0.5em",
            ),
            rx.text(
                correlation_issue,
                color="rgb(255, 165, 0)",
                font_family="'Courier New', monospace",
                font_size="0.85em",
                line_height="1.4",
            ),
            padding="1em",
            background="rgba(255, 100, 0, 0.1)",
            border="1px solid rgba(255, 100, 0, 0.3)",
            border_radius="4px",
            margin_bottom="1em",
        ),
        
        # Track Data
        rx.vstack(
            rx.text(
                "TRACK DATA",
                font_weight="bold",
                color="rgb(0, 255, 100)",
                font_family="'Courier New', monospace",
                font_size="0.9em",
            ),
            rx.grid(
                rx.text("Altitude:", color="rgba(0, 255, 100, 0.7)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text(f"{altitude:,} ft", color="rgb(0, 255, 100)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text("Speed:", color="rgba(0, 255, 100, 0.7)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text(f"{speed} kts", color="rgb(0, 255, 100)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text("Heading:", color="rgba(0, 255, 100, 0.7)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text(f"{heading:03d}°", color="rgb(0, 255, 100)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text("Position:", color="rgba(0, 255, 100, 0.7)", font_family="'Courier New', monospace", font_size="0.85em"),
                rx.text(f"({x:.3f}, {y:.3f})", color="rgb(0, 255, 100)", font_family="'Courier New', monospace", font_size="0.85em"),
                columns="2",
                spacing="2",
                width="100%",
            ),
            align_items="start",
            spacing="2",
            padding_y="1em",
            border_top="1px solid rgba(0, 255, 100, 0.2)",
        ),
        
        # Classification Buttons
        rx.vstack(
            rx.text(
                "MANUAL CLASSIFICATION",
                font_weight="bold",
                color="rgb(0, 255, 100)",
                font_family="'Courier New', monospace",
                font_size="0.9em",
                margin_bottom="0.5em",
            ),
            rx.button(
                "HOSTILE",
                on_click=on_classify_hostile,
                width="100%",
                background="rgba(255, 0, 0, 0.2)",
                border="2px solid rgb(255, 0, 0)",
                color="rgb(255, 0, 0)",
                font_family="'Courier New', monospace",
                font_weight="bold",
                cursor="pointer",
                _hover={
                    "background": "rgba(255, 0, 0, 0.3)",
                    "box_shadow": "0 0 15px rgba(255, 0, 0, 0.5)",
                },
            ),
            rx.button(
                "FRIENDLY",
                on_click=on_classify_friendly,
                width="100%",
                background="rgba(0, 255, 0, 0.2)",
                border="2px solid rgb(0, 255, 0)",
                color="rgb(0, 255, 0)",
                font_family="'Courier New', monospace",
                font_weight="bold",
                cursor="pointer",
                _hover={
                    "background": "rgba(0, 255, 0, 0.3)",
                    "box_shadow": "0 0 15px rgba(0, 255, 0, 0.5)",
                },
            ),
            rx.button(
                "UNKNOWN",
                on_click=on_classify_unknown,
                width="100%",
                background="rgba(255, 255, 0, 0.2)",
                border="2px solid rgb(255, 255, 0)",
                color="rgb(255, 255, 0)",
                font_family="'Courier New', monospace",
                font_weight="bold",
                cursor="pointer",
                _hover={
                    "background": "rgba(255, 255, 0, 0.3)",
                    "box_shadow": "0 0 15px rgba(255, 255, 0, 0.5)",
                },
            ),
            rx.button(
                "IGNORE TRACK",
                on_click=on_ignore,
                width="100%",
                background="rgba(128, 128, 128, 0.2)",
                border="1px solid rgb(128, 128, 128)",
                color="rgb(128, 128, 128)",
                font_family="'Courier New', monospace",
                cursor="pointer",
                _hover={
                    "background": "rgba(128, 128, 128, 0.3)",
                },
            ),
            align_items="stretch",
            spacing="3",
            padding_top="1em",
            border_top="1px solid rgba(0, 255, 100, 0.2)",
        ),
        
        # Panel styling
        position="fixed",
        right="2em",
        top="50%",
        transform="translateY(-50%)",
        width="350px",
        background="rgba(0, 20, 0, 0.95)",
        border="2px solid rgb(0, 255, 100)",
        border_radius="8px",
        padding="1.5em",
        box_shadow="0 0 30px rgba(0, 255, 100, 0.3)",
        z_index="1000",
    )


def correlation_help_panel() -> rx.Component:
    """
    Help panel explaining correlation process (system transparency).
    Can be toggled on/off with ? key or help button.
    """
    return rx.box(
        rx.vstack(
            rx.heading(
                "TRACK CORRELATION",
                size="4",
                color="rgb(0, 255, 100)",
                font_family="'Courier New', monospace",
            ),
            rx.text(
                "The SAGE system automatically correlates raw radar returns into classified tracks using:",
                color="rgba(0, 255, 100, 0.9)",
                font_family="'Courier New', monospace",
                font_size="0.9em",
                line_height="1.6",
            ),
            rx.vstack(
                rx.hstack(
                    rx.box(
                        "1",
                        width="24px",
                        height="24px",
                        border_radius="50%",
                        background="rgb(0, 255, 100)",
                        color="black",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        font_weight="bold",
                    ),
                    rx.text(
                        "IFF Response - Identify Friend or Foe transponder signal",
                        color="rgb(0, 255, 100)",
                        font_family="'Courier New', monospace",
                        font_size="0.85em",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                rx.hstack(
                    rx.box(
                        "2",
                        width="24px",
                        height="24px",
                        border_radius="50%",
                        background="rgb(0, 255, 100)",
                        color="black",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Velocity Profile - Compare speed/altitude to known aircraft",
                        color="rgb(0, 255, 100)",
                        font_family="'Courier New', monospace",
                        font_size="0.85em",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                rx.hstack(
                    rx.box(
                        "3",
                        width="24px",
                        height="24px",
                        border_radius="50%",
                        background="rgb(0, 255, 100)",
                        color="black",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Flight Plan - Check against filed flight plans",
                        color="rgb(0, 255, 100)",
                        font_family="'Courier New', monospace",
                        font_size="0.85em",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                spacing="3",
                width="100%",
                padding="1em 0",
            ),
            rx.text(
                "When auto-correlation fails, operators manually classify tracks using radar characteristics and tactical judgment.",
                color="rgb(255, 255, 0)",
                font_family="'Courier New', monospace",
                font_size="0.85em",
                line_height="1.6",
                padding="1em",
                background="rgba(255, 255, 0, 0.1)",
                border_left="3px solid rgb(255, 255, 0)",
            ),
            spacing="4",
            align_items="start",
        ),
        position="fixed",
        left="2em",
        bottom="2em",
        width="400px",
        background="rgba(0, 20, 0, 0.95)",
        border="2px solid rgb(0, 255, 100)",
        border_radius="8px",
        padding="1.5em",
        box_shadow="0 0 30px rgba(0, 255, 100, 0.3)",
        z_index="900",
    )
