"""
Configuration Module

This module handles loading and managing configuration parameters
for the GNSS train positioning CPN simulation.
"""

import yaml
from typing import Dict, Any
from pathlib import Path


# Default configuration
DEFAULT_CONFIG = {
    'simulation': {
        'duration': 600,  # seconds (10 minutes as per paper)
        'time_step': 1.0,  # 1 second per epoch
        'random_seed': 42
    },
    
    'gnss': {
        'min_satellites': 4,
        'max_satellites': 12,
        'carrier_frequency_l1': 1575.42e6,  # Hz
        'speed_of_light': 299792458.0,  # m/s
        'pseudorange_noise_std': 3.0,  # meters
        'elevation_mask': 10.0,  # degrees
    },
    
    'interference': {
        'am': {
            'enabled': True,
            'amplitude': 0.5,
            'frequency': 1.0  # Hz
        },
        'fm': {
            'enabled': True,
            'freq_deviation_std': 75000.0  # Hz
        },
        'pulse': {
            'enabled': True,
            'probability': 0.1,
            'error_std': 10.0  # meters
        }
    },
    
    'scenarios': {
        'open_area': {
            'enabled': True
        },
        'mountain': {
            'enabled': True,
            'height': 500.0,  # meters
            'distance': 1000.0  # meters
        },
        'tunnel': {
            'enabled': True,
            'length': 2000.0  # meters
        }
    },
    
    'ekf': {
        'process_noise': {
            'position': 0.5,  # m
            'velocity': 0.1,  # m/s
            'clock_bias': 1.0,  # m
            'clock_drift': 0.1  # m/s
        },
        'measurement_noise': {
            'pseudorange': 3.0,  # m
            'position': 5.0  # m
        },
        'initial_covariance': {
            'position': 100.0,  # m^2
            'velocity': 10.0,  # m^2/s^2
            'clock_bias': 1000.0,  # m^2
            'clock_drift': 10.0  # m^2/s^2
        }
    },
    
    'train': {
        'initial_velocity': 0.0,  # m/s
        'max_velocity': 83.33,  # m/s (300 km/h)
        'acceleration': 0.5,  # m/s^2
        'deceleration': -0.8  # m/s^2
    },
    
    'output': {
        'save_results': True,
        'results_dir': 'results',
        'figures_dir': 'results/figures',
        'tables_dir': 'results/tables',
        'save_format': ['png', 'pdf']
    }
}


class Config:
    """Configuration manager for the simulation."""
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to YAML configuration file (optional)
        """
        self.config = DEFAULT_CONFIG.copy()
        
        if config_file is not None:
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """
        Load configuration from YAML file.
        
        Args:
            config_file: Path to YAML file
        """
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
        
        # Merge user config with defaults
        self._merge_config(self.config, user_config)
    
    def _merge_config(self, base: Dict, update: Dict):
        """
        Recursively merge two configuration dictionaries.
        
        Args:
            base: Base configuration dictionary
            update: Update configuration dictionary
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Configuration key path (e.g., 'gnss.min_satellites')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Configuration key path (e.g., 'gnss.min_satellites')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save_to_file(self, config_file: str):
        """
        Save configuration to YAML file.
        
        Args:
            config_file: Path to output YAML file
        """
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
    
    def to_dict(self) -> Dict:
        """Return configuration as dictionary."""
        return self.config.copy()
    
    def __repr__(self):
        return f"Config({self.config})"


def load_config(config_file: str = None) -> Config:
    """
    Load configuration from file or use defaults.
    
    Args:
        config_file: Path to configuration file (optional)
        
    Returns:
        Config object
    """
    return Config(config_file)
