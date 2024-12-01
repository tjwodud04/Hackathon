# 1. data_gathering/__init__.py
"""
Data gathering package for real estate data
"""
from pathlib import Path

# Set package root path
PACKAGE_ROOT = Path(__file__).parent

# Make data directory path available
DATA_DIR = PACKAGE_ROOT / 'data'