"""
Scenario Selector Component

Provides UI controls to switch between different demo scenarios
for testing and demonstration purposes.
"""

import reflex as rx


def scenario_selector_panel(
    current_scenario: str,
    on_select_scenario,
) -> rx.Component:
    """
    Scenario selection dropdown and load button
    
    Args:
        current_scenario: Currently loaded scenario name
        on_select_scenario: Callback(scenario_name: str) when scenario selected
    
    Returns:
        rx.Component with scenario selector UI
    """
    
    scenarios = [
        "Demo 1 - Three Inbound",
        "Demo 2 - Mixed Friendly/Unknown",
        "Demo 3 - High Threat Saturation",
        "Demo 4 - Patrol Route",
    ]
    
    return rx.box(
        rx.vstack(
            rx.heading("SCENARIO SELECTOR", size="6", color="#00FF00"),
            rx.hstack(
                rx.select(
                    scenarios,
                    value=current_scenario,
                    on_change=on_select_scenario,
                    size="2",
                    color_scheme="green",
                    style={
                        "background": "#001100",
                        "border": "1px solid #00FF00",
                        "color": "#00FF00",
                        "font-family": "'Courier New', monospace",
                    }
                ),
                rx.text(f"Current: {current_scenario}", color="#00FF00", size="2"),
                spacing="3",
                width="100%",
            ),
            rx.text(
                "Select a scenario to test different track configurations",
                color="#00AA00",
                size="1",
            ),
            spacing="3",
            width="100%",
        ),
        padding="15px",
        background="#000000",
        border="2px solid #00FF00",
        border_radius="5px",
        style={
            "box-shadow": "0 0 10px rgba(0, 255, 0, 0.3)",
        }
    )
