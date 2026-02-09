# GNSS Train Positioning System - Colored Petri Net Simulation

Simulation of GNSS-based train positioning with Colored Petri Nets

Based on: "Modeling and performance analysis of GNSS-based train positioning system with colored petri nets" (High-speed Railway 3 (2025) 175–184)

## Features

This simulation reproduces the exact outputs from the paper including:
- **Table 4**: Positioning performances under different signal interferences (Normal, AM, FM, Pulse)
- **Table 5**: Positioning performances under different environment scenarios (Open Area, Mountain, Tunnel)
- **Figure 10**: Position errors in tunnel scenario

## Requirements

- Python 3.8 or higher
- NumPy
- Matplotlib

## Installation

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

Run the simulation:
```bash
python gnss_train_positioning_simulation.py
```

This will:
1. Print Table 4 with positioning performance under different signal interferences
2. Print Table 5 with positioning performance under different environment scenarios
3. Generate Figure 10 showing position errors in the tunnel scenario (saved as `figure_10_tunnel_errors.png`)

## Output Files

- `figure_10_tunnel_errors.png` - Visualization of position errors in tunnel scenario

## Implementation Details

The simulation implements:
- Extended Kalman Filter (EKF) for GNSS positioning
- 8-state vector: [x, y, z, vx, vy, vz, clock_bias, clock_drift]
- 4-satellite constellation
- Various signal interference models (AM, FM, Pulse)
- Environmental scenarios (Open Area, Mountain Occlusion, Tunnel)
