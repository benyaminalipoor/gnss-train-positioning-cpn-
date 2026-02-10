# gnss-train-positioning-cpn-

Simulation of GNSS-based train positioning with Colored Petri Nets

## Overview

This repository contains a complete MATLAB/Octave implementation of the research paper:

**"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**  
by Shuting Chen, Daohua Wu, Jiang Liu, and Siqi Wang  
Published in High-speed Railway 3 (2025) 175–184

## Quick Start

Run the complete simulation in MATLAB or Octave:

```matlab
gnss_cpn_simulation()
```

This will generate all 10 figures from the paper plus performance analysis tables.

## Features

✅ Complete CPN model implementation with hierarchical structure  
✅ All 10 figures from the paper accurately reproduced  
✅ EKF-based position estimation algorithm  
✅ 4 interference types: Normal, AM, FM, Pulse  
✅ 3 environment scenarios: Open Area, Mountain, Tunnel  
✅ Performance metrics and analysis tables  
✅ Compatible with MATLAB and Octave  

## Generated Outputs

### CPN Model Diagrams (Figures 1-9)
- Figure 1: Modeling framework
- Figure 2: Hierarchical architecture
- Figure 3: Top-level CPN model
- Figure 4: GNSS Receiver module
- Figure 5: Open Area submodule
- Figure 6: Mountain submodule
- Figure 7: Tunnel submodule
- Figure 8: Position Solution (EKF)
- Figure 9: Evaluation module

### Simulation Results
- Figure 10: Position errors in tunnel scenario
- Table 4: Performance under different signal interferences
- Table 5: Performance under different environment scenarios

## Key Results

### Signal Interference Impact (Table 4)
| Scenario | Mean Error (m) | Std Dev (m) |
|----------|----------------|-------------|
| Normal   | 1.05           | 0.45        |
| AM       | 3.79           | 1.70        |
| FM       | 3.94           | 1.78        |
| Pulse    | 3.28           | 1.34        |

### Environment Scenario Impact (Table 5)
| Scenario   | Mean Error (m) | Std Dev (m) |
|------------|----------------|-------------|
| Open Area  | 1.06           | 0.48        |
| Mountain   | 1.82           | 1.03        |
| Tunnel     | 6.60           | 9.86        |

## Documentation

See [README_SIMULATION.md](README_SIMULATION.md) for detailed documentation including:
- Installation requirements
- Usage instructions
- Implementation details
- Customization guide
- Validation results

## Files

- `gnss_cpn_simulation.m` - Main simulation script
- `Petrii.PDF` - Original research paper
- `README_SIMULATION.md` - Detailed documentation
- Generated figures and tables (PNG and MAT files)

## Requirements

- MATLAB R2019a or later, OR
- GNU Octave 6.0 or later (free, open-source)
- No additional toolboxes required

## Citation

If you use this simulation, please cite the original paper:

```bibtex
@article{chen2025modeling,
  title={Modeling and performance analysis of GNSS-based train positioning system with colored petri nets},
  author={Chen, Shuting and Wu, Daohua and Liu, Jiang and Wang, Siqi},
  journal={High-speed Railway},
  volume={3},
  pages={175--184},
  year={2025},
  publisher={Elsevier}
}
```

## License

This implementation is provided for research and educational purposes.

