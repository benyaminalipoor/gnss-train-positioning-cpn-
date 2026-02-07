"""
Train Positioning Module using Extended Kalman Filter (EKF)
Based on the paper: "Modeling and performance analysis of GNSS-based train 
positioning system with colored petri nets"

Implements the EKF algorithm for GNSS position solution as described in Algorithm 1
"""

import numpy as np
from typing import List, Tuple, Optional
from gnss_processing import SatelliteSignal, GNSSObservation, Position


class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for GNSS positioning
    
    State vector: [x, y, z, vx, vy, vz, clk_bias, clk_drift]
    - x, y, z: Position in ECEF (meters)
    - vx, vy, vz: Velocity (m/s)
    - clk_bias: Receiver clock bias (meters)
    - clk_drift: Receiver clock drift (m/s)
    """
    
    def __init__(self, initial_position: Optional[Position] = None):
        """
        Initialize EKF with initial state
        
        Args:
            initial_position: Initial receiver position (ECEF)
        """
        # State dimension: 8 (position, velocity, clock)
        self.state_dim = 8
        
        # Initialize state vector
        if initial_position is None:
            # Default near Beijing
            initial_position = Position(x=-2148744.0, y=4426641.0, z=4044655.0)
        
        self.state = np.array([
            initial_position.x, initial_position.y, initial_position.z,  # position
            0.0, 0.0, 0.0,  # velocity
            0.0,  # clock bias
            0.0   # clock drift
        ])
        
        # State covariance matrix
        self.P = np.eye(self.state_dim) * 100.0
        self.P[0:3, 0:3] *= 10.0  # Position uncertainty
        self.P[3:6, 3:6] *= 1.0   # Velocity uncertainty
        self.P[6, 6] = 100.0      # Clock bias uncertainty
        self.P[7, 7] = 10.0       # Clock drift uncertainty
        
        # Process noise covariance
        self.Q = np.eye(self.state_dim)
        self.Q[0:3, 0:3] *= 0.1   # Position process noise
        self.Q[3:6, 3:6] *= 0.01  # Velocity process noise
        self.Q[6, 6] = 1.0        # Clock bias process noise
        self.Q[7, 7] = 0.1        # Clock drift process noise
        
        # Measurement noise (pseudorange)
        self.R_base = 10.0  # Base measurement noise (meters)
        
        # Time step
        self.dt = 1.0  # seconds
    
    def predict(self, dt: Optional[float] = None):
        """
        Prediction step of EKF
        
        State transition: Constant velocity model with clock drift
        """
        if dt is None:
            dt = self.dt
        
        # State transition matrix F
        F = np.eye(self.state_dim)
        # Position updated by velocity
        F[0:3, 3:6] = np.eye(3) * dt
        # Clock bias updated by drift
        F[6, 7] = dt
        
        # Predict state
        self.state = F @ self.state
        
        # Predict covariance
        self.P = F @ self.P @ F.T + self.Q
    
    def update(self, observations: List[SatelliteSignal]):
        """
        Update step of EKF using GNSS pseudorange measurements
        
        Args:
            observations: List of satellite signals with pseudoranges
        """
        if len(observations) < 4:
            # Need at least 4 satellites for 3D positioning
            return
        
        num_obs = len(observations)
        
        # Measurement vector
        z = np.array([obs.psr for obs in observations])
        
        # Predicted measurements and Jacobian
        h_pred = np.zeros(num_obs)
        H = np.zeros((num_obs, self.state_dim))
        
        rx, ry, rz = self.state[0], self.state[1], self.state[2]
        clk_bias = self.state[6]
        
        for i, obs in enumerate(observations):
            sx, sy, sz = obs.x, obs.y, obs.z
            
            # Geometric range
            dx = sx - rx
            dy = sy - ry
            dz = sz - rz
            geometric_range = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # Predicted pseudorange (geometric range + clock bias)
            h_pred[i] = geometric_range + clk_bias
            
            # Jacobian: ∂h/∂state
            # ∂ρ/∂rx = -dx/range
            H[i, 0] = -dx / geometric_range
            H[i, 1] = -dy / geometric_range
            H[i, 2] = -dz / geometric_range
            # ∂ρ/∂clk_bias = 1
            H[i, 6] = 1.0
        
        # Innovation (measurement residual)
        y = z - h_pred
        
        # Measurement noise covariance
        R = np.eye(num_obs) * self.R_base
        
        # Innovation covariance
        S = H @ self.P @ H.T + R
        
        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)
        
        # Update state
        self.state = self.state + K @ y
        
        # Update covariance
        I = np.eye(self.state_dim)
        self.P = (I - K @ H) @ self.P
    
    def get_position(self) -> Position:
        """Get current estimated position"""
        return Position(x=self.state[0], y=self.state[1], z=self.state[2])
    
    def get_velocity(self) -> Tuple[float, float, float]:
        """Get current estimated velocity"""
        return (self.state[3], self.state[4], self.state[5])
    
    def get_clock_bias(self) -> float:
        """Get current estimated clock bias"""
        return self.state[6]


class TrainPositioningSystem:
    """
    Complete GNSS-based train positioning system
    
    Integrates EKF with GNSS observations to provide train position estimates
    """
    
    def __init__(self, initial_position: Optional[Position] = None):
        """Initialize positioning system"""
        self.ekf = ExtendedKalmanFilter(initial_position)
        self.position_history = []
        self.timestamp_history = []
    
    def process_observation(self, observation: GNSSObservation) -> Optional[Position]:
        """
        Process a GNSS observation and return estimated position
        
        Args:
            observation: GNSS observation with satellite signals
        
        Returns:
            Estimated position, or None if insufficient satellites
        """
        if len(observation.signals) < 4:
            return None
        
        # Predict step
        self.ekf.predict()
        
        # Update step with measurements
        self.ekf.update(observation.signals)
        
        # Get estimated position
        position = self.ekf.get_position()
        
        # Store history
        self.position_history.append(position)
        self.timestamp_history.append(observation.timestamp)
        
        return position
    
    def process_observations(self, observations: List[GNSSObservation]) -> List[Position]:
        """
        Process multiple GNSS observations
        
        Args:
            observations: List of GNSS observations
        
        Returns:
            List of estimated positions
        """
        positions = []
        for obs in observations:
            pos = self.process_observation(obs)
            if pos is not None:
                positions.append(pos)
        return positions
    
    def get_position_history(self) -> List[Position]:
        """Get history of estimated positions"""
        return self.position_history
    
    def get_timestamps(self) -> List[int]:
        """Get timestamps of position estimates"""
        return self.timestamp_history
    
    def reset(self, initial_position: Optional[Position] = None):
        """Reset the positioning system"""
        self.ekf = ExtendedKalmanFilter(initial_position)
        self.position_history = []
        self.timestamp_history = []


def calculate_position_error(estimated: Position, reference: Position) -> float:
    """
    Calculate Euclidean distance error between estimated and reference positions
    
    As defined in the paper: d = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)
    
    Args:
        estimated: Estimated position
        reference: Reference (true) position
    
    Returns:
        Error distance in meters
    """
    dx = estimated.x - reference.x
    dy = estimated.y - reference.y
    dz = estimated.z - reference.z
    
    error = np.sqrt(dx**2 + dy**2 + dz**2)
    return error


def calculate_position_statistics(estimated_positions: List[Position],
                                 reference_positions: List[Position]) -> dict:
    """
    Calculate positioning performance statistics
    
    Returns statistics matching the paper's tables:
    - Mean error
    - Standard deviation
    - Directional components
    
    Args:
        estimated_positions: List of estimated positions
        reference_positions: List of reference (true) positions
    
    Returns:
        Dictionary with statistics
    """
    if len(estimated_positions) != len(reference_positions):
        raise ValueError("Position lists must have same length")
    
    errors = []
    for est, ref in zip(estimated_positions, reference_positions):
        error = calculate_position_error(est, ref)
        errors.append(error)
    
    errors = np.array(errors)
    
    stats = {
        'mean_error': np.mean(errors),
        'std_deviation': np.std(errors),
        'min_error': np.min(errors),
        'max_error': np.max(errors),
        'rms_error': np.sqrt(np.mean(errors**2))
    }
    
    return stats
