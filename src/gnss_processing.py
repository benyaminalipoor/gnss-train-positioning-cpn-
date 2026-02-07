"""
GNSS Data Processing Module
Based on the paper: "Modeling and performance analysis of GNSS-based train 
positioning system with colored petri nets"

This module implements GNSS signal processing, including:
- Signal data structures
- Pseudorange calculations
- Satellite visibility calculations
- Interference modeling (AM, FM, Pulse)
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum


class ScenarioType(Enum):
    """Environment scenarios"""
    OPEN_AREA = "OpenArea"
    MOUNTAIN = "Mountain"
    TUNNEL = "Tunnel"


class InterferenceType(Enum):
    """Signal interference types"""
    NORMAL = "Normal"
    AM = "AM"  # Amplitude Modulation
    FM = "FM"  # Frequency Modulation
    PULSE = "Pulse"


class TunnelState(Enum):
    """Train position relative to tunnel"""
    IN_TUNNEL = "InTunnel"
    JUST_OUT = "JustOut"
    OUT_TUNNEL = "OutTunnel"


@dataclass
class SatelliteSignal:
    """
    Represents GNSS signal from a single satellite
    
    Attributes:
        id: Satellite identifier
        psr: Pseudorange (meters)
        psr_rate: Pseudorange rate (m/s)
        x, y, z: Satellite position in ECEF (meters)
        vx, vy, vz: Satellite velocity (m/s)
        clk: Satellite clock bias (seconds)
        azimuth: Azimuth angle (degrees)
        elevation: Elevation angle (degrees)
        rate_clock: Satellite clock rate (s/s)
    """
    id: int
    psr: float
    psr_rate: float
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float
    clk: float
    azimuth: float
    elevation: float
    rate_clock: float


@dataclass
class GNSSObservation:
    """
    Complete GNSS observation at a specific epoch
    
    Attributes:
        timestamp: Observation time (seconds)
        sequence: Sequence number
        signals: List of satellite signals
    """
    timestamp: int
    sequence: int
    signals: List[SatelliteSignal]


@dataclass
class Position:
    """3D position coordinates"""
    x: float
    y: float
    z: float
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


class InterferenceModel:
    """
    Models GNSS signal interferences
    
    Based on paper specifications:
    - AM: 1 Hz envelope, 1575.42 MHz carrier, modulation depth 0.5
    - FM: 75 kHz Gaussian deviation around 1575.42 MHz
    - Pulse: Periodic bursts with random width and interval
    """
    
    # GNSS L1 carrier frequency (Hz)
    L1_FREQUENCY = 1575.42e6
    
    # AM parameters
    AM_MODULATION_FREQ = 1.0  # Hz
    AM_MODULATION_DEPTH = 0.5
    
    # FM parameters
    FM_DEVIATION_STD = 75e3  # Hz (75 kHz)
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize interference model with optional random seed"""
        if seed is not None:
            np.random.seed(seed)
    
    def apply_am_interference(self, signal: SatelliteSignal, time: float) -> SatelliteSignal:
        """
        Apply Amplitude Modulation interference
        
        Generates amplitude variations with:
        - Low-frequency envelope: 1 Hz
        - Modulation depth: 0.5
        """
        # Calculate amplitude modulation factor
        envelope = 1.0 + self.AM_MODULATION_DEPTH * np.sin(2 * np.pi * self.AM_MODULATION_FREQ * time)
        
        # Apply to pseudorange (main observable affected)
        modified_signal = SatelliteSignal(
            id=signal.id,
            psr=signal.psr * envelope,
            psr_rate=signal.psr_rate,
            x=signal.x, y=signal.y, z=signal.z,
            vx=signal.vx, vy=signal.vy, vz=signal.vz,
            clk=signal.clk,
            azimuth=signal.azimuth,
            elevation=signal.elevation,
            rate_clock=signal.rate_clock
        )
        return modified_signal
    
    def apply_fm_interference(self, signal: SatelliteSignal, time: float) -> SatelliteSignal:
        """
        Apply Frequency Modulation interference
        
        Simulates frequency deviations with Gaussian distribution
        - Standard deviation: 75 kHz
        """
        # Generate frequency deviation
        freq_deviation = np.random.normal(0, self.FM_DEVIATION_STD)
        
        # Convert frequency error to pseudorange error
        # Δρ = (Δf / f) * ρ
        psr_error = (freq_deviation / self.L1_FREQUENCY) * signal.psr
        
        modified_signal = SatelliteSignal(
            id=signal.id,
            psr=signal.psr + psr_error,
            psr_rate=signal.psr_rate,
            x=signal.x, y=signal.y, z=signal.z,
            vx=signal.vx, vy=signal.vy, vz=signal.vz,
            clk=signal.clk,
            azimuth=signal.azimuth,
            elevation=signal.elevation,
            rate_clock=signal.rate_clock
        )
        return modified_signal
    
    def apply_pulse_interference(self, signal: SatelliteSignal, time: float,
                                 pulse_width: float = None, pulse_interval: float = None) -> SatelliteSignal:
        """
        Apply Pulse interference
        
        Generates periodic pulse signals with:
        - Random pulse width Tp
        - Random pulse interval Ti
        - Amplitude between 1 and 5
        """
        # Generate random pulse parameters if not provided
        if pulse_width is None:
            pulse_width = np.random.uniform(0.1, 0.5)  # 0.1-0.5 seconds
        if pulse_interval is None:
            pulse_interval = np.random.uniform(1.0, 3.0)  # 1-3 seconds
        
        pulse_period = pulse_width + pulse_interval
        time_in_period = time % pulse_period
        
        # Check if we're in pulse active period
        if time_in_period < pulse_width:
            # Generate pulse amplitude (1 to 5)
            amplitude = np.random.uniform(1, 5)
            psr_error = amplitude * 10.0  # Scale to meters
        else:
            psr_error = 0.0
        
        modified_signal = SatelliteSignal(
            id=signal.id,
            psr=signal.psr + psr_error,
            psr_rate=signal.psr_rate,
            x=signal.x, y=signal.y, z=signal.z,
            vx=signal.vx, vy=signal.vy, vz=signal.vz,
            clk=signal.clk,
            azimuth=signal.azimuth,
            elevation=signal.elevation,
            rate_clock=signal.rate_clock
        )
        return modified_signal


class EnvironmentModel:
    """
    Models environmental effects on GNSS signals
    
    Includes:
    - Mountain occlusion
    - Tunnel shielding
    """
    
    def __init__(self):
        self.mountain_height = 0.0  # meters
        self.mountain_distance = 0.0  # meters
    
    def set_mountain_parameters(self, height: float, distance: float):
        """Set mountain obstruction parameters"""
        self.mountain_height = height
        self.mountain_distance = distance
    
    def calculate_obstruction_angle(self) -> float:
        """Calculate obstruction angle from mountain geometry"""
        if self.mountain_distance == 0:
            return 0.0
        return np.degrees(np.arctan(self.mountain_height / self.mountain_distance))
    
    def filter_obstructed_satellites(self, signals: List[SatelliteSignal]) -> List[SatelliteSignal]:
        """
        Filter out satellites obstructed by mountains
        
        Satellites with elevation angle below obstruction angle are removed
        """
        obstruction_angle = self.calculate_obstruction_angle()
        visible_signals = [
            signal for signal in signals 
            if signal.elevation > obstruction_angle
        ]
        return visible_signals
    
    def apply_tunnel_effect(self, signals: List[SatelliteSignal], 
                           tunnel_state: TunnelState, 
                           time_since_exit: float = 0.0) -> Tuple[List[SatelliteSignal], bool]:
        """
        Apply tunnel effects to GNSS signals
        
        Returns:
            (modified_signals, has_signals)
        """
        if tunnel_state == TunnelState.IN_TUNNEL:
            # Complete signal blockage inside tunnel
            return [], False
        
        elif tunnel_state == TunnelState.JUST_OUT:
            # High errors immediately after exiting tunnel
            # Error decreases exponentially with time
            decay_factor = np.exp(-time_since_exit / 10.0)  # 10 second time constant
            base_error = 50.0  # meters initial error
            
            modified_signals = []
            for signal in signals:
                error = base_error * decay_factor * np.random.uniform(0.5, 1.5)
                modified_signal = SatelliteSignal(
                    id=signal.id,
                    psr=signal.psr + error,
                    psr_rate=signal.psr_rate,
                    x=signal.x, y=signal.y, z=signal.z,
                    vx=signal.vx, vy=signal.vy, vz=signal.vz,
                    clk=signal.clk,
                    azimuth=signal.azimuth,
                    elevation=signal.elevation,
                    rate_clock=signal.rate_clock
                )
                modified_signals.append(modified_signal)
            return modified_signals, True
        
        else:  # OUT_TUNNEL
            # Normal reception outside tunnel
            return signals, True


def calculate_satellite_geometry(sat_pos: Tuple[float, float, float],
                                receiver_pos: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """
    Calculate satellite geometry (distance, azimuth, elevation)
    
    Args:
        sat_pos: Satellite position (x, y, z) in ECEF
        receiver_pos: Receiver position (x, y, z) in ECEF
    
    Returns:
        (distance, azimuth, elevation) in meters and degrees
    """
    # Calculate vector from receiver to satellite
    dx = sat_pos[0] - receiver_pos[0]
    dy = sat_pos[1] - receiver_pos[1]
    dz = sat_pos[2] - receiver_pos[2]
    
    # Distance
    distance = np.sqrt(dx**2 + dy**2 + dz**2)
    
    # For azimuth and elevation, need local ENU frame
    # Simplified calculation assuming small area
    azimuth = np.degrees(np.arctan2(dy, dx))
    elevation = np.degrees(np.arcsin(dz / distance))
    
    return distance, azimuth, elevation


def generate_synthetic_gnss_data(num_epochs: int = 600,
                                epoch_interval: float = 1.0,
                                num_satellites: int = 8,
                                receiver_pos: Optional[Position] = None) -> List[GNSSObservation]:
    """
    Generate synthetic GNSS observation data for simulation
    
    Args:
        num_epochs: Number of observation epochs (default 600 = 10 minutes)
        epoch_interval: Time between epochs in seconds
        num_satellites: Number of visible satellites
        receiver_pos: Initial receiver position (default near Beijing)
    
    Returns:
        List of GNSS observations
    """
    if receiver_pos is None:
        # Default position near Beijing (approximate ECEF)
        receiver_pos = Position(x=-2148744.0, y=4426641.0, z=4044655.0)
    
    observations = []
    
    for epoch in range(num_epochs):
        timestamp = int(epoch * epoch_interval)
        signals = []
        
        # Generate signals for each satellite
        for sat_id in range(1, num_satellites + 1):
            # Simplified satellite positions (constellation simulation)
            # Real implementation would use ephemeris data
            angle = (2 * np.pi * sat_id / num_satellites) + (epoch * 0.001)
            radius = 26560e3  # GPS satellite radius in meters
            
            sat_x = radius * np.cos(angle)
            sat_y = radius * np.sin(angle)
            sat_z = radius * np.sin(angle / 2) * 0.5
            
            # Calculate geometry
            distance, azimuth, elevation = calculate_satellite_geometry(
                (sat_x, sat_y, sat_z),
                receiver_pos.to_tuple()
            )
            
            # Add small random noise to pseudorange
            psr = distance + np.random.normal(0, 1.0)
            
            signal = SatelliteSignal(
                id=sat_id,
                psr=psr,
                psr_rate=np.random.normal(0, 0.1),
                x=sat_x, y=sat_y, z=sat_z,
                vx=0.0, vy=0.0, vz=0.0,
                clk=np.random.normal(0, 1e-6),
                azimuth=azimuth,
                elevation=elevation,
                rate_clock=0.0
            )
            signals.append(signal)
        
        observation = GNSSObservation(
            timestamp=timestamp,
            sequence=epoch,
            signals=signals
        )
        observations.append(observation)
    
    return observations
