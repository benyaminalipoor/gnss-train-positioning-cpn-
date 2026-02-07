"""
CPN Model Module

This module defines the complete Colored Petri Net model for
GNSS-based train positioning system.

It implements the hierarchical CPN structure described in the paper.
"""

import numpy as np
from typing import List, Dict, Optional
from .tokens import *
from .places import *
from .transitions import *
from ..gnss.positioning import calculate_position_from_signals, calculate_position_error
from ..filters.kalman import ExtendedKalmanFilter


class CPNModel:
    """
    Complete CPN model for GNSS-based train positioning system.
    
    This implements the hierarchical structure with modules:
    - GNSS Signal Generator
    - GNSS Receiver (with Open Area, Mountain, Tunnel submodules)
    - EKF Filter
    - Positioning
    - Evaluation
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize the CPN model.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config if config is not None else {}
        
        # Initialize places (using global place registry)
        self.places = place_registry
        
        # Initialize EKF
        self.ekf = ExtendedKalmanFilter()
        
        # Simulation state
        self.current_time = 0.0
        self.current_epoch = 0
        
        # Results storage
        self.results = {
            'timestamps': [],
            'positions': [],
            'filtered_positions': [],
            'errors': [],
            'scenarios': [],
            'interferences': []
        }
    
    def initialize(
        self,
        initial_scenario: Scenario = Scenario.OPEN_AREA,
        initial_interference: StateInterference = StateInterference.NORMAL
    ):
        """
        Initialize the model with starting conditions.
        
        Args:
            initial_scenario: Starting environment scenario
            initial_interference: Starting interference state
        """
        # Reset all places
        self.places.reset_all()
        
        # Set initial scenario and interference
        SCENARIO.add_token(initial_scenario)
        INTERFERENCE_STATE.add_token(initial_interference)
        
        # Initialize simulation time
        SIMULATION_TIME.add_token(0.0)
        EPOCH_COUNTER.add_token(0)
        
        # Initialize EKF
        self.ekf = ExtendedKalmanFilter()
        self.current_time = 0.0
        self.current_epoch = 0
    
    def process_gnss_signals(
        self,
        signals: SignalList,
        scenario: Scenario,
        interference: StateInterference,
        mountain_height: float = 0.0,
        mountain_distance: float = 1000.0,
        in_tunnel: bool = False,
        just_out: bool = False
    ) -> SignalList:
        """
        Process GNSS signals through the receiver model.
        
        This implements the GNSS Receiver module with submodules for
        different scenarios and interferences.
        
        Args:
            signals: Input GNSS signals
            scenario: Environment scenario
            interference: Interference state
            mountain_height: Mountain height for obstruction (meters)
            mountain_distance: Distance to mountain (meters)
            in_tunnel: Whether train is in tunnel
            just_out: Whether train just exited tunnel
            
        Returns:
            Processed signal list
        """
        processed_signals = signals.copy()
        
        # Apply scenario-specific processing
        if scenario == Scenario.OPEN_AREA:
            # Apply interference in open area
            if interference == StateInterference.AM:
                processed_signals = apply_am_interference(processed_signals)
            elif interference == StateInterference.FM:
                processed_signals = apply_fm_interference(processed_signals)
            elif interference == StateInterference.PULSE:
                processed_signals = apply_pulse_interference(processed_signals)
            # NORMAL: no interference applied
        
        elif scenario == Scenario.MOUNTAIN:
            # Filter signals based on mountain obstruction
            processed_signals = filter_mountain_obstruction(
                processed_signals,
                mountain_height,
                mountain_distance
            )
            # Also apply interference if present
            if interference == StateInterference.AM:
                processed_signals = apply_am_interference(processed_signals)
            elif interference == StateInterference.FM:
                processed_signals = apply_fm_interference(processed_signals)
            elif interference == StateInterference.PULSE:
                processed_signals = apply_pulse_interference(processed_signals)
        
        elif scenario == Scenario.TUNNEL:
            # Apply tunnel effect
            processed_signals = simulate_tunnel_effect(
                processed_signals,
                in_tunnel,
                just_out
            )
        
        return processed_signals
    
    def step(
        self,
        input_signals: SignalList,
        reference_position: Coordinate,
        scenario: Scenario,
        interference: StateInterference,
        **kwargs
    ) -> Dict:
        """
        Execute one simulation step.
        
        Args:
            input_signals: GNSS signals for this epoch
            reference_position: True position for error calculation
            scenario: Environment scenario
            interference: Interference state
            **kwargs: Additional parameters (mountain_height, in_tunnel, etc.)
            
        Returns:
            Dictionary with step results
        """
        self.current_time += 1.0  # 1 second per step
        self.current_epoch += 1
        
        # 1. Process GNSS signals through receiver model
        processed_signals = self.process_gnss_signals(
            input_signals,
            scenario,
            interference,
            mountain_height=kwargs.get('mountain_height', 0.0),
            mountain_distance=kwargs.get('mountain_distance', 1000.0),
            in_tunnel=kwargs.get('in_tunnel', False),
            just_out=kwargs.get('just_out', False)
        )
        
        # 2. Calculate raw position from processed signals
        if len(processed_signals) >= 4:
            raw_position = calculate_position_from_signals(
                processed_signals,
                self.current_time
            )
            
            # 3. Apply EKF filtering
            self.ekf.update_with_position(
                raw_position.position,
                self.current_time
            )
            filtered_position = self.ekf.get_position_estimate(self.current_time)
        else:
            # Not enough signals for positioning
            raw_position = PositionEstimate(
                timestamp=self.current_time,
                position=Coordinate(0, 0, 0)
            )
            filtered_position = raw_position
        
        # 4. Calculate positioning errors
        raw_error = calculate_position_error(
            reference_position,
            raw_position.position,
            self.current_time
        )
        
        filtered_error = calculate_position_error(
            reference_position,
            filtered_position.position,
            self.current_time
        )
        
        # 5. Store results
        step_result = {
            'timestamp': self.current_time,
            'epoch': self.current_epoch,
            'n_satellites': len(processed_signals),
            'scenario': scenario,
            'interference': interference,
            'raw_position': raw_position,
            'filtered_position': filtered_position,
            'raw_error': raw_error,
            'filtered_error': filtered_error
        }
        
        self.results['timestamps'].append(self.current_time)
        self.results['positions'].append(raw_position)
        self.results['filtered_positions'].append(filtered_position)
        self.results['errors'].append(filtered_error)
        self.results['scenarios'].append(scenario)
        self.results['interferences'].append(interference)
        
        return step_result
    
    def run_simulation(
        self,
        signal_data: List[SignalList],
        reference_trajectory: List[Coordinate],
        scenarios: List[Scenario],
        interferences: List[StateInterference],
        **kwargs
    ) -> Dict:
        """
        Run complete simulation.
        
        Args:
            signal_data: List of signal data for each epoch
            reference_trajectory: List of reference positions
            scenarios: List of scenarios for each epoch
            interferences: List of interferences for each epoch
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with complete simulation results
        """
        n_epochs = len(signal_data)
        
        # Ensure all inputs have same length
        assert len(reference_trajectory) == n_epochs
        assert len(scenarios) == n_epochs
        assert len(interferences) == n_epochs
        
        # Initialize
        self.initialize(scenarios[0], interferences[0])
        
        # Run simulation
        for i in range(n_epochs):
            self.step(
                input_signals=signal_data[i],
                reference_position=reference_trajectory[i],
                scenario=scenarios[i],
                interference=interferences[i],
                **kwargs
            )
        
        return self.results
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from simulation results.
        
        Returns:
            Dictionary with statistics (mean error, std, etc.)
        """
        if len(self.results['errors']) == 0:
            return {}
        
        errors = np.array([e.error_distance for e in self.results['errors']])
        error_east = np.array([e.error_east for e in self.results['errors'] if e.error_east is not None])
        error_north = np.array([e.error_north for e in self.results['errors'] if e.error_north is not None])
        error_up = np.array([e.error_up for e in self.results['errors'] if e.error_up is not None])
        
        stats = {
            'mean_error': np.mean(errors),
            'std_error': np.std(errors),
            'min_error': np.min(errors),
            'max_error': np.max(errors),
            'median_error': np.median(errors),
            'rmse': np.sqrt(np.mean(errors**2))
        }
        
        if len(error_east) > 0:
            stats['mean_error_east'] = np.mean(error_east)
            stats['std_error_east'] = np.std(error_east)
            stats['mean_error_north'] = np.mean(error_north)
            stats['std_error_north'] = np.std(error_north)
            stats['mean_error_up'] = np.mean(error_up)
            stats['std_error_up'] = np.std(error_up)
        
        return stats
