"""
Shared test fixtures for SAGE simulator tests.
"""

import pytest
from an_fsq7_simulator import state_model
from an_fsq7_simulator.sim import models


@pytest.fixture
def sample_track():
    """Create a sample track for testing."""
    return state_model.Track(
        id="TEST-001",
        x=0.5,
        y=0.5,
        vx=0.01,
        vy=0.01,
        altitude=25000,
        speed=450,
        heading=90,
        track_type="aircraft",
        threat_level="MEDIUM",
        time_detected=0.0
    )


@pytest.fixture
def hostile_track():
    """Create a hostile track for testing."""
    track = state_model.Track(
        id="HOSTILE-001",
        x=0.25,
        y=0.75,
        vx=0.015,
        vy=-0.01,
        altitude=35000,
        speed=520,
        heading=315,
        track_type="hostile",
        threat_level="HIGH",
        time_detected=0.0,
        correlation_state="correlated",
        classification_time=1.0
    )
    return track


@pytest.fixture
def friendly_track():
    """Create a friendly track for testing."""
    track = state_model.Track(
        id="FRIENDLY-001",
        x=0.75,
        y=0.25,
        vx=-0.005,
        vy=0.005,
        altitude=22000,
        speed=380,
        heading=135,
        track_type="friendly",
        threat_level="LOW",
        time_detected=5.0,
        correlation_state="correlated",
        classification_time=6.0
    )
    return track


@pytest.fixture
def sample_interceptor():
    """Create a sample interceptor for testing."""
    return state_model.Interceptor(
        id="INT-001",
        x=0.5,
        y=0.1,
        fuel=100.0,
        weapons=2,
        aircraft_type="F-106",
        status="READY"
    )


@pytest.fixture
def sample_scenario():
    """Create a sample scenario for testing."""
    from an_fsq7_simulator.sim.scenarios import get_scenario
    return get_scenario("training")
