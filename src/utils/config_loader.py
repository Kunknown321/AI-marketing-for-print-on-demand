"""Load and validate business configuration."""

import os
from pathlib import Path

import yaml


CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"


def load_business_profile(config_path: str | None = None) -> dict:
    """Load the business profile configuration.

    Args:
        config_path: Optional path to config file. Defaults to config/business_profile.yaml.

    Returns:
        Business profile dictionary.
    """
    if config_path is None:
        config_path = str(CONFIG_DIR / "business_profile.yaml")

    with open(config_path) as f:
        return yaml.safe_load(f)


def get_profile_section(section: str, config_path: str | None = None) -> dict:
    """Get a specific section from the business profile.

    Args:
        section: Section name (e.g., 'business', 'target_audience', 'niche').
        config_path: Optional path to config file.

    Returns:
        Section dictionary.
    """
    profile = load_business_profile(config_path)
    return profile.get(section, {})
