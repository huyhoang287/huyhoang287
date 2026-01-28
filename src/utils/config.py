"""
Application Configuration
Manages application settings and preferences
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "app_name": "HRSG Weld Management System",
    "version": "2.1",
    "database_path": "database/hrsg_welds.db",
    "log_level": "INFO",
    "theme": "slate-blue",
    "language": "en",
    "window_width": 1400,
    "window_height": 900,
    "remember_window_state": True
}


def load_config():
    """
    Load application configuration

    Returns:
        dict: Configuration dictionary
    """
    config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')

    # Load from file if exists, otherwise use defaults
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info("Configuration loaded from file")
                return {**DEFAULT_CONFIG, **config}  # Merge with defaults
        except Exception as e:
            logger.warning(f"Failed to load config file: {e}. Using defaults.")
            return DEFAULT_CONFIG.copy()
    else:
        logger.info("No config file found. Using default configuration.")
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """
    Save application configuration

    Args:
        config: Configuration dictionary to save
    """
    config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')

    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Failed to save config file: {e}")


def get_config_value(key, default=None):
    """
    Get a specific configuration value

    Args:
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value or default
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key, value):
    """
    Set a specific configuration value

    Args:
        key: Configuration key
        value: Value to set
    """
    config = load_config()
    config[key] = value
    save_config(config)
