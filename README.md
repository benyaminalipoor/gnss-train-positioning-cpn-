# GNSS Train Positioning System with Colored Petri Nets

Complete implementation of the simulation described in the research paper:
**"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**
by Chen et al., published in High-speed Railway (2025).

## Overview

This project implements a comprehensive simulation framework for analyzing GNSS-based train positioning systems using Colored Petri Nets (CPNs). The simulation models:

- **Signal Interferences**: AM (Amplitude Modulation), FM (Frequency Modulation), and Pulse interference
- **Environment Scenarios**: Open areas, mountainous terrain, and tunnel conditions
- **Positioning Algorithm**: Extended Kalman Filter (EKF) for position estimation
- **Performance Evaluation**: Statistical analysis matching the paper's results

## Project Structure

```
├── Petrii.PDF                      # Research paper (reference)
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── src/
│   ├── gnss_processing.py         # GNSS signal processing and interference models
│   ├── train_positioning.py       # EKF-based positioning algorithm
│   ├── cpn_model.py               # Colored Petri Net model implementation
│   ├── simulation.py              # Main simulation script
│   └── visualize_results.py       # Results visualization and plotting
├── data/
│   └── (GNSS observation data - generated during simulation)
├── results/
│   ├── outputs/                   # Numerical results (JSON)
│   └── plots/                     # Generated plots and figures
└── notebooks/
    └── (Jupyter notebooks for analysis)
```

## Features

### 1. Signal Interference Modeling

- **AM Interference**: 1 Hz modulation frequency, 1575.42 MHz carrier, 0.5 modulation depth
- **FM Interference**: Gaussian frequency deviation (σ = 75 kHz)
- **Pulse Interference**: Periodic bursts with random width and intervals

### 2. Environment Scenarios

- **Open Area**: Signal interferences only
- **Mountain Occlusion**: Satellite filtering based on elevation angle and obstruction
- **Tunnel**: Three-phase model (inside, just exited, outside)

### 3. Positioning System

- **Extended Kalman Filter (EKF)**: 8-state model (position, velocity, clock bias/drift)
- **GNSS Processing**: Pseudorange measurements, satellite geometry calculations
- **Error Evaluation**: Euclidean distance metrics

### 4. Results Generation

Reproduces all key results from the paper:
- **Table 4**: Positioning performance under different signal interferences
- **Table 5**: Positioning performance under different environment scenarios
- **Figure 10**: Position error evolution in tunnel scenario

## Installation

### Requirements

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/benyaminalipoor/gnss-train-positioning-cpn-.git
cd gnss-train-positioning-cpn-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Complete Simulation

Execute the main simulation script:

```bash
python src/simulation.py
```

This will:
1. Generate synthetic GNSS observation data (600 epochs = 10 minutes)
2. Run simulations for all interference scenarios (Normal, AM, FM, Pulse)
3. Run simulations for all environment scenarios (Open Area, Mountain, Tunnel)
4. Calculate positioning statistics
5. Save results to `results/outputs/simulation_results.json`

### Generating Visualizations

After running the simulation, generate plots:

```bash
python src/visualize_results.py
```

This creates:
- Interference comparison plots
- Environment scenario plots
- Tunnel scenario detail (Figure 10)
- Statistical comparison charts
- Summary tables matching the paper

All plots are saved to `results/plots/`

### Running Individual Components

You can also use the modules programmatically:

```python
from src.gnss_processing import generate_synthetic_gnss_data, InterferenceType
from src.cpn_model import GNSSTrainPositioningCPN
from src.train_positioning import Position

# Generate data
reference_trajectory = [Position(x=-2148744.0, y=4426641.0, z=4044655.0) for _ in range(600)]
gnss_data = generate_synthetic_gnss_data(num_epochs=600, num_satellites=8)

# Create and configure CPN model
cpn = GNSSTrainPositioningCPN(reference_trajectory=reference_trajectory)
cpn.set_interference(InterferenceType.AM)

# Run simulation
results = cpn.run_simulation(gnss_data)
print(f"Mean error: {results['statistics']['mean_error']:.4f} m")
```

## Simulation Parameters

Based on the paper specifications:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Simulation Duration | 600 seconds | 10 minutes of operation |
| Epoch Interval | 1.0 second | Observation frequency |
| Number of Satellites | 8 | Typical GPS constellation visibility |
| L1 Carrier Frequency | 1575.42 MHz | GNSS L1 band |
| AM Modulation Freq | 1 Hz | Low-frequency envelope |
| AM Modulation Depth | 0.5 | Amplitude variation |
| FM Deviation | 75 kHz (σ) | Gaussian distribution |
| Tunnel Entry | 200 seconds | Simulation time |
| Tunnel Exit | 300 seconds | Simulation time |
| EKF State Dimension | 8 | Position, velocity, clock |

## Results

### Expected Performance (from paper)

**Signal Interference Scenarios (Table 4):**

| Scenario | Mean Error | Std Deviation |
|----------|------------|---------------|
| Normal | ~1.03 m | ~0.06 m |
| AM | ~4.95 m | ~4.08 m |
| FM | ~6.22 m | ~5.26 m |
| Pulse | ~4.79 m | ~3.62 m |

**Environment Scenarios (Table 5):**

| Scenario | Mean Error | Std Deviation |
|----------|------------|---------------|
| Open Area | ~1.03 m | ~0.06 m |
| Mountain | ~1.30 m | ~0.45 m |
| Tunnel | ~5.67 m | ~6.69 m |

### Key Findings

1. **FM interference** causes the most severe degradation
2. **Tunnel scenarios** show dramatic performance variation across three phases
3. **Mountain occlusion** moderately affects accuracy through satellite filtering
4. **Elevation direction** is most sensitive to interference

## Technical Implementation

### CPN Model Architecture

The implementation follows the hierarchical CPN structure from the paper:

```
Top-Level Model
├── GNSS Receiver Module
│   ├── Open Area Submodule (AM, FM, Pulse interference)
│   ├── Mountain Submodule (obstruction filtering)
│   └── Tunnel Submodule (three-phase simulation)
├── Position Solution Module (EKF)
└── Evaluation Module (error calculation)
```

### State Space

The model has been verified to be:
- **Bounded**: Finite state space
- **Sound**: No deadlocks in normal operation
- **Deterministic**: Reproducible results with fixed seeds

State space characteristics (from paper):
- Nodes: 5365 markings
- Arcs: 6410 transitions
- Dead markings: 648 (terminal states)

## Development

### Code Structure

- **gnss_processing.py**: Core GNSS signal models and data structures
- **train_positioning.py**: EKF implementation and position calculation
- **cpn_model.py**: CPN places, transitions, and modules
- **simulation.py**: Main simulation loop and scenario management
- **visualize_results.py**: Matplotlib-based plotting and visualization

### Testing

Run a quick test simulation:

```python
python -c "
from src.simulation import main
import sys
sys.exit(0 if main() else 1)
"
```

### Extending the Simulation

To add new scenarios or modifications:

1. **New Interference Type**: Extend `InterferenceModel` in `gnss_processing.py`
2. **New Environment**: Add submodule to `GNSSReceiverModule` in `cpn_model.py`
3. **Different EKF**: Modify `ExtendedKalmanFilter` in `train_positioning.py`
4. **Custom Plots**: Add functions to `visualize_results.py`

## References

### Primary Paper

Chen, S., Wu, D., Liu, J., & Wang, S. (2025). Modeling and performance analysis of GNSS-based train positioning system with colored petri nets. *High-speed Railway*, 3, 175-184.

### Key Concepts

- **Colored Petri Nets**: Jensen & Kristensen (2009)
- **GNSS Positioning**: Mikhaylov et al. (2023)
- **Extended Kalman Filter**: Zhang (2016)
- **Railway Applications**: Wu et al. (2021)

## Citation

If you use this implementation in your research, please cite both the original paper and this repository:

```bibtex
@article{chen2025modeling,
  title={Modeling and performance analysis of GNSS-based train positioning system with colored petri nets},
  author={Chen, Shuting and Wu, Daohua and Liu, Jiang and Wang, Siqi},
  journal={High-speed Railway},
  volume={3},
  pages={175--184},
  year={2025},
  publisher={Elsevier}
}
```

## License

This implementation is provided for academic and research purposes. The original paper is published under CC BY-NC-ND license.

## Contributors

- Implementation based on the paper by Chen et al.
- Code structure follows software engineering best practices
- Comprehensive documentation and comments throughout

## Support

For questions or issues:
1. Check the paper (Petrii.PDF) for theoretical details
2. Review code comments for implementation specifics
3. Open an issue on GitHub for bugs or enhancement requests

## Acknowledgments

This work is based on research supported by:
- National Key Research and Development Program of China (2023YFB3907300)
- Fundamental Research Funds for the Central Universities (2024JBMC002)
- National Natural Science Foundation of China (T2222015, U2268206)

---

**Status**: ✅ Complete implementation with all paper results reproducible
