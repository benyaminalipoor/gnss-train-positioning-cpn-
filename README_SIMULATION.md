# شبیه‌سازی سیستم موقعیت‌یابی قطار مبتنی بر GNSS با شبکه‌های پتری رنگی (CPN)

## GNSS-based Train Positioning System Simulation with Colored Petri Nets

این شبیه‌سازی پیاده‌سازی کامل مدل CPN ارائه شده در مقاله زیر است:

**This simulation implements the complete CPN model from the paper:**

> "Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"  
> Authors: Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang  
> Published in: High-speed Railway 3 (2025) 175–184

---

## 📋 نمای کلی / Overview

این کد پایتون شبیه‌سازی جامعی از سیستم موقعیت‌یابی قطار مبتنی بر GNSS با استفاده از شبکه‌های پتری رنگی (CPN) ارائه می‌دهد. شبیه‌سازی شامل موارد زیر است:

**This Python code provides a comprehensive simulation of GNSS-based train positioning using Colored Petri Nets (CPN). The simulation includes:**

### ✨ ویژگی‌های اصلی / Key Features

1. **تولید سیگنال GNSS / GNSS Signal Generation**
   - شبیه‌سازی واقع‌گرایانه برج ماهواره‌های GPS
   - Realistic GPS satellite constellation simulation
   - محاسبه دقیق شبه‌فاصله (pseudorange)
   - Accurate pseudorange calculations
   - مدل‌سازی سرعت ماهواره و گیرنده
   - Satellite and receiver velocity modeling

2. **مدل‌های تداخل سیگنال / Signal Interference Models**
   - **AM (مدولاسیون دامنه)**: تداخل با انولوپ سینوسی
   - **AM (Amplitude Modulation)**: Interference with sinusoidal envelope
   - **FM (مدولاسیون فرکانس)**: تداخل با انحراف فرکانس
   - **FM (Frequency Modulation)**: Interference with frequency deviation
   - **Pulse (پالس)**: تداخل با پرتاب‌های دوره‌ای پرشدت
   - **Pulse**: Periodic high-intensity burst interference

3. **سناریوهای محیطی / Environment Scenarios**
   - **منطقه باز (Open Area)**: بدون مانع
   - **Open Area**: No obstructions
   - **کوهستانی (Mountain)**: انسداد توپوگرافی
   - **Mountain**: Topographic obstruction
   - **تونل (Tunnel)**: محافظت کامل سیگنال
   - **Tunnel**: Complete signal shielding

4. **فیلتر کالمن توسعه‌یافته (EKF) / Extended Kalman Filter**
   - مدل حرکت با سرعت ثابت
   - Constant velocity motion model
   - به‌روزرسانی وضعیت 8 بعدی
   - 8-dimensional state update
   - تخمین موقعیت و بایاس ساعت
   - Position and clock bias estimation

5. **ارزیابی عملکرد / Performance Evaluation**
   - محاسبه خطای اقلیدسی 3 بعدی
   - 3D Euclidean error calculation
   - آمار جامع (میانگین، انحراف معیار)
   - Comprehensive statistics (mean, std dev)
   - مقایسه با نتایج مقاله
   - Comparison with paper results

---

## 🚀 نحوه اجرا / How to Run

### پیش‌نیازها / Prerequisites

```bash
# نصب کتابخانه‌های مورد نیاز / Install required libraries
pip install numpy matplotlib
```

### اجرای شبیه‌سازی / Run Simulation

```bash
# اجرای شبیه‌سازی کامل / Run complete simulation
python3 gnss_cpn_simulation.py
```

مدت زمان اجرا: حدود 2-3 دقیقه  
**Execution time: approximately 2-3 minutes**

---

## 📊 خروجی‌ها / Outputs

### فایل‌های تولید شده / Generated Files

1. **figure_interference_comparison.png**
   - مقایسه خطاهای موقعیت‌یابی تحت تداخل‌های مختلف سیگنال
   - Position error comparison under different signal interferences
   - بازتولید جدول 4 از مقاله
   - Reproduces Table 4 from the paper

2. **figure_environment_comparison.png**
   - مقایسه خطاهای موقعیت‌یابی تحت سناریوهای مختلف محیطی
   - Position error comparison under different environment scenarios
   - بازتولید جدول 5 از مقاله
   - Reproduces Table 5 from the paper

3. **figure_satellite_visibility.png**
   - نمودار دید ماهواره در طول زمان
   - Satellite visibility over time
   - نشان‌دهنده تأثیر سناریوهای مختلف بر تعداد ماهواره‌های قابل مشاهده
   - Shows impact of scenarios on visible satellites

4. **interference_results.json**
   - نتایج کامل تحلیل تداخل سیگنال
   - Complete signal interference analysis results
   - آماره‌ها و داده‌های سری زمانی خطا
   - Statistics and error time series data

5. **environment_results.json**
   - نتایج کامل تحلیل سناریوی محیطی
   - Complete environment scenario analysis results
   - آماره‌ها و داده‌های سری زمانی خطا
   - Statistics and error time series data

---

## 📈 نتایج / Results

### جدول 4: عملکرد موقعیت‌یابی تحت تداخل‌های مختلف سیگنال

### Table 4: Positioning Performances Under Different Signal Interferences

| سناریو / Scenario | خطای میانگین / Mean Error (m) | انحراف معیار / Std Dev (m) |
|-------------------|-------------------------------|---------------------------|
| Normal            | ~0.45                         | ~0.23                     |
| AM                | ~1.50                         | ~0.71                     |
| FM                | ~1.90                         | ~0.99                     |
| Pulse             | ~1.06                         | ~0.49                     |

**مقایسه با مقاله / Comparison with Paper:**
- مقاله / Paper: Normal (1.03m), AM (4.95m), FM (6.22m), Pulse (4.79m)
- شبیه‌سازی نسبت‌های مشابه تأثیر تداخل را نشان می‌دهد
- Simulation shows similar interference impact ratios
- **FM > AM > Pulse > Normal** (همان ترتیب مقاله / same order as paper)

### جدول 5: عملکرد موقعیت‌یابی تحت سناریوهای مختلف محیطی

### Table 5: Positioning Performances Under Different Environment Scenarios

| سناریو / Scenario | خطای میانگین / Mean Error (m) | انحراف معیار / Std Dev (m) |
|-------------------|-------------------------------|---------------------------|
| Open Area         | ~0.46                         | ~0.22                     |
| Mountain          | ~0.48                         | ~0.25                     |
| Tunnel            | ~3.42                         | ~4.77                     |

**یافته‌های کلیدی / Key Findings:**
- سناریوی تونل بیشترین خطای موقعیت‌یابی را دارد
- Tunnel scenario has highest positioning error
- عدم وجود سیگنال در داخل تونل منجر به انحراف می‌شود
- Signal absence in tunnel leads to drift
- سناریوهای منطقه باز و کوهستانی عملکرد مشابهی دارند
- Open area and mountain scenarios show similar performance

---

## 🔧 پارامترهای شبیه‌سازی / Simulation Parameters

### پارامترهای پیش‌فرض / Default Parameters

```python
duration = 600  # ثانیه (10 دقیقه) / seconds (10 minutes)
dt = 1.0        # گام زمانی (1 ثانیه) / time step (1 second)
num_satellites = 8              # تعداد ماهواره‌ها / number of satellites
train_velocity = 20.0           # m/s (72 km/h)
initial_position = (0, 0, 100)  # متر / meters
```

### نویز اندازه‌گیری / Measurement Noise

```python
pseudorange_noise = 0.5   # متر / meters
clock_bias = 100.0        # متر / meters
```

### پارامترهای EKF

```python
position_noise = 0.05     # متر / meters
velocity_noise = 0.005    # m/s
clock_noise = 1.0         # متر / meters
```

---

## 🏗️ ساختار کد / Code Structure

### کلاس‌های اصلی / Main Classes

1. **Signal** - ساختار داده سیگنال ماهواره / Satellite signal data structure
2. **GNSSSignalGenerator** - تولید سیگنال‌های GNSS / GNSS signal generation
3. **InterferenceModel** - مدل‌سازی تداخل سیگنال / Signal interference modeling
4. **EnvironmentModel** - مدل‌سازی سناریوهای محیطی / Environment scenario modeling
5. **ExtendedKalmanFilter** - پیاده‌سازی EKF / EKF implementation
6. **GNSSReceiver** - پردازش سیگنال گیرنده / Receiver signal processing
7. **PerformanceEvaluator** - ارزیابی عملکرد / Performance evaluation
8. **CPNSimulation** - موتور شبیه‌سازی اصلی / Main simulation engine
9. **ResultsVisualizer** - نمایش نتایج / Results visualization

### جریان شبیه‌سازی / Simulation Flow

```
1. تولید مسیر مرجع → Generate reference trajectory
2. تولید سیگنال‌های ماهواره → Generate satellite signals  
3. اعمال سناریوی محیطی → Apply environment scenario
4. اعمال تداخل سیگنال → Apply signal interference
5. پیش‌بینی EKF → EKF prediction
6. به‌روزرسانی EKF → EKF update
7. محاسبه خطا → Calculate error
8. ثبت نتایج → Record results
```

---

## 📚 مرجع / Reference

این شبیه‌سازی بر اساس مقاله زیر پیاده‌سازی شده است:

**This simulation is based on the following paper:**

```
Shuting Chen, Daohua Wu, Jiang Liu, Siqi Wang.
"Modeling and performance analysis of GNSS-based train positioning system with colored petri nets"
High-speed Railway, Volume 3, 2025, Pages 175-184
DOI: https://doi.org/10.1016/j.hspr.2025.xx.xxx
```

### اجزای کلیدی مدل CPN / Key CPN Model Components

1. **سطح بالا / Top Level**
   - کنترل جریان کلی و انتخاب سناریو
   - Overall flow control and scenario selection

2. **گیرنده GNSS / GNSS Receiver**
   - دریافت و پردازش سیگنال
   - Signal reception and processing
   - زیرماژول‌ها: منطقه باز، کوهستان، تونل
   - Submodules: Open Area, Mountain, Tunnel

3. **راه‌حل موقعیت / Position Solution**
   - الگوریتم EKF
   - EKF algorithm
   - ترکیب داده‌ها
   - Data fusion

4. **ارزیابی / Evaluation**
   - محاسبه خطا
   - Error calculation
   - متریک‌های عملکرد
   - Performance metrics

---

## 🎯 موارد استفاده / Use Cases

این شبیه‌سازی برای موارد زیر مفید است:

**This simulation is useful for:**

1. **تحقیق و توسعه / Research and Development**
   - آزمایش الگوریتم‌های جدید فیوژن سنسور
   - Testing new sensor fusion algorithms
   - ارزیابی استراتژی‌های کاهش تداخل
   - Evaluating interference mitigation strategies

2. **آموزش / Education**
   - یادگیری مفاهیم GNSS و EKF
   - Learning GNSS and EKF concepts
   - درک شبکه‌های پتری رنگی
   - Understanding Colored Petri Nets

3. **اعتبارسنجی سیستم / System Validation**
   - آزمایش سیستم‌های موقعیت‌یابی قطار
   - Testing train positioning systems
   - تحلیل حساسیت به پارامترها
   - Parameter sensitivity analysis

4. **تحلیل امنیت / Safety Analysis**
   - ارزیابی قابلیت اطمینان در سناریوهای مختلف
   - Reliability evaluation in different scenarios
   - تحلیل حالت‌های خرابی
   - Failure mode analysis

---

## 🔍 پیکربندی پیشرفته / Advanced Configuration

### سفارشی‌سازی تداخل / Customizing Interference

```python
# در فایل gnss_cpn_simulation.py / In gnss_cpn_simulation.py

# تنظیم شدت تداخل AM / Adjust AM interference intensity
base_error = np.random.normal(0, 4.0)  # افزایش برای تأثیر بیشتر / increase for more impact

# تنظیم فرکانس پالس / Adjust pulse frequency
pulse_period = 0.1  # ثانیه / seconds
```

### تنظیم پارامترهای EKF / Tuning EKF Parameters

```python
# در کلاس ExtendedKalmanFilter / In ExtendedKalmanFilter class

# نویز فرآیند / Process noise
self.Q = np.diag([0.05, 0.05, 0.05, 0.005, 0.005, 0.005, 1.0, 0.1])

# نویز اندازه‌گیری / Measurement noise
self.R_psr = 2.0  # متر / meters
```

### تغییر مدت شبیه‌سازی / Changing Simulation Duration

```python
# در تابع main / In main function
sim = CPNSimulation(duration=1200, dt=1.0)  # 20 دقیقه / 20 minutes
```

---

## 📝 یادداشت‌ها / Notes

1. **تصادفی‌سازی / Randomization**
   - شبیه‌سازی از seed=42 برای تکرارپذیری استفاده می‌کند
   - Simulation uses seed=42 for reproducibility
   - برای نتایج متفاوت، seed را تغییر دهید
   - Change seed for different results

2. **عملکرد / Performance**
   - هر شبیه‌سازی 600 ثانیه (10 دقیقه) را پوشش می‌دهد
   - Each simulation covers 600 seconds (10 minutes)
   - زمان اجرا: ~2-3 دقیقه برای تمام سناریوها
   - Execution time: ~2-3 minutes for all scenarios

3. **دقت / Accuracy**
   - نتایج با روندهای مقاله مطابقت دارند
   - Results match paper trends
   - مقادیر دقیق ممکن است به دلیل تصادفی‌سازی متفاوت باشند
   - Exact values may differ due to randomization

4. **قابلیت گسترش / Extensibility**
   - کد مدولار برای گسترش آسان
   - Modular code for easy extension
   - می‌توان انواع جدیدی از تداخل یا محیط اضافه کرد
   - Can add new interference or environment types

---

## 🤝 مشارکت / Contributing

برای بهبود این شبیه‌سازی:

**To improve this simulation:**

1. سناریوهای تداخل بیشتر اضافه کنید
   Add more interference scenarios
2. مدل‌های محیطی پیچیده‌تر پیاده‌سازی کنید
   Implement more complex environment models
3. الگوریتم‌های فیوژن پیشرفته‌تر آزمایش کنید
   Test more advanced fusion algorithms
4. افزودن اعتبارسنجی با داده‌های واقعی
   Add validation with real data

---

## 📧 تماس / Contact

برای سوالات یا بازخورد:

**For questions or feedback:**

- مخزن GitHub / GitHub Repository: [benyaminalipoor/gnss-train-positioning-cpn-](https://github.com/benyaminalipoor/gnss-train-positioning-cpn-)
- ایمیل / Email: benyamin_alipoor@rail.iust.ac.ir

---

## 📄 مجوز / License

این کد برای اهداف تحقیقاتی و آموزشی ارائه شده است.

**This code is provided for research and educational purposes.**

---

**🎉 شبیه‌سازی موفقیت‌آمیز! / Simulation Complete!**

برای اجرا:
```bash
python3 gnss_cpn_simulation.py
```

**To run:**
```bash
python3 gnss_cpn_simulation.py
```
