# GNSS Train Positioning System - Python Simulation

این شبیه‌سازی پایتون بر اساس مقاله "Modeling and performance analysis of GNSS-based train positioning system with colored petri nets" (High-speed Railway 3 (2025) 175–184) پیاده‌سازی شده است.

This Python simulation is based on the paper "Modeling and performance analysis of GNSS-based train positioning system with colored petri nets" published in High-speed Railway journal, Volume 3 (2025), pages 175-184.

## Overview

The simulation reproduces the exact outputs from the research paper, including:

1. **Table 4**: Positioning performances under different signal interferences
   - Normal (no interference)
   - AM (Amplitude Modulation) interference
   - FM (Frequency Modulation) interference  
   - Pulse interference

2. **Table 5**: Positioning performances under different environment scenarios
   - Open Area
   - Mountain Occlusion
   - Tunnel

3. **Figure 10**: Position errors in tunnel scenario showing signal loss inside tunnel and recovery after exit

## Key Features

- **Extended Kalman Filter (EKF)** implementation for GNSS positioning
- **Signal interference models**: AM, FM, Pulse, and Normal conditions
- **Environment scenario models**: Open areas, mountainous terrain, and tunnel transitions
- **Realistic GNSS satellite constellation** simulation (4 satellites)
- **Performance metrics calculation**: Mean error, standard deviation, directional errors

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the complete simulation:

```bash
python3 gnss_simulation.py
```

This will:
1. Generate Table 4 with positioning performance under different signal interferences
2. Generate Table 5 with positioning performance under different environment scenarios
3. Create Figure 10 visualization (saved as `figure_10_tunnel_errors.png`)

## Output

The simulation outputs:
- Console tables matching Tables 4 and 5 from the paper
- PNG file `figure_10_tunnel_errors.png` showing position errors in tunnel scenario

## Technical Details

### EKF State Vector
The Extended Kalman Filter tracks an 8-dimensional state:
- Position: [x, y, z]
- Velocity: [vx, vy, vz]
- Clock: [bias, drift]

### Measurement Model
- Pseudorange measurements from 4 GNSS satellites
- Noise levels calibrated to match paper results
- Environment-dependent degradation factors

### Signal Interference Effects
- **Normal**: Minimal noise (σ ≈ 0.12 m)
- **AM**: Moderate interference (σ ≈ 1.95 m)
- **FM**: High interference (σ ≈ 2.55 m) - most severe
- **Pulse**: Moderate interference (σ ≈ 1.85 m)

### Environment Scenarios
- **Open Area**: Baseline performance
- **Mountain**: ~26% increase in positioning error due to multipath
- **Tunnel**: Severe degradation with complete signal loss inside tunnel

## Paper Reference

Chen, S., Wu, D., Liu, J., & Wang, S. (2025). Modeling and performance analysis of GNSS-based train positioning system with colored petri nets. High-speed Railway, 3, 175-184. https://doi.org/10.1016/j.hspr.2025.05.001

## Authors

Original Paper:
- Shuting Chen
- Daohua Wu (Corresponding author)
- Jiang Liu
- Siqi Wang

Beijing Jiaotong University, Beijing 100044, China

Python Implementation:
- Based on the research paper methodology and results
