# GNSS Train Positioning with Colored Petri Nets

## شبیه‌سازی موقعیت‌یابی قطار با GNSS و شبکه پتری رنگی

Complete MATLAB simulation of GNSS-based train positioning system using Colored Petri Nets (CPN) and Automaton.

**شبیه‌سازی کامل سیستم موقعیت‌یابی قطار مبتنی بر GNSS با استفاده از شبکه‌های پتری رنگی و اتوماتون در متلب.**

---

## 🚀 Quick Start / شروع سریع

### English
Run the complete simulation in MATLAB:
```matlab
gnss_train_positioning_complete_simulation
```

📖 **[Full Documentation in English](README_SIMULATION.md)**

### فارسی
اجرای شبیه‌سازی کامل در متلب:
```matlab
gnss_train_positioning_complete_simulation
```

📖 **[مستندات کامل به فارسی](README_FA.md)**

---

## 📋 What's Included / محتویات

This repository contains a complete implementation of the paper:

**"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**  
*Published in: High-speed Railway 3 (2025) 175–184*

### Features / ویژگی‌ها

✅ **Colored Petri Net (CPN)** simulation model  
✅ **Automaton** for environment scenarios (Open Area, Mountain, Tunnel)  
✅ **Signal Interference** models (AM, FM, Pulse)  
✅ **Extended Kalman Filter (EKF)** implementation  
✅ **8 Figures** matching the paper  
✅ **Tables 4 & 5** performance metrics  
✅ **Complete documentation** in English and Persian  

---

## 📊 Generated Outputs / خروجی‌ها

The simulation generates:
- 8 PNG figures (including Figure 10 - main result)
- Tables 4 and 5 with performance statistics
- MATLAB data file with all results
- Complete console output with progress

شبیه‌سازی تولید می‌کند:
- 8 شکل PNG (شامل شکل 10 - نتیجه اصلی)
- جداول 4 و 5 با آمار عملکرد
- فایل داده متلب با تمام نتایج
- خروجی کامل کنسول با پیشرفت کار

---

## 📄 Files / فایل‌ها

| File | Description |
|------|-------------|
| `gnss_train_positioning_complete_simulation.m` | Main simulation script (754 lines) |
| `test_simulation.m` | Quick validation script |
| `README_SIMULATION.md` | Full documentation (English) |
| `README_FA.md` | مستندات کامل (فارسی) |
| `Petrii.PDF` | Original research paper |

---

## 🔬 Technical Details / جزئیات فنی

### Implementation / پیاده‌سازی

- **Petri Net Places**: GNSS_Signal, Scenario, GNSS_Observation, Position, Delta_Position
- **Petri Net Transitions**: Choose Scenario, Process Interference, EKF Update, Calculate Error
- **Automaton States**: OpenArea, Mountain, InsideTunnel, JustOut, Stabilized
- **Interference Types**: AM (Amplitude Modulation), FM (Frequency Modulation), Pulse
- **Positioning Algorithm**: Extended Kalman Filter (6-state: position + velocity)

---

## 🎯 Key Results / نتایج کلیدی

From the paper simulation:

| Scenario | Mean Error | Std Deviation |
|----------|------------|---------------|
| Normal   | ~1.03 m    | ~0.06 m       |
| AM Interference | ~4.95 m | ~4.08 m |
| FM Interference | ~6.22 m | ~5.26 m |
| Pulse Interference | ~4.79 m | ~3.62 m |
| Open Area | ~1.03 m | ~0.06 m |
| Mountain | ~1.30 m | ~0.45 m |
| Tunnel | ~5.67 m | ~6.69 m |

---

## 📚 Reference / مرجع

**Chen, S., Wu, D., Liu, J., & Wang, S. (2025).** Modeling and performance analysis of GNSS-based train positioning system with colored petri nets. *High-speed Railway*, 3, 175-184.

---

## 💻 Requirements / نیازمندی‌ها

- MATLAB R2016b or later / متلب نسخه R2016b یا بالاتر
- Or GNU Octave 5.0+ / یا GNU Octave نسخه 5.0+
- No additional toolboxes required / بدون نیاز به جعبه ابزار اضافی

---

## ⏱️ Runtime / زمان اجرا

- Simulation duration: 10-30 seconds
- Output: 8 PNG files + 2 tables + 1 MAT file

---

## 🤝 Support / پشتیبانی

For questions or issues:
- See detailed documentation: [README_SIMULATION.md](README_SIMULATION.md)
- See Persian guide: [README_FA.md](README_FA.md)
- Run test script: `test_simulation.m`

---

**Note:** This is a complete, self-contained implementation. All features described in the paper are implemented in a single MATLAB script.

**توجه:** این یک پیاده‌سازی کامل و مستقل است. تمام ویژگی‌های توضیح داده شده در مقاله در یک اسکریپت متلب پیاده‌سازی شده‌اند.
