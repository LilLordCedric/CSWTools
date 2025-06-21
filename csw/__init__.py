"""
Yggdrasil Tree - A flexible tree-like data structure for Python.

This package provides the Yggdrasil class, which extends Python's built-in dict
to create a tree-like data structure with automatic creation of nested dictionaries
and customizable leaf node behaviors.
"""

from .yggdrasil import Yggdrasil

__version__ = '0.1.0'
__all__ = ['Yggdrasil']