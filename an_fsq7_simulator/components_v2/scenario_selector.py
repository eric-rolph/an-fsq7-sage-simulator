"""
Scenario Selector Component

Provides UI controls to switch between different demo scenarios
for testing and demonstration purposes.
"""

import reflex as rx
from an_fsq7_simulator.sim import scenarios as sim_scenarios


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
    
    # Get all available scenarios from the scenarios module
    scenarios = list(sim_scenarios.SCENARIOS.keys())
    
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
                    },
                    aria_label="Select simulation scenario. Keyboard shortcut: 1-7 for quick selection",
                    role="combobox",
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
