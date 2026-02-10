% Demo Script: Running Individual Simulations
% This script demonstrates how to run specific parts of the GNSS CPN simulation

fprintf('GNSS CPN Simulation - Demo Script\n');
fprintf('==================================\n\n');

%% Example 1: Run complete simulation
fprintf('Example 1: Running complete simulation...\n');
fprintf('Command: gnss_cpn_simulation()\n\n');
% gnss_cpn_simulation();  % Uncomment to run

%% Example 2: Load and display Table 4 results
fprintf('Example 2: Loading Table 4 results (Signal Interference Analysis)...\n');
if exist('table_4_results.mat', 'file')
    load('table_4_results.mat');
    fprintf('\nTable 4: Performance under Different Signal Interferences\n');
    fprintf('%-12s %12s %12s\n', 'Scenario', 'Mean (m)', 'Std Dev (m)');
    fprintf('%s\n', repmat('-', 1, 40));
    for i = 1:length(scenarios)
        fprintf('%-12s %12.4f %12.4f\n', scenarios{i}, table_data(i, 1), table_data(i, 2));
    end
    fprintf('\nKey Finding: FM interference has the most severe impact on positioning accuracy.\n');
else
    fprintf('Table 4 results not found. Run gnss_cpn_simulation() first.\n');
end

%% Example 3: Load and display Table 5 results
fprintf('\n\nExample 3: Loading Table 5 results (Environment Scenario Analysis)...\n');
if exist('table_5_results.mat', 'file')
    load('table_5_results.mat');
    fprintf('\nTable 5: Performance under Different Environment Scenarios\n');
    fprintf('%-18s %12s %12s\n', 'Scenario', 'Mean (m)', 'Std Dev (m)');
    fprintf('%s\n', repmat('-', 1, 45));
    for i = 1:length(scenarios)
        fprintf('%-18s %12.4f %12.4f\n', scenarios{i}, table_data(i, 1), table_data(i, 2));
    end
    fprintf('\nKey Finding: Tunnel scenario poses the greatest challenge with highest error variance.\n');
else
    fprintf('Table 5 results not found. Run gnss_cpn_simulation() first.\n');
end

%% Example 4: List generated figures
fprintf('\n\nExample 4: Listing generated figures...\n');
figure_files = dir('figure_*.png');
if ~isempty(figure_files)
    fprintf('\nGenerated figures:\n');
    for i = 1:length(figure_files)
        fprintf('  %2d. %s\n', i, figure_files(i).name);
    end
    fprintf('\nThese figures represent the complete CPN model structure from the paper.\n');
else
    fprintf('No figures found. Run gnss_cpn_simulation() first.\n');
end

%% Example 5: Display Figure 10 information
fprintf('\n\nExample 5: Figure 10 - Tunnel Scenario Analysis\n');
if exist('figure_10_tunnel_errors.png', 'file')
    fprintf('\nFigure 10 shows position errors during tunnel transit:\n');
    fprintf('  - Phase 1: Inside tunnel - Complete signal loss\n');
    fprintf('  - Phase 2: Tunnel exit - Signal reacquisition with high errors\n');
    fprintf('  - Phase 3: Stabilization - Gradual error reduction\n');
    fprintf('\nThis demonstrates the critical challenge of GNSS positioning in tunnel environments.\n');
else
    fprintf('Figure 10 not found. Run gnss_cpn_simulation() first.\n');
end

%% Example 6: Accessing the simulation programmatically
fprintf('\n\nExample 6: Programmatic access to simulation functions\n');
fprintf('\nYou can call individual simulation functions:\n');
fprintf('  - simulate_scenario(''Normal'', ''OpenArea'', 1000, 1.0)\n');
fprintf('  - simulate_scenario(''FM'', ''Mountain'', 500, 1.0)\n');
fprintf('  - simulate_scenario(''Pulse'', ''Tunnel'', 1500, 1.0)\n');

%% Summary
fprintf('\n\n=== DEMO COMPLETED ===\n');
fprintf('\nFor full documentation, see README_SIMULATION.md\n');
fprintf('For complete simulation, run: gnss_cpn_simulation()\n');
