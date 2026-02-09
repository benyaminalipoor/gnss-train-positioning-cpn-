# GNSS Train Positioning System - CPN Tools Model Documentation

This document provides complete specifications for implementing the paper "Modeling and performance analysis of GNSS-based train positioning system with colored petri nets" in CPN Tools.

## 1. Color Set Declarations (Table 1)

```sml
(* Boolean and Basic Types *)
colset BOOL = bool;
colset INT = int;
colset INTTIME = int timed;
colset REAL = real;

(* GNSS Signal Structure *)
colset SIGNAL = record 
    id: INT * 
    psr: REAL * 
    psr_rate: REAL *
    x: REAL * 
    y: REAL * 
    z: REAL * 
    vx: REAL * 
    vy: REAL * 
    vz: REAL * 
    clk: REAL * 
    azimuth: REAL * 
    elevation: REAL * 
    Rate_clock: REAL;

colset SIGNALlist = list SIGNAL;
colset SIGNALLIST = product INT * INT * SIGNALlist;

(* Scenario and State Types *)
colset SCENARIO = with OpenArea | Mountain | Tunnel;
colset STATEINFE = with AM | FM | Pulse | Normal;

(* Coordinate Types *)
colset Coordinate = product REAL * REAL * REAL;
colset COORDINATE = product INT * Coordinate;
colset DELTAPOSITION = product INT * Coordinate * REAL;

(* Time and Distance Types *)
colset TIMESTAMP = real;
colset HEIGHT = real;
colset DISTANCE = real;

(* Environment Types *)
colset MOUNTAIN = product HEIGHT * DISTANCE;
colset TUNNELSTATE = with InTunnel | JustOut | OutTunnel;
colset TUNNEL = real;

(* Mutex for synchronization *)
colset MUTEX = unit;
```

## 2. Variable Declarations (Table 2)

```sml
var VisibleBDS, SigInfo: SIGNALLIST;
var Envi: SCENARIO;
var InterferenceData, InterferenceData1: SIGNALLIST;
var Mutex: MUTEX;
var StateInterference: STATEINFE;
var deltaPosition: DELTAPOSITION;
var bAM, bFM, bPulse: BOOL;
var AMError, FMError, PulseError: REAL;
var TrainPosition, TrainPosition1: TUNNELSTATE;
var DelayError, TimeCounter, TimeCounter1: TIMESTAMP;
var position, TrackCoordinate, BDS_ENU: COORDINATE;
var t, epoch: INT;
var signalList: SIGNALlist;
var sig: SIGNAL;
var mountain: MOUNTAIN;
var h: HEIGHT;
var d: DISTANCE;
```

## 3. Helper Functions

```sml
(* Calculate Euclidean distance between two 3D coordinates *)
fun euclideanDistance ((x1, y1, z1): Coordinate) ((x2, y2, z2): Coordinate) : REAL =
    Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1));

(* AM Interference - Amplitude Modulation *)
(* Carrier frequency: 1575.42 MHz (GNSS L1 band) *)
(* Envelope frequency: 1 Hz *)
(* Modulation depth: 0.5 *)
fun applyAMInterference (sig: SIGNAL) (time: REAL) : SIGNAL =
    let
        val modulationDepth = 0.5
        val carrierFreq = 1575.42e6
        val envelopeFreq = 1.0
        val envelope = 1.0 + modulationDepth * Math.sin(2.0 * Math.pi * envelopeFreq * time)
        val errorMag = envelope * 2.0
    in
        {id = #id sig, 
         psr = #psr sig + errorMag,
         psr_rate = #psr_rate sig,
         x = #x sig, y = #y sig, z = #z sig,
         vx = #vx sig, vy = #vy sig, vz = #vz sig,
         clk = #clk sig,
         azimuth = #azimuth sig,
         elevation = #elevation sig,
         Rate_clock = #Rate_clock sig}
    end;

(* FM Interference - Frequency Modulation *)
(* Carrier frequency: 1575.42 MHz (GNSS L1 band) *)
(* Frequency deviation: 75 kHz (Gaussian distribution std) *)
fun applyFMInterference (sig: SIGNAL) (time: REAL) : SIGNAL =
    let
        val carrierFreq = 1575.42e6
        val freqDev = 75000.0
        val freqShift = freqDev * Math.sin(2.0 * Math.pi * 0.5 * time)
        val errorMag = 3.0 * Math.abs(Math.sin(freqShift * time))
    in
        {id = #id sig, 
         psr = #psr sig + errorMag,
         psr_rate = #psr_rate sig,
         x = #x sig, y = #y sig, z = #z sig,
         vx = #vx sig, vy = #vy sig, vz = #vz sig,
         clk = #clk sig,
         azimuth = #azimuth sig,
         elevation = #elevation sig,
         Rate_clock = #Rate_clock sig}
    end;

(* Pulse Interference - Periodic pulse signals *)
(* Pulse width Tp: sampled uniformly *)
(* Pulse interval Ti: sampled uniformly *)
(* Amplitude: uniformly distributed between 1 and 5 *)
fun applyPulseInterference (sig: SIGNAL) (time: REAL) : SIGNAL =
    let
        val pulseWidth = 0.01  (* Tp = 10ms *)
        val pulseInterval = 0.09  (* Ti = 90ms *)
        val pulsePeriod = pulseWidth + pulseInterval
        val timeInPeriod = Real.rem(time, pulsePeriod)
        val amplitude = if timeInPeriod < pulseWidth then 3.5 else 0.0
    in
        {id = #id sig, 
         psr = #psr sig + amplitude,
         psr_rate = #psr_rate sig,
         x = #x sig, y = #y sig, z = #z sig,
         vx = #vx sig, vy = #vy sig, vz = #vz sig,
         clk = #clk sig,
         azimuth = #azimuth sig,
         elevation = #elevation sig,
         Rate_clock = #Rate_clock sig}
    end;

(* Mountain Obstruction Check *)
fun isObstructedByMountain (sig: SIGNAL) (height: HEIGHT) (distance: DISTANCE) : bool =
    let
        val obstructionAngle = Math.atan(height / distance) * 180.0 / Math.pi
        val satElevation = #elevation sig
    in
        satElevation < obstructionAngle
    end;

(* Filter satellites obstructed by mountain *)
fun filterMountainObstructed (signals: SIGNALlist) (mountain: MOUNTAIN) : SIGNALlist =
    let
        val (height, distance) = mountain
        fun notObstructed sig = not (isObstructedByMountain sig height distance)
    in
        List.filter notObstructed signals
    end;

(* Tunnel Error Application *)
(* InTunnel: Complete signal loss *)
(* JustOut: High error with exponential decrease *)
(* OutTunnel: Stable low error *)
fun applyTunnelError (sig: SIGNAL) (state: TUNNELSTATE) (timeCounter: REAL) : SIGNAL =
    let
        val errorMag = case state of
            InTunnel => 0.0
          | JustOut => 15.0 * Math.exp(~0.1 * timeCounter)
          | OutTunnel => 0.5
    in
        {id = #id sig, 
         psr = #psr sig + errorMag,
         psr_rate = #psr_rate sig,
         x = #x sig, y = #y sig, z = #z sig,
         vx = #vx sig, vy = #vy sig, vz = #vz sig,
         clk = #clk sig,
         azimuth = #azimuth sig,
         elevation = #elevation sig,
         Rate_clock = #Rate_clock sig}
    end;

(* Apply interference to signal list *)
fun applyInterferenceToList (signals: SIGNALlist) (intType: STATEINFE) (time: REAL) : SIGNALlist =
    case intType of
        AM => List.map (fn sig => applyAMInterference sig time) signals
      | FM => List.map (fn sig => applyFMInterference sig time) signals
      | Pulse => List.map (fn sig => applyPulseInterference sig time) signals
      | Normal => signals;

(* Simple EKF position calculation *)
fun calculateEKFPosition (signals: SIGNALlist) (epoch: INT) : COORDINATE =
    let
        val numSats = List.length signals
        val sumX = List.foldl (fn (sig, acc) => acc + #x sig) 0.0 signals
        val sumY = List.foldl (fn (sig, acc) => acc + #y sig) 0.0 signals
        val sumZ = List.foldl (fn (sig, acc) => acc + #z sig) 0.0 signals
        val n = Real.fromInt numSats
        val avgPos = (sumX / n, sumY / n, sumZ / n)
    in
        (epoch, avgPos)
    end;
```

## 4. Model Structure

### 4.1 Top-Level Model (Figure 3)

**Places:**
- `Scenario` (SCENARIO) - Initial marking: `1`OpenArea`
- `GNSS Signal` (SIGNALLIST) - Stores visible satellite data
- `GNSS Observation` (SIGNALLIST) - Processed GNSS data with errors
- `Position` (COORDINATE) - Calculated train position
- `Delta Position` (DELTAPOSITION) - Positioning error
- `Reference Position` (COORDINATE) - Ground truth position

**Substitution Transitions:**
- `GNSS Receiver` - Processes GNSS signals and scenarios
- `Position Solution` - EKF algorithm for position calculation
- `Evaluation` - Compares calculated vs reference position

### 4.2 GNSS Receiver Module (Figure 4)

**Places:**
- `Scenario` (Input) - Environment scenario selection
- `GNSS Signal` (Input) - Visible satellites
- `Choose Scenario` - Scenario routing
- `GNSS Observation` (Output) - Processed signals

**Transitions:**
- `Choose Scenario` - Routes to appropriate submodule

**Submodules:**
- Open Area Scenario
- Mountain Occlusion Scenario  
- Tunnel and Exit Tunnel Scenario

### 4.3 Open Area Submodule (Figure 5)

**Places:**
- `Open Area` (Input)
- `GNSS Signal` (Input)
- `Bool Control` - Interference control flags
- `GNSS Number` - Satellite counter
- `GNSS Observation` (Output)

**Transitions:**
- `AM Interference` - Apply AM interference
  - Guard: `bAM = true`
  - Code: Apply AM error based on time-varying envelope
- `FM Interference` - Apply FM interference
  - Guard: `bFM = true`
  - Code: Apply FM error with frequency deviation
- `Pulse Interference` - Apply pulse interference
  - Guard: `bPulse = true`
  - Code: Apply periodic pulse error
- `Mutex` - Ensure mutual exclusion of interference types
- `Interference` - Combine interference with GNSS data

### 4.4 Mountain Submodule (Figure 6)

**Places:**
- `Mountain Height` (HEIGHT) - Mountain elevation
- `Distance` (DISTANCE) - Distance to mountain
- `GNSS Signal` (Input)
- `Data with Mountain Error` - Filtered signals
- `GNSS Observation` (Output)

**Transitions:**
- `Mountain Data Fusion` - Combine height and distance
- `Mountain Scenario` - Filter obstructed satellites
  - Code: Compare satellite elevation with obstruction angle
  - Filter out satellites below obstruction angle

### 4.5 Tunnel Submodule (Figure 7)

**Places:**
- `InTunnel` (TUNNELSTATE)
- `Just Out` (TUNNELSTATE)
- `Out Tunnel` (TUNNELSTATE)
- `Tunnel` (Input) - Tunnel state
- `GNSS Signal` (Input)
- `Time Counter` (TIMESTAMP)
- `GNSS Observation` (Output)

**Transitions:**
- `Tunnel Scenario` - Apply tunnel effects
  - InTunnel: No signals (empty output)
  - JustOut: High errors (15m initially, exponential decay)
  - OutTunnel: Stable low error (0.5m)

### 4.6 GNSS Position Solution Module (Figure 8)

**Places:**
- `GNSS Observation` (Input)
- `bEKF` (BOOL) - EKF completion flag
- `Position` (Output)

**Transitions:**
- `EKF` - Extended Kalman Filter
  - Algorithm 1 implementation
  - Process GNSS observations
  - Calculate position coordinates

### 4.7 Evaluation Module (Figure 9)

**Places:**
- `Position` (Input) - Calculated position
- `Reference Position` (Input) - Ground truth
- `Delta Position` (Output) - Error result
- `Select Environment` - Scenario selector

**Transitions:**
- `Select Environment Scenario` - Choose test scenario
- `Calculate Position Error` - Compute error
  - Formula: d = sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)

## 5. Simulation Data

### 5.1 Input Data Format

```
Example GNSS Signal data entry:
(epoch, timestamp, [
    {id=1, psr=20000000.0, psr_rate=0.0, 
     x=15000000.0, y=20000000.0, z=18000000.0,
     vx=1000.0, vy=500.0, vz=800.0,
     clk=0.0001, azimuth=45.0, elevation=60.0, Rate_clock=0.0},
    {id=2, psr=22000000.0, psr_rate=0.0,
     x=18000000.0, y=15000000.0, z=20000000.0,
     vx=900.0, vy=600.0, vz=700.0,
     clk=0.0001, azimuth=120.0, elevation=55.0, Rate_clock=0.0},
    ...
])
```

### 5.2 Simulation Parameters

- Simulation time: 600 time units (10 minutes)
- Time step: 1 second per unit
- Dataset: Jing-Shen high-speed railway segment
- Satellite constellation: BeiDou/GPS
- RINEX ephemeris data format

## 6. Expected Results (from Paper)

### 6.1 Signal Interference Performance (Table 4)

| Scenario | Mean Error (m) | Std Dev (m) |
|----------|----------------|-------------|
| Normal   | 1.0279         | 0.0552      |
| AM       | 4.9484         | 4.0833      |
| FM       | 6.2241         | 5.2630      |
| Pulse    | 4.7925         | 3.6242      |

### 6.2 Environment Scenario Performance (Table 5)

| Scenario           | Mean Error (m) | Std Dev (m) |
|--------------------|----------------|-------------|
| Open Area          | 1.0279         | 0.0552      |
| Mountain Occlusion | 1.2979         | 0.4528      |
| Tunnel             | 5.6670         | 6.6901      |

### 6.3 State Space Verification (Table 3)

- State space nodes: 5365
- State space arcs: 6410
- Dead markings: 648
- No dead or live transitions
- No infinite occurrence sequences
- Model is sound, bounded, and has finite execution

## 7. Implementation Instructions

1. Open CPN Tools
2. Create new model
3. Declare all color sets in Declarations section
4. Declare all variables in Declarations section
5. Add all helper functions in Declarations section
6. Create Top-level page with structure from Section 4.1
7. Create subpages for each module (Sections 4.2-4.7)
8. Add initial markings as specified
9. Add transition guards and code inscriptions
10. Load simulation data
11. Set breakpoint monitor at time=600
12. Run simulation
13. Collect and analyze results
14. Compare with expected results (Tables 4-5)

## 8. Key Implementation Notes

- All coordinate calculations in UTM system
- Interference signals affect pseudorange (psr) field
- Mountain filtering based on elevation angle comparison
- Tunnel effects modeled as three-phase state machine
- EKF simplified for CPN Tools matrix limitations
- External MATLAB for complex EKF calculations
- Time-based simulation with 1 second per unit

## 9. File Structure

```
GNSS_Train_Positioning.cpn - Main CPN Tools model file
└── Pages
    ├── Top Level (Figure 3)
    ├── GNSS Receiver (Figure 4)
    │   ├── Open Area (Figure 5)
    │   ├── Mountain (Figure 6)
    │   └── Tunnel (Figure 7)
    ├── Position Solution (Figure 8)
    └── Evaluation (Figure 9)
```

## 10. Validation Checklist

- [ ] All 13 color sets declared correctly
- [ ] All variables declared with proper types
- [ ] Helper functions compile without errors
- [ ] All modules connected properly
- [ ] Initial markings set correctly
- [ ] Transition guards work as expected
- [ ] Simulation runs for 600 time units
- [ ] Results match paper Tables 4 and 5
- [ ] State space analysis matches Table 3
- [ ] No syntax errors in CPN Tools
