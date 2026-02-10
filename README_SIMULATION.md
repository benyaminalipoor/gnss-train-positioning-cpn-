# GNSS Train Positioning System - Complete MATLAB Simulation

## شبیه‌سازی کامل سیستم موقعیت‌یابی قطار با GNSS در متلب
## Complete Simulation of GNSS-Based Train Positioning with Petri Nets and Automaton

This repository contains a complete MATLAB simulation implementation of the paper:

**"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**
*Published in: High-speed Railway 3 (2025) 175–184*

---

## 📋 Overview

This simulation implements:

1. **Colored Petri Net (CPN) Model** - Full Petri net structure with places, transitions, and tokens
2. **Environment Scenario Automaton** - State machine for Open Area, Mountain, and Tunnel scenarios
3. **Signal Interference Models** - AM, FM, and Pulse interference simulation
4. **Extended Kalman Filter (EKF)** - Position estimation algorithm
5. **Complete Performance Analysis** - All figures and tables from the paper

---

## 🚀 Quick Start

### Requirements

- MATLAB R2016b or later (or GNU Octave 5.0+)
- No additional toolboxes required - uses only base MATLAB functions

### Running the Simulation

1. Open MATLAB
2. Navigate to the repository directory
3. Run the main script:

```matlab
gnss_train_positioning_complete_simulation
```

The simulation will:
- Run for 600 seconds (10 minutes) of simulated train operation
- Generate all 8 figures as PNG files
- Display Tables 4 and 5 in the command window
- Save results to `gnss_simulation_results.mat`

**Estimated runtime:** 10-30 seconds (depending on your computer)

---

## 📊 Generated Outputs

### Figures

The simulation generates the following figures exactly as shown in the paper:

1. **Figure_01_Modeling_Framework.png** - System architecture diagram
2. **Figure_10_Tunnel_Errors.png** - Main result showing position errors in tunnel scenario
3. **Figure_Interference_Comparison.png** - Comparison of all interference types
4. **Figure_Environment_Comparison.png** - Comparison of environment scenarios
5. **Figure_3D_Trajectory.png** - 3D visualization of train trajectory
6. **Figure_Petri_Net_States.png** - Automaton state evolution
7. **Figure_CPN_Petri_Net_Structure.png** - Petri net structure diagram
8. **Figure_Interference_Signals.png** - Three types of interference signals

### Tables

The simulation prints the following tables to the command window:

- **Table 4:** Positioning performances under different signal interferences (Normal, AM, FM, Pulse)
- **Table 5:** Positioning performances under different environment scenarios (Open Area, Mountain, Tunnel)

### Data Files

- **gnss_simulation_results.mat** - Contains all simulation results for further analysis

---

## 🏗️ System Architecture

### Petri Net Structure

The implementation follows the hierarchical CPN model from the paper:

```
┌─────────────────────────────────────────────────────────┐
│              GNSS TRAIN POSITIONING SYSTEM              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │    GNSS      │───▶│ Environment  │───▶│Interfere │ │
│  │  Receiver    │    │  Scenarios   │    │ Signals  │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│         │                   │                   │      │
│         └───────────────────┴───────────────────┘      │
│                             │                          │
│                             ▼                          │
│                    ┌──────────────┐                   │
│                    │     EKF      │                   │
│                    │Position Soln │                   │
│                    └──────────────┘                   │
│                             │                          │
│                             ▼                          │
│                    ┌──────────────┐                   │
│                    │  Evaluation  │                   │
│                    └──────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

### Automaton States

The environment scenario automaton transitions through these states:

1. **Open Area (State 1)** - Normal operation, all satellites visible
2. **Mountain (State 2)** - Some satellites blocked by terrain
3. **Inside Tunnel (State 3)** - All GNSS signals blocked
4. **Just Out of Tunnel (State 4)** - High initial errors, recovering
5. **Stabilized (State 5)** - Normal operation restored

---

## 🔬 Technical Implementation

### Colored Petri Net Components

#### Places (Tokens)
- `GNSS_Signal` - Available satellite signals
- `Scenario` - Current environment scenario
- `GNSS_Observation` - Processed observations
- `Position` - Calculated train position
- `Delta_Position` - Position error

#### Transitions (Firings)
1. **Choose Scenario** - Select environment based on automaton state
2. **Process Interference** - Apply AM/FM/Pulse interference
3. **EKF Update** - Kalman filter prediction and update
4. **Calculate Error** - Compare with reference trajectory

### Signal Interference Models

#### AM Interference
- Modulation frequency: 1 Hz
- Carrier frequency: 1575.42 MHz (GPS L1)
- Modulation depth: 0.5

#### FM Interference
- Carrier frequency: 1575.42 MHz
- Frequency deviation: ±75 kHz
- Modulation pattern: Gaussian distribution

#### Pulse Interference
- Pulse width: 2 seconds
- Pulse interval: 10 seconds
- Amplitude: 1-5 (variable)

### Extended Kalman Filter

**State vector:** `x = [x, y, z, vx, vy, vz]`
- Position: (x, y, z) in meters
- Velocity: (vx, vy, vz) in m/s

**Measurement:** Pseudoranges from 4 satellites

**Process model:** Constant velocity motion model

```
x(k+1) = F * x(k) + w(k)
z(k) = h(x(k)) + v(k)
```

---

## 📈 Expected Results

### Table 4: Signal Interference Performance

| Scenario | Mean Error (m) | Std Deviation (m) |
|----------|----------------|-------------------|
| Normal   | ~1.03          | ~0.06             |
| AM       | ~4.95          | ~4.08             |
| FM       | ~6.22          | ~5.26             |
| Pulse    | ~4.79          | ~3.62             |

### Table 5: Environment Scenario Performance

| Scenario          | Mean Error (m) | Std Deviation (m) |
|-------------------|----------------|-------------------|
| Open Area         | ~1.03          | ~0.06             |
| Mountain Occlusion| ~1.30          | ~0.45             |
| Tunnel            | ~5.67          | ~6.69             |

### Key Findings

1. **FM interference** has the most severe impact on positioning accuracy
2. **Tunnel scenarios** show the largest positioning errors
3. Position errors **decrease exponentially** after tunnel exit
4. **Open area** provides the best positioning performance
5. The **elevation direction** is most sensitive to signal disruptions

---

## 🎯 Key Features

### Petri Net Simulation
- ✅ Complete CPN model structure
- ✅ Token-based state representation
- ✅ Transition firing rules
- ✅ Hierarchical module organization

### Automaton Implementation
- ✅ Finite state machine for scenarios
- ✅ State transition logic
- ✅ Time-based scenario switching
- ✅ Dynamic satellite visibility

### Signal Processing
- ✅ Realistic GNSS signal generation
- ✅ Three types of interference
- ✅ Multipath effects
- ✅ Tunnel blockage simulation

### Positioning Algorithm
- ✅ Extended Kalman Filter
- ✅ Prediction and update steps
- ✅ Dynamic measurement covariance
- ✅ Robust to missing satellites

---

## 🔧 Customization

### Modify Simulation Parameters

Edit the parameters in Section 1 of the script:

```matlab
% Time simulation
T_sim = 600;         % Simulation duration (seconds)

% Train parameters
v_train = 20;        % Train velocity (m/s)

% Noise parameters
sigma_pseudorange = 1.0;  % Measurement noise (m)

% Scenario timing
% Modify the automaton state transitions in Section 4
```

### Add New Scenarios

To add a new environment scenario:

1. Define the scenario in Section 4 (Automaton)
2. Add processing logic in Section 7
3. Include in the results structure

### Modify Interference Models

Adjust interference parameters in Section 5:

```matlab
% AM parameters
f_am_mod = 1;        % Modulation frequency (Hz)

% FM parameters
f_fm_dev = 75e3;     % Frequency deviation (Hz)

% Pulse parameters
T_pulse = 2;         % Pulse width (seconds)
T_interval = 10;     % Pulse interval (seconds)
```

---

## 📚 Reference

This implementation is based on the paper:

**Chen, S., Wu, D., Liu, J., & Wang, S. (2025).** Modeling and performance analysis of GNSS-based train positioning system with colored petri nets. *High-speed Railway*, 3, 175-184.

### Paper Sections Implemented

- ✅ Section 3.1: Top-level positioning system model
- ✅ Section 3.2: GNSS Receiver module
  - ✅ 3.2.1: Open Area submodule
  - ✅ 3.2.2: Mountain submodule
  - ✅ 3.2.3: Tunnel submodule
- ✅ Section 3.3: GNSS Position Solution (EKF)
- ✅ Section 3.4: Evaluation module
- ✅ Section 4: Simulation and analysis results
  - ✅ 4.1: Different signal interferences
  - ✅ 4.2: Different environment scenarios

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** Figures not saving
- **Solution:** Ensure you have write permissions in the current directory

**Issue:** Out of memory
- **Solution:** Reduce `T_sim` to a smaller value (e.g., 300 seconds)

**Issue:** Slow execution
- **Solution:** Reduce the number of satellites or time steps

**Issue:** MATLAB version compatibility
- **Solution:** The script uses only basic functions. If you encounter errors, check:
  - Matrix operations syntax
  - Figure saving functions
  - Structure array usage

---

## 📝 Code Structure

The script is organized into 12 major sections:

1. **Parameters** - All simulation settings
2. **Trajectory** - Generate reference path
3. **Satellites** - Constellation generation
4. **Automaton** - Environment state machine
5. **Interference** - AM, FM, Pulse signals
6. **Petri Net** - CPN simulation setup
7. **Scenarios** - Run all test cases
8. **Figures** - Generate paper figures
9. **Tables** - Generate paper tables
10. **Petri Net Diagram** - Visual CPN structure
11. **Signals Visualization** - Interference plots
12. **Summary** - Results and statistics

Each section is clearly marked with headers for easy navigation.

---

## 🤝 Contributing

This is an educational implementation for understanding the paper's methodology. 

Suggestions for improvements:
- Add real satellite ephemeris data
- Implement more sophisticated interference models
- Add INS/GNSS integration
- Include map-matching algorithms

---

## 📄 License

This simulation is provided for educational and research purposes, implementing the methodology described in the referenced paper.

---

## ✉️ Contact

For questions about the implementation, please refer to the original paper or open an issue in this repository.

---

## 🌟 Acknowledgments

This implementation is based on the research by Chen, S., Wu, D., Liu, J., & Wang, S. from Beijing Jiaotong University, published in High-speed Railway journal (2025).

The work was supported by:
- National Key Research and Development Program of China (2023YFB3907300)
- Fundamental Research Funds for the Central Universities (2024JBMC002)
- National Natural Science Foundation of China (T2222015, U2268206)

---

**Note:** This is a complete, self-contained MATLAB script that reproduces all major results from the paper. No additional files or toolboxes are required.
