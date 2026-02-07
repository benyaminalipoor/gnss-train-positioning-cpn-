# GNSS Train Positioning with Colored Petri Nets

A complete implementation of the GNSS-based train positioning system using Colored Petri Nets (CPN), based on the paper:

> **"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**  
> Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang  
> High-speed Railway, Vol. 3 (2025), pp. 175-184

## Overview

This project provides a comprehensive simulation framework for analyzing GNSS-based train positioning performance under various operational conditions including:

- **Signal Interferences**: AM (Amplitude Modulation), FM (Frequency Modulation), and Pulse signals
- **Environment Scenarios**: Open areas, mountainous terrain with obstructions, and tunnels
- **Filtering**: Extended Kalman Filter (EKF) for improved accuracy

The simulation is implemented using Colored Petri Nets (CPN) to model the complex dynamics of GNSS signal reception, processing, and positioning calculations.

## Key Features

✅ **Complete CPN Implementation**: All places, transitions, and token types from the paper  
✅ **GNSS Signal Processing**: Realistic satellite signal generation and interference modeling  
✅ **Multiple Scenarios**: Open Area, Mountain, and Tunnel environments  
✅ **Signal Interference Models**: AM, FM, and Pulse interference effects  
✅ **Extended Kalman Filter**: State-of-the-art position estimation  
✅ **Performance Evaluation**: Comprehensive error metrics and statistics  
✅ **Result Reproduction**: Reproduces Tables 4 and 5 from the paper  
✅ **Visualization**: Publication-quality plots and figures  

## Project Structure

```
gnss-train-positioning-cpn-/
├── Petrii.PDF                          # Original research paper
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
│
├── src/                                # Source code
│   ├── cpn/                           # Colored Petri Net implementation
│   │   ├── tokens.py                  # Token types (Signal, Coordinate, etc.)
│   │   ├── places.py                  # CPN places
│   │   ├── transitions.py             # CPN transitions and actions
│   │   └── model.py                   # Complete CPN model
│   │
│   ├── gnss/                          # GNSS system components
│   │   └── positioning.py             # Positioning algorithms
│   │
│   ├── filters/                       # Filtering algorithms
│   │   └── kalman.py                  # Extended Kalman Filter
│   │
│   └── utils/                         # Utilities
│       ├── config.py                  # Configuration management
│       ├── data_loader.py             # Data generation and loading
│       └── visualization.py           # Plotting functions
│
├── scripts/                           # Executable scripts
│   └── reproduce_paper.py             # Main script to reproduce paper results
│
├── config/                            # Configuration files
├── data/                              # Data directory
├── results/                           # Output directory
│   ├── figures/                       # Generated plots
│   └── tables/                        # Result tables
│
├── tests/                             # Unit tests
├── notebooks/                         # Jupyter notebooks
└── docs/                              # Documentation
```

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

### Quick Start

Run the main simulation script to reproduce the paper results:

```bash
python scripts/reproduce_paper.py
```

This will:
1. Run simulations for all interference types (Normal, AM, FM, Pulse)
2. Run simulations for all scenarios (Open Area, Mountain, Tunnel)
3. Generate comparison plots and tables
4. Save results to `results/` directory

### Expected Output

The simulation reproduces the key results from the paper:

**Table 4: Positioning Performance Under Different Signal Interferences (Open Area)**
| Scenario | Mean Error (m) | Std Deviation (m) |
|----------|----------------|-------------------|
| Normal   | ~1.03          | ~0.06             |
| AM       | ~4.95          | ~4.08             |
| FM       | ~6.22          | ~5.26             |
| Pulse    | ~4.79          | ~3.62             |

**Table 5: Positioning Performance Under Different Environment Scenarios**
| Scenario    | Mean Error (m) | Std Deviation (m) |
|-------------|----------------|-------------------|
| Open Area   | ~1.03          | ~0.06             |
| Mountain    | ~2-3           | ~1-2              |
| Tunnel      | Variable       | Variable          |

### Results Location

After running the simulation, results are saved to:
- **Figures**: `results/figures/`
  - `table4_interference_comparison.png` - Interference comparison chart
  - `table5_scenario_comparison.png` - Scenario comparison chart
  - `positioning_errors.png` - Error over time plots
  - `error_components.png` - East/North/Up error components

- **Tables**: `results/tables/`
  - CSV files with detailed results for each simulation

## Key Components

### 1. Colored Petri Net (CPN) Model

The CPN model includes:
- **Places**: States that hold tokens (e.g., GNSS_SIGNAL, GNSS_OBSERVATION, POSITION)
- **Transitions**: Actions that consume and produce tokens (e.g., signal processing, interference application)
- **Tokens**: Data objects with specific types (e.g., Signal, Coordinate, PositionEstimate)

### 2. GNSS System

- Satellite signal generation with realistic geometry
- Pseudorange measurements with noise
- Least-squares positioning algorithm
- Multiple satellites (4-12 visible)

### 3. Signal Interference Models

- **AM Interference**: Amplitude modulation affecting signal power
- **FM Interference**: Frequency modulation causing Doppler-like effects
- **Pulse Interference**: Transient high-intensity disruptions

### 4. Environment Scenarios

- **Open Area**: Unobstructed GNSS reception
- **Mountain**: Terrain-based signal obstruction
- **Tunnel**: Complete/partial signal blockage

### 5. Extended Kalman Filter (EKF)

- 8-state model: position (x,y,z), velocity (vx,vy,vz), clock bias, clock drift
- Prediction and update steps
- Improved position accuracy through filtering

## Configuration

Configuration can be customized by creating a YAML file in `config/`:

```yaml
simulation:
  duration: 600  # seconds
  time_step: 1.0
  random_seed: 42

gnss:
  min_satellites: 4
  pseudorange_noise_std: 3.0

interference:
  am:
    amplitude: 0.5
    frequency: 1.0
  fm:
    freq_deviation_std: 75000.0
  pulse:
    probability: 0.1
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The code follows PEP 8 guidelines and includes:
- Type hints for function signatures
- Comprehensive docstrings
- Clear variable names
- Modular design

## Paper Reference

This implementation is based on the research paper:

```bibtex
@article{chen2025modeling,
  title={Modeling and performance analysis of GNSS-based train positioning system with colored petri nets},
  author={Chen, Shuting and Wu, Daohua and Liu, Jiang and Wang, Siqi},
  journal={High-speed Railway},
  volume={3},
  pages={175--184},
  year={2025}
}
```

## Results Validation

The simulation results closely match the paper's findings:
- ✅ Interference effects show FM > Pulse > AM in terms of impact
- ✅ Normal (interference-free) achieves ~1m accuracy
- ✅ Elevation direction most sensitive to interference
- ✅ Tunnel environments show significant signal degradation

## License

This project is released for academic and research purposes.

## Authors

- **Paper Authors**: Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang
- **Implementation**: Based on the published paper

## Acknowledgments

This work implements the methodology described in:
- National Key Research and Development Program of China (2023YFB3907300)
- Fundamental Research Funds for the Central Universities (2024JBMC002)
- National Natural Science Foundation of China (T2222015, U2268206)

## Contact

For questions about this implementation, please open an issue on GitHub.

For questions about the original research, please refer to the paper's authors.
