"""
Unit tests for GNSS positioning module
"""

import pytest
import numpy as np
from src.cpn.tokens import Signal, Coordinate
from src.gnss.positioning import (
    calculate_satellite_position,
    least_squares_positioning,
    calculate_position_from_signals,
    calculate_position_error
)


def create_test_signals(n_satellites=4):
    """Create test satellite signals."""
    signals = []
    
    # Create signals from satellites at known positions
    for i in range(n_satellites):
        angle = 2 * np.pi * i / n_satellites
        sat_distance = 20000000.0  # 20,000 km
        
        sat_x = sat_distance * np.cos(angle)
        sat_y = sat_distance * np.sin(angle)
        sat_z = sat_distance * 0.5
        
        # True receiver position
        recv_x, recv_y, recv_z = 0.0, 0.0, 0.0
        
        # True geometric range
        true_range = np.sqrt((sat_x - recv_x)**2 + (sat_y - recv_y)**2 + (sat_z - recv_z)**2)
        
        signal = Signal(
            id=i+1,
            psr=true_range,  # No noise for this test
            psr_rate=0.0,
            x=sat_x, y=sat_y, z=sat_z,
            vx=0.0, vy=0.0, vz=0.0,
            clk=0.0,
            azimuth=0.0,
            elevation=45.0,
            rate_clock=0.0
        )
        signals.append(signal)
    
    return signals


def test_calculate_satellite_position():
    """Test satellite position extraction."""
    signal = Signal(
        id=1,
        psr=20000000.0, psr_rate=0.0,
        x=1000.0, y=2000.0, z=3000.0,
        vx=0.0, vy=0.0, vz=0.0,
        clk=0.0, azimuth=0.0, elevation=0.0, rate_clock=0.0
    )
    
    pos = calculate_satellite_position(signal)
    assert pos[0] == 1000.0
    assert pos[1] == 2000.0
    assert pos[2] == 3000.0


def test_least_squares_positioning():
    """Test least squares positioning algorithm."""
    signals = create_test_signals(n_satellites=6)
    
    position, clock_bias, dop = least_squares_positioning(signals)
    
    # Should converge near origin
    assert abs(position.x) < 1000.0
    assert abs(position.y) < 1000.0
    assert abs(position.z) < 1000.0
    
    # DOP values should be reasonable
    assert dop['GDOP'] < 100.0


def test_calculate_position_from_signals():
    """Test position calculation from signals."""
    signals = create_test_signals(n_satellites=5)
    
    estimate = calculate_position_from_signals(signals, timestamp=1.0)
    
    assert estimate.timestamp == 1.0
    assert estimate.position is not None
    assert estimate.dop is not None


def test_calculate_position_error():
    """Test position error calculation."""
    ref_pos = Coordinate(x=100.0, y=200.0, z=50.0)
    est_pos = Coordinate(x=103.0, y=204.0, z=50.0)
    
    error = calculate_position_error(ref_pos, est_pos, timestamp=1.0)
    
    assert error.timestamp == 1.0
    assert error.error_east == 3.0
    assert error.error_north == 4.0
    assert error.error_up == 0.0
    assert abs(error.error_distance - 5.0) < 0.01  # 3-4-5 triangle


def test_insufficient_satellites():
    """Test handling of insufficient satellites."""
    signals = create_test_signals(n_satellites=2)
    
    # Should handle gracefully with < 4 satellites
    estimate = calculate_position_from_signals(signals, timestamp=1.0)
    assert estimate is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
