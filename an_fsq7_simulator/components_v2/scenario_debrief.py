"""
Scenario Debrief Panel - Priority 4 Feature

Displays post-scenario performance summary with:
- Mission objectives and completion status
- Performance metrics (detection, classification, intercepts)
- Learning moments (what went right/wrong)
- Score and grade

Aligns with all three personas:
- Ada: Learning assessment and improvement feedback
- Grace: Mission realism and after-action reports
- Sam: Score improvement and achievement tracking
"""

import reflex as rx
from typing import Dict, List


def scenario_metrics_summary(
    tracks_detected: int,
    tracks_total: int,
    correct_classifications: int,
    total_classifications: int,
    successful_intercepts: int,
    attempted_intercepts: int,
    scenario_duration: float
) -> rx.Component:
    """Display performance metrics in grid"""
    
    detection_pct = (tracks_detected / tracks_total * 100) if tracks_total > 0 else 0
    classification_pct = (correct_classifications / total_classifications * 100) if total_classifications > 0 else 0
    intercept_pct = (successful_intercepts / attempted_intercepts * 100) if attempted_intercepts > 0 else 0
    
    return rx.box(
        rx.heading("PERFORMANCE METRICS", size="4", color="green"),
        rx.grid(
            # Detection
            rx.box(
                rx.text("TRACK DETECTION", size="2", weight="bold"),
                rx.text(f"{tracks_detected}/{tracks_total} tracks", size="1"),
                rx.progress(value=detection_pct, color_scheme="blue"),
                rx.text(f"{detection_pct:.1f}%", size="1", color="cyan"),
                padding="10px",
                border="1px solid rgba(0, 255, 0, 0.3)",
                border_radius="5px"
            ),
            # Classification
            rx.box(
                rx.text("CLASSIFICATION ACCURACY", size="2", weight="bold"),
                rx.text(f"{correct_classifications}/{total_classifications} correct", size="1"),
                rx.progress(value=classification_pct, color_scheme="green"),
                rx.text(f"{classification_pct:.1f}%", size="1", color="green"),
                padding="10px",
                border="1px solid rgba(0, 255, 0, 0.3)",
                border_radius="5px"
            ),
            # Intercepts
            rx.box(
                rx.text("INTERCEPT SUCCESS", size="2", weight="bold"),
                rx.text(f"{successful_intercepts}/{attempted_intercepts} successful", size="1"),
                rx.progress(value=intercept_pct, color_scheme="orange"),
                rx.text(f"{intercept_pct:.1f}%", size="1", color="orange"),
                padding="10px",
                border="1px solid rgba(0, 255, 0, 0.3)",
                border_radius="5px"
            ),
            # Duration
            rx.box(
                rx.text("MISSION DURATION", size="2", weight="bold"),
                rx.text(f"{scenario_duration:.1f} seconds", size="1"),
                padding="10px",
                border="1px solid rgba(0, 255, 0, 0.3)",
                border_radius="5px"
            ),
            columns="2",
            spacing="4",
            width="100%"
        ),
        padding="15px",
        background="rgba(0, 40, 0, 0.4)",
        border="1px solid rgba(0, 255, 0, 0.5)",
        border_radius="8px",
        margin_bottom="15px"
    )


def learning_moments_panel(learning_moments: List[Dict[str, str]]) -> rx.Component:
    """Display what went wrong and learning opportunities"""
    
    if not learning_moments:
        return rx.box(
            rx.text("✓ No critical issues detected", color="green", size="2"),
            padding="10px"
        )
    
    moment_components = []
    for moment in learning_moments:
        icon = "⚠️" if moment["severity"] == "warning" else "❌"
        color = "orange" if moment["severity"] == "warning" else "red"
        
        moment_components.append(
            rx.box(
                rx.hstack(
                    rx.text(icon, size="4"),
                    rx.box(
                        rx.text(moment["title"], weight="bold", color=color, size="2"),
                        rx.text(moment["description"], size="1", color="white"),
                        rx.text(f"💡 Tip: {moment['tip']}", size="1", color="cyan", font_style="italic"),
                    ),
                    spacing="3",
                    align="start"
                ),
                padding="10px",
                border_left=f"3px solid {color}",
                background="rgba(0, 0, 0, 0.3)",
                margin_bottom="8px"
            )
        )
    
    return rx.box(
        rx.heading("LEARNING MOMENTS", size="4", color="yellow"),
        rx.box(*moment_components),
        padding="15px",
        background="rgba(40, 40, 0, 0.3)",
        border="1px solid rgba(255, 255, 0, 0.5)",
        border_radius="8px",
        margin_bottom="15px"
    )


def objectives_panel(
    objectives: List[str],
    completed_objectives: List[bool],
    success_criteria: str
) -> rx.Component:
    """Display scenario objectives with completion status"""
    
    objective_components = []
    for i, (objective, completed) in enumerate(zip(objectives, completed_objectives)):
        icon = "✓" if completed else "○"
        color = "green" if completed else "gray"
        
        objective_components.append(
            rx.hstack(
                rx.text(icon, size="4", color=color, weight="bold"),
                rx.text(objective, size="2", color=color),
                spacing="3"
            )
        )
    
    return rx.box(
        rx.heading("MISSION OBJECTIVES", size="4", color="cyan"),
        rx.vstack(*objective_components, spacing="2", align="start"),
        rx.divider(margin="10px 0"),
        rx.text("SUCCESS CRITERIA", size="2", weight="bold", color="white"),
        rx.text(success_criteria, size="1", color="lightgray"),
        padding="15px",
        background="rgba(0, 20, 40, 0.4)",
        border="1px solid rgba(0, 200, 255, 0.5)",
        border_radius="8px",
        margin_bottom="15px"
    )


def grade_panel(overall_score: float) -> rx.Component:
    """Display overall grade and score"""
    
    # Determine grade
    if overall_score >= 90:
        grade = "A"
        grade_text = "EXCELLENT"
        grade_color = "green"
    elif overall_score >= 80:
        grade = "B"
        grade_text = "GOOD"
        grade_color = "lightgreen"
    elif overall_score >= 70:
        grade = "C"
        grade_text = "SATISFACTORY"
        grade_color = "yellow"
    elif overall_score >= 60:
        grade = "D"
        grade_text = "NEEDS IMPROVEMENT"
        grade_color = "orange"
    else:
        grade = "F"
        grade_text = "UNSATISFACTORY"
        grade_color = "red"
    
    return rx.box(
        rx.vstack(
            rx.text("MISSION GRADE", size="2", color="white"),
            rx.text(grade, size="9", weight="bold", color=grade_color),
            rx.text(grade_text, size="3", color=grade_color),
            rx.text(f"{overall_score:.1f}/100", size="4", color="white"),
            spacing="2",
            align="center"
        ),
        padding="20px",
        background="rgba(0, 0, 0, 0.6)",
        border=f"2px solid {grade_color}",
        border_radius="10px",
        text_align="center",
        width="200px"
    )


def scenario_debrief_panel(state) -> rx.Component:
    """
    Main debrief panel component - shows after scenario completion
    
    This panel appears when scenario_complete is True and displays:
    - Overall grade and score
    - Mission objectives completion
    - Performance metrics
    - Learning moments
    - Next steps
    
    State requirements:
    - scenario_complete: bool
    - scenario_metrics: Dict with keys:
        - tracks_detected, tracks_total
        - correct_classifications, total_classifications
        - successful_intercepts, attempted_intercepts
        - scenario_duration
        - overall_score
        - objectives, completed_objectives, success_criteria
        - learning_moments: List[Dict[str, str]]
    """
    
    # Extract metrics from state
    metrics = state.scenario_metrics
    
    return rx.cond(
        state.scenario_complete,
        rx.box(
            # Header
            rx.box(
                rx.hstack(
                    rx.text("📋", size="8"),
                    rx.heading("MISSION DEBRIEF", size="7", color="green"),
                    spacing="3"
                ),
                padding="20px",
                background="rgba(0, 50, 0, 0.5)",
                border_bottom="2px solid rgba(0, 255, 0, 0.7)"
            ),
            
            # Content
            rx.box(
                rx.hstack(
                    # Left column: Grade and objectives
                    rx.vstack(
                        grade_panel(metrics.get("overall_score", 0)),
                        objectives_panel(
                            metrics.get("objectives", []),
                            metrics.get("completed_objectives", []),
                            metrics.get("success_criteria", "")
                        ),
                        spacing="4",
                        width="300px"
                    ),
                    
                    # Right column: Metrics and learning moments
                    rx.vstack(
                        scenario_metrics_summary(
                            metrics.get("tracks_detected", 0),
                            metrics.get("tracks_total", 0),
                            metrics.get("correct_classifications", 0),
                            metrics.get("total_classifications", 0),
                            metrics.get("successful_intercepts", 0),
                            metrics.get("attempted_intercepts", 0),
                            metrics.get("scenario_duration", 0.0)
                        ),
                        learning_moments_panel(metrics.get("learning_moments", [])),
                        spacing="4",
                        flex="1"
                    ),
                    spacing="5",
                    align="start",
                    width="100%"
                ),
                padding="20px"
            ),
            
            # Footer with actions
            rx.box(
                rx.hstack(
                    rx.button(
                        "CONTINUE",
                        on_click=state.close_debrief,
                        size="3",
                        color_scheme="green",
                        cursor="pointer"
                    ),
                    rx.button(
                        "REPLAY SCENARIO",
                        on_click=state.restart_scenario,
                        size="3",
                        color_scheme="blue",
                        cursor="pointer"
                    ),
                    rx.button(
                        "NEXT SCENARIO",
                        on_click=state.next_scenario,
                        size="3",
                        color_scheme="cyan",
                        cursor="pointer"
                    ),
                    spacing="4",
                    justify="center"
                ),
                padding="15px",
                background="rgba(0, 0, 0, 0.5)",
                border_top="1px solid rgba(0, 255, 0, 0.3)"
            ),
            
            # Modal overlay
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width="90%",
            max_width="1200px",
            max_height="90vh",
            overflow_y="auto",
            background="rgba(0, 0, 0, 0.95)",
            border="2px solid rgba(0, 255, 0, 0.8)",
            border_radius="10px",
            box_shadow="0 0 30px rgba(0, 255, 0, 0.5)",
            z_index="9999"
        ),
        rx.fragment()  # Empty when not showing debrief
    )
