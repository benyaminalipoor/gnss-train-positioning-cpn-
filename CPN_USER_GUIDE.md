# GNSS Train Positioning CPN - User Guide

## Overview

This Colored Petri Net (CPN) model simulates GNSS-based train positioning with Extended Kalman Filter (EKF) for position estimation. The model implements all scenarios from the research paper with different environmental conditions and interference types.

## File Information

**Filename**: `GNSS_Train_Positioning.cpn`

**Compatible with**: CPN Tools 4.0.1 or later

**Format**: CPN Tools XML format version 6

## Model Structure

### Hierarchical Pages

The CPN model consists of 4 hierarchical pages:

#### 1. Top Level Page
The main page that orchestrates the complete simulation workflow:
- **Places**: 
  - `Scenario`: Holds scenario configuration (environment + interference type)
  - `GNSS_Signals`: Contains generated GNSS signals
  - `Filter_State`: Maintains EKF state (position, velocity, covariances)
  - `Position_Estimate`: Current estimated position
  - `Errors`: Accumulated position errors
  - `Time`: Simulation time counter
  
- **Transitions**:
  - `Generate_Signals`: Generates GNSS signals based on scenario and time
  - `EKF_Positioning`: Runs EKF prediction and update
  - `Evaluate_Error`: Calculates positioning error against reference

#### 2. GNSS Receiver Page
Models the GNSS signal reception with environmental and interference effects:
- Splits scenario into environment type and interference type
- Applies environment-specific signal degradation
- Applies interference-specific noise

#### 3. Position Solution Page
Detailed EKF implementation:
- Converts signals to measurements
- Prediction step (state transition)
- Update step (measurement incorporation)
- Outputs updated state and position estimate

#### 4. Evaluation Page
Error analysis and metrics:
- Generates reference trajectory
- Calculates position errors
- Accumulates error history
- Computes RMSE (Root Mean Square Error)

## Scenarios

The model supports **12 different scenarios** combining 3 environment types with 4 interference types:

### Environment Types

1. **OpenArea**: Clear sky conditions
   - 12 visible satellites
   - Low noise (0.5m)
   - Best positioning accuracy

2. **Mountain**: Mountainous terrain
   - 8 visible satellites
   - Medium noise (1.5m)
   - Signal blockage and multipath

3. **Tunnel**: Tunnel/urban canyon
   - 4 visible satellites
   - High noise (3.0m)
   - Severe signal degradation

### Interference Types

1. **Normal**: No interference
   - Baseline conditions
   - No additional noise

2. **AM**: Amplitude Modulation interference
   - Additional noise: 0.8m
   - Medium degradation

3. **FM**: Frequency Modulation interference
   - Additional noise: 1.5m
   - Highest degradation

4. **Pulse**: Pulse interference
   - Additional noise: 1.2m
   - Significant degradation

### Scenario IDs

Use `generateTestScenario(id)` function with these IDs:
- 1: OpenArea + Normal
- 2: OpenArea + AM
- 3: OpenArea + FM
- 4: OpenArea + Pulse
- 5: Mountain + Normal
- 6: Mountain + AM
- 7: Mountain + FM
- 8: Mountain + Pulse
- 9: Tunnel + Normal
- 10: Tunnel + AM
- 11: Tunnel + FM
- 12: Tunnel + Pulse

## How to Use

### Opening the Model

1. Launch CPN Tools 4.0.1 or later
2. Open `GNSS_Train_Positioning.cpn`
3. The model will load with all pages and declarations

### Changing Scenario

To test a different scenario:

1. Locate the `Scenario` place on the Top Level page
2. Change the initial marking from:
   ```sml
   generateTestScenario(1)
   ```
   to any other scenario ID (1-12):
   ```sml
   generateTestScenario(9)  (* For Tunnel + Normal *)
   ```

### Running Simulation

1. Select **Simulation** > **Create simulator** from menu
2. Click on transitions to fire them manually, or
3. Use **Tools** > **Step** for automatic stepping
4. Use **Tools** > **Fast forward** for fast simulation

The simulation will automatically stop after 100 time steps (configured in the monitor).

### Monitoring Results

During simulation, you can inspect:
- **Filter_State** place: Current EKF state and covariances
- **Position_Estimate** place: Latest position estimate
- **Errors** place: Accumulated position errors
- **Time** place: Current simulation time

### Analyzing Results

After simulation:
1. Check the `Errors` place for complete error history
2. Calculate RMSE using the `calculateRMSE()` function
3. Compare results across different scenarios

## Key Functions

### Signal Generation

```sml
generateSignals(scenarioType, interfType, t) : SignalList
```
Generates GNSS signals with appropriate noise and number of satellites based on scenario.

### EKF Functions

```sml
ekfPredict(state, cov, dt) : FilterState
```
Performs EKF prediction step with state transition model.

```sml
ekfUpdate(filterState, measurements, t) : FilterState
```
Performs EKF update step with measurement incorporation.

### Error Calculation

```sml
calculateError(estimated, reference) : ErrorMetric
```
Computes position error between estimated and reference position.

```sml
calculateRMSE(errors) : real
```
Calculates Root Mean Square Error from error list.

### Reference Trajectory

```sml
generateReferenceTrajectory(t) : Position
```
Generates ground truth position at time t (linear motion at 20 m/s).

## Expected Results

Based on the research paper, expected RMSE trends:

**By Interference Type** (in Open Area):
- Normal: ~1.05m (best)
- AM: ~2.10m
- Pulse: ~2.45m
- FM: ~3.94m (worst)

**By Environment** (with Normal interference):
- OpenArea: ~1.06m (best)
- Mountain: ~2.15m
- Tunnel: ~6.60m (worst)

## Simulation Parameters

- **Initial Position**: (0, 0, 100) meters
- **Initial Velocity**: (20, 0, 0) m/s
- **Time Step**: 1 second
- **Simulation Duration**: 100 seconds
- **GPS L1 Frequency**: 1575.42 MHz
- **Satellite Orbital Radius**: 26,560 km

## Color Sets Defined

- `Position`: Real triplet (x, y, z) with time
- `Velocity`: Real triplet (vx, vy, vz)
- `StateVector`: 8-element real vector (position, velocity, clock bias, clock drift)
- `FilterState`: State vector + covariance matrix
- `GNSSSignal`: Satellite ID + range + delta-range + time + quality
- `SignalList`: List of GNSS signals
- `Scenario`: Environment type + interference type
- `Measurement`: Satellite ID + range + delta-range
- `ErrorMetric`: Position error (x, y, z)
- `ErrorList`: List of errors

## Troubleshooting

### Model doesn't load
- Ensure you're using CPN Tools 4.0.1 or later
- Check that the .cpn file is not corrupted
- Verify XML structure is valid

### Simulation doesn't progress
- Check that all required places have tokens
- Verify transition guards are satisfied
- Check for deadlocks in the model

### Incorrect results
- Verify scenario configuration is correct
- Check initial markings are properly set
- Ensure monitor settings match simulation duration

## Technical Details

### State Vector Components
1. x: Position East (m)
2. y: Position North (m)
3. z: Position Up (m)
4. vx: Velocity East (m/s)
5. vy: Velocity North (m/s)
6. vz: Velocity Up (m/s)
7. cb: Clock bias (m)
8. cd: Clock drift (m/s)

### Covariance Matrix
8×8 matrix flattened to 64-element list, initialized with:
- Diagonal elements: 100.0 (position/velocity uncertainty)
- Off-diagonal elements: 0.0

### Process Noise
Diagonal matrix with 0.1 on diagonal elements.

### Measurement Noise
Diagonal matrix with 4.0 on diagonal elements (2m standard deviation).

## References

For theoretical background, refer to the accompanying research paper (Petrii.PDF) which describes:
- GNSS positioning principles
- Extended Kalman Filter algorithm
- Environmental effects on GNSS
- Interference characterization
- Performance analysis

## Support

For issues or questions:
1. Check this user guide
2. Review the ML code in global declarations
3. Inspect the page structure
4. Verify scenario configuration

## Version History

- **Version 1.0** (2026-02-13): Initial complete implementation
  - 4 hierarchical pages
  - 12 scenarios supported
  - Full EKF algorithm
  - Comprehensive error analysis

---

**Note**: This CPN model is designed for educational and research purposes to demonstrate GNSS train positioning with different environmental conditions and interference types as described in the accompanying research paper.
