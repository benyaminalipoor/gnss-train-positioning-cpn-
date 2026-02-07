"""
Color Set (Token Type) Definitions for CPN Model

This module defines all color sets (token types) used in the Colored Petri Net model
for GNSS-based train positioning system, as described in the paper.

Reference: Table 1 in the paper - "Definitions and descriptions of colsets"
"""

from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum


class Scenario(Enum):
    """Different environment scenarios for GNSS reception."""
    OPEN_AREA = "OpenArea"
    MOUNTAIN = "Mountain"
    TUNNEL = "Tunnel"


class StateInterference(Enum):
    """Interference states such as AM, FM, Pulse, and Normal."""
    NORMAL = "Normal"
    AM = "AM"
    FM = "FM"
    PULSE = "Pulse"


@dataclass
class Coordinate:
    """
    A 3D coordinate representation.
    
    Attributes:
        x: X coordinate (Easting in UTM)
        y: Y coordinate (Northing in UTM)
        z: Z coordinate (Height/Elevation)
    """
    x: float
    y: float
    z: float
    
    def __repr__(self):
        return f"Coordinate(x={self.x:.6f}, y={self.y:.6f}, z={self.z:.6f})"


@dataclass
class Signal:
    """
    Represents a signal record containing data from a single satellite.
    
    This includes pseudorange, pseudorange rate, position, velocity, and
    satellite metadata such as clock bias and elevation.
    
    Attributes:
        id: Satellite ID
        psr: Pseudorange (meters)
        psr_rate: Pseudorange rate (meters/second)
        x: Satellite X position (meters)
        y: Satellite Y position (meters)
        z: Satellite Z position (meters)
        vx: Satellite X velocity (m/s)
        vy: Satellite Y velocity (m/s)
        vz: Satellite Z velocity (m/s)
        clk: Clock bias (seconds)
        azimuth: Azimuth angle (degrees)
        elevation: Elevation angle (degrees)
        rate_clock: Clock rate (seconds/second)
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
    
    def __repr__(self):
        return (f"Signal(id={self.id}, psr={self.psr:.2f}, "
                f"elevation={self.elevation:.2f}°)")


# Type aliases for clearer code
SignalList = List[Signal]


@dataclass
class SignalListWithTime:
    """
    Represents a comprehensive dataset for multiple consecutive time points.
    
    This includes all satellite data (SignalList) available to the receiver,
    along with an associated timestamp and sequence number for each epoch.
    
    Attributes:
        timestamp: Time stamp (epoch time in seconds)
        sequence_number: Sequence number for this epoch
        signals: List of Signal records from all visible satellites
    """
    timestamp: int
    sequence_number: int
    signals: SignalList
    
    def __repr__(self):
        return (f"SignalListWithTime(t={self.timestamp}, "
                f"seq={self.sequence_number}, n_signals={len(self.signals)})")


@dataclass
class ObservationData:
    """
    GNSS observation data after signal processing.
    
    Attributes:
        timestamp: Observation time
        signals: Processed signal list
        scenario: Environment scenario
        interference: Interference state
    """
    timestamp: float
    signals: SignalList
    scenario: Scenario
    interference: StateInterference
    
    def __repr__(self):
        return (f"ObservationData(t={self.timestamp:.1f}s, "
                f"n_signals={len(self.signals)}, "
                f"scenario={self.scenario.value}, "
                f"interference={self.interference.value})")


@dataclass
class PositionEstimate:
    """
    Position estimate result from positioning calculation.
    
    Attributes:
        timestamp: Estimation time
        position: Estimated 3D position
        velocity: Estimated 3D velocity (optional)
        clock_bias: Receiver clock bias (optional)
        dop: Dilution of Precision values (optional)
    """
    timestamp: float
    position: Coordinate
    velocity: Coordinate = None
    clock_bias: float = None
    dop: dict = None
    
    def __repr__(self):
        return f"PositionEstimate(t={self.timestamp:.1f}s, pos={self.position})"


@dataclass
class ErrorMetric:
    """
    Positioning error metrics.
    
    Attributes:
        timestamp: Time of measurement
        reference_position: True position
        estimated_position: Estimated position
        error_distance: 3D Euclidean distance error (meters)
        error_east: Error in East direction (meters)
        error_north: Error in North direction (meters)
        error_up: Error in Up direction (meters)
    """
    timestamp: float
    reference_position: Coordinate
    estimated_position: Coordinate
    error_distance: float
    error_east: float = None
    error_north: float = None
    error_up: float = None
    
    def __repr__(self):
        return f"ErrorMetric(t={self.timestamp:.1f}s, error={self.error_distance:.3f}m)"
