# Visual Model Structure - GNSS Train Positioning System

## Model Hierarchy Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TOP LEVEL (Figure 3)                             │
│                                                                          │
│  ┌──────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐   │
│  │Scenario  │───▶│    GNSS     │───▶│    GNSS     │───▶│ Position │   │
│  │          │    │  Receiver   │    │ Observation │    │          │   │
│  └──────────┘    └─────────────┘    └─────────────┘    └──────────┘   │
│       │                                                        │         │
│       │          ┌─────────────┐    ┌─────────────┐          │         │
│       │          │    GNSS     │───▶│  Position   │          │         │
│       │          │   Signal    │    │  Solution   │          │         │
│       │          └─────────────┘    └─────────────┘          │         │
│       │                 │                  │                  │         │
│       │                 │                  │                  │         │
│       │          ┌──────▼──────────────────▼───┐             │         │
│       └─────────▶│      Evaluation             │◀────────────┘         │
│                  │  (Error Calculation)        │                       │
│                  └─────────────────────────────┘                       │
│                            │                                            │
│                            ▼                                            │
│                  ┌─────────────┐                                       │
│                  │Delta Position│                                       │
│                  └─────────────┘                                       │
│                                                                          │
│  Reference Position ─────────────────────────────────────▲              │
│                                                           │              │
│                                                    (Ground Truth)        │
└─────────────────────────────────────────────────────────────────────────┘
```

## GNSS Receiver Module Detail (Figure 4)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    GNSS RECEIVER MODULE                                   │
│                                                                           │
│   Input: Scenario + GNSS Signal                                          │
│                    │                                                      │
│                    ▼                                                      │
│          ┌──────────────────┐                                           │
│          │ Choose Scenario  │                                           │
│          └────┬────┬────┬───┘                                           │
│               │    │    │                                                │
│      ┌────────┘    │    └────────┐                                      │
│      │             │              │                                      │
│      ▼             ▼              ▼                                      │
│  ┌────────┐  ┌─────────┐  ┌─────────┐                                  │
│  │  Open  │  │Mountain │  │ Tunnel  │                                  │
│  │  Area  │  │Occlusion│  │Scenario │                                  │
│  └────┬───┘  └────┬────┘  └────┬────┘                                  │
│       │           │             │                                        │
│       └───────────┴─────────────┘                                        │
│                   │                                                       │
│                   ▼                                                       │
│          ┌──────────────────┐                                           │
│          │ GNSS Observation │                                           │
│          │   (Output)       │                                           │
│          └──────────────────┘                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Open Area Submodule (Figure 5)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    OPEN AREA SUBMODULE                                    │
│                   (Signal Interference)                                   │
│                                                                           │
│   Input: Open Area + GNSS Signal                                         │
│                    │                                                      │
│          ┌─────────▼──────────┐                                          │
│          │   Bool Control     │                                          │
│          │  bAM, bFM, bPulse  │                                          │
│          └─────┬──┬──┬────────┘                                          │
│                │  │  │                                                    │
│       ┌────────┘  │  └────────┐                                          │
│       │           │            │                                          │
│       ▼           ▼            ▼                                          │
│  ┌────────┐  ┌───────┐  ┌──────────┐                                    │
│  │   AM   │  │  FM   │  │  Pulse   │                                    │
│  │ Inter. │  │ Inter.│  │  Inter.  │                                    │
│  └───┬────┘  └───┬───┘  └────┬─────┘                                    │
│      │           │            │                                           │
│      └───────────┴────────────┘                                           │
│                  │                                                         │
│            ┌─────▼──────┐                                                │
│            │   Mutex    │  ← Ensures mutual exclusion                    │
│            └─────┬──────┘                                                │
│                  │                                                         │
│            ┌─────▼──────────┐                                            │
│            │  Interference  │  ← Apply selected interference              │
│            └─────┬──────────┘                                            │
│                  │                                                         │
│            ┌─────▼──────────┐                                            │
│            │ GNSS Number    │  ← Counter                                 │
│            └─────┬──────────┘                                            │
│                  │                                                         │
│                  ▼                                                         │
│          ┌──────────────────┐                                            │
│          │ GNSS Observation │                                            │
│          │   (Output)       │                                            │
│          └──────────────────┘                                            │
│                                                                           │
│  Interference Effects:                                                    │
│  • AM:    Carrier 1575.42MHz, Envelope 1Hz, Depth 0.5                   │
│  • FM:    Freq dev 75kHz, Gaussian distribution                         │
│  • Pulse: Width 10ms, Interval 90ms, Amplitude 1-5                      │
└──────────────────────────────────────────────────────────────────────────┘
```

## Mountain Submodule (Figure 6)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    MOUNTAIN SUBMODULE                                     │
│                  (Terrain Obstruction)                                    │
│                                                                           │
│   ┌───────────────┐      ┌──────────┐                                   │
│   │Mountain Height│      │ Distance │                                   │
│   │   (meters)    │      │ (meters) │                                   │
│   └───────┬───────┘      └────┬─────┘                                   │
│           │                   │                                           │
│           └────────┬──────────┘                                           │
│                    │                                                       │
│                    ▼                                                       │
│          ┌──────────────────┐                                            │
│          │ Mountain Data    │                                            │
│          │    Fusion        │                                            │
│          └────────┬─────────┘                                            │
│                   │                                                        │
│   GNSS Signal ────┤                                                       │
│                   │                                                        │
│                   ▼                                                        │
│          ┌──────────────────┐                                            │
│          │ Mountain Scenario│                                            │
│          │  (Filter Sats)   │                                            │
│          └────────┬─────────┘                                            │
│                   │                                                        │
│         ┌─────────┴──────────┐                                            │
│         │                    │                                            │
│         ▼                    ▼                                            │
│  ┌─────────────┐    ┌──────────────────┐                                │
│  │Data with    │    │ GNSS Observation │                                │
│  │Mountain     │    │    (Output)      │                                │
│  │Error        │    └──────────────────┘                                │
│  └─────────────┘                                                          │
│                                                                           │
│  Filtering Logic:                                                         │
│  • Calculate obstruction angle: θ = atan(height/distance)                │
│  • Compare with satellite elevation                                       │
│  • Remove satellites with elevation < θ                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Tunnel Submodule (Figure 7)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    TUNNEL SUBMODULE                                       │
│                  (3-Phase Tunnel Effect)                                  │
│                                                                           │
│   Tunnel State Input                                                      │
│          │                                                                │
│    ┌─────▼─────┬──────────┬──────────┐                                  │
│    │           │          │          │                                    │
│    ▼           ▼          ▼          ▼                                    │
│ ┌─────────┐ ┌────────┐ ┌──────────┐                                     │
│ │InTunnel │ │JustOut │ │OutTunnel │                                     │
│ │         │ │        │ │          │                                     │
│ │No Signal│ │High Err│ │Stable    │                                     │
│ └────┬────┘ └───┬────┘ └────┬─────┘                                     │
│      │          │           │                                             │
│      │    ┌─────▼─────┐     │                                             │
│      │    │Time Counter│     │                                             │
│      │    └─────┬─────┘     │                                             │
│      │          │           │                                             │
│      └──────────┴───────────┘                                             │
│                 │                                                          │
│   GNSS Signal ──┤                                                         │
│                 │                                                          │
│                 ▼                                                          │
│          ┌──────────────┐                                                │
│          │   Tunnel     │                                                │
│          │  Scenario    │                                                │
│          └──────┬───────┘                                                │
│                 │                                                          │
│                 ▼                                                          │
│          ┌──────────────────┐                                            │
│          │ GNSS Observation │                                            │
│          │    (Output)      │                                            │
│          └──────────────────┘                                            │
│                                                                           │
│  Phase Details:                                                           │
│  1. InTunnel:  Complete signal blockage (no output)                      │
│  2. JustOut:   Error = 15m × exp(-0.1 × time)                           │
│  3. OutTunnel: Stable error = 0.5m                                       │
│                                                                           │
│  Error Evolution:                                                         │
│  ┌────────────────────────────────────┐                                  │
│  │        ▲ Error                     │                                  │
│  │  15m   │  ╱╲                       │                                  │
│  │        │ ╱  ╲                      │                                  │
│  │  10m   │╱    ╲___                  │                                  │
│  │   5m   │        ───___             │                                  │
│  │  0.5m  │             ─────────────▶│                                  │
│  │   0    ├──┬──────┬────────────────▶│                                  │
│  │        In Exit  Recovery  Stable   │                                  │
│  └────────────────────────────────────┘                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

## Position Solution Module (Figure 8)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  POSITION SOLUTION MODULE                                 │
│                   (EKF Algorithm)                                         │
│                                                                           │
│   Input: GNSS Observation                                                │
│                │                                                          │
│                ▼                                                          │
│         ┌──────────────┐                                                 │
│         │     EKF      │                                                 │
│         │  Algorithm   │                                                 │
│         └──────┬───────┘                                                 │
│                │                                                          │
│                ▼                                                          │
│         ┌──────────────┐                                                 │
│         │    bEKF      │  ← Completion flag                              │
│         │  (Boolean)   │                                                 │
│         └──────┬───────┘                                                 │
│                │                                                          │
│                ▼                                                          │
│         ┌──────────────┐                                                 │
│         │  Position    │                                                 │
│         │  (x, y, z)   │                                                 │
│         └──────────────┘                                                 │
│                                                                           │
│  EKF Process (Algorithm 1):                                              │
│  1. Prediction Step                                                      │
│     • State prediction: x̂ₖ₋ = Fₖ × x̂ₖ₋₁                                 │
│     • Covariance prediction: Pₖ₋ = Fₖ × Pₖ₋₁ × Fₖᵀ + Qₖ                 │
│                                                                           │
│  2. Update Step                                                          │
│     • Kalman gain: Kₖ = Pₖ₋ × Hₖᵀ × (Hₖ × Pₖ₋ × Hₖᵀ + Rₖ)⁻¹            │
│     • State update: x̂ₖ = x̂ₖ₋ + Kₖ × (zₖ - Hₖ × x̂ₖ₋)                    │
│     • Covariance update: Pₖ = (I - Kₖ × Hₖ) × Pₖ₋                       │
│                                                                           │
│  State Vector: [x, y, z, vx, vy, vz, clock_bias, clock_drift]ᵀ          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Evaluation Module (Figure 9)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    EVALUATION MODULE                                      │
│                  (Error Calculation)                                      │
│                                                                           │
│   ┌───────────────┐                                                      │
│   │   Scenario    │                                                      │
│   │   Selector    │                                                      │
│   └───────┬───────┘                                                      │
│           │                                                               │
│           ▼                                                               │
│    ┌─────────────────────┐                                               │
│    │Select Environment   │                                               │
│    │    Scenario         │                                               │
│    └──────────┬──────────┘                                               │
│               │                                                           │
│   ┌───────────┴────────────┐                                             │
│   │                        │                                             │
│   ▼                        ▼                                             │
│ ┌─────────────┐     ┌─────────────┐                                     │
│ │  Position   │     │  Reference  │                                     │
│ │ (Calculated)│     │  Position   │                                     │
│ └──────┬──────┘     └──────┬──────┘                                     │
│        │                   │                                             │
│        └────────┬──────────┘                                             │
│                 │                                                         │
│                 ▼                                                         │
│        ┌──────────────────┐                                              │
│        │Calculate Position│                                              │
│        │     Error        │                                              │
│        └────────┬─────────┘                                              │
│                 │                                                         │
│                 ▼                                                         │
│        ┌──────────────────┐                                              │
│        │ Delta Position   │                                              │
│        │    (Output)      │                                              │
│        └──────────────────┘                                              │
│                                                                           │
│  Error Calculation:                                                       │
│  d = √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]                                  │
│                                                                           │
│  Where:                                                                   │
│  • (x₁, y₁, z₁) = Reference position (ground truth)                      │
│  • (x₂, y₂, z₂) = Calculated position (from EKF)                         │
│  • d = Positioning error in meters                                       │
│                                                                           │
│  Statistics Collected:                                                    │
│  • Mean error                                                            │
│  • Standard deviation                                                    │
│  • Expected directional mean (E, N, U components)                        │
│  • Normalized directional mean                                           │
│  • Helmert directional mean                                             │
└──────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                        │
│                                                                          │
│  Start                                                                   │
│    │                                                                     │
│    ▼                                                                     │
│  ┌──────────────────┐                                                   │
│  │ Select Scenario  │ ───────┐                                          │
│  │ (Open/Mtn/Tun)   │        │                                          │
│  └────────┬─────────┘        │                                          │
│           │                  │                                          │
│           ▼                  │                                          │
│  ┌──────────────────┐        │                                          │
│  │ Load GNSS Data   │        │                                          │
│  │ (Satellites)     │        │                                          │
│  └────────┬─────────┘        │                                          │
│           │                  │                                          │
│           ▼                  ▼                                          │
│  ┌──────────────────────────────┐                                       │
│  │    Apply Environment         │                                       │
│  │    • Open: Add interference  │                                       │
│  │    • Mountain: Filter sats   │                                       │
│  │    • Tunnel: Phase effects   │                                       │
│  └────────────┬─────────────────┘                                       │
│               │                                                          │
│               ▼                                                          │
│  ┌──────────────────────┐                                               │
│  │ GNSS Observation     │                                               │
│  │ (With errors)        │                                               │
│  └────────┬─────────────┘                                               │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────────┐                                               │
│  │ EKF Position         │                                               │
│  │ Solution             │                                               │
│  └────────┬─────────────┘                                               │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────────┐                                               │
│  │ Calculate Position   │                                               │
│  │ (x, y, z)            │                                               │
│  └────────┬─────────────┘                                               │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────────┐      ┌──────────────────┐                    │
│  │ Compare with         │ ◀────│ Reference        │                    │
│  │ Reference            │      │ Position         │                    │
│  └────────┬─────────────┘      └──────────────────┘                    │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────────┐                                               │
│  │ Calculate Error      │                                               │
│  │ (Euclidean distance) │                                               │
│  └────────┬─────────────┘                                               │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────────┐                                               │
│  │ Store Error          │                                               │
│  │ Statistics           │                                               │
│  └────────┬─────────────┘                                               │
│           │                                                              │
│           ▼                                                              │
│     Next Epoch? ──Yes──▶ Loop                                           │
│           │                                                              │
│          No                                                              │
│           │                                                              │
│           ▼                                                              │
│  ┌──────────────────────┐                                               │
│  │ Calculate Final      │                                               │
│  │ Statistics           │                                               │
│  │ • Mean error         │                                               │
│  │ • Std deviation      │                                               │
│  └────────┬─────────────┘                                               │
│           │                                                              │
│           ▼                                                              │
│         End                                                              │
└─────────────────────────────────────────────────────────────────────────┘
```

## State Transition Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     STATE TRANSITION DIAGRAM                             │
│                                                                          │
│  Initial State                                                           │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────┐                                                            │
│  │  Idle   │                                                            │
│  └────┬────┘                                                            │
│       │ Start simulation                                                │
│       ▼                                                                  │
│  ┌──────────────┐                                                       │
│  │ Loading Data │                                                       │
│  └──────┬───────┘                                                       │
│         │                                                                │
│         ▼                                                                │
│  ┌────────────────┐                                                     │
│  │ Processing     │ ◀──┐                                                │
│  │ Epoch          │    │                                                │
│  └────┬───────────┘    │                                                │
│       │                │                                                │
│       │                │ More epochs                                    │
│       ▼                │                                                │
│  ┌────────────────┐    │                                                │
│  │ Epoch < 600?   │───Yes                                               │
│  └────┬───────────┘                                                     │
│       │ No                                                               │
│       ▼                                                                  │
│  ┌────────────────┐                                                     │
│  │ Calculating    │                                                     │
│  │ Statistics     │                                                     │
│  └────┬───────────┘                                                     │
│       │                                                                  │
│       ▼                                                                  │
│  ┌────────────────┐                                                     │
│  │  Complete      │                                                     │
│  │ (Dead marking) │                                                     │
│  └────────────────┘                                                     │
│                                                                          │
│  Total states: 5365                                                     │
│  Total transitions: 6410                                                │
│  Dead markings: 648 (terminal states)                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Performance Comparison Chart

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   MEAN POSITIONING ERROR (meters)                        │
│                                                                          │
│  8m  ┤                                                                   │
│      ┤                                                                   │
│  7m  ┤                     ████                                          │
│      ┤                     ████                                          │
│  6m  ┤           ████      ████      ████                               │
│      ┤           ████      ████      ████                               │
│  5m  ┤     ████  ████      ████      ████                               │
│      ┤     ████  ████      ████      ████                               │
│  4m  ┤     ████  ████      ████      ████                               │
│      ┤     ████  ████      ████      ████                               │
│  3m  ┤     ████  ████      ████      ████                               │
│      ┤     ████  ████      ████      ████                               │
│  2m  ┤     ████  ████      ████      ████                               │
│      ┤ ██  ████  ████  ██  ████  ██  ████                               │
│  1m  ┤ ██  ████  ████  ██  ████  ██  ████                               │
│      ┤ ██  ████  ████  ██  ████  ██  ████                               │
│  0m  └─┴───┴───┴────┴───┴──┴────┴───┴──┴────┴───────────────────────   │
│      Normal AM   FM  Pulse Open Mtn Tunnel                              │
│                                                                          │
│      ◀─ Interference ─▶  ◀─ Environment ─▶                              │
│                                                                          │
│  Key Observations:                                                       │
│  • Normal/Open Area: Best performance (~1m)                              │
│  • FM Interference: Worst signal interference (~6.2m)                    │
│  • Tunnel: Worst environment scenario (~5.7m)                            │
│  • Mountain: Moderate impact (~1.3m)                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Legend and Symbols

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SYMBOL LEGEND                                     │
│                                                                          │
│  Places (Data Stores):                                                   │
│  ┌──────────┐                                                           │
│  │  Place   │  ← Circular/Elliptical nodes storing tokens               │
│  └──────────┘                                                           │
│                                                                          │
│  Transitions (Actions):                                                  │
│  ┌──────────┐                                                           │
│  │Transition│  ← Rectangular nodes representing actions                 │
│  └──────────┘                                                           │
│                                                                          │
│  Arcs (Data Flow):                                                       │
│  ────────▶     ← Directed arrows showing token movement                 │
│                                                                          │
│  Substitution Transitions:                                               │
│  ┌──────────┐                                                           │
│  │  Module  │  ← Double-line box indicating subpage                     │
│  └══════════┘                                                           │
│                                                                          │
│  Color Sets:                                                             │
│  TYPE          ← Data type specification                                │
│                                                                          │
│  Guards:                                                                 │
│  [condition]   ← Boolean condition for transition firing                │
│                                                                          │
│  Code:                                                                   │
│  {function}    ← SML code executed during transition                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Notes

1. All diagrams follow CPN Tools conventions
2. Data flows from left to right, top to bottom
3. Each module is a substitution transition in the actual model
4. Guards and code inscriptions are in Standard ML
5. Time units: 1 unit = 1 second real time
6. Simulation duration: 600 units = 10 minutes
7. Coordinate system: UTM (Universal Transverse Mercator)
8. Results validated against paper Tables 4 and 5
