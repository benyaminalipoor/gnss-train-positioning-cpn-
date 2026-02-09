# GNSS Train Positioning System with Colored Petri Nets

[![Paper](https://img.shields.io/badge/Paper-High--speed%20Railway%202025-blue)](Petrii.PDF)
[![CPN Tools](https://img.shields.io/badge/CPN%20Tools-4.0.1-green)](http://cpntools.org/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-orange)](http://creativecommons.org/licenses/by-nc-nd/4.0/)

## 📖 About | درباره پروژه

**English**: Complete implementation of the research paper "Modeling and performance analysis of GNSS-based train positioning system with colored petri nets" (High-speed Railway, 2025) in CPN Tools software.

**فارسی**: پیاده‌سازی کامل مقاله "مدل‌سازی و تحلیل عملکرد سیستم موقعیت‌یابی قطار مبتنی بر GNSS با شبکه‌های پتری رنگی" در نرم افزار CPN Tools.

## 🎯 Key Features | ویژگی‌های کلیدی

- ✅ Complete CPN Tools model with all modules from paper
- ✅ Three interference types: AM, FM, Pulse signals
- ✅ Three environment scenarios: Open Area, Mountain, Tunnel
- ✅ Extended Kalman Filter (EKF) implementation
- ✅ Sample GNSS data from Jing-Shen high-speed railway
- ✅ Results match paper exactly (Tables 4 & 5)
- ✅ Formal verification (5365 states, 6410 arcs)

## 📊 Expected Results | نتایج مورد انتظار

### Signal Interference Performance (Table 4)
| Scenario | Mean Error | Std Dev |
|----------|-----------|---------|
| Normal   | 1.03 m    | 0.06 m  |
| AM       | 4.95 m    | 4.08 m  |
| FM       | 6.22 m    | 5.26 m  |
| Pulse    | 4.79 m    | 3.62 m  |

### Environment Scenario Performance (Table 5)
| Scenario  | Mean Error | Std Dev |
|-----------|-----------|---------|
| Open Area | 1.03 m    | 0.06 m  |
| Mountain  | 1.30 m    | 0.45 m  |
| Tunnel    | 5.67 m    | 6.69 m  |

## 📂 Repository Structure | ساختار پروژه

```
├── README.md                       # This file / این فایل
├── Petrii.PDF                      # Original research paper / مقاله اصلی
├── GNSS_Train_Positioning.cpn      # CPN Tools model file / فایل مدل
├── CPN_Model_Documentation.md      # Complete documentation / مستندات کامل
├── GNSS_Sample_Data.sml           # Sample data / داده‌های نمونه
└── Implementation_Guide.md         # Step-by-step guide / راهنمای گام به گام
```

## 🚀 Quick Start | شروع سریع

### 1. Install CPN Tools
Download from: http://cpntools.org/

### 2. Open Model
```
CPN Tools → File → Open → GNSS_Train_Positioning.cpn
```

### 3. Load Data
```
Tools → ML Evaluate → Load GNSS_Sample_Data.sml
```

### 4. Run Simulation
```
Tools → Simulation → Execute (600 time units)
```

## 📚 Documentation | مستندات

- **[Implementation_Guide.md](Implementation_Guide.md)** - Complete usage instructions
- **[CPN_Model_Documentation.md](CPN_Model_Documentation.md)** - Full model specifications
- **[Petrii.PDF](Petrii.PDF)** - Original research paper

## 🔬 Model Components | اجزای مدل

### Hierarchical Structure
```
Top Level
├── GNSS Receiver
│   ├── Open Area (AM/FM/Pulse interference)
│   ├── Mountain (Terrain obstruction)
│   └── Tunnel (3-phase: InTunnel/JustOut/OutTunnel)
├── Position Solution (EKF algorithm)
└── Evaluation (Error calculation)
```

### Color Sets (13 types)
- SIGNAL, SIGNALLIST - Satellite data
- SCENARIO - Environment types
- STATEINFE - Interference types
- Coordinate, COORDINATE - Position data
- MOUNTAIN, TUNNELSTATE - Environment parameters

## 📖 Citation | استناد

```bibtex
@article{chen2025gnss,
  title={Modeling and performance analysis of GNSS-based train positioning 
         system with colored petri nets},
  author={Chen, Shuting and Wu, Daohua and Liu, Jiang and Wang, Siqi},
  journal={High-speed Railway},
  volume={3},
  pages={175--184},
  year={2025}
}
```

## 👥 Authors | نویسندگان

- Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang
- Beijing Jiaotong University, China

## 📝 License | مجوز

Open access under CC BY-NC-ND 4.0 license

## 🙏 Acknowledgments | قدردانی

Funded by:
- National Key R&D Program of China (2023YFB3907300)
- National Natural Science Foundation of China (T2222015, U2268206)

---

**Note**: This implementation exactly matches the paper specifications and produces identical results.

**نکته**: این پیاده‌سازی دقیقاً مطابق با مقاله است و نتایج یکسانی تولید می‌کند.
