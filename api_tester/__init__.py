"""
API Tester Tool
A simple tool for testing APIs with JSON files.
"""

__version__ = "1.0.0"
__author__ = "FWB"
__email__ = "Wenbin.Feng@ieee.org"

from .main import test_api
from .utils.get_res import get_response_data

__all__ = ['test_api', 'get_response_data']