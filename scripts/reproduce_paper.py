"""
Main Simulation Script to Reproduce Paper Results

This script reproduces the results from the paper:
"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"

It runs simulations for different scenarios and interference types,
matching Table 4 and Table 5 from the paper.
"""

import sys
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cpn.model import CPNModel
from src.cpn.tokens import Scenario, StateInterference, Coordinate
from src.utils.config import load_config
from src.utils.data_loader import (
    generate_satellite_signals,
    generate_reference_trajectory,
    generate_scenario_sequence,
    save_results_to_csv
)
from src.utils.visualization import (
    plot_positioning_errors,
    plot_error_components,
    plot_interference_comparison,
    plot_scenario_comparison,
    create_results_table,
    generate_all_plots
)


def run_single_simulation(
    scenario: Scenario,
    interference: StateInterference,
    n_epochs: int = 600,
    config: dict = None
):
    """
    Run a single simulation with specified scenario and interference.
    
    Args:
        scenario: Environment scenario
        interference: Interference type
        n_epochs: Number of time epochs (seconds)
        config: Configuration dictionary
        
    Returns:
        Simulation results
    """
    print(f"\nRunning simulation: Scenario={scenario.value}, Interference={interference.value}")
    
    # Generate data
    print("Generating reference trajectory...")
    reference_trajectory = generate_reference_trajectory(
        n_epochs=n_epochs,
        velocity=50.0,  # 50 m/s (~180 km/h)
        trajectory_type='linear'
    )
    
    print("Generating satellite signals...")
    from src.utils.data_loader import generate_satellite_signals_for_trajectory
    signal_data = generate_satellite_signals_for_trajectory(
        reference_trajectory=reference_trajectory,
        n_satellites=8,
        noise_std=3.0,
        random_seed=42
    )
    
    # Create scenario and interference sequences
    scenarios = [scenario] * n_epochs
    interferences = [interference] * n_epochs
    
    # Initialize and run CPN model
    print("Running CPN simulation...")
    model = CPNModel(config)
    results = model.run_simulation(
        signal_data=signal_data,
        reference_trajectory=reference_trajectory,
        scenarios=scenarios,
        interferences=interferences,
        mountain_height=500.0,
        mountain_distance=1000.0
    )
    
    # Calculate statistics
    stats = model.get_statistics()
    
    print(f"Results: Mean Error = {stats['mean_error']:.4f} m, "
          f"Std = {stats['std_error']:.4f} m")
    
    return results, stats


def reproduce_table_4(config: dict = None):
    """
    Reproduce Table 4 from the paper:
    "Positioning performances under different signal interferences"
    
    Scenarios: Open Area with different interferences
    """
    print("\n" + "=" * 80)
    print("REPRODUCING TABLE 4: Positioning Performance Under Different Interferences")
    print("=" * 80)
    
    interference_types = [
        ('Normal', StateInterference.NORMAL),
        ('AM', StateInterference.AM),
        ('FM', StateInterference.FM),
        ('Pulse', StateInterference.PULSE)
    ]
    
    results_dict = {}
    stats_dict = {}
    
    for name, interference in interference_types:
        results, stats = run_single_simulation(
            scenario=Scenario.OPEN_AREA,
            interference=interference,
            n_epochs=600,
            config=config
        )
        results_dict[name] = results
        stats_dict[name] = stats
    
    # Print results table
    print("\n" + "=" * 100)
    print("Table 4: Positioning Performance Under Different Signal Interferences")
    print("=" * 100)
    print(f"{'Scenario':<15} {'Mean Error (m)':<20} {'Std Deviation (m)':<20}")
    print("-" * 100)
    
    for name, stats in stats_dict.items():
        print(f"{name:<15} {stats['mean_error']:>18.4f} {stats['std_error']:>18.4f}")
    
    print("=" * 100)
    
    # Generate comparison plot
    from pathlib import Path
    output_dir = Path("results/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_interference_comparison(
        results_dict,
        output_file=str(output_dir / "table4_interference_comparison.png"),
        title="Table 4: Positioning Performance by Interference Type"
    )
    
    # Save detailed results
    for name, results in results_dict.items():
        save_results_to_csv(
            results,
            f"results/tables/table4_{name.lower()}_results.csv"
        )
    
    return results_dict, stats_dict


def reproduce_table_5(config: dict = None):
    """
    Reproduce Table 5 from the paper:
    "Positioning performances under different environment scenarios"
    
    Scenarios: Open Area, Mountain, Tunnel (with Normal interference)
    """
    print("\n" + "=" * 80)
    print("REPRODUCING TABLE 5: Positioning Performance Under Different Scenarios")
    print("=" * 80)
    
    scenario_types = [
        ('Open Area', Scenario.OPEN_AREA),
        ('Mountain', Scenario.MOUNTAIN),
        ('Tunnel', Scenario.TUNNEL)
    ]
    
    results_dict = {}
    stats_dict = {}
    
    for name, scenario in scenario_types:
        results, stats = run_single_simulation(
            scenario=scenario,
            interference=StateInterference.NORMAL,
            n_epochs=600,
            config=config
        )
        results_dict[name] = results
        stats_dict[name] = stats
    
    # Print results table
    print("\n" + "=" * 100)
    print("Table 5: Positioning Performance Under Different Environment Scenarios")
    print("=" * 100)
    print(f"{'Scenario':<15} {'Mean Error (m)':<20} {'Std Deviation (m)':<20}")
    print("-" * 100)
    
    for name, stats in stats_dict.items():
        print(f"{name:<15} {stats['mean_error']:>18.4f} {stats['std_error']:>18.4f}")
    
    print("=" * 100)
    
    # Generate comparison plot
    from pathlib import Path
    output_dir = Path("results/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_scenario_comparison(
        results_dict,
        output_file=str(output_dir / "table5_scenario_comparison.png"),
        title="Table 5: Positioning Performance by Environment Scenario"
    )
    
    # Save detailed results
    for name, results in results_dict.items():
        save_results_to_csv(
            results,
            f"results/tables/table5_{name.lower().replace(' ', '_')}_results.csv"
        )
    
    return results_dict, stats_dict


def main():
    """Main execution function."""
    print("=" * 80)
    print("GNSS Train Positioning CPN Simulation")
    print("Reproducing Paper Results")
    print("=" * 80)
    
    # Load configuration
    config = load_config()
    
    # Set random seed for reproducibility
    np.random.seed(config.get('simulation.random_seed', 42))
    
    # Reproduce paper tables
    print("\n### PART 1: Interference Effects (Table 4) ###")
    results_table4, stats_table4 = reproduce_table_4(config.to_dict())
    
    print("\n### PART 2: Environment Scenarios (Table 5) ###")
    results_table5, stats_table5 = reproduce_table_5(config.to_dict())
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    
    print("\n### Expected Results from Paper ###")
    print("Table 4 (Open Area with different interferences):")
    print("  Normal: Mean = 1.03 m, Std = 0.06 m")
    print("  AM:     Mean = 4.95 m, Std = 4.08 m")
    print("  FM:     Mean = 6.22 m, Std = 5.26 m")
    print("  Pulse:  Mean = 4.79 m, Std = 3.62 m")
    
    print("\n### Simulation Results ###")
    print("Table 4 Results:")
    for name, stats in stats_table4.items():
        print(f"  {name:<8}: Mean = {stats['mean_error']:.2f} m, "
              f"Std = {stats['std_error']:.2f} m")
    
    print("\nTable 5 Results:")
    for name, stats in stats_table5.items():
        print(f"  {name:<12}: Mean = {stats['mean_error']:.2f} m, "
              f"Std = {stats['std_error']:.2f} m")
    
    print("\n" + "=" * 80)
    print("Simulation completed successfully!")
    print("Results saved to:")
    print("  - results/figures/")
    print("  - results/tables/")
    print("=" * 80)


if __name__ == "__main__":
    main()
