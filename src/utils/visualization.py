"""
Visualization Module

This module provides plotting and visualization functions for
simulation results, matching the figures in the paper.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Optional
from ..cpn.tokens import Scenario, StateInterference


# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


def plot_positioning_errors(
    results: Dict,
    output_file: str = None,
    title: str = "Positioning Errors Over Time"
):
    """
    Plot positioning errors over time.
    
    Args:
        results: Simulation results dictionary
        output_file: Output file path (optional)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    timestamps = results['timestamps']
    errors = [e.error_distance for e in results['errors']]
    
    ax.plot(timestamps, errors, 'b-', linewidth=1, alpha=0.7)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Positioning Error (meters)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    # Add mean and std lines
    mean_error = np.mean(errors)
    std_error = np.std(errors)
    ax.axhline(mean_error, color='r', linestyle='--', 
               label=f'Mean: {mean_error:.2f} m')
    ax.axhline(mean_error + std_error, color='g', linestyle=':', 
               label=f'Mean + Std: {mean_error + std_error:.2f} m')
    ax.axhline(mean_error - std_error, color='g', linestyle=':', 
               label=f'Mean - Std: {mean_error - std_error:.2f} m')
    
    ax.legend()
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_error_components(
    results: Dict,
    output_file: str = None,
    title: str = "Error Components (East, North, Up)"
):
    """
    Plot error components in three directions.
    
    Args:
        results: Simulation results dictionary
        output_file: Output file path (optional)
        title: Plot title
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    timestamps = results['timestamps']
    errors = results['errors']
    
    error_east = [e.error_east for e in errors if e.error_east is not None]
    error_north = [e.error_north for e in errors if e.error_north is not None]
    error_up = [e.error_up for e in errors if e.error_up is not None]
    
    if len(error_east) > 0:
        axes[0].plot(timestamps[:len(error_east)], error_east, 'b-', linewidth=1)
        axes[0].set_ylabel('East Error (m)')
        axes[0].set_title('East Component')
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(0, color='k', linestyle='-', linewidth=0.5)
        
        axes[1].plot(timestamps[:len(error_north)], error_north, 'g-', linewidth=1)
        axes[1].set_ylabel('North Error (m)')
        axes[1].set_title('North Component')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(0, color='k', linestyle='-', linewidth=0.5)
        
        axes[2].plot(timestamps[:len(error_up)], error_up, 'r-', linewidth=1)
        axes[2].set_ylabel('Up Error (m)')
        axes[2].set_title('Up Component')
        axes[2].set_xlabel('Time (seconds)')
        axes[2].grid(True, alpha=0.3)
        axes[2].axhline(0, color='k', linestyle='-', linewidth=0.5)
    
    plt.suptitle(title)
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_scenario_comparison(
    results_dict: Dict[str, Dict],
    output_file: str = None,
    title: str = "Positioning Performance by Scenario"
):
    """
    Compare positioning performance across different scenarios.
    
    Args:
        results_dict: Dictionary of {scenario_name: results}
        output_file: Output file path (optional)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scenarios = list(results_dict.keys())
    mean_errors = []
    std_errors = []
    
    for scenario_name, results in results_dict.items():
        errors = [e.error_distance for e in results['errors']]
        mean_errors.append(np.mean(errors))
        std_errors.append(np.std(errors))
    
    x = np.arange(len(scenarios))
    ax.bar(x, mean_errors, yerr=std_errors, capsize=5, alpha=0.7)
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Mean Positioning Error (m)')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def plot_interference_comparison(
    results_dict: Dict[str, Dict],
    output_file: str = None,
    title: str = "Positioning Performance by Interference Type"
):
    """
    Compare positioning performance under different interferences.
    
    Args:
        results_dict: Dictionary of {interference_name: results}
        output_file: Output file path (optional)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    interference_types = list(results_dict.keys())
    mean_errors = []
    std_errors = []
    
    for interference_name, results in results_dict.items():
        errors = [e.error_distance for e in results['errors']]
        mean_errors.append(np.mean(errors))
        std_errors.append(np.std(errors))
    
    x = np.arange(len(interference_types))
    colors = ['green', 'orange', 'red', 'purple'][:len(interference_types)]
    
    ax.bar(x, mean_errors, yerr=std_errors, capsize=5, alpha=0.7, color=colors)
    ax.set_xlabel('Interference Type')
    ax.set_ylabel('Mean Positioning Error (m)')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(interference_types, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (mean, std) in enumerate(zip(mean_errors, std_errors)):
        ax.text(i, mean + std + 0.2, f'{mean:.2f}±{std:.2f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def create_results_table(
    results_dict: Dict[str, Dict],
    output_file: str = None
) -> str:
    """
    Create a formatted table of results matching Table 4 in the paper.
    
    Args:
        results_dict: Dictionary of {scenario_name: results}
        output_file: Output file path for saving table (optional)
        
    Returns:
        Formatted table string
    """
    table_lines = []
    table_lines.append("=" * 100)
    table_lines.append(f"{'Scenario':<20} {'Mean Error':<15} {'Std Dev':<15} {'Min Error':<15} {'Max Error':<15}")
    table_lines.append("=" * 100)
    
    for scenario_name, results in results_dict.items():
        errors = np.array([e.error_distance for e in results['errors']])
        
        mean_error = np.mean(errors)
        std_error = np.std(errors)
        min_error = np.min(errors)
        max_error = np.max(errors)
        
        table_lines.append(
            f"{scenario_name:<20} {mean_error:<15.4f} {std_error:<15.4f} "
            f"{min_error:<15.4f} {max_error:<15.4f}"
        )
    
    table_lines.append("=" * 100)
    
    table_str = "\n".join(table_lines)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(table_str)
    
    return table_str


def plot_trajectory_2d(
    reference_trajectory: List,
    estimated_trajectory: List,
    output_file: str = None,
    title: str = "2D Trajectory Comparison"
):
    """
    Plot 2D trajectory comparison.
    
    Args:
        reference_trajectory: List of reference positions
        estimated_trajectory: List of estimated positions
        output_file: Output file path (optional)
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Extract coordinates
    ref_x = [p.x for p in reference_trajectory]
    ref_y = [p.y for p in reference_trajectory]
    
    est_x = [p.position.x for p in estimated_trajectory]
    est_y = [p.position.y for p in estimated_trajectory]
    
    ax.plot(ref_x, ref_y, 'b-', linewidth=2, label='Reference', alpha=0.7)
    ax.plot(est_x, est_y, 'r--', linewidth=1.5, label='Estimated', alpha=0.7)
    
    # Mark start and end points
    ax.plot(ref_x[0], ref_y[0], 'go', markersize=10, label='Start')
    ax.plot(ref_x[-1], ref_y[-1], 'ro', markersize=10, label='End')
    
    ax.set_xlabel('Easting (m)')
    ax.set_ylabel('Northing (m)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def generate_all_plots(
    results: Dict,
    output_dir: str = "results/figures"
):
    """
    Generate all plots for the simulation results.
    
    Args:
        results: Simulation results dictionary
        output_dir: Output directory for saving plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Plot positioning errors
    plot_positioning_errors(
        results,
        output_file=str(output_path / "positioning_errors.png")
    )
    
    # Plot error components
    plot_error_components(
        results,
        output_file=str(output_path / "error_components.png")
    )
    
    print(f"Plots saved to {output_dir}")
