# GNSS Train Positioning CPN - Quick Start Guide

## Installation

No installation required! Just ensure you have Java 8+ installed.

Check your Java version:
```bash
java -version
```

## Running the Simulation

### Step 1: Compile
```bash
javac GNSSTrainPositioningCPN.java
```

### Step 2: Run
```bash
java GNSSTrainPositioningCPN
```

### Step 3: View Results
The simulation will:
1. Print progress to console
2. Generate `simulation_results.csv` with detailed trajectory data
3. Generate `simulation_statistics.txt` with statistical summaries
4. Open a visualization window (if display available)

## Understanding the Output

### Console Output
```
╔════════════════════════════════════════════════════════════╗
║  GNSS Train Positioning System using Colored Petri Nets  ║
║  Implementation with Extended Kalman Filter              ║
╚════════════════════════════════════════════════════════════╝

=== Starting GNSS Train Positioning CPN Simulation ===

Running scenario: OPEN_AREA_NORMAL
  t=0s: Error=14.76m
  t=20s: Error=4.71m
  ...
Completed OPEN_AREA_NORMAL: Mean Error=4.23m, Max Error=14.76m, Std=1.39m
```

### CSV File Format
```csv
Scenario,Environment,Interference,Time,True_X,True_Y,True_Z,Est_X,Est_Y,Est_Z,Error
OPEN_AREA_NORMAL,OPEN_AREA,NORMAL,0.0,0.000,0.000,100.000,14.677,1.462,99.533,14.757
```

Columns:
- **Scenario**: Unique scenario identifier
- **Environment**: OPEN_AREA, MOUNTAIN, or TUNNEL
- **Interference**: NORMAL, AM, FM, or PULSE
- **Time**: Simulation time in seconds (0-100)
- **True_X/Y/Z**: Ground truth position (meters)
- **Est_X/Y/Z**: Estimated position from EKF (meters)
- **Error**: 3D position error magnitude (meters)

### Statistics File
Contains:
- Mean, max, and standard deviation of errors for each scenario
- Environment comparison (with normal interference)
- Interference comparison (in open area)
- Validation against expected trends

## Simulation Scenarios

### 1. Environmental Scenarios (Normal Interference)
- **OPEN_AREA_NORMAL**: Baseline best case
- **MOUNTAIN_NORMAL**: Moderate signal degradation
- **TUNNEL_NORMAL**: Worst case environment

### 2. Interference Scenarios (Open Area)
- **OPEN_AREA_NORMAL**: Baseline
- **OPEN_AREA_AM**: Amplitude modulation interference
- **OPEN_AREA_FM**: Frequency modulation interference (most severe)
- **OPEN_AREA_PULSE**: Pulse interference

## Visualization Window

The GUI displays 4 panels:

### 1. Error Time Series (Top Left)
- X-axis: Time (0-100 seconds)
- Y-axis: Position error (0-20 meters)
- Shows all 6 scenarios as colored lines
- Legend identifies each scenario

### 2. Environment Comparison (Top Right)
- Bar chart comparing OPEN_AREA, MOUNTAIN, TUNNEL
- Shows mean error with normal interference
- Expected trend: Tunnel > Mountain > Open Area

### 3. Interference Comparison (Bottom Left)
- Bar chart comparing NORMAL, AM, FM, PULSE
- Shows mean error in open area
- Expected trend: FM > AM > Pulse > Normal

### 4. CPN Structure Diagram (Bottom Right)
- Hierarchical architecture visualization
- Shows Places (circles), Transitions (rectangles), and Arcs (arrows)
- Displays all three sub-models:
  - GNSS Receiver CPN
  - Position Solution CPN (with EKF)
  - Evaluation CPN

## Interpreting Results

### Expected Performance
Based on research literature:

| Scenario | Expected Error | Actual Error |
|----------|---------------|--------------|
| Open + Normal | ~1m | ~4m |
| Tunnel + Normal | ~6-7m | ~20m |
| Open + FM | ~3-4m | ~14m |

**Note**: Actual errors may be higher due to conservative noise modeling and initial convergence.

### Key Trends to Verify
✓ FM interference causes highest error
✓ Tunnel environment causes highest error
✓ Open area with normal interference gives best performance
✓ Error decreases over time as EKF converges

## Advanced Usage

### Modifying Simulation Parameters

Edit `GNSSTrainPositioningCPN.java`:

**Change simulation duration:**
```java
int duration = 100; // Change to desired seconds
```

**Adjust train speed:**
```java
double speed = 20.0; // Change to desired m/s
```

**Modify noise levels:**
```java
double processNoise = 0.1;      // Process noise
double measurementNoise = 4.0;  // Measurement noise
```

**Change environment factors:**
```java
OPEN_AREA(1.0),      // Noise multiplier
MOUNTAIN(2.5),
TUNNEL(5.0);
```

### Adding New Scenarios

Add to `runAllScenarios()`:
```java
results.add(runScenario(Environment.MOUNTAIN, Interference.FM, duration));
```

## Troubleshooting

### No display/GUI error
This is normal in headless environments (servers, CI/CD). The simulation still runs and generates CSV/text files.

### Large errors initially
The EKF starts with initial position error (~10m) and needs time to converge. This is expected behavior.

### Different results each run
The simulation uses a fixed random seed (42) for reproducibility. Results should be consistent across runs.

## Data Analysis Tips

### Using Python/Pandas
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load results
df = pd.read_csv('simulation_results.csv')

# Plot specific scenario
scenario_data = df[df['Scenario'] == 'OPEN_AREA_NORMAL']
plt.plot(scenario_data['Time'], scenario_data['Error'])
plt.xlabel('Time (s)')
plt.ylabel('Error (m)')
plt.title('GNSS Position Error')
plt.show()
```

### Using Excel
1. Open `simulation_results.csv` in Excel
2. Create pivot table with Time and Error
3. Generate charts for analysis

## Performance Notes

- Compilation: ~2-3 seconds
- Execution: ~5-10 seconds for 6 scenarios (100 seconds each)
- Memory: ~50-100 MB
- Output files: ~50 KB CSV + ~2 KB statistics

## Support

For questions or issues:
1. Check simulation output for error messages
2. Verify Java version (8+)
3. Review console statistics to validate results
4. Check CSV file for detailed trajectory data

## Next Steps

1. **Analyze Results**: Open CSV in spreadsheet software
2. **Modify Parameters**: Experiment with different settings
3. **Add Scenarios**: Test custom environment/interference combinations
4. **Extend Model**: Add new features like clock bias, ionospheric delay
5. **Optimize EKF**: Tune process/measurement noise covariance

## Citation

If using this implementation for research:
```
GNSS Train Positioning System using Colored Petri Nets
Extended Kalman Filter Implementation
2024
```
