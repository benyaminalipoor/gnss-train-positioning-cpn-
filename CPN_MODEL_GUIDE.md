# GNSS Train Positioning CPN Model - User Guide

## Overview
This Colored Petri Net (CPN) model implements a GNSS-based train positioning system with Extended Kalman Filter (EKF) as described in the Petrii.PDF paper.

## Files
- **GNSS_Train_Positioning.cpn** - Main CPN Tools model file
- **GNSS_Sample_Data.sml** - Sample data and test scenarios
- **Petrii.PDF** - Reference paper

## Model Structure

### Hierarchical Pages

#### 1. Top Level Page
The main page showing the overall flow:
- **Places:**
  - `Scenario`: Input scenarios (Urban, Tunnel, Mountain, Combined)
  - `GNSS_Signals`: Raw GNSS signal data
  - `FilterState`: Current EKF state
  - `RawPosition`: Position calculated from signals
  - `EstimatedPosition`: EKF-filtered position
  - `Results`: Evaluation metrics

- **Transitions:**
  - `ProcessSignals`: Calculates position from GNSS signals
  - `ApplyEKF`: Applies Extended Kalman Filter
  - `Evaluate`: Calculates performance metrics

#### 2. GNSS Receiver Page
Signal processing module:
- Applies interference models (AM/FM/Pulse)
- Processes raw signals
- Outputs filtered signals

#### 3. Position Solution Page
EKF implementation:
- Prediction step
- Update step
- State estimation
- Position output

#### 4. Evaluation Page
Performance analysis:
- Calculates error metrics
- Computes success rates
- Generates evaluation results

## Color Sets (19 total)

### Basic Types
- `INT`, `REAL`, `BOOL`, `STRING`, `TIME`

### Domain-Specific Types
- `SIGNAL`: Individual GNSS signal with id, frequency, amplitude, phase, SNR
- `SIGNALLIST`: List of signals
- `COORDINATE`: 3D position with timestamp
- `COORDINATELIST`: List of coordinates
- `STATEINFE`: EKF state (position, velocity, acceleration, covariance)
- `SCENARIO`: Test scenario configuration
- `MEASUREMENT`: Signal measurement data
- `MEASUREMENTLIST`: List of measurements
- `ERROR`: Error model
- `ERRORLIST`: List of errors
- `POSITION`: Position with actual/estimated/error
- `POSITIONLIST`: List of positions
- `EVALUATION`: Performance metrics
- `EVALUATIONLIST`: List of evaluations
- `FILTERSTATE`: Kalman filter state
- `CONTROL`: Control signals (Start/Stop/Reset/Process)
- `STATUS`: Processing status

## Variables (29 total)
All typed variables for places and transitions including:
- Signal variables: `sig`, `sigList`, `snr`, `freq`, `amp`, `phase`
- Position variables: `coord`, `coordList`, `x`, `y`, `z`
- State variables: `state`, `filterState`, `v`, `a`
- Scenario variables: `scenario`, `intLevel`, `tunnelLen`, `mountHeight`
- And more...

## ML Functions

### Interference Models
1. **AM Interference**: Amplitude modulation interference
2. **FM Interference**: Frequency modulation interference  
3. **Pulse Interference**: Pulsed interference
4. **Combined Interference**: All three types applied

### Environmental Effects
1. **Mountain Filtering**: Simulates signal shadowing from mountains
2. **Tunnel Error**: Models signal loss in tunnels

### EKF Algorithm
1. **ekfPredict**: Prediction step using motion model
2. **ekfUpdate**: Update step using measurements
3. **ekfCycle**: Complete EKF iteration

### Position Calculation
- **calculatePosition**: Computes position from signal list and scenario
- **calculateError**: Computes 3D Euclidean distance error

### Evaluation
- **evaluatePerformance**: Calculates mean, max, RMS error and success rate

## Initial Marking
The model starts with:
- 1 test scenario (Urban scenario with ID=1)
- 4 GNSS signals (L1 frequency, varying SNR)
- Initial EKF state (position at origin, velocity 20 m/s)

## How to Use

### 1. Open in CPN Tools
```
File → Open → Select GNSS_Train_Positioning.cpn
```

### 2. Initialize Simulation
```
Tools → Simulator → Init
```
This loads the initial marking into all places.

### 3. Run Simulation
```
Tools → Simulator → Step (or press F7)
```
Execute transitions one at a time to observe the system behavior.

### 4. Multiple Steps
```
Tools → Simulator → Fast Forward
```
Run multiple steps automatically.

### 5. Monitor Results
Watch the `Results` place to see evaluation metrics appear after simulation.

## Expected Results

According to the paper (Petrii.PDF), expected performance:

### Urban Scenario
- Mean Error: < 3 meters
- Max Error: < 5 meters
- RMS Error: < 3.5 meters
- Success Rate: > 90%

### Tunnel Scenario
- Mean Error: < 10 meters
- Max Error: < 15 meters
- RMS Error: < 11 meters
- Success Rate: > 70%

### Mountain Scenario
- Mean Error: < 8 meters
- Max Error: < 12 meters
- RMS Error: < 8 meters
- Success Rate: > 80%

### Combined Scenario
- Mean Error: < 12 meters
- Max Error: < 20 meters
- RMS Error: < 13 meters
- Success Rate: > 65%

## Validation

The model has been designed to:
1. ✅ Parse without errors in CPN Tools (DTD format 6)
2. ✅ Initialize without errors
3. ✅ Execute simulation steps
4. ✅ Cover all paper sections (interference, filtering, EKF, evaluation)
5. ✅ Properly escape XML characters in ML code
6. ✅ Use unique IDs for all elements
7. ✅ Include all required color sets and variables

## Technical Details

### XML Structure
- DTD: CPN Tools version 6
- Encoding: ISO-8859-1
- Generator: CPN Tools 4.0.1

### ML Code
- Standard ML syntax
- All comparison operators properly escaped (`<` → `&lt;`, `>` → `&gt;`)
- CDATA sections for code blocks

### Graphical Elements
- Places: Ellipses with proper attributes
- Transitions: Boxes with action code
- Arcs: Directed with annotations
- Layout: Organized hierarchically

## Troubleshooting

### If file doesn't open:
1. Check CPN Tools version (4.0.1 or later recommended)
2. Verify XML is well-formed
3. Check for character encoding issues

### If simulation fails:
1. Verify initial marking is loaded (Tools → Simulator → Init)
2. Check that all transitions are enabled
3. Review ML code for syntax errors

### If results don't match paper:
1. Verify initial marking values
2. Check scenario parameters
3. Review EKF tuning parameters (process/measurement noise)
4. Compare with GNSS_Sample_Data.sml expected values

## References
- Petrii.PDF - Original research paper
- CPN Tools documentation: http://cpntools.org
- Standard ML documentation

## Contact
For issues or questions, refer to the repository:
https://github.com/benyaminalipoor/gnss-train-positioning-cpn-
