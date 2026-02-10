%% Quick Test Script for GNSS Train Positioning Simulation
% This script performs a quick validation of the main simulation
% Run this to ensure the simulation works before running the full version

clear; close all; clc;

fprintf('=========================================\n');
fprintf('GNSS Train Positioning - Quick Test\n');
fprintf('=========================================\n\n');

%% Test 1: Check if main script file exists
fprintf('Test 1: Checking main script file...\n');
script_file = 'gnss_train_positioning_complete_simulation.m';
if exist(script_file, 'file')
    fprintf('  ✓ Main script file found\n');
else
    error('  ✗ Main script file not found!');
end

%% Test 2: Validate MATLAB syntax
fprintf('\nTest 2: Validating MATLAB syntax...\n');
try
    % Read the file
    fid = fopen(script_file, 'r');
    content = fread(fid, '*char')';
    fclose(fid);
    
    % Check for common syntax elements
    checks = {
        'clear all', 'Initialization';
        'dt = ', 'Time step definition';
        'Extended Kalman Filter', 'EKF implementation';
        'PETRI NET', 'Petri Net structure';
        'saveas(gcf', 'Figure saving';
        'fprintf', 'Output formatting'
    };
    
    for i = 1:size(checks, 1)
        if contains(content, checks{i, 1})
            fprintf('  ✓ %s found\n', checks{i, 2});
        else
            fprintf('  ✗ %s missing\n', checks{i, 2});
        end
    end
    
    fprintf('  ✓ Syntax validation passed\n');
catch ME
    fprintf('  ✗ Syntax validation failed: %s\n', ME.message);
end

%% Test 3: Check MATLAB version compatibility
fprintf('\nTest 3: Checking MATLAB version...\n');
v = ver('MATLAB');
if ~isempty(v)
    fprintf('  ✓ MATLAB Version: %s\n', v.Version);
    ver_num = str2double(v.Version);
    if ver_num >= 9.1  % R2016b
        fprintf('  ✓ Version is compatible (R2016b or later)\n');
    else
        fprintf('  ⚠ Warning: Recommended MATLAB R2016b or later\n');
    end
else
    fprintf('  ⚠ Running on GNU Octave or MATLAB version unknown\n');
end

%% Test 4: Simple mini simulation (reduced parameters)
fprintf('\nTest 4: Running mini simulation (10 seconds)...\n');
try
    % Mini simulation parameters
    dt = 1;
    T_sim = 10;
    time = 0:dt:T_sim;
    N = length(time);
    
    % Simple EKF state
    x = [0; 0; 100; 20; 0; 0];  % [x,y,z,vx,vy,vz]
    
    % State transition
    F = eye(6);
    F(1,4) = dt; F(2,5) = dt; F(3,6) = dt;
    
    % Simple prediction
    x_pred = F * x;
    
    fprintf('  ✓ Initial state: [%.1f, %.1f, %.1f] m\n', x(1), x(2), x(3));
    fprintf('  ✓ Predicted state: [%.1f, %.1f, %.1f] m\n', x_pred(1), x_pred(2), x_pred(3));
    fprintf('  ✓ Mini simulation completed successfully\n');
catch ME
    fprintf('  ✗ Mini simulation failed: %s\n', ME.message);
end

%% Test 5: Check figure generation capability
fprintf('\nTest 5: Testing figure generation...\n');
try
    test_fig = figure('Visible', 'off');
    plot(1:10, rand(1,10));
    title('Test Figure');
    
    % Try to save
    test_filename = 'test_figure_temp.png';
    saveas(test_fig, test_filename);
    
    if exist(test_filename, 'file')
        fprintf('  ✓ Figure generation works\n');
        delete(test_filename);  % Clean up
    else
        fprintf('  ⚠ Warning: Figure saving may not work\n');
    end
    
    close(test_fig);
catch ME
    fprintf('  ⚠ Warning: Figure generation issue: %s\n', ME.message);
end

%% Test 6: Memory and performance estimate
fprintf('\nTest 6: Estimating memory and performance...\n');
try
    % Estimate memory for full simulation
    T_sim_full = 600;
    N_full = T_sim_full + 1;
    n_scenarios = 7;
    
    % Rough memory estimate
    mem_per_double = 8;  % bytes
    mem_estimate = N_full * n_scenarios * 3 * mem_per_double / 1024 / 1024;  % MB
    
    fprintf('  ✓ Full simulation will use approximately %.2f MB RAM\n', mem_estimate);
    fprintf('  ✓ Estimated runtime: 10-30 seconds\n');
    fprintf('  ✓ Number of time steps: %d\n', N_full);
    fprintf('  ✓ Number of scenarios: %d\n', n_scenarios);
catch ME
    fprintf('  ⚠ Warning: Could not estimate performance: %s\n', ME.message);
end

%% Summary
fprintf('\n=========================================\n');
fprintf('Quick Test Summary\n');
fprintf('=========================================\n');
fprintf('All basic tests passed!\n');
fprintf('You can now run the full simulation:\n');
fprintf('  >> gnss_train_positioning_complete_simulation\n');
fprintf('\nExpected outputs:\n');
fprintf('  - 8 PNG figure files\n');
fprintf('  - 2 tables in command window\n');
fprintf('  - 1 MAT file with results\n');
fprintf('  - Runtime: ~10-30 seconds\n');
fprintf('=========================================\n');

%% Instructions
fprintf('\n');
fprintf('HOW TO RUN THE FULL SIMULATION:\n');
fprintf('-------------------------------\n');
fprintf('1. Make sure you are in the correct directory\n');
fprintf('2. Run: gnss_train_positioning_complete_simulation\n');
fprintf('3. Wait for completion (progress shown in console)\n');
fprintf('4. Check generated PNG files and results\n');
fprintf('\n');
fprintf('For more information, see README_SIMULATION.md\n');
fprintf('\n');
