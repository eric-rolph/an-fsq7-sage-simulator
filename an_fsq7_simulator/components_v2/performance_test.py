"""
Performance / Overload Test Mode

Requirement #7: Performance / Overload Test

Test mode that spawns many tracks to verify:
- UI responsiveness under load
- Readability with high track density
- Filter performance
- Interaction loop still works
- Frame rate stability

Helps validate the system can handle real operational loads.
"""

import reflex as rx
import random
from typing import List
from dataclasses import dataclass


@dataclass
class PerformanceTestConfig:
    """Configuration for performance test"""
    name: str
    track_count: int
    spawn_rate: float  # Tracks per second
    test_duration: int  # Seconds
    track_mix: dict  # {"hostile": 0.4, "friendly": 0.3, "unknown": 0.3}
    altitude_distribution: dict  # {"low": 0.2, "med": 0.5, "high": 0.3}
    movement_pattern: str  # "random", "converging", "crossing", "scatter"
    description: str


# Pre-defined performance test scenarios
PERFORMANCE_TESTS = {
    "light": PerformanceTestConfig(
        name="Light Load Test",
        track_count=25,
        spawn_rate=0.5,
        test_duration=300,
        track_mix={"hostile": 0.3, "friendly": 0.4, "unknown": 0.3},
        altitude_distribution={"low": 0.2, "med": 0.5, "high": 0.3},
        movement_pattern="random",
        description="25 tracks - Typical operational load"
    ),
    
    "medium": PerformanceTestConfig(
        name="Medium Load Test",
        track_count=50,
        spawn_rate=1.0,
        test_duration=300,
        track_mix={"hostile": 0.4, "friendly": 0.3, "unknown": 0.3},
        altitude_distribution={"low": 0.3, "med": 0.4, "high": 0.3},
        movement_pattern="converging",
        description="50 tracks - Busy airspace"
    ),
    
    "heavy": PerformanceTestConfig(
        name="Heavy Load Test",
        track_count=100,
        spawn_rate=2.0,
        test_duration=300,
        track_mix={"hostile": 0.5, "friendly": 0.2, "unknown": 0.3},
        altitude_distribution={"low": 0.3, "med": 0.4, "high": 0.3},
        movement_pattern="crossing",
        description="100 tracks - Mass raid scenario"
    ),
    
    "extreme": PerformanceTestConfig(
        name="Extreme Load Test (STRESS)",
        track_count=200,
        spawn_rate=5.0,
        test_duration=300,
        track_mix={"hostile": 0.6, "friendly": 0.2, "unknown": 0.2},
        altitude_distribution={"low": 0.3, "med": 0.4, "high": 0.3},
        movement_pattern="scatter",
        description="200+ tracks - Maximum stress test"
    ),
    
    "density": PerformanceTestConfig(
        name="High Density Test",
        track_count=150,
        spawn_rate=3.0,
        test_duration=180,
        track_mix={"hostile": 0.7, "friendly": 0.1, "unknown": 0.2},
        altitude_distribution={"low": 0.5, "med": 0.3, "high": 0.2},
        movement_pattern="converging",
        description="150 tracks converging on single point - Density stress"
    )
}


@dataclass
class PerformanceMetrics:
    """Real-time performance metrics during test"""
    fps: float = 60.0  # Frames per second
    frame_time_ms: float = 16.7  # Milliseconds per frame
    track_count: int = 0
    render_time_ms: float = 0.0
    interaction_lag_ms: float = 0.0
    memory_mb: float = 0.0
    dropped_frames: int = 0
    warnings: List[str] = None


def performance_test_menu() -> rx.Component:
    """
    Menu for selecting and starting performance tests
    """
    return rx.box(
        rx.vstack(
            rx.heading(
                "PERFORMANCE TEST MODE",
                size="6",
                color="#ffaa00",
                font_family="Courier New"
            ),
            
            rx.text(
                "Stress test the simulator with high track loads",
                font_size="12px",
                color="#888888"
            ),
            
            rx.divider(border_color="#ffaa00"),
            
            # Test selection buttons
            *[performance_test_button(test_id, test_config) 
              for test_id, test_config in PERFORMANCE_TESTS.items()],
            
            rx.divider(border_color="#444444"),
            
            # Custom test configuration
            rx.text(
                "CUSTOM TEST",
                font_weight="bold",
                color="#00ff88",
                margin_top="10px"
            ),
            rx.hstack(
                rx.input(
                    placeholder="Track count...",
                    type="number",
                    size="2",
                    style={"font_family": "Courier New", "flex": 1}
                ),
                rx.button(
                    "RUN CUSTOM",
                    size="2",
                    color_scheme="cyan",
                    style={"font_family": "Courier New"}
                ),
                spacing="2",
                width="100%"
            ),
            
            spacing="3",
            width="100%"
        ),
        background="#000000",
        border="2px solid #ffaa00",
        border_radius="8px",
        padding="20px",
        width="400px"
    )


def performance_test_button(test_id: str, config: PerformanceTestConfig) -> rx.Component:
    """Button for a specific performance test"""
    # Color code by severity
    severity_colors = {
        "light": "#00ff00",
        "medium": "#ffff00",
        "heavy": "#ff8800",
        "extreme": "#ff0000",
        "density": "#ff00ff"
    }
    color = severity_colors.get(test_id, "#888888")
    
    return rx.button(
        rx.vstack(
            rx.hstack(
                rx.text(config.name, font_weight="bold", font_size="14px"),
                rx.spacer(),
                rx.badge(
                    f"{config.track_count} tracks",
                    color_scheme="gray",
                    variant="soft"
                ),
                width="100%",
                align="center"
            ),
            rx.text(
                config.description,
                font_size="11px",
                color="#888888",
                text_align="left"
            ),
            align_items="start",
            spacing="1",
            width="100%"
        ),
        width="100%",
        variant="soft",
        color_scheme="gray",
        on_click=lambda: [],  # TODO: Start test
        style={
            "font_family": "Courier New",
            "padding": "15px",
            "border": f"2px solid {color}",
            "text_align": "left"
        }
    )


def performance_metrics_overlay(metrics: PerformanceMetrics) -> rx.Component:
    """
    Real-time performance metrics overlay during test
    Shows FPS, render time, warnings
    """
    # Determine FPS health color
    fps_color = "#00ff00" if metrics.fps >= 55 else "#ffff00" if metrics.fps >= 30 else "#ff0000"
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text(
                    "⚡ PERFORMANCE TEST ACTIVE",
                    font_weight="bold",
                    color="#ffaa00"
                ),
                rx.spacer(),
                rx.button(
                    "STOP TEST",
                    size="1",
                    color_scheme="red",
                    variant="soft",
                    on_click=lambda: [],  # TODO: Stop test
                    style={"font_family": "Courier New", "font_size": "10px"}
                ),
                width="100%",
                align="center"
            ),
            
            rx.divider(border_color="#ffaa00"),
            
            # Metrics grid
            rx.grid(
                # FPS
                metric_box(
                    label="FPS",
                    value=f"{metrics.fps:.1f}",
                    color=fps_color,
                    icon="📊"
                ),
                
                # Frame time
                metric_box(
                    label="FRAME TIME",
                    value=f"{metrics.frame_time_ms:.1f}ms",
                    color="#00ff88",
                    icon="⏱"
                ),
                
                # Track count
                metric_box(
                    label="TRACKS",
                    value=str(metrics.track_count),
                    color="#00ffff",
                    icon="◉"
                ),
                
                # Render time
                metric_box(
                    label="RENDER",
                    value=f"{metrics.render_time_ms:.1f}ms",
                    color="#ffff00",
                    icon="🎨"
                ),
                
                # Interaction lag
                metric_box(
                    label="INPUT LAG",
                    value=f"{metrics.interaction_lag_ms:.0f}ms",
                    color="#ff8800" if metrics.interaction_lag_ms > 50 else "#00ff88",
                    icon="🖱"
                ),
                
                # Dropped frames
                metric_box(
                    label="DROPPED",
                    value=str(metrics.dropped_frames),
                    color="#ff0000" if metrics.dropped_frames > 10 else "#00ff00",
                    icon="⚠"
                ),
                
                columns="3",
                spacing="3",
                width="100%"
            ),
            
            # Warnings section
            rx.cond(
                len(metrics.warnings or []) > 0,
                rx.box(
                    rx.vstack(
                        rx.text(
                            "⚠ WARNINGS",
                            font_weight="bold",
                            font_size="11px",
                            color="#ff8800"
                        ),
                        rx.vstack(
                            *[rx.text(
                                f"• {warning}",
                                font_size="10px",
                                color="#ffaa00"
                            ) for warning in (metrics.warnings or [])],
                            spacing="1",
                            align_items="start"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    padding="10px",
                    background="#221100",
                    border="1px solid #ff8800",
                    border_radius="4px",
                    margin_top="10px"
                )
            ),
            
            spacing="3",
            width="100%"
        ),
        background="rgba(0, 0, 0, 0.95)",
        border="3px solid #ffaa00",
        border_radius="8px",
        padding="15px",
        width="450px",
        position="fixed",
        top="80px",
        right="20px",
        z_index="900",
        backdrop_filter="blur(10px)"
    )


def metric_box(label: str, value: str, color: str, icon: str) -> rx.Component:
    """Single metric display box"""
    return rx.box(
        rx.vstack(
            rx.text(icon, font_size="20px"),
            rx.text(
                label,
                font_size="9px",
                color="#888888",
                font_weight="bold"
            ),
            rx.text(
                value,
                font_size="16px",
                color=color,
                font_family="Courier New",
                font_weight="bold"
            ),
            spacing="1",
            align_items="center"
        ),
        padding="10px",
        background="#001100",
        border=f"1px solid {color}44",
        border_radius="4px",
        text_align="center"
    )


def performance_test_results(test_config: PerformanceTestConfig, metrics: PerformanceMetrics) -> rx.Component:
    """
    Results summary after test completes
    """
    # Calculate overall grade
    grade = "A" if metrics.fps >= 55 and metrics.interaction_lag_ms < 30 else \
            "B" if metrics.fps >= 45 and metrics.interaction_lag_ms < 50 else \
            "C" if metrics.fps >= 30 and metrics.interaction_lag_ms < 100 else \
            "D" if metrics.fps >= 20 else "F"
    
    grade_colors = {"A": "#00ff00", "B": "#88ff00", "C": "#ffff00", "D": "#ff8800", "F": "#ff0000"}
    
    return rx.box(
        rx.vstack(
            # Header
            rx.heading(
                "TEST COMPLETE",
                size="6",
                color="#00ff88",
                text_align="center"
            ),
            rx.text(
                test_config.name,
                font_size="14px",
                color="#888888",
                text_align="center"
            ),
            
            # Grade
            rx.box(
                rx.vstack(
                    rx.text("GRADE", font_size="12px", color="#888888"),
                    rx.text(
                        grade,
                        font_size="72px",
                        font_weight="bold",
                        color=grade_colors[grade],
                        font_family="Courier New"
                    ),
                    spacing="0"
                ),
                padding="30px",
                background="#001100",
                border=f"3px solid {grade_colors[grade]}",
                border_radius="8px",
                text_align="center",
                margin="20px 0"
            ),
            
            # Detailed metrics
            rx.vstack(
                result_row("Average FPS", f"{metrics.fps:.1f}", "60.0"),
                result_row("Frame Time", f"{metrics.frame_time_ms:.1f}ms", "16.7ms"),
                result_row("Max Tracks", str(metrics.track_count), f"{test_config.track_count}"),
                result_row("Input Lag", f"{metrics.interaction_lag_ms:.0f}ms", "<30ms"),
                result_row("Dropped Frames", str(metrics.dropped_frames), "0"),
                spacing="2",
                width="100%"
            ),
            
            # Recommendations
            rx.box(
                rx.vstack(
                    rx.text(
                        "RECOMMENDATIONS",
                        font_weight="bold",
                        color="#00ff88"
                    ),
                    rx.text(
                        get_recommendations(grade, metrics),
                        font_size="11px",
                        color="#888888",
                        white_space="pre-wrap"
                    ),
                    spacing="2"
                ),
                padding="15px",
                background="#001100",
                border="1px solid #00ff88",
                border_radius="4px",
                margin_top="20px"
            ),
            
            # Action buttons
            rx.hstack(
                rx.button(
                    "RUN AGAIN",
                    size="3",
                    color_scheme="green",
                    on_click=lambda: [],  # TODO: Rerun test
                    style={"font_family": "Courier New", "flex": 1}
                ),
                rx.button(
                    "CLOSE",
                    size="3",
                    variant="soft",
                    color_scheme="gray",
                    on_click=lambda: [],  # TODO: Close results
                    style={"font_family": "Courier New", "flex": 1}
                ),
                spacing="3",
                width="100%",
                margin_top="20px"
            ),
            
            spacing="4",
            width="100%",
            padding="30px"
        ),
        background="#000000",
        border="3px solid #00ff88",
        border_radius="12px",
        max_width="600px",
        position="fixed",
        top="50%",
        left="50%",
        transform="translate(-50%, -50%)",
        z_index="1000"
    )


def result_row(label: str, actual: str, target: str) -> rx.Component:
    """Single result row showing actual vs target"""
    return rx.hstack(
        rx.text(label, font_size="11px", color="#888888", width="120px"),
        rx.text(actual, font_size="12px", color="#00ff00", font_family="Courier New", width="80px"),
        rx.text(f"(target: {target})", font_size="10px", color="#444444"),
        spacing="3",
        align="center",
        padding="8px",
        background="#001100",
        border_radius="4px",
        width="100%"
    )


def get_recommendations(grade: str, metrics: PerformanceMetrics) -> str:
    """Get performance recommendations based on results"""
    if grade == "A":
        return "Excellent performance! System handles high loads smoothly."
    elif grade == "B":
        return "Good performance. Minor frame drops under peak load.\nConsider reducing visual effects if needed."
    elif grade == "C":
        return "Acceptable performance. Noticeable lag with high track counts.\nRecommend:\n• Reduce trail length\n• Disable some overlays\n• Use filters to reduce visible tracks"
    elif grade == "D":
        return "Poor performance. System struggles with load.\nRecommend:\n• Use lighter scenarios\n• Disable trails and effects\n• Upgrade hardware if possible"
    else:  # F
        return "Unacceptable performance. System cannot handle load.\nREQUIRED:\n• Reduce track counts\n• Disable all visual effects\n• Check system resources\n• Consider hardware upgrade"
