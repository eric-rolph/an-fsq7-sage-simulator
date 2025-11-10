"""
Radar Scope Component

Displays detailed radar tracking information.
"""

import reflex as rx


def radar_scope() -> rx.Component:
    """Radar scope with target details."""
    from ..an_fsq7_simulator import FSQ7State
    
    return rx.box(
        rx.vstack(
            rx.heading(
                "RADAR TRACKING",
                size="5",
                color="#00FF00",
                font_family="monospace",
                text_shadow="0 0 10px #00FF00",
            ),
            
            rx.divider(border_color="#00FF00", opacity="0.3"),
            
            # Target list
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID", color="#00FF00", font_family="monospace"),
                            rx.table.column_header_cell("TYPE", color="#00FF00", font_family="monospace"),
                            rx.table.column_header_cell("ALT", color="#00FF00", font_family="monospace"),
                            rx.table.column_header_cell("SPD", color="#00FF00", font_family="monospace"),
                            rx.table.column_header_cell("HDG", color="#00FF00", font_family="monospace"),
                            rx.table.column_header_cell("THREAT", color="#00FF00", font_family="monospace"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            FSQ7State.radar_targets,
                            lambda target: rx.table.row(
                                rx.table.cell(
                                    target["target_id"],
                                    color=rx.cond(
                                        target["target_id"] == FSQ7State.selected_target,
                                        "#FFFF00",
                                        "#00FF00"
                                    ),
                                    font_family="monospace",
                                    font_size="11px",
                                    font_weight=rx.cond(
                                        target["target_id"] == FSQ7State.selected_target,
                                        "bold",
                                        "normal"
                                    ),
                                ),
                                rx.table.cell(
                                    target["target_type"],
                                    color="#00FFFF",
                                    font_family="monospace",
                                    font_size="11px",
                                ),
                                rx.table.cell(
                                    f"{target['altitude']} ft",
                                    color="#FFFF00",
                                    font_family="monospace",
                                    font_size="11px",
                                ),
                                rx.table.cell(
                                    f"{target['speed']} kts",
                                    color="#FFFF00",
                                    font_family="monospace",
                                    font_size="11px",
                                ),
                                rx.table.cell(
                                    f"{target['heading']}°",
                                    color="#FFFF00",
                                    font_family="monospace",
                                    font_size="11px",
                                ),
                                rx.table.cell(
                                    target["threat_level"],
                                    color=rx.cond(
                                        target["threat_level"] == "HIGH",
                                        "#FF0000",
                                        rx.cond(
                                            target["threat_level"] == "MEDIUM",
                                            "#FF8800",
                                            "#00FF00"
                                        ),
                                    ),
                                    font_family="monospace",
                                    font_size="11px",
                                    font_weight=rx.cond(
                                        target["threat_level"] == "HIGH",
                                        "bold",
                                        "normal"
                                    ),
                                ),
                                background=rx.cond(
                                    target["target_id"] == FSQ7State.selected_target,
                                    "rgba(255, 255, 0, 0.1)",
                                    "transparent"
                                ),
                            ),
                        ),
                    ),
                    variant="surface",
                    size="1",
                ),
                max_height="300px",
                overflow_y="auto",
                width="100%",
            ),
            
            # Summary statistics
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "TRACKED",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    rx.text(
                        f"{FSQ7State.tracked_objects}",
                        color="#FFFF00",
                        font_family="monospace",
                        font_size="16px",
                        font_weight="bold",
                    ),
                    spacing="0",
                    align_items="center",
                ),
                rx.divider(orientation="vertical", border_color="#00FF00"),
                rx.vstack(
                    rx.text(
                        "INTERCEPTS",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    rx.text(
                        f"{FSQ7State.intercept_courses}",
                        color="#FF8800",
                        font_family="monospace",
                        font_size="16px",
                        font_weight="bold",
                    ),
                    spacing="0",
                    align_items="center",
                ),
                rx.divider(orientation="vertical", border_color="#00FF00"),
                rx.vstack(
                    rx.text(
                        "SUCCESS",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="10px",
                    ),
                    rx.text(
                        f"{FSQ7State.successful_intercepts}",
                        color="#00FF00",
                        font_family="monospace",
                        font_size="16px",
                        font_weight="bold",
                    ),
                    spacing="0",
                    align_items="center",
                ),
                width="100%",
                justify="between",
                padding="10px",
                background="rgba(0, 50, 0, 0.3)",
                border="2px solid #00FF00",
                border_radius="5px",
            ),
            
            spacing="3",
            width="100%",
        ),
        
        background="rgba(0, 20, 0, 0.5)",
        padding="15px",
        border="3px solid #00FF00",
        border_radius="10px",
        box_shadow="0 0 20px rgba(0, 255, 0, 0.3)",
    )
