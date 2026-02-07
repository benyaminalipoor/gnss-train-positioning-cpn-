"""
Quick Start Example

This script demonstrates basic usage of the GNSS Train Positioning CPN simulation.
Run this as a simple introduction before running the full paper reproduction.
"""

import sys
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cpn.model import CPNModel
from src.cpn.tokens import Scenario, StateInterference
from src.utils.data_loader import (
    generate_satellite_signals,
    generate_reference_trajectory
)
from src.utils.visualization import plot_positioning_errors


def main():
    print("=" * 60)
    print("GNSS Train Positioning CPN - Quick Start Example")
    print("=" * 60)
    
    # Configuration
    n_epochs = 60  # 60 seconds (1 minute)
    n_satellites = 8
    
    print(f"\nSimulation configuration:")
    print(f"  Duration: {n_epochs} seconds")
    print(f"  Satellites: {n_satellites}")
    
    # Step 1: Generate data
    print("\n[1/4] Generating satellite signals...")
    signal_data = generate_satellite_signals(
        n_epochs=n_epochs,
        n_satellites=n_satellites,
        noise_std=3.0,
        random_seed=42
    )
    print(f"  ✓ Generated {n_epochs} epochs of GNSS signals")
    
    # Step 2: Generate reference trajectory
    print("\n[2/4] Generating reference trajectory...")
    reference_trajectory = generate_reference_trajectory(
        n_epochs=n_epochs,
        velocity=50.0,  # 50 m/s (~180 km/h)
        trajectory_type='linear'
    )
    print(f"  ✓ Generated reference trajectory with {len(reference_trajectory)} points")
    
    # Step 3: Run simulation
    print("\n[3/4] Running CPN simulation...")
    print("  Scenario: Open Area")
    print("  Interference: Normal (no interference)")
    
    model = CPNModel()
    
    # Create scenario and interference sequences
    scenarios = [Scenario.OPEN_AREA] * n_epochs
    interferences = [StateInterference.NORMAL] * n_epochs
    
    # Run simulation
    results = model.run_simulation(
        signal_data=signal_data,
        reference_trajectory=reference_trajectory,
        scenarios=scenarios,
        interferences=interferences
    )
    
    print(f"  ✓ Simulation completed ({n_epochs} epochs)")
    
    # Step 4: Calculate and display statistics
    print("\n[4/4] Calculating statistics...")
    stats = model.get_statistics()
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Mean positioning error:   {stats['mean_error']:.4f} meters")
    print(f"Standard deviation:       {stats['std_error']:.4f} meters")
    print(f"Minimum error:            {stats['min_error']:.4f} meters")
    print(f"Maximum error:            {stats['max_error']:.4f} meters")
    print(f"RMSE:                     {stats['rmse']:.4f} meters")
    
    if 'mean_error_east' in stats:
        print(f"\nDirectional errors:")
        print(f"  East:  {stats['mean_error_east']:.4f} ± {stats['std_error_east']:.4f} m")
        print(f"  North: {stats['mean_error_north']:.4f} ± {stats['std_error_north']:.4f} m")
        print(f"  Up:    {stats['mean_error_up']:.4f} ± {stats['std_error_up']:.4f} m")
    
    print("=" * 60)
    
    # Generate plot
    try:
        from pathlib import Path
        output_dir = Path("results/figures")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        plot_positioning_errors(
            results,
            output_file=str(output_dir / "quickstart_errors.png"),
            title="Quick Start: Positioning Errors"
        )
        print(f"\n✓ Plot saved to: {output_dir / 'quickstart_errors.png'}")
    except Exception as e:
        print(f"\n⚠ Could not generate plot: {e}")
    
    print("\n" + "=" * 60)
    print("Quick start example completed successfully!")
    print("\nNext steps:")
    print("  1. Run the full paper reproduction: python scripts/reproduce_paper.py")
    print("  2. Explore the code in src/")
    print("  3. Read the documentation in docs/")
    print("=" * 60)


if __name__ == "__main__":
    main()
