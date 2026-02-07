"""
Colored Petri Net (CPN) Model for GNSS Train Positioning System
Based on the paper: "Modeling and performance analysis of GNSS-based train 
positioning system with colored petri nets"

This module implements the CPN model structure including:
- Top-level system model
- GNSS Receiver module with submodules (Open Area, Mountain, Tunnel)
- GNSS Position Solution module
- Evaluation module

Note: Due to Python's capabilities, this is a simulation-based implementation
rather than using formal CPN tools like CPN Tools
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from enum import Enum

from gnss_processing import (
    SatelliteSignal, GNSSObservation, Position,
    ScenarioType, InterferenceType, TunnelState,
    InterferenceModel, EnvironmentModel
)
from train_positioning import TrainPositioningSystem, calculate_position_error


class CPNPlace:
    """Represents a place in the Colored Petri Net"""
    
    def __init__(self, name: str):
        self.name = name
        self.tokens = []
    
    def add_token(self, token):
        """Add a token to the place"""
        self.tokens.append(token)
    
    def remove_token(self, token):
        """Remove a token from the place"""
        if token in self.tokens:
            self.tokens.remove(token)
    
    def get_tokens(self):
        """Get all tokens in the place"""
        return self.tokens.copy()
    
    def has_tokens(self) -> bool:
        """Check if place has tokens"""
        return len(self.tokens) > 0
    
    def clear(self):
        """Remove all tokens"""
        self.tokens = []


class CPNTransition:
    """Represents a transition in the Colored Petri Net"""
    
    def __init__(self, name: str, guard=None, action=None):
        self.name = name
        self.guard = guard  # Function that returns True if transition can fire
        self.action = action  # Function to execute when transition fires
    
    def is_enabled(self, input_places: Dict[str, CPNPlace]) -> bool:
        """Check if transition is enabled (can fire)"""
        # Check if all input places have tokens
        for place in input_places.values():
            if not place.has_tokens():
                return False
        
        # Check guard condition if exists
        if self.guard is not None:
            return self.guard(input_places)
        
        return True
    
    def fire(self, input_places: Dict[str, CPNPlace], output_places: Dict[str, CPNPlace]):
        """Fire the transition"""
        if self.action is not None:
            self.action(input_places, output_places)


class GNSSReceiverModule:
    """
    CPN Module: GNSS Receiver
    
    Simulates complete process of GNSS signal reception and processing
    Includes three submodules: Open Area, Mountain, Tunnel
    """
    
    def __init__(self):
        self.interference_model = InterferenceModel()
        self.environment_model = EnvironmentModel()
        
        # Control flags for interference types
        self.enable_am = False
        self.enable_fm = False
        self.enable_pulse = False
    
    def set_interference_flags(self, am: bool = False, fm: bool = False, pulse: bool = False):
        """Set which interference types are active"""
        self.enable_am = am
        self.enable_fm = fm
        self.enable_pulse = pulse
    
    def process_open_area(self, observation: GNSSObservation, time: float) -> GNSSObservation:
        """
        Submodule: Open Area
        
        Applies signal interferences (AM, FM, Pulse) to GNSS signals
        """
        modified_signals = []
        
        for signal in observation.signals:
            modified_signal = signal
            
            # Apply AM interference if enabled
            if self.enable_am:
                modified_signal = self.interference_model.apply_am_interference(
                    modified_signal, time
                )
            
            # Apply FM interference if enabled
            if self.enable_fm:
                modified_signal = self.interference_model.apply_fm_interference(
                    modified_signal, time
                )
            
            # Apply Pulse interference if enabled
            if self.enable_pulse:
                modified_signal = self.interference_model.apply_pulse_interference(
                    modified_signal, time
                )
            
            modified_signals.append(modified_signal)
        
        return GNSSObservation(
            timestamp=observation.timestamp,
            sequence=observation.sequence,
            signals=modified_signals
        )
    
    def process_mountain(self, observation: GNSSObservation, time: float,
                        mountain_height: float = 100.0,
                        mountain_distance: float = 1000.0) -> GNSSObservation:
        """
        Submodule: Mountain
        
        Filters satellites obstructed by mountain and applies interferences
        """
        # Set mountain parameters
        self.environment_model.set_mountain_parameters(mountain_height, mountain_distance)
        
        # Filter obstructed satellites
        visible_signals = self.environment_model.filter_obstructed_satellites(
            observation.signals
        )
        
        # Apply interferences to remaining satellites
        obs_with_visible = GNSSObservation(
            timestamp=observation.timestamp,
            sequence=observation.sequence,
            signals=visible_signals
        )
        
        return self.process_open_area(obs_with_visible, time)
    
    def process_tunnel(self, observation: GNSSObservation, time: float,
                      tunnel_state: TunnelState,
                      time_since_exit: float = 0.0) -> GNSSObservation:
        """
        Submodule: Tunnel
        
        Simulates three-phase tunnel effects:
        1. Inside tunnel: Complete signal loss
        2. Just out: High errors with gradual recovery
        3. Out of tunnel: Normal with interference
        """
        # Apply tunnel effects
        tunnel_signals, has_signals = self.environment_model.apply_tunnel_effect(
            observation.signals, tunnel_state, time_since_exit
        )
        
        if not has_signals:
            # No signals in tunnel
            return GNSSObservation(
                timestamp=observation.timestamp,
                sequence=observation.sequence,
                signals=[]
            )
        
        # Apply additional interferences if out of tunnel
        obs_with_tunnel = GNSSObservation(
            timestamp=observation.timestamp,
            sequence=observation.sequence,
            signals=tunnel_signals
        )
        
        if tunnel_state == TunnelState.OUT_TUNNEL:
            return self.process_open_area(obs_with_tunnel, time)
        else:
            return obs_with_tunnel
    
    def process_observation(self, observation: GNSSObservation,
                          scenario: ScenarioType,
                          **kwargs) -> GNSSObservation:
        """
        Process GNSS observation based on scenario
        
        Args:
            observation: Input GNSS observation
            scenario: Environment scenario type
            **kwargs: Additional scenario-specific parameters
        
        Returns:
            Processed GNSS observation
        """
        time = float(observation.timestamp)
        
        if scenario == ScenarioType.OPEN_AREA:
            return self.process_open_area(observation, time)
        
        elif scenario == ScenarioType.MOUNTAIN:
            mountain_height = kwargs.get('mountain_height', 100.0)
            mountain_distance = kwargs.get('mountain_distance', 1000.0)
            return self.process_mountain(observation, time, 
                                        mountain_height, mountain_distance)
        
        elif scenario == ScenarioType.TUNNEL:
            tunnel_state = kwargs.get('tunnel_state', TunnelState.OUT_TUNNEL)
            time_since_exit = kwargs.get('time_since_exit', 0.0)
            return self.process_tunnel(observation, time, 
                                      tunnel_state, time_since_exit)
        
        else:
            return observation


class GNSSPositionSolutionModule:
    """
    CPN Module: GNSS Position Solution
    
    Implements EKF-based position solution
    """
    
    def __init__(self, initial_position: Optional[Position] = None):
        self.positioning_system = TrainPositioningSystem(initial_position)
    
    def process_observation(self, observation: GNSSObservation) -> Optional[Position]:
        """
        Process GNSS observation through EKF
        
        Returns estimated position or None if insufficient satellites
        """
        return self.positioning_system.process_observation(observation)
    
    def reset(self, initial_position: Optional[Position] = None):
        """Reset position solution"""
        self.positioning_system.reset(initial_position)


class EvaluationModule:
    """
    CPN Module: Evaluation
    
    Calculates positioning errors by comparing estimated vs reference positions
    """
    
    def __init__(self, reference_trajectory: List[Position]):
        """
        Initialize evaluation module
        
        Args:
            reference_trajectory: List of reference (true) positions
        """
        self.reference_trajectory = reference_trajectory
        self.position_errors = []
        self.timestamps = []
    
    def evaluate_position(self, estimated: Position, timestamp: int) -> float:
        """
        Evaluate positioning error at given timestamp
        
        Returns error distance in meters
        """
        # Find corresponding reference position
        if timestamp >= len(self.reference_trajectory):
            timestamp = len(self.reference_trajectory) - 1
        
        reference = self.reference_trajectory[timestamp]
        error = calculate_position_error(estimated, reference)
        
        self.position_errors.append(error)
        self.timestamps.append(timestamp)
        
        return error
    
    def get_statistics(self) -> dict:
        """Get error statistics"""
        if not self.position_errors:
            return {}
        
        errors = np.array(self.position_errors)
        
        return {
            'mean_error': np.mean(errors),
            'std_deviation': np.std(errors),
            'min_error': np.min(errors),
            'max_error': np.max(errors),
            'rms_error': np.sqrt(np.mean(errors**2))
        }
    
    def reset(self):
        """Reset evaluation data"""
        self.position_errors = []
        self.timestamps = []


class GNSSTrainPositioningCPN:
    """
    Top-level CPN Model for GNSS-based Train Positioning System
    
    Integrates all modules:
    - GNSS Receiver
    - Position Solution
    - Evaluation
    """
    
    def __init__(self, reference_trajectory: List[Position],
                 initial_position: Optional[Position] = None):
        """
        Initialize complete CPN model
        
        Args:
            reference_trajectory: Reference train trajectory
            initial_position: Initial receiver position
        """
        self.receiver_module = GNSSReceiverModule()
        self.solution_module = GNSSPositionSolutionModule(initial_position)
        self.evaluation_module = EvaluationModule(reference_trajectory)
        
        # Current scenario
        self.current_scenario = ScenarioType.OPEN_AREA
        self.scenario_params = {}
        
        # Results storage
        self.observations_processed = []
        self.positions_estimated = []
    
    def set_scenario(self, scenario: ScenarioType, **params):
        """
        Set current environment scenario
        
        Args:
            scenario: Scenario type
            **params: Scenario-specific parameters
        """
        self.current_scenario = scenario
        self.scenario_params = params
    
    def set_interference(self, interference_type: InterferenceType):
        """Set signal interference type"""
        if interference_type == InterferenceType.AM:
            self.receiver_module.set_interference_flags(am=True, fm=False, pulse=False)
        elif interference_type == InterferenceType.FM:
            self.receiver_module.set_interference_flags(am=False, fm=True, pulse=False)
        elif interference_type == InterferenceType.PULSE:
            self.receiver_module.set_interference_flags(am=False, fm=False, pulse=True)
        else:  # NORMAL
            self.receiver_module.set_interference_flags(am=False, fm=False, pulse=False)
    
    def process_epoch(self, observation: GNSSObservation) -> Optional[Tuple[Position, float]]:
        """
        Process one observation epoch through complete system
        
        Returns:
            (estimated_position, error) or None if positioning failed
        """
        # Module 1: GNSS Receiver - process signals through scenario
        processed_obs = self.receiver_module.process_observation(
            observation, self.current_scenario, **self.scenario_params
        )
        
        if len(processed_obs.signals) < 4:
            # Insufficient satellites for positioning
            return None
        
        # Module 2: Position Solution - EKF processing
        estimated_position = self.solution_module.process_observation(processed_obs)
        
        if estimated_position is None:
            return None
        
        # Module 3: Evaluation - calculate error
        error = self.evaluation_module.evaluate_position(
            estimated_position, observation.timestamp
        )
        
        # Store results
        self.observations_processed.append(processed_obs)
        self.positions_estimated.append(estimated_position)
        
        return (estimated_position, error)
    
    def run_simulation(self, observations: List[GNSSObservation]) -> dict:
        """
        Run complete simulation
        
        Args:
            observations: List of GNSS observations
        
        Returns:
            Dictionary with simulation results and statistics
        """
        results = {
            'positions': [],
            'errors': [],
            'timestamps': [],
            'valid_epochs': 0,
            'total_epochs': len(observations)
        }
        
        for obs in observations:
            result = self.process_epoch(obs)
            
            if result is not None:
                position, error = result
                results['positions'].append(position)
                results['errors'].append(error)
                results['timestamps'].append(obs.timestamp)
                results['valid_epochs'] += 1
        
        # Add statistics
        results['statistics'] = self.evaluation_module.get_statistics()
        
        return results
    
    def reset(self):
        """Reset simulation state"""
        self.solution_module.reset()
        self.evaluation_module.reset()
        self.observations_processed = []
        self.positions_estimated = []
