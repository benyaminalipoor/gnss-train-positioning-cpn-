#!/usr/bin/env python3
"""
Quick verification script to test the GNSS Train Positioning CPN implementation
Run this to verify everything is working correctly
"""

import sys
import os
from pathlib import Path

def check_files():
    """Check that all required files exist"""
    print("="*70)
    print("GNSS TRAIN POSITIONING CPN - VERIFICATION")
    print("="*70)
    print("\n1. Checking required files...")
    
    required_files = [
        'requirements.txt',
        'README.md',
        'IMPLEMENTATION_SUMMARY.md',
        'src/gnss_processing.py',
        'src/train_positioning.py',
        'src/cpn_model.py',
        'src/simulation.py',
        'src/visualize_results.py',
        'notebooks/analysis.ipynb'
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} - MISSING!")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check that required Python packages are installed"""
    print("\n2. Checking Python dependencies...")
    
    required_packages = ['numpy', 'scipy', 'matplotlib', 'pandas']
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} - NOT INSTALLED!")
            all_installed = False
    
    return all_installed

def check_results():
    """Check if simulation has been run and results exist"""
    print("\n3. Checking simulation results...")
    
    results_file = Path('src/results/outputs/simulation_results.json')
    plots_dir = Path('src/results/plots')
    
    if results_file.exists():
        size = results_file.stat().st_size / 1024
        print(f"   ✓ Results JSON exists ({size:.1f} KB)")
    else:
        print("   ✗ No results found - run simulation first")
        return False
    
    if plots_dir.exists():
        plots = list(plots_dir.glob('*.png'))
        print(f"   ✓ {len(plots)} plots generated")
        if len(plots) < 7:
            print(f"   ⚠ Expected 7 plots, found {len(plots)}")
    else:
        print("   ✗ No plots directory")
        return False
    
    return True

def run_quick_test():
    """Run a quick import test"""
    print("\n4. Running quick import test...")
    
    try:
        sys.path.insert(0, 'src')
        from gnss_processing import Position, InterferenceType
        from train_positioning import ExtendedKalmanFilter
        from cpn_model import GNSSTrainPositioningCPN
        print("   ✓ All modules importable")
        return True
    except Exception as e:
        print(f"   ✗ Import error: {e}")
        return False

def main():
    """Main verification"""
    results = []
    
    results.append(check_files())
    results.append(check_dependencies())
    results.append(check_results())
    results.append(run_quick_test())
    
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    if all(results[:2]):  # Files and dependencies
        print("✓ Installation: OK")
    else:
        print("✗ Installation: ISSUES FOUND")
    
    if results[2]:
        print("✓ Simulation: COMPLETE")
    else:
        print("⚠ Simulation: NOT RUN YET")
        print("\n  Run: python src/simulation.py")
        print("  Then: python src/visualize_results.py")
    
    if results[3]:
        print("✓ Code integrity: OK")
    else:
        print("✗ Code integrity: ISSUES FOUND")
    
    print("\n" + "="*70)
    
    if all(results):
        print("✅ ALL CHECKS PASSED - System ready!")
        return 0
    elif all(results[:2]) and results[3]:
        print("⚠️  READY TO RUN - Execute simulation to generate results")
        return 0
    else:
        print("❌ ISSUES DETECTED - Check errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
