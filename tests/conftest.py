"""
Pytest configuration for Wylie Transliterator tests.

Automatically configures Python path to find:
1. The wylie_transliterator module (from src/)
2. The pyewts module (from ../../pyewts/)
"""

import sys
from pathlib import Path

# Add src/ to path for wylie_transliterator
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Add parent directory for pyewts
pyewts_path = Path(__file__).parent.parent.parent / "pyewts"
if pyewts_path.exists() and str(pyewts_path) not in sys.path:
    sys.path.insert(0, str(pyewts_path))

# Add parent directory for ACIP module
parent_path = Path(__file__).parent.parent.parent
if str(parent_path) not in sys.path:
    sys.path.insert(0, str(parent_path))

