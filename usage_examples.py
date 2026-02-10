#!/usr/bin/env python3
"""
Usage Examples for GNSS Train Positioning Simulation
Shows how to use individual components and customize the simulation
"""

from gnss_train_positioning_simulation import *
import matplotlib.pyplot as plt

def example_1_basic_simulation():
    """Example 1: Run a basic simulation"""
    print("\n=== Example 1: Basic Simulation ===\n")
    
    simulator = GNSSTrainPositioningSimulator()
    
    # Run simulation for open area without interference
    results = simulator.simulate_scenario(
        scenario=Scenario.OPEN_AREA,
        interference=InterferenceState.NORMAL,
        duration=300  # 5 minutes
    )
    
    # Print statistics
    stats = simulator.calculate_statistics(results['errors'])
    print(f"Mean Error: {stats['mean_error']:.2f} m")
    print(f"Std Dev: {stats['std_dev']:.2f} m")
    print(f"Max Error: {stats['max_error']:.2f} m")
    print(f"Min Error: {stats['min_error']:.2f} m")

def example_2_signal_generation():
    """Example 2: Generate GNSS signals manually"""
    print("\n=== Example 2: GNSS Signal Generation ===\n")
    
    signal_gen = GNSSSignalGenerator()
    
    # Generate signals at time step 0
    signals = signal_gen.generate_test_signals(time_step=0, num_satellites=8)
    
    print(f"Generated {len(signals)} satellite signals:")
    for i, sig in enumerate(signals[:3]):  # Show first 3
        print(f"  Satellite {sig.id}: Elevation={sig.elevation:.1f}°, "
              f"Azimuth={sig.azimuth:.1f}°, PSR={sig.psr/1000:.1f} km")

def example_3_interference():
    """Example 3: Apply different interference types"""
    print("\n=== Example 3: Signal Interference ===\n")
    
    signal_gen = GNSSSignalGenerator()
    interference_gen = InterferenceGenerator()
    
    # Generate clean signals
    signals = signal_gen.generate_test_signals(0)
    original_psr = [s.psr for s in signals]
    
    # Apply AM interference
    am_signals, am_error = interference_gen.am_interference(1.0, signals)
    print(f"AM Interference Error: {am_error:.2f} m")
    
    # Apply FM interference
    fm_signals, fm_error = interference_gen.fm_interference(1.0, signals)
    print(f"FM Interference Error: {fm_error:.2f} m")
    
    # Apply Pulse interference
    pulse_signals, pulse_error = interference_gen.pulse_interference(1.0, signals)
    print(f"Pulse Interference Error: {pulse_error:.2f} m")

def example_4_ekf():
    """Example 4: Use Extended Kalman Filter"""
    print("\n=== Example 4: Extended Kalman Filter ===\n")
    
    ekf = ExtendedKalmanFilter()
    signal_gen = GNSSSignalGenerator()
    
    # Initial position
    print(f"Initial Position: ({ekf.state[0]:.1f}, {ekf.state[1]:.1f}, {ekf.state[2]:.1f}) m")
    
    # Run prediction-update cycle
    for i in range(10):
        ekf.predict(dt=1.0)
        signals = signal_gen.generate_test_signals(i)
        if signals:
            ekf.update(signals)
    
    # Final position
    final_pos = ekf.get_position()
    print(f"Final Position: ({final_pos.x:.1f}, {final_pos.y:.1f}, {final_pos.z:.1f}) m")

def example_5_environment_scenarios():
    """Example 5: Test different environment scenarios"""
    print("\n=== Example 5: Environment Scenarios ===\n")
    
    env = EnvironmentScenario()
    signal_gen = GNSSSignalGenerator()
    signals = signal_gen.generate_test_signals(0)
    
    print(f"Original signals: {len(signals)} satellites")
    
    # Mountain scenario
    mountain = Mountain(height=200, distance=1000)
    mountain_signals = env.mountain_scenario(signals, mountain)
    print(f"After mountain filtering: {len(mountain_signals)} satellites")
    
    # Tunnel scenario - inside
    tunnel_signals, error = env.tunnel_scenario(signals, TunnelState.IN_TUNNEL, 0)
    print(f"Inside tunnel: {len(tunnel_signals)} satellites")
    
    # Tunnel scenario - just out
    tunnel_signals, error = env.tunnel_scenario(signals, TunnelState.JUST_OUT, 5)
    print(f"Just out of tunnel: {len(tunnel_signals)} satellites, error: {error:.2f} m")

def example_6_custom_simulation():
    """Example 6: Create a custom simulation scenario"""
    print("\n=== Example 6: Custom Simulation ===\n")
    
    # Create custom components
    signal_gen = GNSSSignalGenerator()
    env = EnvironmentScenario()
    ekf = ExtendedKalmanFilter()
    
    errors = []
    
    # Custom simulation loop
    for t in range(100):
        # Generate signals
        signals = signal_gen.generate_test_signals(t)
        
        # Apply custom interference (AM at specific times)
        if 30 <= t < 60:
            signals, _ = env.open_area_scenario(signals, InterferenceState.AM, t)
        
        # EKF prediction and update
        ekf.predict()
        if signals:
            ekf.update(signals)
        
        # Calculate error (using simplified reference)
        estimated = ekf.get_position()
        reference = Coordinate(t * 20.0, 0, 100)
        error = estimated.distance_to(reference)
        errors.append(error)
    
    print(f"Custom simulation completed: {len(errors)} time steps")
    print(f"Average error: {np.mean(errors):.2f} m")

def example_7_visualization():
    """Example 7: Create custom visualizations"""
    print("\n=== Example 7: Custom Visualization ===\n")
    
    simulator = GNSSTrainPositioningSimulator()
    
    # Run multiple scenarios
    scenarios = [
        (Scenario.OPEN_AREA, 'Open Area'),
        (Scenario.MOUNTAIN, 'Mountain'),
        (Scenario.TUNNEL, 'Tunnel')
    ]
    
    plt.figure(figsize=(12, 6))
    
    for scenario, name in scenarios:
        results = simulator.simulate_scenario(scenario, InterferenceState.NORMAL, 200)
        plt.plot(results['time'], results['errors'], label=name, linewidth=2)
    
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Position Error (m)', fontsize=12)
    plt.title('Custom Comparison: Environment Scenarios', fontsize=14, weight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('custom_visualization.png', dpi=300)
    print("Saved custom_visualization.png")
    plt.close()

def main():
    """Run all examples"""
    print("\n" + "="*80)
    print(" GNSS TRAIN POSITIONING - USAGE EXAMPLES")
    print("="*80)
    
    example_1_basic_simulation()
    example_2_signal_generation()
    example_3_interference()
    example_4_ekf()
    example_5_environment_scenarios()
    example_6_custom_simulation()
    example_7_visualization()
    
    print("\n" + "="*80)
    print(" ALL EXAMPLES COMPLETED")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
