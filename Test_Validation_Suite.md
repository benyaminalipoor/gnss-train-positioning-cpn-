# Test and Validation Suite
# GNSS Train Positioning System CPN Model

## Test Configuration

This document outlines the test cases for validating the CPN model against the paper results.

## Test Cases

### Test Case 1: Open Area - No Interference (Baseline)

**Configuration:**
- Scenario: OpenArea
- Interference: Normal
- Expected Result: Mean error ≈ 1.03m, Std dev ≈ 0.06m

**Initial Marking:**
```sml
Scenario: 1`OpenArea
GNSS Signal: Sample satellite data (7 satellites)
Bool Control: bAM=false, bFM=false, bPulse=false
```

**Validation Criteria:**
- ✓ Mean error within 1.0 ± 0.05m
- ✓ Standard deviation within 0.055 ± 0.01m
- ✓ All satellites visible
- ✓ No interference applied

---

### Test Case 2: AM Interference

**Configuration:**
- Scenario: OpenArea
- Interference: AM
- Expected Result: Mean error ≈ 4.95m, Std dev ≈ 4.08m

**Initial Marking:**
```sml
Scenario: 1`OpenArea
GNSS Signal: Sample satellite data
Bool Control: bAM=true, bFM=false, bPulse=false
StateInterference: AM
```

**AM Parameters:**
- Carrier frequency: 1575.42 MHz
- Envelope frequency: 1 Hz
- Modulation depth: 0.5

**Validation Criteria:**
- ✓ Mean error within 4.9 ± 0.3m
- ✓ Standard deviation within 4.0 ± 0.3m
- ✓ Interference pattern visible in time series
- ✓ Elevation direction most affected

**Test Steps:**
1. Load sample GNSS data
2. Enable AM interference
3. Run simulation for 600 epochs
4. Calculate error statistics
5. Compare with Table 4 (AM row)

---

### Test Case 3: FM Interference

**Configuration:**
- Scenario: OpenArea
- Interference: FM
- Expected Result: Mean error ≈ 6.22m, Std dev ≈ 5.26m

**Initial Marking:**
```sml
Scenario: 1`OpenArea
GNSS Signal: Sample satellite data
Bool Control: bAM=false, bFM=true, bPulse=false
StateInterference: FM
```

**FM Parameters:**
- Carrier frequency: 1575.42 MHz
- Frequency deviation: 75 kHz (Gaussian)

**Validation Criteria:**
- ✓ Mean error within 6.2 ± 0.3m
- ✓ Standard deviation within 5.2 ± 0.3m
- ✓ Highest error among interference types
- ✓ Spectral spreading observable

**Test Steps:**
1. Load sample GNSS data
2. Enable FM interference
3. Run simulation for 600 epochs
4. Calculate error statistics
5. Compare with Table 4 (FM row) - should be worst case

---

### Test Case 4: Pulse Interference

**Configuration:**
- Scenario: OpenArea
- Interference: Pulse
- Expected Result: Mean error ≈ 4.79m, Std dev ≈ 3.62m

**Initial Marking:**
```sml
Scenario: 1`OpenArea
GNSS Signal: Sample satellite data
Bool Control: bAM=false, bFM=false, bPulse=true
StateInterference: Pulse
```

**Pulse Parameters:**
- Pulse width (Tp): 10ms
- Pulse interval (Ti): 90ms
- Amplitude: 1-5 (uniform)

**Validation Criteria:**
- ✓ Mean error within 4.8 ± 0.3m
- ✓ Standard deviation within 3.6 ± 0.3m
- ✓ Periodic bursts in error pattern
- ✓ Affects all spatial dimensions

**Test Steps:**
1. Load sample GNSS data
2. Enable Pulse interference
3. Run simulation for 600 epochs
4. Calculate error statistics
5. Verify periodic pattern in time series
6. Compare with Table 4 (Pulse row)

---

### Test Case 5: Mountain Scenario

**Configuration:**
- Scenario: Mountain
- Interference: None
- Expected Result: Mean error ≈ 1.30m, Std dev ≈ 0.45m

**Initial Marking:**
```sml
Scenario: 1`Mountain
GNSS Signal: Sample satellite data
Mountain Height: 100.0m
Distance: 500.0m
```

**Mountain Parameters:**
- Height: 100m
- Distance: 500m
- Obstruction angle: atan(100/500) ≈ 11.3°

**Validation Criteria:**
- ✓ Mean error within 1.3 ± 0.1m
- ✓ Standard deviation within 0.45 ± 0.05m
- ✓ Satellites below 11.3° elevation filtered
- ✓ Reduced satellite count

**Test Steps:**
1. Load sample GNSS data
2. Set mountain parameters
3. Run simulation for 600 epochs
4. Verify satellite filtering
5. Calculate error statistics
6. Compare with Table 5 (Mountain row)

**Expected Behavior:**
- Satellites with elevation < obstruction angle removed
- Reduced GDOP (Geometric Dilution of Precision)
- Moderate accuracy degradation

---

### Test Case 6: Tunnel Scenario - Phase 1 (InTunnel)

**Configuration:**
- Scenario: Tunnel
- State: InTunnel
- Expected Result: No signal output

**Initial Marking:**
```sml
Scenario: 1`Tunnel
GNSS Signal: Sample satellite data
TunnelState: InTunnel
```

**Validation Criteria:**
- ✓ No GNSS observations output
- ✓ Empty signal list
- ✓ No position calculation possible

**Test Steps:**
1. Load sample GNSS data
2. Set tunnel state to InTunnel
3. Verify GNSS Signal place becomes empty
4. Confirm no position output

---

### Test Case 7: Tunnel Scenario - Phase 2 (JustOut)

**Configuration:**
- Scenario: Tunnel
- State: JustOut
- Expected Result: High initial error with exponential decay

**Initial Marking:**
```sml
Scenario: 1`Tunnel
GNSS Signal: Sample satellite data
TunnelState: JustOut
TimeCounter: 0.0
```

**Tunnel Parameters:**
- Initial error: 15m
- Decay function: 15 × exp(-0.1 × time)

**Validation Criteria:**
- ✓ Initial error ≈ 15m
- ✓ Error decreases exponentially
- ✓ Time constant ≈ 10 seconds
- ✓ Error stabilizes after ~50 seconds

**Test Steps:**
1. Load sample GNSS data
2. Set tunnel state to JustOut
3. Monitor error over time
4. Verify exponential decay pattern
5. Check stabilization time

**Expected Error Evolution:**
```
Time (s)    Error (m)
0           15.0
10          5.5
20          2.0
30          0.7
40          0.3
50+         0.5 (stable)
```

---

### Test Case 8: Tunnel Scenario - Phase 3 (OutTunnel)

**Configuration:**
- Scenario: Tunnel
- State: OutTunnel
- Expected Result: Stable low error

**Initial Marking:**
```sml
Scenario: 1`Tunnel
GNSS Signal: Sample satellite data
TunnelState: OutTunnel
```

**Validation Criteria:**
- ✓ Error ≈ 0.5m (stable)
- ✓ No further decay
- ✓ Normal signal reception
- ✓ All satellites visible

**Test Steps:**
1. Load sample GNSS data
2. Set tunnel state to OutTunnel
3. Run simulation for 100 epochs
4. Verify stable error around 0.5m
5. Confirm normal operation

---

### Test Case 9: Tunnel Scenario - Complete Cycle

**Configuration:**
- Scenario: Tunnel
- States: InTunnel → JustOut → OutTunnel
- Expected Result: Mean error ≈ 5.67m, Std dev ≈ 6.69m

**Initial Marking:**
```sml
Scenario: 1`Tunnel
Sequence: [InTunnel(200 epochs), JustOut(100 epochs), OutTunnel(300 epochs)]
```

**Validation Criteria:**
- ✓ Mean error within 5.6 ± 0.3m
- ✓ Standard deviation within 6.5 ± 0.5m
- ✓ Complete phase transition
- ✓ Match Figure 10 from paper

**Test Steps:**
1. Simulate train entering tunnel (InTunnel)
2. Simulate tunnel exit (JustOut)
3. Simulate recovery (OutTunnel)
4. Calculate overall statistics
5. Compare with Table 5 (Tunnel row)

**Phase Distribution:**
- InTunnel: 33% of time (200 epochs)
- JustOut: 17% of time (100 epochs)
- OutTunnel: 50% of time (300 epochs)

---

### Test Case 10: State Space Verification

**Configuration:**
- All scenarios tested
- Complete state space generation

**Validation Criteria:**
- ✓ State space nodes: 5365
- ✓ State space arcs: 6410
- ✓ Dead markings: 648
- ✓ No infinite sequences
- ✓ Model is bounded

**Test Steps:**
1. Generate state space in CPN Tools
2. Run state space analysis
3. Compare with Table 3
4. Verify no unexpected behaviors

**Expected State Space Report:**
```
State Space Statistics:
- Nodes: 5365
- Arcs: 6410
- Secs: ~1

SCC Graph:
- Nodes: 5365
- Arcs: 6410

Home Properties:
- Home markings: None

Liveness Properties:
- Dead markings: 648
- Dead transition instances: None
- Live transition instances: None

Fairness Properties:
- No infinite occurrence sequences
```

---

## Automated Test Suite

### Test Execution Script

```sml
(* Load test data *)
use "GNSS_Sample_Data.sml";

(* Test results structure *)
datatype TestResult = Pass | Fail of string;

(* Test Case 1: Baseline *)
fun test_baseline () =
    let
        val errors = (* run simulation *)
        val meanErr = calculateMean errors
        val stdErr = calculateStdDev errors
    in
        if abs(meanErr - 1.0279) < 0.05 andalso abs(stdErr - 0.0552) < 0.01
        then Pass
        else Fail ("Mean: " ^ Real.toString meanErr ^ ", Std: " ^ Real.toString stdErr)
    end;

(* Test Case 2: AM Interference *)
fun test_am_interference () =
    let
        val errors = (* run simulation with AM *)
        val meanErr = calculateMean errors
        val stdErr = calculateStdDev errors
    in
        if abs(meanErr - 4.9484) < 0.3 andalso abs(stdErr - 4.0833) < 0.3
        then Pass
        else Fail ("Mean: " ^ Real.toString meanErr ^ ", Std: " ^ Real.toString stdErr)
    end;

(* Test Case 3: FM Interference *)
fun test_fm_interference () =
    let
        val errors = (* run simulation with FM *)
        val meanErr = calculateMean errors
        val stdErr = calculateStdDev errors
    in
        if abs(meanErr - 6.2241) < 0.3 andalso abs(stdErr - 5.2630) < 0.3
        then Pass
        else Fail ("Mean: " ^ Real.toString meanErr ^ ", Std: " ^ Real.toString stdErr)
    end;

(* Run all tests *)
fun run_all_tests () =
    let
        val tests = [
            ("Baseline", test_baseline),
            ("AM Interference", test_am_interference),
            ("FM Interference", test_fm_interference),
            (* Add more tests *)
        ]
        fun runTest (name, testFn) =
            let
                val result = testFn ()
            in
                print ("Test: " ^ name ^ " - ");
                case result of
                    Pass => print "PASS\n"
                  | Fail msg => print ("FAIL: " ^ msg ^ "\n")
            end
    in
        List.app runTest tests
    end;
```

---

## Performance Benchmarks

### Expected Simulation Performance

| Metric | Value |
|--------|-------|
| Simulation time (600 epochs) | < 5 minutes |
| Memory usage | < 2GB |
| State space generation | < 2 seconds |
| Average error calculation | < 1 second |

### Accuracy Requirements

| Scenario | Mean Error Tolerance | Std Dev Tolerance |
|----------|---------------------|-------------------|
| Normal | ±0.05m | ±0.01m |
| AM | ±0.3m | ±0.3m |
| FM | ±0.3m | ±0.3m |
| Pulse | ±0.3m | ±0.3m |
| Mountain | ±0.1m | ±0.05m |
| Tunnel | ±0.3m | ±0.5m |

---

## Validation Checklist

### Pre-simulation Checks
- [ ] CPN Tools installed and working
- [ ] All color sets declared correctly
- [ ] All variables declared with proper types
- [ ] Helper functions compile without errors
- [ ] Sample data loads successfully
- [ ] Initial markings set correctly

### Simulation Checks
- [ ] Model runs without errors
- [ ] Transitions fire as expected
- [ ] Token flow is correct
- [ ] Time advances properly
- [ ] No deadlocks (except terminal states)

### Post-simulation Checks
- [ ] All 600 epochs completed
- [ ] Error data collected
- [ ] Statistics calculated correctly
- [ ] Results match paper (within tolerance)
- [ ] State space analysis complete

### Results Validation
- [ ] Table 4 values matched (signal interference)
- [ ] Table 5 values matched (environment scenarios)
- [ ] Table 3 values matched (state space)
- [ ] Figure 10 pattern matched (tunnel error evolution)

---

## Troubleshooting Guide

### Issue: Mean error significantly different from expected

**Possible Causes:**
1. Incorrect interference parameters
2. Wrong satellite data
3. EKF implementation error
4. Reference position mismatch

**Solutions:**
1. Verify interference function parameters
2. Check GNSS data format
3. Validate EKF calculations
4. Confirm reference trajectory alignment

### Issue: Simulation doesn't complete 600 epochs

**Possible Causes:**
1. Deadlock in model
2. Missing transitions
3. Incorrect guards
4. Token type mismatch

**Solutions:**
1. Check state space for deadlocks
2. Verify all transitions can fire
3. Review guard conditions
4. Validate token colors

### Issue: State space generation fails

**Possible Causes:**
1. Model too complex
2. Unbounded places
3. Infinite loops
4. Memory exhaustion

**Solutions:**
1. Simplify model
2. Add bounds to places
3. Remove circular dependencies
4. Increase available memory

---

## Test Report Template

```
GNSS Train Positioning CPN Model - Test Report
===============================================

Date: [DATE]
Tester: [NAME]
CPN Tools Version: [VERSION]

Test Results Summary:
--------------------
Total Tests: 10
Passed: [X]
Failed: [Y]
Skipped: [Z]

Detailed Results:
-----------------

Test Case 1: Open Area Baseline
Status: [PASS/FAIL]
Mean Error: [VALUE]m (Expected: 1.03m)
Std Dev: [VALUE]m (Expected: 0.06m)
Notes: [NOTES]

Test Case 2: AM Interference
Status: [PASS/FAIL]
Mean Error: [VALUE]m (Expected: 4.95m)
Std Dev: [VALUE]m (Expected: 4.08m)
Notes: [NOTES]

[Continue for all test cases...]

State Space Analysis:
--------------------
Nodes: [VALUE] (Expected: 5365)
Arcs: [VALUE] (Expected: 6410)
Dead Markings: [VALUE] (Expected: 648)

Conclusion:
-----------
[PASS/FAIL] - Model [matches/does not match] paper specifications

Issues Found:
-------------
[LIST ANY ISSUES]

Recommendations:
----------------
[LIST RECOMMENDATIONS]
```

---

## Continuous Validation

### Regression Tests
Run after any model changes:
1. Baseline test (Test Case 1)
2. All interference tests (Test Cases 2-4)
3. All environment tests (Test Cases 5-9)
4. State space verification (Test Case 10)

### Integration Tests
Verify interactions between modules:
1. GNSS Receiver → Position Solution
2. Position Solution → Evaluation
3. Evaluation → Reference Position comparison

### Performance Tests
Monitor computational efficiency:
1. Simulation execution time
2. Memory consumption
3. State space generation time

---

## Final Validation

Before declaring implementation complete:

1. ✓ All test cases pass
2. ✓ Results match paper within tolerance
3. ✓ State space verified
4. ✓ Documentation complete
5. ✓ Code reviewed
6. ✓ Performance acceptable

**Sign-off Required:**
- Technical Reviewer: ___________
- Quality Assurance: ___________
- Project Lead: ___________
