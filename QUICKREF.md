# Quick Reference Guide

## Installation

```bash
pip install -r requirements.txt
```

## Running Simulations

### Quick Demo (1 minute)
```bash
python scripts/quickstart.py
```

### Full Paper Reproduction (~10 minutes)
```bash
python scripts/reproduce_paper.py
```

## Basic Usage

### Simple Simulation
```python
from src.cpn.model import CPNModel
from src.cpn.tokens import Scenario, StateInterference
from src.utils.data_loader import (
    generate_reference_trajectory,
    generate_satellite_signals_for_trajectory
)

# Generate data
trajectory = generate_reference_trajectory(n_epochs=100, velocity=50.0)
signals = generate_satellite_signals_for_trajectory(trajectory, n_satellites=8)

# Run simulation
model = CPNModel()
results = model.run_simulation(
    signal_data=signals,
    reference_trajectory=trajectory,
    scenarios=[Scenario.OPEN_AREA] * 100,
    interferences=[StateInterference.NORMAL] * 100
)

# Get results
stats = model.get_statistics()
print(f"Mean error: {stats['mean_error']:.2f} m")
```

### Test Interference Effects
```python
from src.cpn.tokens import StateInterference

# Test different interferences
for interference in [StateInterference.NORMAL, StateInterference.AM, 
                     StateInterference.FM, StateInterference.PULSE]:
    # ... run simulation with this interference
    pass
```

### Test Environment Scenarios
```python
from src.cpn.tokens import Scenario

# Test different scenarios
for scenario in [Scenario.OPEN_AREA, Scenario.MOUNTAIN, Scenario.TUNNEL]:
    # ... run simulation with this scenario
    pass
```

## Configuration

Edit `config/simulation_params.yaml`:

```yaml
gnss:
  min_satellites: 4
  pseudorange_noise_std: 3.0

interference:
  am:
    amplitude: 5.0
  fm:
    error_std: 6.0
  pulse:
    error_std: 5.0
    probability: 0.3
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_positioning.py -v

# Run with coverage
pytest tests/ --cov=src
```

## Project Structure

```
├── src/                    # Source code
│   ├── cpn/               # CPN model
│   ├── gnss/              # GNSS positioning
│   ├── filters/           # Kalman filter
│   └── utils/             # Utilities
├── scripts/               # Runnable scripts
├── tests/                 # Unit tests
├── config/                # Configuration
├── docs/                  # Documentation
└── results/               # Output (generated)
```

## Key Modules

### CPN Model
```python
from src.cpn.model import CPNModel
model = CPNModel()
model.initialize()
results = model.run_simulation(...)
stats = model.get_statistics()
```

### Positioning
```python
from src.gnss.positioning import calculate_position_from_signals
estimate = calculate_position_from_signals(signals, timestamp)
```

### EKF Filter
```python
from src.filters.kalman import ExtendedKalmanFilter
ekf = ExtendedKalmanFilter()
ekf.update_with_position(position, timestamp)
estimate = ekf.get_position_estimate(timestamp)
```

### Visualization
```python
from src.utils.visualization import plot_positioning_errors
plot_positioning_errors(results, output_file="errors.png")
```

## Common Tasks

### Generate Custom Trajectory
```python
from src.utils.data_loader import generate_reference_trajectory

# Linear trajectory
trajectory = generate_reference_trajectory(
    n_epochs=600,
    velocity=50.0,
    trajectory_type='linear'
)

# Curved trajectory
trajectory = generate_reference_trajectory(
    n_epochs=600,
    velocity=50.0,
    trajectory_type='curved'
)
```

### Save Results
```python
from src.utils.data_loader import save_results_to_csv
save_results_to_csv(results, "my_results.csv")
```

### Generate Plots
```python
from src.utils.visualization import generate_all_plots
generate_all_plots(results, output_dir="results/figures")
```

## Troubleshooting

### ImportError
```bash
# Make sure you're in the project directory
cd /path/to/gnss-train-positioning-cpn-

# Install dependencies
pip install -r requirements.txt
```

### Large Errors
- Check that you're using `generate_satellite_signals_for_trajectory()`
- Verify random seed is set for reproducibility
- Ensure reference trajectory matches signal generation

### No Output
- Check that output directories exist (created automatically)
- Verify matplotlib backend is working
- Try saving plots to files instead of showing

## Expected Results

### Normal (No Interference)
- Mean error: ~2-3 meters
- Std: ~5 meters

### AM Interference
- Mean error: ~8 meters
- Shows sinusoidal pattern

### FM Interference
- Mean error: ~6 meters
- Highest impact (as per paper)

### Pulse Interference
- Mean error: ~4 meters
- Sporadic spikes

## Further Reading

- `README.md`: Complete user guide
- `docs/architecture.md`: System architecture
- `docs/IMPLEMENTATION_SUMMARY.md`: Implementation details
- `Petrii.PDF`: Original research paper

## Support

For issues or questions:
1. Check the documentation
2. Review example scripts
3. Open an issue on GitHub

## License

This project is for academic and research purposes.
