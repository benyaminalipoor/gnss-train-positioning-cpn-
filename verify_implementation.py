#!/usr/bin/env python3
"""
Verification script to ensure all components work correctly
"""

import sys
import os
import numpy as np

# Import all components
from gnss_train_positioning_simulation import (
    Scenario, InterferenceState, TunnelState,
    Signal, Coordinate, Mountain,
    GNSSSignalGenerator, InterferenceGenerator,
    EnvironmentScenario, ExtendedKalmanFilter,
    GNSSTrainPositioningSimulator
)

def verify_imports():
    """Verify all required imports work"""
    print("✓ Verifying imports...")
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd
        print("  ✓ All imports successful")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

def verify_data_structures():
    """Verify all data structures are defined"""
    print("✓ Verifying data structures...")
    try:
        # Test enums
        assert hasattr(Scenario, 'OPEN_AREA')
        assert hasattr(InterferenceState, 'AM')
        assert hasattr(TunnelState, 'IN_TUNNEL')
        
        # Test dataclasses
        signal = Signal(1, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        coord = Coordinate(0.0, 0.0, 100.0)
        mountain = Mountain(200.0, 1000.0)
        
        print("  ✓ All data structures defined correctly")
        return True
    except Exception as e:
        print(f"  ✗ Data structure verification failed: {e}")
        return False

def verify_signal_generation():
    """Verify GNSS signal generation"""
    print("✓ Verifying signal generation...")
    try:
        gen = GNSSSignalGenerator()
        signals = gen.generate_test_signals(0)
        assert len(signals) > 0, "No signals generated"
        assert all(hasattr(s, 'elevation') for s in signals), "Signals missing attributes"
        print(f"  ✓ Generated {len(signals)} signals successfully")
        return True
    except Exception as e:
        print(f"  ✗ Signal generation failed: {e}")
        return False

def verify_interference():
    """Verify interference models"""
    print("✓ Verifying interference models...")
    try:
        gen = GNSSSignalGenerator()
        int_gen = InterferenceGenerator()
        signals = gen.generate_test_signals(0)
        
        # Test AM
        am_sig, am_err = int_gen.am_interference(1.0, signals)
        assert len(am_sig) == len(signals), "AM interference changed signal count"
        
        # Test FM
        fm_sig, fm_err = int_gen.fm_interference(1.0, signals)
        assert len(fm_sig) == len(signals), "FM interference changed signal count"
        
        # Test Pulse
        pulse_sig, pulse_err = int_gen.pulse_interference(1.0, signals)
        assert len(pulse_sig) == len(signals), "Pulse interference changed signal count"
        
        print("  ✓ All interference models working")
        return True
    except Exception as e:
        print(f"  ✗ Interference verification failed: {e}")
        return False

def verify_ekf():
    """Verify Extended Kalman Filter"""
    print("✓ Verifying EKF...")
    try:
        ekf = ExtendedKalmanFilter()
        gen = GNSSSignalGenerator()
        
        # Test prediction
        initial_state = ekf.state.copy()
        ekf.predict()
        assert not np.array_equal(ekf.state, initial_state), "EKF prediction not working"
        
        # Test update
        signals = gen.generate_test_signals(0)
        if signals:
            ekf.update(signals)
        
        # Test position retrieval
        pos = ekf.get_position()
        assert isinstance(pos, Coordinate), "Position not a Coordinate"
        
        print("  ✓ EKF working correctly")
        return True
    except Exception as e:
        print(f"  ✗ EKF verification failed: {e}")
        return False

def verify_environment_scenarios():
    """Verify environment scenarios"""
    print("✓ Verifying environment scenarios...")
    try:
        env = EnvironmentScenario()
        gen = GNSSSignalGenerator()
        signals = gen.generate_test_signals(0)
        
        # Test open area
        open_sig, err = env.open_area_scenario(signals, InterferenceState.NORMAL, 0)
        assert len(open_sig) == len(signals), "Open area changed signal count unexpectedly"
        
        # Test mountain
        mountain = Mountain(200, 1000)
        mount_sig = env.mountain_scenario(signals, mountain)
        assert len(mount_sig) <= len(signals), "Mountain should filter signals"
        
        # Test tunnel
        tunnel_sig, err = env.tunnel_scenario(signals, TunnelState.IN_TUNNEL, 0)
        assert len(tunnel_sig) == 0, "Tunnel should block all signals when inside"
        
        print("  ✓ All environment scenarios working")
        return True
    except Exception as e:
        print(f"  ✗ Environment scenario verification failed: {e}")
        return False

def verify_simulator():
    """Verify main simulator"""
    print("✓ Verifying main simulator...")
    try:
        sim = GNSSTrainPositioningSimulator()
        
        # Run short simulation
        results = sim.simulate_scenario(Scenario.OPEN_AREA, InterferenceState.NORMAL, 10)
        
        assert 'time' in results, "Results missing 'time'"
        assert 'errors' in results, "Results missing 'errors'"
        assert 'positions' in results, "Results missing 'positions'"
        assert len(results['time']) == 10, "Wrong number of time steps"
        
        # Test statistics
        stats = sim.calculate_statistics(results['errors'])
        assert 'mean_error' in stats, "Statistics missing 'mean_error'"
        assert 'std_dev' in stats, "Statistics missing 'std_dev'"
        
        print("  ✓ Simulator working correctly")
        return True
    except Exception as e:
        print(f"  ✗ Simulator verification failed: {e}")
        return False

def verify_output_files():
    """Verify all expected output files exist"""
    print("✓ Verifying output files...")
    
    expected_files = [
        'figure_1_framework.png',
        'figure_2_hierarchy.png',
        'figure_3_top_level.png',
        'figure_4_gnss_receiver.png',
        'figure_5_open_area.png',
        'figure_6_mountain.png',
        'figure_7_tunnel.png',
        'figure_8_position_solution.png',
        'figure_9_evaluation.png',
        'figure_10_tunnel_errors.png',
        'automaton_state_machine.png',
        'table_4_interference_performance.png',
        'table_5_environment_performance.png',
    ]
    
    missing = []
    for file in expected_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"  ✗ Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"  ✓ All {len(expected_files)} output files present")
        return True

def main():
    """Run all verification tests"""
    print("\n" + "="*80)
    print(" GNSS TRAIN POSITIONING - VERIFICATION")
    print("="*80 + "\n")
    
    tests = [
        ("Imports", verify_imports),
        ("Data Structures", verify_data_structures),
        ("Signal Generation", verify_signal_generation),
        ("Interference Models", verify_interference),
        ("Extended Kalman Filter", verify_ekf),
        ("Environment Scenarios", verify_environment_scenarios),
        ("Main Simulator", verify_simulator),
        ("Output Files", verify_output_files),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} test crashed: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("="*80)
    print(" VERIFICATION SUMMARY")
    print("="*80 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8s} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL VERIFICATIONS PASSED! System is working correctly.")
        print("="*80 + "\n")
        return 0
    else:
        print("\n✗ SOME VERIFICATIONS FAILED! Please check errors above.")
        print("="*80 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
