"""
In-App Documentation: How SAGE Works

Requirement #10: Documentation of the Loop

Short in-app panel explaining the SAGE operational loop:
Radar → Track File → Operator Designation → Weapons

New users can understand what they're actually simulating.
"""

import reflex as rx


def sage_loop_documentation() -> rx.Component:
    """
    Educational panel explaining the SAGE operational loop
    Can be shown as modal or sidebar panel
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.heading(
                "HOW SAGE WORKS",
                size="7",
                color="#00ff00",
                font_family="Courier New",
                text_align="center"
            ),
            rx.text(
                "Semi-Automatic Ground Environment Air Defense System",
                font_size="12px",
                color="#88ff88",
                text_align="center",
                font_style="italic"
            ),
            
            rx.divider(border_color="#00ff00", margin="20px 0"),
            
            # The operational loop
            rx.heading(
                "THE OPERATIONAL LOOP",
                size="5",
                color="#ffff00",
                margin_bottom="15px"
            ),
            
            # Step 1: Radar
            sage_loop_step(
                number="1",
                title="RADAR DETECTION",
                icon="📡",
                color="#ffffff",
                description="""
Ground-based radar stations scan the skies continuously.
When an aircraft enters defended airspace, radar waves bounce
back and create a "blip" on the scope.

The radar provides:
• Position (range and bearing)
• Altitude (from height-finding radar)
• Speed and heading (from successive scans)
• Initial track correlation (is this the same aircraft?)
"""
            ),
            
            # Step 2: Track File
            sage_loop_step(
                number="2",
                title="TRACK FILE CREATION",
                icon="📋",
                color="#00ff88",
                description="""
The AN/FSQ-7 computer processes raw radar data and creates
a "track file" for each detected aircraft.

Track file contains:
• Unique identification number
• Position history (last 20+ positions)
• Velocity vector (speed and direction)
• Altitude profile
• Friend-or-Foe classification (IFF transponder)
• Threat assessment (based on heading, speed, altitude)

The computer updates track files every few seconds as new
radar data arrives. This is "REAL-TIME PROCESSING" - a
revolutionary concept in 1958!
"""
            ),
            
            # Step 3: Operator Designation
            sage_loop_step(
                number="3",
                title="OPERATOR DESIGNATION",
                icon="👤",
                color="#ffff00",
                description="""
YOU are the operator at the console.

Your job:
1. Monitor the radar display for threats
2. Use the LIGHT GUN to select suspicious tracks
3. Inspect track details (altitude, speed, heading, IFF)
4. DESIGNATE hostile tracks for intercept
5. Coordinate with other operators and sectors

The light gun was revolutionary - one of the first
"point and click" interfaces in computing history!

Decision-making is critical:
• Is this friendly or hostile?
• What's the threat level?
• Which interceptor base is closest?
• Are there multiple targets (prioritize!)?
"""
            ),
            
            # Step 4: Weapons Assignment
            sage_loop_step(
                number="4",
                title="WEAPONS ASSIGNMENT",
                icon="⚡",
                color="#00ffff",
                description="""
Once you designate a hostile track, the computer:

1. Identifies nearest interceptor base
2. Calculates optimal intercept course
3. Transmits orders to scramble fighters
4. Provides continuous guidance to pilot
5. Updates intercept solution as target moves

The interceptor (F-106 Delta Dart, F-101 Voodoo, etc.)
launches and follows computer guidance to intercept point.

SAGE could track hundreds of aircraft and coordinate
dozens of intercepts simultaneously - across the entire
continental United States!
"""
            ),
            
            # Step 5: Confirmation
            sage_loop_step(
                number="5",
                title="INTERCEPT & CONFIRMATION",
                icon="✓",
                color="#00ff00",
                description="""
Final phase:

• Interceptor closes on target (you monitor on scope)
• Pilot makes visual identification
• If hostile: engage with weapons
• If friendly: break off and investigate
• Report results back to SAGE

The computer logs all actions and updates the "big picture"
shared across all 24 SAGE direction centers.

SUCCESS: Hostile neutralized, airspace defended.
"""
            ),
            
            rx.divider(border_color="#00ff00", margin="20px 0"),
            
            # Why SAGE Mattered
            rx.heading(
                "WHY SAGE MATTERED",
                size="5",
                color="#ff8800",
                margin_bottom="10px"
            ),
            
            rx.vstack(
                innovation_point("Real-Time Computing", "First large-scale system to process data as it arrived"),
                innovation_point("Interactive Graphics", "Light gun interface predated the mouse by 20 years"),
                innovation_point("Networking", "24 centers connected via modems and phone lines"),
                innovation_point("Distributed Computing", "Shared data and coordinated actions across continent"),
                innovation_point("Human-Computer Partnership", "Operators and computers working together"),
                innovation_point("High Availability", "Dual redundant systems, hot backup, 24/7 operation"),
                spacing="3",
                width="100%",
                margin_bottom="20px"
            ),
            
            # Historical Context
            rx.box(
                rx.vstack(
                    rx.text(
                        "HISTORICAL CONTEXT",
                        font_weight="bold",
                        color="#ffff00"
                    ),
                    rx.text(
                        """
During the Cold War (1950s-1980s), the primary threat was
Soviet bomber attack carrying nuclear weapons. SAGE was
America's "shield" - defending against this threat.

Cost: $8 billion ($100+ billion in 2025 dollars)
Deployment: 1958-1983 (25 years)
Coverage: All of North America
Scale: 24 direction centers, 58,000 vacuum tubes per site

SAGE never fired a shot in anger. But it worked - Soviet
strategists knew penetrating SAGE was nearly impossible.
The system was a DETERRENT through capability.

Many modern computing concepts trace back to SAGE:
• Interactive computing
• Computer graphics
• Computer networking
• Distributed databases
• Human-computer interaction
• Real-time operating systems
• Fault-tolerant design
""",
                        font_size="11px",
                        color="#88ff88",
                        white_space="pre-wrap"
                    ),
                    spacing="2"
                ),
                padding="15px",
                background="#001100",
                border="2px solid #00ff00",
                border_radius="8px"
            ),
            
            # Close button
            rx.button(
                "UNDERSTOOD - BEGIN OPERATIONS",
                size="4",
                color_scheme="green",
                width="100%",
                on_click=lambda: [],  # TODO: Close documentation
                style={
                    "font_family": "Courier New",
                    "font_size": "16px",
                    "font_weight": "bold",
                    "margin_top": "30px"
                }
            ),
            
            spacing="4",
            width="100%",
            padding="30px"
        ),
        background="#000000",
        border="4px solid #00ff00",
        border_radius="12px",
        max_width="900px",
        max_height="90vh",
        overflow_y="auto",
        style={
            "scrollbar-width": "thin",
            "scrollbar-color": "#00ff00 #000000"
        }
    )


def sage_loop_step(number: str, title: str, icon: str, color: str, description: str) -> rx.Component:
    """Single step in the SAGE operational loop"""
    return rx.box(
        rx.hstack(
            # Step number circle
            rx.box(
                rx.text(
                    number,
                    font_size="32px",
                    font_weight="bold",
                    color=color,
                    font_family="Courier New"
                ),
                width="60px",
                height="60px",
                border=f"3px solid {color}",
                border_radius="50%",
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0"
            ),
            
            # Content
            rx.vstack(
                rx.hstack(
                    rx.text(icon, font_size="24px"),
                    rx.heading(title, size="4", color=color),
                    spacing="3",
                    align="center"
                ),
                rx.text(
                    description,
                    font_size="12px",
                    color="#00ff88",
                    white_space="pre-wrap"
                ),
                align_items="start",
                spacing="2",
                flex_grow="1"
            ),
            
            spacing="4",
            align="start",
            width="100%"
        ),
        padding="20px",
        background="#001100",
        border=f"2px solid {color}44",
        border_radius="8px",
        width="100%",
        margin_bottom="15px"
    )


def innovation_point(title: str, description: str) -> rx.Component:
    """Single innovation point"""
    return rx.hstack(
        rx.text("•", font_size="20px", color="#ff8800", flex_shrink="0"),
        rx.vstack(
            rx.text(
                title,
                font_weight="bold",
                color="#ffaa00",
                font_size="12px"
            ),
            rx.text(
                description,
                font_size="11px",
                color="#888888"
            ),
            align_items="start",
            spacing="0",
            flex_grow="1"
        ),
        spacing="3",
        align="start",
        width="100%"
    )


def sage_loop_quick_reference() -> rx.Component:
    """
    Compact quick reference card
    Always accessible in UI corner
    """
    return rx.box(
        rx.vstack(
            rx.text(
                "SAGE LOOP",
                font_weight="bold",
                font_size="11px",
                color="#00ff00"
            ),
            rx.vstack(
                rx.text("1. 📡 Radar", font_size="10px", color="#888888"),
                rx.text("2. 📋 Track File", font_size="10px", color="#888888"),
                rx.text("3. 👤 Designate", font_size="10px", color="#888888"),
                rx.text("4. ⚡ Assign", font_size="10px", color="#888888"),
                rx.text("5. ✓ Confirm", font_size="10px", color="#888888"),
                spacing="1",
                align_items="start"
            ),
            rx.button(
                "Learn More",
                size="1",
                variant="soft",
                color_scheme="green",
                width="100%",
                on_click=lambda: [],  # TODO: Open full documentation
                style={
                    "font_family": "Courier New",
                    "font_size": "9px",
                    "margin_top": "10px"
                }
            ),
            spacing="3",
            width="100%"
        ),
        background="#000000",
        border="1px solid #00ff00",
        border_radius="4px",
        padding="12px",
        width="150px",
        position="fixed",
        bottom="20px",
        left="20px",
        z_index="800"
    )


def first_time_welcome() -> rx.Component:
    """
    First-time user welcome with option to learn about SAGE
    """
    return rx.box(
        rx.vstack(
            rx.heading(
                "WELCOME TO SAGE",
                size="8",
                color="#00ff00",
                text_align="center"
            ),
            
            rx.text(
                "You are about to operate the AN/FSQ-7 computer",
                font_size="16px",
                color="#88ff88",
                text_align="center"
            ),
            
            rx.text(
                "Would you like to learn how the SAGE system works?",
                font_size="14px",
                color="#888888",
                text_align="center",
                margin_top="20px"
            ),
            
            rx.hstack(
                rx.button(
                    rx.vstack(
                        rx.text("📚", font_size="32px"),
                        rx.text("LEARN ABOUT SAGE", font_size="14px"),
                        rx.text("(Recommended for first-time users)", font_size="10px", color="#888888"),
                        spacing="2"
                    ),
                    size="4",
                    color_scheme="green",
                    on_click=lambda: [],  # TODO: Show documentation
                    style={
                        "font_family": "Courier New",
                        "padding": "30px",
                        "flex": 1
                    }
                ),
                rx.button(
                    rx.vstack(
                        rx.text("⚡", font_size="32px"),
                        rx.text("START OPERATIONS", font_size="14px"),
                        rx.text("(Skip tutorial)", font_size="10px", color="#888888"),
                        spacing="2"
                    ),
                    size="4",
                    variant="soft",
                    color_scheme="gray",
                    on_click=lambda: [],  # TODO: Skip to main screen
                    style={
                        "font_family": "Courier New",
                        "padding": "30px",
                        "flex": 1
                    }
                ),
                spacing="4",
                width="100%",
                margin_top="30px"
            ),
            
            spacing="4",
            width="100%",
            max_width="800px",
            padding="40px"
        ),
        background="#000000",
        border="4px solid #00ff00",
        border_radius="12px",
        position="fixed",
        top="50%",
        left="50%",
        transform="translate(-50%, -50%)",
        z_index="1000"
    )
