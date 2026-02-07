"""
Data Loader Module

This module handles loading and generating data for the simulation,
including GNSS satellite data and reference trajectory data.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple
from pathlib import Path
from ..cpn.tokens import Signal, SignalList, Coordinate, Scenario, StateInterference


def generate_satellite_signals_for_trajectory(
    reference_trajectory: List[Coordinate],
    n_satellites: int = 8,
    noise_std: float = 3.0,
    random_seed: int = None
) -> List[SignalList]:
    """
    Generate satellite signals matched to a reference trajectory.
    
    This generates GNSS signals where pseudoranges are calculated from
    the actual reference positions, enabling realistic error calculation.
    
    Args:
        reference_trajectory: List of reference positions
        n_satellites: Number of visible satellites
        noise_std: Pseudorange noise standard deviation (meters)
        random_seed: Random seed for reproducibility
        
    Returns:
        List of SignalList for each epoch
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    n_epochs = len(reference_trajectory)
    
    # Generate constellation geometry (satellites at fixed positions)
    satellite_positions = []
    for i in range(n_satellites):
        # Distribute satellites evenly in sky
        elevation = 15 + (i % 3) * 25  # 15, 40, 65 degrees
        azimuth = (i * 360.0 / n_satellites) % 360
        
        # Satellite range (~20,200 km)
        sat_range_base = 20200000.0
        
        # Convert spherical to Cartesian (relative to local origin)
        elev_rad = np.radians(elevation)
        azim_rad = np.radians(azimuth)
        
        # Satellite position offset (in ENU frame from origin)
        dx = sat_range_base * np.cos(elev_rad) * np.sin(azim_rad)
        dy = sat_range_base * np.cos(elev_rad) * np.cos(azim_rad)
        dz = sat_range_base * np.sin(elev_rad)
        
        sat_pos = Coordinate(x=dx, y=dy, z=dz)
        
        satellite_positions.append({
            'position': sat_pos,
            'elevation': elevation,
            'azimuth': azimuth
        })
    
    # Generate signals for each epoch based on true receiver position
    signal_data = []
    for epoch in range(n_epochs):
        signals = []
        receiver_pos = reference_trajectory[epoch]
        
        for sat_id, sat_info in enumerate(satellite_positions):
            sat_pos = sat_info['position']
            
            # True geometric range
            true_range = np.sqrt(
                (sat_pos.x - receiver_pos.x)**2 +
                (sat_pos.y - receiver_pos.y)**2 +
                (sat_pos.z - receiver_pos.z)**2
            )
            
            # Add noise to pseudorange
            noise = np.random.normal(0, noise_std)
            pseudorange = true_range + noise
            
            # Pseudorange rate (simplified)
            psr_rate = np.random.normal(0, 0.5)
            
            # Satellite velocity (simplified)
            sat_velocity = np.array([
                np.random.normal(0, 100.0),
                np.random.normal(0, 100.0),
                np.random.normal(0, 100.0)
            ])
            
            signal = Signal(
                id=sat_id + 1,
                psr=pseudorange,
                psr_rate=psr_rate,
                x=sat_pos.x,
                y=sat_pos.y,
                z=sat_pos.z,
                vx=sat_velocity[0],
                vy=sat_velocity[1],
                vz=sat_velocity[2],
                clk=np.random.normal(0, 1e-7),
                azimuth=sat_info['azimuth'],
                elevation=sat_info['elevation'],
                rate_clock=0.0
            )
            signals.append(signal)
        
        signal_data.append(signals)
    
    return signal_data


def generate_satellite_signals(
    n_epochs: int,
    n_satellites: int = 8,
    receiver_position: Coordinate = None,
    noise_std: float = 3.0,
    random_seed: int = None
) -> List[SignalList]:
    """
    Generate synthetic GNSS satellite signals.
    
    This generates realistic satellite signals for simulation purposes.
    Uses a simplified model where satellites are positioned around the receiver.
    
    Args:
        n_epochs: Number of time epochs
        n_satellites: Number of visible satellites
        receiver_position: Approximate receiver position (relative to local origin)
        noise_std: Pseudorange noise standard deviation (meters)
        random_seed: Random seed for reproducibility
        
    Returns:
        List of SignalList for each epoch
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    if receiver_position is None:
        # Default to a local coordinate system origin
        receiver_position = Coordinate(x=0.0, y=0.0, z=0.0)
    
    signal_data = []
    
    # Generate constellation geometry (satellites distributed around receiver)
    satellite_positions = []
    for i in range(n_satellites):
        # Distribute satellites in sky with varying elevations and azimuths
        elevation = np.random.uniform(15, 85)  # degrees
        azimuth = i * 360.0 / n_satellites + np.random.uniform(-15, 15)  # Spread evenly
        
        # Satellite at approximately 20,200 km altitude
        sat_range = 20200000.0 + np.random.uniform(-100000, 100000)
        
        # Convert spherical to Cartesian (satellite position in local ENU frame)
        elev_rad = np.radians(elevation)
        azim_rad = np.radians(azimuth)
        
        # Position offset from receiver (in East-North-Up frame)
        dx = sat_range * np.cos(elev_rad) * np.sin(azim_rad)  # East
        dy = sat_range * np.cos(elev_rad) * np.cos(azim_rad)  # North
        dz = sat_range * np.sin(elev_rad)  # Up
        
        sat_pos = Coordinate(
            x=receiver_position.x + dx,
            y=receiver_position.y + dy,
            z=receiver_position.z + dz
        )
        
        satellite_positions.append({
            'position': sat_pos,
            'elevation': elevation,
            'azimuth': azimuth,
            'range': sat_range
        })
    
    # Generate signals for each epoch
    for epoch in range(n_epochs):
        signals = []
        
        for sat_id, sat_info in enumerate(satellite_positions):
            # True geometric range from receiver to satellite
            sat_pos = sat_info['position']
            true_range = np.sqrt(
                (sat_pos.x - receiver_position.x)**2 +
                (sat_pos.y - receiver_position.y)**2 +
                (sat_pos.z - receiver_position.z)**2
            )
            
            # Add noise to pseudorange
            noise = np.random.normal(0, noise_std)
            pseudorange = true_range + noise
            
            # Pseudorange rate (Doppler-derived) - simplified
            psr_rate = np.random.normal(0, 1.0)  # m/s
            
            # Satellite velocity (simplified circular orbit)
            sat_velocity = np.random.normal(0, 500.0, size=3)  # m/s
    # Generate signals for each epoch
    for epoch in range(n_epochs):
        signals = []
        
        # Update receiver position if moving (for moving trajectory)
        # In a real scenario, this would be the train's current position
        epoch_receiver_pos = receiver_position
        
        for sat_id, sat_info in enumerate(satellite_positions):
            # Satellite position (remains relatively constant over short periods)
            sat_pos = sat_info['position']
            
            # True geometric range from current receiver position to satellite
            true_range = np.sqrt(
                (sat_pos.x - epoch_receiver_pos.x)**2 +
                (sat_pos.y - epoch_receiver_pos.y)**2 +
                (sat_pos.z - epoch_receiver_pos.z)**2
            )
            
            # Add noise to pseudorange
            noise = np.random.normal(0, noise_std)
            pseudorange = true_range + noise
            
            # Pseudorange rate (Doppler-derived) - simplified
            psr_rate = np.random.normal(0, 1.0)  # m/s
            
            # Satellite velocity (simplified circular orbit)
            sat_velocity = np.random.normal(0, 500.0, size=3)  # m/s
            
            # Clock bias (simplified, small random walk)
            clock_bias = np.random.normal(0, 1e-6)  # seconds
            
            signal = Signal(
                id=sat_id + 1,
                psr=pseudorange,
                psr_rate=psr_rate,
                x=sat_pos.x,
                y=sat_pos.y,
                z=sat_pos.z,
                vx=sat_velocity[0],
                vy=sat_velocity[1],
                vz=sat_velocity[2],
                clk=clock_bias,
                azimuth=sat_info['azimuth'],
                elevation=sat_info['elevation'],
                rate_clock=0.0
            )
            signals.append(signal)
        
        signal_data.append(signals)
    
    return signal_data


def generate_reference_trajectory(
    n_epochs: int,
    start_position: Coordinate = None,
    velocity: float = 50.0,
    trajectory_type: str = 'linear'
) -> List[Coordinate]:
    """
    Generate reference trajectory for the train.
    
    Args:
        n_epochs: Number of time points
        start_position: Starting position (in local coordinates)
        velocity: Train velocity (m/s)
        trajectory_type: Type of trajectory ('linear', 'curved', 'complex')
        
    Returns:
        List of reference positions
    """
    if start_position is None:
        # Default starting position at local origin
        start_position = Coordinate(x=0.0, y=0.0, z=0.0)
    
    trajectory = []
    
    if trajectory_type == 'linear':
        # Simple linear trajectory moving in positive x direction
        for i in range(n_epochs):
            distance = velocity * i  # Distance traveled
            position = Coordinate(
                x=start_position.x + distance,  # Moving along track
                y=start_position.y,  # Straight line
                z=start_position.z   # Constant height
            )
            trajectory.append(position)
    
    elif trajectory_type == 'curved':
        # Curved trajectory (circular arc)
        radius = 5000.0  # meters
        angular_velocity = velocity / radius
        
        for i in range(n_epochs):
            angle = angular_velocity * i
            position = Coordinate(
                x=start_position.x + radius * np.sin(angle),
                y=start_position.y + radius * (1 - np.cos(angle)),
                z=start_position.z
            )
            trajectory.append(position)
    
    else:  # 'complex'
        # Complex trajectory with acceleration/deceleration
        x, y, z = start_position.x, start_position.y, start_position.z
        v = velocity
        
        for i in range(n_epochs):
            # Vary velocity
            if i < n_epochs // 3:
                v += 0.1  # Accelerate
            elif i > 2 * n_epochs // 3:
                v -= 0.1  # Decelerate
            
            v = max(10.0, min(v, 100.0))  # Clamp velocity
            
            # Move with slight curve
            angle = i * 0.001
            x += v * np.cos(angle)
            y += v * np.sin(angle)
            
            position = Coordinate(x=x, y=y, z=z)
            trajectory.append(position)
    
    return trajectory


def generate_scenario_sequence(
    n_epochs: int,
    scenario_type: str = 'mixed'
) -> Tuple[List[Scenario], List[StateInterference]]:
    """
    Generate sequence of scenarios and interferences.
    
    Args:
        n_epochs: Number of time epochs
        scenario_type: Type of scenario sequence
            - 'open': All open area
            - 'mountain': All mountain
            - 'tunnel': All tunnel  
            - 'mixed': Mix of all scenarios
            
    Returns:
        Tuple of (scenario_list, interference_list)
    """
    scenarios = []
    interferences = []
    
    if scenario_type == 'open':
        scenarios = [Scenario.OPEN_AREA] * n_epochs
    elif scenario_type == 'mountain':
        scenarios = [Scenario.MOUNTAIN] * n_epochs
    elif scenario_type == 'tunnel':
        scenarios = [Scenario.TUNNEL] * n_epochs
    else:  # 'mixed'
        # Divide into segments
        third = n_epochs // 3
        scenarios = (
            [Scenario.OPEN_AREA] * third +
            [Scenario.MOUNTAIN] * third +
            [Scenario.TUNNEL] * (n_epochs - 2 * third)
        )
    
    # Generate interference sequence
    # Cycle through different interference types
    interference_types = [
        StateInterference.NORMAL,
        StateInterference.AM,
        StateInterference.FM,
        StateInterference.PULSE
    ]
    
    for i in range(n_epochs):
        # Use different interference for different parts
        interference_idx = (i // (n_epochs // 4)) % len(interference_types)
        interferences.append(interference_types[interference_idx])
    
    return scenarios, interferences


def load_data_from_file(file_path: str) -> dict:
    """
    Load simulation data from file.
    
    Args:
        file_path: Path to data file (CSV, JSON, etc.)
        
    Returns:
        Dictionary with loaded data
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Load based on file extension
    if file_path.suffix == '.csv':
        df = pd.read_csv(file_path)
        # Process DataFrame to extract signals and positions
        # (Implementation depends on data format)
        return {'dataframe': df}
    
    elif file_path.suffix == '.json':
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def save_results_to_csv(results: dict, output_file: str):
    """
    Save simulation results to CSV file.
    
    Args:
        results: Results dictionary from simulation
        output_file: Output CSV file path
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert results to DataFrame
    data = {
        'timestamp': results['timestamps'],
        'scenario': [s.value for s in results['scenarios']],
        'interference': [i.value for i in results['interferences']],
        'error_distance': [e.error_distance for e in results['errors']],
    }
    
    # Add position data if available
    if len(results['filtered_positions']) > 0:
        data['pos_x'] = [p.position.x for p in results['filtered_positions']]
        data['pos_y'] = [p.position.y for p in results['filtered_positions']]
        data['pos_z'] = [p.position.z for p in results['filtered_positions']]
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
