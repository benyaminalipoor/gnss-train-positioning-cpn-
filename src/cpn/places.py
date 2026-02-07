"""
CPN Places Module

This module defines all places (states) in the Colored Petri Net model
for GNSS-based train positioning system.

Places store tokens and represent states in the system.
"""

from typing import List, Any
from .tokens import *


class Place:
    """
    Base class for a CPN Place.
    
    A place can hold tokens of a specific color set (type).
    """
    
    def __init__(self, name: str, color_set: type, initial_marking: List[Any] = None):
        """
        Initialize a place.
        
        Args:
            name: Name of the place
            color_set: Type of tokens this place can hold
            initial_marking: Initial tokens in this place
        """
        self.name = name
        self.color_set = color_set
        self.tokens = initial_marking if initial_marking is not None else []
        
    def add_token(self, token: Any):
        """Add a token to this place."""
        if not isinstance(token, self.color_set) and self.color_set != Any:
            raise TypeError(f"Token type {type(token)} does not match place color set {self.color_set}")
        self.tokens.append(token)
    
    def remove_token(self, token: Any):
        """Remove a token from this place."""
        if token in self.tokens:
            self.tokens.remove(token)
        else:
            raise ValueError(f"Token {token} not found in place {self.name}")
    
    def has_tokens(self) -> bool:
        """Check if place has any tokens."""
        return len(self.tokens) > 0
    
    def get_tokens(self) -> List[Any]:
        """Get all tokens in this place."""
        return self.tokens.copy()
    
    def clear(self):
        """Remove all tokens from this place."""
        self.tokens.clear()
    
    def __repr__(self):
        return f"Place({self.name}, tokens={len(self.tokens)})"


# Define all places used in the CPN model according to the paper

# Module: GNSS Signal Generator
SATELLITE_DATA = Place("SatelliteData", SignalListWithTime)
GNSS_SIGNAL = Place("GNSSSignal", SignalList)

# Module: GNSS Receiver
SCENARIO = Place("Scenario", Scenario)
INTERFERENCE_STATE = Place("InterferenceState", StateInterference)
GNSS_OBSERVATION = Place("GNSSObservation", ObservationData)

# Submodule: Open Area (Interference handling)
AM_ENABLED = Place("AMEnabled", bool)
FM_ENABLED = Place("FMEnabled", bool)
PULSE_ENABLED = Place("PulseEnabled", bool)
INTERFERENCE_SIGNAL = Place("InterferenceSignal", SignalList)

# Submodule: Mountain
MOUNTAIN_HEIGHT = Place("MountainHeight", float)
MOUNTAIN_DISTANCE = Place("MountainDistance", float)
DATA_WITH_MOUNTAIN_ERROR = Place("DataWithMountainError", SignalList)

# Submodule: Tunnel
IN_TUNNEL = Place("InTunnel", bool)
JUST_OUT = Place("JustOut", bool)
OUT_TUNNEL = Place("OutTunnel", bool)
TUNNEL_POSITION = Place("TunnelPosition", Coordinate)

# Module: EKF Filter
PREDICTED_STATE = Place("PredictedState", PositionEstimate)
FILTERED_POSITION = Place("FilteredPosition", PositionEstimate)

# Module: Positioning
RAW_POSITION = Place("RawPosition", PositionEstimate)
POSITION = Place("Position", PositionEstimate)

# Module: Evaluation
REFERENCE_POSITION = Place("ReferencePosition", Coordinate)
DELTA_POSITION = Place("DeltaPosition", ErrorMetric)
ENVIRONMENT_SCENARIO = Place("EnvironmentScenario", Scenario)

# Additional places for system control
SIMULATION_TIME = Place("SimulationTime", float)
EPOCH_COUNTER = Place("EpochCounter", int)


class PlaceRegistry:
    """
    Registry to manage all places in the CPN model.
    """
    
    def __init__(self):
        self.places = {}
        
    def register(self, place: Place):
        """Register a place."""
        self.places[place.name] = place
        
    def get(self, name: str) -> Place:
        """Get a place by name."""
        return self.places.get(name)
    
    def get_all(self) -> dict:
        """Get all registered places."""
        return self.places.copy()
    
    def reset_all(self):
        """Clear all tokens from all places."""
        for place in self.places.values():
            place.clear()


# Create a global registry
place_registry = PlaceRegistry()

# Register all places
for place_obj in [
    SATELLITE_DATA, GNSS_SIGNAL, SCENARIO, INTERFERENCE_STATE,
    GNSS_OBSERVATION, AM_ENABLED, FM_ENABLED, PULSE_ENABLED,
    INTERFERENCE_SIGNAL, MOUNTAIN_HEIGHT, MOUNTAIN_DISTANCE,
    DATA_WITH_MOUNTAIN_ERROR, IN_TUNNEL, JUST_OUT, OUT_TUNNEL,
    TUNNEL_POSITION, PREDICTED_STATE, FILTERED_POSITION,
    RAW_POSITION, POSITION, REFERENCE_POSITION, DELTA_POSITION,
    ENVIRONMENT_SCENARIO, SIMULATION_TIME, EPOCH_COUNTER
]:
    place_registry.register(place_obj)
