"""
Unit tests for CPN tokens module
"""

import pytest
import numpy as np
from src.cpn.tokens import (
    Scenario, StateInterference, Coordinate, Signal, SignalList,
    SignalListWithTime, ObservationData, PositionEstimate, ErrorMetric
)


def test_scenario_enum():
    """Test Scenario enum values."""
    assert Scenario.OPEN_AREA.value == "OpenArea"
    assert Scenario.MOUNTAIN.value == "Mountain"
    assert Scenario.TUNNEL.value == "Tunnel"


def test_interference_enum():
    """Test StateInterference enum values."""
    assert StateInterference.NORMAL.value == "Normal"
    assert StateInterference.AM.value == "AM"
    assert StateInterference.FM.value == "FM"
    assert StateInterference.PULSE.value == "Pulse"


def test_coordinate_creation():
    """Test Coordinate dataclass."""
    coord = Coordinate(x=100.0, y=200.0, z=50.0)
    assert coord.x == 100.0
    assert coord.y == 200.0
    assert coord.z == 50.0


def test_signal_creation():
    """Test Signal dataclass."""
    signal = Signal(
        id=1,
        psr=20000000.0,
        psr_rate=100.0,
        x=1000.0, y=2000.0, z=3000.0,
        vx=10.0, vy=20.0, vz=30.0,
        clk=0.001,
        azimuth=45.0,
        elevation=30.0,
        rate_clock=0.0
    )
    assert signal.id == 1
    assert signal.psr == 20000000.0
    assert signal.elevation == 30.0


def test_signal_list_with_time():
    """Test SignalListWithTime dataclass."""
    signals = [
        Signal(1, 20000000.0, 100.0, 1000, 2000, 3000, 10, 20, 30, 0.001, 45, 30, 0),
        Signal(2, 21000000.0, 110.0, 1100, 2100, 3100, 11, 21, 31, 0.001, 50, 35, 0)
    ]
    
    signal_list = SignalListWithTime(
        timestamp=1000,
        sequence_number=1,
        signals=signals
    )
    
    assert signal_list.timestamp == 1000
    assert signal_list.sequence_number == 1
    assert len(signal_list.signals) == 2


def test_position_estimate():
    """Test PositionEstimate dataclass."""
    pos = Coordinate(x=100.0, y=200.0, z=50.0)
    vel = Coordinate(x=10.0, y=5.0, z=0.0)
    
    estimate = PositionEstimate(
        timestamp=1.0,
        position=pos,
        velocity=vel,
        clock_bias=0.001,
        dop={'GDOP': 2.5}
    )
    
    assert estimate.timestamp == 1.0
    assert estimate.position.x == 100.0
    assert estimate.velocity.x == 10.0
    assert estimate.clock_bias == 0.001
    assert estimate.dop['GDOP'] == 2.5


def test_error_metric():
    """Test ErrorMetric dataclass."""
    ref_pos = Coordinate(x=100.0, y=200.0, z=50.0)
    est_pos = Coordinate(x=102.0, y=201.0, z=51.0)
    
    error = ErrorMetric(
        timestamp=1.0,
        reference_position=ref_pos,
        estimated_position=est_pos,
        error_distance=np.sqrt(2**2 + 1**2 + 1**2),
        error_east=2.0,
        error_north=1.0,
        error_up=1.0
    )
    
    assert error.timestamp == 1.0
    assert error.error_east == 2.0
    assert error.error_north == 1.0
    assert error.error_up == 1.0
    assert abs(error.error_distance - np.sqrt(6)) < 0.01


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
