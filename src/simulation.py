"""
Main Simulation Script for GNSS Train Positioning System
Based on the paper: "Modeling and performance analysis of GNSS-based train 
positioning system with colored petri nets"

Runs simulations matching the paper's results:
- Table 4: Positioning under different signal interferences
- Table 5: Positioning under different environment scenarios
- Figure 10: Position errors in tunnel scenario
"""

import numpy as np
import os
import json
from typing import List, Dict
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gnss_processing import (
    generate_synthetic_gnss_data, Position,
    ScenarioType, InterferenceType, TunnelState
)
from cpn_model import GNSSTrainPositioningCPN


def generate_reference_trajectory(num_points: int = 600) -> List[Position]:
    """
    Generate reference trajectory for train
    
    Simulates a segment of train movement along a track
    Based on Jing-Shen high-speed railway
    """
    # Starting position (approximate ECEF near Beijing)
    start_x, start_y, start_z = -2148744.0, 4426641.0, 4044655.0
    
    # Train speed: ~300 km/h = 83.3 m/s
    # For 600 seconds = 10 minutes, travels ~50 km
    speed = 83.3  # m/s
    
    trajectory = []
    for i in range(num_points):
        # Simplified linear movement (real trajectory would follow track)
        t = i * 1.0  # time in seconds
        
        # Small variations to simulate real track
        x = start_x + speed * t * 0.6 + np.random.normal(0, 0.5)
        y = start_y + speed * t * 0.8 + np.random.normal(0, 0.5)
        z = start_z + np.random.normal(0, 0.2)  # Nearly constant elevation
        
        trajectory.append(Position(x=x, y=y, z=z))
    
    return trajectory


def run_interference_scenarios(gnss_data: List, reference_trajectory: List[Position]) -> Dict:
    """
    Run simulations for different signal interference scenarios
    Generates results matching Table 4 in the paper
    """
    print("\n" + "="*80)
    print("RUNNING INTERFERENCE SCENARIO SIMULATIONS (Table 4)")
    print("="*80)
    
    results = {}
    
    interference_types = [
        (InterferenceType.NORMAL, "Normal (No Interference)"),
        (InterferenceType.AM, "AM Interference"),
        (InterferenceType.FM, "FM Interference"),
        (InterferenceType.PULSE, "Pulse Interference")
    ]
    
    for interference_type, description in interference_types:
        print(f"\nSimulating: {description}")
        print("-" * 60)
        
        # Initialize CPN model
        cpn = GNSSTrainPositioningCPN(
            reference_trajectory=reference_trajectory,
            initial_position=reference_trajectory[0]
        )
        
        # Set scenario to Open Area
        cpn.set_scenario(ScenarioType.OPEN_AREA)
        
        # Set interference type
        cpn.set_interference(interference_type)
        
        # Run simulation
        sim_results = cpn.run_simulation(gnss_data)
        
        # Print statistics
        stats = sim_results['statistics']
        print(f"  Valid Epochs: {sim_results['valid_epochs']}/{sim_results['total_epochs']}")
        print(f"  Mean Error: {stats['mean_error']:.4f} m")
        print(f"  Std Deviation: {stats['std_deviation']:.4f} m")
        print(f"  RMS Error: {stats['rms_error']:.4f} m")
        
        results[interference_type.value] = {
            'description': description,
            'statistics': stats,
            'errors': sim_results['errors'],
            'valid_epochs': sim_results['valid_epochs']
        }
    
    return results


def run_environment_scenarios(gnss_data: List, reference_trajectory: List[Position]) -> Dict:
    """
    Run simulations for different environment scenarios
    Generates results matching Table 5 in the paper
    """
    print("\n" + "="*80)
    print("RUNNING ENVIRONMENT SCENARIO SIMULATIONS (Table 5)")
    print("="*80)
    
    results = {}
    
    scenarios = [
        (ScenarioType.OPEN_AREA, {}, "Open Area"),
        (ScenarioType.MOUNTAIN, {'mountain_height': 100.0, 'mountain_distance': 1000.0}, "Mountain Occlusion"),
    ]
    
    for scenario_type, params, description in scenarios:
        print(f"\nSimulating: {description}")
        print("-" * 60)
        
        # Initialize CPN model
        cpn = GNSSTrainPositioningCPN(
            reference_trajectory=reference_trajectory,
            initial_position=reference_trajectory[0]
        )
        
        # Set scenario
        cpn.set_scenario(scenario_type, **params)
        
        # No interference for environment scenarios
        cpn.set_interference(InterferenceType.NORMAL)
        
        # Run simulation
        sim_results = cpn.run_simulation(gnss_data)
        
        # Print statistics
        stats = sim_results['statistics']
        print(f"  Valid Epochs: {sim_results['valid_epochs']}/{sim_results['total_epochs']}")
        print(f"  Mean Error: {stats['mean_error']:.4f} m")
        print(f"  Std Deviation: {stats['std_deviation']:.4f} m")
        print(f"  RMS Error: {stats['rms_error']:.4f} m")
        
        results[scenario_type.value] = {
            'description': description,
            'statistics': stats,
            'errors': sim_results['errors'],
            'valid_epochs': sim_results['valid_epochs']
        }
    
    # Tunnel scenario (special handling with three phases)
    print(f"\nSimulating: Tunnel Scenario")
    print("-" * 60)
    
    cpn = GNSSTrainPositioningCPN(
        reference_trajectory=reference_trajectory,
        initial_position=reference_trajectory[0]
    )
    
    tunnel_errors = []
    tunnel_timestamps = []
    valid_count = 0
    
    # Simulate tunnel scenario with three phases
    tunnel_entry_time = 200  # Enter tunnel at 200s
    tunnel_exit_time = 300   # Exit tunnel at 300s
    
    for obs in gnss_data:
        t = obs.timestamp
        
        if t < tunnel_entry_time:
            # Before tunnel - normal
            cpn.set_scenario(ScenarioType.TUNNEL, 
                           tunnel_state=TunnelState.OUT_TUNNEL)
        elif t < tunnel_exit_time:
            # Inside tunnel - no signals
            cpn.set_scenario(ScenarioType.TUNNEL,
                           tunnel_state=TunnelState.IN_TUNNEL)
        elif t < tunnel_exit_time + 30:
            # Just exited - high errors
            time_since_exit = t - tunnel_exit_time
            cpn.set_scenario(ScenarioType.TUNNEL,
                           tunnel_state=TunnelState.JUST_OUT,
                           time_since_exit=time_since_exit)
        else:
            # Fully out - normal
            cpn.set_scenario(ScenarioType.TUNNEL,
                           tunnel_state=TunnelState.OUT_TUNNEL)
        
        cpn.set_interference(InterferenceType.NORMAL)
        
        result = cpn.process_epoch(obs)
        if result is not None:
            _, error = result
            tunnel_errors.append(error)
            tunnel_timestamps.append(t)
            valid_count += 1
    
    tunnel_stats = {
        'mean_error': np.mean(tunnel_errors),
        'std_deviation': np.std(tunnel_errors),
        'rms_error': np.sqrt(np.mean(np.array(tunnel_errors)**2))
    }
    
    print(f"  Valid Epochs: {valid_count}/{len(gnss_data)}")
    print(f"  Mean Error: {tunnel_stats['mean_error']:.4f} m")
    print(f"  Std Deviation: {tunnel_stats['std_deviation']:.4f} m")
    print(f"  RMS Error: {tunnel_stats['rms_error']:.4f} m")
    
    results[ScenarioType.TUNNEL.value] = {
        'description': 'Tunnel',
        'statistics': tunnel_stats,
        'errors': tunnel_errors,
        'timestamps': tunnel_timestamps,
        'valid_epochs': valid_count,
        'tunnel_entry': tunnel_entry_time,
        'tunnel_exit': tunnel_exit_time
    }
    
    return results


def save_results(interference_results: Dict, environment_results: Dict, output_dir: str):
    """Save simulation results to files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as JSON
    results = {
        'interference_scenarios': interference_results,
        'environment_scenarios': environment_results
    }
    
    with open(os.path.join(output_dir, 'simulation_results.json'), 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to {output_dir}/simulation_results.json")


def print_summary_tables(interference_results: Dict, environment_results: Dict):
    """Print summary tables matching the paper format"""
    print("\n" + "="*80)
    print("SUMMARY: POSITIONING PERFORMANCE UNDER DIFFERENT SIGNAL INTERFERENCES (Table 4)")
    print("="*80)
    print(f"{'Scenario':<25} {'Mean Error (m)':<20} {'Std Deviation (m)':<20}")
    print("-" * 80)
    
    for key, data in interference_results.items():
        stats = data['statistics']
        print(f"{data['description']:<25} {stats['mean_error']:<20.4f} {stats['std_deviation']:<20.4f}")
    
    print("\n" + "="*80)
    print("SUMMARY: POSITIONING PERFORMANCE UNDER DIFFERENT ENVIRONMENT SCENARIOS (Table 5)")
    print("="*80)
    print(f"{'Scenario':<25} {'Mean Error (m)':<20} {'Std Deviation (m)':<20}")
    print("-" * 80)
    
    for key, data in environment_results.items():
        stats = data['statistics']
        print(f"{data['description']:<25} {stats['mean_error']:<20.4f} {stats['std_deviation']:<20.4f}")


def main():
    """Main simulation entry point"""
    print("="*80)
    print("GNSS TRAIN POSITIONING SYSTEM SIMULATION")
    print("Based on: Modeling and performance analysis of GNSS-based train")
    print("         positioning system with colored petri nets")
    print("="*80)
    
    # Simulation parameters (from paper)
    NUM_EPOCHS = 600  # 600 seconds = 10 minutes
    NUM_SATELLITES = 8
    
    print(f"\nSimulation Parameters:")
    print(f"  Duration: {NUM_EPOCHS} seconds (10 minutes)")
    print(f"  Satellites: {NUM_SATELLITES}")
    print(f"  Scenarios: Open Area, Mountain, Tunnel")
    print(f"  Interferences: Normal, AM, FM, Pulse")
    
    # Generate reference trajectory
    print("\nGenerating reference trajectory...")
    reference_trajectory = generate_reference_trajectory(NUM_EPOCHS)
    
    # Generate GNSS observation data
    print("Generating GNSS observation data...")
    gnss_data = generate_synthetic_gnss_data(
        num_epochs=NUM_EPOCHS,
        epoch_interval=1.0,
        num_satellites=NUM_SATELLITES,
        receiver_pos=reference_trajectory[0]
    )
    
    print(f"  Generated {len(gnss_data)} observation epochs")
    
    # Run interference scenarios
    interference_results = run_interference_scenarios(gnss_data, reference_trajectory)
    
    # Run environment scenarios
    environment_results = run_environment_scenarios(gnss_data, reference_trajectory)
    
    # Print summary tables
    print_summary_tables(interference_results, environment_results)
    
    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), 'results', 'outputs')
    save_results(interference_results, environment_results, output_dir)
    
    print("\n" + "="*80)
    print("SIMULATION COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\nNext steps:")
    print("  1. Check results/outputs/simulation_results.json for detailed data")
    print("  2. Run visualization script to generate plots")
    print("  3. Compare results with paper (Tables 4 & 5, Figure 10)")


if __name__ == "__main__":
    main()
