# src/artigen/__init__.py

from .example import add_one  # existing import
from .submodule1 import sub1  # new import
from .submodule2 import sub2  # new import

__all__ = ['add_one', 'sub1', 'sub2']  # Update this list as needed