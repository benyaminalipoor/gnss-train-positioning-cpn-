"""
GNSS Positioning Module

This module implements GNSS positioning calculations including
pseudorange-based position estimation.
"""

import numpy as np
from typing import List, Tuple, Optional
from ..cpn.tokens import Signal, SignalList, Coordinate, PositionEstimate


def calculate_satellite_position(signal: Signal) -> np.ndarray:
    """
    Get satellite position from signal data.
    
    Args:
        signal: Signal containing satellite position
        
    Returns:
        3D position array [x, y, z]
    """
    return np.array([signal.x, signal.y, signal.z])


def least_squares_positioning(
    signals: SignalList,
    initial_position: Optional[np.ndarray] = None,
    max_iterations: int = 10,
    convergence_threshold: float = 1e-4
) -> Tuple[Coordinate, float, dict]:
    """
    Calculate receiver position using least squares method.
    
    This implements the standard GNSS positioning algorithm using
    pseudorange observations from multiple satellites.
    
    Args:
        signals: List of satellite signals with pseudorange measurements
        initial_position: Initial guess for receiver position [x, y, z, clock_bias]
        max_iterations: Maximum number of iterations
        convergence_threshold: Convergence threshold for position change
        
    Returns:
        Tuple of (position, clock_bias, dop_values)
    """
    if len(signals) < 4:
        raise ValueError("At least 4 satellites required for 3D positioning")
    
    # Initialize position estimate
    if initial_position is None:
        # Use approximate center of satellite positions
        sat_positions = np.array([
            [s.x, s.y, s.z] for s in signals
        ])
        initial_position = np.mean(sat_positions, axis=0)
        initial_position = np.append(initial_position, 0.0)  # Add clock bias
    
    # Speed of light
    c = 299792458.0  # m/s
    
    # State vector: [x, y, z, clock_bias]
    state = initial_position.copy()
    
    # Iterative least squares
    for iteration in range(max_iterations):
        # Build observation matrix H and residual vector
        n_satellites = len(signals)
        H = np.zeros((n_satellites, 4))
        residuals = np.zeros(n_satellites)
        
        for i, signal in enumerate(signals):
            # Satellite position
            sat_pos = calculate_satellite_position(signal)
            
            # Geometric range
            diff = state[:3] - sat_pos
            geometric_range = np.linalg.norm(diff)
            
            # Unit vector from satellite to receiver
            if geometric_range > 0:
                unit_vector = diff / geometric_range
            else:
                unit_vector = np.array([0, 0, 0])
            
            # Design matrix row: partial derivatives
            H[i, :3] = unit_vector
            H[i, 3] = 1.0  # Partial derivative w.r.t. clock bias
            
            # Residual: observed pseudorange - predicted pseudorange
            predicted_range = geometric_range + state[3]
            residuals[i] = signal.psr - predicted_range
        
        # Solve normal equations: (H^T H) delta_x = H^T residuals
        try:
            HTH = H.T @ H
            HTr = H.T @ residuals
            delta_state = np.linalg.solve(HTH, HTr)
        except np.linalg.LinAlgError:
            # Singular matrix, use pseudoinverse
            delta_state = np.linalg.lstsq(H, residuals, rcond=None)[0]
        
        # Update state
        state += delta_state
        
        # Check convergence
        position_change = np.linalg.norm(delta_state[:3])
        if position_change < convergence_threshold:
            break
    
    # Calculate DOP (Dilution of Precision) values
    try:
        Q = np.linalg.inv(H.T @ H)
        gdop = np.sqrt(np.trace(Q))
        pdop = np.sqrt(np.trace(Q[:3, :3]))
        hdop = np.sqrt(Q[0, 0] + Q[1, 1])
        vdop = np.sqrt(Q[2, 2])
        tdop = np.sqrt(Q[3, 3])
    except:
        gdop = pdop = hdop = vdop = tdop = 999.0
    
    dop_values = {
        'GDOP': gdop,
        'PDOP': pdop,
        'HDOP': hdop,
        'VDOP': vdop,
        'TDOP': tdop
    }
    
    position = Coordinate(x=state[0], y=state[1], z=state[2])
    clock_bias = state[3] / c  # Convert to seconds
    
    return position, clock_bias, dop_values


def calculate_position_from_signals(
    signals: SignalList,
    timestamp: float,
    previous_position: Optional[PositionEstimate] = None
) -> PositionEstimate:
    """
    Calculate position estimate from GNSS signals.
    
    Args:
        signals: List of satellite signals
        timestamp: Current time
        previous_position: Previous position estimate (for initialization)
        
    Returns:
        PositionEstimate object
    """
    if len(signals) < 4:
        # Not enough satellites for positioning
        if previous_position is not None:
            # Return previous position if available
            return PositionEstimate(
                timestamp=timestamp,
                position=previous_position.position,
                clock_bias=previous_position.clock_bias,
                dop={'GDOP': 999.0}
            )
        else:
            # Return zero position
            return PositionEstimate(
                timestamp=timestamp,
                position=Coordinate(0, 0, 0),
                dop={'GDOP': 999.0}
            )
    
    # Use previous position as initial guess if available
    initial_pos = None
    if previous_position is not None:
        initial_pos = np.array([
            previous_position.position.x,
            previous_position.position.y,
            previous_position.position.z,
            previous_position.clock_bias * 299792458.0 if previous_position.clock_bias else 0.0
        ])
    
    # Calculate position
    position, clock_bias, dop_values = least_squares_positioning(
        signals,
        initial_position=initial_pos
    )
    
    return PositionEstimate(
        timestamp=timestamp,
        position=position,
        clock_bias=clock_bias,
        dop=dop_values
    )


def calculate_position_error(
    reference: Coordinate,
    estimated: Coordinate,
    timestamp: float
) -> 'ErrorMetric':
    """
    Calculate positioning error between reference and estimated positions.
    
    Args:
        reference: Reference (true) position
        estimated: Estimated position
        timestamp: Time of measurement
        
    Returns:
        ErrorMetric object with error calculations
    """
    from ..cpn.tokens import ErrorMetric
    
    # Calculate 3D Euclidean distance error
    dx = estimated.x - reference.x
    dy = estimated.y - reference.y
    dz = estimated.z - reference.z
    
    error_distance = np.sqrt(dx**2 + dy**2 + dz**2)
    
    return ErrorMetric(
        timestamp=timestamp,
        reference_position=reference,
        estimated_position=estimated,
        error_distance=error_distance,
        error_east=dx,
        error_north=dy,
        error_up=dz
    )
