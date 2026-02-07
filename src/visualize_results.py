"""
Visualization Script for GNSS Train Positioning Results
Generates plots matching the paper's figures
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import sys

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def load_results(results_file: str) -> dict:
    """Load simulation results from JSON file"""
    with open(results_file, 'r') as f:
        return json.load(f)


def plot_interference_comparison(results: dict, output_dir: str):
    """
    Plot comparison of positioning errors under different interference scenarios
    Matches Table 4 analysis
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Positioning Performance Under Different Signal Interferences', 
                 fontsize=14, fontweight='bold')
    
    scenarios = ['Normal', 'AM', 'FM', 'Pulse']
    colors = ['green', 'blue', 'orange', 'red']
    
    for idx, (scenario_key, scenario_name, color) in enumerate(zip(
        ['Normal', 'AM', 'FM', 'Pulse'], scenarios, colors
    )):
        ax = axes[idx // 2, idx % 2]
        
        if scenario_key in results['interference_scenarios']:
            data = results['interference_scenarios'][scenario_key]
            errors = data['errors']
            stats = data['statistics']
            
            # Plot error time series
            ax.plot(range(len(errors)), errors, color=color, alpha=0.7, linewidth=1)
            ax.axhline(y=stats['mean_error'], color='red', linestyle='--', 
                      label=f"Mean: {stats['mean_error']:.2f} m")
            ax.fill_between(range(len(errors)), 
                           stats['mean_error'] - stats['std_deviation'],
                           stats['mean_error'] + stats['std_deviation'],
                           alpha=0.2, color=color, 
                           label=f"±1σ: {stats['std_deviation']:.2f} m")
            
            ax.set_title(f'{scenario_name} Interference', fontweight='bold')
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Position Error (m)')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'interference_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: interference_comparison.png")
    plt.close()


def plot_interference_statistics(results: dict, output_dir: str):
    """
    Bar chart comparing statistics across interference types
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Statistical Comparison of Interference Effects', 
                 fontsize=14, fontweight='bold')
    
    scenarios = []
    mean_errors = []
    std_devs = []
    
    for key in ['Normal', 'AM', 'FM', 'Pulse']:
        if key in results['interference_scenarios']:
            data = results['interference_scenarios'][key]
            scenarios.append(key)
            mean_errors.append(data['statistics']['mean_error'])
            std_devs.append(data['statistics']['std_deviation'])
    
    x = np.arange(len(scenarios))
    width = 0.6
    
    # Mean error bars
    bars1 = ax1.bar(x, mean_errors, width, 
                    color=['green', 'blue', 'orange', 'red'][:len(scenarios)],
                    alpha=0.7)
    ax1.set_xlabel('Interference Type')
    ax1.set_ylabel('Mean Position Error (m)')
    ax1.set_title('Mean Error Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}m',
                ha='center', va='bottom')
    
    # Std deviation bars
    bars2 = ax2.bar(x, std_devs, width,
                    color=['green', 'blue', 'orange', 'red'][:len(scenarios)],
                    alpha=0.7)
    ax2.set_xlabel('Interference Type')
    ax2.set_ylabel('Standard Deviation (m)')
    ax2.set_title('Standard Deviation Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenarios)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}m',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'interference_statistics.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: interference_statistics.png")
    plt.close()


def plot_environment_comparison(results: dict, output_dir: str):
    """
    Plot comparison of positioning errors under different environment scenarios
    Matches Table 5 analysis
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Positioning Performance Under Different Environment Scenarios', 
                 fontsize=14, fontweight='bold')
    
    scenarios = [
        ('OpenArea', 'Open Area', 'green'),
        ('Mountain', 'Mountain Occlusion', 'brown'),
        ('Tunnel', 'Tunnel', 'darkblue')
    ]
    
    for idx, (scenario_key, scenario_name, color) in enumerate(scenarios):
        if scenario_key in results['environment_scenarios']:
            ax = axes[idx]
            data = results['environment_scenarios'][scenario_key]
            errors = data['errors']
            stats = data['statistics']
            
            # Plot error time series
            ax.plot(range(len(errors)), errors, color=color, alpha=0.7, linewidth=1)
            ax.axhline(y=stats['mean_error'], color='red', linestyle='--',
                      label=f"Mean: {stats['mean_error']:.2f} m")
            ax.fill_between(range(len(errors)),
                           stats['mean_error'] - stats['std_deviation'],
                           stats['mean_error'] + stats['std_deviation'],
                           alpha=0.2, color=color,
                           label=f"±1σ: {stats['std_deviation']:.2f} m")
            
            ax.set_title(scenario_name, fontweight='bold')
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Position Error (m)')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'environment_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: environment_comparison.png")
    plt.close()


def plot_tunnel_scenario_detail(results: dict, output_dir: str):
    """
    Plot detailed tunnel scenario analysis
    Matches Figure 10 in the paper
    """
    if 'Tunnel' not in results['environment_scenarios']:
        print("  Warning: No tunnel scenario data found")
        return
    
    data = results['environment_scenarios']['Tunnel']
    errors = data['errors']
    timestamps = data.get('timestamps', list(range(len(errors))))
    tunnel_entry = data.get('tunnel_entry', 200)
    tunnel_exit = data.get('tunnel_exit', 300)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot error evolution
    ax.plot(timestamps, errors, color='darkblue', linewidth=2, label='Position Error')
    
    # Mark tunnel phases
    # Inside tunnel (gray shaded region)
    ax.axvspan(tunnel_entry, tunnel_exit, alpha=0.3, color='gray', 
              label='Inside Tunnel (Signal Loss)')
    
    # Tunnel exit marker
    ax.axvline(x=tunnel_exit, color='red', linestyle='--', linewidth=2,
              label='Tunnel Exit')
    
    # Add text annotations
    ax.text(tunnel_entry + (tunnel_exit - tunnel_entry)/2, ax.get_ylim()[1] * 0.9,
           'Signal Blocked', ha='center', va='center', fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.text(tunnel_exit + 20, ax.get_ylim()[1] * 0.8,
           'Signal Reacquisition\n(High Errors)', ha='left', va='center', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    
    ax.set_title('Position Error Evolution in Tunnel Scenario (Figure 10)', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Position Error (m)', fontsize=12)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'tunnel_scenario_detail.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: tunnel_scenario_detail.png")
    plt.close()


def plot_environment_statistics(results: dict, output_dir: str):
    """
    Bar chart comparing environment scenario statistics
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Statistical Comparison of Environment Scenarios', 
                 fontsize=14, fontweight='bold')
    
    scenarios = []
    mean_errors = []
    std_devs = []
    
    for key in ['OpenArea', 'Mountain', 'Tunnel']:
        if key in results['environment_scenarios']:
            data = results['environment_scenarios'][key]
            scenarios.append(data['description'])
            mean_errors.append(data['statistics']['mean_error'])
            std_devs.append(data['statistics']['std_deviation'])
    
    x = np.arange(len(scenarios))
    width = 0.6
    colors = ['green', 'brown', 'darkblue'][:len(scenarios)]
    
    # Mean error bars
    bars1 = ax1.bar(x, mean_errors, width, color=colors, alpha=0.7)
    ax1.set_xlabel('Environment Scenario')
    ax1.set_ylabel('Mean Position Error (m)')
    ax1.set_title('Mean Error Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios)
    ax1.grid(True, alpha=0.3, axis='y')
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}m',
                ha='center', va='bottom')
    
    # Std deviation bars
    bars2 = ax2.bar(x, std_devs, width, color=colors, alpha=0.7)
    ax2.set_xlabel('Environment Scenario')
    ax2.set_ylabel('Standard Deviation (m)')
    ax2.set_title('Standard Deviation Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenarios)
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}m',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'environment_statistics.png'), dpi=300, bbox_inches='tight')
    print(f"  Saved: environment_statistics.png")
    plt.close()


def create_summary_table_image(results: dict, output_dir: str):
    """
    Create images of summary tables matching the paper
    """
    # Table 4: Interference scenarios
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = [['Scenario', 'Mean Error (m)', 'Std Deviation (m)', 'RMS Error (m)']]
    
    for key in ['Normal', 'AM', 'FM', 'Pulse']:
        if key in results['interference_scenarios']:
            data = results['interference_scenarios'][key]
            stats = data['statistics']
            table_data.append([
                data['description'],
                f"{stats['mean_error']:.4f}",
                f"{stats['std_deviation']:.4f}",
                f"{stats['rms_error']:.4f}"
            ])
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.4, 0.2, 0.2, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title('Table 4: Positioning Performance Under Different Signal Interferences',
             fontsize=12, fontweight='bold', pad=20)
    plt.savefig(os.path.join(output_dir, 'table4_interference.png'), 
               dpi=300, bbox_inches='tight')
    print(f"  Saved: table4_interference.png")
    plt.close()
    
    # Table 5: Environment scenarios
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    table_data = [['Scenario', 'Mean Error (m)', 'Std Deviation (m)', 'RMS Error (m)']]
    
    for key in ['OpenArea', 'Mountain', 'Tunnel']:
        if key in results['environment_scenarios']:
            data = results['environment_scenarios'][key]
            stats = data['statistics']
            table_data.append([
                data['description'],
                f"{stats['mean_error']:.4f}",
                f"{stats['std_deviation']:.4f}",
                f"{stats['rms_error']:.4f}"
            ])
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.4, 0.2, 0.2, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(4):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title('Table 5: Positioning Performance Under Different Environment Scenarios',
             fontsize=12, fontweight='bold', pad=20)
    plt.savefig(os.path.join(output_dir, 'table5_environment.png'),
               dpi=300, bbox_inches='tight')
    print(f"  Saved: table5_environment.png")
    plt.close()


def main():
    """Main visualization entry point"""
    print("="*80)
    print("GENERATING VISUALIZATION PLOTS")
    print("="*80)
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_file = os.path.join(script_dir, 'results', 'outputs', 'simulation_results.json')
    output_dir = os.path.join(script_dir, 'results', 'plots')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load results
    print(f"\nLoading results from: {results_file}")
    results = load_results(results_file)
    
    # Generate plots
    print("\nGenerating plots:")
    
    print("\n1. Interference Scenario Plots...")
    plot_interference_comparison(results, output_dir)
    plot_interference_statistics(results, output_dir)
    
    print("\n2. Environment Scenario Plots...")
    plot_environment_comparison(results, output_dir)
    plot_environment_statistics(results, output_dir)
    
    print("\n3. Tunnel Scenario Detail (Figure 10)...")
    plot_tunnel_scenario_detail(results, output_dir)
    
    print("\n4. Summary Tables...")
    create_summary_table_image(results, output_dir)
    
    print("\n" + "="*80)
    print("VISUALIZATION COMPLETED")
    print("="*80)
    print(f"\nAll plots saved to: {output_dir}")
    print("\nGenerated files:")
    print("  - interference_comparison.png")
    print("  - interference_statistics.png")
    print("  - environment_comparison.png")
    print("  - environment_statistics.png")
    print("  - tunnel_scenario_detail.png (Figure 10)")
    print("  - table4_interference.png")
    print("  - table5_environment.png")


if __name__ == "__main__":
    main()
