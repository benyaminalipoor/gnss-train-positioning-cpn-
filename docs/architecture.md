# Architecture Documentation

## System Architecture Overview

The GNSS Train Positioning CPN simulation system follows a modular, hierarchical architecture based on Colored Petri Nets (CPN) as described in the research paper.

## Hierarchical Structure

```
┌─────────────────────────────────────────────────────────┐
│              CPN Model (Main Controller)                 │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Module: GNSS Signal Generator                   │   │
│  │  - Generate satellite ephemeris data             │   │
│  │  - Simulate visible satellites                   │   │
│  └──────────────────────────────────────────────────┘   │
│                        │                                 │
│                        ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Module: GNSS Receiver                           │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │ Submodule: Open Area                       │  │   │
│  │  │ - AM Interference                          │  │   │
│  │  │ - FM Interference                          │  │   │
│  │  │ - Pulse Interference                       │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │ Submodule: Mountain                        │  │   │
│  │  │ - Terrain obstruction filtering            │  │   │
│  │  │ - Elevation angle calculation              │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │ Submodule: Tunnel                          │  │   │
│  │  │ - Signal blockage simulation               │  │   │
│  │  │ - Partial signal recovery                  │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                        │                                 │
│                        ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Module: Positioning                             │   │
│  │  - Least squares positioning                     │   │
│  │  - Pseudorange processing                        │   │
│  │  - DOP calculation                               │   │
│  └──────────────────────────────────────────────────┘   │
│                        │                                 │
│                        ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Module: EKF Filter                              │   │
│  │  - State prediction                              │   │
│  │  - Measurement update                            │   │
│  │  - Covariance propagation                        │   │
│  └──────────────────────────────────────────────────┘   │
│                        │                                 │
│                        ▼                                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Module: Evaluation                              │   │
│  │  - Error calculation                             │   │
│  │  - Performance metrics                           │   │
│  │  - Results storage                               │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. CPN Model (`src/cpn/model.py`)

The main controller that orchestrates the entire simulation:
- Manages the flow of tokens through places
- Coordinates transition firing
- Collects and aggregates results

**Key Methods:**
- `initialize()`: Set up initial marking
- `step()`: Execute one simulation epoch
- `run_simulation()`: Complete simulation run
- `get_statistics()`: Calculate performance metrics

### 2. Token Types (`src/cpn/tokens.py`)

Defines all data structures (color sets) in the CPN:

- **Signal**: Satellite signal data (pseudorange, position, velocity)
- **Coordinate**: 3D position (x, y, z)
- **Scenario**: Environment type (OPEN_AREA, MOUNTAIN, TUNNEL)
- **StateInterference**: Interference type (NORMAL, AM, FM, PULSE)
- **PositionEstimate**: Estimated position with metadata
- **ErrorMetric**: Positioning error measurements

### 3. Places (`src/cpn/places.py`)

Defines all places (states) in the CPN model:

**Main Places:**
- `GNSS_SIGNAL`: Raw satellite signals
- `GNSS_OBSERVATION`: Processed observations
- `RAW_POSITION`: Unfiltered position estimates
- `FILTERED_POSITION`: EKF-filtered positions
- `REFERENCE_POSITION`: True positions
- `DELTA_POSITION`: Error measurements

### 4. Transitions (`src/cpn/transitions.py`)

Implements transitions (actions) that process tokens:

**Key Transitions:**
- Signal interference application (AM, FM, Pulse)
- Mountain obstruction filtering
- Tunnel effect simulation
- Scenario selection

### 5. GNSS Positioning (`src/gnss/positioning.py`)

Implements GNSS positioning algorithms:

**Algorithms:**
- Least Squares Method: Iterative position calculation
- Pseudorange processing
- DOP (Dilution of Precision) calculation
- Error metric computation

**Key Function:**
```python
def least_squares_positioning(signals, initial_position=None):
    """
    Calculate position using iterative least squares.
    Returns: (position, clock_bias, dop_values)
    """
```

### 6. Extended Kalman Filter (`src/filters/kalman.py`)

Implements EKF for improved position estimation:

**State Vector (8D):**
- Position: [x, y, z]
- Velocity: [vx, vy, vz]
- Clock: [bias, drift]

**Methods:**
- `predict(dt)`: Predict state forward in time
- `update_with_position()`: Update with position measurement
- `update_with_pseudoranges()`: Update with pseudorange measurements

### 7. Data Generation (`src/utils/data_loader.py`)

Generates synthetic data for simulation:

**Functions:**
- `generate_satellite_signals()`: Create GNSS signals
- `generate_reference_trajectory()`: Create true train path
- `generate_scenario_sequence()`: Create scenario timeline

### 8. Visualization (`src/utils/visualization.py`)

Creates plots and tables:

**Functions:**
- `plot_positioning_errors()`: Error over time
- `plot_error_components()`: East/North/Up errors
- `plot_interference_comparison()`: Compare interference types
- `create_results_table()`: Generate summary tables

## Data Flow

1. **Input Generation**: Satellite signals and reference trajectory
2. **Signal Reception**: Process signals through scenario-specific submodules
3. **Positioning**: Calculate position using least squares
4. **Filtering**: Apply EKF for smoothing
5. **Evaluation**: Compare with reference and calculate errors
6. **Visualization**: Generate plots and tables

## Configuration

All parameters are configured via YAML files in `config/`:

```yaml
gnss:
  min_satellites: 4
  pseudorange_noise_std: 3.0  # meters

interference:
  am:
    amplitude: 0.5
    frequency: 1.0  # Hz
  
ekf:
  process_noise:
    position: 0.5  # m
    velocity: 0.1  # m/s
```

## Performance Metrics

The system calculates:

1. **Mean Error**: Average positioning error (meters)
2. **Standard Deviation**: Error variability
3. **RMSE**: Root Mean Square Error
4. **Directional Errors**: East, North, Up components
5. **DOP Values**: Geometric dilution of precision

## Extensibility

The modular architecture allows easy extension:

- Add new interference types in `transitions.py`
- Add new scenarios by creating submodules
- Add new filters in `src/filters/`
- Add new positioning algorithms in `src/gnss/`

## References

For detailed algorithmic descriptions, refer to:
- `Petrii.PDF`: Original research paper
- Code docstrings: Inline documentation
- `README.md`: User guide
