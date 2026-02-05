"""
Extended cardinality estimation algorithms with demographic tracking
"""

from .extended_hyperloglog import ExtendedHyperLogLogSketch
from .extended_hyperreal import ExtendedHyperRealSketch

__all__ = [
    'ExtendedHyperLogLogSketch',
    'ExtendedHyperRealSketch'
]