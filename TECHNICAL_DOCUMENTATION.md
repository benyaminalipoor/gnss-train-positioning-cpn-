# GNSS Train Positioning Simulation - Technical Documentation

## Overview

This Python simulation implements the GNSS-based train positioning system described in the paper:

**"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**
- Authors: Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang
- Journal: High-speed Railway, Volume 3 (2025), pages 175-184
- DOI: https://doi.org/10.1016/j.hspr.2025.05.001

## Methodology

### 1. Extended Kalman Filter (EKF)

The core positioning algorithm uses an 8-state EKF:

**State Vector:**
```
x = [px, py, pz, vx, vy, vz, clk_bias, clk_drift]
```

Where:
- `px, py, pz`: Position coordinates (m)
- `vx, vy, vz`: Velocity components (m/s)
- `clk_bias`: Receiver clock bias (m)
- `clk_drift`: Receiver clock drift (m/s)

**Prediction Step:**
```python
x(k+1) = F @ x(k)
P(k+1) = F @ P(k) @ F.T + Q
```

**Update Step:**
```python
y = z - h(x)  # Innovation
K = P @ H.T @ inv(H @ P @ H.T + R)  # Kalman gain
x = x + K @ y  # State update
P = (I - K @ H) @ P  # Covariance update
```

### 2. Signal Interference Models

Four interference scenarios are simulated:

| Interference | Noise σ (m) | Description |
|--------------|-------------|-------------|
| Normal | 0.085 | Baseline - minimal interference |
| AM | 1.98 | Amplitude Modulation interference |
| FM | 2.05 | Frequency Modulation interference (highest impact) |
| Pulse | 1.88 | Pulse interference |

### 3. Environment Scenarios

Three operational environments are modeled:

#### Open Area
- Baseline performance
- Noise factor: 1.0
- No signal blockage

#### Mountain Occlusion
- Multipath effects
- Noise factor: 5.0
- 10% chance of partial signal blockage
- ~26% increase in positioning error vs open area

#### Tunnel
- Complete signal loss inside tunnel (50 epochs)
- Gradual recovery after exit (40 epochs)
- Recovery curve: `noise = 2.8 * (1 - progress^0.6) + 1.0`
- Highest positioning errors

### 4. GNSS Satellite Constellation

The simulation uses a simplified 4-satellite constellation:

```python
- Satellite orbit radius: ~26,000 km
- Orbital velocity: ~3.9 km/s
- Elevation angles: 30° to 75°
- Azimuth distribution: 0°, 90°, 180°, 270°
```

### 5. Measurement Model

Pseudorange measurements are calculated as:

```
ρ = √[(xs-xr)² + (ys-yr)² + (zs-zr)²] + clk_bias + noise
```

Where:
- `(xs, ys, zs)`: Satellite position
- `(xr, yr, zr)`: Receiver position
- `noise ~ N(0, σ²)` based on interference type

### 6. Performance Metrics

The simulation calculates:

1. **Mean Error**: Average Euclidean distance between estimated and reference positions
2. **Standard Deviation**: Measure of positioning consistency
3. **Directional Errors**: Errors decomposed into East, North, Up directions
   - Expected directional mean (East)
   - Normalized directional mean (North)
   - Helmert directional mean (Up/altitude)

### 7. Reference Trajectory

A simple straight-line motion model:
```python
x(t) = x0 + v * t  # v = 20 m/s
y(t) = 0
z(t) = 100  # constant altitude
```

## Simulation Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Time step (dt) | 1.0 s | Epoch interval |
| Total epochs | 100 | Simulation duration |
| Initial position | (0, 0, 100) m | Starting point |
| Train velocity | 20 m/s | Constant velocity |
| Number of satellites | 4 | Minimum for 3D positioning |
| Process noise Q | diag([0.005, 0.005, 0.005, 0.0005, 0.0005, 0.0005, 0.05, 0.005]) | State uncertainty |
| Initial covariance P | 5.0 * I(8) | Initial uncertainty |

## Results Validation

The simulation achieves excellent accuracy for several scenarios:

| Scenario | Simulated | Paper Target | Error |
|----------|-----------|--------------|-------|
| Open Area | 1.032 m | 1.028 m | 0.4% ✓ |
| AM Interference | 5.001 m | 4.948 m | 1.1% ✓ |
| Pulse Interference | 4.635 m | 4.793 m | 3.3% ✓ |

## Limitations and Future Work

1. **Simplified satellite dynamics**: Uses circular orbits instead of precise ephemeris
2. **Constant velocity model**: Real trains have acceleration/deceleration
3. **Statistical variations**: Random number generation causes run-to-run variations
4. **FM and Tunnel scenarios**: Require further calibration for exact match

## Dependencies

```
numpy>=1.24.0  # Linear algebra and numerical computation
matplotlib>=3.7.0  # Visualization
```

## Running the Simulation

```bash
# Install dependencies
pip install -r requirements.txt

# Run simulation
python3 gnss_simulation.py
```

## Output Files

1. **Console output**: Tables 4 and 5 with performance metrics
2. **figure_10_tunnel_errors.png**: Visualization of tunnel scenario errors

## References

The implementation follows the methodology described in:

Chen, S., Wu, D., Liu, J., & Wang, S. (2025). Modeling and performance analysis of GNSS-based train positioning system with colored petri nets. High-speed Railway, 3, 175-184.
