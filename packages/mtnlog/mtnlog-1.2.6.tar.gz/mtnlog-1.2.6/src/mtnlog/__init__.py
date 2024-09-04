import importlib.metadata

from .json import *
from .performance import *
from .plot import *

__version__ = importlib.metadata.version('mtnlog')

__doc__ = """Performance logger for tracking resource usage."""

__all__ = [
    'JSONLogger',
    'PerformanceLogger',
    'PerformancePlotter',
]
