# GNSS Train Positioning System - Complete Simulation

شبیه‌سازی کامل سیستم موقعیت‌یابی قطار مبتنی بر GNSS با شبکه‌های پتری رنگی و اتوماتون

## Overview / نمای کلی

This repository contains a complete Python implementation of the GNSS-based train positioning system with Colored Petri Nets (CPN) and automaton, based on the paper:

**"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"**  
*High-speed Railway 3 (2025) 175-184*

این مخزن شامل یک پیاده‌سازی کامل پایتون از سیستم موقعیت‌یابی قطار مبتنی بر GNSS با شبکه‌های پتری رنگی و اتوماتون است.

## Features / ویژگی‌ها

✅ **Complete CPN Model Implementation** / پیاده‌سازی کامل مدل CPN
- Hierarchical Petri Net structure / ساختار سلسله‌مراتبی شبکه پتری
- All color sets and variables from Table 1 & 2 / تمام مجموعه‌های رنگی و متغیرها
- State space analysis / تحلیل فضای حالت

✅ **GNSS Signal Generation** / تولید سیگنال GNSS
- Satellite signal simulation / شبیه‌سازی سیگنال ماهواره
- Pseudorange calculations / محاسبات شبه فاصله
- Elevation and azimuth angles / زوایای ارتفاع و سمت

✅ **Signal Interference Models** / مدل‌های تداخل سیگنال
- AM (Amplitude Modulation) interference / تداخل مدولاسیون دامنه
- FM (Frequency Modulation) interference / تداخل مدولاسیون فرکانس  
- Pulse interference / تداخل پالسی

✅ **Environment Scenarios** / سناریوهای محیطی
- Open Area scenario / سناریو منطقه باز
- Mountain occlusion / انسداد کوهستانی
- Tunnel scenario (3 phases: inside, just out, stabilized) / سناریو تونل

✅ **Extended Kalman Filter** / فیلتر کالمن توسعه‌یافته
- Position estimation / تخمین موقعیت
- Prediction and update steps / مراحل پیش‌بینی و به‌روزرسانی
- Covariance matrix management / مدیریت ماتریس کوواریانس

✅ **Automaton State Machine** / ماشین حالت اتوماتون
- State transitions / انتقال‌های حالت
- Event-driven behavior / رفتار رویداد-محور

✅ **Complete Figure Reproduction** / بازتولید کامل اشکال
- All 10 figures from the paper / تمام 10 شکل مقاله
- Petri net diagrams / نمودارهای شبکه پتری
- Performance plots / نمودارهای عملکرد
- Automaton diagrams / نمودارهای اتوماتون

✅ **Performance Analysis Tables** / جداول تحلیل عملکرد
- Table 4: Interference performance / عملکرد تداخل
- Table 5: Environment performance / عملکرد محیطی

## Installation / نصب

```bash
# Clone the repository
git clone https://github.com/benyaminalipoor/gnss-train-positioning-cpn-.git
cd gnss-train-positioning-cpn-

# Install required packages from requirements.txt
pip install -r requirements.txt
```

## Usage / استفاده

```bash
# Run the complete simulation
python3 gnss_train_positioning_simulation.py
```

This will generate all figures and tables from the paper:

### Generated Figures / اشکال تولید شده

1. **figure_1_framework.png** - System modeling framework / چارچوب مدل‌سازی سیستم
2. **figure_2_hierarchy.png** - Hierarchical CPN architecture / معماری سلسله‌مراتبی CPN
3. **figure_3_top_level.png** - Top-level CPN model / مدل CPN سطح بالا
4. **figure_4_gnss_receiver.png** - GNSS Receiver module / ماژول گیرنده GNSS
5. **figure_5_open_area.png** - Open Area submodule / زیرماژول منطقه باز
6. **figure_6_mountain.png** - Mountain submodule / زیرماژول کوهستان
7. **figure_7_tunnel.png** - Tunnel submodule / زیرماژول تونل
8. **figure_8_position_solution.png** - Position Solution module / ماژول حل موقعیت
9. **figure_9_evaluation.png** - Evaluation module / ماژول ارزیابی
10. **figure_10_tunnel_errors.png** - Tunnel scenario errors / خطاهای سناریو تونل

### Additional Visualizations / تجسم‌های اضافی

- **automaton_state_machine.png** - State machine diagram / نمودار ماشین حالت
- **comparison_interference_errors.png** - Interference comparison / مقایسه تداخل‌ها
- **comparison_environment_errors.png** - Environment comparison / مقایسه محیط‌ها
- **table_4_interference_performance.png** - Performance table / جدول عملکرد
- **table_5_environment_performance.png** - Performance table / جدول عملکرد

## Mathematical Models Implemented / مدل‌های ریاضی پیاده‌سازی شده

### 1. GNSS Signal Model / مدل سیگنال GNSS

```python
# Pseudorange calculation
ρ = √[(x_sat - x_recv)² + (y_sat - y_recv)² + (z_sat - z_recv)²] + c·δt + ε
```

Where:
- ρ: Pseudorange / شبه فاصله
- (x_sat, y_sat, z_sat): Satellite position / موقعیت ماهواره
- (x_recv, y_recv, z_recv): Receiver position / موقعیت گیرنده
- δt: Clock bias / خطای ساعت
- ε: Measurement errors / خطاهای اندازه‌گیری

### 2. AM Interference / تداخل AM

```python
I_AM(t) = [1 + m·sin(2πf_e·t)] · sin(2πf_c·t)
```

Where:
- m = 0.5: Modulation depth / عمق مدولاسیون
- f_e = 1 Hz: Envelope frequency / فرکانس پوشش
- f_c = 1575.42 MHz: Carrier frequency / فرکانس حامل

### 3. FM Interference / تداخل FM

```python
I_FM(t) = [sin(2π(f_c + Δf)t) + sin(2π(f_c - Δf)t)] / 2
```

Where:
- Δf ~ N(0, 75 kHz): Frequency deviation / انحراف فرکانس

### 4. Pulse Interference / تداخل پالسی

```python
I_pulse(t) = A · rect((t mod T_p) / T_p)
```

Where:
- A ∈ [1, 5]: Random amplitude / دامنه تصادفی
- T_p: Pulse width / عرض پالس
- T_i: Pulse interval / فاصله پالس

### 5. Extended Kalman Filter / فیلتر کالمن توسعه‌یافته

**State vector:** x = [x, y, z, vx, vy, vz, δt]ᵀ

**Prediction:**
```python
x̂_k|k-1 = F·x̂_k-1|k-1
P_k|k-1 = F·P_k-1|k-1·Fᵀ + Q
```

**Update:**
```python
K_k = P_k|k-1·Hᵀ·(H·P_k|k-1·Hᵀ + R)⁻¹
x̂_k|k = x̂_k|k-1 + K_k·(z_k - h(x̂_k|k-1))
P_k|k = (I - K_k·H)·P_k|k-1
```

### 6. Error Calculation / محاسبه خطا

```python
d = √[(x₂ - x₁)² + (y₂ - y₁)² + (z₂ - z₁)²]
```

Where:
- (x₁, y₁, z₁): Reference position / موقعیت مرجع
- (x₂, y₂, z₂): Calculated position / موقعیت محاسبه شده

## Code Structure / ساختار کد

```
gnss_train_positioning_simulation.py
├── Data Structures (Table 1)
│   ├── Scenario (enum)
│   ├── InterferenceState (enum)
│   ├── TunnelState (enum)
│   ├── Signal (dataclass)
│   ├── Coordinate (dataclass)
│   └── Mountain (dataclass)
├── GNSS Signal Generation
│   └── GNSSSignalGenerator
├── Interference Models
│   └── InterferenceGenerator
│       ├── am_interference()
│       ├── fm_interference()
│       └── pulse_interference()
├── Environment Scenarios
│   └── EnvironmentScenario
│       ├── open_area_scenario()
│       ├── mountain_scenario()
│       └── tunnel_scenario()
├── Extended Kalman Filter
│   └── ExtendedKalmanFilter
│       ├── predict()
│       └── update()
├── Simulation Engine
│   └── GNSSTrainPositioningSimulator
│       ├── simulate_scenario()
│       └── calculate_statistics()
└── Visualization Functions
    ├── create_figure_1_framework()
    ├── create_figure_2_hierarchy()
    ├── create_petri_net_diagram()
    ├── create_figure_10_tunnel_errors()
    ├── create_automaton_diagram()
    └── create_comparison_plots()
```

## Results / نتایج

### Performance Metrics / معیارهای عملکرد

The simulation reproduces all performance metrics from the paper:

#### Signal Interference Impact / تأثیر تداخل سیگنال

| Scenario / سناریو | Mean Error / خطای میانگین | Std Dev / انحراف معیار |
|----------|-----------|---------|
| Normal | ~1.03 m | ~0.06 m |
| AM | ~4.95 m | ~4.08 m |
| FM | ~6.22 m | ~5.26 m |
| Pulse | ~4.79 m | ~3.62 m |

#### Environment Impact / تأثیر محیط

| Scenario / سناریو | Mean Error / خطای میانگین | Std Dev / انحراف معیار |
|----------|-----------|---------|
| Open Area | ~1.03 m | ~0.06 m |
| Mountain | ~1.30 m | ~0.45 m |
| Tunnel | ~5.67 m | ~6.69 m |

## Key Findings / یافته‌های کلیدی

1. **FM interference has the most severe impact** / تداخل FM شدیدترین تأثیر را دارد
2. **Tunnel scenarios show highest positioning errors** / سناریوهای تونل بیشترین خطای موقعیت‌یابی را نشان می‌دهند
3. **Error stabilization occurs after exiting tunnel** / پایدارسازی خطا پس از خروج از تونل رخ می‌دهد
4. **Mountain occlusion affects satellite visibility** / انسداد کوهستانی بر دیده شدن ماهواره تأثیر می‌گذارد

## Petri Net Components / اجزای شبکه پتری

### Places / مکان‌ها
- Input data places / مکان‌های داده ورودی
- Processing state places / مکان‌های حالت پردازش
- Output result places / مکان‌های نتیجه خروجی
- Control places / مکان‌های کنترل

### Transitions / انتقال‌ها
- Signal processing transitions / انتقال‌های پردازش سیگنال
- Scenario selection transitions / انتقال‌های انتخاب سناریو
- Error calculation transitions / انتقال‌های محاسبه خطا
- EKF computation transitions / انتقال‌های محاسبه EKF

### Tokens / نشانه‌ها
- GNSS signal data / داده سیگنال GNSS
- Position estimates / تخمین‌های موقعیت
- Error measurements / اندازه‌گیری خطاها
- Control flags / پرچم‌های کنترل

## Automaton States / حالت‌های اتوماتون

1. **Initial** - System initialization / مقداردهی اولیه سیستم
2. **Receiving Signals** - GNSS signal reception / دریافت سیگنال GNSS
3. **Processing** - Signal processing / پردازش سیگنال
4. **Open Area** - Open area processing / پردازش منطقه باز
5. **Mountain** - Mountain scenario processing / پردازش سناریو کوهستان
6. **Tunnel** - Tunnel scenario processing / پردازش سناریو تونل
7. **Position Solution** - EKF position calculation / محاسبه موقعیت EKF

## Paper Reference / مرجع مقاله

```
Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang
"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"
High-speed Railway, Volume 3, 2025, Pages 175-184
https://doi.org/10.1016/j.hspr.2025.05.001
```

## Authors / نویسندگان

Implementation by: GitHub Copilot Agent  
Based on paper by: Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang  
Beijing Jiaotong University

## License / مجوز

This implementation is for educational and research purposes.  
این پیاده‌سازی برای اهداف آموزشی و تحقیقاتی است.

## Requirements / نیازمندی‌ها

- Python 3.8+
- NumPy 1.20+
- Matplotlib 3.3+
- Pandas 1.2+

## Contact / تماس

For questions or issues, please open an issue on GitHub.  
برای سؤالات یا مشکلات، لطفاً یک issue در GitHub باز کنید.
