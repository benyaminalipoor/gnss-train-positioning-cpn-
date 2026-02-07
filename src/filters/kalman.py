"""
Extended Kalman Filter Module

This module implements the Extended Kalman Filter (EKF) for
GNSS-based train positioning as described in the paper.

The EKF is used to fuse GNSS observations and improve positioning accuracy.
"""

import numpy as np
from typing import Optional, Tuple
from ..cpn.tokens import Coordinate, PositionEstimate, SignalList


class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for GNSS train positioning.
    
    State vector: [x, y, z, vx, vy, vz, clock_bias, clock_drift]
    - x, y, z: 3D position (meters)
    - vx, vy, vz: 3D velocity (m/s)
    - clock_bias: Receiver clock bias (meters)
    - clock_drift: Receiver clock drift (m/s)
    """
    
    def __init__(
        self,
        initial_state: Optional[np.ndarray] = None,
        initial_covariance: Optional[np.ndarray] = None,
        process_noise_std: dict = None,
        measurement_noise_std: dict = None
    ):
        """
        Initialize the EKF.
        
        Args:
            initial_state: Initial state vector [x, y, z, vx, vy, vz, cb, cd]
            initial_covariance: Initial state covariance matrix (8x8)
            process_noise_std: Process noise standard deviations
            measurement_noise_std: Measurement noise standard deviations
        """
        # Initialize state (8-dimensional)
        if initial_state is None:
            self.state = np.zeros(8)
        else:
            self.state = initial_state.copy()
        
        # Initialize covariance matrix
        if initial_covariance is None:
            # Default initial covariance (large uncertainty)
            self.P = np.diag([100.0, 100.0, 100.0,  # position uncertainty (m^2)
                             10.0, 10.0, 10.0,      # velocity uncertainty (m^2/s^2)
                             1000.0, 10.0])         # clock bias/drift uncertainty
        else:
            self.P = initial_covariance.copy()
        
        # Process noise parameters
        if process_noise_std is None:
            process_noise_std = {
                'position': 0.5,      # m
                'velocity': 0.1,      # m/s
                'clock_bias': 1.0,    # m
                'clock_drift': 0.1    # m/s
            }
        self.process_noise_std = process_noise_std
        
        # Measurement noise parameters
        if measurement_noise_std is None:
            measurement_noise_std = {
                'pseudorange': 3.0,   # m
                'position': 5.0       # m
            }
        self.measurement_noise_std = measurement_noise_std
        
        # Speed of light
        self.c = 299792458.0  # m/s
        
        self.last_time = 0.0
    
    def predict(self, dt: float):
        """
        Prediction step of EKF.
        
        Args:
            dt: Time step (seconds)
        """
        if dt <= 0:
            return
        
        # State transition matrix F (constant velocity model)
        F = np.eye(8)
        F[0, 3] = dt  # x = x + vx*dt
        F[1, 4] = dt  # y = y + vy*dt
        F[2, 5] = dt  # z = z + vz*dt
        F[6, 7] = dt  # clock_bias = clock_bias + clock_drift*dt
        
        # Predict state
        self.state = F @ self.state
        
        # Process noise covariance Q
        Q = np.diag([
            self.process_noise_std['position']**2 * dt**2,
            self.process_noise_std['position']**2 * dt**2,
            self.process_noise_std['position']**2 * dt**2,
            self.process_noise_std['velocity']**2 * dt,
            self.process_noise_std['velocity']**2 * dt,
            self.process_noise_std['velocity']**2 * dt,
            self.process_noise_std['clock_bias']**2 * dt,
            self.process_noise_std['clock_drift']**2 * dt
        ])
        
        # Predict covariance
        self.P = F @ self.P @ F.T + Q
    
    def update_with_position(self, measured_position: Coordinate, timestamp: float):
        """
        Update step with position measurement.
        
        Args:
            measured_position: Measured position
            timestamp: Measurement time
        """
        # Time since last update
        if self.last_time > 0:
            dt = timestamp - self.last_time
            if dt > 0:
                self.predict(dt)
        
        self.last_time = timestamp
        
        # Measurement vector (position only)
        z = np.array([measured_position.x, measured_position.y, measured_position.z])
        
        # Measurement matrix H (observe position only)
        H = np.zeros((3, 8))
        H[0, 0] = 1.0  # observe x
        H[1, 1] = 1.0  # observe y
        H[2, 2] = 1.0  # observe z
        
        # Measurement noise covariance R
        R = np.eye(3) * self.measurement_noise_std['position']**2
        
        # Innovation (measurement residual)
        y = z - H @ self.state
        
        # Innovation covariance
        S = H @ self.P @ H.T + R
        
        # Kalman gain
        try:
            K = self.P @ H.T @ np.linalg.inv(S)
        except np.linalg.LinAlgError:
            # Singular matrix, skip update
            return
        
        # Update state
        self.state = self.state + K @ y
        
        # Update covariance
        I_KH = np.eye(8) - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ R @ K.T
    
    def update_with_pseudoranges(
        self,
        signals: SignalList,
        timestamp: float
    ):
        """
        Update step with pseudorange measurements.
        
        Args:
            signals: List of satellite signals with pseudoranges
            timestamp: Measurement time
        """
        if len(signals) < 4:
            return  # Not enough measurements
        
        # Time since last update
        if self.last_time > 0:
            dt = timestamp - self.last_time
            if dt > 0:
                self.predict(dt)
        
        self.last_time = timestamp
        
        n_sats = len(signals)
        
        # Build measurement vector and Jacobian
        z = np.zeros(n_sats)  # Measured pseudoranges
        H = np.zeros((n_sats, 8))  # Measurement Jacobian
        
        for i, signal in enumerate(signals):
            # Satellite position
            sat_pos = np.array([signal.x, signal.y, signal.z])
            
            # Predicted receiver position
            recv_pos = self.state[:3]
            
            # Geometric range
            diff = recv_pos - sat_pos
            geometric_range = np.linalg.norm(diff)
            
            # Predicted pseudorange
            predicted_psr = geometric_range + self.state[6]
            
            # Measured pseudorange
            z[i] = signal.psr
            
            # Jacobian (partial derivatives)
            if geometric_range > 0:
                unit_vector = diff / geometric_range
                H[i, :3] = unit_vector  # d_psr/d_position
                H[i, 6] = 1.0          # d_psr/d_clock_bias
        
        # Measurement noise covariance R
        R = np.eye(n_sats) * self.measurement_noise_std['pseudorange']**2
        
        # Innovation (measurement residual)
        predicted_measurements = np.zeros(n_sats)
        for i, signal in enumerate(signals):
            sat_pos = np.array([signal.x, signal.y, signal.z])
            recv_pos = self.state[:3]
            geometric_range = np.linalg.norm(recv_pos - sat_pos)
            predicted_measurements[i] = geometric_range + self.state[6]
        
        y = z - predicted_measurements
        
        # Innovation covariance
        S = H @ self.P @ H.T + R
        
        # Kalman gain
        try:
            K = self.P @ H.T @ np.linalg.inv(S)
        except np.linalg.LinAlgError:
            # Singular matrix, skip update
            return
        
        # Update state
        self.state = self.state + K @ y
        
        # Update covariance
        I_KH = np.eye(8) - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ R @ K.T
    
    def get_position_estimate(self, timestamp: float) -> PositionEstimate:
        """
        Get current position estimate.
        
        Args:
            timestamp: Current time
            
        Returns:
            PositionEstimate object
        """
        position = Coordinate(
            x=self.state[0],
            y=self.state[1],
            z=self.state[2]
        )
        
        velocity = Coordinate(
            x=self.state[3],
            y=self.state[4],
            z=self.state[5]
        )
        
        clock_bias = self.state[6] / self.c  # Convert to seconds
        
        # Calculate position uncertainty (standard deviations)
        pos_std = np.sqrt(np.diag(self.P[:3, :3]))
        
        return PositionEstimate(
            timestamp=timestamp,
            position=position,
            velocity=velocity,
            clock_bias=clock_bias,
            dop={'position_std': pos_std}
        )
