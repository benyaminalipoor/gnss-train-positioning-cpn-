# GNSS Train Positioning System using Colored Petri Nets

A comprehensive Java implementation of a GPS-based train positioning system using hierarchical Colored Petri Nets (CPN) with Extended Kalman Filter (EKF) for position estimation.

## Overview

This implementation models a GNSS positioning system for railway applications, simulating various environmental conditions and interference types that affect positioning accuracy. The system uses Colored Petri Nets to model the hierarchical architecture and Extended Kalman Filter for optimal state estimation.

## Features

### 1. Hierarchical CPN Structure
- **Top Level CPN**: Coordinates overall system workflow
- **GNSS Receiver CPN**: Satellite signal generation and processing
- **Position Solution CPN**: EKF-based position estimation
- **Evaluation CPN**: Error analysis and performance metrics

### 2. Environmental Modeling
- **Open Area**: Clear sky conditions (minimal interference)
- **Mountain**: Partial signal obstruction with multipath effects
- **Tunnel**: Severe signal degradation

### 3. Interference Types
- **Normal**: No interference baseline
- **AM**: Amplitude Modulation interference
- **FM**: Frequency Modulation interference (most severe)
- **Pulse**: Pulse interference

### 4. Extended Kalman Filter
- Full prediction and update steps
- State transition modeling (position and velocity)
- Process and measurement noise covariance matrices
- Complete matrix operations (multiplication, inversion, transpose)

### 5. Simulation Features
- 100-second simulations with 1-second time steps
- Train motion at 20 m/s along curved track
- 6 main scenarios combining environments and interferences
- Real-time error tracking and analysis

### 6. Visualization (Java Swing)
- Error time series plots for all scenarios
- Environment comparison bar charts
- Interference comparison bar charts
- Hierarchical CPN structure diagram
- All visualizations in a single 1200×900 window

## Requirements

- Java 8 or higher
- Java Swing (included in standard JDK)
- No external dependencies required

## Usage

### Compilation
```bash
javac GNSSTrainPositioningCPN.java
```

### Execution
```bash
java GNSSTrainPositioningCPN
```

### Output Files
The simulation generates two files:
1. **simulation_results.csv**: Complete trajectory data with timestamps, positions, and errors
2. **simulation_statistics.txt**: Statistical summaries and validation results

## Results

The implementation validates against expected research outcomes:

### Expected Trends (Confirmed)
- **Interference Severity**: FM > AM > Pulse > Normal
- **Environment Impact**: Tunnel > Mountain > Open Area
- **Best Case**: Open Area + Normal interference (~4m mean error)
- **Worst Case**: Tunnel + Normal interference (~20m mean error)
- **FM Impact**: ~14m mean error in open area

### Sample Statistics
```
Scenario                  Environment     Interference    Mean (m)     Max (m)      Std (m)
----------------------------------------------------------------------------------------
OPEN_AREA_NORMAL          OPEN_AREA       NORMAL          4.229        14.757       1.391
MOUNTAIN_NORMAL           MOUNTAIN        NORMAL          10.636       25.613       2.912
TUNNEL_NORMAL             TUNNEL          NORMAL          20.358       29.545       3.542
OPEN_AREA_AM              OPEN_AREA       AM              10.423       26.358       2.767
OPEN_AREA_FM              OPEN_AREA       FM              14.010       27.795       3.045
OPEN_AREA_PULSE           OPEN_AREA       PULSE           8.043        24.086       2.301
```

## Architecture

### CPN Components
- **Places**: Hold colored tokens representing system states
- **Transitions**: Represent actions/transformations
- **Arcs**: Define token flow between places and transitions

### Key Classes
- `Place`: CPN place implementation
- `Transition`: CPN transition implementation
- `GNSSSignal`: Satellite signal representation
- `TrainState`: Train position, velocity, and covariance
- `GNSSReceiverCPN`: Satellite signal generation and processing
- `PositionSolutionCPN`: EKF implementation
- `EvaluationCPN`: Error metrics calculation
- `Matrix`: Matrix operations for EKF
- `Simulator`: Main simulation orchestrator

## Technical Details

### EKF Implementation
The Extended Kalman Filter consists of two main steps:

**Prediction Step**:
- State transition: x = x + v*dt
- Covariance prediction: P = F*P*F^T + Q

**Update Step**:
- Kalman gain: K = P*H^T*(H*P*H^T + R)^(-1)
- State update: x = x + K*(z - h(x))
- Covariance update: P = (I - K*H)*P

Note: * denotes matrix multiplication, ^T denotes transpose, ^(-1) denotes inverse

### Satellite Configuration
- 4 satellites in view
- Pseudorange measurements with realistic noise
- Carrier phase measurements
- Environment-dependent signal quality

### Error Sources
1. Base measurement noise (2m σ)
2. Environmental factors (1.0× to 5.0× multiplier)
3. Multipath errors (up to 3m in tunnels)
4. Interference effects (0× to 2.5× multiplier)

## Educational Value

This implementation serves as:
- A complete example of Colored Petri Net modeling
- A reference implementation of Extended Kalman Filter
- A demonstration of GNSS error modeling
- A practical example of Java Swing visualization
- A production-quality simulation framework

## References

Based on Petri net modeling research for GNSS positioning in railway environments, focusing on:
- Hierarchical CPN modeling
- Extended Kalman Filter theory
- GNSS signal processing
- Railway positioning requirements

## License

This implementation is provided for educational and research purposes.

## Author

Created as a comprehensive implementation of GNSS Train Positioning using Colored Petri Nets.
