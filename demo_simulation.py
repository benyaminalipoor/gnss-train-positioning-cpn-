#!/usr/bin/env python3
"""
Demonstration script for GNSS Train Positioning Simulation
Shows key features and capabilities of the implementation
"""

import numpy as np
from gnss_train_positioning_simulation import (
    GNSSTrainPositioningSimulator,
    Scenario,
    InterferenceState
)

def demonstrate_features():
    """Demonstrate key features of the simulation"""
    
    print("\n" + "="*80)
    print(" GNSS TRAIN POSITIONING - DEMONSTRATION")
    print("="*80 + "\n")
    
    # Initialize simulator
    simulator = GNSSTrainPositioningSimulator()
    
    # Demo 1: Compare interference types
    print("Demo 1: Comparing Signal Interference Types")
    print("-" * 80)
    
    interference_types = [
        (InterferenceState.NORMAL, "Normal (No Interference)"),
        (InterferenceState.AM, "AM Interference"),
        (InterferenceState.FM, "FM Interference"),
        (InterferenceState.PULSE, "Pulse Interference")
    ]
    
    for interference, name in interference_types:
        results = simulator.simulate_scenario(
            Scenario.OPEN_AREA,
            interference,
            duration=100  # Short duration for demo
        )
        stats = simulator.calculate_statistics(results['errors'])
        print(f"{name:25s} - Mean Error: {stats['mean_error']:8.2f} m, "
              f"Max Error: {stats['max_error']:8.2f} m")
    
    # Demo 2: Compare environment scenarios
    print("\n\nDemo 2: Comparing Environment Scenarios")
    print("-" * 80)
    
    scenarios = [
        (Scenario.OPEN_AREA, "Open Area"),
        (Scenario.MOUNTAIN, "Mountain Occlusion"),
        (Scenario.TUNNEL, "Tunnel")
    ]
    
    for scenario, name in scenarios:
        results = simulator.simulate_scenario(
            scenario,
            InterferenceState.NORMAL,
            duration=100
        )
        stats = simulator.calculate_statistics(results['errors'])
        print(f"{name:25s} - Mean Error: {stats['mean_error']:8.2f} m, "
              f"Satellites: {np.mean(results['num_satellites']):.1f}")
    
    # Demo 3: Tunnel scenario analysis
    print("\n\nDemo 3: Tunnel Scenario - Three Phases")
    print("-" * 80)
    
    results = simulator.simulate_scenario(
        Scenario.TUNNEL,
        InterferenceState.NORMAL,
        duration=500
    )
    
    # Analyze different phases
    inside_tunnel = results['errors'][200:300]  # Inside tunnel
    just_out = results['errors'][300:350]       # Just exited
    stabilized = results['errors'][400:450]     # Stabilized
    
    print(f"Inside Tunnel (200-300s):  Mean Error: {np.mean(inside_tunnel):8.2f} m")
    print(f"Just After Exit (300-350s): Mean Error: {np.mean(just_out):8.2f} m")
    print(f"Stabilized (400-450s):      Mean Error: {np.mean(stabilized):8.2f} m")
    
    # Demo 4: Signal characteristics
    print("\n\nDemo 4: GNSS Signal Characteristics")
    print("-" * 80)
    
    signals = simulator.signal_gen.generate_test_signals(0)
    print(f"Number of visible satellites: {len(signals)}")
    print(f"Average elevation angle: {np.mean([s.elevation for s in signals]):.1f}°")
    print(f"Average pseudorange: {np.mean([s.psr for s in signals])/1000:.1f} km")
    
    # Demo 5: EKF performance
    print("\n\nDemo 5: Extended Kalman Filter Performance")
    print("-" * 80)
    
    ekf = simulator.ekf
    print(f"Initial state: Position = ({ekf.state[0]:.1f}, {ekf.state[1]:.1f}, {ekf.state[2]:.1f}) m")
    print(f"Initial velocity: ({ekf.state[3]:.1f}, {ekf.state[4]:.1f}, {ekf.state[5]:.1f}) m/s")
    
    # Run a few prediction steps
    for i in range(5):
        ekf.predict()
    
    print(f"After 5 predictions: Position = ({ekf.state[0]:.1f}, {ekf.state[1]:.1f}, {ekf.state[2]:.1f}) m")
    
    print("\n" + "="*80)
    print(" DEMONSTRATION COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    demonstrate_features()
