"""
CPN Transitions Module

This module defines all transitions in the Colored Petri Net model
for GNSS-based train positioning system.

Transitions represent actions or events that move tokens between places.
"""

from typing import Callable, List, Dict, Any
import numpy as np
from .tokens import *
from .places import Place


class Transition:
    """
    Base class for a CPN Transition.
    
    A transition fires when its guard condition is satisfied,
    consuming tokens from input places and producing tokens in output places.
    """
    
    def __init__(
        self,
        name: str,
        input_places: Dict[str, Place],
        output_places: Dict[str, Place],
        guard: Callable = None,
        action: Callable = None
    ):
        """
        Initialize a transition.
        
        Args:
            name: Name of the transition
            input_places: Dictionary of input places {label: place}
            output_places: Dictionary of output places {label: place}
            guard: Guard condition function (returns bool)
            action: Action function that transforms input tokens to output tokens
        """
        self.name = name
        self.input_places = input_places
        self.output_places = output_places
        self.guard = guard if guard is not None else lambda *args: True
        self.action = action
        self.enabled = False
        
    def is_enabled(self) -> bool:
        """Check if transition is enabled (can fire)."""
        # Check if all input places have tokens
        for place in self.input_places.values():
            if not place.has_tokens():
                return False
        
        # Check guard condition
        input_tokens = {label: place.tokens[0] for label, place in self.input_places.items()}
        return self.guard(**input_tokens)
    
    def fire(self):
        """Fire the transition, consuming input tokens and producing output tokens."""
        if not self.is_enabled():
            raise RuntimeError(f"Transition {self.name} is not enabled")
        
        # Consume input tokens
        input_tokens = {}
        for label, place in self.input_places.items():
            token = place.tokens[0]
            place.remove_token(token)
            input_tokens[label] = token
        
        # Execute action to produce output tokens
        if self.action is not None:
            output_tokens = self.action(**input_tokens)
            
            # Add output tokens to output places
            if output_tokens is not None:
                for label, token in output_tokens.items():
                    if label in self.output_places:
                        self.output_places[label].add_token(token)
    
    def __repr__(self):
        return f"Transition({self.name}, enabled={self.is_enabled()})"


# Signal interference functions (used by transitions)

def apply_am_interference(signals: SignalList, amplitude: float = 5.0, freq: float = 1.0) -> SignalList:
    """
    Apply Amplitude Modulation interference to GNSS signals.
    
    AM interference causes signal power variations which affect pseudorange accuracy.
    Based on paper results showing ~5m mean error increase.
    
    Args:
        signals: List of GNSS signals
        amplitude: Error amplitude in meters (default 5.0m)
        freq: Modulation frequency in Hz
        
    Returns:
        Modified signal list with AM interference
    """
    modified_signals = []
    for i, signal in enumerate(signals):
        # AM interference adds varying error to pseudorange
        # Sinusoidal pattern with amplitude modulation
        am_error = amplitude * np.sin(2 * np.pi * freq * i / len(signals))
        
        # Add random component for realism
        am_error += np.random.normal(0, amplitude * 0.5)
        
        new_signal = Signal(
            id=signal.id,
            psr=signal.psr + am_error,  # Add error to pseudorange
            psr_rate=signal.psr_rate,
            x=signal.x, y=signal.y, z=signal.z,
            vx=signal.vx, vy=signal.vy, vz=signal.vz,
            clk=signal.clk,
            azimuth=signal.azimuth,
            elevation=signal.elevation,
            rate_clock=signal.rate_clock
        )
        modified_signals.append(new_signal)
    
    return modified_signals


def apply_fm_interference(signals: SignalList, error_std: float = 6.0) -> SignalList:
    """
    Apply Frequency Modulation interference to GNSS signals.
    
    FM interference causes frequency deviations affecting pseudorange measurements.
    Based on paper results showing ~6m mean error, highest impact.
    
    Args:
        signals: List of GNSS signals
        error_std: Standard deviation of error in meters (default 6.0m)
        
    Returns:
        Modified signal list with FM interference
    """
    modified_signals = []
    for signal in signals:
        # FM interference causes larger random errors
        # More severe impact than AM (as per paper)
        fm_error = np.random.normal(0, error_std)
        
        # Additional systematic bias
        fm_error += np.random.uniform(-3.0, 3.0)
        
        new_signal = Signal(
            id=signal.id,
            psr=signal.psr + fm_error,
            psr_rate=signal.psr_rate + np.random.normal(0, 0.5),  # Also affect rate
            x=signal.x, y=signal.y, z=signal.z,
            vx=signal.vx, vy=signal.vy, vz=signal.vz,
            clk=signal.clk,
            azimuth=signal.azimuth,
            elevation=signal.elevation,
            rate_clock=signal.rate_clock
        )
        modified_signals.append(new_signal)
    
    return modified_signals


def apply_pulse_interference(signals: SignalList, error_std: float = 5.0, pulse_probability: float = 0.3) -> SignalList:
    """
    Apply Pulse interference to GNSS signals.
    
    Pulse interference causes transient high-intensity disruptions.
    Based on paper results showing ~5m mean error.
    
    Args:
        signals: List of GNSS signals
        error_std: Standard deviation of pulse error in meters
        pulse_probability: Probability of pulse affecting each satellite
        
    Returns:
        Modified signal list with pulse interference
    """
    modified_signals = []
    for signal in signals:
        # Pulse interference causes sporadic large errors
        if np.random.random() < pulse_probability:
            # Strong pulse causes significant error
            pulse_error = np.random.normal(0, error_std)
            
            new_signal = Signal(
                id=signal.id,
                psr=signal.psr + pulse_error,
                psr_rate=signal.psr_rate,
                x=signal.x, y=signal.y, z=signal.z,
                vx=signal.vx, vy=signal.vy, vz=signal.vz,
                clk=signal.clk,
                azimuth=signal.azimuth,
                elevation=signal.elevation,
                rate_clock=signal.rate_clock
            )
            modified_signals.append(new_signal)
        else:
            modified_signals.append(signal)
    
    return modified_signals


def filter_mountain_obstruction(
    signals: SignalList,
    mountain_height: float,
    mountain_distance: float,
    receiver_height: float = 0.0
) -> SignalList:
    """
    Filter out satellites obstructed by mountains.
    
    Args:
        signals: List of GNSS signals
        mountain_height: Height of mountain obstruction (meters)
        mountain_distance: Distance from receiver to mountain (meters)
        receiver_height: Height of receiver (meters)
        
    Returns:
        Filtered signal list with obstructed satellites removed
    """
    # Calculate obstruction angle
    relative_height = mountain_height - receiver_height
    if mountain_distance > 0:
        obstruction_angle = np.degrees(np.arctan(relative_height / mountain_distance))
    else:
        obstruction_angle = 90.0
    
    # Filter signals: keep only those with elevation above obstruction angle
    visible_signals = [
        signal for signal in signals
        if signal.elevation > obstruction_angle
    ]
    
    return visible_signals


def simulate_tunnel_effect(
    signals: SignalList,
    in_tunnel: bool,
    just_out: bool
) -> SignalList:
    """
    Simulate effect of tunnel on GNSS signal reception.
    
    Args:
        signals: List of GNSS signals
        in_tunnel: Whether train is inside tunnel
        just_out: Whether train just exited tunnel
        
    Returns:
        Modified signal list based on tunnel state
    """
    if in_tunnel:
        # Inside tunnel: no GNSS signals received
        return []
    elif just_out:
        # Just exited: reduced number of satellites and increased error
        n_visible = max(4, len(signals) // 2)  # At least 4 satellites
        reduced_signals = signals[:n_visible]
        
        # Add extra error to signals
        modified_signals = []
        for signal in reduced_signals:
            error = np.random.normal(0, 3.0)  # 3m standard deviation
            new_signal = Signal(
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
            modified_signals.append(new_signal)
        return modified_signals
    else:
        # Out of tunnel: normal operation
        return signals
