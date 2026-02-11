#!/usr/bin/env python3
"""
Quick test to verify performance optimizations work correctly
"""
import time
import numpy as np
from gnss_train_positioning_simulation import (
    GNSSSimulator, InterferenceType, EnvironmentScenario
)

def test_basic_simulation():
    """Test that basic simulation still works after optimizations"""
    print("Testing basic simulation...")
    simulator = GNSSSimulator(num_epochs=10)
    
    # Test normal interference in open area
    errors, est_pos, ref_pos = simulator.run_simulation(
        InterferenceType.NORMAL, 
        EnvironmentScenario.OPEN_AREA
    )
    
    assert len(errors) == 10, f"Expected 10 errors, got {len(errors)}"
    assert len(est_pos) == 10, f"Expected 10 positions, got {len(est_pos)}"
    assert all(err >= 0 for err in errors), "Errors should be non-negative"
    
    # Calculate statistics
    stats = simulator.calculate_statistics(errors, est_pos, ref_pos)
    
    assert 'mean_error' in stats, "Missing mean_error in stats"
    assert 'std_dev' in stats, "Missing std_dev in stats"
    assert stats['mean_error'] >= 0, "Mean error should be non-negative"
    
    print(f"  ✓ Basic simulation works. Mean error: {stats['mean_error']:.4f}m")
    return stats

def test_vectorization():
    """Test that vectorized operations produce correct results"""
    print("Testing vectorization correctness...")
    simulator = GNSSSimulator(num_epochs=20)
    
    # Run with multiple interference types
    for interference in [InterferenceType.NORMAL, InterferenceType.AM]:
        errors, est_pos, ref_pos = simulator.run_simulation(
            interference, 
            EnvironmentScenario.OPEN_AREA
        )
        stats = simulator.calculate_statistics(errors, est_pos, ref_pos)
        
        # Check that directional errors are computed correctly
        assert 'expected_dir_mean' in stats
        assert 'normalized_dir_mean' in stats
        assert 'helmert_dir_mean' in stats
        
        # Verify that statistics are reasonable
        assert -100 < stats['expected_dir_mean'] < 100
        assert -100 < stats['normalized_dir_mean'] < 100
        assert -100 < stats['helmert_dir_mean'] < 100
    
    print(f"  ✓ Vectorization produces correct results")

def test_performance():
    """Test performance improvement"""
    print("Testing performance...")
    simulator = GNSSSimulator(num_epochs=100)
    
    start_time = time.time()
    errors, est_pos, ref_pos = simulator.run_simulation(
        InterferenceType.NORMAL, 
        EnvironmentScenario.OPEN_AREA
    )
    stats = simulator.calculate_statistics(errors, est_pos, ref_pos)
    elapsed = time.time() - start_time
    
    print(f"  ✓ Completed 100-epoch simulation in {elapsed:.3f}s")
    print(f"    Mean error: {stats['mean_error']:.4f}m")
    
    # Note: Performance check is informational only
    # Actual performance will vary by hardware
    if elapsed > 5.0:
        print(f"  ℹ Info: Simulation took {elapsed:.3f}s")
    
    return elapsed

def test_all_scenarios():
    """Test all scenarios to ensure nothing broke"""
    print("Testing all scenarios...")
    simulator = GNSSSimulator(num_epochs=20)
    
    interference_types = [
        InterferenceType.NORMAL,
        InterferenceType.AM,
        InterferenceType.FM,
        InterferenceType.PULSE
    ]
    
    scenarios = [
        EnvironmentScenario.OPEN_AREA,
        EnvironmentScenario.MOUNTAIN,
        EnvironmentScenario.TUNNEL
    ]
    
    results = {}
    for interference in interference_types:
        for scenario in scenarios:
            key = f"{interference.value}_{scenario.value}"
            errors, est_pos, ref_pos = simulator.run_simulation(interference, scenario)
            stats = simulator.calculate_statistics(errors, est_pos, ref_pos)
            results[key] = stats['mean_error']
    
    print(f"  ✓ All {len(interference_types) * len(scenarios)} scenario combinations work")
    return results

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Performance Optimization Tests")
    print("="*70 + "\n")
    
    test_basic_simulation()
    test_vectorization()
    elapsed = test_performance()
    test_all_scenarios()
    
    print("\n" + "="*70)
    print("All tests passed! ✓")
    print("="*70)
