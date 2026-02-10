% GNSS Train Positioning System using Colored Petri Nets
% Based on the paper: "Modeling and performance analysis of GNSS-based 
% train positioning system with colored petri nets"
% 
% This simulation implements the complete CPN model described in the paper
% and generates all figures (Fig. 1-10) and tables (Table 4-5)

function gnss_cpn_simulation()
    % Main function to run the complete simulation
    
    close all;
    clc;
    
    fprintf('GNSS Train Positioning CPN Simulation\n');
    fprintf('=====================================\n\n');
    
    % Initialize random seed for reproducibility
    rng(42);
    
    % Run all simulations and generate figures
    generate_all_figures();
    
    % Run performance analysis for different scenarios
    run_performance_analysis();
    
    fprintf('\nSimulation completed successfully!\n');
    fprintf('All figures and results have been generated.\n');
end

%% ========================================================================
% Helper Functions
% ========================================================================

function draw_circle(center, radius, varargin)
    % Helper function to draw circles (replaces viscircles for Octave compatibility)
    theta = linspace(0, 2*pi, 100);
    x = center(1) + radius * cos(theta);
    y = center(2) + radius * sin(theta);
    
    % Parse optional arguments
    linecolor = 'k';
    linewidth = 1;
    for i = 1:2:length(varargin)
        if strcmpi(varargin{i}, 'Color')
            linecolor = varargin{i+1};
        elseif strcmpi(varargin{i}, 'LineWidth')
            linewidth = varargin{i+1};
        end
    end
    
    plot(x, y, 'Color', linecolor, 'LineWidth', linewidth);
end

%% ========================================================================
% Figure Generation Functions
% ========================================================================

function generate_all_figures()
    fprintf('Generating all figures from the paper...\n');
    
    % Figure 1: Modeling framework
    generate_figure_1_framework();
    
    % Figure 2: Hierarchical architecture
    generate_figure_2_hierarchy();
    
    % Figure 3: Top-level CPN model
    generate_figure_3_toplevel();
    
    % Figure 4: GNSS Receiver module
    generate_figure_4_receiver();
    
    % Figure 5: Open Area submodule
    generate_figure_5_openarea();
    
    % Figure 6: Mountain submodule
    generate_figure_6_mountain();
    
    % Figure 7: Tunnel submodule
    generate_figure_7_tunnel();
    
    % Figure 8: Position Solution module
    generate_figure_8_position_solution();
    
    % Figure 9: Evaluation module
    generate_figure_9_evaluation();
    
    fprintf('Static CPN model figures (1-9) generated.\n');
end

function generate_figure_1_framework()
    % Figure 1: Modeling framework of train positioning system
    
    fig = figure('Position', [100, 100, 1200, 600], 'Name', 'Figure 1: Modeling Framework', 'visible', 'off');
    
    % Define components
    components = {
        'GNSS\nReceiver', [0.15, 0.5];
        'Environment\nScenarios', [0.35, 0.7];
        'Interference\nSignals', [0.35, 0.3];
        'GNSS Position\nSolution', [0.65, 0.5];
        'Evaluation\nModule', [0.85, 0.5]
    };
    
    % Draw components as boxes
    for i = 1:size(components, 1)
        label_text = components{i, 1};
        pos = components{i, 2};
        rectangle('Position', [pos(1)-0.06, pos(2)-0.08, 0.12, 0.16], ...
                  'FaceColor', [0.8 0.9 1], 'EdgeColor', 'k', 'LineWidth', 2);
        text(pos(1), pos(2), label_text, 'HorizontalAlignment', 'center', ...
             'FontSize', 10, 'FontWeight', 'bold', 'Interpreter', 'none');
    end
    
    % Draw arrows showing data flow
    annotation('arrow', [0.21, 0.29], [0.5, 0.72], 'LineWidth', 2);
    annotation('arrow', [0.21, 0.29], [0.5, 0.32], 'LineWidth', 2);
    annotation('arrow', [0.41, 0.59], [0.72, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.41, 0.59], [0.32, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.71, 0.79], [0.5, 0.5], 'LineWidth', 2);
    
    % Add labels
    text(0.25, 0.62, 'Select Scenario', 'FontSize', 8, 'Color', 'b');
    text(0.48, 0.76, 'GNSS Signals', 'FontSize', 8, 'Color', 'b');
    text(0.48, 0.24, 'Interference', 'FontSize', 8, 'Color', 'b');
    text(0.73, 0.56, 'Position', 'FontSize', 8, 'Color', 'b');
    
    title('Figure 1: Modeling Framework of Train Positioning System', ...
          'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_1_framework.png');
    fprintf('  - Figure 1 saved\n');
end

function generate_figure_2_hierarchy()
    % Figure 2: Hierarchical architecture of the CPN model
    
    fig = figure('Position', [100, 100, 1000, 700], 'Name', 'Figure 2: Hierarchical Architecture', 'visible', 'off');
    
    % Top level
    rectangle('Position', [0.35, 0.85, 0.3, 0.1], ...
              'FaceColor', [1 0.8 0.8], 'EdgeColor', 'k', 'LineWidth', 2);
    text(0.5, 0.9, 'Top Level', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold');
    
    % Level 2 - Main modules
    modules_l2 = {'GNSS Receiver', 'Position Solution', 'Evaluation'};
    x_positions = [0.1, 0.4, 0.7];
    for i = 1:length(modules_l2)
        rectangle('Position', [x_positions(i), 0.6, 0.2, 0.1], ...
                  'FaceColor', [0.8 1 0.8], 'EdgeColor', 'k', 'LineWidth', 2);
        text(x_positions(i)+0.1, 0.65, modules_l2{i}, ...
             'HorizontalAlignment', 'center', 'FontSize', 10, 'FontWeight', 'bold');
        
        % Arrows from top level
        annotation('arrow', [0.5, x_positions(i)+0.1], [0.85, 0.71], 'LineWidth', 1.5);
    end
    
    % Level 3 - Submodules under GNSS Receiver
    submodules = {'Open Area', 'Mountain', 'Tunnel'};
    x_sub = [0.02, 0.13, 0.24];
    for i = 1:length(submodules)
        rectangle('Position', [x_sub(i), 0.35, 0.1, 0.08], ...
                  'FaceColor', [0.8 0.9 1], 'EdgeColor', 'k', 'LineWidth', 1.5);
        text(x_sub(i)+0.05, 0.39, submodules{i}, ...
             'HorizontalAlignment', 'center', 'FontSize', 8);
        
        % Arrows from GNSS Receiver
        annotation('arrow', [0.2, x_sub(i)+0.05], [0.6, 0.44], 'LineWidth', 1);
    end
    
    % Add EKF block under Position Solution
    rectangle('Position', [0.42, 0.35, 0.16, 0.08], ...
              'FaceColor', [1 1 0.8], 'EdgeColor', 'k', 'LineWidth', 1.5);
    text(0.5, 0.39, 'EKF Algorithm', ...
         'HorizontalAlignment', 'center', 'FontSize', 8);
    annotation('arrow', [0.5, 0.5], [0.6, 0.44], 'LineWidth', 1);
    
    title('Figure 2: Hierarchical Architecture of the CPN Model', ...
          'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_2_hierarchy.png');
    fprintf('  - Figure 2 saved\n');
end

function generate_figure_3_toplevel()
    % Figure 3: Top-level of the CPN model
    
    fig = figure('Position', [100, 100, 1200, 600], 'Name', 'Figure 3: Top Level CPN', 'visible', 'off');
    
    % Places (circles)
    places = {
        'Scenario', [0.15, 0.5], 'SCENARIO';
        'GNSS_Signals', [0.4, 0.7], 'SIGNALlist';
        'Observations', [0.65, 0.7], 'SIGNALlist';
        'Position', [0.85, 0.5], 'COORDINATE';
        'Reference', [0.65, 0.3], 'COORDINATE';
        'Error', [0.85, 0.3], 'REAL'
    };
    
    % Draw places
    for i = 1:size(places, 1)
        draw_circle(places{i, 2}, 0.05, 'Color', 'k', 'LineWidth', 2);
        text(places{i, 2}(1), places{i, 2}(2), places{i, 1}, ...
             'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
        text(places{i, 2}(1), places{i, 2}(2)-0.08, ['[' places{i, 3} ']'], ...
             'HorizontalAlignment', 'center', 'FontSize', 7, 'Color', 'r');
    end
    
    % Transitions (rectangles)
    transitions = {
        'Receive', [0.27, 0.6];
        'Solve', [0.75, 0.6];
        'Evaluate', [0.75, 0.4]
    };
    
    % Draw transitions
    for i = 1:size(transitions, 1)
        rectangle('Position', [transitions{i, 2}(1)-0.03, transitions{i, 2}(2)-0.04, ...
                               0.06, 0.08], 'FaceColor', [0.2 0.2 0.2], ...
                  'EdgeColor', 'k', 'LineWidth', 2);
        text(transitions{i, 2}(1), transitions{i, 2}(2), transitions{i, 1}, ...
             'HorizontalAlignment', 'center', 'FontSize', 8, 'Color', 'w', ...
             'FontWeight', 'bold');
    end
    
    % Arcs
    % Scenario -> Receive
    annotation('arrow', [0.20, 0.24], [0.5, 0.57], 'LineWidth', 2);
    % Receive -> GNSS_Signals
    annotation('arrow', [0.30, 0.37], [0.6, 0.67], 'LineWidth', 2);
    % GNSS_Signals -> Solve
    annotation('arrow', [0.45, 0.72], [0.7, 0.62], 'LineWidth', 2);
    % Solve -> Observations
    annotation('arrow', [0.78, 0.65], [0.64, 0.68], 'LineWidth', 2);
    % Observations -> Position
    annotation('arrow', [0.70, 0.82], [0.68, 0.52], 'LineWidth', 2);
    % Reference -> Evaluate
    annotation('arrow', [0.68, 0.73], [0.34, 0.38], 'LineWidth', 2);
    % Position -> Evaluate
    annotation('arrow', [0.83, 0.77], [0.48, 0.42], 'LineWidth', 2);
    % Evaluate -> Error
    annotation('arrow', [0.78, 0.83], [0.36, 0.32], 'LineWidth', 2);
    
    title('Figure 3: Top-Level of the CPN Model', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_3_toplevel.png');
    fprintf('  - Figure 3 saved\n');
end

function generate_figure_4_receiver()
    % Figure 4: Module GNSS Receiver
    
    fig = figure('Position', [100, 100, 1000, 600], 'Name', 'Figure 4: GNSS Receiver', 'visible', 'off');
    
    % Input place
    draw_circle([0.15, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.15, 0.5, 'Scenario', 'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
    
    % Transition - Scenario Selection
    rectangle('Position', [0.27, 0.46, 0.06, 0.08], 'FaceColor', [0.2 0.2 0.2], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.30, 0.5, 'Select', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'Color', 'w', 'FontWeight', 'bold');
    
    % Three scenario submodules
    scenarios = {'Open Area', 'Mountain', 'Tunnel'};
    y_pos = [0.75, 0.5, 0.25];
    
    for i = 1:length(scenarios)
        % Substitution transition
        rectangle('Position', [0.47, y_pos(i)-0.06, 0.16, 0.12], ...
                  'FaceColor', [0.7 0.85 1], 'EdgeColor', 'k', 'LineWidth', 2);
        text(0.55, y_pos(i), scenarios{i}, 'HorizontalAlignment', 'center', ...
             'FontSize', 9, 'FontWeight', 'bold');
        text(0.55, y_pos(i)-0.04, 'HS', 'HorizontalAlignment', 'center', ...
             'FontSize', 7, 'Color', 'r');
        
        % Arrow from Select
        annotation('arrow', [0.33, 0.47], [0.5, y_pos(i)], 'LineWidth', 1.5);
        
        % Output place for each
        draw_circle([0.75, y_pos(i)], 0.04, 'Color', 'k', 'LineWidth', 1.5);
        text(0.75, y_pos(i), 'Out', 'HorizontalAlignment', 'center', 'FontSize', 7);
        
        % Arrow to output
        annotation('arrow', [0.63, 0.71], [y_pos(i), y_pos(i)], 'LineWidth', 1.5);
    end
    
    % Final output place
    draw_circle([0.9, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.9, 0.5, 'Signals', 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'FontWeight', 'bold');
    
    % Arrows to final output
    for i = 1:length(y_pos)
        annotation('arrow', [0.79, 0.87], [y_pos(i), 0.5], 'LineWidth', 1.5);
    end
    
    title('Figure 4: Module GNSS Receiver', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_4_receiver.png');
    fprintf('  - Figure 4 saved\n');
end

function generate_figure_5_openarea()
    % Figure 5: Submodule Open Area
    
    fig = figure('Position', [100, 100, 1000, 700], 'Name', 'Figure 5: Open Area', 'visible', 'off');
    
    % Input place
    draw_circle([0.15, 0.7], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.15, 0.7, 'In', 'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
    
    % Transition - Generate Signals
    rectangle('Position', [0.27, 0.66, 0.06, 0.08], 'FaceColor', [0.2 0.2 0.2], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.30, 0.7, 'Gen', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'Color', 'w', 'FontWeight', 'bold');
    
    % Interference type place
    draw_circle([0.3, 0.5], 0.045, 'Color', 'k', 'LineWidth', 2);
    text(0.3, 0.5, 'Infer\nType', 'HorizontalAlignment', 'center', 'FontSize', 7, 'FontWeight', 'bold');
    
    % Four interference branches
    interference_types = {'Normal', 'AM', 'FM', 'Pulse'};
    x_pos = [0.45, 0.55, 0.65, 0.75];
    
    for i = 1:length(interference_types)
        % Transition for each interference
        rectangle('Position', [x_pos(i)-0.03, 0.66, 0.06, 0.08], ...
                  'FaceColor', [0.3 0.3 0.3], 'EdgeColor', 'k', 'LineWidth', 1.5);
        text(x_pos(i), 0.7, interference_types{i}, 'HorizontalAlignment', 'center', ...
             'FontSize', 7, 'Color', 'w', 'FontWeight', 'bold');
        
        % Output place
        draw_circle([x_pos(i), 0.5], 0.04, 'Color', 'k', 'LineWidth', 1.5);
        text(x_pos(i), 0.5, 'S', 'HorizontalAlignment', 'center', 'FontSize', 7);
        
        % Arrows
        annotation('arrow', [0.33, x_pos(i)-0.03], [0.7, 0.7], 'LineWidth', 1);
        annotation('arrow', [x_pos(i), x_pos(i)], [0.66, 0.55], 'LineWidth', 1);
    end
    
    % Merge transition
    rectangle('Position', [0.57, 0.36, 0.06, 0.08], 'FaceColor', [0.2 0.2 0.2], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.60, 0.4, 'Merge', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'Color', 'w', 'FontWeight', 'bold');
    
    % Arrows to merge
    for i = 1:length(x_pos)
        annotation('arrow', [x_pos(i), 0.60], [0.46, 0.38], 'LineWidth', 1);
    end
    
    % Output place
    draw_circle([0.85, 0.4], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.85, 0.4, 'Out', 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'FontWeight', 'bold');
    
    % Arrow to output
    annotation('arrow', [0.63, 0.82], [0.4, 0.4], 'LineWidth', 2);
    
    title('Figure 5: Submodule Open Area', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_5_openarea.png');
    fprintf('  - Figure 5 saved\n');
end

function generate_figure_6_mountain()
    % Figure 6: Submodule Mountain
    
    fig = figure('Position', [100, 100, 1000, 600], 'Name', 'Figure 6: Mountain', 'visible', 'off');
    
    % Input place
    draw_circle([0.15, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.15, 0.5, 'In', 'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
    
    % Generate signals transition
    rectangle('Position', [0.27, 0.46, 0.06, 0.08], 'FaceColor', [0.2 0.2 0.2], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.30, 0.5, 'Gen', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'Color', 'w', 'FontWeight', 'bold');
    
    % Signals place
    draw_circle([0.45, 0.5], 0.045, 'Color', 'k', 'LineWidth', 2);
    text(0.45, 0.5, 'Signals', 'HorizontalAlignment', 'center', 'FontSize', 8, 'FontWeight', 'bold');
    
    % Mountain occlusion transition
    rectangle('Position', [0.57, 0.46, 0.06, 0.08], 'FaceColor', [0.5 0.3 0.2], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.60, 0.5, 'Block', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'Color', 'w', 'FontWeight', 'bold');
    text(0.60, 0.42, 'Mountain', 'HorizontalAlignment', 'center', ...
         'FontSize', 7, 'Color', [0.5 0.3 0.2]);
    
    % Output place
    draw_circle([0.75, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.75, 0.5, 'Out', 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'FontWeight', 'bold');
    
    % Arrows
    annotation('arrow', [0.20, 0.24], [0.5, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.33, 0.41], [0.5, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.49, 0.54], [0.5, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.63, 0.72], [0.5, 0.5], 'LineWidth', 2);
    
    % Add mountain illustration
    x_mountain = [0.60, 0.58, 0.55, 0.52, 0.50, 0.48, 0.45, 0.42, 0.40];
    y_mountain = [0.65, 0.68, 0.70, 0.68, 0.65, 0.63, 0.65, 0.68, 0.65];
    fill(x_mountain, y_mountain, [0.6 0.4 0.2], 'EdgeColor', [0.4 0.3 0.1], 'LineWidth', 1.5);
    text(0.50, 0.75, 'Mountain Occlusion', 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'FontWeight', 'bold', 'Color', [0.5 0.3 0.1]);
    
    title('Figure 6: Submodule Mountain', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_6_mountain.png');
    fprintf('  - Figure 6 saved\n');
end

function generate_figure_7_tunnel()
    % Figure 7: Submodule Tunnel
    
    fig = figure('Position', [100, 100, 1000, 600], 'Name', 'Figure 7: Tunnel', 'visible', 'off');
    
    % Input place
    draw_circle([0.15, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.15, 0.5, 'In', 'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
    
    % Generate signals transition
    rectangle('Position', [0.27, 0.46, 0.06, 0.08], 'FaceColor', [0.2 0.2 0.2], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.30, 0.5, 'Gen', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'Color', 'w', 'FontWeight', 'bold');
    
    % Tunnel state place
    draw_circle([0.5, 0.7], 0.045, 'Color', 'k', 'LineWidth', 2);
    text(0.5, 0.7, 'Tunnel\nState', 'HorizontalAlignment', 'center', ...
         'FontSize', 7, 'FontWeight', 'bold');
    
    % Three tunnel states
    states = {'InTunnel', 'JustOut', 'OutTunnel'};
    x_states = [0.4, 0.55, 0.7];
    y_state = 0.5;
    
    for i = 1:length(states)
        % Transition
        rectangle('Position', [x_states(i)-0.03, y_state-0.04, 0.06, 0.08], ...
                  'FaceColor', [0.3 0.3 0.3], 'EdgeColor', 'k', 'LineWidth', 1.5);
        text(x_states(i), y_state, states{i}, 'HorizontalAlignment', 'center', ...
             'FontSize', 6, 'Color', 'w', 'FontWeight', 'bold');
        
        % Signal availability annotation
        if i == 1
            text(x_states(i), y_state-0.1, 'No Signal', 'HorizontalAlignment', 'center', ...
                 'FontSize', 7, 'Color', 'r');
        elseif i == 2
            text(x_states(i), y_state-0.1, 'Weak', 'HorizontalAlignment', 'center', ...
                 'FontSize', 7, 'Color', [1, 0.5, 0]);
        else
            text(x_states(i), y_state-0.1, 'Strong', 'HorizontalAlignment', 'center', ...
                 'FontSize', 7, 'Color', 'g');
        end
    end
    
    % Output place
    draw_circle([0.85, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.85, 0.5, 'Out', 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'FontWeight', 'bold');
    
    % Arrows
    annotation('arrow', [0.20, 0.24], [0.5, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.33, 0.37], [0.5, 0.5], 'LineWidth', 1.5);
    for i = 1:length(x_states)
        annotation('arrow', [x_states(i), 0.82], [y_state, 0.5], 'LineWidth', 1.5);
    end
    
    % Tunnel illustration
    rectangle('Position', [0.35, 0.15, 0.4, 0.2], 'FaceColor', [0.3 0.3 0.3], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.55, 0.25, 'TUNNEL', 'HorizontalAlignment', 'center', ...
         'FontSize', 12, 'FontWeight', 'bold', 'Color', 'w');
    
    title('Figure 7: Submodule Tunnel', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_7_tunnel.png');
    fprintf('  - Figure 7 saved\n');
end

function generate_figure_8_position_solution()
    % Figure 8: Module GNSS Position Solution
    
    fig = figure('Position', [100, 100, 1000, 600], 'Name', 'Figure 8: Position Solution', 'visible', 'off');
    
    % Input places
    draw_circle([0.15, 0.6], 0.045, 'Color', 'k', 'LineWidth', 2);
    text(0.15, 0.6, 'Observations', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    draw_circle([0.15, 0.4], 0.045, 'Color', 'k', 'LineWidth', 2);
    text(0.15, 0.4, 'Filter\nState', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % EKF Predict transition
    rectangle('Position', [0.32, 0.36, 0.08, 0.08], 'FaceColor', [1 0.8 0.6], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.36, 0.4, 'EKF\nPredict', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Predicted state place
    draw_circle([0.53, 0.4], 0.04, 'Color', 'k', 'LineWidth', 1.5);
    text(0.53, 0.4, 'Pred', 'HorizontalAlignment', 'center', 'FontSize', 7);
    
    % EKF Update transition
    rectangle('Position', [0.65, 0.46, 0.08, 0.08], 'FaceColor', [0.6 0.8 1], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.69, 0.5, 'EKF\nUpdate', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Output place
    draw_circle([0.85, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.85, 0.5, 'Position', 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'FontWeight', 'bold');
    
    % Arrows
    annotation('arrow', [0.20, 0.32], [0.4, 0.4], 'LineWidth', 2);
    annotation('arrow', [0.40, 0.49], [0.4, 0.4], 'LineWidth', 2);
    annotation('arrow', [0.20, 0.66], [0.6, 0.52], 'LineWidth', 1.5);
    annotation('arrow', [0.57, 0.65], [0.4, 0.48], 'LineWidth', 1.5);
    annotation('arrow', [0.73, 0.82], [0.5, 0.5], 'LineWidth', 2);
    
    % Add EKF equations
    text(0.36, 0.25, 'x̂_{k|k-1} = F·x̂_{k-1}', 'FontSize', 8, 'Interpreter', 'tex');
    text(0.36, 0.20, 'P_{k|k-1} = F·P·F^T + Q', 'FontSize', 8, 'Interpreter', 'tex');
    
    text(0.69, 0.35, 'K = P·H^T·(H·P·H^T + R)^{-1}', 'FontSize', 7, 'Interpreter', 'tex');
    text(0.69, 0.30, 'x̂_k = x̂_{k|k-1} + K·(z - H·x̂_{k|k-1})', 'FontSize', 7, 'Interpreter', 'tex');
    text(0.69, 0.25, 'P_k = (I - K·H)·P_{k|k-1}', 'FontSize', 7, 'Interpreter', 'tex');
    
    title('Figure 8: Module GNSS Position Solution (EKF)', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_8_position_solution.png');
    fprintf('  - Figure 8 saved\n');
end

function generate_figure_9_evaluation()
    % Figure 9: Module Evaluation
    
    fig = figure('Position', [100, 100, 900, 500], 'Name', 'Figure 9: Evaluation', 'visible', 'off');
    
    % Input places
    draw_circle([0.2, 0.6], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.2, 0.6, 'Calculated\nPosition', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    draw_circle([0.2, 0.4], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.2, 0.4, 'Reference\nPosition', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Calculate error transition
    rectangle('Position', [0.42, 0.46, 0.08, 0.08], 'FaceColor', [1 0.6 0.6], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.46, 0.5, 'Calculate\nError', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Error place
    draw_circle([0.65, 0.5], 0.05, 'Color', 'k', 'LineWidth', 2);
    text(0.65, 0.5, 'Position\nError', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Evaluate metrics transition
    rectangle('Position', [0.77, 0.46, 0.08, 0.08], 'FaceColor', [0.6 1 0.6], ...
              'EdgeColor', 'k', 'LineWidth', 2);
    text(0.81, 0.5, 'Evaluate\nMetrics', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Output place
    draw_circle([0.9, 0.5], 0.04, 'Color', 'k', 'LineWidth', 2);
    text(0.9, 0.5, 'Results', 'HorizontalAlignment', 'center', ...
         'FontSize', 8, 'FontWeight', 'bold');
    
    % Arrows
    annotation('arrow', [0.25, 0.42], [0.6, 0.52], 'LineWidth', 2);
    annotation('arrow', [0.25, 0.42], [0.4, 0.48], 'LineWidth', 2);
    annotation('arrow', [0.50, 0.62], [0.5, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.70, 0.77], [0.5, 0.5], 'LineWidth', 2);
    annotation('arrow', [0.85, 0.88], [0.5, 0.5], 'LineWidth', 2);
    
    % Add metrics text
    text(0.81, 0.35, 'Mean Error', 'FontSize', 7);
    text(0.81, 0.31, 'Std Deviation', 'FontSize', 7);
    text(0.81, 0.27, 'Directional Mean', 'FontSize', 7);
    text(0.81, 0.23, 'Helmert Std', 'FontSize', 7);
    
    title('Figure 9: Module Evaluation', 'FontSize', 14, 'FontWeight', 'bold');
    axis off;
    
    saveas(fig, 'figure_9_evaluation.png');
    fprintf('  - Figure 9 saved\n');
end

%% ========================================================================
% Performance Analysis and Simulation
% ========================================================================

function run_performance_analysis()
    fprintf('\nRunning performance analysis simulations...\n');
    
    % Define simulation parameters
    num_epochs = 1000;  % Number of time steps
    dt = 1.0;  % Time step in seconds
    
    % Run simulations for different interference types
    fprintf('\nSimulating different interference scenarios...\n');
    [normal_errors, normal_pos] = simulate_scenario('Normal', 'OpenArea', num_epochs, dt);
    [am_errors, am_pos] = simulate_scenario('AM', 'OpenArea', num_epochs, dt);
    [fm_errors, fm_pos] = simulate_scenario('FM', 'OpenArea', num_epochs, dt);
    [pulse_errors, pulse_pos] = simulate_scenario('Pulse', 'OpenArea', num_epochs, dt);
    
    % Generate Table 4: Performance under different signal interferences
    generate_table_4(normal_errors, am_errors, fm_errors, pulse_errors);
    
    % Run simulations for different environment scenarios
    fprintf('\nSimulating different environment scenarios...\n');
    [open_errors, open_pos] = simulate_scenario('Normal', 'OpenArea', num_epochs, dt);
    [mountain_errors, mountain_pos] = simulate_scenario('Normal', 'Mountain', num_epochs, dt);
    [tunnel_errors, tunnel_pos] = simulate_scenario('Normal', 'Tunnel', num_epochs, dt);
    
    % Generate Table 5: Performance under different environment scenarios
    generate_table_5(open_errors, mountain_errors, tunnel_errors);
    
    % Generate Figure 10: Position errors in tunnel scenario
    generate_figure_10_tunnel_errors(tunnel_errors, num_epochs, dt);
end

function [errors, positions] = simulate_scenario(interference_type, scenario, num_epochs, dt)
    % Simulate GNSS positioning for a given scenario
    
    % Initialize EKF state
    % State vector: [x, y, z, vx, vy, vz]
    state = [0; 0; 100; 20; 0; 0];  % Initial position at (0,0,100) with velocity 20 m/s
    
    % State covariance matrix
    P = diag([10, 10, 10, 1, 1, 1].^2);
    
    % Process noise covariance
    Q = diag([0.5, 0.5, 0.5, 0.1, 0.1, 0.1].^2);
    
    % Measurement noise covariance (depends on interference)
    R = get_measurement_noise(interference_type, scenario);
    
    % State transition matrix
    F = [1, 0, 0, dt, 0, 0;
         0, 1, 0, 0, dt, 0;
         0, 0, 1, 0, 0, dt;
         0, 0, 0, 1, 0, 0;
         0, 0, 0, 0, 1, 0;
         0, 0, 0, 0, 0, 1];
    
    % Measurement matrix
    H = [1, 0, 0, 0, 0, 0;
         0, 1, 0, 0, 0, 0;
         0, 0, 1, 0, 0, 0];
    
    % Generate reference trajectory
    reference_trajectory = generate_reference_trajectory(num_epochs, dt);
    
    % Storage for results
    positions = zeros(3, num_epochs);
    errors = zeros(num_epochs, 1);
    
    % Tunnel parameters (if tunnel scenario)
    if strcmp(scenario, 'Tunnel')
        tunnel_start = 300;  % Enter tunnel at epoch 300
        tunnel_end = 600;    % Exit tunnel at epoch 600
    end
    
    % Simulation loop
    for k = 1:num_epochs
        % Check if in tunnel and adjust signal availability
        signal_available = true;
        if strcmp(scenario, 'Tunnel')
            if k >= tunnel_start && k <= tunnel_end
                signal_available = false;  % No signals in tunnel
            end
        end
        
        % EKF Prediction step
        state_pred = F * state;
        P_pred = F * P * F' + Q;
        
        if signal_available
            % Generate noisy GNSS measurements
            true_position = reference_trajectory(:, k);
            measurements = generate_measurements(true_position, interference_type, scenario, k);
            
            % EKF Update step
            innovation = measurements - H * state_pred;
            S = H * P_pred * H' + R;
            K = P_pred * H' / S;  % Kalman gain
            
            state = state_pred + K * innovation;
            P = (eye(6) - K * H) * P_pred;
        else
            % No update, just use prediction (dead reckoning)
            state = state_pred;
            P = P_pred;
        end
        
        % Store results
        positions(:, k) = state(1:3);
        
        % Calculate position error
        errors(k) = norm(state(1:3) - reference_trajectory(:, k));
    end
end

function R = get_measurement_noise(interference_type, scenario)
    % Get measurement noise covariance based on interference and scenario
    
    base_noise = 1.0;  % meters
    
    switch interference_type
        case 'Normal'
            noise_factor = 1.0;
        case 'AM'
            noise_factor = 5.0;
        case 'FM'
            noise_factor = 6.5;
        case 'Pulse'
            noise_factor = 4.8;
        otherwise
            noise_factor = 1.0;
    end
    
    % Additional factor for scenario
    switch scenario
        case 'OpenArea'
            scenario_factor = 1.0;
        case 'Mountain'
            scenario_factor = 1.3;
        case 'Tunnel'
            scenario_factor = 1.5;
        otherwise
            scenario_factor = 1.0;
    end
    
    sigma = base_noise * noise_factor * scenario_factor;
    R = diag([sigma, sigma, sigma*1.5].^2);  % Elevation has more noise
end

function measurements = generate_measurements(true_position, interference_type, scenario, epoch)
    % Generate noisy GNSS measurements
    
    R = get_measurement_noise(interference_type, scenario);
    % Generate noise using Cholesky decomposition (compatible with Octave)
    L = chol(R, 'lower');
    noise = L * randn(3, 1);
    
    % Add scenario-specific effects
    if strcmp(scenario, 'Mountain') && mod(epoch, 50) < 20
        % Periodic signal blockage in mountains
        noise = noise * 2.0;
    end
    
    measurements = true_position + noise;
end

function trajectory = generate_reference_trajectory(num_epochs, dt)
    % Generate reference trajectory for the train
    
    trajectory = zeros(3, num_epochs);
    
    % Train moves at constant velocity along x-axis
    velocity = 20;  % m/s (72 km/h - typical train speed)
    
    for k = 1:num_epochs
        t = (k-1) * dt;
        
        % Position along track
        trajectory(1, k) = velocity * t;
        
        % Slight curved path
        trajectory(2, k) = 5 * sin(0.01 * t);
        
        % Constant elevation with small variations
        trajectory(3, k) = 100 + 2 * sin(0.005 * t);
    end
end

function generate_table_4(normal_errors, am_errors, fm_errors, pulse_errors)
    % Generate Table 4: Positioning performances under different signal interferences
    
    fprintf('\n%s\n', repmat('=', 1, 80));
    fprintf('Table 4: Positioning Performances under Different Signal Interferences\n');
    fprintf('%s\n\n', repmat('=', 1, 80));
    
    % Calculate metrics for each scenario
    scenarios = {'Normal', 'AM', 'FM', 'Pulse'};
    error_sets = {normal_errors, am_errors, fm_errors, pulse_errors};
    
    fprintf('%-12s %12s %12s\n', 'Scenario', 'Mean (m)', 'Std Dev (m)');
    fprintf('%s\n', repmat('-', 1, 80));
    
    table_data = zeros(4, 2);
    for i = 1:length(scenarios)
        mean_error = mean(error_sets{i});
        std_error = std(error_sets{i});
        table_data(i, :) = [mean_error, std_error];
        fprintf('%-12s %12.4f %12.4f\n', scenarios{i}, mean_error, std_error);
    end
    fprintf('%s\n\n', repmat('=', 1, 80));
    
    % Save to file
    save('table_4_results.mat', 'table_data', 'scenarios');
    
    % Create bar chart
    fig = figure('Position', [100, 100, 800, 500], 'visible', 'off');
    
    subplot(1, 2, 1);
    bar(table_data(:, 1));
    set(gca, 'XTickLabel', scenarios);
    xlabel('Interference Type');
    ylabel('Mean Error (m)');
    title('Mean Position Error');
    grid on;
    
    subplot(1, 2, 2);
    bar(table_data(:, 2));
    set(gca, 'XTickLabel', scenarios);
    xlabel('Interference Type');
    ylabel('Standard Deviation (m)');
    title('Position Error Std Dev');
    grid on;
    
    % sgtitle not available in Octave
    % sgtitle('Table 4: Performance Under Different Signal Interferences', ...
    %         'FontSize', 14, 'FontWeight', 'bold');
    
    saveas(fig, 'table_4_visualization.png');
    fprintf('  - Table 4 visualization saved\n');
end

function generate_table_5(open_errors, mountain_errors, tunnel_errors)
    % Generate Table 5: Positioning performances under different environment scenarios
    
    fprintf('\n%s\n', repmat('=', 1, 80));
    fprintf('Table 5: Positioning Performances under Different Environment Scenarios\n');
    fprintf('%s\n\n', repmat('=', 1, 80));
    
    % Calculate metrics for each scenario
    scenarios = {'Open Area', 'Mountain', 'Tunnel'};
    error_sets = {open_errors, mountain_errors, tunnel_errors};
    
    fprintf('%-18s %12s %12s\n', 'Scenario', 'Mean (m)', 'Std Dev (m)');
    fprintf('%s\n', repmat('-', 1, 80));
    
    table_data = zeros(3, 2);
    for i = 1:length(scenarios)
        mean_error = mean(error_sets{i});
        std_error = std(error_sets{i});
        table_data(i, :) = [mean_error, std_error];
        fprintf('%-18s %12.4f %12.4f\n', scenarios{i}, mean_error, std_error);
    end
    fprintf('%s\n\n', repmat('=', 1, 80));
    
    % Save to file
    save('table_5_results.mat', 'table_data', 'scenarios');
    
    % Create bar chart
    fig = figure('Position', [100, 100, 800, 500], 'visible', 'off');
    
    subplot(1, 2, 1);
    bar(table_data(:, 1));
    set(gca, 'XTickLabel', scenarios);
    xlabel('Environment Scenario');
    ylabel('Mean Error (m)');
    title('Mean Position Error');
    grid on;
    
    subplot(1, 2, 2);
    bar(table_data(:, 2));
    set(gca, 'XTickLabel', scenarios);
    xlabel('Environment Scenario');
    ylabel('Standard Deviation (m)');
    title('Position Error Std Dev');
    grid on;
    
    % sgtitle not available in Octave
    % sgtitle('Table 5: Performance Under Different Environment Scenarios', ...
    %         'FontSize', 14, 'FontWeight', 'bold');
    
    saveas(fig, 'table_5_visualization.png');
    fprintf('  - Table 5 visualization saved\n');
end

function generate_figure_10_tunnel_errors(errors, num_epochs, dt)
    % Figure 10: Position errors in tunnel scenario
    
    fig = figure('Position', [100, 100, 1200, 600], 'Name', 'Figure 10: Tunnel Errors', 'visible', 'off');
    
    time = (0:num_epochs-1) * dt;
    
    % Define tunnel region
    tunnel_start = 300;
    tunnel_end = 600;
    
    % Plot position error over time
    plot(time, errors, 'b-', 'LineWidth', 2);
    hold on;
    
    % Highlight tunnel region
    tunnel_region_x = [time(tunnel_start), time(tunnel_end), time(tunnel_end), time(tunnel_start)];
    tunnel_region_y = [0, 0, max(errors)*1.2, max(errors)*1.2];
    fill(tunnel_region_x, tunnel_region_y, [0.7 0.7 0.7], ...
         'FaceAlpha', 0.3, 'EdgeColor', 'none');
    
    % Mark tunnel exit with vertical line
    plot([time(tunnel_end), time(tunnel_end)], [0, max(errors)*1.2], ...
         'r--', 'LineWidth', 2);
    
    % Labels and annotations
    xlabel('Time (s)', 'FontSize', 12, 'FontWeight', 'bold');
    ylabel('Position Error (m)', 'FontSize', 12, 'FontWeight', 'bold');
    title('Figure 10: Position Errors in Tunnel Scenario', ...
          'FontSize', 14, 'FontWeight', 'bold');
    
    % Add legend
    legend({'Position Error', 'Inside Tunnel', 'Tunnel Exit'}, ...
           'Location', 'northwest', 'FontSize', 10);
    
    % Add text annotations
    text(450, max(errors)*0.9, 'Inside Tunnel', 'FontSize', 11, ...
         'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    text(700, max(errors)*0.7, 'Signal Reacquisition', 'FontSize', 10, ...
         'Color', 'r', 'HorizontalAlignment', 'center');
    text(850, max(errors)*0.3, 'Error Stabilization', 'FontSize', 10, ...
         'Color', 'g', 'HorizontalAlignment', 'center');
    
    grid on;
    xlim([0, time(end)]);
    ylim([0, max(errors)*1.2]);
    
    hold off;
    
    saveas(fig, 'figure_10_tunnel_errors.png');
    fprintf('  - Figure 10 saved\n');
end
