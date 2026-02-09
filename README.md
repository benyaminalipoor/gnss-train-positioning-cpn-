# GNSS Train Positioning with Colored Petri Nets

Simulation of GNSS-based train positioning system using Colored Petri Nets (CPN) with Extended Kalman Filter (EKF) for accurate position estimation under various interference and environmental conditions.

## 📋 Overview

This repository contains a complete CPN Tools model implementing the GNSS train positioning system described in **Petrii.PDF**. The model includes:

- **Signal Processing**: GNSS signal reception and processing
- **Interference Modeling**: AM/FM/Pulse interference simulation
- **Environmental Effects**: Mountain shadowing and tunnel signal loss
- **Extended Kalman Filter**: Position estimation with prediction and update steps
- **Performance Evaluation**: Mean/Max/RMS error calculation and success rate analysis

## 🚀 Quick Start

1. **Open the model**: `GNSS_Train_Positioning.cpn` in CPN Tools 4.0.1+
2. **Initialize**: Tools → Simulator → Init
3. **Run**: Tools → Simulator → Step (F7)
4. **View results**: Check the Results place for evaluation metrics

For detailed instructions, see [QUICK_START.md](QUICK_START.md)

## 📁 Files

| File | Description |
|------|-------------|
| **GNSS_Train_Positioning.cpn** | Main CPN model (39 KB) |
| **GNSS_Sample_Data.sml** | Test data and scenarios (3.5 KB) |
| **Petrii.PDF** | Original research paper |
| **QUICK_START.md** | Quick start guide |
| **CPN_MODEL_GUIDE.md** | Complete user guide |
| **VALIDATION_REPORT.md** | Technical validation |
| **PAPER_VERIFICATION.md** | Paper compliance verification |

## ✨ Features

- ✅ 4 hierarchical pages (modular design)
- ✅ 22 color sets (signals, positions, states, scenarios)
- ✅ 29+ variables (fully typed)
- ✅ 18 ML functions (interference, EKF, evaluation)
- ✅ DTD format 6 compliant
- ✅ All IDs unique
- ✅ Proper XML escaping
- ✅ Initial marking configured
- ✅ Validated and tested

## 📊 Expected Performance

| Scenario | Mean Error | Max Error | RMS Error | Success Rate |
|----------|-----------|-----------|-----------|--------------|
| Urban | < 3m | < 5m | < 3.5m | > 90% |
| Tunnel | < 10m | < 15m | < 11m | > 70% |
| Mountain | < 8m | < 12m | < 8m | > 80% |
| Combined | < 12m | < 20m | < 13m | > 65% |

## 🛠️ Requirements

- **CPN Tools** 4.0.1 or later
- **Standard ML** compiler (included with CPN Tools)

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[CPN_MODEL_GUIDE.md](CPN_MODEL_GUIDE.md)** - Complete user guide
- **[VALIDATION_REPORT.md](VALIDATION_REPORT.md)** - Technical validation
- **[PAPER_VERIFICATION.md](PAPER_VERIFICATION.md)** - Paper compliance

## 🎯 Model Structure

```
Top Level (Main Flow)
├── GNSS Receiver (Signal Processing)
│   ├── Raw Signals → Interference Models → Processed Signals
│   └── AM/FM/Pulse Interference
├── Position Solution (EKF)
│   ├── Prediction Step (Motion Model)
│   └── Update Step (Kalman Filter)
└── Evaluation (Performance Analysis)
    └── Mean/Max/RMS Error, Success Rate
```

## 🔬 Algorithms Implemented

1. **AM Interference**: Amplitude modulation with SNR degradation
2. **FM Interference**: Frequency modulation with phase shift
3. **Pulse Interference**: Pulsed jamming simulation
4. **Mountain Filtering**: Signal shadowing by terrain
5. **Tunnel Error**: Signal loss in enclosed spaces
6. **EKF Prediction**: Motion model with velocity/acceleration
7. **EKF Update**: Kalman gain and innovation calculation
8. **Position Calculation**: Trilateration from multiple signals
9. **Error Metrics**: Statistical performance analysis

## ✅ Validation Status

- ✅ XML well-formed and DTD compliant
- ✅ Parses without errors in CPN Tools
- ✅ All transitions have valid ML code
- ✅ All arcs have proper inscriptions
- ✅ Initial marking configured correctly
- ✅ Covers all sections from Petrii.PDF paper
- ✅ Ready for simulation and validation

## 🤝 Contributing

This is an academic implementation based on the research paper. For improvements or bug reports, please refer to the documentation.

## 📄 License

As per repository license terms.

## 📚 References

- Research paper: Petrii.PDF (included)
- CPN Tools: http://cpntools.org
- Standard ML: https://www.standardml.org

---

**Status**: ✅ Complete and Validated  
**Version**: 1.0  
**Date**: 2026-02-09
