# GNSS Train Positioning with Colored Petri Nets

Simulation of GNSS-based train positioning with Colored Petri Nets and Extended Kalman Filter

## 🎯 Overview

This repository contains a complete Colored Petri Net (CPN) model for simulating GNSS-based train positioning with Extended Kalman Filter (EKF). The model implements all scenarios from the research paper including different environmental conditions and interference types.

## 📁 Main Files

- **`GNSS_Train_Positioning.cpn`** - Complete CPN model (CPN Tools 4.0.1+)
- **`CPN_USER_GUIDE.md`** - Comprehensive user guide
- **`IMPLEMENTATION_README.md`** - Complete documentation
- **`COMPLETION_SUMMARY.md`** - Implementation summary
- **`validate_cpn.py`** - Validation script
- **`Petrii.PDF`** - Research paper

## ✨ Features

✅ 4 hierarchical pages (Top Level, GNSS Receiver, Position Solution, Evaluation)
✅ 12 simulation scenarios (3 environments × 4 interference types)
✅ Complete Extended Kalman Filter algorithm
✅ 26 helper functions including matrix operations
✅ Comprehensive error analysis and RMSE calculation
✅ Validated structure - passes all checks

## 🚀 Quick Start

1. Install CPN Tools 4.0.1 or later
2. Open `GNSS_Train_Positioning.cpn`
3. Create simulator and run
4. See `CPN_USER_GUIDE.md` for details

## 📊 Scenarios

| ID | Environment | Interference | Description |
|----|-------------|--------------|-------------|
| 1-4 | OpenArea | Normal/AM/FM/Pulse | Best conditions |
| 5-8 | Mountain | Normal/AM/FM/Pulse | Mountainous terrain |
| 9-12 | Tunnel | Normal/AM/FM/Pulse | Urban canyon/tunnel |

## 📖 Documentation

- **CPN_USER_GUIDE.md** - How to use the model
- **IMPLEMENTATION_README.md** - Technical details
- **COMPLETION_SUMMARY.md** - Project completion status

## ✅ Status

**COMPLETE** - Ready to use for education and research
