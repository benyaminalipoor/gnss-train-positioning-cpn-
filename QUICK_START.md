# Quick Reference Guide - GNSS Train Positioning Simulation
# راهنمای سریع - شبیه‌سازی موقعیت‌یابی قطار با GNSS

## FOR ENGLISH USERS

### Step 1: Open MATLAB
- Launch MATLAB on your computer

### Step 2: Set Directory
```matlab
cd 'path/to/gnss-train-positioning-cpn-'
```

### Step 3: Run Simulation
```matlab
gnss_train_positioning_complete_simulation
```

### Expected Output:
- Runtime: 10-30 seconds
- 8 PNG figure files
- 2 tables in console
- 1 MAT file with results

### Troubleshooting:
If you encounter errors, run the test first:
```matlab
test_simulation
```

---

## برای کاربران فارسی‌زبان

### گام 1: باز کردن متلب
- متلب را در رایانه خود اجرا کنید

### گام 2: تنظیم پوشه
```matlab
cd 'مسیر/به/gnss-train-positioning-cpn-'
```

### گام 3: اجرای شبیه‌سازی
```matlab
gnss_train_positioning_complete_simulation
```

### خروجی مورد انتظار:
- زمان اجرا: 10-30 ثانیه
- 8 فایل تصویر PNG
- 2 جدول در کنسول
- 1 فایل MAT با نتایج

### عیب‌یابی:
در صورت بروز خطا، ابتدا تست را اجرا کنید:
```matlab
test_simulation
```

---

## Key Files / فایل‌های کلیدی

| File | Purpose |
|------|---------|
| `gnss_train_positioning_complete_simulation.m` | Main simulation |
| `test_simulation.m` | Test script |
| `README_SIMULATION.md` | Full English docs |
| `README_FA.md` | مستندات کامل فارسی |

---

## Output Files / فایل‌های خروجی

After running the simulation, you will find:

```
Figure_01_Modeling_Framework.png
Figure_10_Tunnel_Errors.png           ← Main result
Figure_Interference_Comparison.png
Figure_Environment_Comparison.png
Figure_3D_Trajectory.png
Figure_Petri_Net_States.png
Figure_CPN_Petri_Net_Structure.png
Figure_Interference_Signals.png
gnss_simulation_results.mat
```

---

## Command Summary / خلاصه دستورات

### Quick Test / تست سریع
```matlab
test_simulation
```

### Full Simulation / شبیه‌سازی کامل
```matlab
gnss_train_positioning_complete_simulation
```

### Load Results / بارگذاری نتایج
```matlab
load('gnss_simulation_results.mat')
```

### View Specific Result / مشاهده نتیجه خاص
```matlab
% View Normal scenario errors
plot(time, results.Normal.pos_error)
xlabel('Time (s)'); ylabel('Error (m)');

% View Tunnel scenario errors  
plot(time, results.Tunnel.pos_error)
xlabel('Time (s)'); ylabel('Error (m)');
```

---

## Performance Metrics / معیارهای عملکرد

The simulation calculates these metrics for each scenario:
- Mean position error (میانگین خطای موقعیت)
- Standard deviation (انحراف معیار)
- 3D trajectory comparison (مقایسه مسیر سه‌بعدی)
- Satellite visibility (قابلیت رویت ماهواره)

---

## Customization / سفارشی‌سازی

To modify simulation parameters, edit Section 1 of the main script:

```matlab
% Time
T_sim = 600;         % Simulation duration (seconds)

% Train  
v_train = 20;        % Train velocity (m/s)

% Noise
sigma_pseudorange = 1.0;  % Measurement noise (m)
```

---

## Support / پشتیبانی

- English: See `README_SIMULATION.md`
- Persian: See `README_FA.md`
- Test: Run `test_simulation.m`
- Paper: See `Petrii.PDF`

---

## Citation / استناد

If you use this simulation in your research, please cite:

```
Chen, S., Wu, D., Liu, J., & Wang, S. (2025). 
Modeling and performance analysis of GNSS-based train positioning 
system with colored petri nets. High-speed Railway, 3, 175-184.
```

---

**Last Updated:** February 2026
**Version:** 1.0
**Language:** MATLAB (compatible with Octave)
